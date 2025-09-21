import { Header } from '@/components/layout/header';
import { Button } from '@/components/ui/button';
import { PlusCircle } from 'lucide-react';
import Link from 'next/link';
import { getStartups } from '@/lib/data';
import { StartupCard } from '@/components/startup-card';

export default async function DashboardPage() {
  const startups = await getStartups();
  return (
    <div className="flex flex-col h-full">
      <Header
        title="Dashboard"
        description="Here is your pipeline of startups for evaluation."
        actions={
          <Link href="/startups/new">
            <Button>
              <PlusCircle className="mr-2" />
              Analyze New Startup
            </Button>
          </Link>
        }
      />
      <div className="flex-1 p-6 pt-0">
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {startups.map((startup) => (
            <StartupCard key={startup.id} startup={startup} />
          ))}
        </div>
      </div>
    </div>
  );
}
