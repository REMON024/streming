'use client';

import * as Dialog from '@radix-ui/react-dialog';
import { X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '@/lib/utils';

interface Props {
  open: boolean;
  onClose: () => void;
  children: React.ReactNode;
  title?: string;
  description?: string;
  className?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
}

const SIZE_CLASSES = {
  sm: 'max-w-sm',
  md: 'max-w-md',
  lg: 'max-w-lg',
  xl: 'max-w-2xl',
  full: 'max-w-4xl',
};

export function Modal({
  open,
  onClose,
  children,
  title,
  description,
  className,
  size = 'md',
}: Props) {
  return (
    <Dialog.Root open={open} onOpenChange={(o) => !o && onClose()}>
      <AnimatePresence>
        {open && (
          <Dialog.Portal forceMount>
            {/* Overlay */}
            <Dialog.Overlay asChild>
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50"
              />
            </Dialog.Overlay>

            {/* Content */}
            <Dialog.Content asChild>
              <motion.div
                initial={{ opacity: 0, scale: 0.95, y: 10 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.95, y: 10 }}
                transition={{ duration: 0.2 }}
                className={cn(
                  'fixed z-50 left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2',
                  'w-full mx-4 bg-zinc-900 rounded-lg shadow-2xl border border-zinc-700',
                  'max-h-[90vh] overflow-y-auto',
                  SIZE_CLASSES[size],
                  className
                )}
              >
                {/* Header */}
                {(title || description) && (
                  <div className="p-6 border-b border-zinc-700">
                    {title && (
                      <Dialog.Title className="text-lg font-semibold text-white">
                        {title}
                      </Dialog.Title>
                    )}
                    {description && (
                      <Dialog.Description className="text-sm text-zinc-400 mt-1">
                        {description}
                      </Dialog.Description>
                    )}
                  </div>
                )}

                {/* Close button */}
                <Dialog.Close asChild>
                  <button
                    className="absolute top-4 right-4 text-zinc-400 hover:text-white transition-colors"
                    aria-label="Close"
                  >
                    <X size={20} />
                  </button>
                </Dialog.Close>

                {/* Content */}
                <div className="p-6">{children}</div>
              </motion.div>
            </Dialog.Content>
          </Dialog.Portal>
        )}
      </AnimatePresence>
    </Dialog.Root>
  );
}
