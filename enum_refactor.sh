#!/bin/bash


for filename in homeassistant/components/a*; do
    filename=$(basename -- "$filename")
    echo "Processing $filename..."
    branchname="refactor_enum_${filename}_tests"

    if [ `git branch --list $branchname` ]
    then
        echo "Branch name $branchname already exists, skipping."
        continue
    fi

    python3 script/enum_refactor.py $filename || { echo 'Command failed' ; exit 1; }
    if [ ! -d "tests/components/$filename" ]
    then
        echo "No tests for $filename, skipping."
        continue
    fi
    COUNT=$(git --no-pager diff --stat tests/components/${filename}/ | grep "changed" | sed 's@^[^0-9]*\([0-9]\+\).*@\1@')
    if test -z "$COUNT"
    then
        echo " No changes for $filename"
        continue
    else
        echo "$COUNT Changes for $filename"
    fi
    pytest tests/components/$filename

    if [ "$?" -ne 0 ]; then
        echo " Some tests failed. Stopping."
        break
    fi
    read -p " Examine the diff.  press [enter] to continue with commit and push, <ctrl>-c to stop.  If you make any edits, isort and restart this script."
    git stash || { echo 'Command failed' ; exit 1; }
    git checkout -b $branchname || { echo 'Command failed' ; exit 1; }
    git stash pop || { echo 'Command failed' ; exit 1; }
    COUNT=$(git --no-pager diff --stat homeassistant/components/${filename}/ | grep "changed" | sed 's@^[^0-9]*\([0-9]\+\).*@\1@')
    if test -z "$COUNT"
    then
        echo " No changes to main component for $filename"
    else
        echo " CHANGES for main component $filename"
        git add homeassistant/components/${filename}/* || { echo 'Command failed' ; exit 1; }
        git commit -m"Use DeviceClass Enums in ${filename}" || { echo 'Command failed' ; exit 1; }
    fi
    git add tests/components/${filename}/* || { echo 'Command failed' ; exit 1; }
    git commit -m"Use DeviceClass Enums in ${filename} tests"

    git push --set-upstream origin $branchname || { echo 'Command failed' ; exit 1; }
    git checkout dev || { echo 'Command failed' ; exit 1; }
    break
done

echo Finished, used 'git checkout -- .' to revert changed files
#git checkout -- .
