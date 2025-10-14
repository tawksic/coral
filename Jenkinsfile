pipeline {
    agent {
        docker {
            image 'harbor.tawksic.com/coral/jenkins:latest'
            registryUrl 'https://harbor.tawksic.com'
            registryCredentialsId 'harbor-credentials'
            alwaysPull true
        }
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
        stage('Lint') {
            steps {
                sh 'python -m flake8 app/ --extend-ignore=E302,E501,W391'
            }
        }
    }
}
