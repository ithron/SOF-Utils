#!/usr/bin/env bash

set -eou pipefail

VERSION=${GITHUB_REF#refs/tags/}
CHANGELOG=$(sed -n "/## ${VERSION}/,/## v[0-9]*\.[0-9]*\.[0-9]*/ p" CHANGELOG.md | sed '$d')
CHANGELOG="${CHANGELOG//'%'/'%25'}"
CHANGELOG="${CHANGELOG//$'\n'/'%0A'}"
CHANGELOG="${CHANGELOG//$'\r'/'%0D'}"
echo "$CHANGELOG"
