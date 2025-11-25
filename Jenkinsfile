pipeline {
    agent any

    environment {
        IMAGE_TAG = "divyareddy8/todo-app:latest"
        VENV = ".venv"
        PYTHON_CMD = "python3"
        CONTAINER_NAME = "todo-app"
    }

    stages {
        stage('Checkout Source Code') {
            steps {
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
                sh "rm -rf ${env.VENV} || true"
                sh "${env.PYTHON_CMD} -m venv ${env.VENV}"
                sh "${env.VENV}/bin/pip install --upgrade pip"
            }
        }

        stage('Install Dependencies') {
            steps {
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
                sh "${env.VENV}/bin/pytest -v"
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${env.IMAGE_TAG} ."
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-creds',
                                                  usernameVariable: 'USER',
                                                  passwordVariable: 'PASS')]) {
                    sh '''
                    echo "$PASS" | docker login -u "$USER" --password-stdin
                    docker push ${IMAGE_TAG}
                    '''
                }
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                echo "Deploying container: ${CONTAINER_NAME}"
                docker pull ${IMAGE_TAG}
                docker stop ${CONTAINER_NAME} || true
                docker rm ${CONTAINER_NAME} || true
                docker run -d -p 5000:5000 --name ${CONTAINER_NAME} ${IMAGE_TAG}
                echo "Deployment complete!"
                '''
            }
        }
    }

    post {
        always {
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
