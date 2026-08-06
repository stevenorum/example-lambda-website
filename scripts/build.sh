#!/bin/bash

# Clean up the old build directory
if [ -e build ] ; then
    rm -rf build/
fi
mkdir -p build

# Copy everything over to the build directory
cp -r lambda/* build/

# Store a file containing the build timestamp, because why not.
date +%Y-%m-%dT%H:%M:%S%z >  build/BUILD_TIMESTAMP

# Clean up emacs backup and lockfiles. Not for any super important reason, they just annoy me.
# Only run it on a Mac so it doesn't clog the CodeBuild logs with pointless error messages when it doesn't find anything.
if [ "$(uname)" = "Darwin" ]; then
    find build/* | grep '~$' | xargs rm
    find build/* | grep '#$' | xargs rm
fi

# Install any dependencies
if [ -e lambda/requirements.txt ] ; then
    pip3 install --no-cache-dir -t build/ -r lambda/requirements.txt
fi
