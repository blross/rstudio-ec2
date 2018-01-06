#!/usr/bin/env python
import pickle
import subprocess
from sys import argv

import boto3

from resources.attributes import *


ec2 = boto3.resource('ec2')

file_name = argv[1]

with open(CONFIG_PICKLE_FILE_NAME, 'rb') as f:
    config_dict = pickle.load(f)

instances = ec2.instances.filter(InstanceIds=config_dict['instance_ids'])
public_ips = [instance.public_ip_address
              for instance in instances]

subprocess.run(['scp',
                '-i', PEM_FILE_NAME,
                '-o', 'StrictHostKeyChecking=no',
                USERNAME + '@' + str(public_ips[0]) + ':' \
                + file_name,
                '.'])
