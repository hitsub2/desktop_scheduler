#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import django
path = '/var/www/ecscloud_web/ecscloud_web'
if path not in sys.path:
    sys.path.append(path)
path = '/var/www/ecscloud_web/.venv/lib64/python2.7/site-packages'
if path not in sys.path:
    sys.path.append(path)
path = '/var/www/ecscloud_web/.venv/lib64/python2.7'
if path not in sys.path:
    sys.path.append(path)
print sys.path

os.environ["DJANGO_SETTINGS_MODULE"] = 'ecscloud_web.settings'
django.setup()

import logging
import pika
import json
import uuid
from django.conf import settings
from common.rabbitmq_service import RabbitMQService


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='myapp.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
LOG = logging.getLogger(__name__)


def get_uuid():
    s_uuid=str(uuid.uuid4())
    l_uuid = s_uuid.split('-')
    s_uuid = ''.join(l_uuid)
    return s_uuid


LOG.info(json.dumps(settings.WORKORDER_RABBITMQ_PROP))
# send message
mq_sender = RabbitMQService(settings.WORKORDER_RABBITMQ_PROP)
workOrderId = get_uuid()
workorder_info = {
    "workOrderId": workOrderId,  # "1b3adb663c6d4b758e5360f767ef35ee",
    "workOrderNo": "20151112150857104803",
    "workOrderType": 1,
    "workOrderConfig": {
        "payPattern": "month"
    },
    "accountType": 4,
    "masterOrderId": "6d4ebf1bcfba4a28a354edacca9ae3e4",
    "orderId": "4af3b5d306eb46a3bfc47d127e09acde",
    "innerOrderId": "14a72dc107854e8db73b1b7991fb437e",
    "accountId": "051682e703624f1185fccfab9ae1f123",
    "userId": "614c1f6670484127bb1478a1a1d145fa",
    "serviceTag": "VMS",
    "resourceId": "3b22631e801c4860a4bb420ab6edbdd0",
    "resourceType": "VM",
    "cycleType": 3,
    "workOrderItems": [
        {
            "workOrderItemId": get_uuid(),
            "workOrderItemNo": "20151112150857115903",
            "workOrderId": workOrderId,
            "masterOrderId": "6d4ebf1bcfba4a28a354edacca9ae3e4",
            "orderId": "4af3b5d306eb46a3bfc47d127e09acde",
            "innerOrderId": "14a72dc107854e8db73b1b7991fb437e",
            "innerOrderItemId": "54e64ecc1fae49199aa1ebee49f94bcc",
            "salesEntryId": "17ed2e07cf8111e39c2b9a348d686bbe",
            "productId": "461bb2f4d9414769b2b62d21cf2a7add",
            "workOrderItemConfig": {
                "workOrderCount": 1,
                "value": 2,
                "number": 2,
                "zoneId": "a6df949281904fe18ba877c0ded33199",
                "vpc_name":"myvpc-001",
                "vpc_net_segment":"192.168.0.0/16",
                "cycleCnt": 1,
                "cycleType": 3,
                # Appended
                "name": "network001",
                "cidr": "192.168.0.0/16",
                "dns1": "114.114.114.114",
                "dns2": "8.8.8.8",
                "dhcp": "1"
            },
            "master": "false",
            "masterResourceId": "3b22631e801c4860a4bb420ab6edbdd0",
            "resourceId": "076c75a8fcd34a0a8283490a4b40c6c9",
            "serviceTag": "VMS",
            "resourceType": "NETWORK",
            "cycleType": 3,
            "orderItemId": "7012b1f682974d74828de0874405e3c7"
        }
    ]
}
mq_sender.send_msg(workorder_info)
LOG.info("send msg %s", workorder_info)
mq_sender.close()
print "finish send mq"

