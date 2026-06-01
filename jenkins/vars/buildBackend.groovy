def call() {
    echo "Building Backend Docker Image..."

    sh '''
    docker build -t cloudpilot-backend ./backend
    docker images | grep cloudpilot-backend
    '''
}