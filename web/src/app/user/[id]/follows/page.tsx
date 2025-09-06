import UserFollowComponent from '@/components/UserFollowComponent';

interface UserFollowPageProps {
  params: { id: string };
  searchParams: { username?: string };
}

export default function UserFollowPage({ params, searchParams }: UserFollowPageProps) {
  const userId = parseInt(params.id);
  const username = searchParams.username || 'Unknown User';

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <UserFollowComponent userId={userId} username={username} />
    </div>
  );
}