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
                    sh 'terraform init'
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
                        env.TERRAFORM_BACKEND_APPLY_FAILED = 'true'
                    }
                    echo 'Terraform Apply - Backend failed.'
                }
            }
        }

        stage('Terraform Init - Main Creation') {
            when {
                expression { env.TERRAFORM_BACKEND_APPLY_FAILED != 'true' }
            }
            steps {
                dir('Terraform/main-creation') {
                    sh 'terraform init'
                }
            }
            post {
                failure {
                    script {
                        currentBuild.result = 'FAILURE'
                        env.TERRAFORM_MAIN_INIT_FAILED = 'true'
                    }
                    echo 'Terraform Init - Main Creation failed.'
                }
            }
        }

        stage('Terraform Apply - Main Creation') {
            when {
                expression { env.TERRAFORM_MAIN_INIT_FAILED != 'true' }
            }
            steps {
                dir('Terraform/main-creation') {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
                        sh 'terraform apply -auto-approve'
                    }
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
            cleanWs()
        }
        failure {
            echo 'Pipeline failed!'
        }
        success {
            echo 'Pipeline succeeded!'
        }
    }
}
