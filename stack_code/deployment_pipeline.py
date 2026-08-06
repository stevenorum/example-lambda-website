from typing import Optional

import aws_cdk
from constructs import Construct
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep

class DeploymentPipelineStack(aws_cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 owner: str,
                 repo: str,
                 branch: str = "main",
                 pipeline_name: Optional[str] = None,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # May need to add some sanitization to ensure that this pipeline name meets the CodePipeline requirements.
        pipeline_name = pipeline_name or f"{owner}-{repo}-{branch}"
        pipeline =  CodePipeline(
            self, "Pipeline",
            pipeline_name=pipeline_name,
            synth=ShellStep(
                "Synth",
                input=CodePipelineSource.git_hub(f"{owner}/{repo}", branch),
                commands=[
                    "npm install -g aws-cdk",
                    "python -m pip install -r requirements.txt",
                    "cdk synth"
                ]
            )
        )
