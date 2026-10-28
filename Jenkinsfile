pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build Image') {
            steps {
                sh 'docker build -t hello-uat:${BUILD_NUMBER} .'
            }
        }
        stage('Test') {
            steps {
                sh '''
                    mkdir -p reports
                    docker run --rm -v "$WORKSPACE/reports:/app/reports" hello-uat:${BUILD_NUMBER} pytest --junitxml=reports/report.xml
                '''
            }
            post {
                always {
                    junit 'reports/report.xml'
                }
            }
        }
        stage('Run App') {
            steps {
                sh 'docker run --rm hello-uat:${BUILD_NUMBER}'
            }
        }
        stage('Monitor') {
            steps {
                sh 'docker run --rm -v "$WORKSPACE/reports:/app/reports" hello-uat:${BUILD_NUMBER} python monitor.py'
            }
        }
        stage('Archive') {
            steps {
                archiveArtifacts artifacts: 'reports/evidently_report.html', fingerprint: true
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
