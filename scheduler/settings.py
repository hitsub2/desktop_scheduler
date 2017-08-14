# -*- coding: utf-8 -*-

# RabbitMQ

WORKORDER_RABBITMQ_PROP={
    "rabbitmq.host": "192.168.1.48",
    "rabbitmq.vhost": "/",
    "rabbitmq.username":"guest",
    "rabbitmq.password":"guest",
    "rabbitmq.port":5672,
    "rabbitmq.exchange_name":"openstack",
    "rabbitmq.exchange_type":"topic",
    "rabbitmq.exchange_durable":False,
    "rabbitmq.exchange_auto_delete": False,
    "rabbitmq.queue_durable": False,
    "rabbitmq.queue_auto_delete": False,
    "rabbitmq.queue_exclusive": False,
    "rabbitmq.routing_key":"VMS1.*",
    "rabbitmq.prefetch_count": 32,
    "rabbitmq.workOrderQueue":"VMS1.workOrderResourceAMQP"
}


WORKORDER_RABBITMQ_REPORT={
    "rabbitmq.host": "192.168.1.48",
    "rabbitmq.vhost": "/",
    "rabbitmq.username":"guest",
    "rabbitmq.password":"guest",
    "rabbitmq.port":5672,
    "rabbitmq.exchange_name":"openstack",
    "rabbitmq.exchange_type":"topic",
    "rabbitmq.exchange_durable":False,
    "rabbitmq.exchange_auto_delete": False,
    "rabbitmq.queue_durable": False,
    "rabbitmq.queue_auto_delete": False,
    "rabbitmq.queue_exclusive": False,
    "rabbitmq.routing_key":"VMS1.*",
    "rabbitmq.prefetch_count": 32,
    "rabbitmq.workOrderQueue":"VMS1.workOrderResourceAMQP"
}

# Log
log_file_path = '/var/log/scheduler.log'

# Ecscloud
ecs_addr = "http://172.18.143.37:8000"
ecs_admin_usr = 'gtt'
ecs_admin_pwd = '123qweASD'

# Thread Pool Size
thread_pool_size = 8


