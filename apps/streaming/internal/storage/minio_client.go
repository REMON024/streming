package storage

import (
	"context"
	"io"
	"time"

	"github.com/minio/minio-go/v7"
	"github.com/minio/minio-go/v7/pkg/credentials"
	"streaming/internal/config"
	"go.uber.org/zap"
)

type MinioClient struct {
	client *minio.Client
	logger *zap.Logger
}

func NewMinioClient(cfg *config.Config, logger *zap.Logger) *MinioClient {
	client, err := minio.New(cfg.MinioEndpoint, &minio.Options{
		Creds:  credentials.NewStaticV4(cfg.MinioAccessKey, cfg.MinioSecretKey, ""),
		Secure: cfg.MinioUseSSL,
	})
	if err != nil {
		logger.Fatal("failed to create MinIO client", zap.Error(err))
	}
	return &MinioClient{client: client, logger: logger}
}

func (m *MinioClient) GetObject(bucket, key string) (io.ReadCloser, error) {
	obj, err := m.client.GetObject(context.Background(), bucket, key, minio.GetObjectOptions{})
	if err != nil {
		return nil, err
	}
	return obj, nil
}

func (m *MinioClient) PutObject(bucket, key string, r io.Reader, size int64, contentType string) error {
	_, err := m.client.PutObject(context.Background(), bucket, key, r, size,
		minio.PutObjectOptions{ContentType: contentType})
	return err
}

func (m *MinioClient) PresignedGetURL(bucket, key string, expiry time.Duration) (string, error) {
	url, err := m.client.PresignedGetObject(context.Background(), bucket, key, expiry, nil)
	if err != nil {
		return "", err
	}
	return url.String(), nil
}

func (m *MinioClient) FGetObject(bucket, key, localPath string) error {
	return m.client.FGetObject(context.Background(), bucket, key, localPath, minio.GetObjectOptions{})
}

func (m *MinioClient) FPutObject(bucket, key, localPath, contentType string) error {
	_, err := m.client.FPutObject(context.Background(), bucket, key, localPath,
		minio.PutObjectOptions{ContentType: contentType})
	return err
}
