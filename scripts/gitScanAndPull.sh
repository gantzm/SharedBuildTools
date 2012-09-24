#!/bin/bash

for projectDir in *
do
    if [ -d "${projectDir}/.git" ] ; then
	echo
	echo Found a git repository : ${projectDir}
	echo
	bash -c "set -x; cd \"${projectDir}\"; git pull"
    fi
done
