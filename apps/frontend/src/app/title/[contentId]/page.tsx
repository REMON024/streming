import { notFound } from 'next/navigation';
import { Navbar } from '@/components/layout/Navbar';
import { TitleDetail } from '@/components/title/TitleDetail';
import { getContentById } from '@/lib/api/content';
import type { ContentDetail } from '@/types/content';

interface Props {
  params: Promise<{ contentId: string }>;
}

export async function generateMetadata({ params }: Props) {
  const { contentId } = await params;
  try {
    const content = await getContentById(contentId);
    return {
      title: content.title,
      description: content.description?.slice(0, 160),
      openGraph: {
        images: content.backdropUrl ? [content.backdropUrl] : [],
      },
    };
  } catch {
    return { title: 'Title not found' };
  }
}

export default async function TitlePage({ params }: Props) {
  const { contentId } = await params;

  let content: ContentDetail;
  try {
    content = await getContentById(contentId);
  } catch {
    notFound();
  }

  return (
    <div className="min-h-screen bg-[#141414]">
      <Navbar />
      <TitleDetail content={content} />
    </div>
  );
}
