pipeline {
    agent any  // Use any available Jenkins agent

    environment {
        AWS_CREDENTIALS = credentials('aws-creds-id')  // Jenkins credential ID for AWS
        AWS_REGION = 'eu-central-1'  // Set to your AWS region
    }
    
    triggers {
        pollSCM('* * * * *')  // Poll the SCM for changes every minute
    }

    stages {
        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM', 
                    branches: [[name: '*/maran']],  // Adjust branch name as needed
                    userRemoteConfigs: [[
                        url: 'https://github.com/Ahmedyehia12/LibraryManagmentSystem.git',
                        credentialsId: 'MarwanMohammed2500/******'  // Jenkins credential ID for GitHub
                    ]]
                ])
            }
        }

        stage('Terraform Init') {
            steps {
                dir('terraform') {  // Navigate to the Terraform directory
                    sh 'terraform init'  // Initialize Terraform
                }
            }
        }

        stage('Terraform Apply') {
            steps {
                dir('terraform') {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds-id']]) {
                        sh 'terraform apply -auto-approve'  // Apply Terraform configuration
                    }
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()  // Clean workspace after build
        }
    }
}
