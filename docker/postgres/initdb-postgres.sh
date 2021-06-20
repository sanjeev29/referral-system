#!/bin/sh

set -e

# Perform all actions as $POSTGRES_USER
export PGUSER="$POSTGRES_USER"

# Create the database
"${psql[@]}" <<- 'EOSQL'
CREATE DATABASE referral_system_db;
UPDATE pg_database SET datistemplate = TRUE WHERE datname = 'referral_system_db';
EOSQL
