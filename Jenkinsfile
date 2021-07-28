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
        sh 'docker run -it -d --name=${DOCKER_NAME} jenkinstest'
      }
    }

    stage('Exec Docker') {
      steps {
        sh 'docker exec --tty jenkinstest /bin/bash'
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