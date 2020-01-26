import boto3
from utils.utils import isPublic

# const declaration
ec2 = boto3.client('ec2')
instances = ec2.describe_instances()

for instance in instances['Reservations']:
    instanceId = instance['Instances'][0]['InstanceId']
    response = ec2.describe_instances(
        InstanceIds=[
            instanceId,
        ],
    )
    subnetId = response['Reservations'][0]['Instances'][0]['SubnetId']
    vpcId = response['Reservations'][0]['Instances'][0]['VpcId']

    if isPublic(subnetId,ec2,vpcId):
        print('{0},{1}'.format(instanceId,'public=true'))
