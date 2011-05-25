#!/bin/bash

RAW_SCRIPT_DIR=`dirname $0`
SCRIPT_DIR=`readlink -m ${RAW_SCRIPT_DIR}`

DEV_ENVIRONMENT=dell.laptop
OUTPUT_FILE=${SCRIPT_DIR}/output.$$.sh

rm -f ${OUTPUT_FILE}

${SCRIPT_DIR}/environment.py ${SCRIPT_DIR}/environment.xml ${DEV_ENVIRONMENT} ${OUTPUT_FILE}

if [ ! -f ${OUTPUT_FILE} ]
then
    exit
fi

. ${OUTPUT_FILE}

if [ -n "${JAVA_HOME}" ]
then
    echo From script : JAVA_HOME = ${JAVA_HOME}
    export JAVA_HOME
    export JRE_HOME=${JAVA_HOME}
    export PATH=${JAVA_HOME}/bin:${PATH}
fi

if [ -n "${MAVEN_HOME}" ]
then
    echo From script : MAVEN_HOME = ${MAVEN_HOME}
    export MAVEN_HOME
    export PATH=${MAVEN_HOME}/bin:${PATH}
fi

if [ -n "${ANT_HOME}" ]
then
    echo From script : ANT_HOME = ${ANT_HOME}
    export ANT_HOME
    export PATH=${ANT_HOME}/bin:${PATH}
fi

if [ -n "${ECLIPSE_HOME}" ]
then
    echo From script : ECLIPSE_HOME = ${ECLIPSE_HOME}
    export ECLIPSE_HOME
    export PATH=${ECLIPSE_HOME}:${PATH}
fi

if [ -n "${CATALINA_HOME}" ]
then
    echo From script : CATALINA_HOME = ${CATALINA_HOME}
    export CATALINA_HOME
    export PATH=${CATALINA_HOME}/bin:${PATH}
fi

if [ -n "${RUBY_HOME}" ]
then
    echo From script : RUBY_HOME = ${RUBY_HOME}
    export RUBY_HOME
    export PATH=${RUBY_HOME}/bin:${PATH}
fi

if [ -n "${NODEJS_HOME}" ]
then
    echo From script : NODEJS_HOME = ${NODEJS_HOME}
    export NODEJS_HOME
    export PATH=${NODEJS_HOME}/bin:${PATH}
fi


rm -f ${OUTPUT_FILE}
