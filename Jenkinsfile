pipeline {
    agent any

    environment {
        MONGO_URI = "mongodb"
        MONGO_PORT = "27017"
        MONGO_USER = "root"
        MONGO_PASS = "pass"
        DOCKER_REGISTRY = "your-docker-registry" // Replace with your Docker registry URL
        DOCKER_IMAGE_NAME = "your-docker-image"
        HELM_CHART_PATH = "./your-helm-chart"
        HELM_RELEASE_NAME = "your-release-name"
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    echo 'Checking out the repository...'
                    git url: 'https://github.com/yourusername/your-repo.git'
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    echo 'Building and pushing Docker image...'
                    docker.build("${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}")
                    docker.withRegistry("${DOCKER_REGISTRY}", 'docker-registry-credentials') {
                        docker.image("${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}").push()
                    }
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo 'Running tests...'
                    sh 'docker-compose up -d --build'
                    // Wait for the application to start
                    sh 'sleep 10'

                    // Run the curl command to add data inside the container
                    def curlOutput = sh(script: "docker exec -it app  curl -X POST -d 'name=John' http://localhost:5000", returnStdout: true).trim()

                    // Check the response for the success message
                    if (curlOutput.contains('added to the database')) {
                        echo 'Data added to the database successfully.'
                    } else {
                        echo "Failed to add data to the database. Aborting pipeline."
                        return 1  // Return a non-zero value to indicate failure

                    }

                    // Cleanup: Stop and remove the containers
                    sh "docker-compose down"

                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo 'Deploying with Helm...'
                    sh "helm upgrade --install ${HELM_RELEASE_NAME} ${HELM_CHART_PATH} -f ${HELM_CHART_PATH}/values.yaml --set app.image.repository=${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME} --set app.image.tag=latest"
                }
            }
        }
    }
}
