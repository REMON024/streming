import { cn } from '@/lib/utils';

interface Props {
  children: React.ReactNode;
  variant?: 'free' | 'basic' | 'premium' | 'live' | 'default';
  className?: string;
}

export function Badge({ children, variant = 'default', className }: Props) {
  return (
    <span
      className={cn(
        'inline-flex items-center text-xs font-semibold px-2 py-0.5 rounded',
        variant === 'free' && 'bg-zinc-700 text-zinc-300',
        variant === 'basic' && 'bg-blue-900/50 text-blue-300 border border-blue-700',
        variant === 'premium' && 'bg-yellow-900/50 text-yellow-300 border border-yellow-700',
        variant === 'live' && 'bg-red-600 text-white',
        variant === 'default' && 'bg-zinc-800 text-zinc-300',
        className
      )}
    >
      {children}
    </span>
  );
}
