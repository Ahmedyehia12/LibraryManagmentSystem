pipeline {
    agent any
    environment {
        TF_VAR_credentials = credentials('your-cloud-provider-credentials-id') // Cloud provider credentials
    }
    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from the GitHub repository using the PAT
                git branch: 'maran', credentialsId: 'GH-Pat', url: 'https://github.com/Ahmedyehia12/LibraryManagmentSystem.git'
            }
        }
        stage('Terraform Init') {
            steps {
                dir('Terraform') {
                    // Initialize Terraform
                    sh 'terraform init'
                }
            }
        }
        stage('Terraform Apply') {
            steps {
                dir('Terraform') {
                    // Apply Terraform configuration with auto-approve
                    sh 'terraform apply -auto-approve'
                }
            }
        }
        stage('Wait for 24 Hours') {
            steps {
                // Wait 24 hours before destroying resources
                sleep time: 24, unit: 'HOURS'
            }
        }
        stage('Terraform Destroy') {
            steps {
                dir('Terraform') {
                    // Destroy Terraform-managed infrastructure with auto-approve
                    sh 'terraform destroy -auto-approve'
                }
            }
        }
    }
    post {
        always {
            cleanWs() // Clean workspace after build
        }
        success {
            echo 'Terraform apply and destroy cycle completed successfully.'
        }
        failure {
            echo 'An error occurred during the Terraform pipeline.'
        }
    }
}
