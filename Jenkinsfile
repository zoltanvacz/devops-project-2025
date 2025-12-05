def config = [:]

pipeline {
    agent any
    stages {
        stage('Generate config') {
            steps {
                script {
                    echo 'Preparing the build...'
                    // Add preparation steps here
                    config.dockerBuild      = ["app": "devops-app", "nginx": "devops-nginx"]
                    config.repository       = "zoltanvacz"
                    config.tag              = "latest"
                }
            }
        }
        stage('Build') {
            steps {
                script {
                    echo 'Building the application...'
                    // Add build steps here
                    performDockerBuildPush(config)
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    echo 'Testing the application...'
                    // Add test steps here
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    echo 'Deploying the application...'
                    // Add deploy steps here
                }
            }
        }
    }
}

def performDockerBuildPush(config) {
    def apps = config.dockerBuild
    echo apps.toString()
    for (app in apps) {
        echo "[INFO] Processing Docker build for: ${app.key}"
        echo "[INFO] Image name: ${app.value}"
        dockerBuildPush(config)
    }
}

def dockerBuildPush(config) {
    def path = config.dockerBuild.key
    def imageName = config.dockerBuild.value
    def repository = config.repository
    def tag = config.tag

    echo "[INFO] Building Docker image: ${repository}/${imageName}:${tag}"

    withCredentials([usernamePassword(credentialsId: 'docker', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
        try {
            dir(path) {
                sh "docker build -t ${repository}/${imageName}:${tag} ."
                sh 'docker login -u $DOCKER_USER -p $DOCKER_PASS'
                sh "docker push ${repository}/${imageName}:${tag}"
            }
        } catch (err) {
            echo "[ERROR] Docker build or push failed: ${err}"
        }
    }
}