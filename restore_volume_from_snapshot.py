import boto3
from operator import itemgetter


ec2_client = boto3.client('ec2', region_name = "eu-central-1")
ec2_resource = boto3.resource('ec2', region_name = "eu-central-1")

instance_id = "i-05b3481059b8498ec"

#Get the volume attached to the ec2 instance
volumes = ec2_client.describe_volumes(
        Filters=[
            {
                'Name':'attachment.instance-id',
                'Values':[instance_id]
            }
        ]
    )['Volumes']

instance_volume = volumes[0]
print(instance_volume)


#Retrieve the latest snapshot
instance_snapshots=ec2_client.describe_snapshots(
    OwnerIds = ["self"],
    Filters = [
        {
            "Name":"volume-id",
            "Values": [instance_volume['VolumeId']]
        }
    ]
)

latest_snapshot = sorted(instance_snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)[0]
print(latest_snapshot)


#Create a new volume from the latest snapshot
new_volume = ec2_client.create_volume(
        SnapshotId = latest_snapshot['SnapshotId'],
        AvailabilityZone = "eu-central-1b",
        TagSpecifications =[
            {
                "ResourceType": "volume",
                "Tags" :[
                    {
                        "Key":"Name",
                        "Value": "prod"
                    }
                ]
            }
        ]
    )


while(True):
    if ec2_resource.Volume(new_volume['VolumeId']).state == "available":
        break

#Attache the newly created volume to the ec2 instance
ec2_resource.Instance(instance_id).attach_volume(
    VolumeId = new_volume["VolumeId"],
    Device = '/dev/xvdb'
)
