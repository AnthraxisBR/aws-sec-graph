import boto3


def get_ec2_instances(profile):
    ec2 = boto3.client("ec2")
    response = ec2.describe_instances()
    return response
