#!/usr/bin/env bash

# Get project prefix
echo -n "Type your desired services prefix (e.g. demo), and hit [ENTER]: "
read prefix

# Configure Postgres Instance
cf create-service postgres shared-nr $prefix-postgres

# Configure UAA Instance
echo -n "Type your desired UAA admin client password, and hit [ENTER]: "
read -s adminClientSecret
cf cs predix-uaa Free $prefix-uaa -c '{"adminClientSecret": "'"$adminClientSecret"'"}'

uaaTenant=`cf service $prefix-uaa --guid`
uaaTarget="https://$uaaTenant.predix-uaa.run.aws-usw02-pr.ice.predix.io"
uaac target $uaaTarget
uaac token client get admin -s $adminClientSecret

clientSecret=$adminClientSecret
clientSecretBase64=`echo -n $prefix-client:$clientSecret | base64`

uaac client add $prefix-client -s $clientSecret --scope "uaa.none openid" --authorized_grant_types "authorization_code client_credentials refresh_token password" --authorities "openid uaa.none uaa.resource" --autoapprove "openid"
uaac user add app_user_1 -p app_user_1 --emails app_user_1@email.net

# Copy Templates
cp manifest-template.yml manifest.yml
cp config-template.py config.py

# Update Manifest
sed -i "s/<APP_NAME>/$prefix/" manifest.yml
sed -i "s/<POSTGRES_SERVICE_INSTANCE_NAME>/$prefix-postgres/" manifest.yml
# sed -i "s/<CLIENT_ID>/$$prefix-client/g" manifest.yml
# sed -i "s/<BASE_64_CREDENTIALS>/$clientSecretBase64" manifest.yml

# Update Config
# sed -i "s/<CLIENT_ID>/$$prefix-client/g" config.py
# sed -i "s/<BASE_64_CREDENTIALS>/$clientSecretBase64" config.py