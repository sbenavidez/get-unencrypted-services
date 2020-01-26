###############################################################
# Get list of services which have public access
# Author: SBenavidez
# Usage: run 'python3 get-exposed-services.py'
###############################################################


import boto3
import json
import datetime

regions = ['us-east-1','us-east-2','us-west-1','us-west-2','sa-east-1']

# method to convert datetime to string for dumps printing
def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

# ElasticSearch: get publicly exposed domains
print("-----Elastic Search Public exposition check-------")
for region in regions:
    es = boto3.client('es',region_name=region)
    domains = es.list_domain_names()

    if (len(domains['DomainNames']) > 0) :
        for domianName in domains['DomainNames']:

            domain = es.describe_elasticsearch_domain(
                DomainName=domianName['DomainName']
            )
            # print('Checking Domain {0} in region {1}'.format(domianName['DomainName'],region))
            # print(json.dumps(domain,default=myconverter,indent=''))
            if 'VPCOptions' not in domain['DomainStatus']:
                print('Domain {0} is public access policy is')
                print(json.dumps(domain['DomainStatus']['AccessPolicies'],indent=1))
    # else:
        # print('No ES domains found on region',region)


# # DocumentDB: get publicly exposed instances
# print("-----DocumentDB Public exposition check-------")
# for region in regions:
#     docdb = boto3.client('docdb',region_name=region)
#     instances = docdb.describe_db_clusters()

#     for instance in instances['DBClusters']:
#         # print(json.dumps(instance,default=myconverter,indent=1))
#         if 'PubliclyAccessible' in instance:
#             if (instance['PubliclyAccessible'] == True):
#                 print(("{0},{1},{2}").format(instance['DBClusterIdentifier'],region,instance['PubliclyAccessible']))



# # RDS: get publicly exposed instances
# print("-----RDS Public exposition check-------")
# for region in regions:
#     rds = boto3.client('rds',region_name=region)
#     instances = rds.describe_db_instances();

#     for instance in instances['DBInstances']:
#         if 'PubliclyAccessible' in instance:
#             if (instance['PubliclyAccessible'] == True):
#                 print(("{0},{1},{2}").format(instance['DBInstanceIdentifier'],instance['PubliclyAccessible'],region))

