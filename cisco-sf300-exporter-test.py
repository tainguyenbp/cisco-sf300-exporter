from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException,NetMikoAuthenticationException
from paramiko.ssh_exception import SSHException
from http.server import HTTPServer
import re
import requests
from netmiko import ConnectHandler
import logging
from datetime import datetime, timedelta
from netmiko.ssh_exception import NetMikoTimeoutException,NetMikoAuthenticationException
from paramiko.ssh_exception import SSHException
logging.basicConfig(filename="/var/log/cisco-sf300-exporter-test.log", level=logging.DEBUG)
#logging.getLogger('paramiko.transport').disabled = True
cisco_ios = {
    'device_type': 'cisco_s300',
    'host':   '192.168.1.1',
    'username': 'admin',
    'password': 'admin',
    'port' : 8222,
    'secret': 'admin',
    'blocking_timeout': 20,
    'verbose': False,
    'timeout': 60,
    'global_delay_factor': 3
}

mode_enable = 'enable'
  
net_connect_device = ConnectHandler(**cisco_ios)
net_connect_device.enable()
        
command_show_cpu = 'show cpu utilization'

result_run_command_cpu = net_connect_device.send_command(command_show_cpu, expect_string=r'#')
      
[cpu_5_seconds, cpu_1_minutes, cpu_5_minutes] = re.findall("\d+", result_run_command_cpu)

print("Load Average 5 seconds: "+ cpu_5_seconds)
print("Load Average 1 minutes: "+ cpu_1_minutes)
print("Load Average 5 minutes: "+ cpu_5_minutes)

net_connect_device.disconnect()