# Title : Clean up scaling conf and related data
# Desc  : This code snippet removes launch conf, ami and snapshots associated with it.

from boto.regioninfo import *
from boto.ec2.connection import EC2Connection
from boto.ec2.autoscale import AutoScaleConnection
from boto.ec2.autoscale import LaunchConfiguration
from boto.ec2.autoscale import AutoScalingGroup
from boto.ec2.autoscale import ScalingPolicy
from random import randint
import datetime
import time

# AWS connect info
aws_access_key_id='########## AWS Access Key ############'
aws_secret_access_key='########### AWS Secret Key ############'
region_name='ap-southeast-1'
region_ec2_endpoint='ec2.ap-southeast-1.amazonaws.com'
region_autoscale_endpoint='autoscaling.ap-southeast-1.amazonaws.com'

# Engine Scaling conf names to clean
scaling_confs = ['scaling_conf_name_1','scaling_conf_name_2']

# Connect EC2
aws_region = RegionInfo(name=region_name, endpoint=region_endpoint)
conn = EC2Connection(aws_access_key_id,aws_secret_access_key,region=aws_region)

# Connect autoscaling service
aws_region_as = RegionInfo(name=region_name, endpoint=region_autoscale_endpoint)
conn_as = AutoScaleConnection(aws_access_key_id, aws_secret_access_key,region=aws_region_as)

lcs = conn_as.get_all_launch_configurations(names=scaling_confs)

for lc in lcs:
    try:
        img = conn.get_image(lc.image_id)
        snaps = conn.get_all_snapshots(filters={"description":"*"+img.id+"*"})
        image.deregister(delete_snapshot=False)
        for snap in snaps:
            snap.delete()
        print "scaling configuration image and these related "+str(snaps)+ " snapshots removed"
    except:
        print "ami not found " + lc.image_id
        pass
    conn_as.delete_launch_configuration(lc.name)
    print "\ndeleted scaling configuration "+ str(lc.name)
