import os
import boto3

client = boto3.client('ssm', region_name=os.getenv('AWS_REGION', 'us-east-1'))

class SSM:
    def __init__(self, ssm_path):
        self.ssm_path = ssm_path
        self.secret = client.get_parameter(Name=self.ssm_path, WithDecryption=True)['Parameter']['Value']
