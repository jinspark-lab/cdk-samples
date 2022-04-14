#!/usr/bin/env python
from cdk8s import App
from kube_deploy import KubeDeploy
from kube_service import KubeService
from kube_ingress import KubeIngress
from kube_ingress_class import KubeIngressClass

class MyKube(App):
    def __init__(self):
        super().__init__()

        # Label used for tagging pods to link in the service
        label = {"app": "mycdk8s"}
        id = "mykube"

        kube_deploy = KubeDeploy(self, label, id)
        kube_service = KubeService(self, label, id)

app = MyKube()

app.synth()
