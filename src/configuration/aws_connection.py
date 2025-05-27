import boto3
import os
from src.constants import *

"This class is the AWS cofiguration class which will help us to connect AWS and my Local code."

class S3client:
    s3_client=None
    s3_resource=None
    def __init__(self, region_name=AWS_REGION):
        if S3client.s3_client==None or S3client.s3_resource==None:
            access_key_id=AWS_ACCESS_KEY_ID
            secret_key_id=AWS_SECRET_ACCESS_KEY_ID
            if access_key_id is None:
                raise Exception(f"Environment variable: {access_key_id} is not set in the .env file.🔴")
            if secret_key_id is None:
                raise Exception(f"Environment variable: {secret_key_id} is not set in the .env file.🔴")
            
            S3client.s3_resource=boto3.resource('s3',
                                            aws_access_key_id=access_key_id,
                                            aws_secret_access_key=secret_key_id,
                                            region_name=region_name)
            S3client.s3_client=boto3.client('s3',
                                              aws_access_key_id=access_key_id,
                                              aws_secret_access_key=secret_key_id,
                                              region_name=region_name)
            
            self.s3_resource=S3client.s3_resource
            self.s3_client=S3client.s3_client
