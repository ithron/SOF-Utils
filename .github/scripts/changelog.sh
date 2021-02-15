#!/usr/bin/env bash

VERSION=$1
sed -n "/## ${VERSION}/,/## [0-9]*\.[0-9]*\.[0-9]*/ p" CHANGELOG.md | sed '$d'

