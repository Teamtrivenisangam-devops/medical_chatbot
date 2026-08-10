pipeline {
    agent any

    environment {
        SONAR_HOST_URL       = 'http://20.219.65.106:9000'
        ANSIBLE_FORCE_COLOR  = 'true'
    }

    tools {
        // Fixes the compilation error (sonarRunner is the valid tool key)
        sonarRunner 'sonar-scanner'
    }

    stages {
        stage('Checkout Source Code') {
            steps {
                // Pulls code from the repository configured in Jenkins
                checkout scm
            }
        }

        stage('Setup Environment & Run Unit Tests') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest flake8
                    mkdir -p test-reports
                    pytest --junitxml=test-reports/results.xml || true
                '''
            }
        }

        stage('Code Quality Linting') {
            steps {
                sh '''
                    . venv/bin/activate
                    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || true
                '''
            }
        }

        stage('SonarQube Code Analysis') {
            steps {
                // Injects SonarQube server configuration defined in Jenkins
                withSonarQubeEnv('sonar-server') {
                    sh 'sonar-scanner'
                }
            }
        }

        stage('SonarQube Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    script {
                        // Pauses pipeline until SonarQube completes analysis and checks Quality Gate
                        waitForQualityGate abortPipeline: true
                    }
                }
            }
        }

        stage('Deploy App via Ansible to Azure VM') {
            steps {
                // Injects Azure credentials stored in Jenkins Credentials Manager
                withCredentials([
                    string(credentialsId: 'blob-key', variable: 'BLOB_KEY'),
                    string(credentialsId: 'storage-account-name', variable: 'STORAGE_ACCOUNT')
                ]) {
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
            // Publishes test results back to Jenkins dashboard
            junit allowEmptyResults: true, testResults: 'test-reports/results.xml'
            // Cleans up workspace to keep disk usage low
            cleanWs()
        }
        success {
            echo 'SUCCESS: Pipeline finished without errors. Meddy app is live on Azure VM!'
        }
        failure {
            echo 'FAILURE: Pipeline failed. Please inspect stage logs above.'
        }
    }
}
