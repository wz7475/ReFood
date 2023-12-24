pipeline {
    agent any

    environment {
        NEXUS_USER = credentials('nexus-user')
        NEXUS_PASSWORD = credentials('nexus-password')
    }

    stages {
        stage('run tests') {
            agent {
              docker { image 'python:3.10' }
            }
            steps {
              sh 'cd hello-world && pip install -r requirements.txt && pytest test_main.py'
            }
        }

        stage('build images and send to nexus') {
          when{
            branch 'main'
          }
            steps {
              sh 'cd api && docker build -t api .'
              sh 'echo "api BUILD SUCCESSFUL"'
              sh 'cd frontend && docker build -t frontend .'
              sh 'echo "frontend BUILD SUCCESSFUL"'
              sh 'cd fulltext && docker build -t fulltext .'
              sh 'echo "fulltext BUILD SUCCESSFUL"'
              sh 'echo "SENDING IMAGES TO NEXUS"'
              sh 'docker login maluch.mikr.us:40480 -u ${NEXUS_USER} -p ${NEXUS_PASSWORD}'
              sh 'echo "LOGIN SUCCESSFUL"'
              sh 'docker tag api maluch.mikr.us:40480/refood-docker/api:latest'
              sh 'docker push maluch.mikr.us:40480/refood-docker/api:latest'
              sh 'echo "PUSHED api IMAGE"'
              sh 'docker tag frontend maluch.mikr.us:40480/refood-docker/frontend:latest'
              sh 'docker push maluch.mikr.us:40480/refood-docker/frontend:latest'
              sh 'echo "PUSHED frontend IMAGE"'
              sh 'docker tag fulltext maluch.mikr.us:40480/refood-docker/fulltext:latest'
              sh 'docker push maluch.mikr.us:40480/refood-docker/fulltext:latest'
              sh 'echo "PUSHED fulltext IMAGE"'
            }
        }

        stage('deploy application') {
          when{
            branch 'main'
          }
          steps {
            sh 'ssh rszczep2@172.19.0.1 "docker login maluch.mikr.us:40480 -u ${NEXUS_USER} -p ${NEXUS_PASSWORD} && docker-compose down && docker pull maluch.mikr.us:40480/refood-docker/api:latest && docker pull maluch.mikr.us:40480/refood-docker/frontend:latest && docker pull maluch.mikr.us:40480/refood-docker/fulltext:latest && docker-compose build --no-cache && docker-compose up -d"'
          }
        }
    }

    post {
      failure {
        updateGitlabCommitStatus name: 'build', state: 'failed'
      }
      success {
        updateGitlabCommitStatus name: 'build', state: 'success'
      }
      aborted {
        updateGitlabCommitStatus name: 'build', state: 'canceled'
      }
    }
}