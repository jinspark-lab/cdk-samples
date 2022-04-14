from aws_cdk import (
    # Duration,
    Stack
)
from constructs import Construct
from chat_app.vpc_stack import VpcStack
from chat_app.ec2_stack import Ec2Stack

class ChatAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc_stack = VpcStack(self, "mychat-vpc")
        ec2_stack = Ec2Stack(self, "mychat-ec2", vpc=vpc_stack.vpc)
        ec2_stack.add_dependency(vpc_stack)

        # vpc_stack = VpcStack(scope, "chat-vpc")
        # ec2_stack = Ec2Stack(scope, "chat-ec2", vpc=vpc_stack.vpc)
