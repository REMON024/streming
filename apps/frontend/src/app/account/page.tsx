'use client';

import { useSession, signOut } from 'next-auth/react';
import { useQuery } from '@tanstack/react-query';
import { Navbar } from '@/components/layout/Navbar';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { useAuthStore } from '@/store/auth';
import api from '@/lib/api/client';

const TIER_LABELS = ['Free', 'Basic', 'Standard', 'Premium'];
const TIER_COLORS = ['gray', 'blue', 'green', 'gold'] as const;

export default function AccountPage() {
  const { data: session } = useSession();
  const user = useAuthStore((s) => s.user);
  const subscriptionTier = useAuthStore((s) => s.subscriptionTier);

  const { data: accountData } = useQuery({
    queryKey: ['account'],
    queryFn: async () => {
      const { data } = await api.get('/api/users/me');
      return data;
    },
    enabled: !!session,
  });

  const handleSignOut = async () => {
    await signOut({ callbackUrl: '/login' });
  };

  return (
    <div className="min-h-screen bg-[#141414]">
      <Navbar />
      <main className="pt-24 px-4 sm:px-8 lg:px-12 pb-16 max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-white mb-2">Account</h1>
        <p className="text-zinc-400 mb-10">Manage your StreamFlix account settings</p>

        {/* Membership */}
        <section className="mb-8">
          <div className="bg-zinc-900 rounded-lg p-6 sm:p-8">
            <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
              <div>
                <h2 className="text-sm font-semibold text-zinc-400 uppercase tracking-wider mb-3">
                  Membership &amp; Billing
                </h2>
                <div className="flex items-center gap-3 mb-2">
                  <span className="text-white font-medium">{user?.email || session?.user?.email}</span>
                  <Badge variant={subscriptionTier === 3 ? 'premium' : subscriptionTier === 2 ? 'basic' : 'free'}>
                    {TIER_LABELS[subscriptionTier] || 'Free'}
                  </Badge>
                </div>
                <p className="text-zinc-400 text-sm">
                  {subscriptionTier === 0
                    ? 'Upgrade to access more content'
                    : 'Your subscription is active'}
                </p>
              </div>
              <div className="flex flex-col gap-2">
                <Button variant="outline" size="sm">Manage Plan</Button>
                <Button variant="ghost" size="sm">Billing Details</Button>
              </div>
            </div>
          </div>
        </section>

        {/* Profile settings */}
        <section className="mb-8">
          <div className="bg-zinc-900 rounded-lg p-6 sm:p-8">
            <h2 className="text-sm font-semibold text-zinc-400 uppercase tracking-wider mb-4">
              Profile &amp; Parental Controls
            </h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between py-2 border-b border-zinc-800">
                <div>
                  <p className="text-white text-sm font-medium">Manage Profiles</p>
                  <p className="text-zinc-400 text-xs">Add or edit viewing profiles</p>
                </div>
                <Button variant="ghost" size="sm" onClick={() => window.location.href = '/profile/select'}>
                  Manage
                </Button>
              </div>
              <div className="flex items-center justify-between py-2 border-b border-zinc-800">
                <div>
                  <p className="text-white text-sm font-medium">Language</p>
                  <p className="text-zinc-400 text-xs">English</p>
                </div>
                <Button variant="ghost" size="sm">Change</Button>
              </div>
              <div className="flex items-center justify-between py-2">
                <div>
                  <p className="text-white text-sm font-medium">Viewing History</p>
                  <p className="text-zinc-400 text-xs">Manage what you&apos;ve watched</p>
                </div>
                <Button variant="ghost" size="sm">View</Button>
              </div>
            </div>
          </div>
        </section>

        {/* Security */}
        <section className="mb-8">
          <div className="bg-zinc-900 rounded-lg p-6 sm:p-8">
            <h2 className="text-sm font-semibold text-zinc-400 uppercase tracking-wider mb-4">
              Security
            </h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between py-2 border-b border-zinc-800">
                <div>
                  <p className="text-white text-sm font-medium">Password</p>
                  <p className="text-zinc-400 text-xs">Last changed: Unknown</p>
                </div>
                <Button variant="ghost" size="sm">Change</Button>
              </div>
              <div className="flex items-center justify-between py-2">
                <div>
                  <p className="text-white text-sm font-medium">Sign Out of All Devices</p>
                  <p className="text-zinc-400 text-xs">Sign out from all active sessions</p>
                </div>
                <Button variant="ghost" size="sm" className="text-red-400 hover:text-red-300">
                  Sign Out All
                </Button>
              </div>
            </div>
          </div>
        </section>

        {/* Sign out */}
        <div className="mt-8">
          <Button variant="outline" onClick={handleSignOut} className="text-red-400 border-red-800 hover:bg-red-900/20">
            Sign Out
          </Button>
        </div>
      </main>
    </div>
  );
}
