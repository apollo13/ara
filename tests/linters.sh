#!/bin/bash
# Copyright (c) 2022 The ARA Records Ansible authors
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# The parent directory of this script
tests=$(dirname $0)
export PROJECT_ROOT=$(cd `dirname $tests` && pwd -P)
export PROJECT_LIB="${PROJECT_ROOT}/ara"
ret=0

function banner() {
    echo
    printf '#%.0s' {1..50}
    echo
    echo "# ${1}"
    printf '#%.0s' {1..50}
    echo
}

# Let this script work even though it might not be run by tox
if [ -z "${VIRTUAL_ENV}" ]; then
    pushd "${PROJECT_ROOT}"
    tox -e linters --notest
    source .tox/linters/bin/activate
    popd
fi

banner black
time black --config ${PROJECT_ROOT}/.black.toml --diff --check "${PROJECT_LIB}"
ret+=$?

banner isort
time isort --recursive --check-only --diff "${PROJECT_LIB}"
ret+=$?

banner flake8
time flake8 "${PROJECT_LIB}"
ret+=$?

# B303 - Use of insecure MD2, MD4, or MD5 hash function.
# B324 - Use of weak MD4, MD5, or SHA1 hash for security. Consider usedforsecurity=False
# We're using sha1 to generate a hash of file contents.
banner bandit
time bandit -r "${PROJECT_LIB}" --skip B303,B324
ret+=$?

if [ $ret -gt 0 ]
then
  echo
  echo "At least one linter detected errors!"
  exit 1
fi
