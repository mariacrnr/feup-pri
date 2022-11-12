FROM solr:8.10

# COPY data/ps.json /data/ps.json

# COPY data/chega.json /data/chega.json

# COPY data/il.json /data/il.json

# COPY data/psd.json /data/psd.json

# COPY data/pcp.json /data/pcp.json

# COPY data/pan.json /data/pan.json

# COPY data/livre.json /data/livre.json

# COPY data/bloco.json /data/bloco.json

COPY data/sample.json /data/sample.json

COPY schema.json /data/schema.json

COPY startup.sh /scripts/startup.sh

ENTRYPOINT ["/scripts/startup.sh"]