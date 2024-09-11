pipeline {
    agent any

    stages {
        stage('Checkout SCM') {
            steps {
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
                sh 'mkdir -p /var/lib/jenkins/.terraform.d/plugin-cache'
            }
        }

        stage('Terraform Init - Backend') {
            steps {
                dir('Terraform/backend-init') {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
                        sh 'terraform init'
                    }
                }
            }
        }

        stage('Terraform Apply - Backend') {
            steps {
                dir('Terraform/backend-init') {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
                        sh 'terraform apply -auto-approve'
                    }
                }
            }
            post {
                failure {
                    script {
                        currentBuild.result = 'FAILURE'
                        echo 'Terraform Apply - Backend failed. Cleaning up...'
                        dir('Terraform/backend-init') {
                            withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
                                sh 'terraform destroy -auto-approve'
                            }
                        }
                    }
                }
            }
        }

        stage('Terraform Init - Main Creation') {
            when {
                expression { currentBuild.result != 'FAILURE' }
            }
            steps {
                dir('Terraform/main_creation') {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
                        sh 'terraform init'
                    }
            }
            post {
                failure {
                    script {
                        currentBuild.result = 'FAILURE'
                        echo 'Terraform Init - Main Creation failed. Cleaning up...'
                        // Clean up resources created in the backend stage
                        dir('Terraform/backend-init') {
                            withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
                                sh 'terraform destroy -auto-approve'
                            }
                        }
                    }
                }
            }
        }

        stage('Terraform Apply - Main Creation') {
            when {
                expression { currentBuild.result != 'FAILURE' }
            }
            steps {
                dir('Terraform/main_creation') {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
                        sh 'terraform apply -auto-approve'
                    }
                }
            }
            post {
                failure {
                    script {
                        currentBuild.result = 'FAILURE'
                        echo 'Terraform Apply - Main Creation failed. Cleaning up...'
                        // Clean up resources created in the main creation stage
                        dir('Terraform/main_creation') {
                            withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
                                sh 'terraform destroy -auto-approve'
                            }
                        }
                        // Clean up resources created in the backend stage
                        dir('Terraform/backend-init') {
                            withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
                                sh 'terraform destroy -auto-approve'
                            }
                        }
                    }
                }
            }
        }
    }

    post {
        always {
                cleanWs() // Wrap cleanWs inside a node block
        }
        failure {
            echo 'Pipeline failed!'
        }
        success {
            echo 'Pipeline succeeded!'
        }
    }
}
