Here is a draft of the README file based on the provided project information:

---

# Banque Misr Internship 2024 - Library Management System

## Project Overview

This project was developed as part of the Banque Misr Internship 2024 by **Team 5**. The primary focus of the project was to create a **Library Management System** using modern web technologies, containerize the application, and deploy it on **Amazon Elastic Kubernetes Service (EKS)**. The infrastructure was provisioned using **Terraform** as Infrastructure as Code (IaC), and continuous integration/continuous deployment (CI/CD) was set up using **Jenkins**.

## Team Members

1. **Ahmed Yehia** - Scrum Master
2. **Marwan Mohammed**
3. **Safia Adel**
4. **Sama Hatem**

## Features

The Library Management System provides basic functionalities for both admins and users:

- **Admins** can:
  - Add new books.
  - Add other admin users.
  - Search for books using ISBN, title, or author.
  
- **Users** can:
  - Borrow and return books.
  - Search for books using ISBN, title, or author.

## Technologies Used

### Frontend:
- **HTML**
- **CSS**
- **JavaScript**

### Backend:
- **Python Flask**

### Database:
- **JSON files** were used to store data.

### DevOps Tools:
- **Docker** for containerization.
- **Terraform** for AWS Infrastructure management.
- **Jenkins** for CI/CD pipeline.

## Project Breakdown

### 1. **Application Development**
   - A simple Library Management System was created with user authentication, book search functionality, and borrowing and returning mechanisms.
   - Admins can manage book records and other admins.

### 2. **Dockerization**
   - A Dockerfile was created to containerize the application, specifying the base image, copying the application code, and installing dependencies.
   - The Docker image was pushed to **Docker Hub** for easy deployment.

### 3. **Infrastructure as Code (IaC) with Terraform**
   - Terraform was used to manage the AWS infrastructure.
   - Two modules were created:
     - **Backend Module**: For creating an S3 bucket to store Terraform state files and a DynamoDB table to prevent concurrent state changes.
     - **Main Infrastructure Module**: For creating VPC, subnets, Internet Gateway, NAT Gateway, and EKS clusters and node groups.

### 4. **Kubernetes Deployment**
   - The application was deployed on **Amazon EKS** using Kubernetes deployment and service configuration files.
   - Two YAML files were used for deployment:
     - `library-management-deployment.yaml`: Defines the deployment configuration for the application.
     - `service.yaml`: Defines the service configuration for the application.

### 5. **CI/CD Pipeline**
   - A CI/CD pipeline was created using **Jenkins** with the following stages:
     1. **Checkout Code**: Pulls the code from the GitHub repository.
     2. **Build Docker Image**: Builds the Docker image using the provided Dockerfile.
     3. **Push Docker Image**: Pushes the image to Docker Hub.
     4. **Deploy to EKS**: Deploys the application to the EKS cluster using `kubectl`.
     5. **Retrieve Load Balancer IP**: Retrieves the IP/hostname of the Load Balancer after deployment.

### 6. **Monitoring and Logging**
   - **Prometheus** and **Grafana** were used for monitoring:
     - Prometheus was set up to collect and store metrics.
     - Grafana was set up to visualize the metrics via dashboards.

## Infrastructure Configuration (Terraform)

### VPC Configuration:
- **CIDR Block**: `10.0.0.0/16`

### Subnets:
- **Public Subnet 1**: `10.0.1.0/24`
- **Public Subnet 2**: `10.0.2.0/24`
- **Private Subnet 1**: `10.0.3.0/24`
- **Private Subnet 2**: `10.0.4.0/24`

### Internet Gateway:
- **Name**: `team5-igw`

### NAT Gateway:
- **Name**: `team5-nat-gateway`

### IAM Roles for EKS:
- **EKS Cluster Role**
  - Policy Attachments: `AmazonEC2FullAccess`, `AmazonEKSClusterPolicy`
  
- **EKS Node Group Role**
  - Managed Policies: `AmazonEKSWorkerNodePolicy`, `AmazonEC2ContainerRegistryReadOnly`

## Prometheus & Grafana Setup

- Prometheus was used to collect metrics from the application.
- Grafana was integrated with Prometheus for visualization via a dashboard.

---

This draft README provides a comprehensive overview of the project. You can modify or add additional sections based on specific project requirements or details from the internship.
