pipeline {
  agent any

  environment {
    DOCKER_NAME = "jtdocker"
  }

  stages {
    stage('Start') {
      steps {
        echo '[${DOCKER_NAME}] Start'
      }
    }

    stage('Build Docker') {
      steps {
        sh 'docker build -t ${DOCKER_NAME} .'
      }
    }

    stage('Run Docker') {
      steps {
        sh 'docker run --rm --name=${DOCKER_NAME} ${DOCKER_NAME}'
      }
    }

    stage('End') {
      steps {
        echo '[${DOCKER_NAME}] End'
      }
    }

  }
}