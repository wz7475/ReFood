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

        stage('build image') {
          when {
            branch 'main'
          }
            steps {
              sh 'cd hello-world && docker build -t hello-world-fastapi .'
              sh 'echo "BUILD SUCCESSFUL FROM BRANCH EMPTY PROJECT"'
              sh 'docker login maluch.mikr.us:40480 -u ${NEXUS_USER} -p ${NEXUS_PASSWORD}'
              sh 'docker tag hello-world-fastapi maluch.mikr.us:40480/refood-docker/hello-world-fastapi:latest'
              sh 'docker push maluch.mikr.us:40480/refood-docker/hello-world-fastapi:latest'
            }
        }

        stage('deploy application') {
          steps {
            sh 'ssh rszczep2@172.19.0.1 "docker login maluch.mikr.us:40480 -u ${NEXUS_USER} -p ${NEXUS_PASSWORD} && docker pull maluch.mikr.us:40480/refood-docker/hello-world-fastapi:latest && docker run hello-world-fastapi"'
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