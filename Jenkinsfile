pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

    stage('Install Python and Pip') {
        steps {
            script {
                sh 'apt-get update && apt-get install -y python3 python3-pip'
            }
        }
    }


        stage('Run Tests') {
            steps {
                script {
                    // Example: Use pytest for Python projects
                    sh 'python3 -m pip install -r requirements.txt'  // Install dependencies if needed
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
            cleanWs()
            // Clean up steps, if needed
        }
    }
}
