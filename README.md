# aws-sec-graph

# Pourpose

Give a overview of AWS Security Group and EC2 instances, allowing you to see the relation over instances X security groups X opened ports.

# Requirements

### Packages

- python3
- awscli
- graphviz

### AWS Permissions
- Read-Only
    
- Permissions

    ec2:DescribeInstances
    ec2:DescribeSecurityGroups

- Resources

    * All

# Usage

python3 run.py --command=analyze


# Recomendations

- https://github.com/jrfonseca/xdot.py

# TODO 
1. Use aws profile
2. Filter for instances to graph
3. Filter for ports
4. Generate different page for security group

