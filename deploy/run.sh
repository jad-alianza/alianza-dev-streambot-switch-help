#!/bin/bash -e
# :vi ft=bash

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" 1>/dev/null 2>/dev/null && pwd )"

if [ "$#" -ne 3 ]; then
echo "Usage: $0 <environment-type> <environment-name> <appVersion>"
exit 1
fi

ENVIRONMENT_NAME=${1}
ENVIRONMENT_TYPE=${2}
APP_VERSION=${3}

export $(grep -v '^#' < .core.env | tr -d '[:blank:]')

if [[ "$(pwd)" != "$SCRIPT_DIR" ]]; then
    cd ${SCRIPT_DIR}
fi

#temp=$(mktemp -d)
#cp -r deploy/* ${temp}/
export ANSIBLE_CONFIG=${SCRIPT_DIR}/ansible/ansible.cfg
ansible --version

if [[ ${DEBUG} == 'true' ]]; then
  echo "Debug mode enabled."
  playbook='-vvv ansible/deploy.yml'
else
  playbook='ansible/deploy.yml'
fi

#pushd ${temp}

echo "Install Phoenix Ansible collection..."
ansible-galaxy collection install -vvv -i -f -r ansible/requirements.yml

command="ansible-playbook -e mfaToken=${MFA_TOKEN}
                -e appDir=${SCRIPT_DIR}/.. \
                -e environmentName=${ENVIRONMENT_NAME} \
                -e environmentType=${ENVIRONMENT_TYPE} \
                -e ARTIFACT_VERSION=${APP_VERSION} \
                -e region=${REGION:-us-east-2} \
                ${playbook}"

echo ${command}
exec ${command}

#popd
#rm -rf ${temp}
