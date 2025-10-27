# Demo Guide - Nova Task Application

## Quick Start

### 1. Start the Backend Server
First, ensure the Go backend server is running:

```bash
# Clone the backend repository
git clone https://github.com/u289-bit/trialtask
cd trialtask

# Run the server (follow the README in that repository)
# The server should be accessible at http://127.0.0.1:8080
# And WebSocket at ws://127.0.0.1:8080/connect
```

### 2. Start the Frontend Application
In a new terminal:

```bash
cd nova-task
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Testing the Application

### Cosmo Page (Token Feed)
1. Navigate to the home page
2. You should see "Connected to WebSocket" status
3. If the backend is running and generating tokens, you'll see them appear in real-time
4. Each token shows:
   - Name and symbol
   - Wallet address
   - Logo (if available)
   - Metadata
   - Timestamp

### Transfer Page
1. Click "Transfer" in the navigation
2. Connect your Phantom wallet (make sure it's set to Devnet)
3. You'll see your wallet balance
4. Enter a recipient address (use a valid Solana address)
5. Enter an amount (small amount for testing)
6. Toggle USD value display if desired
7. Click "Send SOL" to execute the transaction

## Expected Behavior

### WebSocket Connection
- ✅ Green dot when connected
- ✅ Red dot when disconnected
- ✅ Auto-reconnection every 5 seconds
- ✅ Real-time token updates

### Wallet Integration
- ✅ Phantom wallet connection
- ✅ Balance display
- ✅ SOL to USD conversion
- ✅ Transaction signing and sending
- ✅ Success/error notifications

### Form Validation
- ✅ Address format validation
- ✅ Amount validation (positive, within balance)
- ✅ Real-time validation feedback
- ✅ Disabled button until form is valid

## Troubleshooting

### WebSocket Issues
- Check if backend server is running on port 8080
- Verify firewall settings
- Check browser console for connection errors

### Wallet Issues
- Ensure Phantom extension is installed
- Switch to Devnet network in Phantom
- Clear browser cache if needed

### Transaction Issues
- Use small amounts for testing
- Ensure sufficient SOL balance on Devnet
- Check RPC endpoint connectivity

## Sample Test Data

### Valid Solana Addresses (Devnet)
```
9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM
5U3bH5b6XtG99aVKr7Zp8y4KQxJbJtQq8KQxJbJtQq8K
```

### Test Scenarios
1. **Valid Transfer**: Send 0.001 SOL to a valid address
2. **Invalid Address**: Try sending to "invalid-address"
3. **Insufficient Balance**: Try sending more SOL than you have
4. **Zero Amount**: Try sending 0 SOL

## Success Indicators

- ✅ WebSocket shows green connection status
- ✅ Tokens appear in real-time feed
- ✅ Wallet connects successfully
- ✅ Balance displays correctly
- ✅ Transactions complete with success toast
- ✅ Form validation works as expected