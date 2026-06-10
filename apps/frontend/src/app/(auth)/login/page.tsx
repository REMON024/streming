'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { signIn } from 'next-auth/react';
import { Eye, EyeOff, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { useAuthStore } from '@/store/auth';

const loginSchema = z.object({
  email: z.string().email('Please enter a valid email'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
});

type LoginFormData = z.infer<typeof loginSchema>;

export default function LoginPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const callbackUrl = searchParams.get('callbackUrl') || '/profile/select';
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const setAuth = useAuthStore((s) => s.setAuth);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormData) => {
    setError(null);
    try {
      const result = await signIn('credentials', {
        email: data.email,
        password: data.password,
        redirect: false,
      });

      if (result?.error) {
        setError('Invalid email or password. Please try again.');
        return;
      }

      router.push(callbackUrl);
    } catch (err) {
      setError('An unexpected error occurred. Please try again.');
    }
  };

  return (
    <>
      <h1 className="text-3xl font-bold text-white mb-8">Sign In</h1>

      {error && (
        <div className="mb-6 p-4 bg-red-900/30 border border-red-700 rounded text-red-300 text-sm">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <Input
            type="email"
            placeholder="Email address"
            autoComplete="email"
            {...register('email')}
            error={errors.email?.message}
          />
        </div>

        <div className="relative">
          <Input
            type={showPassword ? 'text' : 'password'}
            placeholder="Password"
            autoComplete="current-password"
            {...register('password')}
            error={errors.password?.message}
          />
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-3 top-3 text-zinc-400 hover:text-white transition-colors"
          >
            {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
          </button>
        </div>

        <Button
          type="submit"
          variant="primary"
          size="lg"
          className="w-full mt-6"
          disabled={isSubmitting}
        >
          {isSubmitting ? (
            <span className="flex items-center justify-center gap-2">
              <Loader2 size={18} className="animate-spin" />
              Signing in...
            </span>
          ) : (
            'Sign In'
          )}
        </Button>
      </form>

      <div className="mt-4 text-center">
        <Link href="#" className="text-sm text-zinc-400 hover:text-white transition-colors">
          Forgot password?
        </Link>
      </div>

      <div className="mt-6 text-center text-sm text-zinc-500">
        New to StreamFlix?{' '}
        <Link href="/register" className="text-white hover:underline font-medium">
          Sign up now
        </Link>
      </div>
    </>
  );
}
