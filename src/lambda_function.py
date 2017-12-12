import boto3

from jinja2 import Environment, FileSystemLoader

content_types = {
    "jpg":"image/jpg",
    "jpeg":"image/jpeg",
    "png":"image/png",
    "gif":"image/gif",
    "bmp":"image/bmp",
    "tiff":"image/tiff",
    "txt":"text/plain",
    "rtf":"application/rtf",
    "ttf":"font/ttf",
    "css":"text/css",
    "html":"text/html",
    "js":"application/javascript",
    "eot":"application/vnd.ms-fontobject",
    "svg":"image/svg+xml",
    "woff":"application/x-font-woff",
    "woff2":"application/x-font-woff",
    "otf":"application/x-font-otf",
    "json":"application/json",
    }

def get_content_type(fname, body=None):
    return content_types.get(fname.split(".")[-1].lower(),"binary/octet-stream")

env = Environment(loader=FileSystemLoader("/var/task/templates/"))

def make_response(body, code=200, headers={"Content-Type": "text/html"}, is_base64=False):
    return {
        "body": body,
        "statusCode": code,
        "headers": headers,
        "isBase64Encoded": is_base64
    }

def render(name, params={}, code=200, headers={}):
    params = params if params else {}
    headers = headers if headers else {}

    template = env.get_template(name)
    body = template.render(**params)
    _headers = {"Content-Type": get_content_type(name)}
    _headers.update(headers)
    return make_response(body=body, code=code, headers=_headers, is_base64=False)

def lambda_handler(event, context):
    print(event)
