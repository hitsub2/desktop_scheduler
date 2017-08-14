# -*- coding: utf-8 -*-

from mqhandler import MQ_ReceiveService
from api_server import run_server
from settings import WORKORDER_RABBITMQ_PROP, thread_pool_size, log_file_path

import thread
import logging

logging.basicConfig(level=logging.DEBUG, \
        format='[%(asctime)s] %(name)-12s %(levelname)-8s %(message)s', \
        datefmt='%m-%d %H:%M', \
        filename=log_file_path, \
        filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

LOG = logging.getLogger(__name__)

def start_api_server():
    run_server()

def main():
    while True:
        try:
            h = MQ_ReceiveService(WORKORDER_RABBITMQ_PROP, thread_pool_size)
            thread.start_new_thread(start_api_server,())
            h.receive_message()
        except Exception, e:
            LOG.error(e)

if __name__ == '__main__':
    main()

