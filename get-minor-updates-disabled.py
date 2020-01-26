###############################################################
# Get list of services with maintenance minor updates disabled
# Author: SBenavidez
# Usage: run 'python3 get-minor-updates-disabled.py'
###############################################################

import boto3

regions = ['us-east-1','us-east-2','us-west-1','us-west-2','sa-east-1']


#RDS: get minor updates disabled instances
print("-----RDS CHECK-------")
for region in regions:

    rds = boto3.client('rds',region_name=region)

    instances = rds.describe_db_instances();

    for instance in instances['DBInstances']:
        if (instance['AutoMinorVersionUpgrade'] == False):
            print(("{0},{1},{2}").format(instance['DBInstanceIdentifier'],instance['AutoMinorVersionUpgrade'],region))


#Redshift: get minor updates disabled instances
print("-----Redshift CHECK-------")
for region in regions:

    rs = boto3.client('redshift',region_name=region)

    instances = rs.describe_clusters()

    for instance in instances['Clusters']:
        if (instance['AllowVersionUpgrade'] == False):
            print(("{0},{1},{2}").format(instance['ClusterIdentifier'],instance['AllowVersionUpgrade'],region))



#DocumentDB: get minor updates disabled instances
## Tener en cuenta que la API de docdb en parte es la misma que RDS, por lo cual puede devolver instances que no sean DocDB sino RDS.
## Se identifican dado que apareceran tambien en la seccion de RDS
print("-----DocumentDB CHECK-------")
for region in regions:
    docdb = boto3.client('docdb',region_name=region)
    instances = docdb.describe_db_instances()

    for instance in instances['DBInstances']:
        if (instance['AutoMinorVersionUpgrade'] == False):
            print(("{0},{1},{2}").format(instance['DBInstanceIdentifier'],instance['AutoMinorVersionUpgrade'],region))



#ElastiCache: get minor updates disabled instances
print("-----ElastiCache CHECK-------")
for region in regions:
    ec = boto3.client('elasticache',region_name=region)
    instances = ec.describe_cache_clusters()

    for instance in instances['CacheClusters']:
        if (instance['AutoMinorVersionUpgrade'] == False):
            print(("{0},{1},{2}").format(instance['CacheClusterId'],instance['AutoMinorVersionUpgrade'],region))

