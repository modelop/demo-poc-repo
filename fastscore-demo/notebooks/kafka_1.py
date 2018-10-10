#!/usr/local/bin/python3
import threading, logging, time
import multiprocessing

from kafka import KafkaConsumer, KafkaProducer


class Producer(threading.Thread):
    daemon = True

    def run(self):
        producer = KafkaProducer(bootstrap_servers='kafka:9092')

        while True:
            producer.send('test-topic', b"test")
            producer.send('test-topic', b"Hello, world!")
            producer.flush()
            time.sleep(1)


class Consumer(multiprocessing.Process):
    daemon = True

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers='kafka:9092',
                                 auto_offset_reset='earliest')
        consumer.subscribe(['model-output'])

        for message in consumer:
            print (message)


def main():
    tasks = [
        Consumer()
#        Producer()
    ]

    for t in tasks:
        t.start()

    time.sleep(10)
    print("***********************************")
    print("********10 second test done********")
    print("***********************************")

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
        )
    main()
