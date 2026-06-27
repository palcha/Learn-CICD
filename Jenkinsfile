pipeline {
agent any


environment {
    REPO_URL      = 'https://github.com/palcha/Learn-CICD.git'
    BRANCH_NAME   = 'main'

    IMAGE_NAME    = 'chakrabortypallab42/flask-demo'
    IMAGE_TAG     = "${BUILD_NUMBER}"

    AWS_REGION    = 'eu-north-1'
    ASG_NAME      = 'tf-demo-asg'
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
        docker run --rm \
          -v "$PWD:/app" \
          -w /app \
          python:3.12-slim \
          sh -c "
            pip install flake8 &&
            flake8 . \
              --max-line-length=120 \
              --exclude=.git,__pycache__,venv
          "
        '''
    }
}

    stage('Unit Test') {
    steps {
        sh '''
        docker run --rm \
          -v "$PWD:/app" \
          -w /app \
          python:3.12-slim \
          sh -c "
            pip install -r requirements.txt &&
            pip install pytest &&
            pytest -v
          "
        '''
    }
}

    stage('Security Scan') {
    steps {
        sh '''
        echo "===== Python SAST Scan ====="

        docker run --rm \
          -v "$PWD:/app" \
          -w /app \
          python:3.12-slim \
          sh -c "
            pip install bandit &&
            bandit -r . -ll
          "

        echo "===== Container Vulnerability Scan ====="

        docker run --rm \
          -v /var/run/docker.sock:/var/run/docker.sock \
          aquasec/trivy image \
          ${IMAGE_NAME}:latest
        '''
    }
}

    stage('Performance Test') {
        steps {
            echo 'Performance test stage placeholder'
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

    stage('Refresh Auto Scaling Group') {
steps {
withCredentials([
usernamePassword(
credentialsId: 'aws-creds',
usernameVariable: 'AWS_ACCESS_KEY_ID',
passwordVariable: 'AWS_SECRET_ACCESS_KEY'
)
]) {


        sh '''
        export AWS_DEFAULT_REGION=${AWS_REGION}

        aws autoscaling start-instance-refresh \
          --auto-scaling-group-name ${ASG_NAME}
        '''
    }
}


}

}

post {
    success {
        echo 'Pipeline Successful'
    }

    failure {
        echo 'Pipeline Failed'
    }

    always {
        sh '''
        docker image prune -f || true
        '''
    }
}


}
