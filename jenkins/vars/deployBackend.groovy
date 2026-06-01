def call() {
    echo "Deploying Backend Container..."

    sh '''
    docker stop cloudpilot-backend || true
    docker rm cloudpilot-backend || true

    docker run -d \
        --name cloudpilot-backend \
        -p 8000:8000 \
        cloudpilot-backend:latest
    '''
}