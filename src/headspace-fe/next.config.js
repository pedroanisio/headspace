/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  skipTrailingSlashRedirect: true,
  distDir: 'dist',
  images: {
    unoptimized: true
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://10.10.10.187:8000/api/:path*',
      },
    ]
  },
}

module.exports = nextConfig 