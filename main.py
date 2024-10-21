import boto3


client = boto3.client('eks', region_name = "eu-central-1")
ec2_resource = boto3.resource('ec2', region_name = "eu-central-1")

clusters = client.list_clusters()["clusters"]

for cluster in clusters:
    response = client.describe_cluster(
        name=cluster
    )
    cluster_info = response["cluster"]
    cluster_status = response["cluster"]["status"]
    cluster_endpoint = response["cluster"]["endpoint"]
    cluster_version = response["cluster"]["version"]


    print(f"Cluster {cluster} status is {cluster_status}")
    print(f"Cluster endpoint {cluster_endpoint}")
    print(f"cluster version {cluster_version}")