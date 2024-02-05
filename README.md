# Streaming <NAME> Data Project Template
## Infrastructure for streaming <NAME> entities into the Alianza datalake


# Setup for local development and testing:
1. The following software should be installed:
 - Docker and docker-compose
 - https://github.com/awslabs/amazon-ecr-credential-helper
 - Python3.11+ and poetry (version 1.6.1 or newer)
2. Configure bellow environment variables:
 - 'POETRY_HTTP_BASIC_ALIANZA_INTERNAL_USERNAME=${ARTIFACTORY_PYPI_USER}'
 - 'POETRY_HTTP_BASIC_ALIANZA_INTERNAL_PASSWORD=${ARTIFACTORY_PYPI_PASSWORD}'
 - 'POETRY_HTTP_BASIC_ALIANZA_SNAPSHOT_USERNAME=${ARTIFACTORY_PYPI_USER}'
 - 'POETRY_HTTP_BASIC_ALIANZA_SNAPSHOT_PASSWORD=${ARTIFACTORY_PYPI_PASSWORD}'
 - 'ARTIFACTORY_PYPI_USER=your_jfrog_username'
 - 'ARTIFACTORY_PYPI_PASSWORD=your_jfrog_password'
3. If you want to have venv in your project directory execute command bellow:
```
poetry config virtualenvs.in-project true
poetry config virtualenvs.create true
poetry config virtualenvs.path .venv
```
4. In case you have multiple python versions installed locally, and you want to use specific version for the project, run the following command:
```
poetry env use 3.11
```
and the following command to check the current version that is used in virtualenv:  
```
poetry env info
```
5. Get the latest shared utilities (also run this target periodically)
```
make update-base
```
5. Create virtualenv and setup python libraries:
```
make install
```

## Make sure the following environment variables have the following values in the .core.env file:
 - APP_NAME_FULL=streaming-<NAME> # is typically just the repo name and is used for naming resources. Valid regex: ^[a-b-]{10,35}$ e.g. streaming-device-management, streaming-switch-help- 
 - APP_NAME_SHORT=<NAME> # is a shortened derivative name used for naming resources with name length constraints like databases. Valid regex: ^[a-b-]{2,13}$ e.g. devman, switch-help
 - APP_NAME_FULL_SQL=streaming_<NAME> # is simply APP_NAME with underscores. Valid regex: ^[a-b_]{10,35}$ e.g. streaming_device_management, streaming_switch_help
 - APP_NAME_SHORT_SQL=<NAME> # is simply APP_SHORT with underscores. Valid regex: ^[a-b_]{2,13}$ e.g. devman, switch_help

## Make sure the virtual environment has a name in pyproject.toml
- name - replace the name for your venv from "streaming-<NAME>" to match APP_NAME

# Manual Testing

## Run docker to test locally
```
make exec
```
## Make sure you are authenticated in AWS to work with labs or prod account

* AWS CLI should be installed
* make sure appropriate aws profiles are added to your ~/.aws/config file, called data-lab and data-prod, please refer to https://alianza.atlassian.net/wiki/spaces/DEV/pages/2951480108/How+to+Log+Into+AWS+at+Alianza
* or if you have another profile name please set the AWS_DEFAULT_PROFILE environment variable with desired value
```
# labs
aws sso login --profile data-lab

# prod
aws sso login --profile data-prod
```

## Subsequently to test lambdas locally
```
AWS_DEFAULT_PROFILE=data-lab poetry run python lambdas/<NAME>_transformer_lambda.py

AWS_DEFAULT_PROFILE=data-lab poetry run python lambdas/daily_snapshotter_lambda.py
```

&nbsp;

# Automated Testing
## Usage:
### Run linter tools for tests:
```
make lint
```
### Format tests using `isort` and `black` tools:
```
make format
```
### Run tests with `pytest`:
```
make tests
```
### Run Behave tests:
 1. Make sure there are valid AWS security credentials:
```
aws sso login --profile data-lab
```
 2. Start all behave tests
```
make behave
```
 3. Or start specific feature file or scenario:
```
# test whole feature file:
AWS_DEFAULT_PROFILE=data-lab poetry run behave ./behave_tests/features/<NAME>_streaming.feature
# test specific scenario:
AWS_DEFAULT_PROFILE=data-lab poetry run behave ./behave_tests/  -n "Test <NAME> data transformation"
```

### Test Reports
- Tests Analytics report for unittest is available here:
https://buildkite.com/organizations/alianza-inc/analytics/suites/streaming-<NAME>-unittests
- Behave tests Allure report is available for every build in the following file in artifacts:
behave_tests/reports/allure-report/index.html

## Buildkite CI setup:
* Open "Edit Steps" page in buildkite WebUI, for example https://buildkite.com/alianza-inc/streaming-ax/steps
* In the Legacy Steps section click on the small button with blue circle
* In the "Commands to run" text area write the following:
```
buildkite-agent pipeline upload data-shared-project-utils/.buildkite/pipeline.yml
```
* Click "Save Steps" button

## Deployment
* please refer to [Readme.md file](deploy/README.md)
