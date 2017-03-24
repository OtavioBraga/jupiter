#!/bin/bash
set -e

echo "Installing extensions..."
psql -v ON_ERROR_STOP=1 -d $POSTGRES_DB --username "$POSTGRES_USER" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS hstore;
    CREATE EXTENSION IF NOT EXISTS unaccent;
EOSQL
echo "Extensions successfully installed!"
