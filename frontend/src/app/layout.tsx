import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import "./globals.css";
import { WalletProvider } from '@/components/WalletProvider';
import { Toaster } from 'react-hot-toast';

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Nova Solana App",
  description: "Real-time Solana token feed and SOL transfer",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <WalletProvider>
          <nav className="bg-gray-900 text-white p-4">
            <div className="container mx-auto flex justify-between items-center">
              <h1 className="text-xl font-bold">Nova Solana</h1>
              <div className="space-x-4">
                <Link href="/" className="hover:text-gray-300">Cosmo</Link>
                <Link href="/transfer" className="hover:text-gray-300">Transfer</Link>
              </div>
            </div>
          </nav>
          <main className="container mx-auto p-4">
            {children}
          </main>
          <Toaster position="top-right" />
        </WalletProvider>
      </body>
    </html>
  );
}
