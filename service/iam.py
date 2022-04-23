from aws_cdk import (
    Stack,
    aws_iam as iam,
)
from constructs import Construct

import utils
from config import config
from utils import add_tags


class IAM(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

    # Create IAM Role

    def create_iam_role(self,
                        role_name: str,
                        role_description: str,
                        role_path: str,
                        inline_policies: iam.PolicyDocument,
                        assumed_by: str,
                        role_tags: dict) -> iam.Role:
        role = iam.Role(
            self,
            role_name,
            description=role_description,
            role_name=role_name,
            role_path=role_path,
            assumed_by=iam.ServicePrincipal(assumed_by),
            inline_policies=inline_policies
        )

        utils.add_tags(source=role, tag_value=role_name, env=config.env, custom_tags=role_tags)
        return role
