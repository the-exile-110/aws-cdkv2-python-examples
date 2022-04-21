from aws_cdk import (
    Stack,
    Tags as tag,
    aws_iam as iam,
    aws_ec2 as ec2,
)
from constructs import Construct


class EC2InstanceStack(Stack):

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

        # Ec2 Instance Role
        self.ec2_instance_role = self.create_ec2_instance_role(
            role_name='example-ec2-instance-role',
            tags={'Name': 'example-ec2-instance-role', 'Environment': 'Dev'}
        )

        # EC2 Instance Security Group
        self.ec2_instance_security_group = self.create_ec2_instance_security_group(
            security_group_name='example-ec2-instance-security-group',
            vpc=self.vpc,
            tags={'Name': 'example-ec2-instance-security-group', 'Environment': 'Dev'}
        )

        # Ec2 Instance
        # if iops, volume_size, volume_type is None, then create the default ebs
        # Tor key_name, to create a key pair, open the EC2 Management console and click on > .Key Pairs > Create key pair
        self.ec2_instance = self.create_ec2_instance(
            instance_name='example-ec2-instance',
            instance_type='t2.micro',
            machine_image=ec2.AmazonLinuxImage(),
            vpc=self.vpc,
            subnet_type=ec2.SubnetType.PUBLIC,
            security_group=self.ec2_instance_security_group,
            role=self.ec2_instance_role,
            user_data=ec2.UserData.add_execute_file_command(self, file_path='./user-data.sh'),
            device_name='/dev/sda1',
            iops=None,
            volume_size=10,
            volume_type=ec2.EbsDeviceVolumeType.GP2,
            key_name='example-key-pair'
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

    def create_ec2_instance_role(self, role_name: str, tags: dict = None) -> iam.Role:
        role = iam.Role(
            self, role_name,
            assumed_by=iam.ServicePrincipal('ec2.amazonaws.com')
        )
        None if not tags else [tag.of(role).add(key, value) for key, value in tags.items()]
        return role

    def create_ec2_instance_security_group(self,
                                           security_group_name: str,
                                           vpc: ec2.Vpc,
                                           tags: dict = None) -> ec2.SecurityGroup:
        security_group = ec2.SecurityGroup(
            self, security_group_name,
            vpc=vpc,
            allow_all_outbound=True,
        )
        None if not tags else [tag.of(security_group).add(key, value) for key, value in tags.items()]
        return security_group

    def create_ec2_instance(self,
                            instance_name: str,
                            instance_type: str,
                            machine_image: ec2.IMachineImage,
                            vpc: ec2.Vpc,
                            subnet_type: ec2.SubnetType,
                            security_group: ec2.SecurityGroup = None,
                            role: iam.Role = None,
                            user_data: ec2.UserData = None,
                            key_name: str = None,
                            device_name: str = None,
                            iops: int = None,
                            volume_size: int = None,
                            encrypted: bool = False,
                            volume_type: ec2.EbsDeviceVolumeType = None,
                            tags: dict = None
                            ) -> ec2.Instance:
        block_device = None if not iops and volume_size and volume_type else [
            ec2.BlockDevice(
                device_name=device_name,
                volume=ec2.BlockDeviceVolume.ebs(
                    volume_size=volume_size,
                    encrypted=encrypted,
                    iops=iops,
                    volume_type=volume_type,
                )
            )
        ]

        ec2_instance = ec2.Instance(
            self, instance_name,
            instance_type=ec2.InstanceType(instance_type),
            machine_image=machine_image,
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=subnet_type,
            ),
            security_group=security_group,
            role=role,
            user_data=user_data,
            block_devices=block_device,
            key_name=key_name,
        )
        None if not tags else [tag.of(ec2_instance).add(key, value) for key, value in tags.items()]
        return ec2_instance
