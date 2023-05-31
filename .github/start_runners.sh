#!/bin/bash

# Replace following variables with your values
owner="YourGitHubName"
repo="YourRepoName"
num_runners=3
personal_access_token="YourPersonalAccessToken"
base_dir="/path/to/runners"

# Loop to create the desired number of runners
for (( i=1; i<=$num_runners; i++ ))
do
    echo "Starting runner $i"
    runner_dir="$base_dir/runner$i"
    mkdir -p $runner_dir
    cd $runner_dir
    curl -X POST -H "Authorization: token $personal_access_token" -H "Accept: application/vnd.github.v3+json" https://api.github.com/repos/$owner/$repo/actions/runners/registration-token
    ./config.sh --url https://github.com/$owner/$repo --token $personal_access_token --work $runner_dir
    RUNNER_ALLOW_RUNASROOT=1 ./run.sh &
done
