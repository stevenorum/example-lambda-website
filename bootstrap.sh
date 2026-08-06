#!/bin/bash

if [ -f private.sh ]; then
    source private.sh
fi

cdk bootstrap --profile $PROFILE_NAME
