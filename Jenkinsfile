pipeline {
agent any
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
                ssh -o StrictHostKeyChecking=no ec2-user@51.20.71.231 << 'EOF'

                # Clone repo first time if missing
                if [ ! -d "$HOME/Learn-CICD" ]; then
                    git clone https://github.com/palcha/Learn-CICD.git $HOME/Learn-CICD
                fi

                cd $HOME/Learn-CICD

                # Get latest code
                git pull origin main

                # Stop existing container
                docker rm -f flask-demo || true

                # Remove old image
                docker rmi flask-demo || true

                # Build new image
                docker build -t flask-demo .

                # Run new container
                docker run -d \
                  --name flask-demo \
                  -p 80:5000 \
                  flask-demo

                # Verify container
                docker ps

                EOF
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
