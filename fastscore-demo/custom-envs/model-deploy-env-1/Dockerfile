FROM fastscore/model-deploy:dev
USER root
ADD ./sudoers.txt /etc/sudoers
RUN chmod 440 /etc/sudoers
USER jovyan
RUN sudo apt-get update && \
    sudo apt-get -y install default-jre && \
    sudo apt-get -y install iputils-ping && \
    sudo apt-get -y install python3-pip
ADD ./requirements.txt .
RUN pip3 install --isolated -r requirements.txt
RUN pip3 install --isolated -r requirements.txt
RUN wget https://s3-us-west-1.amazonaws.com/fastscore-cli/fastscore-cli-1.7.tar.gz
RUN tar xzf fastscore-cli-1.7.tar.gz
RUN cd fastscore-cli-1.7 && sudo /opt/conda/bin/python setup.py install
USER root
ADD ./fastscore-model-deploy .
RUN cd fastscoredeploy/python && python3 setup.py install
USER jovyan
#RUN fastscore connect https://dashboard:8000
