#!/usr/bin/env python3

import argparse
import hashlib
import json
import logging

import boto3

logging.basicConfig(level=logging.INFO)
for too_noisy in ["boto3", "botocore"]:
    logging.getLogger(too_noisy).setLevel(logging.WARN)
for make_noisy in ["__main__"]:
    logging.getLogger(make_noisy).setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src-profile', required=True, help="Boto profile name for the account containing the parent hosted zone.")
    parser.add_argument('-d', '--dst-profile', required=True, help="Boto profile name for the account in which to create the child hosted zone.")
    parser.add_argument('--name', required=True, help="Parent hosted zone name (e.g., 'example.org')")
    parser.add_argument('--subdomain', required=True, help="Subdomain, to be prepended to the parent name with a . (e.g., 'blog' would result in delegating 'blog.example.org')")
    return parser.parse_args()

def map_by(list_of_dicts, key_key):
    return {d[key_key]:d for d in list_of_dicts}

def dumps(x, title=None):
    title = title or ""
    logger.debug(f"{title}\n"+json.dumps(x, indent=2, sort_keys=True, default=str))

def get_hosted_zone(client, name, throw_if_missing=True):
    response = client.list_hosted_zones_by_name(
        DNSName=name,
        MaxItems="100",
    )
    if response.get("IsTruncated"):
        raise RuntimeError("I haven't bothered to add pagination yet, sorry.")
    zones = response["HostedZones"]
    zone_map = map_by(zones, "Name")
    if name in zone_map:
        return zone_map[name]["Id"]
    if throw_if_missing:
        raise RuntimeError(f"No hosted zone with name {name} found!")
    return None

def get_records(client, zone_id, record_type=None, exclude_types=[], name=None):
    response = client.list_resource_record_sets(
        HostedZoneId=zone_id,
        MaxItems='300'
    )
    if response.get("IsTruncated"):
        raise RuntimeError("I haven't bothered to add pagination yet, sorry.")
    records = response["ResourceRecordSets"]
    if name:
        records = [x for x in records if x["Name"] == name]
    if record_type:
        records = [x for x in records if x["Type"] == record_type]
    if exclude_types:
        records = [x for x in records if x["Type"] not in exclude_types]
    return records

def create_hosted_zone(client, name):
    zone = get_hosted_zone(client, name, throw_if_missing=False)
    if zone:
        logger.info(f"zone {name} already exists: {zone['Id']}")
        return zone["Id"]
    logger.info(f"creating zone {name}")
    response = client.create_hosted_zone(
        Name=name,
        CallerReference=hashlib.sha256(name.encode("utf-8")).hexdigest(),
    )
    zone_id = response["HostedZone"]["Id"]
    logger.info(f"zone {name} created: {zone_id}")
    return zone_id

def create_ns_record(client, zone_id, name, records):
    logger.info(f"Creating NS record for {name} in {zone_id}")
    client.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            'Comment': 'string',
            'Changes': [
                {
                    'Action': 'CREATE',
                    'ResourceRecordSet': {
                        'Name': name,
                        'Type': 'NS',
                        'TTL': 3600,
                        'ResourceRecords': records,
                    }
                },
            ]
        }
    )
    return map_by(get_records(client, zone_id=zone_id, record_type="NS", name=name), "Name")[name]

def main():
    args = parse_args()
    src_sesh = boto3.Session(profile_name=args.src_profile)
    src_client = src_sesh.client("route53")
    dst_sesh = boto3.Session(profile_name=args.dst_profile)
    dst_client = dst_sesh.client("route53")
    dns_name = f"{args.name}."
    dns_subdomain = f"{args.subdomain}.{dns_name}"
    parent_zone_id = get_hosted_zone(src_client, name=dns_name)
    parent_ns_records = map_by(get_records(src_client, zone_id=parent_zone_id, record_type="NS", name=dns_subdomain), "Name")
    child_zone_id = get_hosted_zone(dst_client, name=dns_subdomain, throw_if_missing=False)
    dumps(parent_ns_records)
    if not child_zone_id:
        if dns_subdomain in parent_ns_records:
            raise RuntimeError(f"No hosted zone for {dns_subdomain} found in expected account, but {dns_name} already has an NS record set for it. It may exist in a different account already; aborting to avoid breaking stuff.")
        child_zone_id = create_hosted_zone(dst_client, name=dns_subdomain)
    child_ns_record = map_by(get_records(dst_client, zone_id=child_zone_id, record_type="NS"), "Name")[dns_subdomain]
    dumps(child_ns_record, "Child NS record:")
    if dns_subdomain not in parent_ns_records:
        parent_ns_record = create_ns_record(src_client, zone_id=parent_zone_id, name=dns_subdomain, records=child_ns_record["ResourceRecords"])
        dumps(parent_ns_record, "Parent NS record:")
    else:
        dumps(parent_ns_records[dns_subdomain], "Parent NS record:")
        canonicalize = lambda l: ", ".join(sorted([x["Value"] for x in l["ResourceRecords"]]))
        parent_values = canonicalize(parent_ns_records[dns_subdomain])
        child_values = canonicalize(child_ns_record)
        if parent_values != child_values:
            raise RuntimeError(f"Parent delegated name servers ({parent_values}) and child declared name servers ({child_values}) don't match!")
        logger.info(f"NS delegation record in {parent_zone_id} matches declared NS in {child_zone_id}")


if __name__ == "__main__":
    main()
