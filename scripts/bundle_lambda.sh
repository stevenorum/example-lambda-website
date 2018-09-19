#!/bin/bash

# Once the code and all that is in the build/ directory,
# process the template and get it ready for deployment.

python3 generate_lambda_template.py SamTemplate.json ProcessedSamTemplate.json
python3 process_static_functions.py ProcessedSamTemplate.json ProcessedSamTemplate.json
