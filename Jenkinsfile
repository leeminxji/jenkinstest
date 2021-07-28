pipeline {
  agent any

  environment {
    DOCKER_NAME = "jenkinstest"
  }

  stages {
    stage('Start') {
      steps {
        echo '[jenkinstest] Start'
      }
    }

    stage('Build Docker') {
      steps {
        sh 'docker build -t jenkinstest .'
      }
    }

    stage('Run Docker') {
      steps {
        sh 'docker run -it -d jenkinstest --name=${DOCKER_NAME}'
      }
    }

    stage('Exec Docker') {
      steps {
        sh 'docker exec -it jenkinstest /bin/bash'
      }
    }

    stage('Preprocess') {
      steps {
        sh 'python preprocess.py'
      }
    }

    stage('Training') {
      steps {
        sh 'python training.py'
      }
    }

    stage('End') {
      steps {
        echo '[jenkinstest] End'
      }
    }

  }
}