'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Eye, EyeOff, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import api from '@/lib/api/client';

const registerSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Please enter a valid email'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
});

type RegisterFormData = z.infer<typeof registerSchema>;

export default function RegisterPage() {
  const router = useRouter();
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  });

  const onSubmit = async (data: RegisterFormData) => {
    setError(null);
    try {
      await api.post('/api/auth/register', {
        name: data.name,
        email: data.email,
        password: data.password,
      });
      router.push('/login?registered=true');
    } catch (err: any) {
      const message = err.response?.data?.message || 'Registration failed. Please try again.';
      setError(message);
    }
  };

  return (
    <>
      <h1 className="text-3xl font-bold text-white mb-2">Create Account</h1>
      <p className="text-zinc-400 text-sm mb-8">Start watching in minutes.</p>

      {error && (
        <div className="mb-6 p-4 bg-red-900/30 border border-red-700 rounded text-red-300 text-sm">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <Input
          type="text"
          placeholder="Full name"
          autoComplete="name"
          {...register('name')}
          error={errors.name?.message}
        />

        <Input
          type="email"
          placeholder="Email address"
          autoComplete="email"
          {...register('email')}
          error={errors.email?.message}
        />

        <div className="relative">
          <Input
            type={showPassword ? 'text' : 'password'}
            placeholder="Password (min. 8 characters)"
            autoComplete="new-password"
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

        <div className="relative">
          <Input
            type={showConfirm ? 'text' : 'password'}
            placeholder="Confirm password"
            autoComplete="new-password"
            {...register('confirmPassword')}
            error={errors.confirmPassword?.message}
          />
          <button
            type="button"
            onClick={() => setShowConfirm(!showConfirm)}
            className="absolute right-3 top-3 text-zinc-400 hover:text-white transition-colors"
          >
            {showConfirm ? <EyeOff size={18} /> : <Eye size={18} />}
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
              Creating account...
            </span>
          ) : (
            'Create Account'
          )}
        </Button>
      </form>

      <p className="mt-4 text-xs text-zinc-500 text-center">
        By signing up, you agree to our{' '}
        <Link href="#" className="text-zinc-400 hover:text-white underline">Terms of Service</Link>{' '}
        and{' '}
        <Link href="#" className="text-zinc-400 hover:text-white underline">Privacy Policy</Link>.
      </p>

      <div className="mt-6 text-center text-sm text-zinc-500">
        Already have an account?{' '}
        <Link href="/login" className="text-white hover:underline font-medium">
          Sign in
        </Link>
      </div>
    </>
  );
}
