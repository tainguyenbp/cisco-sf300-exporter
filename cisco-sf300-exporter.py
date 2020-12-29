from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException,NetMikoAuthenticationException
from paramiko.ssh_exception import SSHException
from http.server import HTTPServer

import logging
import time
import socket
import threading
from prometheus.collectors import Gauge
from prometheus.registry import Registry
from prometheus.exporter import PrometheusMetricHandler
import psutil
import re

logging.basicConfig(filename="/var/log/cisco-sf300-exporter.log", level=logging.DEBUG)

PORT_NUMBER = 9253

switch_cisco_sf300 = {
    'device_type': 'cisco_s300',
    'host':   '192.168.1.1',
    'username': 'admin',
    'password': 'admin',
    'port' : 8222,
    'secret': 'admin',
    'verbose': False,
    'timeout': 60,
    'global_delay_factor': 3,
    'conn_timeout': 60,
    'blocking_timeout': 20,
}

def draytek_gather_data(registry):
    host = '192.168.1.1'
    """Gathers the metrics"""

    # Get the host name of the machine

    metric_cpu_5_seconds = Gauge("switch_cisso_sf300_cpu_5_seconds", "switch cisco sf300 cpu usage 5 seconds", {'host': host})
    metric_cpu_1_minutes = Gauge("switch_cisso_sf300_cpu_1_minutes", "switch cisco sf300 cpu usage 1 minutes", {'host': host})
    metric_cpu_5_minutes = Gauge("switch_cisso_sf300_cpu_5_minutes", "switch cisco sf300 cpu usage 5 minutes", {'host': host})

    registry.register(metric_cpu_5_seconds)
    registry.register(metric_cpu_1_minutes)
    registry.register(metric_cpu_5_minutes)
    
    while True:
        time.sleep(1)
        mode_enable = 'enable'
  
        net_connect_device = ConnectHandler(**switch_cisco_sf300)
        net_connect_device.enable()
        
        command_show_cpu = 'show cpu utilization'

        result_run_command_cpu = net_connect_device.send_command(command_show_cpu, expect_string=r'#')
        
        [cpu_5_seconds, cpu_1_minutes, cpu_5_minutes] = re.findall("\d+", result_run_command_cpu)

        metric_cpu_5_seconds.set({},cpu_5_seconds)
        metric_cpu_1_minutes.set({},cpu_1_minutes)
        metric_cpu_5_minutes.set({},cpu_5_minutes)    

        net_connect_device.disconnect()

if __name__ == '__main__':
#    gather_data()
    # Create the registry
    registry = Registry()

    # Create the thread that gathers the data while we serve it
    thread = threading.Thread(target=draytek_gather_data, args=(registry, ))
    thread.start()

    # Set a server to export (expose to prometheus) the data (in a thread)
    try:
        # We make this to set the registry in the handler
        def handler(*args, **kwargs):
            PrometheusMetricHandler(registry, *args, **kwargs)

        server = HTTPServer(('', PORT_NUMBER), handler)
        server.serve_forever()

    except KeyboardInterrupt:
        server.socket.close()
        thread.join()

