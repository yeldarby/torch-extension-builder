#!/bin/bash

# Replace following variables with your values
personal_access_token="YourPersonalAccessToken"
owner="YourGitHubName"

# Get list of runner IDs
runner_ids=$(gh api "repos/$owner/self-hosted-runners" -H "Authorization: token $personal_access_token" | jq '.runners[].id')

# Stop each runner
for id in $runner_ids
do
    echo "Stopping runner with ID $id"
    gh api -X DELETE "repos/$owner/self-hosted-runners/$id" -H "Authorization: token $personal_access_token"
done
