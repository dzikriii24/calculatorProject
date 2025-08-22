'use client';

import { useEffect, useState } from 'react';

interface TokenData {
  name: string;
  symbol: string;
  uri: string;
  mint: string;
}

export default function CosmoPage() {
  const [tokens, setTokens] = useState<TokenData[]>([]);
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'disconnected'>('disconnected');

  useEffect(() => {
    let ws: WebSocket | null = null;
    let reconnectTimeout: NodeJS.Timeout;

    const connectWebSocket = () => {
      setConnectionStatus('connecting');
      ws = new WebSocket('ws://127.0.0.1:8080/connect');

      ws.onopen = () => {
        console.log('WebSocket connected');
        setConnectionStatus('connected');
      };

      ws.onmessage = (event) => {
        try {
          const tokenData: TokenData = JSON.parse(event.data);
          console.log('New token received:', tokenData);
          
          setTokens((prevTokens) => [tokenData, ...prevTokens.slice(0, 99)]); // Keep only latest 100 tokens
        } catch (error) {
          console.error('Error parsing token data:', error);
        }
      };

      ws.onclose = () => {
        console.log('WebSocket disconnected');
        setConnectionStatus('disconnected');
        
        // Attempt to reconnect after 3 seconds
        reconnectTimeout = setTimeout(() => {
          connectWebSocket();
        }, 3000);
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setConnectionStatus('disconnected');
      };
    };

    connectWebSocket();

    return () => {
      if (reconnectTimeout) {
        clearTimeout(reconnectTimeout);
      }
      if (ws) {
        ws.close();
      }
    };
  }, []);

  const getStatusColor = () => {
    switch (connectionStatus) {
      case 'connected': return 'text-green-500';
      case 'connecting': return 'text-yellow-500';
      case 'disconnected': return 'text-red-500';
      default: return 'text-gray-500';
    }
  };

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Cosmo - Live Token Feed</h1>
        <div className={`text-sm ${getStatusColor()}`}>
          Status: {connectionStatus.charAt(0).toUpperCase() + connectionStatus.slice(1)}
        </div>
      </div>

      {tokens.length === 0 ? (
        <div className="text-center text-gray-500 py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
          <p>Waiting for new tokens...</p>
          <p className="text-sm mt-2">Make sure the backend server is running on port 8080</p>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {tokens.map((token, index) => (
            <div key={`${token.mint}-${index}`} className="bg-white rounded-lg shadow-md p-6 border border-gray-200 hover:shadow-lg transition-shadow">
              <div className="flex items-start space-x-4">
                <div className="w-12 h-12 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full flex items-center justify-center text-white font-bold">
                  {token.symbol.charAt(0)}
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="text-lg font-semibold text-gray-900 truncate">{token.name}</h3>
                  <p className="text-sm text-gray-600 font-mono">{token.symbol}</p>
                  <p className="text-xs text-gray-400 mt-2 break-all">
                    Mint: {token.mint}
                  </p>
                  {token.uri && (
                    <a 
                      href={token.uri} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-xs text-blue-500 hover:text-blue-700 mt-1 inline-block"
                    >
                      View Metadata →
                    </a>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
