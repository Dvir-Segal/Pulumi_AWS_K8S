import pulumi_kubernetes as k8s

def create_deployment(labels, image, cpu, memory, env_vars):
    return k8s.apps.v1.Deployment("holiday-app-dep",
        spec=k8s.apps.v1.DeploymentSpecArgs(
            selector=k8s.meta.v1.LabelSelectorArgs(match_labels=labels),
            replicas=2,
            template=k8s.core.v1.PodTemplateSpecArgs(
                metadata=k8s.meta.v1.ObjectMetaArgs(labels=labels),
                spec=k8s.core.v1.PodSpecArgs(
                    containers=[k8s.core.v1.ContainerArgs(
                        name="holiday-app",
                        image=image,
                        resources=k8s.core.v1.ResourceRequirementsArgs(
                            limits={"cpu": cpu, "memory": memory},
                        ),
                        ports=[k8s.core.v1.ContainerPortArgs(container_port=8080)],
                        env=env_vars,
                    )],
                ),
            ),
        ))
