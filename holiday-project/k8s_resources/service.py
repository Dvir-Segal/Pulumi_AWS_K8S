import pulumi_kubernetes as k8s

def create_service(labels):
    return k8s.core.v1.Service("holiday-app-svc",
        spec=k8s.core.v1.ServiceSpecArgs(
            selector=labels,
            ports=[k8s.core.v1.ServicePortArgs(port=80, target_port=8080)],
            type="ClusterIP",
        ))
