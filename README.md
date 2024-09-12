
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
- **Admin Page**
- ![image](https://github.com/user-attachments/assets/739be630-2208-47e4-8ffe-a280f024a9e3)
![image](https://github.com/user-attachments/assets/a75e010a-38bb-4ef6-b6a2-e3f3c1bb8c95)
![image](https://github.com/user-attachments/assets/81f76552-f664-4ba5-af82-08a98cfcbb67)
![image](https://github.com/user-attachments/assets/a6fdb307-95fb-4ced-8aa5-c8549be3f261)

- **Admins** can:
  - Add new books.
  - Add other admin users.
  - Search for books using ISBN, title, or author.
    ![image](https://github.com/user-attachments/assets/d24b226e-4235-4888-bdc4-405f46d73745)
    ![image](https://github.com/user-attachments/assets/a0f96062-33b0-407d-b9a6-6d3a0a67a964)
    ![image](https://github.com/user-attachments/assets/9a18a57c-57d5-422e-897b-d9607ebdb955)
    ![image](https://github.com/user-attachments/assets/774544c0-1a10-4ed0-a6b6-16e09be7017c)
    ![image](https://github.com/user-attachments/assets/44e57825-9bc1-4743-b789-0c53311c118b)
- **User Page**
- ![image](https://github.com/user-attachments/assets/ef4a00bb-a993-46d1-be68-431a85469e42)

- **Users** can:
  - Borrow and return books.
  - Search for books using ISBN, title, or author.
![image](https://github.com/user-attachments/assets/08a0434e-2a3a-4376-9d7f-a20ab3806160)

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
![image](https://github.com/user-attachments/assets/0ceb60b2-3ffc-49cc-b1f3-ae101cd5ff8a)

### 3. **Infrastructure as Code (IaC) with Terraform**
   - Terraform was used to manage the AWS infrastructure.
   - Two modules were created:
     - **Backend Module**: For creating an S3 bucket to store Terraform state files and a DynamoDB table to prevent concurrent state changes.
     - **Main Infrastructure Module**: For creating VPC, subnets, Internet Gateway, NAT Gateway, and EKS clusters and node groups.
     - our main module contains a module for every AWS resource

### 4. **Kubernetes Deployment**
   - The application was deployed on **Amazon EKS** using Kubernetes deployment and service configuration files.
   - Two YAML files were used for deployment:
     - `library-management-deployment.yaml`: Defines the deployment configuration for the application.
     - `service.yaml`: Defines the service configuration for the application.
![image](https://github.com/user-attachments/assets/21b1e169-1bbd-40ea-850c-add44d859a1f)

### 5. **CI/CD Pipeline**
   - A CI/CD pipeline was created using **Jenkins** with the following stages:
     1. **Checkout Code**: Pulls the code from the GitHub repository.
     2. **Build Docker Image**: Builds the Docker image using the provided Dockerfile.
     3. **Push Docker Image**: Pushes the image to Docker Hub.
     4. **Deploy to EKS**: Deploys the application to the EKS cluster using `kubectl`.
     5. **Retrieve Load Balancer IP**: Retrieves the IP/hostname of the Load Balancer after deployment.
![image](https://github.com/user-attachments/assets/c4a4e743-c49c-4512-9fd1-c632812ceea6)

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
- Promethues Screen Shots:
![image](https://github.com/user-attachments/assets/ca5c0e55-5fc6-4a6f-a789-5fb7d01c3090)
![image](https://github.com/user-attachments/assets/ae7e3ec7-7b6b-4453-bf8e-f43c11d38520)
- Grafana Screen Shots
- ![image](https://github.com/user-attachments/assets/0f8dad5b-8ed8-4299-89a0-2294b5246ad7)
- ![image](https://github.com/user-attachments/assets/47cfbab5-c078-484b-9e6c-7b8c1503822f)


## Bonus Task: Terraform Pipeline:
This Jenkins pipeline is designed to automate the process of deploying infrastructure using Terraform. The pipeline includes stages for checking out source code from Git, initializing and applying Terraform configurations, and handling failures by cleaning up resources. Below is a detailed explanation of each stage and how the pipeline operates.

<h1>Please read the documentation as it is more detailed.</h1>


