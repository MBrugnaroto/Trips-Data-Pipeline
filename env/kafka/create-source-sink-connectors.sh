#!/bin/bash

curl -H 'Accept:application/json' -H 'Content-Type:application/json' POST http://localhost:8083/connectors \
--retry 5 \
--retry-connrefused \
--retry-delay 10 \
--fail \
-d @env/kafka/source/config/config-source-connect-postgres.json \
-v

curl -H 'Accept:application/json' -H 'Content-Type:application/json' POST http://localhost:8083/connectors \
--retry 5 \
--retry-connrefused \
--retry-delay 10 \
--fail \
-d @env/kafka/sink/config/config-sink-connect-s3.json \
-v
