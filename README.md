# Nova Solana App

A real-time Solana token feed and SOL transfer application built with NextJS, TypeScript, and Golang backend.

## Features

- **Cosmo Page**: Real-time feed of new Solana tokens created on PumpFun
- **Transfer Page**: Send SOL from Phantom wallet to other addresses
- **Phantom Wallet Integration**: Connect and sign transactions
- **USD Price Conversion**: Real-time SOL to USD conversion using CoinGecko API
- **Address Validation**: Validates Solana wallet addresses
- **WebSocket Connection**: Real-time data streaming from backend

## Architecture

### Backend (Golang)
- WebSocket server listening on `ws://127.0.0.1:8080/connect`
- Connects to Solana mainnet to monitor PumpFun program for new token creations
- Streams token data (name, symbol, mint address, metadata URI) to connected clients

### Frontend (NextJS + TypeScript)
- **Cosmo Page** (`/`): Displays live feed of new tokens
- **Transfer Page** (`/transfer`): SOL transfer interface
- Phantom wallet integration for signing transactions
- Real-time WebSocket connection to backend
- Responsive design with Tailwind CSS

## Setup Instructions

### Prerequisites
- Node.js (v18 or higher)
- Go (v1.21 or higher)
- Phantom Wallet browser extension

### Backend Setup
```bash
cd backend
go mod download
go run main.go
```
The server will start on `http://127.0.0.1:8080`

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
The frontend will be available at `http://localhost:3000`

## Usage

### 1. Cosmo Page (Token Feed)
- Visit `http://localhost:3000`
- The page will automatically connect to the WebSocket and display new tokens
- Each token shows: name, symbol, mint address, and metadata link
- Connection status indicator shows WebSocket connection state

### 2. Transfer Page (SOL Transfer)
- Visit `http://localhost:3000/transfer`
- Connect your Phantom wallet (make sure it's set to Devnet)
- Enter amount in SOL and recipient wallet address
- View estimated USD value (click to toggle between SOL/USD)
- Click "Send SOL" to execute the transaction
- Transaction confirmation will be shown via toast notification

## Technical Implementation

### WebSocket Data Structure
```typescript
interface TokenData {
  name: string;    // Token name
  symbol: string;  // Token symbol
  uri: string;     // Metadata URI
  mint: string;    // Token mint address
}
```

### Key Dependencies
- `@solana/web3.js`: Solana blockchain interaction
- `@solana/wallet-adapter-*`: Phantom wallet integration
- `react-hot-toast`: Toast notifications
- `tailwindcss`: Styling

### Network Configuration
- **Solana Network**: Devnet (for testing)
- **RPC Endpoint**: Helius Devnet RPC
- **Backend WebSocket**: `ws://127.0.0.1:8080/connect`

## Development Notes

- The backend monitors Solana mainnet for real token creations
- Frontend uses Devnet for safe testing of SOL transfers
- WebSocket automatically reconnects if connection is lost
- Address validation prevents invalid transaction attempts
- SOL price updates every 30 seconds from CoinGecko API

## Security Considerations

- All SOL transfers are executed on Devnet for safety
- Wallet private keys never leave the user's browser
- Address validation prevents sending to invalid addresses
- Transaction confirmation required before completion