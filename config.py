import os
import aws_cdk as cdk
from pydantic import BaseSettings


class Config(BaseSettings):
    # Project
    account_id: str = ''
    project_name: str = 'aws-cdk-demo'
    region: str = 'ap-northeast-1'

    env: str = 'dev' if not os.getenv('ENV') else os.getenv('ENV')
    stack_env = cdk.Environment(account=account_id, region=region)


config = Config()
