from aws_cdk import (
    # Duration,
    Stack,
    NestedStack,
    CfnOutput,
    aws_ec2 as ec2
)
from constructs import Construct

class VpcStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(self, "MyVpc", max_azs=2,
                                        cidr="10.10.0.0/16",
                                        subnet_configuration=[ec2.SubnetConfiguration(
                                            subnet_type=ec2.SubnetType.PUBLIC,
                                            name="MyPublic1",
                                            cidr_mask=24
                                        ), ec2.SubnetConfiguration(
                                            subnet_type=ec2.SubnetType.PUBLIC,
                                            name="MyPublic2",
                                            cidr_mask=24
                                        ), ec2.SubnetConfiguration(
                                            subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                                            name="MyPrivate1",
                                            cidr_mask=24
                                        ), ec2.SubnetConfiguration(
                                            subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                                            name="MyPrivate2",
                                            cidr_mask=24
                                        )],
                                        nat_gateways=2,
        )
        CfnOutput(self, "Output", value=self.vpc.vpc_id)

