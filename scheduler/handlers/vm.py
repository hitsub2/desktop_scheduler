# -*- coding: utf-8 -*-

from scheduler import cloud_api
from utils import get_running_ip_by_settings

import logging, json
import ast

LOG = logging.getLogger(__name__)

def _create(msg):
    res = {}
    
    for item in msg['workOrderItems']:
        res[item['resourceType']] = item

    # image_id
    # LOG.info("Call cloud API: get_image_id_by_name, parameter is %s." % \
    #         {'image_name': res['VM']['workOrderItemConfig']['osType']})
    # image_info = cloud_api.get_image_id_by_name( {'image_name': res['VM']['workOrderItemConfig']['osType']})
    image_id = None
    if type(res['VM']['workOrderItemConfig']) == unicode:
        _image_id = json.loads(res['VM']['workOrderItemConfig'])
        image_id = _image_id['imageId']
    else:
        image_id = res['VM']['workOrderItemConfig']['imageId']

    # network_id
    # if res['NETWORK']['workOrderItemConfig']['networkId'] == '':
        # # TODO: new a network and get the network id
        # network_id = u'8'
    # else:
        # network_id = unicode(res['NETWORK']['workOrderItemConfig']['networkId'])
    if res.has_key('EBS') :
        LOG.info("res has key EBS")
        data_volumes = [json.dumps({ \
                'type': dv['type'], \
                'size': dv['size'] \
            }) for dv in json.loads(res['EBS']['workOrderItemConfig'])['dataVolumes'] if res.has_key('EBS')]
    else:
        LOG.info("res has no key EBS")
        data_volumes=None

    LOG.info("start to get networkCards")
    networkCards = None
    if type(res['VM']['workOrderItemConfig']) == unicode:
        _networkCards = json.loads(res['VM']['workOrderItemConfig'])
        networkCards = _networkCards['networkCards']
    else:
        networkCards = res['VM']['workOrderItemConfig']['networkCards']
    LOG.info("networkCards is" + str(networkCards))
    if networkCards:
        network_cards=[]
        for nc in networkCards:
            temp_dict={}
            LOG.info("nc is" + str(nc))
            temp_dict['subnet_id']=nc['subnetId']
            temp_dict['subnet_name']=nc['subnetName']
            temp_dict['master']=nc['master']
            if nc.has_key('ip'):
                temp_dict['ip']=nc['ip']
            network_cards.append(temp_dict)

        # network_cards = [json.dumps({ \
        #         'subnet_id': nc['subnetId'],
        #         'subnet_name': nc['subnetName'],
        #         'ip': nc['ip'],
        #         'master': nc['master']
        #     }) for nc in networkCards]

    else:
        network_cards = None

    LOG.info("start to composite vminfo")
    try:
        vminfo = {
        #Rest API authentication params
        'os_id': json.loads(res['VM']['workOrderItemConfig'])['platformId'],
        'ct_user_id': msg['userId'],
        'ct_account_id': msg['accountId'],
        #vmInfo
        'pay_type': json.loads(msg['workOrderConfig'])['payPattern'],
        'name': json.loads(res['VM']['workOrderItemConfig'])['vmName'],
        'network_id': json.loads(res['NETWORK']['workOrderItemConfig'])['networkId'],
        'image': image_id,
        'instance': json.loads(res['VM']['workOrderItemConfig'])['vmNumber'],
        'memory': json.loads(res['VM']['workOrderItemConfig'])['memSize'],
        'image_info': image_id,
        'password': json.loads(res['VM']['workOrderItemConfig'])['rootPassword'],
        'pay_num': json.loads(res['VM']['workOrderItemConfig'])['vmNumber'],
        'cpu': json.loads(res['VM']['workOrderItemConfig'])['cpuNum'],
        # NOTE: Additional parameters
        'security_group_id': json.loads(res['VM']['workOrderItemConfig'])['securityGroupId'],
        'exist_floating_ip': json.loads(res['NETWORK']['workOrderItemConfig'])['existFloatingIP'],
        'newBandwidthValue': int(json.loads(res['NETWORK']['workOrderItemConfig'])['newBandwidthValue']),
        #Fix error
        'sys_disk':json.loads(res['VM']['workOrderItemConfig'])['sysVolumeSize'],
        'sys_disk_type':json.loads(res['VM']['workOrderItemConfig'])['sysVolumeType'],
        'scheduler_url': get_running_ip_by_settings()
        }
    except Exception as e:
        LOG.info(str(e))

    LOG.info("8888")
    if network_cards:
        vminfo['network_cards']=network_cards
    LOG.info("8888")
    if data_volumes:
        vminfo['data_volumes']=data_volumes

    LOG.info("8888")
    if res.has_key('EBS'):
        try:
            vminfo['sys_disk']=json.loads(res['EBS']['workOrderItemConfig'])['sysVolumeSize']
            vminfo['sys_disk_type']=json.loads(res['EBS']['workOrderItemConfig'])['sysVolumeType']

        except:
            pass




    LOG.info("Call cloud API: create_vm, parameter is %s." % vminfo)
    return cloud_api.create_vm(vminfo)


