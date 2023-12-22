pipeline {
    agent any

    environment {
        NEXUS_USER = credentials('nexus-user')
        NEXUS_PASSWORD = credentials('nexus-password')
        GITLAB_API_TOKEN = credentials('6dbbe98b-efbc-4c79-afc2-eafd13becba3')
        GITLAB_API_URL = 'https://gitlab.com/pis2023z/backend/api/v4'
        GITLAB_PROJECT_ID = '52104183'
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
        failure {
            script {
                updateGitlabCommitStatusDef(name: 'build', state: 'failed')
            }
        }
        success {
            script {
                updateGitlabCommitStatusDef(name: 'build', state: 'success')
            }
        }
        aborted {
            script {
                updateGitlabCommitStatusDef(name: 'build', state: 'canceled')
            }
        }
    }
}

def updateGitlabCommitStatusDef(Map params) {
    script {
        def apiUrl = "${env.GITLAB_API_URL}/projects/${env.GITLAB_PROJECT_ID}/statuses/${env.GIT_COMMIT}"
        def requestBody = [ state: params.state, name: params.name, context: 'jenkins' ]

        sh "curl --request POST --header 'PRIVATE-TOKEN: ${env.GITLAB_API_TOKEN}' --data-urlencode 'state=${requestBody.state}' --data-urlencode 'name=${requestBody.name}' --data-urlencode 'context=${requestBody.context}' '${apiUrl}'"
    }
}
