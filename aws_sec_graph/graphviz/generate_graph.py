from graphviz import Digraph

INBOUND_TYPES: dict = {
    'IpRanges': 'CidrIp',
    'Ipv6Ranges': 'CidrIpv6',
    'UserIdGroupPairs': 'GroupId',
    'PrefixListIds': 'GroupId'
}


def extract_node_name_node_from_security_groups(
        nodes: dict,
        security_groups: dict
) -> dict:
    for security_group in security_groups['SecurityGroups']:
        name: str = security_group['GroupId']
        if name not in nodes:
            nodes[name] = {
                'name':  security_group['GroupName'],
                'inbound': {},
                'outboud': {}
            }
    return nodes


def set_inbound_port_range(
        nodes: dict,
        node: dict,
        security_group: dict
) -> dict:
    for ip_permission in security_group['IpPermissions']:
        if node in nodes and 'FromPort' in ip_permission:
            from_port = ip_permission['FromPort']
            if from_port not in nodes[node]['inbound']:
                nodes[node]['inbound'][from_port] = []
    return nodes


def append_inbound_options(
        nodes: dict,
        node: dict,
        ip_permission: dict,
        port_range: str,
        inbound_type: str
) -> dict:
    for ip_info in ip_permission[inbound_type]:
        if port_range in nodes[node]['inbound']:
            nodes[node]['inbound'][port_range].append(
                ip_info[INBOUND_TYPES[inbound_type]]
            )
    return nodes


def iterate_inbound_options(
        nodes: dict,
        node: dict,
        ip_permission: dict,
        port_range: str
) -> dict:
    for inbound_type in INBOUND_TYPES:
        nodes = append_inbound_options(
            nodes=nodes,
            node=node,
            ip_permission=ip_permission,
            port_range=port_range,
            inbound_type=inbound_type
        )
    return nodes


def extract_node_inbound_from_security_groups(
        nodes: dict,
        security_groups: dict
) -> dict:
    for security_group in security_groups['SecurityGroups']:
        node: str = security_group['GroupId']

        nodes: dict = set_inbound_port_range(
            nodes=nodes,
            node=node,
            security_group=security_group
        )

        for ip_permission in security_group['IpPermissions']:
            if node in nodes and 'FromPort' in ip_permission:
                port_range = ip_permission['FromPort']
                nodes: dict = iterate_inbound_options(
                    nodes=nodes,
                    node=node,
                    ip_permission=ip_permission,
                    port_range=port_range
                )
            elif 'IpProtocol' in ip_permission:
                port_range: str = 'All'
                nodes: dict = iterate_inbound_options(
                    nodes=nodes,
                    node=node,
                    ip_permission=ip_permission,
                    port_range=port_range
                )

    return nodes


def get_ec2_name(instance: dict) -> str:
    name: str = 'none'
    if 'Tags' in instance:
        for tag in instance['Tags']:
            if tag['Key'] == 'Name':
                name = tag['Value']
    return name


def extract_ec2_instances_into_nodes(
        instance_nodes: dict,
        nodes: dict,
        ec2_instances: dict
) -> dict:

    for reservation in ec2_instances['Reservations']:
        for instance in reservation['Instances']:
            name: str = get_ec2_name(instance=instance)
            instance_id: str = instance['InstanceId']
            if instance_id not in nodes:
                instance_nodes[instance_id]: dict = {
                    'SecurityGroups': instance['SecurityGroups'],
                    'name': name
                }
    return instance_nodes


def mount_graph_from_nodes(
        graph: Digraph,
        nodes: dict,
        instance_nodes: dict
) -> Digraph:

    graph.node('world')

    ip_nodes: list = []
    for node in nodes:
        graph.node(node, label=nodes[node]['name'])

    for node in nodes:
        for inbound_port in nodes[node]['inbound']:
            for sub in nodes[node]['inbound'][inbound_port]:
                if sub in nodes:
                    graph.edge(node, sub, label=str(inbound_port))
                else:
                    inbound_node_name: str = str(sub).replace('/', '//')
                    if inbound_node_name not in ip_nodes:
                        graph.node(inbound_node_name)
                        ip_nodes.append(inbound_node_name)
                    graph.edge(
                        inbound_node_name,
                        node,
                        label=str(inbound_port)
                    )

    for instance_node in instance_nodes:
        graph.node(instance_node,  label=instance_nodes[instance_node]['name'])

    for node in nodes:
        for instance_node in instance_nodes:
            for sg in instance_nodes[instance_node]['SecurityGroups']:
                if sg['GroupId'] == node:
                    graph.edge(sg['GroupId'], instance_node)
    return graph


def generate_graph(
        security_groups,
        ec2_instances,
        comment: str = 'Security Group Digraph',
        graphviz_format: str = 'xdot'
):
    graph = Digraph(comment=comment, format=graphviz_format, strict=False)

    instance_nodes: dict = {}
    nodes: dict = {}

    nodes: dict = extract_node_name_node_from_security_groups(
        nodes=nodes,
        security_groups=security_groups
    )

    nodes: dict = extract_node_inbound_from_security_groups(
        nodes=nodes,
        security_groups=security_groups
    )

    instance_nodes: dict = extract_ec2_instances_into_nodes(
        instance_nodes=instance_nodes,
        nodes=nodes,
        ec2_instances=ec2_instances
    )

    graph = mount_graph_from_nodes(
        graph=graph,
        nodes=nodes,
        instance_nodes=instance_nodes
    )

    graph.render(view=True)
