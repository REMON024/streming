import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { QueryProvider } from '@/components/providers/QueryProvider';
import { AuthProvider } from '@/components/providers/AuthProvider';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
});

export const metadata: Metadata = {
  title: {
    default: 'StreamFlix',
    template: '%s | StreamFlix',
  },
  description: 'Watch TV shows, movies, live sports and TV channels anytime, anywhere.',
  keywords: ['streaming', 'movies', 'tv shows', 'live sports', 'tv channels'],
  themeColor: '#141414',
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: process.env.NEXTAUTH_URL,
    siteName: 'StreamFlix',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.variable} bg-[#141414] text-white antialiased`}>
        <AuthProvider>
          <QueryProvider>
            {children}
          </QueryProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
