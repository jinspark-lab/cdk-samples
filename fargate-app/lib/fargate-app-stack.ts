import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import cdk = require('aws-cdk-lib');
import ec2 = require('aws-cdk-lib/aws-ec2');
import ecs = require('aws-cdk-lib/aws-ecs');
import ecs_patterns = require('aws-cdk-lib/aws-ecs-patterns');

export class FargateAppStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const vpc = ec2.Vpc.fromLookup(this, 'Default', { isDefault: true });
    const cluster = new ecs.Cluster(this, 'Fargate', { vpc });

    const fargate = new ecs_patterns.ApplicationLoadBalancedFargateService(this, "MyFargate", {
      cluster,
      taskImageOptions: {
        containerName: 'sample',
        image: ecs.ContainerImage.fromRegistry('amazon/amazon-ecs-sample')
      }
    });

    const autoScaling = fargate.service.autoScaleTaskCount({
      maxCapacity: 2
    });
    autoScaling.scaleOnCpuUtilization('CpuScaling', {
      targetUtilizationPercent: 70,
      scaleInCooldown: cdk.Duration.seconds(60),
      scaleOutCooldown: cdk.Duration.seconds(60)
    });
    new cdk.CfnOutput(this, 'LoadBalancerDns', { value: fargate.loadBalancer.loadBalancerDnsName });
  }
}
