# Basic Python Lambda website

Based on https://docs.aws.amazon.com/cdk/v2/guide/serverless-example.html and https://docs.aws.amazon.com/cdk/v2/guide/cdk-pipeline.html

## Prerequisites

You need to have an AWS account set up, and you need to have creds stored locally so boto3 can access them.
The profile name for those creds should be in the environment variable $PROFILE_NAME

If you don't want it to be the same as whatever the default in your shell is, store it in the file `private.sh` and the scripts in this package will load it for you.

## Setup

Create and activate the virtual env:
```
python -m venv .venv
source .venv/bin/activate
```

Install the dependencies:
```
python3 -m pip install -r requirements.txt
```

First time, to set up some AWS resources that CDK relies on:

```
cdk bootstrap --profile $PROFILE_NAME
```

or just `bootstrap.sh`

Build:
```
./build.sh
cdk synth
cdk deploy --profile $PROFILE_NAME
```

Or, if you prefer, simply `./deploy.sh`
