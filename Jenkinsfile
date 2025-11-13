pipeline {
  agent { label 'docker-agent'}

  stages {
    stage('Checkout') {
      steps {
        git branch: 'main', url: 'https://github.com/sreeharinath1/my_web.git'
      }
    }

    stage('Build Docker Images') {
      steps {
        sh 'docker-compose build'
      }
    }
    stage('Deploy') {
      steps {
        sh 'docker-compose up -d'
      }
    }
  }

  }
}

