import json
import boto3


def get_ec2_instances(profile: str, filter: str = ''):
    session = boto3.Session(profile_name=profile)
    ec2 = session.client('ec2')
    if filter != '':
        response = ec2.describe_instances(
            Filters=json.loads(filter)
        )
    else:
        response = ec2.describe_instances()
    return response
