import Image from 'next/image';
import Link from 'next/link';

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-[#141414] flex flex-col">
      {/* Background overlay */}
      <div className="fixed inset-0 bg-gradient-to-br from-black/80 via-[#141414] to-black/60 z-0" />

      {/* Header */}
      <header className="relative z-10 px-6 py-5 sm:px-12">
        <Link href="/" className="inline-block">
          <span className="text-3xl font-extrabold text-red-600 tracking-tight">
            StreamFlix
          </span>
        </Link>
      </header>

      {/* Main content */}
      <main className="relative z-10 flex flex-1 items-center justify-center px-4 py-12">
        <div className="w-full max-w-md">
          <div className="bg-black/75 backdrop-blur-sm rounded-lg px-8 py-10 sm:px-12">
            {children}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="relative z-10 px-6 py-6 sm:px-12 border-t border-zinc-800">
        <p className="text-xs text-zinc-500">
          &copy; {new Date().getFullYear()} StreamFlix. All rights reserved.
        </p>
      </footer>
    </div>
  );
}
