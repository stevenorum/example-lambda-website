#!/bin/bash

if [ -f private.sh ]; then
    source private.sh
fi

scripts/build.sh && cdk synth && cdk deploy --profile $PROFILE_NAME DeploymentPipelineStack
scripts/build.sh && cdk synth && cdk deploy --profile $PROFILE_NAME HelloworldCdkPythonStack
