'use client';

import { useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { ArrowLeft, Loader2 } from 'lucide-react';
import Link from 'next/link';
import { Navbar } from '@/components/layout/Navbar';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import api from '@/lib/api/client';

const profileSchema = z.object({
  name: z.string().min(1, 'Name is required').max(50, 'Name too long'),
  maturityRating: z.enum(['all', 'teen', 'adult']),
  language: z.string(),
});

type ProfileFormData = z.infer<typeof profileSchema>;

export default function ProfileSettingsPage() {
  const router = useRouter();
  const params = useParams();
  const profileId = params.profileId as string;
  const queryClient = useQueryClient();

  const { data: profile, isLoading } = useQuery({
    queryKey: ['profile', profileId],
    queryFn: async () => {
      const { data } = await api.get(`/api/users/me/profiles/${profileId}`);
      return data;
    },
  });

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
    values: profile
      ? { name: profile.name, maturityRating: profile.maturityRating || 'adult', language: profile.language || 'en' }
      : undefined,
  });

  const updateMutation = useMutation({
    mutationFn: async (data: ProfileFormData) => {
      const response = await api.put(`/api/users/me/profiles/${profileId}`, data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['profiles'] });
      router.push('/profile/select');
    },
  });

  const deleteMutation = useMutation({
    mutationFn: async () => {
      await api.delete(`/api/users/me/profiles/${profileId}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['profiles'] });
      router.push('/profile/select');
    },
  });

  if (isLoading) {
    return (
      <div className="min-h-screen bg-[#141414]">
        <Navbar />
        <div className="pt-24 flex justify-center">
          <Loader2 className="animate-spin text-red-600" size={40} />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#141414]">
      <Navbar />
      <main className="pt-24 px-4 pb-16 max-w-2xl mx-auto">
        <Link
          href="/profile/select"
          className="flex items-center gap-2 text-zinc-400 hover:text-white transition-colors mb-8"
        >
          <ArrowLeft size={18} />
          Back to Profiles
        </Link>

        <h1 className="text-3xl font-bold text-white mb-8">Edit Profile</h1>

        <form onSubmit={handleSubmit((data) => updateMutation.mutate(data))} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-zinc-300 mb-2">Profile Name</label>
            <Input {...register('name')} error={errors.name?.message} />
          </div>

          <div>
            <label className="block text-sm font-medium text-zinc-300 mb-2">Maturity Rating</label>
            <select
              {...register('maturityRating')}
              className="w-full bg-zinc-800 text-white border border-zinc-600 rounded px-3 py-2.5 text-sm focus:outline-none focus:border-zinc-400"
            >
              <option value="all">All Ages</option>
              <option value="teen">Teen (13+)</option>
              <option value="adult">Adult (18+)</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-zinc-300 mb-2">Language</label>
            <select
              {...register('language')}
              className="w-full bg-zinc-800 text-white border border-zinc-600 rounded px-3 py-2.5 text-sm focus:outline-none focus:border-zinc-400"
            >
              <option value="en">English</option>
              <option value="es">Spanish</option>
              <option value="fr">French</option>
              <option value="de">German</option>
              <option value="pt">Portuguese</option>
              <option value="ja">Japanese</option>
            </select>
          </div>

          <div className="flex flex-col sm:flex-row gap-3 pt-4">
            <Button type="submit" variant="primary" disabled={isSubmitting || updateMutation.isPending}>
              {updateMutation.isPending ? (
                <span className="flex items-center gap-2">
                  <Loader2 size={16} className="animate-spin" />
                  Saving...
                </span>
              ) : 'Save Changes'}
            </Button>

            <Button
              type="button"
              variant="outline"
              onClick={() => router.push(`/profile/${profileId}/watchlist`)}
            >
              View Watchlist
            </Button>

            <Button
              type="button"
              variant="ghost"
              className="text-red-400 hover:text-red-300"
              onClick={() => {
                if (confirm('Delete this profile? This cannot be undone.')) {
                  deleteMutation.mutate();
                }
              }}
              disabled={deleteMutation.isPending}
            >
              Delete Profile
            </Button>
          </div>
        </form>
      </main>
    </div>
  );
}
