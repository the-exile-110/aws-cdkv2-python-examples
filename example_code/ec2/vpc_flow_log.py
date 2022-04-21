from aws_cdk import (
    Stack,
    Tags as tag,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_logs as logs,
)
from constructs import Construct


class VpcFlowLogStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Vpc
        self.vpc = self.create_vpc(
            vpc_name='example-vpc',
            cidr='10.0.0.0/16',
            subnet_cidr_mask=24,
            max_azs=1,
            enable_public_subnet=True,
            enable_private_subnet=True,
            nat_gateway_count=0,
            tags={'Name': 'example-vpc', 'Environment': 'Dev'}
        )

        # Vpc Flow Log
        self.vpc_flow_log = self.create_vpc_flow_log(
            vpc_log_group_name='example-vpc-flow-log-group',
            vpc_flow_log_name='example-vpc-flow-log',
            vpc_flow_log_role_name='example-vpc-flow-log-role',
            vpc=self.vpc,
            tags={'Name': 'example-vpc-flow-log-group', 'Environment': 'example-env'}
        )

    def create_vpc(self,
                   vpc_name: str,
                   cidr: str,
                   subnet_cidr_mask: int,
                   max_azs: int = 1,
                   enable_public_subnet: bool = False,
                   enable_private_subnet: bool = False,
                   nat_gateway_count: int = 0,
                   tags: dict = None
                   ) -> ec2.Vpc:
        public_subnets = [] if not enable_public_subnet else [
            ec2.SubnetConfiguration(
                cidr_mask=subnet_cidr_mask,
                name=f'{vpc_name}-public-',
                subnet_type=ec2.SubnetType.PUBLIC,  # PRIVATE_ISOLATED | PRIVATE_WITH_NAT | PUBLIC
            )
        ]

        private_subnets = [] if not enable_private_subnet else [
            ec2.SubnetConfiguration(
                cidr_mask=subnet_cidr_mask,
                name=f'{vpc_name}-private-is-olated-',
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
            )
        ]

        private_subnets_with_nat = [] if not enable_private_subnet else [
            ec2.SubnetConfiguration(
                cidr_mask=subnet_cidr_mask,
                name=f'{vpc_name}-private-with-nat-',
                subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
            )
        ]

        subnets = public_subnets + private_subnets + private_subnets_with_nat

        vpc = ec2.Vpc(
            self, vpc_name,
            cidr=cidr,
            max_azs=max_azs,
            subnet_configuration=subnets if len(subnets) > 0 else None,
            nat_gateways=nat_gateway_count if nat_gateway_count > 0 else None,
        )
        None if not tags else [tag.of(vpc).add(key, value) for key, value in tags.items()]
        return vpc

    def create_vpc_flow_log(self,
                            vpc_log_group_name: str,
                            vpc_flow_log_name: str,
                            vpc_flow_log_role_name: str, vpc: ec2.Vpc,
                            tags: dict = None) -> logs.CfnLogGroup:
        log_group = logs.LogGroup(self, vpc_log_group_name)

        role = iam.Role(
            self, vpc_flow_log_role_name,
            assumed_by=iam.ServicePrincipal('vpc-flow-logs.amazonaws.com')
        )

        vpc_flow_log = ec2.FlowLog(
            self, vpc_flow_log_name,
            resource_type=ec2.FlowLogResourceType.from_vpc(vpc),
            destination=ec2.FlowLogDestination.to_cloud_watch_logs(log_group, role)
        )

        None if not tags else [tag.of(vpc_flow_log).add(key, value) for key, value in tags.items()]

        return vpc_flow_log
