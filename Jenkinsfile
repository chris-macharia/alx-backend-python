pipeline {
    agent any

    environment {
        VIRTUAL_ENV = "${WORKSPACE}/venv"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git credentialsId: 'github-credentials', url: 'https://github.com/your-user/messaging-app.git', branch: 'main'
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh 'python3 -m venv venv'
                sh 'source venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'source venv/bin/activate && pytest --junitxml=report.xml'
            }
        }

        stage('Archive Test Report') {
            steps {
                junit 'report.xml'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'report.xml', fingerprint: true
        }
    }
}
