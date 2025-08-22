# Nova Task - Solana Token Feed & Transfer Application

A Next.js application that demonstrates real-time Solana token monitoring and SOL transfer capabilities using Phantom wallet integration.

## Features

### 🚀 Cosmo Page (Live Token Feed)
- Real-time WebSocket connection to `ws://127.0.0.1:8080/connect`
- Displays new Solana tokens as they are created
- Shows token address, name, symbol, logo, and metadata
- Auto-reconnection on connection loss
- Live connection status indicator

### 💰 Transfer Page
- Connect Phantom wallet for Solana transactions
- Send SOL to any valid wallet address
- Real-time SOL price from CoinGecko API
- USD value conversion toggle
- Input validation for wallet addresses and amounts
- Transaction confirmation and success notifications
- Wallet balance display

## Tech Stack

- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **Blockchain**: Solana Web3.js, Phantom Wallet Adapter
- **Real-time**: WebSocket for token feed
- **APIs**: CoinGecko for SOL price
- **RPC**: Helius Devnet RPC endpoint
- **Notifications**: React Hot Toast

## Prerequisites

1. **Backend Server**: Ensure the Go REST API server is running at `http://127.0.0.1:8080`
   - Clone: `https://github.com/u289-bit/trialtask`
   - Run the server locally

2. **Phantom Wallet**: Install Phantom browser extension and switch to Devnet

3. **Node.js**: Version 18 or higher

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd nova-task

# Install dependencies
npm install

# Run the development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
nova-task/
├── src/
│   ├── app/
│   │   ├── page.tsx          # Cosmo page (token feed)
│   │   ├── transfer/
│   │   │   └── page.tsx      # Transfer page
│   │   ├── layout.tsx        # Root layout with wallet providers
│   │   └── globals.css       # Global styles
│   └── components/
│       ├── WalletProvider.tsx # Solana wallet context
│       ├── WalletConnectButton.tsx # Wallet connection UI
│       └── Navigation.tsx    # Main navigation
├── package.json
└── README.md
```

## Usage

### 1. Cosmo Page (Token Feed)
- Navigate to the home page
- The application automatically connects to the WebSocket
- View real-time token creation feed
- Monitor connection status

### 2. Transfer Page
- Click "Transfer" in the navigation
- Connect your Phantom wallet
- Enter recipient address and SOL amount
- Toggle USD value display if needed
- Click "Send SOL" to execute transaction

## Configuration

### RPC Endpoint
The application uses the Helius Devnet RPC endpoint as specified:
```
https://devnet.helius-rpc.com/?api-key=0f803376-0189-4d72-95f6-a5f41cef157d
```

### WebSocket Connection
Connects to the local Go server:
```
ws://127.0.0.1:8080/connect
```

## Development

### Available Scripts

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
```

### Environment Variables

No environment variables are required for basic functionality. The application uses hardcoded endpoints as specified in the requirements.

## Testing

1. **Backend Connection**: Ensure the Go server is running and accessible
2. **Wallet Connection**: Test Phantom wallet integration on Devnet
3. **WebSocket**: Verify real-time token feed functionality
4. **Transactions**: Test SOL transfers with small amounts on Devnet

## Troubleshooting

### WebSocket Connection Issues
- Verify the Go backend server is running on port 8080
- Check firewall settings
- Ensure the WebSocket endpoint is accessible

### Wallet Connection Problems
- Make sure Phantom extension is installed
- Switch to Devnet network in Phantom
- Clear browser cache and reload

### Transaction Failures
- Verify sufficient SOL balance on Devnet
- Check recipient address validity
- Ensure network connectivity to RPC endpoint

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is created for the Nova task assignment.

## Support

For issues related to:
- **Backend**: Check the Go server repository
- **Frontend**: Review this README and code comments
- **Solana**: Refer to official Solana documentation
- **Phantom**: Check Phantom wallet documentation
