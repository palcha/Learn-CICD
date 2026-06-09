pipeline {

    agent any

    environment {
        EC2_IP      = '13.51.194.130'
        APP_PATH    = '/home/ec2-user/Learn-CICD'
        REPO_URL    = 'https://github.com/palcha/Learn-CICD.git'
        BRANCH_NAME = 'main'
        APP_NAME    = 'flask-demo'
        SSH_USER    = 'ec2-user'
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: "${BRANCH_NAME}",
                    url: "${REPO_URL}"
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent(['ec2-ssh']) {

                    sh """
                    ssh -o StrictHostKeyChecking=no ${SSH_USER}@${EC2_IP} "

                    if [ ! -d ${APP_PATH} ]; then
                        git clone ${REPO_URL} ${APP_PATH}
                    fi

                    cd ${APP_PATH} &&

                    git pull origin ${BRANCH_NAME} &&

                    docker rm -f ${APP_NAME} || true &&

                    docker build -t ${APP_NAME} . &&

                    docker run -d \
                        --name ${APP_NAME} \
                        -p 80:5000 \
                        ${APP_NAME}
                    "
                    """
                }
            }
        }
    }
}

post {
    success {
        echo 'Deployment Successful'
    }

    failure {
        echo 'Deployment Failed'
    }
}

}