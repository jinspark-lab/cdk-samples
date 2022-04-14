from constructs import Construct
from cdk8s import App, Chart
from imports import k8s

# Chart is container of Single k8s Manifest
class KubeDeploy(Chart):
    def __init__(self, scope: Construct, label, id: str):
        super().__init__(scope, f"{id}-deploy")

        # Creates the deployment to spin up pods with your container
        k8s.KubeDeployment(self, 'deployment',
                            spec=k8s.DeploymentSpec(
                                replicas=2,
                                selector=k8s.LabelSelector(match_labels=label),
                                template=k8s.PodTemplateSpec(
                                    metadata=k8s.ObjectMeta(labels=label),
                                    spec=k8s.PodSpec(containers=[
                                        k8s.Container(
                                            name='cdk8s',
                                            image='public.ecr.aws/s9u7u6x1/sample_app_001:no-db',
                                            ports=[k8s.ContainerPort(container_port=80)]
                                        )
                                    ])
                                )
                            ))
