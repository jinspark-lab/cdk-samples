#!/usr/bin/env python
from cdk8s import App
from kube_deploy import KubeDeploy
from kube_service import KubeService
from kube_ingress import KubeIngress

class MyKube(App):
    def __init__(self):
        super().__init__()

        # Label used for tagging pods to link in the service
        label = {"app": "mycdk8s"}
        id = "mykube"

        kube_deploy = KubeDeploy(self, label, id)
        kube_service = KubeService(self, label, id)
        service_name = kube_service.to_json()[0]['metadata']['name']
        # kube_ingress_class = KubeIngressClass(self, id)
        # ingress_class_name = kube_ingress_class.to_json()[0]['metadata']['name']
        kube_ingress = KubeIngress(self, id, service_name)


app = MyKube()

app.synth()