# recode the create VM message
# Finished ADD Log AT 2017-6-5 17:47
# Finished Test This Function AT 2017-6-5 17:36
def re_create(msg):
    LOG.info("Start Creating parse VM message")

    # Create Resource Type From msg
    # There Is Three Resource Types,VM EBS NETWORK
    def construt_type(decode_msg):
        LOG.info("Decode VM message")
        resources={}
        for item in decode_msg['workOrderItems']:
            resources[item['resourceType']] = item
            resources['workorder']=''
        LOG.info("Decode VM message Finshed")
        return  resources
    resources=construt_type(msg)

    # Get WorkOrder ID
    def get_workorder(decode_msg):
        LOG.info("Decode VM message")
        resources_list=[]
        for item in decode_msg['workOrderItems']:
            resources = {}
            resources['type'] = item['resourceType']
            resources['workorder']=item['workOrderItemId']
            resources_list.append(resources)
        LOG.info("Decode VM message Finshed")
        return  resources_list
    workinfo=get_workorder(msg)


    # Get UserInfo
    def account_info(msg,decode_msg):
        LOG.info("Start Getting User from VM message")
        userinfo={}
        if msg.has_key("userId"):
            userinfo['ct_user_id']=msg['userId']
        if msg.has_key('accountId'):
            userinfo['accountId']=msg['accountId']
        if decode_msg.has_key('VM'):
            if decode_msg['VM'].has_key('workOrderItemConfig'):
                config_msg=json.loads(decode_msg['VM']['workOrderItemConfig'])
                if config_msg.has_key('platformId'):
                    userinfo['os_id']=config_msg['platformId']
        LOG.info("Getting User from VM message Fishied")
        return userinfo if len(userinfo)==3 else False


    # Get ImageID
    def get_imageid(structor):
        LOG.info("Start Getting ImageID from VM message")
        image={}
        if 'workOrderItemConfig' in structor['VM'].keys():
            config_msg = json.loads(structor['VM']['workOrderItemConfig'])
            if 'imageId' in config_msg.keys():
                image['image'] = config_msg['imageId']
                image['image_info'] =image['image']
        LOG.info("Start Getting ImageID from VM message Fishied")
        return image


    # Get EBS INFO
    def get_ebs(structor):
        LOG.info("Start Getting EBS from VM message")
        data_info={}
        if structor.has_key('EBS'):
            if structor['EBS'].has_key('workOrderItemConfig'):
                config_msg=json.loads(structor['EBS']['workOrderItemConfig'])
                if config_msg.has_key('dataVolumes'):
                    data_volumes = [json.dumps({ \
                            'type': dv['type'], \
                            'size': dv['size'] \
                        }) for dv in config_msg['dataVolumes']]
                    data_info['data_volumes']=data_volumes
        LOG.info("Getting EBS from VM message Finshed")
        return data_info


    # Get Netcards
    def get_netcards(structor):
        LOG.info("Start Getting NetCards from VM message")
        cardinfo={}
        if structor.has_key('VM'):
            if structor['VM'].has_key('workOrderItemConfig'):
                config_msg=json.loads(structor['VM']['workOrderItemConfig'])
                if config_msg.has_key('networkCards'):
                    networkCards=config_msg['networkCards']

        if networkCards:
            network_cards = []
            for nc in networkCards:
                temp_dict = {}
                temp_dict['subnet_id'] = nc['subnetId']
                temp_dict['subnet_name'] = nc['subnetName']
                temp_dict['master'] = nc['master']
                if nc.has_key('ip'):
                    temp_dict['ip'] = nc['ip']
                network_cards.append(temp_dict)
            cardinfo['network_cards']= network_cards
        LOG.info("Getting EBS from VM message Finished")
        return cardinfo


    # GET NetWork
    def get_network(strucor):
        LOG.info("Start Getting NetWork from VM message")
        networks={}
        if strucor.has_key('NETWORK'):
            if strucor['NETWORK'].has_key('workOrderItemConfig'):
                config_msg = json.loads(strucor['NETWORK']['workOrderItemConfig'])
                if config_msg.has_key('networkId'):
                    networks['network_id']=config_msg['networkId']
                if config_msg.has_key('existFloatingIP'):
                    networks['exist_floating_ip']=config_msg['existFloatingIP'],
                if config_msg.has_key('newBandwidthValue'):
                    networks['newBandwidthValue']=config_msg['newBandwidthValue']
        LOG.info("Getting NetWork from VM message Finshed")
        return networks


    # GET DiskInfo
    def get_diskinfo(strucor):
        LOG.info("Start Getting DiskInfo from VM message")
        disk={}
        if strucor.has_key('VM'):
            if strucor['VM'].has_key('workOrderItemConfig'):
                config_msg = json.loads(strucor['VM']['workOrderItemConfig'])
                if config_msg.has_key('sysVolumeSize'):
                    disk['sys_disk']=config_msg['sysVolumeSize']
                if config_msg.has_key('sysVolumeType'):
                    disk['sys_disk_type']=config_msg['sysVolumeType']
        LOG.info("Start Getting DiskInfo from VM message Finshed")
        return disk


    # Get Instance Info
    def get_instance(strucor):
        LOG.info("Start Getting Instance Info from VM message")
        vminfo={}
        if strucor.has_key('VM'):
            if strucor['VM']['workOrderItemConfig']:
                config_msg = json.loads(strucor['VM']['workOrderItemConfig'])
                if config_msg.has_key('vmName'):
                    vminfo['name']=config_msg['vmName']
                if config_msg.has_key('vmNumber'):
                    vminfo['instance']=config_msg['vmNumber']
                    vminfo['pay_num']=vminfo['instance']
                if config_msg.has_key('memSize'):
                    vminfo['memory']=config_msg['memSize']
                if config_msg.has_key('rootPassword'):
                    vminfo['password']=config_msg['rootPassword']
                if config_msg.has_key('cpuNum'):
                    vminfo['cpu']=config_msg['cpuNum']
                if config_msg.has_key('securityGroupId'):
                    vminfo['security_group_id'] = config_msg['securityGroupId']
        LOG.info("Start Getting Instance Info from VM message Finshed")
        return vminfo


    # Get Pay Type
    def get_paytype(decode_msg):
        LOG.info("Start Getting Paytype Info from VM message")
        pay_info={}
        if decode_msg.has_key('workOrderConfig'):
            config_msg=json.loads(decode_msg['workOrderConfig'])
            if config_msg.has_key('payPattern'):
                pay_info['pay_type']=config_msg['payPattern']
        LOG.info("Getting Paytype Info from VM message Finshed")
        return pay_info


    # Check User Info
    user_info=account_info(msg,resources)
    if not user_info:
        LOG.info("Check Request User Failed")
        return False



    # Build VMInfo
    LOG.info("Building Create Info")
    vminfo=dict(user_info.items()+get_imageid(resources).items()+ \
                get_ebs(resources).items()+get_netcards(resources).items()+ \
                get_network(resources).items()+get_diskinfo(resources).items()+ \
                get_instance(resources).items()+get_paytype(msg).items())
    vminfo['work_order']=workinfo
    vminfo['scheduler_url'] = get_running_ip_by_settings()
    LOG.info("Building Create Info Finshed,Start Creating VM")

    return cloud_api.create_vm(vminfo)


