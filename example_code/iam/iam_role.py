import aws_cdk as cdk
from aws_cdk import (
    Stack,
    Tags as tag,
    aws_iam as iam
)
from constructs import Construct


class IamRoleStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # iam role
        self.iam_role = self.create_iam_role(
            role_name='example-iam-role',
            assumed_by=iam.ServicePrincipal('ec2.amazonaws.com'),
            description='example-destination',
            external_ids=['example-external-id'],
            inline_policies=[
                iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            actions=["kms:Create*", "kms:Describe*", "kms:Enable*", "kms:List*", "kms:Put*"],
                            # A PolicyStatement used in an identity-based policy cannot specify any IAM principals.
                            principals=None,
                            resources=["*"]
                        )
                    ]
                )
            ],
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name('example-policy-name')
            ],
            max_session_duration=cdk.Duration.seconds(3600),
            path='/',
            permissions_boundary=[
                iam.ManagedPolicy.from_aws_managed_policy_name('example-policy-name')
            ],
            tags={'Name': 'example-iam-role', 'Environment': 'example-environment'},
        )

    def create_iam_role(self,
                        role_name: str,
                        assumed_by: iam.ServicePrincipal = None,
                        description: str = None,
                        external_ids: list[str] = None,
                        inline_policies: list[iam.PolicyDocument] = None,
                        managed_policies: list[iam.Role.add_managed_policy] = None,
                        max_session_duration: cdk.Duration = None,
                        path: str = None,
                        permissions_boundary: [iam.IManagedPolicy] = None,
                        tags: dict = None,
                        ) -> iam.Role:
        if not assumed_by:
            raise 'The parameter assumed_by is required'

        iam_role = iam.Role(
            self, role_name,
            assumed_by=assumed_by,
            description=description,
            external_ids=external_ids,
            inline_policies=inline_policies,
            managed_policies=managed_policies,
            max_session_duration=max_session_duration,
            path=path,
            permissions_boundary=permissions_boundary,
            role_name=role_name,
        )
        None if not tags else [tag.of(iam_role).add(key, value) for key, value in tags.items()]
        return iam_role
