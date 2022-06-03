## Overview

![EKS-Ingress](https://d1zrwss8zuawdm.cloudfront.net/cdk-eks-ingress.png)

This sample constructs above architecture with CDK and CDK8s.
You can start EKS Ingress sample with this simple CDK.

## Prerequisites

If you are first to use CDK, you need to run CDK BootStrap.

How to install CDK?
 : [AWS Doc](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)

This sample uses cdk8s for deploying Kubernetes objects. You should install cdk8s and uses it inside the folder(/kubernetes)      

How to install CDK8s?
 : [CNCF Doc](https://cdk8s.io/)

If you are building your own k8s Python sample, you need to initialize cdk8s directory with command below
 : cdk8s init python-app

### Please Note

This sample uses default VPC in "us-east-1". If you are going to deploy different region, you should fix the region & availability zone codes.

As this sample uses default VPC, you need to put "kubernetes.io/role/elb" tag into your Public Subnet.

* Key : kubernetes.io/role/elb      
* Value : 1

Sample deploys Application Load Balancer to the us-east-1a and us-east-1c by default.

For more detail, please refer the official document. (https://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html)


## How to Start EKS-Ingress Sample

1. cd kubernetes
2. pipenv install
3. cdk8s import --language python
4. cdk8s synth
5. cd ../
6. pip install -r requirements.txt
7. cdk synth
8. cdk deploy

If you don't set AWS CLI / CDK environment in your system, 

## Support

If you need any support, please feel free to ping me. (jinsangp@gmail.com)
Have fun!