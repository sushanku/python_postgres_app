pipeline {
    agent any
    
    parameters {
        string(name: 'DOCKER_IMAGE', defaultValue: 'your-dockerhub-username/your-image-name', description: 'Docker image name (including DockerHub username)')
        string(name: 'DOCKER_TAG', defaultValue: '${BUILD_NUMBER}', description: 'Docker image tag')
    }

    environment {
        DOCKER_IMAGE = "${params.DOCKER_IMAGE}"
        DOCKER_TAG = "${params.DOCKER_TAG}"
        DOCKERHUB_CREDENTIALS_ID = "dockerhub_creds"
    }
    
    stages {        
        stage('Build Docker Image') {
            steps {
                    sh """
                        echo "Building docker image for flask application with postgres DB"
                        docker build -t ${params.DOCKER_IMAGE}:${params.DOCKER_TAG} .
                    """
                }
        }
        
        stage('Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: "${env.DOCKERHUB_CREDENTIALS_ID}", passwordVariable: 'DOCKERHUB_PASSWORD', usernameVariable: 'DOCKERHUB_USERNAME')]) {
                        sh """
                            echo ${DOCKERHUB_PASSWORD} | docker login -u ${DOCKERHUB_USERNAME} --password-stdin
                            docker tag ${params.DOCKER_IMAGE}:${params.DOCKER_TAG} ${params.DOCKER_IMAGE}:latest
                            docker push ${params.DOCKER_IMAGE}:latest
                        """
                    }
                }
            }
        }
        
        stage('Deploy with Docker') {
            steps {
                    sh """
                        echo "Deploying docker image for spring petclinic application"
                        docker compose -f docker-compose.yml up -d
                    """
            }
        }
    }
    
    post {
        always {
            sh "docker logout"
        }
    }
}