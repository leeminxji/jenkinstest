pipeline {
  agent any
  stages {
    stage('Start') {
      steps {
        echo 'Jenkins Pipeline Start'
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
        echo 'Jenkins Pipeline End'
      }
    }

  }
}