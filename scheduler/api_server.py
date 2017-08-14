# -*- coding: utf-8 -*-
import web
import json
import logging

from settings import WORKORDER_RABBITMQ_REPORT
from api_settings import api_port,STATUS_OK
from mqhandler import MQ_Send_Service

LOG = logging.getLogger()


urls = (
    '/api/test', 'test',
    '/api/resource/status', 'resource_stat',
    # '/api/proc/watch', 'watch_process',
    # '/api/proc/unwatch', 'unwatch_process',
    # '/api/vm/status', 'vm_status'
)


class resource_stat:
    def POST(self):
        data = json.loads(web.input().data)
        data_dumps = json.dumps(data)
        h = MQ_Send_Service(WORKORDER_RABBITMQ_REPORT)
        h.send_message(data_dumps)
        return json.dumps({"errorCode":STATUS_OK, "errorMsg": "mshandler report to rabbit success"})

    def GET(self):
        print "start to return"
        return json.dumps({"resource":"OK"})

class test:
    def POST(self):
        return json.dumps({"errorCode":STATUS_OK, "errorMsg": "mshandler post action is ok"})

    def GET(self):
        print "start to return"
        return json.dumps({"errorCode":STATUS_OK, "errorMsg": "mshandler api server is ok"})

class MyApplication(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))

def run_server():
    app = MyApplication(urls, globals(), True)
    app.run(port=api_port)

if __name__ == "__main__":
    app = MyApplication(urls, globals(), True)
    app.run(port=api_port)
