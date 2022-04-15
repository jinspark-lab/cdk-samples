from constructs import Construct
from cdk8s import App, Chart
from imports import k8s
# from aws_cdk import CfnOutput

class KubeService(Chart):
    def __init__(self, scope: Construct, label, id: str):
        super().__init__(scope, f"{id}-service")

        # Creates the service to expose the pods to traffic from the loadbalancer (NLB)
        k8s.KubeService(self, "service",
            metadata=k8s.ObjectMeta(
                annotations={
                    "service.beta.kubernetes.io/aws-load-balancer-type":"nlb",
                    "service.beta.kubernetes.io/aws-load-balancer-scheme":"internet-facing"
                }
            ),
            spec=k8s.ServiceSpec(
                type='LoadBalancer',
                # type='NodePort',
                ports=[k8s.ServicePort(port=80, target_port=k8s.IntOrString.from_number(80))],
                selector=label
            )
        )

