FROM golang:1.24-alpine AS build
RUN apk add --no-cache ffmpeg git gcc musl-dev
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o streaming-server ./cmd/server

FROM alpine:3.21
RUN apk add --no-cache ffmpeg ca-certificates
COPY --from=build /app/streaming-server /usr/local/bin/streaming-server
EXPOSE 8080
ENTRYPOINT ["streaming-server"]
