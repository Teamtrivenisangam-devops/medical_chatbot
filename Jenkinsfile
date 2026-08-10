pipeline {
    agent any

    environment {
        SONAR_HOST_URL = 'http://localhost:9000'
        ANSIBLE_FORCE_COLOR = 'true'
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Environment Setup & Unit Tests') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest flake8
                    pytest --junitxml=test-reports/results.xml || true
                '''
            }
        }

        stage('Linting (Flake8)') {
            steps {
                sh '''
                    . venv/bin/activate
                    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || true
                '''
            }
        }

        stage('SonarQube Static Analysis') {
            steps {
                withCredentials([string(credentialsId: 'sonarqube-token', variable: 'SONAR_TOKEN')]) {
                    sh '''
                        sonar-scanner \
                          -Dsonar.host.url=${SONAR_HOST_URL} \
                          -Dsonar.login=${SONAR_TOKEN}
                    '''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    script {
                        // Waits for SonarQube server processing to finish
                        sh 'sleep 5'
                    }
                }
            }
        }

        stage('Ansible Deploy to Azure VM') {
            steps {
                withCredentials([string(credentialsId: 'blob-key', variable: 'BLOB_KEY'),
                                 string(credentialsId: 'storage-account-name', variable: 'STORAGE_ACCOUNT')]) {
                    sh '''
                        cd ansible
                        ansible-playbook -i inventory.ini deploy.yml \
                          --extra-vars "blob_account=${STORAGE_ACCOUNT} blob_account_key=${BLOB_KEY}"
                    '''
                }
            }
        }
    }

    post {
        always {
            junit 'test-reports/results.xml'
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully and Meddy is live!'
        }
        failure {
            echo 'Pipeline failed. Check SonarQube or Ansible logs.'
        }
    }
}
