from typing import Optional

import aws_cdk
from constructs import Construct
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep

class DeploymentPipelineStack(aws_cdk.Stack):

    # the docs recommend using CodeStar instead of CodePipelineSource.git_hub, but this works for now and is how their example tutorial does it
    def __init__(self, scope: Construct, construct_id: str,
                 owner: str,
                 repo: str,
                 branch: str = "main",
                 pipeline_name: Optional[str] = None,
                 auth_token: Optional[aws_cdk.SecretValue] = None,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # May need to add some sanitization to ensure that this pipeline name meets the CodePipeline requirements.
        pipeline_name = pipeline_name or f"{owner}-{repo}-{branch}"
        self.pipeline =  CodePipeline(
            self, "Pipeline",
            pipeline_name=pipeline_name,
            synth=ShellStep(
                "Synth",
                input=CodePipelineSource.git_hub(
                    repo_string=f"{owner}/{repo}",
                    branch=branch,
                    authentication=auth_token,
                ),
                commands=[
                    "npm install -g aws-cdk",
                    "python -m pip install -r requirements.txt",
                    "./scripts/build.sh",
                    "cdk synth"
                ]
            )
        )
