#!/usr/bin/env python3
import os
import aws_cdk as cdk
from cdkstudy_stack import CdkstudyStack

app = cdk.App()
CdkstudyStack(app, "CdkstudyStack")
app.synth()
