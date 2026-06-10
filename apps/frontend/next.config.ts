import type { NextConfig } from 'next';

const config: NextConfig = {
  images: {
    remotePatterns: [
      { protocol: 'http', hostname: 'localhost', port: '9000' },
      { protocol: 'http', hostname: 'minio', port: '9000' },
    ],
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.BACKEND_URL || 'http://localhost:5000'}/api/:path*`,
      },
      {
        source: '/stream/:path*',
        destination: `${process.env.STREAMING_URL || 'http://localhost:8080'}/stream/:path*`,
      },
      {
        source: '/live/:path*',
        destination: `${process.env.STREAMING_URL || 'http://localhost:8080'}/live/:path*`,
      },
      {
        source: '/channel/:path*',
        destination: `${process.env.STREAMING_URL || 'http://localhost:8080'}/channel/:path*`,
      },
    ];
  },
};
export default config;
