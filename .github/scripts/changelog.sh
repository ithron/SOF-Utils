#!/usr/bin/env bash

VERSION=${GITHUB_REF#refs/tags/}
sed -n "/## ${VERSION}/,/## [0-9]*\.[0-9]*\.[0-9]*/ p" CHANGELOG.md | sed '$d'

