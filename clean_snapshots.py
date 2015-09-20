# Title : deregister ami & its associated snapshots
# Desc : Usually when you deregister ami from console its related ebs volume snapshots are
#        left behind, this code scippet basically deregister ami and deletes all the snapshots
#        associated with it.

from boto.regioninfo import *
from boto.ec2.connection import EC2Connection

# AWS connect info
aws_access_key_id='########## AWS Access Key ############'
aws_secret_access_key='########### AWS Secret Key ############'
region_name='ap-southeast-1'
region_ec2_endpoint='ec2.ap-southeast-1.amazonaws.com'

# Enter amis that you want to clean in the array
img_arr = ['ami-xxxxxxxx','ami-xxxxxxxx']

# Connect EC2
aws_region = RegionInfo(name=region_name, endpoint=region_endpoint)
conn = EC2Connection(aws_access_key_id,aws_secret_access_key,region=aws_region)

# Clean components
for each in img_arr:
    image = conn.get_image(each)
    snaps = conn.get_all_snapshots(filters={"description":"*"+each+"*"})
    try:
        image.deregister(delete_snapshot=False)
    except:
        pass
    for snap in snaps:
        try:
            snap.delete()
        except:
            pass
    print each+" image and these "+str(snaps)+ " snapshots removed"
