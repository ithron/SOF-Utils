#!/usr/bin/env bash

set -eou pipefail

VERSION=${GITHUB_REF#refs/tags/}
echo "VERSION=${VERSION}"
sed -n "/## ${VERSION}/,/## [0-9]*\.[0-9]*\.[0-9]*/ p" CHANGELOG.md | sed '$d'

