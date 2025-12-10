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
                    config.deployK8s        = ["devops-app": "app", "devops-nginx": "nginx", "devops-db": "postgres"]
                    config.newDeployment    = false
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


//Methods
//Build methods
def performDockerBuildPush(config) {
    def apps = config.dockerBuild
    apps.each { key, value ->
        echo "[INFO] Processing Docker build for: ${key}"
        echo "[INFO] Image name: ${value}"
        dockerBuildPush(config, key, value)
    }   
}

def dockerBuildPush(config, path, imageName) {
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

//K8s apply methods
def deployK8s(config) {
    def deployments = config.deployK8s

    if (config.newDeployment) {
        sh "kubectl apply -f ./k8s"
    }
    deployments.each { key, value ->
        echo "[INFO] Deploying to K8s: ${key}"
        def path = value
        sh "kubectl apply -f ./k8s/${path}"
    }   
}