'use client';

import { useWallet } from '@solana/wallet-adapter-react';
import { WalletMultiButton } from '@solana/wallet-adapter-react-ui';

export const WalletConnectButton = () => {
  const { publicKey } = useWallet();

  return (
    <div className="flex items-center gap-4">
      <WalletMultiButton className="!bg-blue-600 hover:!bg-blue-700 !text-white !rounded-lg !px-4 !py-2" />
      {publicKey && (
        <div className="text-sm text-gray-600">
          Connected: {publicKey.toString().slice(0, 4)}...{publicKey.toString().slice(-4)}
        </div>
      )}
    </div>
  );
};