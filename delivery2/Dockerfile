FROM solr:8.10

COPY data/ps_merged_refined.json /data/ps_merged_refined.json

COPY data/ch_refined.json /data/ch_refined.json

COPY data/il_refined.json /data/il_refined.json

COPY data/psd_refined.json /data/psd_refined.json

COPY simple_schema.json /data/simple_schema.json

COPY startup.sh /scripts/startup.sh

ENTRYPOINT ["/scripts/startup.sh"]