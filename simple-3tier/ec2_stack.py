from aws_cdk import (
    # Duration,
    Stack,
    NestedStack,
    CfnOutput,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elb,
    aws_autoscaling as autoscaling,
    aws_iam as iam
)
from constructs import Construct


linux = ec2.AmazonLinuxImage(
    generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
    edition=ec2.AmazonLinuxEdition.STANDARD,
    virtualization=ec2.AmazonLinuxVirt.HVM,
    storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
)
# with open("./user_data.sh") as f:
#     user_data = f.read()

class Ec2Stack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        role = iam.Role.from_role_arn(self, "Role", "<EC2-Instance Role>", mutable=False)
        server = ec2.Instance(self, "Instance",
                                    instance_type=ec2.InstanceType("t3.micro"),
                                    machine_image=linux,
                                    vpc=vpc,
                                    role=role
        )


