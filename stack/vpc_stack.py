from constructs import Construct
from config import config
from service.ec2 import EC2


class VpcStack(EC2):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc_cidr: str = '10.0.0.0/16'
        subnet_cidr_mask: int = 24
        max_azs: int = 3
        enable_public_subnet: bool = True
        enable_private_subnet: bool = True
        nat_gateway_count: int = 0
        self.vpc = self.create_vpc(
            vpc_name=f'{config.env}-{config.project_name}-vpc',
            cidr=vpc_cidr,
            subnet_cidr_mask=subnet_cidr_mask,
            max_azs=max_azs,
            enable_public_subnet=enable_public_subnet,
            enable_private_subnet=enable_private_subnet,
            nat_gateway_count=nat_gateway_count,
            enable_vpc_flow_log=True,
            tags={
                'TestKey': 'TestValue'
            }
        )
