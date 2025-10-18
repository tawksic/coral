pipeline {
    agent any

    environment {
        HARBOR_REGISTRY = 'harbor.tawksic.com'
        JENKINS_IMAGE = 'coral/jenkins'
        IMAGE_TAG = "${env.BUILD_NUMBER}-${env.GIT_COMMIT[0..7]}"
        HARBOR_CREDENTIALS = credentials('harbor-credentials')
    }

    triggers {
        githubPush()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Jenkins Container') {
            steps {
                script {
                    def image = docker.build("${HARBOR_REGISTRY}/${JENKINS_IMAGE}:${IMAGE_TAG}")
                    docker.withRegistry("https://${HARBOR_REGISTRY}", 'harbor-credentials') {
                        image.push()
                        image.push('latest')
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Jenkins container built and pushed to Harbor.'
        }
        failure {
            echo 'Jenkins container build failed.'
        }
        always {
            cleanWs()
        }
    }
}
