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

        stage('Terraform Init - Backend') {
            steps {
                dir('Terraform/backend-init') {  // Navigate to the Terraform directory
                    script {
                        // Retry up to 3 times in case of transient errors
                        retry(3) {
                            // Export cache directory and increase plugin download timeout
                            sh '''
                            export TF_PLUGIN_CACHE_DIR="$HOME/.terraform.d/plugin-cache"
                            terraform init -get-plugins=true -plugin-download-timeout=5m
                            '''
                        }
                    }
                }
            }
        }

        stage('Terraform Apply - Backend') {
            steps {
                dir('Terraform/backend-init') {
                    script {
                        // Retry up to 3 times in case of transient errors
                        retry(3) {
                            sh 'terraform apply -auto-approve'  // Apply Terraform configuration
                        }
                    }
                }
            }
        }

        stage('Terraform Init - Main Creation') {
            steps {
                dir('Terraform/main_creation') {  // Navigate to the Terraform directory
                    script {
                        // Retry up to 3 times in case of transient errors
                        retry(3) {
                            // Export cache directory and increase plugin download timeout
                            sh '''
                            export TF_PLUGIN_CACHE_DIR="$HOME/.terraform.d/plugin-cache"
                            terraform init -get-plugins=true -plugin-download-timeout=5m
                            '''
                        }
                    }
                }
            }
        }

        stage('Terraform Apply - Main Creation') {
            steps {
                dir('Terraform/main_creation') {
                    script {
                        // Retry up to 3 times in case of transient errors
                        retry(3) {
                            sh 'terraform apply -auto-approve'  // Apply Terraform configuration
                        }
                    }
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()  // Clean workspace after the build
        }
        failure {
            echo 'Build failed! Check the logs for more details.'  // Failure handling
        }
    }
}
