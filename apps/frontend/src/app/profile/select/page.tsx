'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useQuery, useMutation } from '@tanstack/react-query';
import { Plus, Loader2, Pencil } from 'lucide-react';
import Image from 'next/image';
import api from '@/lib/api/client';
import { useAuthStore } from '@/store/auth';

export default function ProfileSelectPage() {
  const router = useRouter();
  const setProfile = useAuthStore((s) => s.setProfile);
  const setAuth = useAuthStore((s) => s.setAuth);
  const [selecting, setSelecting] = useState<string | null>(null);
  const [isEditing, setIsEditing] = useState(false);

  const { data: profiles = [], isLoading } = useQuery({
    queryKey: ['profiles'],
    queryFn: async () => {
      const { data } = await api.get('/api/users/me/profiles');
      return data;
    },
  });

  const selectProfile = async (profileId: string) => {
    if (selecting) return;
    setSelecting(profileId);
    try {
      const { data } = await api.post(`/api/users/me/profiles/${profileId}/select`);
      setProfile(data.profile);
      if (data.accessToken) {
        setAuth({
          user: useAuthStore.getState().user,
          accessToken: data.accessToken,
          refreshToken: useAuthStore.getState().refreshToken,
        });
      }
      router.push('/browse');
    } catch (err) {
      setSelecting(null);
    }
  };

  const AVATAR_COLORS = [
    'bg-red-600', 'bg-blue-600', 'bg-green-600', 'bg-purple-600',
    'bg-yellow-600', 'bg-pink-600', 'bg-indigo-600', 'bg-teal-600',
  ];

  return (
    <div className="min-h-screen bg-[#141414] flex flex-col items-center justify-center px-4">
      {/* Logo */}
      <div className="mb-12">
        <span className="text-4xl font-extrabold text-red-600 tracking-tight">StreamFlix</span>
      </div>

      <div className="text-center mb-12">
        <h1 className="text-3xl sm:text-4xl lg:text-5xl font-medium text-white mb-2">
          Who&apos;s watching?
        </h1>
      </div>

      {isLoading ? (
        <div className="flex gap-6">
          {Array.from({ length: 3 }).map((_, i) => (
            <div key={i} className="flex flex-col items-center gap-2">
              <div className="w-24 h-24 sm:w-32 sm:h-32 skeleton rounded" />
              <div className="h-4 w-20 skeleton rounded" />
            </div>
          ))}
        </div>
      ) : (
        <div className="flex flex-wrap justify-center gap-4 sm:gap-6 lg:gap-8 max-w-2xl">
          {profiles.map((profile: any, index: number) => (
            <button
              key={profile.id}
              onClick={() => !isEditing && selectProfile(profile.id)}
              className="group flex flex-col items-center gap-3 cursor-pointer"
              disabled={selecting === profile.id}
            >
              <div className="relative">
                <div className={`w-24 h-24 sm:w-32 sm:h-32 rounded overflow-hidden border-2 transition-all duration-200 ${
                  selecting === profile.id
                    ? 'border-white opacity-70'
                    : 'border-transparent group-hover:border-white'
                }`}>
                  {profile.avatarUrl ? (
                    <Image
                      src={profile.avatarUrl}
                      alt={profile.name}
                      fill
                      className="object-cover"
                    />
                  ) : (
                    <div className={`w-full h-full ${AVATAR_COLORS[index % AVATAR_COLORS.length]} flex items-center justify-center`}>
                      <span className="text-white text-4xl font-bold">
                        {profile.name.charAt(0).toUpperCase()}
                      </span>
                    </div>
                  )}
                </div>
                {selecting === profile.id && (
                  <div className="absolute inset-0 flex items-center justify-center">
                    <Loader2 className="text-white animate-spin" size={28} />
                  </div>
                )}
                {isEditing && (
                  <div className="absolute inset-0 bg-black/60 flex items-center justify-center rounded">
                    <Pencil className="text-white" size={24} />
                  </div>
                )}
              </div>
              <span className="text-zinc-400 group-hover:text-white transition-colors text-sm sm:text-base font-medium">
                {profile.name}
              </span>
            </button>
          ))}

          {/* Add profile button */}
          {profiles.length < 5 && (
            <button
              onClick={() => router.push('/profile/new')}
              className="group flex flex-col items-center gap-3"
            >
              <div className="w-24 h-24 sm:w-32 sm:h-32 rounded border-2 border-zinc-600 flex items-center justify-center group-hover:border-white transition-colors">
                <Plus className="text-zinc-400 group-hover:text-white transition-colors" size={40} />
              </div>
              <span className="text-zinc-400 group-hover:text-white transition-colors text-sm sm:text-base font-medium">
                Add Profile
              </span>
            </button>
          )}
        </div>
      )}

      <div className="mt-12">
        <button
          onClick={() => setIsEditing(!isEditing)}
          className="px-6 py-2 border border-zinc-400 text-zinc-400 hover:text-white hover:border-white transition-colors text-sm font-medium tracking-wider"
        >
          {isEditing ? 'Done' : 'Manage Profiles'}
        </button>
      </div>
    </div>
  );
}
