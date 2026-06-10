'use client';

import { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { useRouter, usePathname } from 'next/navigation';
import { signOut, useSession } from 'next-auth/react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Search, Bell, ChevronDown, Menu, X, User,
  LogOut, Settings, List, Radio, Tv, Trophy
} from 'lucide-react';
import Image from 'next/image';
import { useAuthStore } from '@/store/auth';
import { SearchBar } from '@/components/search/SearchBar';
import { cn } from '@/lib/utils';

const NAV_LINKS = [
  { href: '/browse', label: 'Home' },
  { href: '/browse/series', label: 'TV Shows' },
  { href: '/browse/movies', label: 'Movies' },
  { href: '/browse/new', label: 'New & Popular' },
  { href: '/sports', label: 'Sports' },
  { href: '/live', label: 'Live' },
];

export function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [showSearch, setShowSearch] = useState(false);
  const [showMobileMenu, setShowMobileMenu] = useState(false);
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const pathname = usePathname();
  const router = useRouter();
  const { data: session } = useSession();
  const profile = useAuthStore((s) => s.profile);
  const profileMenuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (profileMenuRef.current && !profileMenuRef.current.contains(e.target as Node)) {
        setShowProfileMenu(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Close mobile menu on route change
  useEffect(() => {
    setShowMobileMenu(false);
    setShowSearch(false);
  }, [pathname]);

  return (
    <nav
      className={cn(
        'fixed top-0 left-0 right-0 z-50 transition-all duration-300',
        isScrolled || showMobileMenu
          ? 'bg-[#141414]'
          : 'bg-gradient-to-b from-black/80 to-transparent'
      )}
    >
      <div className="flex items-center justify-between px-4 sm:px-8 lg:px-12 h-16">
        {/* Left: Logo + nav links */}
        <div className="flex items-center gap-6 lg:gap-8">
          {/* Logo */}
          <Link href="/browse" className="flex-shrink-0">
            <span className="text-2xl font-extrabold text-red-600 tracking-tight">StreamFlix</span>
          </Link>

          {/* Desktop nav links */}
          <div className="hidden lg:flex items-center gap-5">
            {NAV_LINKS.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={cn(
                  'text-sm transition-colors hover:text-white',
                  pathname.startsWith(link.href) && link.href !== '/browse'
                    ? 'text-white font-medium'
                    : pathname === '/browse' && link.href === '/browse'
                    ? 'text-white font-medium'
                    : 'text-zinc-300'
                )}
              >
                {link.label}
              </Link>
            ))}
          </div>

          {/* Mobile: browse dropdown */}
          <div className="hidden sm:flex lg:hidden items-center">
            <button
              onClick={() => setShowMobileMenu(!showMobileMenu)}
              className="flex items-center gap-1 text-sm text-white"
            >
              Browse <ChevronDown size={14} className={cn('transition-transform', showMobileMenu && 'rotate-180')} />
            </button>
          </div>
        </div>

        {/* Right: search, bell, profile */}
        <div className="flex items-center gap-3 sm:gap-4">
          {/* Search */}
          <AnimatePresence>
            {showSearch ? (
              <motion.div
                initial={{ width: 0, opacity: 0 }}
                animate={{ width: '200px', opacity: 1 }}
                exit={{ width: 0, opacity: 0 }}
                className="hidden sm:block overflow-hidden"
              >
                <SearchBar
                  autoFocus
                  onClose={() => setShowSearch(false)}
                  compact
                />
              </motion.div>
            ) : null}
          </AnimatePresence>

          <button
            onClick={() => {
              if (showSearch) {
                setShowSearch(false);
              } else {
                setShowSearch(true);
              }
            }}
            className="text-zinc-300 hover:text-white transition-colors p-1"
            aria-label="Search"
          >
            <Search size={20} />
          </button>

          {/* Notifications */}
          <button className="text-zinc-300 hover:text-white transition-colors p-1 relative hidden sm:block">
            <Bell size={20} />
            <span className="absolute top-0.5 right-0.5 w-2 h-2 bg-red-600 rounded-full" />
          </button>

          {/* Profile menu */}
          <div className="relative" ref={profileMenuRef}>
            <button
              onClick={() => setShowProfileMenu(!showProfileMenu)}
              className="flex items-center gap-1.5 text-zinc-300 hover:text-white transition-colors"
            >
              <div className="w-8 h-8 rounded bg-red-700 flex items-center justify-center text-white text-sm font-bold overflow-hidden">
                {profile?.avatarUrl ? (
                  <Image src={profile.avatarUrl} alt={profile.name} width={32} height={32} className="object-cover" />
                ) : (
                  <span>{(profile?.name || session?.user?.name || 'U').charAt(0).toUpperCase()}</span>
                )}
              </div>
              <ChevronDown
                size={14}
                className={cn('transition-transform hidden sm:block', showProfileMenu && 'rotate-180')}
              />
            </button>

            <AnimatePresence>
              {showProfileMenu && (
                <motion.div
                  initial={{ opacity: 0, y: -8 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -8 }}
                  className="absolute right-0 top-full mt-2 w-56 bg-zinc-900 border border-zinc-700 rounded-lg shadow-2xl overflow-hidden"
                >
                  {/* Profile name */}
                  <div className="px-4 py-3 border-b border-zinc-700">
                    <p className="text-xs text-zinc-400">Signed in as</p>
                    <p className="text-sm font-medium text-white truncate">
                      {session?.user?.email}
                    </p>
                  </div>

                  <div className="py-1">
                    <Link
                      href="/profile/select"
                      className="flex items-center gap-3 px-4 py-2.5 text-sm text-zinc-300 hover:text-white hover:bg-zinc-800 transition-colors"
                    >
                      <User size={16} />
                      Switch Profile
                    </Link>
                    <Link
                      href="/account"
                      className="flex items-center gap-3 px-4 py-2.5 text-sm text-zinc-300 hover:text-white hover:bg-zinc-800 transition-colors"
                    >
                      <Settings size={16} />
                      Account Settings
                    </Link>
                    <Link
                      href="/profile/select"
                      className="flex items-center gap-3 px-4 py-2.5 text-sm text-zinc-300 hover:text-white hover:bg-zinc-800 transition-colors"
                    >
                      <List size={16} />
                      My List
                    </Link>
                  </div>

                  <div className="border-t border-zinc-700 py-1">
                    <button
                      onClick={() => signOut({ callbackUrl: '/login' })}
                      className="flex items-center gap-3 px-4 py-2.5 text-sm text-zinc-300 hover:text-white hover:bg-zinc-800 transition-colors w-full text-left"
                    >
                      <LogOut size={16} />
                      Sign Out
                    </button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Mobile hamburger */}
          <button
            onClick={() => setShowMobileMenu(!showMobileMenu)}
            className="lg:hidden text-zinc-300 hover:text-white transition-colors p-1"
            aria-label="Menu"
          >
            {showMobileMenu ? <X size={22} /> : <Menu size={22} />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      <AnimatePresence>
        {showMobileMenu && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="lg:hidden overflow-hidden bg-[#141414] border-t border-zinc-800"
          >
            <div className="px-4 py-4 space-y-1">
              {NAV_LINKS.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className={cn(
                    'block px-3 py-2.5 rounded text-sm transition-colors',
                    pathname.startsWith(link.href)
                      ? 'bg-zinc-800 text-white font-medium'
                      : 'text-zinc-300 hover:text-white hover:bg-zinc-800'
                  )}
                >
                  {link.label}
                </Link>
              ))}
              {/* Mobile search */}
              <div className="pt-2">
                <SearchBar compact />
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
}
