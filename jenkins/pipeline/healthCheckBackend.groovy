echo "Running Health Check..."

sh '''
sleep 10
curl -f http://localhost:8000/health
'''