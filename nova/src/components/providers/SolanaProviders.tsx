'use client'

import React, { useMemo, PropsWithChildren } from 'react'
import { ConnectionProvider, WalletProvider } from '@solana/wallet-adapter-react'
import { WalletModalProvider } from '@solana/wallet-adapter-react-ui'
import { PhantomWalletAdapter } from '@solana/wallet-adapter-phantom'
import '@solana/wallet-adapter-react-ui/styles.css'
import { Toaster } from 'sonner'

const HELIUS_DEVNET_RPC = 'https://devnet.helius-rpc.com/?api-key=0f803376-0189-4d72-95f6-a5f41cef157d'

export default function SolanaProviders({ children }: PropsWithChildren) {
  const wallets = useMemo(() => [new PhantomWalletAdapter()], [])

  return (
    <ConnectionProvider endpoint={HELIUS_DEVNET_RPC}>
      <WalletProvider wallets={wallets} autoConnect>
        <WalletModalProvider>
          {children}
          <Toaster position="top-right" richColors />
        </WalletModalProvider>
      </WalletProvider>
    </ConnectionProvider>
  )
}