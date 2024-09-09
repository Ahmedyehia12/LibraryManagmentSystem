pipeline {
    agent any

    environment {
        // Define environment variables to hold AWS credentials
        AWS_ACCESS_KEY_ID = ''
        AWS_SECRET_ACCESS_KEY = ''
    }

    stages {
        stage('Checkout SCM') {
            steps {
                // Checkout the code from the Git repository
                checkout([$class: 'GitSCM', branches: [[name: '*/maran']],
                    doGenerateSubmoduleConfigurations: false, 
                    extensions: [], 
                    submoduleCfg: [], 
                    userRemoteConfigs: [[url: 'https://github.com/Ahmedyehia12/LibraryManagmentSystem']]
                ])
            }
        }

        stage('Setup Plugin Cache Directory') {
            steps {
                // Create a directory for Terraform plugin cache
                sh 'mkdir -p /var/lib/jenkins/.terraform.d/plugin-cache'
            }
        }

        stage('Terraform Init - Backend') {
            steps {
                dir('Terraform/backend-init') {
                    // Initialize Terraform backend
                    sh 'terraform init'
                }
            }
        }

        stage('Terraform Apply - Backend') {
            environment {
                // Load AWS credentials from Jenkins credentials store
                AWS_ACCESS_KEY_ID = credentials('aws-creds')
                AWS_SECRET_ACCESS_KEY = credentials('aws-creds')
            }
            steps {
                dir('Terraform/backend-init') {
                    // Apply Terraform configurations with AWS credentials
                    sh 'terraform apply -auto-approve'
                }
            }
            post {
                // Mark the build as failed if this stage fails
                failure {
                    echo 'Terraform Apply - Backend failed.'
                }
            }
        }

        stage('Terraform Init - Main Creation') {
            when {
                // Skip this stage if the previous stage failed
                not {
                    stage('Terraform Apply - Backend').result == 'FAILURE'
                }
            }
            steps {
                dir('Terraform/main-creation') {
                    // Initialize Terraform main creation
                    sh 'terraform init'
                }
            }
        }

        stage('Terraform Apply - Main Creation') {
            when {
                // Skip this stage if the previous stage failed
                not {
                    stage('Terraform Init - Main Creation').result == 'FAILURE'
                }
            }
            steps {
                dir('Terraform/main-creation') {
                    // Apply Terraform configurations for main creation
                    sh 'terraform apply -auto-approve'
                }
            }
            post {
                // Mark the build as failed if this stage fails
                failure {
                    echo 'Terraform Apply - Main Creation failed.'
                }
            }
        }
    }

    post {
        always {
            // Clean up the workspace after the pipeline completes
            cleanWs()
        }
        failure {
            // Mark the pipeline as failed
            echo 'Pipeline failed!'
        }
        success {
            // Mark the pipeline as successful
            echo 'Pipeline succeeded!'
        }
    }
}
