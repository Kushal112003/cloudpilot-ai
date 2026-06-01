echo "Running Trivy Scan..."

sh '''
chmod +x security/trivy/trivy-scan.sh
./security/trivy/trivy-scan.sh
'''