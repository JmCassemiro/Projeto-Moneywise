pipeline {
    agent any

    environment {
        IMAGE_NAME = "moneywise-app"
        SECRET_KEY = credentials('SECRET_KEY')
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
                sh '''
                docker run --rm \
                  -e SECRET_KEY=$SECRET_KEY \
                  $IMAGE_NAME pytest
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/test-results/**', allowEmptyArchive: true
        }
    }
}