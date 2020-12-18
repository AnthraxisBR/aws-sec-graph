from graphviz import Digraph

INBOUND_TYPES: dict = {
    'IpRanges': 'CidrIp',
    'Ipv6Ranges': 'CidrIpv6',
    'UserIdGroupPairs': 'GroupId',
    'PrefixListIds': 'GroupId'
}


def check_if_security_group_is_attached_to_an_instance(
        ec2_instances,
        group_name
) -> bool:
    for reservation in ec2_instances['Reservations']:
        for instance in reservation['Instances']:
            for security_group in instance['SecurityGroups']:
                if group_name == security_group['GroupId']:
                    return True
    return False


def extract_only_filtered_ports(
        security_group: dict,
        port: int = 0,
        port_range: list = []
) -> tuple:
    security_group_copy = security_group.copy()
    security_group_copy['IpPermissions'] = []
    for index, ip_permission in enumerate(security_group['IpPermissions']):
        if 'FromPort' in ip_permission:
            from_port = ip_permission['FromPort']
            to_port = ip_permission['ToPort']
            if len(port_range) > 0:
                if from_port in port_range:
                    security_group_copy['IpPermissions'].append(ip_permission)
            else:
                if to_port <= port >= from_port:
                    security_group_copy['IpPermissions'].append(ip_permission)
    return (
        len(security_group_copy['IpPermissions']) > 0,
        security_group_copy
    )


def extract_node_name_node_from_security_groups(
        nodes: dict,
        security_groups: dict,
        ec2_instances: dict,
        port_filter
) -> dict:
    for security_group in security_groups['SecurityGroups']:
        name: str = security_group['GroupId']
        port_filter_math = False
        security_group_filtered = {}

        if type(port_filter) != int and ':' in port_filter:
            filter_ = [int(port) for port in port_filter.split(':')]
            port_filter_math, security_group_filtered = extract_only_filtered_ports(
                port_range=filter_,
                security_group=security_group
            )
        elif type(port_filter) == str:
            try:
                filter: int = int(port_filter)
                port_filter_math, security_group_filtered = extract_only_filtered_ports(
                    port=filter,
                    security_group=security_group
                )
            except ValueError as error:
                port_filter_math = False

        attach_inbound = check_if_security_group_is_attached_to_an_instance(
            ec2_instances=ec2_instances,
            group_name=name
        )

        if name not in nodes \
                and attach_inbound is True and \
                port_filter_math is True:
            nodes[name] = {
                'name': security_group_filtered['GroupName'],
                'inbound': {},
                'outbound': {}
            }
    return nodes


def set_inbound_port_range(
        nodes: dict,
        node: str,
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
        node: str,
        ip_permission: dict,
        port_range: str,
        inbound_type: str
) -> dict:
    for ip_info in ip_permission[inbound_type]:
        if node in nodes:
            if port_range in nodes[node]['inbound']:
                nodes[node]['inbound'][port_range].append(
                    ip_info[INBOUND_TYPES[inbound_type]]
                )
    return nodes


def iterate_inbound_options(
        nodes: dict,
        node: str,
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
        security_groups: dict,
        port_filter
) -> dict:
    for security_group in security_groups['SecurityGroups']:
        node: str = security_group['GroupId']
        security_group_filtered = security_group
        if type(port_filter) != int and ':' in port_filter:
            filter_ = [int(port) for port in port_filter.split(':')]
            port_filter_math, security_group_filtered = extract_only_filtered_ports(
                port_range=filter_,
                security_group=security_group
            )
        elif type(port_filter) == str:
            try:
                filter: int = int(port_filter)
                port_filter_math, security_group_filtered = extract_only_filtered_ports(
                    port=filter,
                    security_group=security_group
                )
            except ValueError as error:
                port_filter_math = False


        nodes: dict = set_inbound_port_range(
            nodes=nodes,
            node=node,
            security_group=security_group_filtered
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
        instance_nodes: dict,
        security_groups: dict
) -> Digraph:
    graph.node('world', color='red')

    already_mapped: list = []
    not_in_node: list = []

    for node in nodes:
        graph.node(node, label=nodes[node]['name'], color='green')
        already_mapped.append(node)

    for node in nodes:
        for inbound_port in nodes[node]['inbound']:
            for sub in nodes[node]['inbound'][inbound_port]:
                inbound_node_name: str = str(sub).replace('/', '//')
                if inbound_node_name not in node:
                    not_in_node.append(inbound_node_name)

                graph.edge(
                    inbound_node_name,
                    node,
                    label=str(inbound_port),
                    color='yellow'
                )

    for node in not_in_node:
        for security_group in security_groups['SecurityGroups']:
            if node == security_group['GroupId'] \
                    and node not in already_mapped:
                graph.node(
                    node,
                    label=security_group['GroupName'],
                    color='green'
                )

    for instance_node in instance_nodes:
        graph.node(
            instance_node,
            label=instance_nodes[instance_node]['name'],
            color='blue'
        )

    for node in nodes:
        for instance_node in instance_nodes:
            for sg in instance_nodes[instance_node]['SecurityGroups']:
                if sg['GroupId'] == node:
                    graph.edge(
                        sg['GroupId'],
                        instance_node,
                        color='yellow'
                    )
    return graph


def generate_graph(
        security_groups,
        ec2_instances,
        port_filter,
        comment: str = 'Security Group Digraph',
        graphviz_format: str = 'xdot'
):
    graph = Digraph(comment=comment, format=graphviz_format, strict=False)

    instance_nodes: dict = {}
    nodes: dict = {}

    nodes: dict = extract_node_name_node_from_security_groups(
        nodes=nodes,
        security_groups=security_groups,
        ec2_instances=ec2_instances,
        port_filter=port_filter
    )

    nodes: dict = extract_node_inbound_from_security_groups(
        nodes=nodes,
        security_groups=security_groups,
        port_filter=port_filter
    )

    instance_nodes: dict = extract_ec2_instances_into_nodes(
        instance_nodes=instance_nodes,
        nodes=nodes,
        ec2_instances=ec2_instances
    )

    graph = mount_graph_from_nodes(
        graph=graph,
        nodes=nodes,
        instance_nodes=instance_nodes,
        security_groups=security_groups
    )

    graph.render(view=True)
