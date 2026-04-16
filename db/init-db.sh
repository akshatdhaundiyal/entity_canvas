#!/bin/bash
set -e

# Create the pagila database
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE pagila;
EOSQL

# Load the pagila dump into the pagila database
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "pagila" < /tmp/local_pagila.sql
