# aws-sec-graph

# Purpose

Give a graph of the AWS Security Groups and EC2 instances relation.

This allow you to see relations over *instances* **X** *security groups* **X** *opened ports* based on AWS Filters(with boto3, Port filters or in all ec2 available instances and Security Groups.

### Output Example:
![Output Example](example.jpg)


# Requirements

### Packages

- python3
- awscli
- graphviz
- pip
- boto3 

### Install from source (recommended)

    sudo apt install graphviz
    sudo apt install xdot
    sudo apt-get install python3-gi
    pip install -r requirements.txt

    ''' Only for virutalenv '''
    pip install vext
    pip install vext.gi

### Installation from pip
    
    sudo apt install graphviz
    pip install aws-sec-graph

### AWS Permissions
*Read-Only*
    
*Permissions:*

    ec2:DescribeInstances
    ec2:DescribeTags
    ec2:DescribeSecurityGroups

*Resources:*

    *(All)

*Example:*
 
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "ec2:DescribeInstances",
                    "ec2:DescribeTags",
                    "ec2:DescribeSecurityGroups"
                ],
                "Resource": "*"
            }
        ]
    }

# Options:
    
    --command : 
        Only "analyze" command available
    --profile  : Inform aws profile to authenticate using boto3 lib
    --filter : Filter to apply on describe instances (https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-instances.html)
    --format : output format (https://graphviz.org/doc/info/output.html)
    --port-filter : Inform a especific port or a range of ports to filter the output, example: 1 unique port "22" or range of ports "20:22"

# Usage

### General usage
   
    aws-sec-graph --command=analyze

### Using filter

     aws-sec-graph --command=analyze --profile=default --filter='[{"Name": "tag:environment","Values": ["staging"]}]'

### Using port filter
       
Range of ports:
     
     aws-sec-graph --command=analyze --profile=default --port-filter=20:22
     
Unique port:
     
     aws-sec-graph --command=analyze --profile=default --port-filter=22
     
 ## Change output format (based on graphviz lib)

    aws-sec-graph --command=analyze --profile=default --filter='[{"Name": "tag:environment","Values": ["staging"]}]' --format=xdot

# Recomendations

- https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
- https://graphviz.org/documentation/
- https://github.com/jrfonseca/xdot.py

# TODO 
1. Use aws profile: done (08/11/2020)
2. Filter for instances to graph: done (08/11/2020)
3. Filter for ports: done (18/12/2020)
4. Generate different page for security group
5. Optmize and clear code 

