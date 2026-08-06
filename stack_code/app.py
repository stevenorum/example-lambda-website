#!/usr/bin/env python3
import os

import aws_cdk

# from stack_code.python_lambda_website import PythonLambdaWebsiteStack
# from stack_code.deployment_pipeline import DeploymentPipelineStack
from python_lambda_website import PythonLambdaWebsiteStack
from deployment_pipeline import DeploymentPipelineStack

OWNER = "stevenorum"
REPO = "example-lambda-website"
BRANCH = "main"

ENV = aws_cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))

app = aws_cdk.App()

auth_token = aws_cdk.SecretValue.secrets_manager(
    # obviously this'll be different for your account
    secret_id="arn:aws:secretsmanager:us-east-1:959113775746:secret:prod/github-KzCYji",
    json_field="codesuite_oauth"
)

DeploymentPipelineStack(app, "DeploymentPipelineStack", env=ENV, owner=OWNER, repo=REPO, branch=BRANCH, auth_token=auth_token)

PythonLambdaWebsiteStack(app, "HelloworldCdkPythonStack", env=ENV)

app.synth()
