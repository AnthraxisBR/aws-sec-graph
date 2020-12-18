# aws-sec-graph

# Pourpose

Give a overview of AWS Security Group and EC2 instances, allowing you to see the relation over instances X security groups X opened ports.

# Requirements

### Packages

- python3
- awscli
- graphviz


### Prerequisites

- awscli configured
- sudo apt install graphviz (https://graphviz.org/download/)
- pip install graphviz (https://graphviz.readthedocs.io/en/stable/manual.html#installation)

### AWS Permissions
- Read-Only
    
- Permissions


    ec2:DescribeInstances
   
    ec2:DescribeSecurityGroups

- Resources

    * All

# Options:
    
    --command : Only "analyze" command available
    --profile  : Inform aws profile to authenticate using boto3 lib
    --filter : Filter to apply on describe instances (https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-instances.html)
    --format : output format (https://graphviz.org/doc/info/output.html)
    --port-filter : Inform a especific port or a range of ports to filter the output, example: 1 unique port "22" or range of ports "20:22"

# Usage

### General usage
   
    python3 run.py --command=analyze

### Using filter

     python run.py --command=analyze --profile=default --filter='[{"Name": "tag:environment","Values": ["staging"]}]'

### Using port filter
       
Range of ports:
     
     python run.py --command=analyze --profile=default --port-filter=20:22
     
Unique port:
     
     python run.py --command=analyze --profile=default --port-filter=22
     
 ## Change output format (based on graphviz lib)

    python run.py --command=analyze --profile=default --filter='[{"Name": "tag:environment","Values": ["staging"]}]' --format=xdot

# Recomendations

- https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
- https://graphviz.org/documentation/
- https://github.com/jrfonseca/xdot.py

# TODO 
1. Use aws profile: done (08/11/2020)
2. Filter for instances to graph: done (08/11/2020)
3. Filter for ports: done (18/12/2020)
4. Generate different page for security group

