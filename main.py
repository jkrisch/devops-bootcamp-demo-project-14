import boto3
import schedule

ec2_client = boto3.client('ec2', region_name = "eu-central-1")
ec2_resource = boto3.resource('ec2', region_name = "eu-central-1")

#retrieve all instances in the specified region
instances = ec2_client.describe_instances()

# What we get is a list of Reservations
# Reservation represents startin/launcing multiple instances
# One reservation is an act of launching/starting instances so we might have multiple reservations and each reservations might have multiple instances



def check_ec2_instance_status():
    statuses = ec2_client.describe_instance_status(IncludeAllInstances=True)

    for status in statuses['InstanceStatuses']:
        ins_status = status['InstanceStatus']['Status']
        sys_status = status['SystemStatus']['Status']
        state = status['InstanceState']['Name']
        print(f"Instance {status['InstanceId']} is {state} with instance status {ins_status} and system status {sys_status}")
        
    print("################################################")

schedule.every(10).seconds.do(check_ec2_instance_status)

while(True):
    schedule.run_pending()
