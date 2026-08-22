pipeline{
    agent any
    stages {
        stage("Checkout") {
            steps{
                deleteDir()
                git url: "https://github.com/jjkusio/Phishing-analyzer", branch: "main"
            }
        }
        stage("Inspect"){
            steps{
                sh 'pwd'
                sh 'whoami'
                sh 'ls -alp'
            }
        }
        stage("Env info"){
            steps{
                sh '''
                     echo "=== Python ==="
                    if command -v python3 >/dev/null 2>&1; then
                        python3 --version
                    else
                        echo "Python3: BRAK"
                    fi

                    echo "=== Docker ==="
                    if command -v docker >/dev/null 2>&1; then
                        docker --version
                    else
                        echo "Docker: BRAK"
                    fi
                '''
            }
        }
        stage("Dockerinfo"){
            steps{
                sh 'docker info'
            }
        }
        stage("Build image"){
            steps{
                sh 'docker build -t phishing-analyzer:${BUILD_NUMBER} .'
            }
        }
        stage("Dockerrun"){
            steps{
                sh 'docker run --rm phishing-analyzer:${BUILD_NUMBER} python -m pytest -q'
            }
        }
        stage("Background image"){
            steps{
                sh 'docker run -d --name phishing-analyzer-${BUILD_NUMBER} phishing-analyzer:${BUILD_NUMBER}'
            }
        }
        stage("health check"){
            steps{
                retry(12){
                    sleep 5
                    sh "docker inspect --format='{{.State.Health.Status}}' phishing-analyzer-${BUILD_NUMBER} | grep -qx healthy"
                }
            }
        }
        stage("API smoke test") {
            steps {
                sh '''
                    STATUS=$(docker exec phishing-analyzer-${BUILD_NUMBER} \
                        curl --silent --output /dev/null --write-out "%{http_code}" \
                        --request POST \
                        --header "Content-Type: application/json" \
                        --data '{"url":"ftp://example.com"}' \
                        http://localhost:8000/v1/analyze)
        
                    echo "API returned HTTP $STATUS"
                    test "$STATUS" = "403"
                '''
            }
        }
    }
    post{
        always{
            sh 'docker rm -f phishing-analyzer-${BUILD_NUMBER} || true'
        }
    }
}
