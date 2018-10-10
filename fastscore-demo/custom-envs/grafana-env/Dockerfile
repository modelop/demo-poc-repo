FROM grafana/grafana

RUN apt-get update

RUN apt-get install -y python python-pip wget python-yaml

RUN pip install --upgrade pip==8.0

RUN pip install potsdb websocket_client urllib3==1.21.1

COPY consume.py consume.py

RUN wget https://s3-us-west-1.amazonaws.com/fastscore-cli/fastscore-cli-1.6.1.tar.gz && \
    tar xzf fastscore-cli-1.6.1.tar.gz && \
    cd fastscore-cli-1.6.1 && \
    python setup.py install

ENTRYPOINT ["/bin/sh", "-c", "/run.sh & python consume.py"]