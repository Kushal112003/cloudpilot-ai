echo "Running Kubernetes Health Check..."

sh '''
export KUBECONFIG=/var/lib/jenkins/.kube/config

kubectl rollout status deployment/cloudpilot-backend \ -n cloudpilot --timeout=120s

kubectl get pods -n cloudpilot

kubectl get svc -n cloudpilot