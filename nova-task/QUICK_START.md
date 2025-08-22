# 🚀 Quick Start - Nova Task

## ⚡ Get Running in 5 Minutes

### 1. Prerequisites
- Node.js 18+ installed
- Phantom wallet extension (set to Devnet)
- Go backend server running (optional for full functionality)

### 2. Start the Application
```bash
# Navigate to project directory
cd nova-task

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

### 3. Open in Browser
Navigate to: [http://localhost:3000](http://localhost:3000)

## 🎯 What You'll See

### Home Page (Cosmo)
- Real-time token feed via WebSocket
- Connection status indicator
- Live token updates (if backend is running)

### Transfer Page
- Phantom wallet connection
- SOL transfer functionality
- Real-time price conversion

## 🔧 Alternative Commands

### Using Scripts
```bash
# Start development (with checks)
./start-dev.sh

# Test application
./test-app.sh

# Build for production
./build-prod.sh
```

### Manual Commands
```bash
# Development
npm run dev

# Build
npm run build

# Production
npm run start

# Lint
npm run lint
```

## 🌐 Backend Connection

### WebSocket Status
- **Green dot**: Connected to backend
- **Red dot**: Disconnected
- **Auto-reconnect**: Every 5 seconds

### Backend Setup (Optional)
```bash
# Clone backend repository
git clone https://github.com/u289-bit/trialtask
cd trialtask

# Follow README to start server
# Should run on ws://127.0.0.1:8080/connect
```

## 🎮 Test the Features

### 1. Wallet Connection
- Click "Connect Wallet" button
- Approve in Phantom extension
- See your balance displayed

### 2. Token Feed
- Watch for real-time updates
- Check connection status
- View token details

### 3. SOL Transfer
- Enter recipient address
- Specify SOL amount
- Execute transaction
- See confirmation toast

## 🆘 Need Help?

### Quick Fixes
- **Build errors**: Run `npm run build`
- **Dependencies**: Run `npm install`
- **Port conflicts**: Change port in `package.json`

### Documentation
- `README.md` - Full project guide
- `DEMO.md` - Testing instructions
- `PROJECT_SUMMARY.md` - Feature overview

### Common Issues
- **WebSocket errors**: Backend not running
- **Wallet issues**: Phantom not on Devnet
- **Build fails**: Check Node.js version

## 🎉 You're Ready!

The application is now running and ready for:
- ✅ Development and testing
- ✅ Solana integration demo
- ✅ Wallet functionality testing
- ✅ Real-time token monitoring

---

**Next Steps**: 
1. Test wallet connection
2. Try SOL transfer (small amounts)
3. Monitor token feed
4. Explore the codebase

**Happy Coding! 🚀**