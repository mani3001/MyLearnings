import boto3

from pprint import pprint

iam = boto3.client('iam')

response = iam.list_users()
#pprint(response['Users'])

for each in response['Users']:
    print(each['UserName'])
