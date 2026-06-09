pipeline {
agent any

```
stages {

    stage('Checkout') {
        steps {
            git branch: 'main',
                url: 'https://github.com/palcha/Learn-CICD.git'
        }
    }

    stage('Deploy to EC2') {
        steps {
            sshagent(['ec2-ssh']) {
                sh '''
                ssh -o StrictHostKeyChecking=no ec2-user@13.51.194.130 "

                if [ ! -d /home/ec2-user/Learn-CICD ]; then
                    git clone https://github.com/palcha/Learn-CICD.git /home/ec2-user/Learn-CICD
                fi

                cd /home/ec2-user/Learn-CICD &&

                git pull origin main &&

                docker rm -f flask-demo || true &&

                docker build -t flask-demo . &&

                docker run -d \
                  --name flask-demo \
                  -p 80:5000 \
                  flask-demo
                "
                '''
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
