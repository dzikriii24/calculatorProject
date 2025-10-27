# Deployment Guide - Nova Task Application

## Overview
This guide covers deploying the Nova Task application to various environments.

## Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Access to deployment platform (Vercel, Netlify, etc.)

## Local Development Deployment

### 1. Development Mode
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Access at: http://localhost:3000
```

### 2. Production Build (Local)
```bash
# Build for production
npm run build

# Start production server
npm run start

# Access at: http://localhost:3000
```

## Cloud Deployment

### Vercel (Recommended for Next.js)

1. **Install Vercel CLI**
```bash
npm i -g vercel
```

2. **Deploy**
```bash
# Login to Vercel
vercel login

# Deploy
vercel

# Follow the prompts
```

3. **Environment Variables** (if needed)
```bash
# Set environment variables in Vercel dashboard
NEXT_PUBLIC_RPC_ENDPOINT=https://devnet.helius-rpc.com/?api-key=0f803376-0189-4d72-95f6-a5f41cef157d
NEXT_PUBLIC_WEBSOCKET_URL=ws://127.0.0.1:8080/connect
```

### Netlify

1. **Build Command**
```bash
npm run build
```

2. **Publish Directory**
```
.next
```

3. **Environment Variables**
```bash
# Set in Netlify dashboard
NEXT_PUBLIC_RPC_ENDPOINT=https://devnet.helius-rpc.com/?api-key=0f803376-0189-4d72-95f6-a5f41cef157d
NEXT_PUBLIC_WEBSOCKET_URL=ws://127.0.0.1:8080/connect
```

### Docker Deployment

1. **Create Dockerfile**
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

2. **Build and Run**
```bash
# Build image
docker build -t nova-task .

# Run container
docker run -p 3000:3000 nova-task
```

## Environment Configuration

### Development
- Uses local WebSocket: `ws://127.0.0.1:8080/connect`
- Uses Helius Devnet RPC
- Hot reload enabled

### Production
- WebSocket URL should be configured for production backend
- RPC endpoint remains the same (or can be customized)
- Optimized build with minification

## Backend Integration

### WebSocket Connection
The frontend expects a WebSocket server at:
```
ws://127.0.0.1:8080/connect
```

For production, update the WebSocket URL in:
```typescript
// src/app/page.tsx
const ws = new WebSocket('YOUR_PRODUCTION_WEBSOCKET_URL');
```

### API Endpoints
- WebSocket: `ws://127.0.0.1:8080/connect`
- CoinGecko API: `https://api.coingecko.com/api/v3/simple/price`
- Solana RPC: `https://devnet.helius-rpc.com/?api-key=0f803376-0189-4d72-95f6-a5f41cef157d`

## Security Considerations

### Frontend
- No sensitive data exposed
- Wallet connections handled securely
- Input validation on all forms

### Backend
- Ensure WebSocket server is secure
- Implement rate limiting if needed
- Validate WebSocket messages

## Monitoring and Logging

### Frontend Logs
- Console logs for debugging
- Error boundaries for React errors
- WebSocket connection status

### Performance
- Next.js built-in performance monitoring
- Lighthouse scores
- Bundle size analysis

## Troubleshooting

### Build Issues
```bash
# Clear cache
rm -rf .next
npm run build

# Check Node.js version
node --version
```

### Runtime Issues
```bash
# Check logs
npm run dev

# Verify dependencies
npm ls
```

### Deployment Issues
- Check build logs in deployment platform
- Verify environment variables
- Check Node.js version compatibility

## Maintenance

### Regular Updates
```bash
# Update dependencies
npm update

# Check for security vulnerabilities
npm audit

# Update Next.js
npm install next@latest
```

### Backup
- Source code in version control
- Environment configurations
- Deployment scripts

## Support

For deployment issues:
1. Check this guide
2. Review platform-specific documentation
3. Check Next.js deployment docs
4. Review error logs