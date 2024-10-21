import boto3
import schedule

ec2_client = boto3.client('ec2', region_name = "eu-central-1")


def create_snapshot_for_region():
    volumes = ec2_client.describe_volumes(
        Filters=[
            {
                'Name':'tag:Name',
                'Values':['prod']
            }
        ]
    )['Volumes']


    for vol in volumes:
        new_snapshot = ec2_client.create_snapshot(
            VolumeId = vol["VolumeId"]
        )
        print(new_snapshot)

create_snapshot_for_region()

"""
schedule.every(5).seconds.do(create_snapshot_for_region)

while True:
    schedule.run_pending()
"""