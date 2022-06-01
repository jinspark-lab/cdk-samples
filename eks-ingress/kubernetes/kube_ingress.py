from constructs import Construct
from cdk8s import App, Chart
from imports import k8s
import cdk8s_plus_22 as kplus

class KubeIngress(Chart):
    def __init__(self, scope: Construct, id: str, service_name: str):
        super().__init__(scope, f"{id}-ingress")

        # If it is required to make ingress with ALB, service backend should route traffic to NodePort type.
        ingress_service_backend = k8s.IngressServiceBackend(
            name=service_name,
            port=k8s.ServiceBackendPort(
                number=80
            )
        )

        ingress_backend = k8s.IngressBackend(
            service=ingress_service_backend
        )

        k8s.KubeIngress(self, "ingress",
            metadata=k8s.ObjectMeta(
                annotations={
                    "kubernetes.io/ingress.class":"alb",
                    "alb.ingress.kubernetes.io/scheme":"internet-facing",
                    "alb.ingress.kubernetes.io/target-type":"instance"
                    # "alb.ingress.kubernetes.io/target-type":"ip"
                }
            ),
            spec=k8s.IngressSpec(
                default_backend=ingress_backend,
                rules=[
                    k8s.IngressRule(
                        http=k8s.HttpIngressRuleValue(
                            paths=[
                                k8s.HttpIngressPath(
                                    path='/',
                                    path_type='Prefix',
                                    backend=k8s.IngressBackend(
                                        service=ingress_service_backend
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )

