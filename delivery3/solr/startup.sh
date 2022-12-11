#!/bin/bash

precreate-core parties

# Start Solr in background mode so we can use the API to upload the schema
solr start

sleep 2

# Add synonyms
mkdir -p /var/solr/data/parties/res
cp /data/synonyms.txt /var/solr/data/parties/res/synonyms.txt
echo "Added synonyms"

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary @/data/schema.json \
    http://localhost:8983/solr/parties/schema

# Populate collection
bin/post -c parties /data/ps.json

bin/post -c parties /data/il.json

bin/post -c parties /data/chega.json

bin/post -c parties /data/psd.json

bin/post -c parties /data/pcp.json

bin/post -c parties /data/pan.json

bin/post -c parties /data/livre.json

bin/post -c parties /data/bloco.json


sleep 2


# Restart in foreground mode so we can access the interface
solr restart -f
