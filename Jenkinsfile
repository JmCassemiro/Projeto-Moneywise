pipeline {
    agent any

    environment {
        IMAGE_NAME = "moneywise-app"
        // O Jenkins vai mascarar o valor nos logs automaticamente
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
                // Usando aspas duplas para expansão de variáveis
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Run Tests') {
            steps {
                // Criamos a pasta antes para evitar problemas de permissão com o Docker
                sh "mkdir -p htmlcov"
                
                // Rodando o container com a variável de ambiente e o volume para o relatório
                sh """
                    docker run --rm \
                    -e SECRET_KEY=${SECRET_KEY} \
                    -v \$(pwd)/htmlcov:/app/htmlcov \
                    ${IMAGE_NAME} pytest --cov=app --cov-report=html
                """
            }
        }
    }

    post {
        always {
            // Publica o relatório HTML para que você possa ver a cobertura direto na interface do Jenkins
            publishHTML([
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'htmlcov',
                reportFiles: 'index.html',
                reportName: 'Coverage Report'
            ])
            
            archiveArtifacts artifacts: 'htmlcov/**', fingerprint: true, allowEmptyArchive: true
        }
        
        // Limpeza opcional: remover a imagem local após o build para não encher o disco
        cleanup {
            sh "docker rmi ${IMAGE_NAME} || true"
        }
    }
}