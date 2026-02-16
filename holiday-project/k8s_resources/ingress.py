import pulumi_kubernetes as k8s

def create_ingress(service_name):
    return k8s.networking.v1.Ingress("holiday-app-ingress",
        metadata=k8s.meta.v1.ObjectMetaArgs(
            annotations={"kubernetes.io/ingress.class": "traefik"}
        ),
        spec=k8s.networking.v1.IngressSpecArgs(
            rules=[k8s.networking.v1.IngressRuleArgs(
                http=k8s.networking.v1.HTTPIngressRuleValueArgs(
                    paths=[k8s.networking.v1.HTTPIngressPathArgs(
                        path="/",
                        path_type="Prefix",
                        backend=k8s.networking.v1.IngressBackendArgs(
                            service=k8s.networking.v1.IngressServiceBackendArgs(
                                name=service_name,
                                port=k8s.networking.v1.ServiceBackendPortArgs(number=80),
                            ),
                        ),
                    )],
                ),
            )],
        ))
