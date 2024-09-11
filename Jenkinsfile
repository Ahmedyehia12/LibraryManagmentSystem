pipeline {
    agent any
    stages {
        stage('Test Credentials') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
                    sh 'echo "Credentials are accessible"'
                }
            }
        }
    }
}
