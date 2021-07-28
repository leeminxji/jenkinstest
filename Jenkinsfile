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
        sh 'docker stop jenkinstest'
        sh 'docker rm jenkinstest'
        sh 'docker run -it -d --name=${DOCKER_NAME} jenkinstest'
      }
    }

    stage('Preprocess') {
      steps {
        sh 'docker exec ${DOCKER_NAME} python preprocess.py'
      }
    }

    stage('Training') {
      steps {
        sh 'docker exec ${DOCKER_NAME} python training.py'
      }
    }

    stage('End') {
      steps {
        echo '[jenkinstest] End'
      }
    }

  }
}