## Overview

![EKS-Service](https://d1zrwss8zuawdm.cloudfront.net/cdk-eks-service.png)

This sample constructs above architecture with CDK and CDK8s.
You can start EKS Service sample with this simple CDK.

## Prerequisites

If you are first to use CDK, you need to run CDK BootStrap.

How to install CDK?
 : [AWS Doc](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)


This sample uses cdk8s for deploying Kubernetes objects. You should install cdk8s and uses it inside the folder(/kubernetes)      

How to install CDK8s?
 : [CNCF Doc](https://cdk8s.io/)

## How to Start EKS-Service Sample

1. cd kubernetes
2. cdk8s init python-app
3. cdk8s synth
4. cd ../
5. cdk synth
6. cdk deploy

## Support

If you need any support, please feel free to ping me. (jinsangp@gmail.com)
Have fun!