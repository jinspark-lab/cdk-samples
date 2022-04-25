#!/usr/bin/env python3
import aws_cdk as cdk
from eks_stack import EksStack

app = cdk.App()

eks_stack = EksStack(app, "my-eks",
                    env=cdk.Environment(account='<YOUR ACCOUNT ID>', region='<YOUR REGION>')
                    )

app.synth()
