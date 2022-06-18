pipeline {

  environment {
    PROJECT = "lawyer-document-search"
    APP_NAME = "search"
    FE_SVC_NAME = "${APP_NAME}-${env.BRANCH_NAME}"
    CLUSTER = "jenkins-cd"
    CLUSTER_ZONE = "us-east1-d"
    //IMAGE_TAG = "gcr.io/${PROJECT}/${APP_NAME}:${env.BRANCH_NAME}.${env.BUILD_NUMBER}"
    DEV_IMAGE_TAG = "gcr.io/${PROJECT}/${APP_NAME}:dev"
    PROD_IMAGE_TAG = "gcr.io/${PROJECT}/${APP_NAME}:latest"
    JENKINS_CRED = "${PROJECT}"
  }

  agent {
    kubernetes {
      label 'jenkins-pod'  // all your pods will be named with this prefix, followed by a unique id
      idleMinutes 4  // how long the pod will live after no jobs have run on it
      yamlFile 'pod-build.yaml'  // path to the pod definition relative to the root of our project 
      defaultContainer 'jnlp'  // define a default container if more than a few stages use it, will default to jnlp container
    }
  }
  stages {
    stage('check kubectl works') {
      when { branch 'master' }
      steps {
        container('kubectl') {
          sh "kubectl set image --namespace=frontend deployment/frontend-prod frontend-1=gcr.io/lawyer-document-search/search:latest"
        }
      }
    }
    stage('build and push dev image with cloud builder') {
      when { branch 'dev' }
      steps {
        container('gcloud') {  
          sh "PYTHONUNBUFFERED=1 gcloud builds submit -t ${DEV_IMAGE_TAG} ."  
        }
      }
    }
    stage('build and push prod image with cloud builder') {
      when { branch 'master' }
      steps {
        container('gcloud') {  
          sh "PYTHONUNBUFFERED=1 gcloud builds submit -t ${PROD_IMAGE_TAG} ."  
        }
      }
    }
  }
}
