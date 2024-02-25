pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Example: Use pytest for Python projects
                    sh 'pip install -r requirements.txt'  // Install dependencies if needed
                    sh 'pytest --cov=app test_app.py'   // Run tests and generate coverage report
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner';
                    withSonarQubeEnv('sonarqube') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }
    }

    post {
        always {
            // Clean up steps, if needed
        }
    }
}
