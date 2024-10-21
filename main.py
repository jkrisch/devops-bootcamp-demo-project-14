import boto3

def add_tag_to_ec2_instances(region, tag):
    ec2_client = boto3.client('ec2', region_name=region)
    ec2_resource = boto3.resource ('ec2', region_name=region)

    #retrieve all instances in the specified region
    instances = ec2_client.describe_instances()['Reservations']

    instances_ids = []
    if instances:
        for res in instances:
            instances = res['Instances']
            for instance in instances:
                instances_ids.append(instance["InstanceId"])


        response = ec2_resource.create_tags(
            Resources =  instances_ids,
            Tags = [
                tag
            ]
        )

#adding prod to frankfurt
region = "eu-central-1"
tag = {
    "Key":"environment",
    "Value": "prod"
}
add_tag_to_ec2_instances(region=region, tag=tag)

#adding dev to paris
region = "eu-west-3"
tag = {
    "Key":"environment",
    "Value": "dev"
}
add_tag_to_ec2_instances(region=region, tag=tag)