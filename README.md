# kdavis-eks-platform

Production-grade AWS EKS platform built from scratch using Terraform — provisioned, deployed, secured, and monitored end to end.

## What this repo contains

- **Terraform** — VPC, EKS cluster (k8s 1.31), ECR, IAM, node groups
- **App** — Containerized Flask app with Dockerfile
- **Kubernetes** — Deployment, Service, SecretProviderClass YAML
- **CI/CD** — GitHub Actions pipeline (build → ECR push → EKS deploy)

## Architecture

- VPC with public/private subnets, NAT Gateway, Internet Gateway
- EKS cluster with managed node groups (t3.medium)
- ECR container registry with vulnerability scanning
- Network Load Balancer (internet-facing) via AWS Load Balancer Controller
- AWS Secrets Manager — secrets mounted via CSI driver and IRSA
- CloudWatch Container Insights — pod restart and node CPU alarms via SNS
- Security groups layered across cluster, nodes, and load balancer
- IAM access entries and IRSA for least-privilege pod authentication

## How to deploy

### Prerequisites
- AWS CLI v2 configured
- Terraform >= 1.3.0
- kubectl
- Docker
- Helm

### Infrastructure
```bash
terraform init
terraform apply
```

### Configure kubectl
```bash
aws eks update-kubeconfig --region us-east-1 --name kdavis-eks-cluster
```

### Add cluster access
```bash
aws eks create-access-entry \
  --cluster-name kdavis-eks-cluster \
  --principal-arn arn:aws:iam::YOUR_ACCOUNT_ID:user/terraform-admin \
  --type STANDARD

aws eks associate-access-policy \
  --cluster-name kdavis-eks-cluster \
  --principal-arn arn:aws:iam::YOUR_ACCOUNT_ID:user/terraform-admin \
  --policy-arn arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy \
  --access-scope type=cluster
```

### Build and push image
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
docker build -t kdavis-app:latest ./app
docker tag kdavis-app:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/kdavis-devops-app:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/kdavis-devops-app:latest
```

### Deploy to EKS
```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f secret-provider.yaml
```

### Verify
```bash
kubectl get pods
kubectl get svc kdavis-app-service
```

## Teardown

Always delete Kubernetes services before destroying infrastructure:
```bash
kubectl delete svc kdavis-app-service
aws elb describe-load-balancers
aws elbv2 describe-load-balancers
terraform destroy
```

## CI/CD

GitHub Actions pipeline automates the full build → ECR push → EKS deploy cycle on every push to main.

See `.github/workflows/deploy.yml`

## Author

**Kelvin Davis** — Senior Cloud Platform & DevOps Engineer
- [linkedin.com/in/kelvin-davis](https://www.linkedin.com/in/kelvin-davis)
- [github.com/KDavisCodeCloud](https://github.com/KDavisCodeCloud)
