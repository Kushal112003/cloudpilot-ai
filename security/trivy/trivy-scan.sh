#!/bin/bash

echo "Starting Trivy Scan..."

trivy image \
--exit-code 0 \
--severity CRITICAL \
cloudpilot-backend:latest