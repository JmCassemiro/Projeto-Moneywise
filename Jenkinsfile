def notifyUsers(String buildStatus) {
    def result = buildStatus ?: 'UNKNOWN'
    def recipients = (env.NOTIFICATION_EMAIL ?: env.MAIL_CONTACT_RECIPIENT ?: '').trim()
    def sender = (env.NOTIFICATION_FROM ?: env.MAIL_DEFAULT_SENDER ?: '').trim()
    def subjectPrefix = (env.NOTIFICATION_SUBJECT_PREFIX ?: '[MoneyWise]').trim()
    def subject = "${subjectPrefix} ${env.JOB_NAME} #${env.BUILD_NUMBER} - ${result}"
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
    writeFile(file: "${env.REPORT_DIR}/notification/subject.txt", text: subject)
    writeFile(file: "${env.REPORT_DIR}/notification/body.txt", text: body)
    writeFile(
        file: "${env.REPORT_DIR}/notification/last-notification.txt",
        text: """To: ${recipients ?: 'not configured'}
From: ${sender ?: 'not configured'}
Subject: ${subject}

${body}
"""
    )

    withEnv([
        "NOTIFICATION_SUBJECT_FILE=${env.REPORT_DIR}/notification/subject.txt",
        "NOTIFICATION_BODY_FILE=${env.REPORT_DIR}/notification/body.txt"
    ]) {
        sh '''
            set -eu

            if command -v python3 >/dev/null 2>&1; then
                python3 scripts/ci/send_notification.py
            else
                echo "python3 is not available in the Jenkins image; email notification skipped."
            fi
        '''
    }

    env.NOTIFICATION_SENT = 'true'
}

