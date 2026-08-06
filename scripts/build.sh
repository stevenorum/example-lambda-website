#!/bin/bash

# Clean up the old build directory
if [ -e build ] ; then
    rm -rf build/
fi
mkdir -p build

# Copy everything over to the build directory
cp -r lambda/* build/

date -z UTC +%Y/%m/%d-%H:%M:%S+00:00 > build/BUILD_TIMESTAMP

# Clean up emacs backup and lockfiles, not for any super important reason. They just annoy me.
find build/* | grep '~$' | xargs rm
find build/* | grep '#$' | xargs rm

# The following can be handy when you want to inject stuff in CodeBuild
# if [ ! -z "$BUILD_PARAMS" ] ; then
#     echo "$BUILD_PARAMS" > build/extra_params.json
# fi

# Install any dependencies
if [ -e lambda/requirements.txt ] ; then
    pip3 install --no-cache-dir -t build/ -r lambda/requirements.txt
fi
