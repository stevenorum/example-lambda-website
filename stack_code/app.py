#!/usr/bin/env python3
import os

import aws_cdk

from stack_code.python_lambda_website import PythonLambdaWebsiteStack
from stack_code.deployment_pipeline import DeploymentPipelineStack

OWNER = "stevenorum"
REPO = "example-lambda-website"
BRANCH = "main"

ENV = aws_cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))

app = aws_cdk.App()

DeploymentPipelineStack(app, "DeploymentPipelineStack", env=ENV, owner=OWNER, repo=REPO, branch=BRANCH)

PythonLambdaWebsiteStack(app, "HelloworldCdkPythonStack", env=ENV)

app.synth()
