#!/bin/bash

EMAIL='put your email here'
AWS_ACCESS_KEY_ID='put your s3 key here'
AWS_SECRET_ACCESS_KEY='put your s3 secret access key here'

sh env/prepare-variables.sh $EMAIL $AWS_ACCESS_KEY_ID $AWS_SECRET_ACCESS_KEY
