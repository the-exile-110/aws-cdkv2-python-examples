from aws_cdk import (
    aws_ec2 as ec2,
    aws_logs as logs,
    aws_iam as iam,
)
from constructs import Construct

import utils
from config import config
from utils import add_tags


class IAM:

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
