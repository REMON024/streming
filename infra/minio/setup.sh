#!/bin/sh
set -e
sleep 5
mc alias set local http://minio:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"
mc mb --ignore-existing local/videos-raw
mc mb --ignore-existing local/videos-hls
mc mb --ignore-existing local/thumbnails
mc mb --ignore-existing local/subtitles
mc mb --ignore-existing local/live-streams
mc anonymous set download local/videos-hls
mc anonymous set download local/thumbnails
mc anonymous set download local/subtitles
mc anonymous set download local/live-streams
echo "MinIO buckets ready"
