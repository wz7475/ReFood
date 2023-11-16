pipeline {
    agent any
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
                    sh 'echo "BUILD SUCCESSFUL"'
                    sh 'docker login maluch.mikr.us:40480 -u admin -p 4a7a7129-3e61-4aaa-866c-c81d7e71395b'
                    sh 'docker tag hello-world-fastapi maluch.mikr.us:40480/refood-docker/hello-world-fastapi:latest'
                    sh 'docker push maluch.mikr.us:40480/refood-docker/hello-world-fastapi:latest'
            }
	    }
    }
}
