# -*- coding: utf-8 -*-

import logging
import pika
import sys
import json

import cloud_api
from handlers import vm, network, ebs, ees, elb, image, backup

LOG = logging.getLogger(__name__)

class MQ_Send_Service(object):
    def __init__(self, mqconfig):
        self.mqconfig = mqconfig
        self.mqhost = mqconfig["rabbitmq.host"]
        self.mqVhost = mqconfig["rabbitmq.vhost"]
        self.mqUser = mqconfig["rabbitmq.username"]
        self.mqPasswd = mqconfig["rabbitmq.password"]
        self.msgQueue = mqconfig["rabbitmq.workOrderQueue"]
        self.queueDurable = mqconfig["rabbitmq.queue_durable"]
        self.queueAutoDelete = mqconfig["rabbitmq.queue_auto_delete"]
        self.queueExclusive = mqconfig["rabbitmq.queue_exclusive"]
        self.port = mqconfig["rabbitmq.port"]
        self.exchange = mqconfig["rabbitmq.exchange_name"]
        self.exchangeType = mqconfig["rabbitmq.exchange_type"]
        self.exchangeDurable = mqconfig["rabbitmq.exchange_durable"]
        self.exchangeAutoDelete = mqconfig["rabbitmq.exchange_auto_delete"]
        self.routingkey = mqconfig["rabbitmq.routing_key"]

        self.credentials = pika.PlainCredentials(self.mqUser, self.mqPasswd)
        self.parameters = pika.ConnectionParameters(self.mqhost, \
                self.port, self.mqVhost, self.credentials)
        self.connection = pika.BlockingConnection(self.parameters)

    def send_message(self, msgBody):
        channel = self.connection.channel()
        channel.exchange_declare(exchange=self.exchange, \
                                type=self.exchangeType, \
                                durable=self.exchangeDurable, \
                                auto_delete=self.exchangeAutoDelete)
        channel.basic_publish(routing_key=self.routingkey, \
                exchange=self.exchange, body=msgBody)
        LOG.info("Sent %r" % msgBody)
        channel.close()

class MQ_ReceiveService(object):
    def __init__(self, mqconfig, tp_size=4):
        self.mqconfig = mqconfig
        self.mqhost = mqconfig["rabbitmq.host"]
        self.mqVhost = mqconfig["rabbitmq.vhost"]
        self.mqUser = mqconfig["rabbitmq.username"]
        self.mqPasswd = mqconfig["rabbitmq.password"]
        self.msgQueue = mqconfig["rabbitmq.workOrderQueue"]
        self.queueDurable = mqconfig["rabbitmq.queue_durable"]
        self.queueAutoDelete = mqconfig["rabbitmq.queue_auto_delete"]
        self.queueExclusive = mqconfig["rabbitmq.queue_exclusive"]
        self.port = mqconfig["rabbitmq.port"]
        self.exchange = mqconfig["rabbitmq.exchange_name"]
        self.exchangeType = mqconfig["rabbitmq.exchange_type"]
        self.exchangeDurable = mqconfig["rabbitmq.exchange_durable"]
        self.exchangeAutoDelete = mqconfig["rabbitmq.exchange_auto_delete"]
        self.routingkey = mqconfig["rabbitmq.routing_key"]

        self.credentials = pika.PlainCredentials(self.mqUser, self.mqPasswd)
        self.parameters = pika.ConnectionParameters(self.mqhost, \
                                                    self.port, \
                                                    self.mqVhost, \
                                                    self.credentials)
        self.connection = pika.BlockingConnection(self.parameters)

    def receive_message(self):
        channel = self.connection.channel()
        channel.exchange_declare(exchange=self.exchange, \
                                type=self.exchangeType, \
                                durable=self.exchangeDurable, \
                                auto_delete=self.exchangeAutoDelete)
        channel.queue_declare(queue=self.msgQueue, \
                            durable=self.queueDurable, \
                            exclusive=self.queueExclusive, \
                            auto_delete=self.queueAutoDelete)
        channel.queue_bind(exchange=self.exchange, \
                queue=self.msgQueue, \
                routing_key=self.routingkey)
        # print " [*] Waiting for logs. To exit press CTRL+C"

        def callback(ch, method, properties, body):
            # print " [x] %r:%r" % (method.routing_key, body)
            LOG.info('Message received: %s' % body)
            msg = json.loads(body)

            # Persistence
            LOG.info("Call cloud API: message_persistance, parameter is %s." % msg)
            ret = cloud_api.message_persistance(msg)
            LOG.info("ret is" + str(ret))
            if not ret['success']:
                LOG.error(ret['data'])
                return

            LOG.info("message persist successfuly.")

            # Verification
            # TODO: Change method
            # ret = cloud_api.verify_user({'user_id': msg['userId']})
            # if not ret['success']:
            #     LOG.error(ret['data'])
            #     return

            # Take actions based on message type
            if msg['resourceType'] == 'VM':
                LOG.info("resoucetype is" + str("VM"))
                ret = vm.handler(msg)
            elif msg['resourceType'] == 'EBS':
                ret = ebs.handler(msg)
            elif msg['resourceType'] == 'NETWORK':
                ret = network.handler(msg)
            elif msg['resourceType'] == 'BACKUP':
                ret = backup.handler(msg)
            elif msg['resourceType'] == 'EES':
                ret = ees.handler(msg)
            elif msg['resourceType'] == 'ELB':
                ret = elb.handler(msg)
            elif msg['resourceType'] == 'IMAGE':
                ret = image.handler(msg)
            else:
                ret = {
                    'success': False,
                    'msg': 'Unkonwn resource type'
                }
            LOG.info('Message handle result: %s' % ret)
            #ch.basic_publish(routing_key=self.routingkey, \
            #         exchange=self.exchange, body=json.dumps(ret))

        channel.basic_consume(callback, queue=self.msgQueue, no_ack=True)
        channel.start_consuming()

