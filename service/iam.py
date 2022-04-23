from aws_cdk import (
    Stack,
    aws_iam as iam,
)
from constructs import Construct

import utils
from config import config


class IAM(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

    # Create IAM Role
    def create_iam_role(self,
                        role_name: str,
                        role_description: str,
                        add_managed_policy_names: list[str],  # list of managed policy names
                        custom_inline_policy: list[dict],  # [{'Effect': 'Allow', 'Action': '*', 'Resource': '*'}]
                        assumed_by: str,
                        tags: dict) -> iam.Role:
        role = iam.Role(
            self,
            role_name,
            description=role_description,
            role_name=role_name,
            assumed_by=iam.ServicePrincipal(assumed_by),
        )

        for policy_name in add_managed_policy_names:
            role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name(policy_name))

        """
        {
                "Effect": "Allow",
                "Action": ["ec2:Describe*"],
                "Resource": ["*"]
        }
        """
        for policy in custom_inline_policy:
            role.add_to_policy(
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW if policy.get('Effect') == 'Allow' else iam.Effect.DENY,
                    actions=policy['Action'],
                    resources=policy['Resource']
                )
            )

        utils.add_tags(source=role, tag_value=role_name, env=config.env, custom_tags=tags)
        return role
