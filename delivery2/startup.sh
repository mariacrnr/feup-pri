#!/bin/bash

precreate-core parties

# Start Solr in background mode so we can use the API to upload the schema
solr start

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary @/data/simple_schema.json \
    http://localhost:8983/solr/parties/schema

# Populate collection
bin/post -c parties /data/ps_merged_refined.json

bin/post -c parties /data/il_refined.json

bin/post -c parties /data/ch_refined.json

bin/post -c parties /data/psd_refined.json

# Restart in foreground mode so we can access the interface
solr restart -f
