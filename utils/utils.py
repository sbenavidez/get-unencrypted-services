import boto3
import datetime

# method to convert datetime to string for proper dumps printing
def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

# function to determine if an specified subnet is public
# returns bool
def isPublic(subnet,ec2,vpc):
    rt = ec2.describe_route_tables(
        Filters=[
            {'Name': 'association.subnet-id',
                'Values': [subnet]}
                ],
    )

    if (rt['RouteTables']):
        routes = rt['RouteTables'][0]['Routes']
        for route in routes:
            gateway = str(route['GatewayId'])
            dest = str(route['DestinationCidrBlock'])
            if(gateway.startswith('igw-')) and (dest.startswith('0.0.0.0/0')):
                return True

        # if no public rout found, returns false 
        return False

    else:
        # if rt not found, then subnet is on main rt
        # on main rt there's no explicit association
        # se we must search from the vpcId of the instance
        rtAssociations = ec2.describe_route_tables(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [
                        vpc,
                    ]
                },
            ],
        )
        for association in rtAssociations['RouteTables']:
            if(association['Associations'][0]['Main'] == True):
                mainrt=association['Associations'][0]['RouteTableId']


        rt = ec2.describe_route_tables(
            Filters=[
                {'Name': 'association.route-table-id',
                    'Values': [mainrt]}
                    ],
        )

        routes = rt['RouteTables'][0]['Routes']
        for route in routes:
            gateway = str(route['GatewayId'])
            dest = str(route['DestinationCidrBlock'])
            if(gateway.startswith('igw-')) and (dest.startswith('0.0.0.0/0')):
                return True

        # if no public rout found, returns false 
        return False
