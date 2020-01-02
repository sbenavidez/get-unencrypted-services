import boto3

regions = ['us-east-1','us-east-2','us-west-1','us-west-2','sa-east-1']

# EBS: get unencrypted EBS volumes 
print("-----EBS CHECK-------")
for region in regions:

    ec2 = boto3.resource('ec2',region_name=region)
    volume_iterator = ec2.volumes.all()

    for v in volume_iterator:
        attached = True if len(v.attachments) > 0 else False 

        if (ec2.Volume(v.id).encrypted == False):
            print(("{0},{1},{2}").format(ec2.Volume(v.id).id,region,attached))

        # If you need data about the ec2 instance 
        # for a in v.attachments:
        #     print("{0} {1} {2} {3}".format(v.id, v.state, a['InstanceId'],v.encrypted))


#RDS: get unencrypted RDS instances 
print("-----RDS CHECK-------")
for region in regions:

    rds = boto3.client('rds',region_name=region)

    instances = rds.describe_db_instances();

    for instance in instances['DBInstances']:
        if (instance['StorageEncrypted'] == False):
            print(("{0},{1},{2}").format(instance['DBInstanceIdentifier'],instance['StorageEncrypted'],region))

#SQS: get unencrypted SQS queues
print("-----SQS CHECK-------")
for region in regions:
    sqs = boto3.client('sqs',region_name=region)
    queues = sqs.list_queues()

    # One positions if for the ResponseMetadata block
    if len(queues) > 1:
        for queueURL in queues['QueueUrls']:
            queue = sqs.get_queue_attributes(
                QueueUrl=queueURL,
                AttributeNames=['KmsMasterKeyId']
            )
            if(len(queue) == 1):
                print(("{0},{1}").format(queueURL,region))

#SNS: get unencrypted SNS topics 
print("-----SNS CHECK-------")
for region in regions:
    sns = boto3.client('sns',region_name=region)
    topics = sns.list_topics()

    if len(topics['Topics']) > 0:
        for topicARN in topics['Topics']:
            topic = sns.get_topic_attributes(
                TopicArn=topicARN['TopicArn']
            )
            if 'KmsMasterKeyId' not in topic['Attributes']:
                print('{0},{1}'.format(topic['Attributes']['TopicArn'],region))
            #else:
                #print('Its encrypted --> ', topic['Attributes']['TopicArn'])


#Redshift: get unencrypted Redshift instances
print("-----Redshift CHECK-------")
for region in regions:

    rs = boto3.client('redshift',region_name=region)

    instances = rs.describe_clusters()

    for instance in instances['Clusters']:
        if (instance['Encrypted'] == False):
            print(("{0},{1},{2}").format(instance['ClusterIdentifier'],region,instance['Encrypted'],))


#EFS: get unencrypted EFS volumes
print("-----EFS CHECK-------")
for region in regions:
    efs = boto3.client('efs',region_name=region)
    volumes = efs.describe_file_systems()

    for volume in volumes['FileSystems']:
        if (volume['Encrypted'] == False):
            print(("{0},{1},{2}").format(volume['FileSystemId'],region,volume['Encrypted'],))


#DocumentDB: get unencrypted DocumentDB instances
print("-----DocumentDB CHECK-------")
for region in regions:
    docdb = boto3.client('docdb',region_name=region)
    instances = docdb.describe_db_clusters()

    for instance in instances['DBClusters']:
        if (instance['StorageEncrypted'] == False):
            print(("{0},{1},{2}").format(instance['DBClusterIdentifier'],region,instance['StorageEncrypted'],))

#ElastiCache: get unencrypted ElastiCache instances
print("-----ElastiCache CHECK-------")
for region in regions:
    ec = boto3.client('elasticache',region_name=region)
    instances = ec.describe_cache_clusters()

    for instance in instances['CacheClusters']:
        if (instance['AtRestEncryptionEnabled'] == False):
            print(("{0},{1},{2}").format(instance['CacheClusterId'],region,instance['AtRestEncryptionEnabled'],))

#ES: get unencrypted ES Domains
print("-----ES CHECK-------")
for region in regions:
    es = boto3.client('es',region_name=region)
    domains = es.list_domain_names()

    if (len(domains['DomainNames']) > 0):
        for domianName in domains['DomainNames']:
            domain = es.describe_elasticsearch_domain(
                DomainName=domianName['DomainName']
            )
            if (domain['DomainStatus']['EncryptionAtRestOptions']['Enabled'] == False):
                print(("{0},{1}").format(domianName['DomainName'],region))


#DynamoDB: get unencrypted Dynamo tables
# print("-----DynamoDB CHECK-------")
# for region in regions:
#     dyn = boto3.client('dynamodb',region_name=region)
#     tables = dyn.list_tables()
#     print(tables)
#     print(len(tables['TableNames']))

#     if (len(tables['TableNames']) > 0):
#         print('hola')
#         for tableName in tables['TableNames']:
#             table = dyn.describe_table(
#                 TableName=tableName
#             )
#             print(table)
#             print(table['Table']['SSEDescription'])
