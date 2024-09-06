pipeline {
    agent any  // Use any available Jenkins agent
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
                        credentialsId: 'c6d6be8b-c4b5-450b-a13c-1b8aca95fc69'  // Jenkins credential ID for GitHub
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
