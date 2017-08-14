# -*- coding: utf-8 -*-

from scheduler import cloud_api

import logging

LOG = logging.getLogger(__name__)

def _create(msg):
    res = {}
    for item in msg['workOrderItems']:
        res[item['resourceType']] = item
    volumeInfo = {
        'pay_type': [unicode(msg['workOrderConfig']['payPattern'])],
        'pay_num': [unicode(res['EBS']['workOrderItemConfig']['volumeNumber'])],
        'name': [unicode(res['EBS']['workOrderItemConfig']['volumeName'])],
        'size': [unicode(res['EBS']['workOrderItemConfig']['volumeSize'])],
        # NOTE: additional paramters
        'volume_type': [unicode(res['EBS']['workOrderItemConfig']['volumeType'])],
        'backup_volume_id': [unicode(res['EBS']['workOrderItemConfig']['backupVolumeId'])],
        # Rest API authentication params
        'os_id': res['EBS']['workOrderItemConfig']['platformId'],
        'ct_user_id': msg['userId'],
        'ct_account_id': msg['accountId'],
    }
    LOG.info("Call cloud API: create_volume, parameter is %s." % volumeInfo)
    return cloud_api.create_volume(volumeInfo)

def _upgrade(msg):
    ret = []
    # TODO: concurrent
    for item in msg['workOrderItems']:
        info = {
            'volume_id': [unicode(item['workOrderItemConfig']['volumeId'])],
            # NOTE: new_size is the size after extending, may not be compatible with addVolumeSize
            'new_size': [unicode(item['workOrderItemConfig']['addVolumeSize'])],
            # Rest API authentication params
            'os_id': item['workOrderItemConfig']['platformId'],
            'ct_user_id': msg['userId'],
            'ct_account_id': msg['accountId'],
        }
        LOG.info("Call cloud API: extend_volume, parameter is %s." % info)
        ret.append(cloud_api.extend_volume(info))

    return ret

def _delete(msg):
    ret = []
    # TODO: concurrent
    for item in msg['workOrderItems']:
        info = {
            'action': [u'delete'],
            'volume_id': [unicode(item['workOrderItemConfig']['volumeId'])],
            # Rest API authentication params
            'os_id': item['workOrderItemConfig']['platformId'],
            'ct_user_id': msg['userId'],
            'ct_account_id': msg['accountId'],
        }
        LOG.info("Call cloud API: volume_action, parameter is %s." % info)
        ret.append(cloud_api.volume_action(info))

    return ret

def handler(msg):
    if msg['workOrderType'] == 1:
        return _create(msg)
    elif msg['workOrderType'] == 3:
        return _upgrade(msg)
    elif msg['workOrderType'] == 7:
        return _delete(msg)
    else:
        raise ValueError("Unknown work order type.")

