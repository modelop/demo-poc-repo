FROM openjdk:jre-slim
RUN apt-get update && apt-get -y install wget
WORKDIR /kafkaesq/
RUN wget http://apache.spinellicreations.com/kafka/1.0.0/kafka_2.11-1.0.0.tgz
RUN tar xzf kafka_2.11-1.0.0.tgz
RUN wget https://s3-us-west-1.amazonaws.com/kafkaesq/kafkaesq
RUN chmod u+x kafkaesq
CMD bash
