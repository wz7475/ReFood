pipeline {
    agent any
    stages {
        stage('print variables') {
            steps{
                sh 'ls'
                sh 'ls /'
                sh 'ls /certs/client'
            }
        }
	    stage('setup requirements') {
            // steps {
            //     withPythonEnv('python3') {
            //         sh 'cd hello-world'
            //         sh 'pip -r requirements.txt'
            //     }
            // }
            agent { docker { image 'python:3.9' } }
            steps {
                    sh 'cd hello-world'
                    sh 'pip -r requirements.txt'
            }
        }
        stage('run_tests') {
    	    agent { docker { image 'python:3.9' } }
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
