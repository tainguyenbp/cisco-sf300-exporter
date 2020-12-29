# Cisco SF300 exporter for hardware CPU. written in Python with pluggable metric collectors.
This project is built with:

- Python 3.6.x

And is packaged as a Docker container. The two top level dependencies are:

- prometheus-client==0.0.21
- netmiko==3.3.0
- cryptography==2.8
- pip==9.0.3
- prometheus==0.3.0
- psutil==5.7.2



See the [requirements file](./requirements.txt) for more details.

## Prometheus

monitoring application.

To instrument our Python code we need to manipulate the metrics each
time a new HTTP request is received.

See [the application](./cisco-sf300_exporter.py) for more details.

## Building

This project is automatically built by Docker Automated Builds.

To build manually:
```
git clone https://github.com/tainguyenbp/cisco-sf300_exporter.git
cd cisco-sf300_exporter
docker build -t cisco-sf300_exporter/tainguyenbp:v1.1 .
```

## Running

Simply open port 9253 when running as a container:

`docker-comose up --build -d`

## Access URL check metrics

access url with port 9253:

`curl http://192.168.1.10:9253/metrics`

## Add config to the prometheus.yml file:

```
  - job_name: 'cisco_sf300_exporter'
    scrape_interval: 60s
    scrape_timeout: 60s
    static_configs:
    - targets: ['192.168.1.10:9253']
```
## metric collects:

```
# HELP switch_cisso_sf300_cpu_1_minutes switch cisco sf300 cpu usage 1 minutes
# TYPE switch_cisso_sf300_cpu_1_minutes gauge
switch_cisso_sf300_cpu_1_minutes{host="192.168.1.1"} 34
# HELP switch_cisso_sf300_cpu_5_minutes switch cisco sf300 cpu usage 5 minutes
# TYPE switch_cisso_sf300_cpu_5_minutes gauge
switch_cisso_sf300_cpu_5_minutes{host="192.168.1.1"} 32
# HELP switch_cisso_sf300_cpu_5_seconds switch cisco sf300 cpu usage 5 seconds
# TYPE switch_cisso_sf300_cpu_5_seconds gauge
switch_cisso_sf300_cpu_5_seconds{host="192.168.1.1"} 1
```
