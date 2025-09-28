# Multi-Region Distributed Analytics Platform

> A production-grade, chaos-tested, multi-region event ingestion system with auto-healing and full observability.

## 🎯 Problem Solved
Enterprises lose revenue when analytics pipelines go down. This system ensures **99.95% uptime** via multi-region failover.

## 🏗️ Architecture
![Architecture Diagram](docs/architecture.png)

## 🚀 Features
- ✅ Multi-region AWS failover (Route53 + EKS)
- ✅ GitOps CI/CD (GitHub Actions + ArgoCD)
- ✅ Observability (Prometheus/Grafana + Slack alerts)
- ✅ Chaos-tested resilience (LitmusChaos)
- ✅ Secure (K8s Secrets, IAM least privilege)

## 🧪 Local Dev
```bash
docker-compose up --build
curl -X POST http://localhost:8000/events -d '{"user_id":"u1","event_type":"click","url":"..."}'
