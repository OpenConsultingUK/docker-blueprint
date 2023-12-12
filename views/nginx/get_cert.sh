#!/bin/bash

cp /etc/letsencrypt/live/poc.openconsultinguk.com/fullchain.pem certs/
cp /etc/letsencrypt/live/poc.openconsultinguk.com/privkey.pem certs/

echo "Files copied to successfully."
