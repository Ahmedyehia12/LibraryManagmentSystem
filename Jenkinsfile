pipeline {
    agent any  // Use any available Jenkins agent
    triggers {
        pollSCM('* * * * *')  // Poll the SCM for changes every minute
    }

environment {
    AWS_ACCESS_KEY_ID = credentials('AKIAZI2LGPGWWB2A52XS')
    AWS_SECRET_ACCESS_KEY = credentials('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')
}

    
    stages {
        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM', 
                    branches: [[name: '*/maran']],  // Adjust branch name as needed
                    userRemoteConfigs: [[
                        url: 'https://github.com/Ahmedyehia12/LibraryManagmentSystem.git',
                        credentialsId: 'c6d6be8b-c4b5-450b-a13c-1b8aca95fc69'  // Jenkins credential ID for GitHub
                    ]]
                ])
            }
        }

        stage('Terraform Init - Backend') {
            steps {
                dir('Terraform/backend-init') {  // Navigate to the Terraform directory
                    sh 'terraform init'  // Initialize Terraform
                }
            }
        }

        stage('Terraform Apply - Backend') {
            steps {
                dir('Terraform/backend-init') {
                    sh 'terraform apply -auto-approve'  // Apply Terraform configuration
                }
            }
        }

        stage('Terraform Init - Main Creation') {
            steps {
                dir('Terraform/main_creation') {  // Navigate to the Terraform directory
                    sh 'terraform init'  // Initialize Terraform
                }
            }
        }

        stage('Terraform Apply - Main Creation') {
            steps {
                dir('Terraform/main_creation') {
                    sh 'terraform apply -auto-approve'  // Apply Terraform configuration
                }
            }
        }
    }
    
    post {
        always {
            node {
                cleanWs()
            }
        }
    }
}
