pipeline {


agent any

environment {
    REPO_URL    = 'https://github.com/palcha/Learn-CICD.git'
    BRANCH_NAME = 'main'

    APP_NAME    = 'flask-demo'
    IMAGE_NAME  = 'chakrabortypallab42/flask-demo'
    IMAGE_TAG   = "${BUILD_NUMBER}"
}

stages {

    stage('Checkout') {
        steps {
            git branch: "${BRANCH_NAME}",
                url: "${REPO_URL}"
        }
    }

    stage('Lint Test') {
        steps {
            sh '''
            python3 -m pip install flake8 || true
            flake8 app.py || true
            '''
        }
    }

    stage('Unit Test') {
        steps {
            sh '''
            echo "Unit tests placeholder"
            '''
        }
    }

    stage('Security Scan') {
        steps {
            sh '''
            echo "Security scan placeholder"
            '''
        }
    }

    stage('Performance Test') {
        steps {
            sh '''
            echo "Performance test placeholder"
            '''
        }
    }

    stage('Build Docker Image') {
        steps {
            sh '''
            docker build \
              -t ${IMAGE_NAME}:${IMAGE_TAG} \
              -t ${IMAGE_NAME}:latest \
              .
            '''
        }
    }

    stage('Docker Login') {
        steps {
            withCredentials([
                usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )
            ]) {

                sh '''
                echo $DOCKER_PASS | docker login \
                  -u $DOCKER_USER \
                  --password-stdin
                '''
            }
        }
    }

    stage('Push Docker Image') {
        steps {
            sh '''
            docker push ${IMAGE_NAME}:${IMAGE_TAG}
            docker push ${IMAGE_NAME}:latest
            '''
        }
    }
}

post {

    success {
        echo "Docker image pushed successfully."
        echo "New ASG instances will automatically pull the latest image."
    }

    failure {
        echo "Pipeline Failed"
    }

    always {
        sh '''
        docker image prune -f || true
        '''
    }
}


}
