export default function Home() {
  return (
    <div className="mx-auto max-w-5xl p-6 w-full">
      <h1 className="text-xl font-semibold mb-4">Welcome</h1>
      <p className="text-sm text-black/70 dark:text-white/70 mb-4">Use the navigation above to open Cosmo (live token feed) or Transfer (send SOL).</p>
      <div className="text-sm">
        <ul className="list-disc pl-4">
          <li>Cosmo: Live stream of newly minted tokens via WebSocket</li>
          <li>Transfer: Send SOL on Devnet using Phantom</li>
        </ul>
      </div>
    </div>
  )
}
