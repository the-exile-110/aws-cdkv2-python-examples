import aws_cdk as cdk
from config import config
from stack.vpc_stack import VpcStack
app = cdk.App()

VpcStack(app, 'vpc-stack', env=config.stack_env)

app.synth()
