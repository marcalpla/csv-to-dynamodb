#!/bin/bash

cd $(dirname "$(realpath "$0")")/..
poetry run csv-to-dynamodb \
    --csv-file ../data/example.csv \
    --csv-delimiter ";" \
    --dynamodb-table-name MyDynamoDBTable