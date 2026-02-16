# Jewish Holiday API - End-to-End Infrastructure Deployment

## 📝 Project Overview
This project demonstrates a complete **Infrastructure-as-Code (IaC)** lifecycle. It automates the deployment of a secure Python-based holiday API onto a **Kubernetes (K3s)** cluster.

The solution covers the entire delivery pipeline: from application logic and containerization to cloud networking and automated resource provisioning using **Pulumi**.

---

## 🏗 Infrastructure & DevOps Stack
* **Cloud Provider**: AWS (EC2 Hosting).
* **Container Orchestration**: K3s (Lightweight Kubernetes).
* **IaC Framework**: Pulumi (Python SDK).
* **Networking & Ingress**: Traefik Ingress Controller for external traffic routing.
* **Secrets Management**: Pulumi Native Secrets provider for encrypted environment variables.



---

## 📂 Modular Project Structure
To maintain a production-grade codebase, the infrastructure is modularized to ensure separation of concerns:

- **holiday-project/**
    - **Pulumi.yaml**: Infrastructure project metadata
    - **Pulumi.dev.yaml**: Environment-specific config & encrypted secrets
    - **__main__.py**: Main Orchestrator (Invokes k8s modules)
    - **k8s_resources/**: Kubernetes Resource Package
        - **__init__.py**: Package entry point
        - **deployment.py**: Workload definition: 2 replicas & resource quotas
        - **service.py**: Internal networking (ClusterIP)
        - **ingress.py**: External traffic management (Traefik rules)

---

## ⚙️ Deep Dive: Infrastructure Management with Pulumi

One of the core strengths of this project is the use of **Pulumi** to manage the lifecycle of our resources. Unlike manual configuration (ClickOps), we treat our infrastructure as software.

### 1. State Management & Stacks
The project is managed within a **Stack** (named `dev`). This stack acts as an isolated environment that maintains the "State" of our deployment. 
* Pulumi tracks every resource (Deployment, Service, Ingress) and knows if they need to be updated, replaced, or deleted based on code changes.

### 2. Pulumi Configuration (Dynamic Parameters)
To avoid hardcoding values and make the infrastructure reusable, we utilized the **Pulumi Config** system. This allows us to inject parameters at runtime:
* **`container_image`**: Allows us to swap versions of our app without touching the code.
* **`cpu_limit` / `memory_limit`**: Defines the resource boundaries for our Kubernetes Pods.

### 3. Secrets Management (Security First)
Handling an `api_key` requires high security. We utilized Pulumi's **Built-in Encryption**:
* **Encryption at Rest**: When running `pulumi config set --secret api_key ...`, the value is encrypted using a unique provider key before being stored in the `Pulumi.dev.yaml` file.
* **Secure Injection**: The secret is passed into the Kubernetes Deployment as an **Environment Variable**. Pulumi ensures the value is masked in logs and only decrypted inside the actual Pod.



### 4. The Pulumi Automation Loop
Every time `pulumi up` is executed, the following happens:
1. **Preview**: Pulumi compares the desired state (our Python code) with the actual state (what's currently in AWS/K3s).
2. **Diff**: It calculates exactly what needs to change.
3. **Execution**: It communicates with the Kubernetes API to apply changes in the correct dependency order.
4. **Outputs**: It exports critical data, like the `ingress_ip`, for external use.

---

## 🛡 Security & Validation
* **Endpoint Protection**: Requests without headers return `401 Unauthorized`.
* **Health Check**: Successful authentication returns Jewish holiday JSON for the upcoming quarter. The following pipeline check the authentication with the api key:
* [https://github.com/Dvir-Segal/Pulumi_AWS_K8S/blob/master/.github/workflows/smoke-test.yml](url)
* **External URL**: `http://34.201.58.95`

---

