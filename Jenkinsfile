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
                sh 'python -m flake8 app/ --ignore=E302'
            }
        }
    }
}
