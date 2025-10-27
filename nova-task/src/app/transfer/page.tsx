'use client';

import { useState, useEffect } from 'react';
import { useWallet } from '@solana/wallet-adapter-react';
import { useConnection } from '@solana/wallet-adapter-react';
import { LAMPORTS_PER_SOL, PublicKey, SystemProgram, Transaction } from '@solana/web3.js';
import { Navigation } from '@/components/Navigation';
import toast from 'react-hot-toast';

export default function TransferPage() {
  const { publicKey, sendTransaction } = useWallet();
  const { connection } = useConnection();
  
  const [amount, setAmount] = useState('');
  const [walletAddress, setWalletAddress] = useState('');
  const [showUSD, setShowUSD] = useState(false);
  const [solPrice, setSolPrice] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [balance, setBalance] = useState<number | null>(null);

  // Fetch SOL price from CoinGecko
  useEffect(() => {
    const fetchSolPrice = async () => {
      try {
        const response = await fetch('https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd');
        const data = await response.json();
        setSolPrice(data.solana.usd);
      } catch (error) {
        console.error('Error fetching SOL price:', error);
        toast.error('Failed to fetch SOL price');
      }
    };

    fetchSolPrice();
    const interval = setInterval(fetchSolPrice, 60000); // Update every minute

    return () => clearInterval(interval);
  }, []);

  // Fetch wallet balance
  useEffect(() => {
    if (publicKey && connection) {
      const fetchBalance = async () => {
        try {
          const balance = await connection.getBalance(publicKey);
          setBalance(balance / LAMPORTS_PER_SOL);
        } catch (error) {
          console.error('Error fetching balance:', error);
        }
      };

      fetchBalance();
      const interval = setInterval(fetchBalance, 10000); // Update every 10 seconds

      return () => clearInterval(interval);
    }
  }, [publicKey, connection]);

  const validateWalletAddress = (address: string): boolean => {
    try {
      new PublicKey(address);
      return true;
    } catch {
      return false;
    }
  };

  const validateAmount = (amount: string): boolean => {
    const numAmount = parseFloat(amount);
    return !isNaN(numAmount) && numAmount > 0 && numAmount <= (balance || 0);
  };

  const getUSDValue = (solAmount: string): string => {
    if (!solPrice || !solAmount) return '0';
    const usdValue = parseFloat(solAmount) * solPrice;
    return usdValue.toFixed(2);
  };

  const handleTransfer = async () => {
    if (!publicKey) {
      toast.error('Please connect your wallet first');
      return;
    }

    if (!validateWalletAddress(walletAddress)) {
      toast.error('Invalid wallet address');
      return;
    }

    if (!validateAmount(amount)) {
      toast.error('Invalid amount or insufficient balance');
      return;
    }

    setIsLoading(true);

    try {
      const recipientPubkey = new PublicKey(walletAddress);
      const amountInLamports = parseFloat(amount) * LAMPORTS_PER_SOL;

      const transaction = new Transaction().add(
        SystemProgram.transfer({
          fromPubkey: publicKey,
          toPubkey: recipientPubkey,
          lamports: amountInLamports,
        })
      );

      // Get recent blockhash
      const { blockhash } = await connection.getLatestBlockhash();
      transaction.recentBlockhash = blockhash;
      transaction.feePayer = publicKey;

      // Send transaction
      const signature = await sendTransaction(transaction, connection);
      
      // Wait for confirmation
      const confirmation = await connection.confirmTransaction(signature, 'confirmed');
      
      if (confirmation.value.err) {
        throw new Error('Transaction failed');
      }

      toast.success(`Successfully sent ${amount} SOL!`);
      
      // Reset form
      setAmount('');
      setWalletAddress('');
      
      // Refresh balance
      if (publicKey) {
        const newBalance = await connection.getBalance(publicKey);
        setBalance(newBalance / LAMPORTS_PER_SOL);
      }

    } catch (error) {
      console.error('Transfer error:', error);
      toast.error('Transfer failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const isFormValid = () => {
    return (
      publicKey &&
      amount &&
      walletAddress &&
      validateWalletAddress(walletAddress) &&
      validateAmount(amount)
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      
      <main className="max-w-2xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Transfer SOL</h1>
          <p className="text-gray-600">
            Send SOL from your Phantom wallet to another wallet address
          </p>
        </div>

        {/* Wallet Balance */}
        {publicKey && balance !== null && (
          <div className="bg-white rounded-lg shadow p-6 mb-6 border">
            <h2 className="text-lg font-semibold text-gray-900 mb-2">Wallet Balance</h2>
            <div className="text-2xl font-bold text-blue-600">
              {balance.toFixed(4)} SOL
            </div>
            {solPrice && (
              <div className="text-sm text-gray-600">
                ≈ ${(balance * solPrice).toFixed(2)} USD
              </div>
            )}
          </div>
        )}

        {/* Transfer Form */}
        <div className="bg-white rounded-lg shadow p-6 border">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Transfer Details</h2>
          
          <div className="space-y-4">
            {/* Amount Input */}
            <div>
              <label htmlFor="amount" className="block text-sm font-medium text-gray-700 mb-2">
                Amount (in SOL)
              </label>
              <div className="relative">
                <input
                  type="number"
                  id="amount"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  placeholder="0.0"
                  step="0.0001"
                  min="0"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                {solPrice && amount && (
                  <div className="absolute right-3 top-2 text-sm text-gray-500">
                    ≈ ${getUSDValue(amount)}
                  </div>
                )}
              </div>
              {amount && !validateAmount(amount) && (
                <p className="mt-1 text-sm text-red-600">
                  {parseFloat(amount) > (balance || 0) ? 'Insufficient balance' : 'Amount must be greater than 0'}
                </p>
              )}
            </div>

            {/* Wallet Address Input */}
            <div>
              <label htmlFor="walletAddress" className="block text-sm font-medium text-gray-700 mb-2">
                Wallet Address
              </label>
              <input
                type="text"
                id="walletAddress"
                value={walletAddress}
                onChange={(e) => setWalletAddress(e.target.value)}
                placeholder="Enter recipient wallet address"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              {walletAddress && !validateWalletAddress(walletAddress) && (
                <p className="mt-1 text-sm text-red-600">
                  Invalid wallet address
                </p>
              )}
            </div>

            {/* USD Toggle */}
            <div className="flex items-center">
              <input
                type="checkbox"
                id="showUSD"
                checked={showUSD}
                onChange={(e) => setShowUSD(e.target.checked)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label htmlFor="showUSD" className="ml-2 block text-sm text-gray-900">
                Show USD value
              </label>
            </div>

            {/* USD Value Display */}
            {showUSD && solPrice && amount && (
              <div className="bg-gray-50 rounded-lg p-3">
                <div className="text-sm text-gray-600">Estimated USD Value:</div>
                <div className="text-lg font-semibold text-gray-900">
                  ${getUSDValue(amount)}
                </div>
              </div>
            )}

            {/* Transfer Button */}
            <button
              onClick={handleTransfer}
              disabled={!isFormValid() || isLoading}
              className={`w-full py-3 px-4 rounded-md font-medium text-white ${
                isFormValid() && !isLoading
                  ? 'bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'
                  : 'bg-gray-400 cursor-not-allowed'
              }`}
            >
              {isLoading ? 'Processing...' : 'Send SOL'}
            </button>

            {!publicKey && (
              <p className="text-center text-sm text-red-600">
                Please connect your Phantom wallet to continue
              </p>
            )}
          </div>
        </div>

        {/* Instructions */}
        <div className="mt-6 bg-blue-50 rounded-lg p-4">
          <h3 className="text-sm font-medium text-blue-900 mb-2">Instructions:</h3>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• Connect your Phantom wallet using the button in the top right</li>
            <li>• Enter the amount of SOL you want to send</li>
            <li>• Enter the recipient&apos;s wallet address</li>
            <li>• Click &quot;Send SOL&quot; to complete the transaction</li>
            <li>• This uses Solana Devnet for testing purposes</li>
          </ul>
        </div>
      </main>
    </div>
  );
}