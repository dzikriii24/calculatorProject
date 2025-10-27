'use client'

import { useEffect, useRef, useState } from 'react'

interface TokenInfo {
  mint?: string
  mint_address?: string
  address?: string
  name?: string
  symbol?: string
  logo?: string
  image?: string
  logoURI?: string
  metadata_uri?: string
  [key: string]: unknown
}

export default function CosmoPage() {
  const [items, setItems] = useState<TokenInfo[]>([])
  const wsRef = useRef<WebSocket | null>(null)

  const getMint = (t: TokenInfo) => (t.mint as string) || (t.mint_address as string) || (t.address as string) || ''
  const getImage = (t: TokenInfo) => (t.logo as string) || (t.image as string) || (t.logoURI as string) || ''

  useEffect(() => {
    const ws = new WebSocket('ws://127.0.0.1:8080/connect')
    wsRef.current = ws

    ws.onmessage = (ev) => {
      try {
        const data = JSON.parse(ev.data as string) as TokenInfo
        setItems((prev) => {
          const next = [data, ...prev]
          return next.slice(0, 50)
        })
      } catch {
        // ignore malformed messages
      }
    }
    ws.onerror = () => {
      // no-op for simplicity
    }
    ws.onclose = () => {
      // no-op
    }

    return () => {
      try { ws.close() } catch {}
      wsRef.current = null
    }
  }, [])

  return (
    <div className="mx-auto max-w-5xl p-6 w-full">
      <h1 className="text-xl font-semibold mb-4">Cosmo: New Token Feed</h1>
      <div className="grid gap-3">
        {items.length === 0 && (
          <div className="text-sm text-black/60 dark:text-white/60">Connecting to feed… Make sure the Go server is running.</div>
        )}
        {items.map((t, idx) => {
          const mint = getMint(t)
          const img = getImage(t)
          return (
            <div key={`${mint}-${idx}`} className="rounded-lg border border-black/10 dark:border-white/10 p-3 flex items-center gap-3">
              {img ? (
                // eslint-disable-next-line @next/next/no-img-element
                <img src={img} alt={t.symbol || t.name || 'logo'} className="h-10 w-10 rounded" />
              ) : (
                <div className="h-10 w-10 rounded bg-black/5 dark:bg-white/10" />)
              }
              <div className="flex-1 min-w-0">
                <div className="text-sm font-medium truncate">{t.name || 'Unknown'} {t.symbol ? `(${t.symbol})` : ''}</div>
                <div className="text-xs text-black/60 dark:text-white/60 truncate">{mint}</div>
                {t.metadata_uri && (
                  <a className="text-xs text-blue-600 hover:underline" href={String(t.metadata_uri)} target="_blank" rel="noreferrer">Metadata</a>
                )}
              </div>
              {mint && (
                <a
                  className="text-xs px-2 py-1 rounded border border-black/10 dark:border-white/10 hover:bg-black/5 dark:hover:bg-white/10"
                  href={`https://explorer.solana.com/address/${mint}?cluster=devnet`}
                  target="_blank"
                  rel="noreferrer"
                >
                  Explorer
                </a>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}