def _upgrade(msg):
    ret = []
    # TODO: concurrent
    for item in msg['workOrderItems']:
        info = {
            'id': item['workOrderItemConfig']['instanceId'],
            'vcpu': item['workOrderItemConfig']['cpuNum'],
            # NOTE: There isn't this key in message.
            'sys_disk': [u'10'],
            'memory': item['workOrderItemConfig']['memSize'],
            # Rest API authentication params
            'os_id': item['workOrderItemConfig']['platformId'],
            'ct_user_id': msg['userId'],
            'ct_account_id': msg['accountId'],
        }
        LOG.info("Call cloud API: resize_instance, parameter is %s." % info)
        ret.append(cloud_api.resize_instance(info))

    return ret

def _delete(msg):
    ret = []
    # TODO: concurrent
    for item in msg['workOrderItems']:
        info = {
            'action': 'terminate',
            'instance': item['workOrderItemConfig']['instanceId'],
            'release_floating_ip': item['workOrderItemConfig']['releaseFloatingIP'],
            'delete_data_volume': item['workOrderItemConfig']['deleteDataVolume'],
            # Rest API authentication params
            'os_id': item['workOrderItemConfig']['platformId'],
            'ct_user_id': msg['userId'],
            'ct_account_id': msg['accountId'],
        }
        LOG.info("Call cloud API: instance_action, parameter is %s." % info)
        instance_id = item['workOrderItemConfig']['instanceId']
        ret.append(cloud_api.instance_action(info, instance_id))

    return ret

def _degrade(msg):
    return _upgrade(msg)

def handler(msg):
    if msg['workOrderType'] == 1:
        return re_create(msg)
        # return _create(msg)
    elif msg['workOrderType'] == 3:
        return _upgrade(msg)
    elif msg['workOrderType'] == 7:
        return _delete(msg)
    elif msg['workOrderType'] == 13:
        return _degrade(msg)
    else:
        raise ValueError("Unknown work order type.")

