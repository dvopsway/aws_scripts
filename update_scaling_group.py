# Title : Update autoscaling group with new launch configuration
# Desc : this code snippet updates a scaling group with new launch configuration with new ami
#        created based on an current instance.

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

# Variables needed for scaling
instance_id = "i-xxxxxxxx"
app_name = "random_name"
key_name = "key_name"
security_group = ['sg-xxxxxxxx']
instance_type = "c3.xlarge"
scaling_group_name = "XXXXXXXX_AS"
as_desired_capacity = 2
as_min_size = 2

# name used for ami and autoscaling configuration
today = datetime.date.today()
rand_id = randint(1000, 9999)
build_name = app_name + "_" + str(today) + "_" + str(rand_id)
print "Autoscaling configuration update will complete in 3 steps.\n"

# Connect EC2
aws_region = RegionInfo(name=region_name, endpoint=region_endpoint)
conn = EC2Connection(aws_access_key_id,aws_secret_access_key,region=aws_region)

# create ami
print "Step 1 : Creating ami"
ami_id = conn.create_image(instance_id,build_name,no_reboot=True)
ami_status = "Pending"
print "ami is being launched " + ami_id

# check_ami_status
image = conn.get_image(ami_id)
while image.state == "pending":
    time.sleep(10)
    image = conn.get_image(ami_id)
    print "ami is in pending state, waiting for 10 sec before next check"

image = conn.get_image(ami_id)
print "Image is now " + image.state

# Connect autoscaling service
print "\nStep 2 : Creating scaling configuration"
aws_region_as = RegionInfo(name=region_name, endpoint=region_autoscale_endpoint)
conn_as = AutoScaleConnection(aws_access_key_id, aws_secret_access_key,region=aws_region_as)

# Create autoscaling configuration
lc = LaunchConfiguration(name=build_name, image_id=ami_id, key_name=key_name, security_groups=security_group, instance_type=instance_type)
conn_as.create_launch_configuration(lc)
print "Autoscaling configuration ready : " + build_name

# Upgrading autoscaling group
print "\nStep 3 : Updating scaling group"
print "Updating Scaling group with new conf & terminating all the existing instances in the scaling group"
as_group = conn_as.get_all_groups(names=[scaling_group_name])[0]
setattr(as_group,'launch_config_name',build_name)
setattr(as_group,'desired_capacity',0)
setattr(as_group,'min_size',0)
as_group.update()

# Launching new systems
print "Waiting for 60 secs before launching new systems"
time.sleep(60)
setattr(as_group,'desired_capacity',as_desired_capacity)
setattr(as_group,'min_size',as_min_size)
as_group.update()
print "Systems are being launched, Updation process complete.\n\nLife is that easy , Have fun scaling :) :)"
