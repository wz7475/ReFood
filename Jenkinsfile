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
            steps {
                    sh 'cd hello-world && docker build -t hello-world-fastapi .'
                    sh 'echo "BUILD SUCCESSFUL FROM BRANCH EMPTY PROJECT"'
                    sh 'docker login maluch.mikr.us:40480 -u ${NEXUS_USER} -p ${NEXUS_PASSWORD}'
                    sh 'docker tag hello-world-fastapi maluch.mikr.us:40480/refood-docker/hello-world-fastapi:latest'
                    sh 'docker push maluch.mikr.us:40480/refood-docker/hello-world-fastapi:latest'
            }
	    }
    }
    post {
        success {
            script {
                gitLabCommitStatus('success')
            }
        }
        failure {
            script {
                gitLabCommitStatus('failed')
            }
        }
    }
}
