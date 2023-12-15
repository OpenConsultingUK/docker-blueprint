#!/bin/bash

cp /etc/letsencrypt/live/sample.domain.com/fullchain.pem certs/ # Change sample.domain.com
cp /etc/letsencrypt/live/sample.domain.com/privkey.pem certs/ # Change sample.domain.com

echo "Files copied to successfully."
