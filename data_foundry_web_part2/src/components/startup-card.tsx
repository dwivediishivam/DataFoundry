import Link from 'next/link';
import Image from 'next/image';
import type { Startup } from '@/lib/types';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { ArrowRight } from 'lucide-react';

type StartupCardProps = {
  startup: Startup;
};

export function StartupCard({ startup }: StartupCardProps) {
  return (
    <Link href={`/startups/${startup.id}`} className="group">
      <Card className="h-full transition-all duration-200 ease-in-out group-hover:border-primary group-hover:shadow-lg">
        <CardHeader className="flex flex-row items-center gap-4">
          <Image
            src={startup.logoUrl}
            alt={`${startup.name} logo`}
            width={64}
            height={64}
            className="rounded-lg"
            data-ai-hint={startup.imageHint}
          />
          <div className="grid">
            <CardTitle>{startup.name}</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <CardDescription className="mb-4">{startup.description}</CardDescription>
          <div className="flex justify-end">
             <div className="flex items-center text-sm font-medium text-primary opacity-0 transition-opacity duration-200 group-hover:opacity-100">
                View Analysis
               <ArrowRight className="ml-2 h-4 w-4" />
             </div>
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}
