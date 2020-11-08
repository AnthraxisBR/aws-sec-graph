import json
import boto3


def get_security_groups(profile, filter: str = ''):
    session = boto3.Session(profile_name=profile)
    ec2 = session.client('ec2')
    response = ec2.describe_security_groups()
    return response
