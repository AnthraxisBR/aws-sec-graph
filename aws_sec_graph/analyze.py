from aws_sec_graph.graphviz.generate_graph import generate_graph
from aws_sec_graph.aws.security_groups import get_security_groups
from aws_sec_graph.aws.ec2 import get_ec2_instances


def analyze(args):
    profile: str = args.profile

    security_groups = get_security_groups(profile)
    ec2_instances = get_ec2_instances(profile)
    generate_graph(
        security_groups=security_groups,
        ec2_instances=ec2_instances
    )
