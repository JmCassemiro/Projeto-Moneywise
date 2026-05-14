pipeline {
    agent any

    environment {
        IMAGE_NAME = "moneywise-app"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest'
            }
        }

    }

    post {
        always {
            archiveArtifacts artifacts: '**/test-results/**', allowEmptyArchive: true
        }
    }
}