import { cn } from '@/lib/utils';

interface Props {
  className?: string;
  size?: 'sm' | 'md';
}

export function LiveBadge({ className, size = 'md' }: Props) {
  return (
    <span
      className={cn(
        'inline-flex items-center gap-1 bg-red-600 text-white font-bold rounded uppercase',
        size === 'sm' ? 'text-[10px] px-1.5 py-0.5' : 'text-xs px-2 py-0.5',
        className
      )}
    >
      <span className="animate-pulse w-1.5 h-1.5 bg-white rounded-full flex-shrink-0" />
      LIVE
    </span>
  );
}
