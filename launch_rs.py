#!/usr/bin/env python
import getopt
import pickle
import subprocess
import time
import sys

import boto3

from resources.attributes import *


ec2 = boto3.resource('ec2')

# Get commands to run on instance and files to copy to instance
opts, _ = getopt.getopt(sys.argv[1:],
                        's:f:i:m:',
                        ['setup-file=',
                         'files=',
                         'instance-type=',
                         'max-price='])
opt_dict = dict(opts)

setup_file = (opt_dict.get('-s')
              or opt_dict.get('--setup-file'))
files_to_copy = (opt_dict.get('-f')
                 or opt_dict.get('--files')
                 or [])
instance_type = (opt_dict.get('-i')
                 or opt_dict.get('--instance-type')
                 or INSTANCE_TYPE)
max_price = (opt_dict.get('-m')
                 or opt_dict.get('--max-price')
                 or MAX_PRICE)

if setup_file:
    with open(setup_file) as f:
        setup_commands = f.read()
else:
    setup_commands = ''

if files_to_copy:
    files_to_copy = files_to_copy.split(',')

# Initialize security group for instance (if necessary)
try:
    group = ec2.create_security_group(
        GroupName=GROUP_NAME,
        Description=GROUP_DESCRIPTION
    )
    group.authorize_ingress(
        IpPermissions=[
            {
                'FromPort': 22,
                'ToPort': 22,
                'IpProtocol': 'tcp',
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}],
                'Ipv6Ranges': [{'CidrIpv6': '::/0'}],
            },
            {
                'FromPort': 80,
                'ToPort': 80,
                'IpProtocol': 'tcp',
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}],
                'Ipv6Ranges': [{'CidrIpv6': '::/0'}],
            },
            {
                'FromPort': 8787,
                'ToPort': 8787,
                'IpProtocol': 'tcp',
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}],
                'Ipv6Ranges': [{'CidrIpv6': '::/0'}],
            },
            {
                'FromPort': 443,
                'ToPort': 443,
                'IpProtocol': 'tcp',
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}],
                'Ipv6Ranges': [{'CidrIpv6': '::/0'}],
            },
        ]
    )
except:
    group = list(ec2.security_groups.filter(GroupNames=[GROUP_NAME]))[0]

# Initialize key pair for instance
try:
    key_pair = ec2.create_key_pair(KeyName=KEY_PAIR_NAME)
except:
    key_pair = ec2.KeyPair(KEY_PAIR_NAME)
    key_pair.delete()
    key_pair = ec2.create_key_pair(KeyName=KEY_PAIR_NAME)

# Record instances' SSH secret key in .pem file
with open(PEM_FILE_NAME, 'w') as f:
    f.write(key_pair.key_material)
subprocess.run(['chmod', '600', PEM_FILE_NAME])

# Create instances
instances = ec2.create_instances(
    InstanceType=instance_type,
    ImageId=IMAGE_ID,
    MinCount=MIN_COUNT,
    MaxCount=MAX_COUNT,
    SecurityGroups=[group.group_name],
    KeyName=key_pair.name,
    InstanceInitiatedShutdownBehavior='terminate',
    InstanceMarketOptions={
        'MarketType': 'Spot',
        'SpotOptions': {
            'MaxPrice': max_price,
        }
    },
    UserData=USER_DATA_SCRIPT + setup_commands
)

# Save all ids for use in the remove file
instance_ids = [instance.id for instance in instances]
group_ids = [group.id]
key_pair_names = [key_pair.name]

with open(CONFIG_PICKLE_FILE_NAME, 'wb') as f:
    pickle.dump({'instance_ids': instance_ids,
                 'group_ids': group_ids,
                 'key_pair_names': key_pair_names},
                f)

# Output message when instances are ready
all_running = False
while not all_running:
    if all(instance.state['Name'] == 'running'
           for instance in ec2.instances.filter(InstanceIds=instance_ids)):
        all_running = True
    time.sleep(0.1)

print('The instance is running.')

public_ips = [instance.public_ip_address
              for instance in ec2.instances.filter(InstanceIds=instance_ids)]
public_dnss = [instance.public_dns_name
               for instance in ec2.instances.filter(InstanceIds=instance_ids)]

# Copy necessary files over
for file_name in files_to_copy:
    subprocess.run(['scp',
                    '-i', PEM_FILE_NAME,
                    '-o', 'StrictHostKeyChecking=no',
                    file_name,
                    USERNAME + '@' + str(public_ips[0]) \
                    + ':/home/' + USERNAME])

# Show user how to access the instance
print('Access the server with the following command:\n'
      'ssh -i {PEM_FILE_NAME} ubuntu@{public_ip}\n'
      'Access the app at the following address:\n'
      '{public_dns}:8787'.format(
          PEM_FILE_NAME=PEM_FILE_NAME,
          public_ip=str(public_ips[0]),
          public_dns=public_dnss[0]
      )
)
