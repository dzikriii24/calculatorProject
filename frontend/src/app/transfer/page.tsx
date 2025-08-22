'use client';

import { useState, useEffect } from 'react';
import { useWallet, useConnection } from '@solana/wallet-adapter-react';
import { PublicKey, Transaction, SystemProgram, LAMPORTS_PER_SOL } from '@solana/web3.js';
import toast from 'react-hot-toast';

export default function TransferPage() {
  const { publicKey, sendTransaction, connected } = useWallet();
  const { connection } = useConnection();
  
  const [amount, setAmount] = useState('');
  const [recipientAddress, setRecipientAddress] = useState('');
  const [solPrice, setSolPrice] = useState<number | null>(null);
  const [showUSD, setShowUSD] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [addressError, setAddressError] = useState('');

  // Fetch SOL price from CoinGecko
  useEffect(() => {
    const fetchSolPrice = async () => {
      try {
        const response = await fetch('https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd');
        const data = await response.json();
        setSolPrice(data.solana.usd);
      } catch (error) {
        console.error('Failed to fetch SOL price:', error);
        toast.error('Failed to fetch SOL price');
      }
    };

    fetchSolPrice();
    // Refresh price every 30 seconds
    const interval = setInterval(fetchSolPrice, 30000);
    return () => clearInterval(interval);
  }, []);

  // Validate Solana address
  const validateAddress = (address: string) => {
    if (!address) {
      setAddressError('');
      return false;
    }

    try {
      new PublicKey(address);
      setAddressError('');
      return true;
    } catch {
      setAddressError('Invalid Solana address');
      return false;
    }
  };

  const handleAddressChange = (value: string) => {
    setRecipientAddress(value);
    validateAddress(value);
  };

  const handleTransfer = async () => {
    if (!connected || !publicKey) {
      toast.error('Please connect your Phantom wallet first');
      return;
    }

    if (!amount || parseFloat(amount) <= 0) {
      toast.error('Please enter a valid amount');
      return;
    }

    if (!validateAddress(recipientAddress)) {
      toast.error('Please enter a valid recipient address');
      return;
    }

    setIsLoading(true);

    try {
      const recipientPubKey = new PublicKey(recipientAddress);
      const lamports = parseFloat(amount) * LAMPORTS_PER_SOL;

      // Create transfer transaction
      const transaction = new Transaction().add(
        SystemProgram.transfer({
          fromPubkey: publicKey,
          toPubkey: recipientPubKey,
          lamports,
        })
      );

      // Send transaction
      const signature = await sendTransaction(transaction, connection);
      
      // Wait for confirmation
      await connection.confirmTransaction(signature, 'processed');
      
      toast.success(`Transaction successful! Signature: ${signature.slice(0, 8)}...`);
      
      // Clear form
      setAmount('');
      setRecipientAddress('');
      
    } catch (error) {
      console.error('Transaction failed:', error);
      toast.error('Transaction failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const usdValue = solPrice && amount ? parseFloat(amount) * solPrice : null;

  return (
    <div className="max-w-md mx-auto space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Transfer SOL</h1>
        <p className="text-gray-600">Send SOL to another wallet on Devnet</p>
      </div>

      {!connected && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 text-center">
          <p className="text-yellow-800">Please connect your Phantom wallet to continue</p>
        </div>
      )}

      <div className="bg-white rounded-lg shadow-md p-6 space-y-4">
        <div>
          <label htmlFor="amount" className="block text-sm font-medium text-gray-700 mb-2">
            Amount (SOL)
          </label>
          <input
            id="amount"
            type="number"
            step="0.001"
            min="0"
            placeholder="0.000"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            disabled={!connected}
          />
        </div>

        <div>
          <label htmlFor="recipient" className="block text-sm font-medium text-gray-700 mb-2">
            Recipient Wallet Address
          </label>
          <input
            id="recipient"
            type="text"
            placeholder="Enter Solana wallet address"
            value={recipientAddress}
            onChange={(e) => handleAddressChange(e.target.value)}
            className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent ${
              addressError ? 'border-red-300' : 'border-gray-300'
            }`}
            disabled={!connected}
          />
          {addressError && (
            <p className="mt-1 text-sm text-red-600">{addressError}</p>
          )}
        </div>

        {solPrice && amount && parseFloat(amount) > 0 && (
          <div className="bg-gray-50 rounded-lg p-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Estimated Value:</span>
              <button
                onClick={() => setShowUSD(!showUSD)}
                className="text-sm text-purple-600 hover:text-purple-700 font-medium"
              >
                {showUSD ? `$${usdValue?.toFixed(2)} USD` : `${amount} SOL`}
              </button>
            </div>
            <div className="text-xs text-gray-500 mt-1">
              SOL Price: ${solPrice.toFixed(2)} USD
            </div>
          </div>
        )}

        <button
          onClick={handleTransfer}
          disabled={!connected || !amount || !recipientAddress || !!addressError || isLoading}
          className="w-full bg-purple-600 hover:bg-purple-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-medium py-3 px-4 rounded-md transition-colors"
        >
          {isLoading ? (
            <div className="flex items-center justify-center space-x-2">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              <span>Sending...</span>
            </div>
          ) : (
            'Send SOL'
          )}
        </button>

        {connected && publicKey && (
          <div className="text-xs text-gray-500 text-center">
            From: {publicKey.toString().slice(0, 8)}...{publicKey.toString().slice(-8)}
          </div>
        )}
      </div>
    </div>
  );
}