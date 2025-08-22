'use client';

import { useEffect, useState } from 'react';
import { Navigation } from '@/components/Navigation';

interface TokenData {
  address: string;
  name: string;
  symbol: string;
  logo?: string;
  metadata?: Record<string, unknown>;
  timestamp: string;
}

export default function CosmoPage() {
  const [tokens, setTokens] = useState<TokenData[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const connectWebSocket = () => {
      try {
        const ws = new WebSocket('ws://127.0.0.1:8080/connect');
        
        ws.onopen = () => {
          console.log('WebSocket connected');
          setIsConnected(true);
          setError(null);
        };

        ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            console.log('Received token data:', data);
            
            // Add timestamp to the token data
            const tokenWithTimestamp = {
              ...data,
              timestamp: new Date().toLocaleTimeString()
            };
            
            setTokens(prev => [tokenWithTimestamp, ...prev.slice(0, 49)]); // Keep last 50 tokens
          } catch (parseError) {
            console.error('Error parsing WebSocket message:', parseError);
          }
        };

        ws.onerror = (error) => {
          console.error('WebSocket error:', error);
          setError('WebSocket connection error');
          setIsConnected(false);
        };

        ws.onclose = () => {
          console.log('WebSocket disconnected');
          setIsConnected(false);
          // Try to reconnect after 5 seconds
          setTimeout(connectWebSocket, 5000);
        };

        return ws;
      } catch (error) {
        console.error('Error creating WebSocket:', error);
        setError('Failed to create WebSocket connection');
        setIsConnected(false);
        return null;
      }
    };

    const ws = connectWebSocket();

    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      
      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Cosmo - Live Token Feed</h1>
          <p className="text-gray-600">
            Real-time feed of new Solana tokens being created
          </p>
          
          {/* Connection Status */}
          <div className="mt-4 flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
            <span className={`text-sm ${isConnected ? 'text-green-600' : 'text-red-600'}`}>
              {isConnected ? 'Connected to WebSocket' : 'Disconnected'}
            </span>
          </div>
          
          {error && (
            <div className="mt-2 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
              {error}
            </div>
          )}
        </div>

        {/* Token Feed */}
        <div className="grid gap-4">
          {tokens.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-gray-400 text-lg">
                {isConnected ? 'Waiting for new tokens...' : 'Connecting to WebSocket...'}
              </div>
            </div>
          ) : (
            tokens.map((token, index) => (
              <div key={`${token.address}-${index}`} className="bg-white rounded-lg shadow p-6 border">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      {token.logo && (
                        <img 
                          src={token.logo} 
                          alt={token.name}
                          className="w-8 h-8 rounded-full"
                          onError={(e) => {
                            const target = e.target as HTMLImageElement;
                            target.style.display = 'none';
                          }}
                        />
                      )}
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">{token.name}</h3>
                        <p className="text-sm text-gray-500">{token.symbol}</p>
                      </div>
                    </div>
                    
                    <div className="text-sm text-gray-600 mb-2">
                      <span className="font-medium">Address:</span> {token.address}
                    </div>
                    
                    {token.metadata && (
                      <div className="text-sm text-gray-600">
                        <span className="font-medium">Metadata:</span> {JSON.stringify(token.metadata)}
                      </div>
                    )}
                  </div>
                  
                  <div className="text-right">
                    <div className="text-xs text-gray-400">{token.timestamp}</div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </main>
    </div>
  );
}
