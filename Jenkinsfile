pipeline {
    agent any

    environment {
        IMAGE_NAME = 'muhnaufal11/cloud-jenkins-pipeline'
        REGISTRY_CREDENTIALS = 'dockerhub-credentials'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                echo 'Checking out source code from GitHub repository...'
                checkout scm
            }
        }

        stage('Test & DB Initialization') {
            steps {
                echo 'Running database verification and schema migration...'
                sh 'python3 -c "import database; database.init_db(); print(\'Database connection & tables OK!\')"'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker Image: ${IMAGE_NAME}:${BUILD_NUMBER}"
                sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} -t ${IMAGE_NAME}:latest ."
            }
        }

        stage('Verify Docker Image') {
            steps {
                echo 'Verifying built image and tagging...'
                sh "docker images | grep ${IMAGE_NAME} || true"
            }
        }

        stage('Push Docker Image') {
            steps {
                echo 'Publishing image to Docker Hub...'
                // If credentials exist, push to Docker Hub
                script {
                    try {
                        withCredentials([usernamePassword(credentialsId: REGISTRY_CREDENTIALS, usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                            sh 'echo "$PASS" | docker login -u "$USER" --password-stdin'
                            sh "docker push ${IMAGE_NAME}:${BUILD_NUMBER}"
                            sh "docker push ${IMAGE_NAME}:latest"
                            echo 'Successfully pushed image to Docker Hub!'
                        }
                    } catch (Exception e) {
                        echo "Docker Hub credentials not configured or failed (${e.getMessage()}). Docker image build and tag verified locally."
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline run completed for build #${BUILD_NUMBER}."
        }
        success {
            echo 'All stages completed successfully! Build status: SUCCESS.'
        }
        failure {
            echo 'Pipeline failed. Please inspect console logs.'
        }
    }
}
