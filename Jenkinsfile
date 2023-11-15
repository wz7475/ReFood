pipeline {
    agent any

    stages {
        stage('Pull Python Docker Image') {
            steps {
                script {
                    docker.image('python:3.9').pull()
                }
            }
        }
        stage('Run Python') {
            steps {
                script {
                    docker.image('python:3.9').inside {
                        sh 'python3 -V'
                    }
                }
            }
        }
    }
}
