import UserFollowComponent from '@/components/UserFollowComponent';

interface UserFollowPageProps {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ username?: string }>;
}

export default async function UserFollowPage({ params, searchParams }: UserFollowPageProps) {
  const { id } = await params;
  const { username } = await searchParams;
  const userId = parseInt(id);
  const finalUsername = username || 'Unknown User';

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <UserFollowComponent userId={userId} username={finalUsername} />
    </div>
  );
}