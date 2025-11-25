pipeline {
    agent any

    environment {
        // Docker Image Tag
        IMAGE_TAG = "divyareddy8/todo-app:latest"
        VENV = ".venv"
        // Use 'python' or 'python3' and rely on PATH.
        PYTHON_CMD = "python" 
        CONTAINER_NAME = "todo-app"
    }

    stages {
        stage('Checkout Source Code') {
            steps {
                // Git checkout remains the same
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
                // 1. Use 'rmdir /s /q' for Windows folder removal
                bat "rmdir /s /q ${env.VENV}"
                
                // 2. Create venv using Python command
                bat "${env.PYTHON_CMD} -m venv ${env.VENV}"

                // 3. Use 'Scripts\pip' on Windows
                bat "${env.VENV}\\Scripts\\pip install --upgrade pip"
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    if (fileExists('requirements.txt')) {
                        // Use 'Scripts\pip' on Windows
                        bat "${env.VENV}\\Scripts\\pip install -r requirements.txt"
                    } else {
                        error "requirements.txt not found! Cannot install dependencies."
                    }
                }
            }
        }

        stage('Run Unit and Integration Tests') {
            steps {
                // Use 'Scripts\pytest' on Windows
                bat "${env.VENV}\\Scripts\\pytest -v"
            }
        }

        stage('Build Docker Image') {
            // Docker commands work on both if Docker is in the PATH
            steps {
                bat "docker build -t ${env.IMAGE_TAG} ."
            }
        }

        stage('Push Docker Image') {
            steps {
                // Use 'bat' for the login/push commands
                withCredentials([usernamePassword(credentialsId: 'docker-creds',
                                                 usernameVariable: 'USER',
                                                 passwordVariable: 'PASS')]) {
                    bat '''
                    echo %PASS% | docker login -u %USER% --password-stdin
                    docker push %IMAGE_TAG%
                    '''
                }
            }
        }

        stage('Deploy Container') {
            // Use 'bat' for the deployment script
            steps {
                bat '''
                echo Attempting to deploy and restart container: %CONTAINER_NAME%
                docker pull %IMAGE_TAG%
                docker stop %CONTAINER_NAME%
                docker rm %CONTAINER_NAME%
                docker run -d -p 5000:5000 --name %CONTAINER_NAME% %IMAGE_TAG%
                echo Deployment complete. Container %CONTAINER_NAME% is running.
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
