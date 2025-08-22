'use client'

import { FormEvent, useEffect, useMemo, useState } from 'react'
import { LAMPORTS_PER_SOL, PublicKey, SystemProgram, Transaction } from '@solana/web3.js'
import { useConnection, useWallet } from '@solana/wallet-adapter-react'
import { toast } from 'sonner'

function getErrorMessage(err: unknown): string {
  if (typeof err === 'object' && err !== null && 'message' in err) {
    const m = (err as Record<string, unknown>).message
    return typeof m === 'string' ? m : 'Failed to send transaction'
  }
  return 'Failed to send transaction'
}

export default function TransferPage() {
  const { connection } = useConnection()
  const { publicKey, connected, sendTransaction } = useWallet()

  const [amount, setAmount] = useState('')
  const [toAddress, setToAddress] = useState('')
  const [showUsd, setShowUsd] = useState(true)
  const [solUsd, setSolUsd] = useState<number | null>(null)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    const fetchPrice = async () => {
      try {
        const res = await fetch('https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd')
        const json = await res.json()
        const price = json?.solana?.usd
        if (typeof price === 'number') setSolUsd(price)
      } catch {}
    }
    fetchPrice()
  }, [])

  const parsedAmount = useMemo(() => Number(amount), [amount])
  const amountError = useMemo(() => {
    if (!amount) return 'Amount is required'
    const n = Number(amount)
    if (!isFinite(n) || n <= 0) return 'Enter a valid positive number'
    return ''
  }, [amount])

  const addressError = useMemo(() => {
    if (!toAddress) return 'Destination address is required'
    try {
      // Validate base58 public key
      new PublicKey(toAddress)
      return ''
    } catch {
      return 'Invalid Solana address'
    }
  }, [toAddress])

  const canSubmit = connected && !submitting && !amountError && !addressError

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()
    if (!publicKey) {
      toast.error('Please connect Phantom wallet')
      return
    }
    if (amountError || addressError) return

    try {
      setSubmitting(true)
      const dest = new PublicKey(toAddress)
      const lamports = Math.round(Number(parsedAmount) * LAMPORTS_PER_SOL)

      const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash('finalized')
      const tx = new Transaction({ recentBlockhash: blockhash, feePayer: publicKey })
      tx.add(
        SystemProgram.transfer({
          fromPubkey: publicKey,
          toPubkey: dest,
          lamports,
        })
      )

      const signature = await sendTransaction(tx, connection, { minContextSlot: undefined })

      toast.loading('Confirming transaction…', { id: signature })
      await connection.confirmTransaction({ signature, blockhash, lastValidBlockHeight }, 'confirmed')
      toast.success('Transaction sent', {
        id: signature,
        action: (
          <a className="underline" href={`https://explorer.solana.com/tx/${signature}?cluster=devnet`} target="_blank" rel="noreferrer">
            View on explorer
          </a>
        ),
      })
      setAmount('')
      setToAddress('')
    } catch (err: unknown) {
      toast.error(getErrorMessage(err))
    } finally {
      setSubmitting(false)
    }
  }

  const usdEstimate = useMemo(() => {
    if (!solUsd || !amount) return null
    const n = Number(amount)
    if (!isFinite(n)) return null
    return n * solUsd
  }, [solUsd, amount])

  return (
    <div className="mx-auto max-w-md p-6 w-full">
      <h1 className="text-xl font-semibold mb-4">Transfer SOL</h1>
      <form onSubmit={onSubmit} className="grid gap-4">
        <div className="grid gap-2">
          <label className="text-sm">Amount (in SOL)</label>
          <input
            type="number"
            min="0"
            step="0.000001"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            className="border rounded px-3 py-2 bg-transparent"
            placeholder="0.01"
          />
          {amountError && <div className="text-xs text-red-600">{amountError}</div>}
        </div>
        <div className="grid gap-2">
          <label className="text-sm">Wallet Address</label>
          <input
            type="text"
            value={toAddress}
            onChange={(e) => setToAddress(e.target.value.trim())}
            className="border rounded px-3 py-2 bg-transparent"
            placeholder="Destination public key"
          />
          {addressError && <div className="text-xs text-red-600">{addressError}</div>}
        </div>
        <div className="flex items-center justify-between text-sm">
          <label className="flex items-center gap-2">
            <input type="checkbox" checked={showUsd} onChange={(e) => setShowUsd(e.target.checked)} />
            Show USD estimate
          </label>
          {showUsd && usdEstimate !== null && (
            <div className="text-black/70 dark:text-white/70">≈ ${usdEstimate.toFixed(2)} USD</div>
          )}
        </div>
        <button
          type="submit"
          disabled={!canSubmit}
          className="rounded bg-black text-white dark:bg-white dark:text-black px-4 py-2 disabled:opacity-50"
        >
          {submitting ? 'Sending…' : 'Send SOL'}
        </button>
        {!connected && (
          <div className="text-xs text-black/60 dark:text-white/60">Connect your Phantom wallet using the button in the top-right.</div>
        )}
      </form>
    </div>
  )
}