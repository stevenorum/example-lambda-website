from aws_cdk import (
    Stack,
    aws_lambda,
    aws_apigateway,
)
from constructs import Construct

class PythonLambdaWebsiteStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        hello_world_function = aws_lambda.Function(
            self,
            "HelloWorldFunction",
            runtime = aws_lambda.Runtime.determine_latest_python_runtime(scope),
            code = aws_lambda.Code.from_asset("build"),
            handler = "src.handler.handle",
        )
        api = aws_apigateway.LambdaRestApi(
            self,
            "HelloWorldApi",
            handler = hello_world_function,
            proxy = True,
        )
