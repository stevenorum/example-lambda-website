import hashlib
from typing import Any, Dict, Optional, Union
from aws_cdk import (
    Environment,
    Stack,
    Stage,
    aws_lambda,
    aws_apigateway,
    aws_certificatemanager,
    aws_route53,
)
from constructs import Construct

class PythonLambdaWebsiteStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, url: Optional[str]=None, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.construct_id = construct_id
        self.existing = {}
        hello_world_function = aws_lambda.Function(
            self,
            f"{construct_id}Function",
            runtime = aws_lambda.Runtime.determine_latest_python_runtime(scope),
            code = aws_lambda.Code.from_asset("build"),
            handler = "src.handler.handle",
        )
        api = aws_apigateway.LambdaRestApi(
            self,
            f"{construct_id}Api",
            handler = hello_world_function,
            proxy = True,
        )
        if url:
            url = url.split("://")[-1].rstrip("/")+"/"
            domain_name, suffix = url.split("/", 1)
            suffix = suffix.strip("/")
            suffix = suffix or None
            apig_domain_name = aws_apigateway.DomainName(
                self,
                domain_name.replace(".","-"),
                domain_name=domain_name,
                mapping=api,
                certificate=self.create_cert(domain_name),
                base_path=suffix,
                security_policy=aws_apigateway.SecurityPolicy.TLS_1_0
            )

    def hosted_zone(self, domain_name):
        construct_id = hashlib.md5(domain_name.encode("utf-8")).hexdigest()
        if construct_id in self.existing:
            return self.existing[construct_id]
        self.existing[construct_id] = aws_route53.HostedZone.from_lookup(self, construct_id, domain_name=domain_name)
        return self.existing[construct_id]

    def create_cert(self, domain_name, sans=None):
        sans = sans or []
        cert = aws_certificatemanager.Certificate(
            self, f"{self.construct_id}Cert",
            domain_name=domain_name,
            subject_alternative_names=sans,
            validation=aws_certificatemanager.CertificateValidation.from_dns_multi_zone({
                k:self.hosted_zone(k) for k in sans+[domain_name]
            })
        )
        return cert


    # Need to add stage for this to the deployment pipeline.
    # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/CodePipeline.html
    # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk/Stage.html#aws_cdk.Stage

class PythonLambdaWebsiteStage(Stage):
    def __init__(self, scope: Construct, construct_id: str, env: Union[Environment, Dict[str, Any], None]=None, **kwargs) -> None:
        super().__init__(scope, construct_id, env=env)
        self.stack = PythonLambdaWebsiteStack(self, "PythonLambdaWebsiteStack", env=env, **kwargs)
