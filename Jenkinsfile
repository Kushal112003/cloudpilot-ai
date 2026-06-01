pipeline {
    agent any

    stages {

        stage('Clone Verification') {
            steps {
                echo 'Repository cloned successfully'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t cloudpilot-backend ./backend'
            }
        }

        stage('Verify Docker Image') {
            steps {
                sh 'docker images | grep cloudpilot-backend'
            }
        }

        stage('Security Scan') {
            steps {
                sh 'trivy image --exit-code 1 --severity CRITICAL cloudpilot-backend:latest'
            }
        }
    }
}
