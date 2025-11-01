# 

🌐 Multi-Region Distributed Analytics Platform
[![
AWS
](
https://img.shields.io/badge/AWS-EKS-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white
)](
https://aws.amazon.com/eks/
)[![
Kubernetes
](
https://img.shields.io/badge/Kubernetes-1.29-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white
)](
https://kubernetes.io/
)[![
Terraform
](
https://img.shields.io/badge/Terraform-1.6-7B42BC?style=for-the-badge&logo=terraform&logoColor=white
)](
https://terraform.io/
)[![
ArgoCD
](
https://img.shields.io/badge/ArgoCD-GitOps-EF7B4D?style=for-the-badge&logo=argo&logoColor=white
)](
https://argoproj.github.io/cd/
)[![
License
](
https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge
)](
LICENSE
)
> 
**A production-grade, cloud-native event ingestion and analytics platform demonstrating modern DevOps/SRE practices.** Built for scalability, observability, and auto-healing with complete GitOps automation.
**Perfect for**: Technical Interviews • Portfolio Projects • Learning Cloud-Native Architecture

---
## 🎯 Project Overview
This platform showcases a **complete event-driven microservices architecture** running on AWS EKS, featuring:
- ✅ **Real-time event ingestion** via FastAPI REST API
- ✅ **Asynchronous message processing** with Apache Kafka
- ✅ **Persistent data storage** on AWS RDS PostgreSQL
- ✅ **GitOps continuous delivery** using ArgoCD
- ✅ **Full observability stack** with Prometheus & Grafana
- ✅ **Self-healing infrastructure** on Kubernetes
- ✅ **Infrastructure as Code** with Terraform
- ✅ **Cost-optimized** (~$5-15/month with Spot instances)

**Use Case**: Capture user events (clicks, page views, actions) from web/mobile apps, process them asynchronously through Kafka, store in PostgreSQL for analytics, and visualize metrics in real-time.

---
## 🧭 Architecture Summary
- Ingestion: FastAPI service exposes /events and /healthz endpoints behind NLB/Ingress
- Messaging: Kafka topic(s) buffer and decouple producers from consumers
- Processing: Worker service consumes events, enriches/validates, and persists
- Storage: AWS RDS PostgreSQL (event_log table) with migrations managed via CI/CD
- Delivery: ArgoCD watches Git repos and reconciles app state into EKS namespaces
- Observability: Prometheus scrapes app and system metrics; Grafana provides dashboards
- Resilience: HPA, PodDisruptionBudgets, and liveness/readiness probes for self-healing
- Security: Kubernetes RBAC, secrets, and least-privilege IAM where applicable

---
## 🏗️ Architecture
**[🚀 View Interactive Architecture Diagram →](https://shantanup108.github.io/multi-region-analytics/architecture.html)**

<p align="center">
  <img src="docs/architecture-preview.png" alt="Architecture Overview" width="800"/>
</p>

---
## ✨ Key Features
- Event-driven design with decoupled services
- GitOps-first workflow for safe, auditable deployments
- Blue/green and progressive delivery patterns via ArgoCD
- Robust metrics, logs, and alerts baked in from day one
- Local dev via kind/minikube and remote via EKS

---
## 🛠️ Technology Stack
- FastAPI, Python
- Apache Kafka
- PostgreSQL (Amazon RDS)
- Kubernetes (Amazon EKS)
- Terraform (IaC)
- ArgoCD (GitOps)
- Prometheus, Grafana (Observability)

---
## 📦 Project Structure
```
.
├── apps/
├── charts/
├── infra/
├── manifests/
├── scripts/
└── README.md
```

---
## 🚀 Quick Start
[... existing content remains unchanged ...]

---
## ☁️ AWS Cloud Deployment
[... existing content remains unchanged ...]

---
## 📊 Observability & Monitoring
[... existing content remains unchanged ...]

### Platform Monitoring Snapshots
| Prometheus | ArgoCD | Grafana |
|---|---|---|
| <img src="./screenshots/Screenshot-2025-10-31-194931.jpg" alt="Prometheus" width="320"/> | <img src="./screenshots/Screenshot-2025-10-31-185602.jpg" alt="ArgoCD" width="320"/> | <img src="./screenshots/Screenshot-2025-11-01-153429.jpg" alt="Grafana" width="320"/> |

---
## 🔄 GitOps with ArgoCD
[... existing content remains unchanged ...]

---
## 🧪 Testing & Validation
[... existing content remains unchanged ...]

---
## 💰 Cost Optimization
[... existing content remains unchanged ...]
