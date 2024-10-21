import boto3
from operator import itemgetter


ec2_client = boto3.client('ec2', region_name = "eu-central-1")

volumes = ec2_client.describe_volumes(
        Filters=[
            {
                'Name':'tag:Name',
                'Values':['prod']
            }
        ]
    )['Volumes']

for vol in volumes:
    snapshots = ec2_client.describe_snapshots(
        OwnerIds = ["self"],
        Filters = [
            {
                "Name":"volume-id",
                "Values": [vol['VolumeId']]
            }
        ]
    )['Snapshots']


#sort the list by creation timestamp
sorted_snapshots = sorted(snapshots, key=itemgetter("StartTime"), reverse=True)

#only keep the two newest snapshots by selecting a slice of the list starting from [2] (meaning the third element)
for snapshot in sorted_snapshots[2:]:
    ec2_client.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
