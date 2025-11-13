pipeline {
    agent { label 'docker-agent'}
    environment {
        DOCKER_CREDS = 'dockerhub_credentials'
        IMAGE_NAME = 'sreeharinathpdev/justme'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }
    stages{
        stage('Checkout') {
            steps{
                git branch: 'main', url: 'https://github.com/sreeharinath1/my_web.git'  
            }

        }
        stage(' Build Docker Image') {
            steps{
                script{
                    dockerImage = docker.build("${env.IMAGE_NAME}:${env.IMAGE_TAG}")
                }
            }
        }
        stage('Push Docker Image') {
            steps{
                script{
                    docker.withRegistry('https://registry.hub.docker.com', DOCKER_CREDS)
                    {
                    dockerImage.push()
                    dockerImage.push('latest')
                    }
                }
            }
        }
        stage('Approval Gate') {
    steps {
        script {
            timeout(time: 1, unit: 'HOURS') {   // Optional: auto-abort after 1 hour
                input message: 'Deploy to Production?', ok: 'Approve'
            }
        }
    }
}
        stage('Deploy Container') {
            steps {
                script {
                    sh '''
					#private : docker login myprivateregistry.com -u $DOCKER_USER -p $DOCKER_PASS
                    docker ps -q --filter "name=justme" | grep -q . && docker stop justme && docker rm justme || true
                    docker run -d --name justme -p 8000:8000 sreeharinathpdev/justme:${IMAGE_TAG}
                    '''
        }
    }
}

    }
    post {
        success {
            echo 'Iam success..............'
        }
        failure {
            echo 'Iam failure.........................'
        }
        always {
            echo ' cleaning work place...............................'
            cleanWs()
            echo 'complete cleaning'
        }
    }
}
