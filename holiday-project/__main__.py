import pulumi
import pulumi_kubernetes as k8s
from k8s_resources.deployment import create_deployment
from k8s_resources.service import create_service
from k8s_resources.ingress import create_ingress

config = pulumi.Config()
api_key = config.require_secret("api_key")

env_vars = [
    k8s.core.v1.EnvVarArgs(name="APP_ENV", value=config.get("app_env")),
    k8s.core.v1.EnvVarArgs(name="API_KEY", value=api_key),
]

labels = {"app": "holiday-app"}

dept = create_deployment(labels, config.get("container_image"), config.get("cpu_limit"), config.get("memory_limit"), env_vars)
svc = create_service(labels)
ing = create_ingress(svc.metadata.name)

pulumi.export("ingress_ip", ing.status.apply(
    lambda s: s.load_balancer.ingress[0].ip if s.load_balancer.ingress else "Pending..."
))
