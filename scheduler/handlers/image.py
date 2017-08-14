# -*- coding: utf-8 -*-

from scheduler import cloud_api

def _create(msg):
    pass

def _upgrade(msg):
    pass

def _delete(msg):
    pass

def _degrade(msg):
    pass

def handler(msg):
    if msg['workOrderType'] == 1:
        return _create(msg)
    elif msg['workOrderType'] == 3:
        return _upgrade(msg)
    elif msg['workOrderType'] == 7:
        return _delete(msg)
    elif msg['workOrderType'] == 13:
        return _degrade(msg)
    else:
        raise ValueError("Unknown work order type.")

