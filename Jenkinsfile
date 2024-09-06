pipeline {
    agent {
        // This uses any available agent with the label 'eks', which should match your EKS nodes
        label 'eks'
    }
    
    environment {
        // Replace 'aws-credentials-id' with the ID of the AWS credentials stored in Jenkins
        AWS_CREDENTIALS = credentials('aws-credentials-id')
        // Ensure AWS_REGION is set to your specific region
        AWS_REGION = 'us-west-2' // Modify to your AWS region
    }
    
    stages {
        stage('Checkout') {
            steps {
                // Checkout your Terraform directory from the specified branch
                checkout([
                    $class: 'GitSCM', 
                    branches: [[name: '*/maran']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/Ahmedyehia12/LibraryManagmentSystem.git',
                        credentialsId: 'your-jenkins-github-credentials-id'
                    ]]
                ])
            }
        }

        stage('Terraform Init') {
            steps {
                dir('Terraform') { // Navigate to your Terraform directory
                    sh 'terraform init'
                }
            }
        }

        stage('Terraform Apply') {
            steps {
                dir('Terraform') {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials-id']]) {
                        // Run terraform apply with auto-approve
                        sh 'terraform apply -auto-approve'
                    }
                }
            }
        }
        
        stage('Schedule Destroy') {
            steps {
                script {
                    // Schedule a job to run 'terraform destroy' after 24 hours
                    // You can use Jenkins Job DSL, pipeline steps like 'build' with cron, or any scheduling method available in Jenkins
                    currentBuild.rawBuild.getExecutor().interrupt() // Placeholder: customize as per your scheduling method
                }
            }
        }
    }
    
    post {
        always {
            node('eks') {  // Use the appropriate label or 'any' if EKS nodes are available to Jenkins
                cleanWs() // Clean workspace after build
            }
        }
    }
}
