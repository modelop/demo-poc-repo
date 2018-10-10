FROM influxdb

COPY fastscore.dump /etc/fastscore.dump
COPY start.sh /etc/start.sh
RUN chmod +x /etc/start.sh

ENTRYPOINT ["/etc/start.sh"]
