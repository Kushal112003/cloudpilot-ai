#!/bin/bash

echo "Starting Trivy Scan..."

trivy image \
--exit-code 1 \
--severity CRITICAL \
cloudpilot-backend:latest