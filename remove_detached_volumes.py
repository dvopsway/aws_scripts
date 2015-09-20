# Title : Delete detached volumes from aws account
# Desc  : This code snippet deletes detached volumes all at once.

from boto.regioninfo import *
from boto.ec2.connection import EC2Connection
from random import randint

# AWS connect info
aws_access_key_id='########## AWS Access Key ############'
aws_secret_access_key='########### AWS Secret Key ############'
region_name='ap-southeast-1'
region_ec2_endpoint='ec2.ap-southeast-1.amazonaws.com'

# Connect EC2
aws_region = RegionInfo(name=region_name, endpoint=region_endpoint)
conn = EC2Connection(aws_access_key_id,aws_secret_access_key,region=aws_region)

# Remove detached volumes
print "Looking for detached volumes and then removing them"
all_volumes = conn.get_all_volumes()
count = 0
for each in all_volumes:
    if str(each.attachment_state()) != "attached":
        count += 1
        each.delete()
        print str(each.id) + " is deleted"
print str(count) + " volumes cleaned"
