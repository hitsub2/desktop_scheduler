# -*- coding: utf-8 -*-

import requests
import json
import logging

from settings import ecs_addr, ecs_admin_usr, ecs_admin_pwd

LOG = logging.getLogger(__name__)

def _get_client(usr, pwd):
    URL = ecs_addr + '/login'

    c = requests.session()
    try:
        c.get(URL, verify=False, timeout=2)

        login_data = dict(username=usr, \
                password=pwd, \
                next='/')
        login_return = c.post(URL, \
                data=login_data, \
                headers=dict(Referer=URL), \
                timeout=2)
    except Exception, e:
        LOG.error(e)
        return None

    return c

def _do_get(URL, headers, data, usr, pwd):
    # c = _get_client(usr, pwd)
    c = requests.session()
    if not c:
        return {
            "success": False,
            "data": "Get verified client failed"
        }
    try:
        re = c.get(URL, params=data, headers=headers, timeout=2)
        LOG.debug(re.status_code)
        ret = {
            "success": True,
            "status": re.status_code,
            "data": re.json()
        }
    except Exception, e:
        LOG.error("%s, %s, %s" % (URL, e, data))
        ret = {
            "success": False,
            "data": str(e)
        }

    return ret

def _do_post(URL, headers, data, usr, pwd):
    #c = _get_client(usr, pwd)
    c = requests.session()
    if not c:
        return {
            "success": False,
            "data": "Get verified client failed"
        }
    try:
        re = c.post(URL, data=data, headers=headers, timeout=35)
        LOG.debug(re.status_code)
        ret = {
            "success": True,
            "status": re.status_code,
            "data": re.json()
        }
    except Exception, e:
        LOG.error("%s, %s, %s" % (URL, e, data))
        ret = {
            "success": False,
            "data": str(e)
        }

    return ret

def message_persistance(msg, usr=ecs_admin_usr, pwd=ecs_admin_pwd):
    URL = ecs_addr + '/api/work_order/create/'
    headers = {'Content-Type': 'application/json'}
    return _do_post(URL, headers, json.dumps(msg), usr, pwd)

def create_vm(info, usr=ecs_admin_usr, pwd=ecs_admin_pwd):
    URL = ecs_addr + '/api/instances/create/'
    headers = {'Content-Type': 'application/json'}
    return _do_post(URL, headers, json.dumps(info), usr, pwd)

def instance_action(info, instance_id, usr=ecs_admin_usr, pwd=ecs_admin_pwd):
    URL = ecs_addr + '/api/instances/' + instance_id + '/action/'
    return _do_post(URL, dict(Referer=URL), info, usr, pwd)

def resize_instance(info, usr=ecs_admin_usr, pwd=ecs_admin_pwd):
    URL = ecs_addr + '/api/instances/c/'
    return _do_post(URL, dict(Referer=URL), info, usr, pwd)

def create_network(info, usr=ecs_admin_usr, pwd=ecs_admin_pwd):
    URL = ecs_addr + '/api/networks/create/'
    return _do_post(URL, dict(Referer=URL), info, usr, pwd)

def network_action(info, usr=ecs_admin_usr, pwd=ecs_admin_pwd):
    URL = ecs_addr + '/api/networks/delete/'
    return _do_post(URL, dict(Referer=URL), info, usr, pwd)

def create_volume(info, usr=ecs_admin_usr, pwd=ecs_admin_pwd):
    URL = ecs_addr + '/api/volumes/create/'
    return _do_post(URL, dict(Referer=URL), info, usr, pwd)

def extend_volume(info, usr=ecs_admin_usr, pwd=ecs_admin_pwd):
    URL = ecs_addr + '/api/volumes/extend/'
    return _do_post(URL, dict(Referer=URL), info, usr, pwd)

def list_volume_by_instance(info, usr=ecs_admin_usr, pwd=ecs_admin_pwd):
    URL = ecs_addr + '/api/volumes/search/'
    return _do_post(URL, dict(Referer=URL), info, usr, pwd)

def volume_action(info, usr=ecs_admin_usr, pwd=ecs_admin_pwd):
    URL = ecs_addr + '/api/volumes/action/'
    return _do_post(URL, dict(Referer=URL), info, usr, pwd)

def verify_user(info, usr=ecs_admin_usr, pwd=ecs_admin_pwd):
    URL = ecs_addr + '/api/account/verify/'
    return _do_post(URL, dict(Referer=URL), info, usr, pwd)

def get_image_id_by_name(image_name, usr=ecs_admin_usr, pwd=ecs_admin_pwd):
    URL = ecs_addr + '/api/images/get-image-by-name/'
    return _do_get(URL, dict(Referer=URL), image_name, usr, pwd)

def create_floating(info, usr=ecs_admin_usr, pwd=ecs_admin_pwd):
    URL = ecs_addr + '/api/floatings/create/'
    return _do_post(URL, dict(Referer=URL), info, usr, pwd)

def floating_action(info, usr=ecs_admin_usr, pwd=ecs_admin_pwd):
    URL = ecs_addr + '/api/floatings/action/'
    return _do_post(URL, dict(Referer=URL), info, usr, pwd)

def list_fip_by_instance(instance_id, usr=ecs_admin_usr, pwd=ecs_admin_pwd):
    URL = ecs_addr + '/api/floatings/' + instance_id + '/list_fip_by_instance/'
    return _do_get(URL, dict(Referer=URL), {}, usr, pwd)

def create_keypair(info, usr=ecs_admin_usr, pwd=ecs_admin_pwd):
    URL = ecs_addr + '/api/keypairs/create/'
    return _do_post(URL, dict(Referer=URL), info, usr, pwd)

