import boto3


def get_security_groups(profile):
    ec2 = boto3.client('ec2')
    response = ec2.describe_security_groups()
    return response
