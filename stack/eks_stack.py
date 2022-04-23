from constructs import Construct
from config import config
from service.eks import EKS


class EksStack(EKS):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.eks_cluster = self.create_eks_cluster_with_autoscaling(
            cluster_name=f'{config.env}-{config.project_name}-eks-cluster',
            version='1.22',
            vpc_id='vpc-0f0dd4d529aa0ccdb',
            use_private_subnets=False,
            endpoint_access='public',  # 'public' | 'private' | 'public-and-private'
            node_instance_type='t3.micro',
            autoscaling_group_min_size=1,
            autoscaling_group_max_size=2,
            spot_price='0.0041',
            role_mapping=[
                'arn:aws:iam::123456789012:role/demo-role',
            ],
            user_mapping=[
                'arn:aws:iam::123456789012:user/demo-user',
            ]
        )
