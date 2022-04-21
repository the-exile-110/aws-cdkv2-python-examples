import aws_cdk as cdk
from aws_cdk import (
    Stack,
    Tags as tag,
    aws_iam as iam
)
from constructs import Construct


class IamUserStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.user = self.create_iam_user(
            user_name='example-user',
            groups=[
                iam.Group(self, 'example-group')
            ],
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name('example-policy-name')
            ],
            password='example-password',
            password_reset_required=True,
            path='/',
            permissions_boundary=[
                iam.ManagedPolicy.from_aws_managed_policy_name('example-policy-name')
            ],
            tags={'Name': 'example-user'},
        )

    def create_iam_user(self,
                        user_name: str,
                        groups: [iam.IGroup] = None,
                        managed_policies: [iam.IManagedPolicy] = None,
                        password: str = None,
                        password_reset_required: bool = False,
                        path: str = None,
                        permissions_boundary: [iam.IManagedPolicy] = None,
                        tags: dict = None,
                        ) -> iam.User:
        user = iam.User(
            self, user_name,
            managed_policies=managed_policies,
            password=None if not password else cdk.SecretValue.plain_text(password),
            password_reset_required=password_reset_required,
            path=path,
            permissions_boundary=permissions_boundary,
        )
        None if not groups else [user.add_to_groups(group) for group in groups]
        None if not tags else [tag.of(user).add(key, value) for key, value in tags.items()]
        return user
