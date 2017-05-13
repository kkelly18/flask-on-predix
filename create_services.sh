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

# Update Manifest
cp manifest-template.yml manifest.yml
sed -i '' "s/<APP_NAME>/$prefix-flask/" manifest.yml
sed -i '' "s/<UAA_SERVICE_INSTANCE_NAME>/$prefix-uaa/" manifest.yml
sed -i '' "s/<POSTGRES_SERVICE_INSTANCE_NAME>/$prefix-postgres/" manifest.yml
sed -i '' "s/<BASE_64_CREDENTIALS>/$clientSecretBase64/" manifest.yml

# Update Config
cp config-template.py config.py
sed -i '' "s@<UAA_TARGET>@$uaaTarget@" config.py
sed -i '' "s/<UAA_CLIENT_ID>/$prefix-client/" config.py
sed -i '' "s/<UAA_CLIENT_SECRET>/$clientSecret/" config.py

# Update Postman Environments
cp postman/flask_on_predix_postman_env_local-template.json postman/flask_on_predix_postman_env_local.json
sed -i '' "s/<UAA_TENANT_ID>/$uaaTenant/" postman/flask_on_predix_postman_env_local.json
sed -i '' "s/<UAA_CLIENT_ID>/$prefix-client/" postman/flask_on_predix_postman_env_local.json

cp postman/flask_on_predix_postman_env_predix-template.json postman/flask_on_predix_postman_env_predix.json
sed -i '' "s/<UAA_TENANT_ID>/$uaaTenant/" postman/flask_on_predix_postman_env_predix.json
sed -i '' "s/<UAA_CLIENT_ID>/$prefix-client/" postman/flask_on_predix_postman_env_predix.json
sed -i '' "s/<APP_URL>/$prefix-flask.run.aws-usw02-pr.ice.predix.io/" postman/flask_on_predix_postman_env_predix.json

# Config SQLAlchemy
python manage.py db init
python manage.py db migrate
python manage.py db upgrade