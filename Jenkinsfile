pipeline {
  agent any
  stages {
    stage('venv') {
      steps {
        sh 'source .venv/bin/activate'
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