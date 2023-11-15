pipeline {
    agent any
    stages {
	    stage('setup requirements') {
            agent { docker { image 'python:3.12.0-alpine3.18' } }
            steps {
                    sh 'cd hello-world'
                    sh 'pip -r requirements.txt'
            }
        }
        stage('run_tests') {
    	    agent { docker { image 'python:3.12.0-alpine3.18' } }
            steps {
                    sh 'cd hello-world'
                    sh 'pytest test_main.py'
            }
        }
	    stage('build image') {
            agent { docker { image 'dind' } }
            steps {
                    sh 'cd hello-world'
                    sh 'docker build -t hello-world-fastapi'
                    sh 'echo "BUILD SUCCESSFUL"'
            }
	    }
    }
}
