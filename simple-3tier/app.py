#!/usr/bin/env python3
import aws_cdk as cdk
from app_stack import AppStack

app = cdk.App()

app_stack = AppStack(app, "my-app",
                    env=cdk.Environment(account='<YOUR ACCOUNT ID>', region='<YOUR REGION>')
                    )

app.synth()
