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
        python3 -m venv venv
        . venv/bin/activate

        pip install flake8

        flake8 . \
          --max-line-length=120 \
          --exclude=.git,__pycache__,venv \
          --ignore=W292,W293
        '''
    }
}
    stage('Unit Test') {
    steps {
        sh '''
        . venv/bin/activate

        pip install -r requirements.txt
        pip install pytest

        pytest -v
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
	#stage('Security Scan') {
    #steps {
     #   sh '''
      #  . venv/bin/activate

       # pip install bandit

        #bandit app.py test_app.py -ll
        #'''
   # }
#}

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
