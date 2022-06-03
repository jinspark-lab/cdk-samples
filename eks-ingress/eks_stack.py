from aws_cdk import (
    # Duration,
    Stack,
    aws_eks as eks,
    aws_ec2 as ec2,
    aws_iam as iam
)
from constructs import Construct
import yaml

class EksStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, id="VPC", is_default=True)

        # master IAM role that will be added to the system:masters k8s RBAC group
        master_role = iam.Role(self,
                            id=f"{construct_id}-iam-master",
                            role_name=f"{construct_id}-iam-master",
                            assumed_by=iam.AccountRootPrincipal())

        # Create Cluster with Managed NodeGroup
        cluster = eks.Cluster(self,
                            version=eks.KubernetesVersion.V1_21,
                            id=f"{construct_id}-cluster",
                            cluster_name=f"{construct_id}-cluster",
                            vpc=vpc,
                            # vpc_subnets=vpc.public_subnets,
                            vpc_subnets=[ec2.SubnetSelection(
                                subnet_type=ec2.SubnetType.PUBLIC, 
                                availability_zones=[
                                    "us-east-1a",
                                    "us-east-1c"
                                ],
                                one_per_az=True
                            )],
                            # default_capacity_instance=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.SMALL),
                            # default_capacity=2,
                            default_capacity=0,
                            alb_controller=eks.AlbControllerOptions(
                                version=eks.AlbControllerVersion.V2_3_1
                            ),
                            masters_role=master_role)

        # IAM Role for Nodes with default managed policies. (EC2 Compute)
        # Node groups should have AmazonEKSWorkerNodePolicy, AmazonEC2ContainerRegistryReadOnly, AmazonEKS_CNI_Policy
        node_role = iam.Role(self,
                            id=f"{construct_id}-iam-node",
                            role_name=f"{construct_id}-iam-node",
                            managed_policies=[
                                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEKSWorkerNodePolicy"),
                                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ContainerRegistryReadOnly"),
                                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEKS_CNI_Policy"),
                                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMFullAccess"),
                                iam.ManagedPolicy.from_aws_managed_policy_name("AWSCertificateManagerReadOnly")
                            ],
                            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        # Add Managed Node Group to Cluster
        cluster.add_nodegroup_capacity(id='my-node-group',
                                        instance_types=[
                                            ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.LARGE)
                                        ],
                                        min_size=2,
                                        max_size=4,
                                        desired_size=2,
                                        # remote_access=eks.NodegroupRemoteAccess(
                                        #     ssh_key_name="linux"
                                        # ),
                                        node_role=node_role,
                                        subnets=ec2.SubnetSelection(
                                            availability_zones=[
                                                "us-east-1a",
                                                "us-east-1c"
                                            ],
                                            one_per_az=True
                                        ),
                                        tags={
                                            "Name":"my-eks-node"
                                        }
        )

        # Add manifests to EKS Cluster
        with open("./kubernetes/dist/mykube-deploy.k8s.yaml", 'r') as stream:
            deployment_yaml = yaml.load(stream, Loader=yaml.FullLoader)
        cluster.add_manifest(f"{construct_id}-app-deployment", deployment_yaml)
        with open("./kubernetes/dist/mykube-service.k8s.yaml", 'r') as stream:
            service_yaml = yaml.load(stream, Loader=yaml.FullLoader)
        cluster.add_manifest(f"{construct_id}-app-service", service_yaml)
        with open("./kubernetes/dist/mykube-ingress.k8s.yaml", 'r') as stream:
            ingress_yaml = yaml.load(stream, Loader=yaml.FullLoader)
        cluster.add_manifest(f"{construct_id}-app-ingress", ingress_yaml)
