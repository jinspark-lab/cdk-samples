#!/usr/bin/env python3
import os
import aws_cdk as cdk
from eks_stack import EksStack

app = cdk.App()

eks_stack = EksStack(app, "my-eks",
                    env=cdk.Environment(account='486403792456', region='us-east-1')
                    )

app.synth()
