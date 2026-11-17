FROM debian:12-slim
RUN apt-get update \
 && apt-get install -y --no-install-recommends openssh-server openssh-client sshpass sudo rsyslog python3 \
 && rm -rf /var/lib/apt/lists/*
COPY start.sh triage.py /opt/
RUN chmod +x /opt/start.sh
CMD ["/opt/start.sh"]
