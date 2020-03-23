#!/usr/bin/env python3
import subprocess
import os
import json
import requests

def cpu_temp():
	thermal_zone = subprocess.Popen(['cat', '/sys/class/thermal/thermal_zone0/temp'], stdout=subprocess.PIPE)
	out, err = thermal_zone.communicate()
	cpu_temp = int(out.decode())/1000
	return cpu_temp

def gpu_temp():
	measure_temp = subprocess.Popen(['/opt/vc/bin/vcgencmd', 'measure_temp'], stdout=subprocess.PIPE)
	out, err = measure_temp.communicate()
	gpu_temp = out.decode().split('=')[1].split('\'')[0]
	return gpu_temp

def send_warning(message):
	dir = os.path.dirname(os.path.abspath(__file__))
	filename = os.path.join(dir,'keys.json')
	f = open(filename, 'r')
	content = f.read()
	f.close()
	data = json.loads(content)
	url = 'https://api.telegram.org/bot{0}/sendMessage'.format(data['token'])
	data = {'chat_id': data['channel_id'], 'text': message}
	r = requests.post(url, data)

def check_temp():
	cpu = cpu_temp()
	gpu = gpu_temp()
	if float(cpu) > 50 or float(gpu) > 50:
		send_warning("CPU: "+str(cpu)+"º\nGPU: "+str(gpu)+"º")

check_temp()

print ("CPU: "+str(cpu_temp())+"º")
print ("GPU: "+str(gpu_temp())+"º")
