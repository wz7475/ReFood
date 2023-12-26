pipeline {
  agent any

  environment {
    NEXUS_USER = credentials('nexus-user')
    NEXUS_PASSWORD = credentials('nexus-password')
    GITLAB_API_TOKEN = credentials('6dbbe98b-efbc-4c79-afc2-eafd13becba3')
  }

  post {
    always {
      script {
        def status = currentBuild.currentResult == 'SUCCESS' ? 'success' :
                      currentBuild.currentResult == 'FAILURE' ? 'failed' :
                      currentBuild.currentResult == 'ABORTED' ? 'canceled' : 'unknown'

        updateGitlabCommitStatus name: 'Jenkins pipeline', state: status
      }
    }
  }

  options {
    gitLabConnection('Refood')
  }

  stages {
    stage('run tests') {
      agent {
        docker { image 'python:3.10' }
      }
      steps {
        script {
          try {
            updateGitlabCommitStatus name: 'Run tests', state: 'running'
            sh 'cd hello-world && pip install -r requirements.txt && pytest test_main.py'
            updateGitlabCommitStatus name: 'Run tests', state: 'success'
          } catch (Exception e) {
            if (e instanceof InterruptedException) {
              updateGitlabCommitStatus name: 'Run tests', state: 'canceled'  
            }
            else {
              updateGitlabCommitStatus name: 'Run tests', state: 'failed'
            }
            throw e
          }
        }
      }
    }

    stage('build images and send to nexus') {
      when {
        branch 'main'
      }
      steps {
        script {
          try {
            updateGitlabCommitStatus name: 'Build and push docker images to Nexus', state: 'running'
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
            updateGitlabCommitStatus name: 'Build and push docker images to Nexus', state: 'success'
          } catch (Exception e) {
            if (e instanceof InterruptedException) {
              updateGitlabCommitStatus name: 'Build and push docker images to Nexus', state: 'canceled'  
            }
            else {
              updateGitlabCommitStatus name: 'Build and push docker images to Nexus', state: 'failed'
            }
            throw e
          }
        }
      }
    }
    stage('Deploy application') {
      when {
        branch 'main'
      }
      steps {
        script {
          try {
            updateGitlabCommitStatus name: 'Deploy application', state: 'running'
            sh 'ssh rszczep2@172.19.0.1 "docker login maluch.mikr.us:40480 -u ${NEXUS_USER} -p ${NEXUS_PASSWORD} && docker-compose down && docker pull maluch.mikr.us:40480/refood-docker/api:latest && docker pull maluch.mikr.us:40480/refood-docker/frontend:latest && docker pull maluch.mikr.us:40480/refood-docker/fulltext:latest && docker-compose build --no-cache && docker-compose up -d"'
            updateGitlabCommitStatus name: 'Deploy application', state: 'success'
          }
          catch (Exception e) {
            if (e instanceof InterruptedException) {
              updateGitlabCommitStatus name: 'Deploy application', state: 'canceled'  
            }
            else {
              updateGitlabCommitStatus name: 'Deploy application', state: 'failed'
            }
            throw e
          }
        }
      }
    }
  }
}
