#!/bin/bash
# setup.sh
cd "$(dirname "$0")/docker"
docker-compose up -d
echo "Services started. Check with: docker-compose ps"
echo "n8n UI: http://localhost:5678"
echo "Weaviate: http://localhost:8080"
echo "PostgreSQL: localhost:5432"