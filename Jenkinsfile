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
                checkout([$class: 'GitSCM', 
                          branches: [[name: '*/maran']],
                          doGenerateSubmoduleConfigurations: false, 
                          extensions: [], 
                          submoduleCfg: [], 
                          userRemoteConfigs: [[url: 'https://github.com/Ahmedyehia12/LibraryManagmentSystem', credentialsId: 'c6d6be8b-c4b5-450b-a13c-1b8aca95fc69']]
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
            steps {
                dir('Terraform/backend-init') {
                    // Apply Terraform configurations with AWS credentials
                    sh 'terraform apply -auto-approve'
                }
            }
            post {
                failure {
                    script {
                        // Set a flag to indicate the stage failed
                        currentBuild.result = 'FAILURE'
                        env.TERRAFORM_BACKEND_APPLY_FAILED = 'true'
                    }
                    echo 'Terraform Apply - Backend failed.'
                }
            }
        }

        stage('Terraform Init - Main Creation') {
            when {
                // Skip this stage if the Terraform Apply - Backend stage failed
                expression { env.TERRAFORM_BACKEND_APPLY_FAILED != 'true' }
            }
            steps {
                dir('Terraform/main-creation') {
                    // Initialize Terraform main creation
                    sh 'terraform init'
                }
            }
            post {
                failure {
                    script {
                        // Set a flag to indicate the stage failed
                        currentBuild.result = 'FAILURE'
                        env.TERRAFORM_MAIN_INIT_FAILED = 'true'
                    }
                    echo 'Terraform Init - Main Creation failed.'
                }
            }
        }

        stage('Terraform Apply - Main Creation') {
            when {
                // Skip this stage if the Terraform Init - Main Creation stage failed
                expression { env.TERRAFORM_MAIN_INIT_FAILED != 'true' }
            }
            steps {
                dir('Terraform/main-creation') {
                    // Apply Terraform configurations for main creation
                    sh 'terraform apply -auto-approve'
                }
            }
            post {
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
