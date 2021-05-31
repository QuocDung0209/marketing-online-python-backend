#!/bin/sh -e
set -x

touch .env
cat << EOF > .env
# PostgreSQL
POSTGRES_SERVER=localhost
POSTGRES_USER=database_user
POSTGRES_PASSWORD=database_password
POSTGRES_DB=marketing-online
EOF