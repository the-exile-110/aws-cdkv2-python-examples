import aws_cdk as cdk
from config import config

from stack.vpc_stack import VpcStack
from stack.iam_stack import IamStack

app = cdk.App()

VpcStack(app, 'vpc-stack', env=config.stack_env)
IamStack(app, 'iam-stack', env=config.stack_env)

app.synth()
