def notifyUsers(String buildStatus) {
    def result = buildStatus ?: 'UNKNOWN'
    def recipients = (env.NOTIFICATION_EMAIL ?: 'moneywise-devops@example.com').trim()
    def subject = "[MoneyWise] ${env.JOB_NAME} #${env.BUILD_NUMBER} - ${result}"
    def body = """MoneyWise pipeline finished with status: ${result}

Job: ${env.JOB_NAME}
Build: #${env.BUILD_NUMBER}
URL: ${env.BUILD_URL ?: 'Not available'}
Branch: ${env.BRANCH_NAME ?: 'Not available'}

Artifacts generated:
- ${env.PACKAGE_DIR}/
- ${env.REPORT_DIR}/
"""

    sh "mkdir -p ${env.REPORT_DIR}/notification"
    writeFile(
        file: "${env.REPORT_DIR}/notification/last-notification.txt",
        text: """To: ${recipients}
Subject: ${subject}

${body}
"""
    )

    try {
        mail(to: recipients, subject: subject, body: body)
        echo "Notification email sent to ${recipients}"
    } catch (err) {
        echo "Notification email could not be sent by Jenkins: ${err.getMessage()}"
        echo "Notification content was saved as an artifact."
    }

    env.NOTIFICATION_SENT = 'true'
}

pipeline {
    agent any

    environment {
        APP_IMAGE = 'moneywise-app'
        PACKAGE_DIR = 'dist'
        REPORT_DIR = 'reports'
        NOTIFICATION_EMAIL = 'moneywise-devops@example.com'

        CI_SECRET_KEY = 'ci-secret-key'
        CI_SECURITY_PASSWORD_SALT = 'ci-security-salt'
        CI_JWT_SECRET_KEY = 'ci-jwt-secret'
        CI_TEST_DATABASE_URL = 'sqlite:////tmp/moneywise_test.db'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Prepare Tools') {
            steps {
                sh '''
                    set -eu

                    if ! command -v docker >/dev/null 2>&1; then
                        apt-get update
                        apt-get install -y docker.io
                    fi

                    docker --version
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    set -eu
                    docker build -t "${APP_IMAGE}:${BUILD_NUMBER}" -t "${APP_IMAGE}:latest" .
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    set -eu

                    rm -rf "${REPORT_DIR}"
                    mkdir -p "${REPORT_DIR}/tests" "${REPORT_DIR}/coverage"

                    TEST_CONTAINER="${APP_IMAGE}-tests-${BUILD_NUMBER}"
                    docker rm -f "${TEST_CONTAINER}" >/dev/null 2>&1 || true

                    docker create --name "${TEST_CONTAINER}" \
                        -e FLASK_CONFIG=testing \
                        -e SECRET_KEY="${CI_SECRET_KEY}" \
                        -e SECURITY_PASSWORD_SALT="${CI_SECURITY_PASSWORD_SALT}" \
                        -e DATABASE_URL="${CI_TEST_DATABASE_URL}" \
                        -e TEST_DATABASE_URL="${CI_TEST_DATABASE_URL}" \
                        -e TESTING=true \
                        -e WTF_CSRF_ENABLED=false \
                        -e SQLALCHEMY_TRACK_MODIFICATIONS=false \
                        -e MAIL_SERVER=localhost \
                        -e MAIL_PORT=1025 \
                        -e MAIL_USE_TLS=false \
                        -e MAIL_USE_SSL=false \
                        -e MAIL_USERNAME= \
                        -e MAIL_PASSWORD= \
                        -e MAIL_DEFAULT_SENDER=ci@moneywise.local \
                        -e MAIL_CONTACT_RECIPIENT=team@moneywise.local \
                        -e JWT_SECRET_KEY="${CI_JWT_SECRET_KEY}" \
                        -e JWT_TOKEN_LOCATION=cookies \
                        -e JWT_COOKIE_SECURE=false \
                        -e JWT_COOKIE_SAMESITE=Lax \
                        -e JWT_COOKIE_CSRF_PROTECT=false \
                        -e JWT_COOKIE_NAME=access_token_cookie \
                        -e JWT_ACCESS_COOKIE_PATH=/ \
                        -e JWT_REFRESH_COOKIE_PATH=/token/refresh \
                        -e JWT_ACCESS_TOKEN_MINUTES=15 \
                        "${APP_IMAGE}:${BUILD_NUMBER}" \
                        sh -c 'mkdir -p reports/tests reports/coverage && python -m pytest tests/unit tests/integration --junitxml=reports/tests/pytest.xml --cov=app --cov-report=term-missing --cov-report=html:reports/coverage --cov-report=xml:reports/coverage/coverage.xml --cov-fail-under=90'

                    set +e
                    docker start -a "${TEST_CONTAINER}"
                    TEST_EXIT=$?

                    docker cp "${TEST_CONTAINER}:/app/reports/." "${REPORT_DIR}/" || true
                    docker rm -f "${TEST_CONTAINER}" >/dev/null 2>&1 || true

                    exit "${TEST_EXIT}"
                '''
            }
        }

        stage('Package Image') {
            steps {
                sh '''
                    set -eu

                    rm -rf "${PACKAGE_DIR}"
                    mkdir -p "${PACKAGE_DIR}"

                    docker save "${APP_IMAGE}:${BUILD_NUMBER}" -o "${PACKAGE_DIR}/${APP_IMAGE}-${BUILD_NUMBER}.tar"
                '''
            }
        }

        stage('Notify Users') {
            steps {
                script {
                    notifyUsers(currentBuild.currentResult ?: 'SUCCESS')
                }
            }
        }
    }

    post {
        always {
            script {
                if (env.NOTIFICATION_SENT != 'true') {
                    notifyUsers(currentBuild.currentResult ?: 'UNKNOWN')
                }
            }

            junit testResults: "${env.REPORT_DIR}/tests/*.xml", allowEmptyResults: true
            archiveArtifacts(
                artifacts: "${env.PACKAGE_DIR}/**/*, ${env.REPORT_DIR}/**/*",
                fingerprint: true,
                allowEmptyArchive: true
            )
        }
    }
}
