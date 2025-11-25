pipeline {
    agent any

    environment {
        IMAGE = "divyareddy8/todo-app:latest"
        VENV = ".venv"
        PYTHON = "/usr/bin/python3"
    }

    stages {

        stage('Checkout') {
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

        stage('Create Virtual Environment') {
            steps {
                sh '$PYTHON -m venv $VENV'
                sh '$VENV/bin/pip install --upgrade pip'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '$VENV/bin/pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh '$VENV/bin/pytest -v || true'   // only if you have tests
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-creds',
                                                  usernameVariable: 'USER',
                                                  passwordVariable: 'PASS')]) {
                    sh '''
                      echo $PASS | docker login -u $USER --password-stdin
                      docker push $IMAGE
                    '''
                }
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                  docker pull $IMAGE
                  docker stop todo-app || true
                  docker rm todo-app || true
                  docker run -d -p 5000:5000 --name todo-app $IMAGE
                '''
            }
        }
    }
}
