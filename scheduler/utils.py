import netifaces as ni
from api_settings import api_address,api_port

def get_running_ip_by_settings():
    scheduler_url = "http://" + str(api_address) + ":" + str(api_port)
    return scheduler_url


def get_running_ip():
    interfaces = ni.interfaces()
    print interfaces
    ni.ifaddresses('em1')
    ip = ni.ifaddresses('em1')[2][0]['addr']
    print ip  # should print "192.168.100.37"


get_running_ip()