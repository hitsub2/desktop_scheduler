# -*- coding: utf-8 -*-

from scheduler import cloud_api

import logging

LOG = logging.getLogger(__name__)

def _create(msg):
    res = {}
    for item in msg['workOrderItems']:
        res[item['resourceType']] = item

    netInfo = {
        'vpc_name': [unicode(res['NETWORK']['workOrderItemConfig']['vpcName'])],
        'vpc_cidr': [unicode(res['NETWORK']['workOrderItemConfig']['vpcCidr'])],
        'enable_dhcp': [unicode(res['NETWORK']['workOrderItemConfig']['enableDhcp'])],
        'dns1': [unicode(res['NETWORK']['workOrderItemConfig']['DNS1'])],
        'dns2': [unicode(res['NETWORK']['workOrderItemConfig']['DNS2'])],
        'address': [unicode(res['NETWORK']['workOrderItemConfig']['subnetCidr'])],
        'subnet_gateway': [unicode(res['NETWORK']['workOrderItemConfig']['subnetGateway'])],
        'subnet_name': [unicode(res['NETWORK']['workOrderItemConfig']['subnetName'])],
        'floating_ip': {
            'bandwidthName': [unicode(res['NETWORK']['workOrderItemConfig']['bandwidthName'])],
            'bandwidthValue': [unicode(res['NETWORK']['workOrderItemConfig']['bandwidthValue'])],
            'floatingIpNum': [unicode(res['NETWORK']['workOrderItemConfig']['floatingIpNum'])]
        },
        # Rest API authentication params
        'os_id': res['NETWORK']['workOrderItemConfig']['platformId'],
        'ct_user_id': msg['userId'],
        'ct_account_id': msg['accountId'],
    }

    LOG.info("Call cloud API: create_network, parameter is %s." % netInfo)
    return cloud_api.create_network(netInfo)

def _upgrade(msg):
    pass

def _delete(msg):
    ret = []
    # TODO: concurrent
    for item in msg['workOrderItems']:
        netInfo = {
            'action': [u'delete'],
            'network_id': [unicode(item['workOrderItemConfig']['networkId'])],
            # Rest API authentication params
            'os_id': item['workOrderItemConfig']['platformId'],
            'ct_user_id': msg['userId'],
            'ct_account_id': msg['accountId'],
        }
        LOG.info("Call cloud API: create_action, parameter is %s." % netInfo)
        re1 = cloud_api.network_action(netInfo)

        floatingInfo = {
            'action': [u'release'],
            'floating_id': [unicode(item['workOrderItemConfig']['floatingIpId'])],
            # Rest API authentication params
            'os_id': item['workOrderItemConfig']['platformId'],
            'ct_user_id': msg['userId'],
            'ct_account_id': msg['accountId'],
        }
        LOG.info("Call cloud API: floating_action, parameter is %s." % floatingInfo)
        re2 = cloud_api.floating_action(floatingInfo)

        ret.append({
            'net': (item['workOrderItemConfig']['networkId'], re1),
            'fip': (item['workOrderItemConfig']['floatingIpId'], re2)
        })

    return ret


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
