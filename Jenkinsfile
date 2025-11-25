pipeline {
    agent any

    environment {
        // Docker Image Tag
        IMAGE_TAG = "divyareddy8/todo-app:latest"
        VENV = ".venv"
        // Use the full path for Python if 'python' isn't in PATH (e.g., C:\\Python313\\python.exe)
        // Sticking with 'python' for now, but be prepared to change this if it fails again.
        PYTHON_CMD = "python" 
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
                // FIX: Use '|| exit 0' to prevent build failure if the directory (.venv) doesn't exist yet.
                // This makes cleanup non-critical for the build.
                bat "rmdir /s /q ${env.VENV} || exit 0"
                
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
                // This step will likely fail if requirements.txt does not contain pytest
                bat "${env.VENV}\\Scripts\\pytest -v" 
            }
        }

        stage('Build Docker Image') {
            steps {
                bat "docker build -t ${env.IMAGE_TAG} ."
            }
        }

        stage('Push Docker Image') {
            steps {
                // Use withCredentials only to expose the variables
                withCredentials([usernamePassword(credentialsId: 'docker-creds',
                                                     usernameVariable: 'USER',
                                                     passwordVariable: 'PASS')]) {
                    // FIX: Pass the environment variables as command arguments to the bat block.
                    // This is safer than relying on bat's environment variable propagation, 
                    // especially for variables exposed by 'withCredentials'.
                    bat """
                    echo %PASS% | docker login -u %USER% --password-stdin
                    docker push ${env.IMAGE_TAG}
                    """
                }
            }
        }

        stage('Deploy Container') {
            steps {
                // Docker stop/rm commands include '|| exit 0' to prevent failure if container doesn't exist
                bat '''
                echo Attempting to deploy and restart container: %CONTAINER_NAME%
                docker pull %IMAGE_TAG%
                docker stop %CONTAINER_NAME% || exit 0
                docker rm %CONTAINER_NAME% || exit 0
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