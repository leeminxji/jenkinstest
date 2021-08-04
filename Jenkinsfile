pipeline {
  agent any

  environment {
    DOCKER_NAME = "jtdocker"
  }

  stages {
    stage('Start') {
      steps {
        echo '[jtdocker] Start'
      }
    }

    stage('Build Docker') {
      steps {
        sh 'docker build -t jtdocker .'
      }
    }

    stage('Run Docker') {
      steps {
        sh 'docker stop jtdocker'
        sh 'docker rm jtdocker'
        sh 'docker run -it -d --name=${DOCKER_NAME} jtdocker'
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
        echo '[jtdocker] End'
      }
    }

  }
}