pipeline {
    // 1. Agent configuration
    agent any

    // 2. Environment variables for configuration
    environment {
        // Docker Image Tag - Changed to use lowercase for consistency with Docker best practices
        IMAGE_TAG = "divyareddy8/todo-app:latest"
        VENV = ".venv"
        // It's often safer to just use 'python' if it's in the PATH, but keeping /usr/bin/python3 as per your original request
        PYTHON_CMD = "/usr/bin/python3"
        CONTAINER_NAME = "todo-app"
    }

    stages {
        stage('Checkout Source Code') {
            steps {
                // Ensure the Git credentials are used correctly
                checkout([$class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/Divyareddy8/todo.git',
                        credentialsId: 'git-creds'
                    ]]
                ])
            }
        }

        stage('Setup Python Environment') {
            steps {
                // Remove existing environment to ensure a clean slate
                sh "rm -rf ${env.VENV}"
                sh "${env.PYTHON_CMD} -m venv ${env.VENV}"
                sh "${env.VENV}/bin/pip install --upgrade pip"
            }
        }

        stage('Install Dependencies') {
            steps {
                // Check if requirements.txt exists before attempting to install
                script {
                    if (fileExists('requirements.txt')) {
                        sh "${env.VENV}/bin/pip install -r requirements.txt"
                    } else {
                        error "requirements.txt not found! Cannot install dependencies."
                    }
                }
            }
        }

        stage('Run Unit and Integration Tests') {
            steps {
                // BEST PRACTICE: Removed '|| true' so the build fails if tests fail.
                // If you MUST ignore test failures, re-add '|| true'
                sh "${env.VENV}/bin/pytest -v"
            }
        }

        stage('Build Docker Image') {
            steps {
                // Using IMAGE_TAG variable defined in environment
                sh "docker build -t ${env.IMAGE_TAG} ."
            }
        }

        stage('Push Docker Image') {
            steps {
                // Use a standard approach for Docker Login/Push with credentials
                withCredentials([usernamePassword(credentialsId: 'docker-creds',
                                                 usernameVariable: 'USER',
                                                 passwordVariable: 'PASS')]) {
                    sh '''
                    echo "${PASS}" | docker login -u "${USER}" --password-stdin
                    docker push ${IMAGE_TAG}
                    '''
                }
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                echo "Attempting to deploy and restart container: ${CONTAINER_NAME}"
                
                # Pull the new image first
                docker pull ${IMAGE_TAG}
                
                # Stop and remove existing container (if it exists)
                docker stop ${CONTAINER_NAME} || true
                docker rm ${CONTAINER_NAME} || true
                
                # Run the new container instance
                docker run -d -p 5000:5000 --name ${CONTAINER_NAME} ${IMAGE_TAG}
                
                echo "Deployment complete. Container ${CONTAINER_NAME} is running."
                '''
            }
        }
    }
    
    // 3. Post-build actions for cleanup and notifications
    post {
        always {
            // Clean up the workspace to prevent issues in the next run
            cleanWs()
        }
        success {
            echo "Pipeline succeeded! Image ${env.IMAGE_TAG} deployed."
        }
        failure {
            echo "Pipeline failed. Check the logs for details."
        }
    }
}
