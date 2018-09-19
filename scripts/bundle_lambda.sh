#!/bin/bash

# Once the code and all that is in the build/ directory,
# process the template and get it ready for deployment.

aws cloudformation package --template-file SamTemplate.yml --s3-bucket $S3_BUCKET --output-template-file NewSamTemplate.yml
