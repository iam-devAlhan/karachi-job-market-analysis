#!/bin/bash

docker run --rm \
  --env-file .env \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json \
  -v $(pwd)/credentials.json:/app/credentials.json:ro \
  khi-jobs-pipeline