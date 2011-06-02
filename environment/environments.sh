#!/bin/bash

if [ -n "${BASH_SOURCE}" ] ; then
    RAW_SCRIPT_DIR=`dirname ${BASH_SOURCE}`
else
    RAW_SCRIPT_DIR=`dirname $0`
fi

SCRIPT_DIR=`readlink -m ${RAW_SCRIPT_DIR}`
OUTPUT_FILE=${SCRIPT_DIR}/output.$$.sh

echo BASH_SOURCE = $BASH_SOURCE
echo RAW_SCRIPT_DIR = ${RAW_SCRIPT_DIR}
echo SCRIPT_DIR = ${SCRIPT_DIR}

rm -f ${OUTPUT_FILE}

${SCRIPT_DIR}/environments.py ${SCRIPT_DIR}/environments.xml > ${OUTPUT_FILE}

cat ${OUTPUT_FILE}

. ${OUTPUT_FILE}

rm -f ${OUTPUT_FILE}

unset RAW_SCRIPT_DIR
unset SCRIPT_DIR
