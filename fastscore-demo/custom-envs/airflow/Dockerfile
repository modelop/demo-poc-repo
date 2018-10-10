FROM puckel/docker-airflow:1.8.0
USER root
RUN apt-get update && \
    apt-get -y install sudo
USER root
ADD ./sudoers.txt /etc/sudoers
RUN chmod 440 /etc/sudoers
RUN apt-get update && \
    apt-get -y install python3-pip && \
    apt-get -y install vim && \
    apt-get -y install wget
ADD ./requirements.txt .
RUN pip3 install -r requirements.txt
RUN wget https://s3-us-west-1.amazonaws.com/fastscore-cli/fastscore-cli-1.7.tar.gz
RUN tar xzf fastscore-cli-1.7.tar.gz
RUN cd fastscore-cli-1.7 && sudo python setup.py install
USER airflow
#RUN fastscore connect https://dashboard:8000
