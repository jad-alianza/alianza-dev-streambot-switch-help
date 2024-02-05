#!/usr/bin/env bash

#export DEBUG=true
ENVIRONMENT_TYPE=${DG_TARGET_ID}
ENVIRONMENT_NAME=${DG_SITE_NAME}
DEPLOY_VERSION=${DG_ARTIFACT_VERSION:-0.0.0}
export APP_ROOT_PATH=${BUILDKITE_BUILD_CHECKOUT_PATH}

deploy/run.sh ${ENVIRONMENT_NAME} ${ENVIRONMENT_TYPE} ${DEPLOY_VERSION}

if [ $BUILDKITE == "true" ] && [ ${ENVIRONMENT_TYPE} == "q2" ]; then
    buildkite-agent pipeline upload data-shared-project-utils/.buildkite/medium_tests_streaming.yml
else
    echo "Skipping because ENVIRONMENT_TYPE is not q2"
fi
