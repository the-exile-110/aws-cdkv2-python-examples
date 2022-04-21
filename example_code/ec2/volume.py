import aws_cdk as cdk
from aws_cdk import (
    Stack,
    Tags as tag,
    aws_ec2 as ec2,
    aws_kms as kms,
)
from constructs import Construct


class EbsVolumeStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.volume = self.create_ebs_volume(volume_name='example-ebs-volume',
                                             volume_type=ec2.EbsDeviceVolumeType.GP2,
                                             size=cdk.Size.gibibytes(amount=8),
                                             availability_zone='ap-northeast-1a',
                                             auto_enable_io=False,
                                             enable_multi_attach=False,
                                             encrypted=True,
                                             encryption_key=kms.Key.from_key_arn(self, 'example-kms-key',
                                                                                 'arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012'
                                                                                 ),
                                             removal_policy=cdk.RemovalPolicy.DESTROY,
                                             snapshot_id=None,
                                             tags={'Name': 'example-ebs-volume'},
                                             )

    def create_ebs_volume(self, volume_name: str,
                          volume_type: ec2.EbsDeviceVolumeType = None,
                          size: cdk.Size = None,
                          availability_zone: str = None,
                          auto_enable_io: bool = False,
                          encrypted: bool = False,
                          enable_multi_attach: bool = False,
                          encryption_key: kms.IKey = None,
                          iops: int = None,
                          removal_policy: cdk.RemovalPolicy = None,
                          snapshot_id: str = None,
                          tags: dict = None,
                          ) -> ec2.Volume:
        ebs_volume = ec2.Volume(self, volume_name,
                                volume_name=volume_name,
                                volume_type=volume_type,
                                availability_zone=availability_zone,
                                auto_enable_io=auto_enable_io,
                                size=size,
                                encrypted=encrypted,
                                enable_multi_attach=enable_multi_attach,
                                encryption_key=encryption_key,
                                iops=iops,
                                removal_policy=removal_policy,
                                snapshot_id=snapshot_id,
                                )

        [tag.of(ebs_volume).add(key, value) for key, value in tags.items()]
        return ebs_volume
