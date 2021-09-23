# RabbitMQ Notes

## Introduction

- Producer: Who produces messages.
- Consumer: Who consumes messages.
- Message has two parts: a payload and a label. Payload can be any data even
binary files. The label describes the payload.
- AMQP doesn't specify a sender and receiver, there is just message with label.
Based on that label the implementation software like RabbitMQ decides who will
get the message. It is like fire and forget and one directional communication.
In TCP there is a sender and a receiver.
- Before an application can connect to RabbitMQ server, it needs to setup a
channel.


## Resources

- If you want to check in detail the technical differences between these two
serialization mechanisms (JSON and Java Serialized Object), you can read the
article at
https://thepracticaldeveloper.com/produce-and-consume-json-messages-with-spring-boot-amqp/
. 






