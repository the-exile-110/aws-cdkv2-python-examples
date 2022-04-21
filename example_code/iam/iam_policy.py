from aws_cdk import (
    Stack,
    Tags as tag,
    aws_iam as iam,
)
from constructs import Construct


class IamPolicyStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.user = self.create_iam_policy(
            policy_name='example-iam-policy',
            # Bug? get jsii.errors.JSIIError: Expected object reference, got [{"$jsii.byref":"aws-cdk-lib.aws_iam.PolicyDocument@10041"}] error
            # document=[
            #     iam.PolicyDocument(
            #         statements=[
            #             iam.PolicyStatement(
            #                 actions=["kms:*"],
            #                 principals=[iam.AccountRootPrincipal()],
            #                 resources=["*"]
            #             )
            #         ]
            #     )
            # ],
            force=False,
            groups=[
                iam.Group(self, 'example-group')
            ],
            roles=[
                iam.Role(self, 'example-role', assumed_by=iam.ServicePrincipal('ec2.amazonaws.com'))
            ],
            statements=[
                iam.PolicyStatement(
                    actions=["kms:Create*", "kms:Describe*", "kms:Enable*", "kms:List*", "kms:Put*"],
                    # A PolicyStatement used in an identity-based policy cannot specify any IAM principals.
                    principals=None,
                    resources=["*"]
                )
            ],
            users=[
                iam.User(self, 'example-user')
            ],
            tags={'Name': 'example-user'},
        )

    def create_iam_policy(self,
                          policy_name: str,
                          document: [iam.PolicyDocument] = None,
                          force: bool = False,
                          groups: [iam.IGroup] = None,
                          roles: [iam.Role] = None,
                          statements: [iam.PolicyStatement] = None,
                          users: [iam.User] = None,
                          tags: dict = None,
                          ) -> iam.Policy:
        policy = iam.Policy(
            self, policy_name,
            policy_name=policy_name,
            document=document,
            force=force,
        )
        None if not statements else [policy.add_statements(statement) for statement in statements]
        None if not users else [policy.attach_to_user(user) for user in users]
        None if not groups else [policy.attach_to_group(group) for group in groups]
        None if not roles else [policy.attach_to_role(role) for role in roles]
        None if not tags else [tag.of(policy).add(key, value) for key, value in tags.items()]
        return policy
