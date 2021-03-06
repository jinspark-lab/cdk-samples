#!/usr/bin/env python3
import os
import aws_cdk as cdk
from eks_stack import EksStack

app = cdk.App()

eks_stack = EksStack(app, "my-eks-ingress",
                    env=cdk.Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"], 
                                        region=os.environ["CDK_DEFAULT_REGION"])
                    )

app.synth()
