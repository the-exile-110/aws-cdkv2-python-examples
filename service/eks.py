from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_eks as eks,
    aws_kms as kms,
    aws_iam as iam,
)
from constructs import Construct

import utils
from config import config


class EKS(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

    def create_eks_cluster_with_autoscaling(self,
                                            cluster_name: str,
                                            version: str,
                                            vpc_id: str,
                                            use_private_subnets: bool = True,
                                            endpoint_access: str = 'private',
                                            custom_kms_key_alias_name: str = None,
                                            role_mapping: list[str] = None,
                                            user_mapping: list[str] = None,
                                            work_node_ssh_key_name: str = None,
                                            node_instance_type: str = None,
                                            autoscaling_group_min_size: int = None,
                                            autoscaling_group_max_size: int = None,
                                            spot_price: str = None,
                                            tags: dict = None,
                                            ) -> eks.Cluster:
        vpc = ec2.Vpc.from_lookup(self, cluster_name + '-vpc', vpc_id=vpc_id)

        match endpoint_access:
            case 'public':
                endpoint_access = eks.EndpointAccess.PUBLIC
            case 'private':
                endpoint_access = eks.EndpointAccess.PRIVATE
            case 'public-and-private':
                endpoint_access = eks.EndpointAccess.PUBLIC_AND_PRIVATE

        vpc_subnets = vpc_subnets = [ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC)]
        if use_private_subnets:
            vpc_subnets.append(ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE))

        eks_cluster = eks.Cluster(
            self, cluster_name,
            cluster_name=cluster_name,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
            default_capacity=0,
            version=eks.KubernetesVersion.of(version),
            secrets_encryption_key=kms.Alias.from_alias_name(self, custom_kms_key_alias_name,
                                                             custom_kms_key_alias_name) if custom_kms_key_alias_name else None,
            endpoint_access=endpoint_access,
            cluster_logging=[
                eks.ClusterLoggingTypes.API,
                eks.ClusterLoggingTypes.AUDIT,
                eks.ClusterLoggingTypes.AUTHENTICATOR,
                eks.ClusterLoggingTypes.CONTROLLER_MANAGER,
                eks.ClusterLoggingTypes.SCHEDULER
            ],
        )

        if role_mapping:
            for role_arn in role_mapping:
                role = iam.Role.from_role_arn(self, role_arn, role_arn)
                eks_cluster.aws_auth.add_role_mapping(role=role, groups=['system:masters'])

        if user_mapping:
            for user_arn in user_mapping:
                user = iam.User.from_user_arn(self, user_arn, user_arn=user_arn)
                eks_cluster.aws_auth.add_user_mapping(user, groups=['system:masters'])

        autoscaling_group_subnets = ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC)
        if use_private_subnets:
            autoscaling_group_subnets = ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE)
        
        eks_cluster.add_auto_scaling_group_capacity(
            f'{cluster_name}-worker-group',
            auto_scaling_group_name=f'{cluster_name}-worker-group',
            instance_type=ec2.InstanceType(node_instance_type),
            key_name=work_node_ssh_key_name,
            min_capacity=autoscaling_group_min_size,
            max_capacity=autoscaling_group_max_size,
            spot_price=spot_price,
            vpc_subnets=autoscaling_group_subnets,
        )

        utils.add_tags(source=eks_cluster, tag_value=cluster_name, env=config.env, custom_tags=tags)

        return eks_cluster
