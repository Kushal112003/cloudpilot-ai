echo "Deploying Backend to Kubernetes..."

sh '''
export KUBECONFIG=/var/lib/jenkins/.kube/config

echo "Importing image into K3s..."

docker save cloudpilot-backend:latest -o cloudpilot-backend.tar

sudo k3s ctr images import cloudpilot-backend.tar

echo "Applying manifests..."

kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/backend-deployment.yaml
kubectl apply -f kubernetes/backend-service.yaml

echo "Waiting for rollout..."

kubectl rollout status deployment/cloudpilot-backend -n cloudpilot --timeout=120s
'''