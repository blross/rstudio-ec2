#!/usr/bin/env python
import os
import pickle
import time

import boto3

from resources.attributes import *


ec2 = boto3.resource('ec2')

with open(CONFIG_PICKLE_FILE_NAME, 'rb') as f:
    config_dict = pickle.load(f)

instances = ec2.instances.filter(InstanceIds=config_dict['instance_ids'])
groups = ec2.security_groups.filter(GroupIds=config_dict['group_ids'])
key_pairs = ec2.key_pairs.filter(KeyNames=config_dict['key_pair_names'])

instances.terminate()

for key_pair in key_pairs:
    key_pair.delete()

# while True:
#     try:
#         for group in groups:
#             group.delete()
#         break
#     except:
#         time.sleep(1)
#         continue

os.remove(CONFIG_PICKLE_FILE_NAME)
os.remove(PEM_FILE_NAME)
