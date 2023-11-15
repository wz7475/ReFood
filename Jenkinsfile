pipeline {
    agent any
    stages {
	    stage('setup requirements') {
            agent { docker { image 'python:3.12.0-alpine3.18' } }
            steps {
                step {
                    sh 'cd hello-world'
                }
                step {
                    sh 'pip -r requirements.txt'
                }
            }
        }
        stage('run_tests') {
    	    agent { docker { image 'python:3.12.0-alpine3.18' } }
            steps {
                step {
                    sh 'cd hello-world'
                }
                step {
                    sh 'pytest test_main.py'
                }
            }
        }
	    stage('build image') {
            agent { docker { image 'dind' } }
            steps {
                step {
                    sh 'cd hello-world'
                }
                step {
                    sh 'docker build -t hello-world-fastapi'
                }
                step {
                    sh 'echo "BUILD SUCCESSFUL"'
                }
            }
	    }
    }
}
