package transcoder

import (
	"context"

	"go.uber.org/zap"
)

// JobProcessor is implemented by service.TranscodeService.
// Defined here so the transcoder package does not import service,
// breaking the otherwise circular dependency.
type JobProcessor interface {
	ProcessJob(ctx context.Context, job TranscodeJob) error
}

type TranscodeJob struct {
	VideoAssetID string
	RawMinioPath string
	ContentID    string
}

type WorkerPool struct {
	jobs   chan TranscodeJob
	sem    chan struct{}
	svc    JobProcessor
	logger *zap.Logger
}

func NewWorkerPool(maxWorkers int, svc JobProcessor, logger *zap.Logger) *WorkerPool {
	return &WorkerPool{
		jobs:   make(chan TranscodeJob, 100),
		sem:    make(chan struct{}, maxWorkers),
		svc:    svc,
		logger: logger,
	}
}

func (p *WorkerPool) Enqueue(job TranscodeJob) {
	p.jobs <- job
}

func (p *WorkerPool) Start(ctx context.Context) {
	go func() {
		for {
			select {
			case <-ctx.Done():
				return
			case job := <-p.jobs:
				p.sem <- struct{}{}
				go func(j TranscodeJob) {
					defer func() { <-p.sem }()
					if err := p.svc.ProcessJob(ctx, j); err != nil {
						p.logger.Error("transcode job failed",
							zap.String("assetId", j.VideoAssetID),
							zap.Error(err))
					}
				}(job)
			}
		}
	}()
}
