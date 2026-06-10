import { forwardRef } from 'react';
import { cn } from '@/lib/utils';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'outline';
  size?: 'sm' | 'md' | 'lg';
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', children, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          'inline-flex items-center justify-center font-semibold rounded transition-all duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-zinc-900 disabled:opacity-50 disabled:cursor-not-allowed',
          // Variants
          variant === 'primary' && [
            'bg-red-600 text-white hover:bg-red-700 focus-visible:ring-red-500',
          ],
          variant === 'secondary' && [
            'bg-zinc-700/80 text-white hover:bg-zinc-600 focus-visible:ring-zinc-500',
          ],
          variant === 'ghost' && [
            'text-zinc-300 hover:text-white hover:bg-zinc-800 focus-visible:ring-zinc-500',
          ],
          variant === 'outline' && [
            'border border-zinc-500 text-zinc-200 hover:text-white hover:border-white bg-transparent focus-visible:ring-zinc-400',
          ],
          // Sizes
          size === 'sm' && 'text-xs px-3 py-1.5 gap-1',
          size === 'md' && 'text-sm px-4 py-2 gap-1.5',
          size === 'lg' && 'text-base px-6 py-3 gap-2',
          className
        )}
        {...props}
      >
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';
