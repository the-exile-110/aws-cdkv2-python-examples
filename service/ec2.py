from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_logs as logs,
    aws_iam as iam,
)
from constructs import Construct

import utils
from config import config


class EC2(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc_name = None

    def create_vpc(self,
                   vpc_name: str,
                   cidr: str,
                   subnet_cidr_mask: int,
                   max_azs: int,
                   enable_public_subnet: bool,
                   enable_private_subnet: bool,
                   nat_gateway_count: int,
                   tags: dict = None,
                   enable_vpc_flow_log: bool = False,
                   ) -> ec2.Vpc:
        self.vpc_name = vpc_name

        public_subnets = [
            ec2.SubnetConfiguration(
                cidr_mask=subnet_cidr_mask,
                name=f'{vpc_name}-public-',
                subnet_type=ec2.SubnetType.PUBLIC,
            )
        ] if enable_public_subnet else []

        private_subnets = [
            ec2.SubnetConfiguration(
                cidr_mask=subnet_cidr_mask,
                name=f'{vpc_name}-private-isolated-',
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
            )
        ] if enable_private_subnet else []

        private_subnets_with_nat = [
            ec2.SubnetConfiguration(
                cidr_mask=subnet_cidr_mask,
                name=f'{vpc_name}-private-with-nat-',
                subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
            )
        ] if nat_gateway_count > 0 else []

        subnets = public_subnets + private_subnets + private_subnets_with_nat

        vpc = ec2.Vpc(
            self, vpc_name,
            cidr=cidr,
            max_azs=max_azs,
            subnet_configuration=subnets if len(subnets) > 0 else None,
            nat_gateways=nat_gateway_count if nat_gateway_count > 0 else None,
        )

        if enable_vpc_flow_log:
            vpc_flow_log_role = self.create_vpc_flow_log_role()
            self.create_vpc_flow_log(vpc=vpc, role=vpc_flow_log_role)

        utils.add_tags(source=vpc, tag_value=vpc_name, env=config.env, custom_tags=tags)
        return vpc

    def create_vpc_flow_log_role(self) -> iam.Role:
        role_name = f'{self.vpc_name}-vpc-flow-log-role'
        vpc_flow_log_role = iam.Role(
            self, role_name,
            role_name=role_name,
            assumed_by=iam.ServicePrincipal('vpc-flow-logs.amazonaws.com'),
            inline_policies={
                f'{self.vpc_name}-vpc-flow-logs-policy': iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            actions=[
                                'logs:CreateLogGroup',
                                'logs:CreateLogStream',
                                'logs:PutLogEvents',
                            ],
                            resources=['arn:aws:logs:*:*:*'],
                        ),
                    ],
                ),
            },
        )
        utils.add_tags(source=vpc_flow_log_role, tag_value=role_name, env=config.env)
        return vpc_flow_log_role

    def create_vpc_flow_log(self, vpc: ec2.Vpc, role: iam.Role) -> ec2.FlowLog:
        vpc_log_group_name = f'{self.vpc_name}-vpc-flow-log-group'

        log_group = logs.LogGroup(self, vpc_log_group_name)

        vpc_flow_log = ec2.FlowLog(
            self, f'{self.vpc_name}-vpc-flow-log',
            resource_type=ec2.FlowLogResourceType.from_vpc(vpc),
            destination=ec2.FlowLogDestination.to_cloud_watch_logs(log_group, role)
        )

        utils.add_tags(source=log_group, tag_value=vpc_log_group_name, env=config.env)
        return vpc_flow_log

    def create_security_group(self,
                              vpc: ec2.Vpc,
                              security_group_name: str,
                              description: str,
                              ingress_rules: list,
                              egress_rules: list,
                              tags: list = None) -> ec2.SecurityGroup:
        security_group = ec2.SecurityGroup(
            self, security_group_name,
            vpc=vpc,
            description=description,
            allow_all_outbound=True,
            security_group_name=security_group_name,
            security_group_ingress=ingress_rules,
            security_group_egress=egress_rules,
        )

        utils.add_tags(source=security_group, tag_value=security_group_name, env=config.env, custom_tags=tags)
        return security_group