pipeline {
    agent any

    environment {
        APP_IMAGE = 'moneywise-app'
        PACKAGE_DIR = 'dist'
        REPORT_DIR = 'reports'
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

                    ENV_FILE_ARGS=""
                    if [ -f .env ]; then
                        ENV_FILE_ARGS="--env-file .env"
                    fi

                    CI_SECRET_KEY_VALUE="${CI_SECRET_KEY:-$(dd if=/dev/urandom bs=32 count=1 2>/dev/null | base64 | tr -dc 'A-Za-z0-9' | head -c 48)}"
                    CI_SECURITY_PASSWORD_SALT_VALUE="${CI_SECURITY_PASSWORD_SALT:-$(dd if=/dev/urandom bs=32 count=1 2>/dev/null | base64 | tr -dc 'A-Za-z0-9' | head -c 48)}"
                    CI_JWT_SECRET_KEY_VALUE="${CI_JWT_SECRET_KEY:-$(dd if=/dev/urandom bs=32 count=1 2>/dev/null | base64 | tr -dc 'A-Za-z0-9' | head -c 48)}"
                    CI_TEST_DATABASE_URL_VALUE="${CI_TEST_DATABASE_URL:-sqlite:////tmp/moneywise_test.db}"
                    CI_MAIL_DEFAULT_SENDER_VALUE="${MAIL_DEFAULT_SENDER:-ci-${BUILD_NUMBER}@localhost}"
                    CI_MAIL_CONTACT_RECIPIENT_VALUE="${MAIL_CONTACT_RECIPIENT:-ci-${BUILD_NUMBER}@localhost}"

                    docker create --name "${TEST_CONTAINER}" \
                        ${ENV_FILE_ARGS} \
                        -e FLASK_CONFIG=testing \
                        -e DEBUG=false \
                        -e SECRET_KEY="${CI_SECRET_KEY_VALUE}" \
                        -e SECURITY_PASSWORD_SALT="${CI_SECURITY_PASSWORD_SALT_VALUE}" \
                        -e DATABASE_URL="${CI_TEST_DATABASE_URL_VALUE}" \
                        -e TEST_DATABASE_URL="${CI_TEST_DATABASE_URL_VALUE}" \
                        -e TESTING=true \
                        -e WTF_CSRF_ENABLED=false \
                        -e SQLALCHEMY_TRACK_MODIFICATIONS=false \
                        -e MAIL_SERVER="${MAIL_SERVER:-localhost}" \
                        -e MAIL_PORT="${MAIL_PORT:-1025}" \
                        -e MAIL_USE_TLS="${MAIL_USE_TLS:-false}" \
                        -e MAIL_USE_SSL="${MAIL_USE_SSL:-false}" \
                        -e MAIL_USERNAME="${MAIL_USERNAME:-}" \
                        -e MAIL_PASSWORD="${MAIL_PASSWORD:-}" \
                        -e MAIL_DEFAULT_SENDER="${CI_MAIL_DEFAULT_SENDER_VALUE}" \
                        -e MAIL_CONTACT_RECIPIENT="${CI_MAIL_CONTACT_RECIPIENT_VALUE}" \
                        -e JWT_SECRET_KEY="${CI_JWT_SECRET_KEY_VALUE}" \
                        -e JWT_TOKEN_LOCATION=cookies \
                        -e JWT_COOKIE_SECURE=false \
                        -e JWT_COOKIE_SAMESITE=Lax \
                        -e JWT_COOKIE_CSRF_PROTECT=false \
                        -e JWT_COOKIE_NAME=access_token_cookie \
                        -e JWT_ACCESS_COOKIE_PATH=/ \
                        -e JWT_REFRESH_COOKIE_PATH=/auth/refresh \
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

        stage('Package and Publish') {
            parallel {
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

                stage('Publish Docker Image') {
                    when {
                        expression { return env.DOCKERHUB_IMAGE?.trim() }
                    }
                    steps {
                        script {
                            def dockerHubCredentialsId = (env.DOCKERHUB_CREDENTIALS_ID ?: 'dockerhub-credentials').trim()

                            withCredentials([usernamePassword(
                                credentialsId: dockerHubCredentialsId,
                                usernameVariable: 'DOCKERHUB_USERNAME',
                                passwordVariable: 'DOCKERHUB_TOKEN'
                            )]) {
                                sh '''
                                    set -eu

                                    docker tag "${APP_IMAGE}:${BUILD_NUMBER}" "${DOCKERHUB_IMAGE}:${BUILD_NUMBER}"
                                    docker tag "${APP_IMAGE}:${BUILD_NUMBER}" "${DOCKERHUB_IMAGE}:latest"

                                    printf "%s" "${DOCKERHUB_TOKEN}" | docker login --username "${DOCKERHUB_USERNAME}" --password-stdin
                                    trap 'docker logout >/dev/null 2>&1 || true' EXIT

                                    docker push "${DOCKERHUB_IMAGE}:${BUILD_NUMBER}"
                                    docker push "${DOCKERHUB_IMAGE}:latest"
                                '''
                            }
                        }
                    }
                }
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
            script {
                if (fileExists("${env.REPORT_DIR}/coverage/index.html")) {
                    try {
                        publishHTML(target: [
                            allowMissing: true,
                            alwaysLinkToLastBuild: true,
                            keepAll: true,
                            reportDir: "${env.REPORT_DIR}/coverage",
                            reportFiles: 'index.html',
                            reportName: 'Coverage HTML'
                        ])
                    } catch (err) {
                        echo "HTML coverage publication skipped: ${err.getMessage()}"
                    }
                }

                if (fileExists("${env.REPORT_DIR}/coverage/coverage.xml")) {
                    try {
                        recordCoverage(
                            tools: [[parser: 'COBERTURA', pattern: "${env.REPORT_DIR}/coverage/coverage.xml"]],
                            enabledForFailure: true
                        )
                    } catch (err) {
                        echo "Coverage publication skipped: ${err.getMessage()}"
                    }
                }
            }
            archiveArtifacts(
                artifacts: "${env.PACKAGE_DIR}/**/*, ${env.REPORT_DIR}/**/*",
                fingerprint: true,
                allowEmptyArchive: true
            )
        }
    }
}
