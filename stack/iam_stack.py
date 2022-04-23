from constructs import Construct
from config import config
from service.iam import IAM


class IamStack(IAM):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.create_iam_role(
            role_name=f'{config.env}-{config.project_name}-role',
            role_description=f'{config.env}-{config.project_name}-role',
            add_managed_policy_names=['AmazonRDSFullAccess'],
            custom_inline_policy=[{'Effect': 'Allow', 'Action': ['*'], 'Resource': ['*']}],
            assumed_by='ec2.amazonaws.com',
            tags={}
        )
