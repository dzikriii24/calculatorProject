'use client'

import Link from 'next/link'
import { WalletMultiButton } from '@solana/wallet-adapter-react-ui'

export default function NavBar() {
  return (
    <div className="w-full sticky top-0 z-50 border-b border-black/10 dark:border-white/10 bg-white/60 dark:bg-black/40 backdrop-blur">
      <div className="mx-auto max-w-5xl px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-4 text-sm">
          <Link href="/" className="font-semibold">Nova</Link>
          <Link href="/cosmo" className="hover:underline">Cosmo</Link>
          <Link href="/transfer" className="hover:underline">Transfer</Link>
        </div>
        <WalletMultiButton className="!rounded-full !h-9 !text-sm" />
      </div>
    </div>
  )
}