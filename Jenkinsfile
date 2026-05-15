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
            mkdir -p htmlcov

            docker run --rm \
                -e SECRET_KEY=${SECRET_KEY} \
                -v $(pwd)/htmlcov:/app/htmlcov \
                ${IMAGE_NAME} \
                python -m pytest --cov=app --cov-report=html
        '''
    }
}

    }

    post {
        always {
            archiveArtifacts artifacts: 'htmlcov/**', fingerprint: true, allowEmptyArchive: true
        }
    }
}