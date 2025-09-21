import { notFound } from 'next/navigation';
import { getStartup } from '@/lib/data';
import { Header } from '@/components/layout/header';
import Image from 'next/image';
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@/components/ui/tabs';
import { SummaryTab } from './components/summary-tab';
import { BenchmarkingTab } from './components/benchmarking-tab';
import { RiskAssessmentTab } from './components/risk-assessment-tab';
import { DealNoteTab } from './components/deal-note-tab';
import { DataTab } from './components/data-tab';
import { Button } from '@/components/ui/button';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';

type StartupDetailPageProps = {
  params: {
    id: string;
  };
};

export default async function StartupDetailPage({ params }: StartupDetailPageProps) {
  const startup = await getStartup(params.id);

  if (!startup) {
    notFound();
  }

  return (
    <div className="flex flex-col h-full">
      <Header
        title={startup.name}
        description={startup.description}
        actions={
            <Link href="/" passHref>
                <Button variant="outline">
                <ArrowLeft className="mr-2" />
                Back to Dashboard
                </Button>
            </Link>
        }
      />
      <div className="flex-1 p-6 pt-0">
        <Tabs defaultValue="summary" className="w-full">
          <TabsList className="grid w-full grid-cols-5 mb-4">
            <TabsTrigger value="summary">Summary</TabsTrigger>
            <TabsTrigger value="benchmarking">Benchmarking</TabsTrigger>
            <TabsTrigger value="risk">Risk Assessment</TabsTrigger>
            <TabsTrigger value="deal-note">Deal Note</TabsTrigger>
            <TabsTrigger value="data">DATA FOUNDRY & Weights</TabsTrigger>
          </TabsList>
          <TabsContent value="summary">
            <SummaryTab analysis={startup.analysis} />
          </TabsContent>
          <TabsContent value="benchmarking">
            <BenchmarkingTab startup={startup} />
          </TabsContent>
          <TabsContent value="risk">
            <RiskAssessmentTab startup={startup} />
          </TabsContent>
          <TabsContent value="deal-note">
            <DealNoteTab startup={startup} />
          </TabsContent>
          <TabsContent value="data">
            <DataTab data={startup.data} weightages={startup.weightages} />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
