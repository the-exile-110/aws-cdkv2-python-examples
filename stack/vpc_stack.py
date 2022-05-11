from constructs import Construct
from config import config
from service.ec2 import EC2


class VpcStack(EC2):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = self.create_vpc(
            vpc_name=f'{config.env}-{config.project_name}-vpc',
            cidr='10.0.0.0/16',
            subnet_cidr_mask=24,
            max_azs=3,
            enable_public_subnet=True,
            enable_private_subnet=True,
            nat_gateway_count=0,
            enable_vpc_flow_log=True,
            tags={
                'TestKey': 'TestValue'
            }
        )
