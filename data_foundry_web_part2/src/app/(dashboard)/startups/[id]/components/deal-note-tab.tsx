'use client';
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Bot, PenSquare, Loader2 } from 'lucide-react';
import type { Startup } from '@/lib/types';
import { Skeleton } from '@/components/ui/skeleton';
import { generateDealNote } from '@/ai/flows/generate-deal-note';

export function DealNoteTab({
  startup,
}: {
  startup: Startup;
}) {
  const [isLoading, setIsLoading] = useState(false);
  const [dealNote, setDealNote] = useState<string | null>(null);

  const handleGenerate = async () => {
    setIsLoading(true);
    setDealNote(null);
    
    const result = await generateDealNote({
        companyName: startup.name,
        businessModelSummary: startup.analysis.summary,
        tractionSummary: 'Traction data not available.',
        marketOpportunitySummary: 'Market opportunity not fully analyzed.',
        industryBenchmarks: startup.analysis.benchmarking,
        riskAssessment: startup.analysis.risk.assessment,
        growthPotentialSummary: 'Growth potential not yet generated.',
        customizableWeightages: `Market: ${startup.weightages.marketSize}%, Team: ${startup.weightages.teamExperience}%, Traction: ${startup.weightages.traction}%`,
    });
    
    setDealNote(result.dealNote);
    setIsLoading(false);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <PenSquare className="h-5 w-5" />
            <span>Deal Note</span>
          </div>
          <Button onClick={handleGenerate} disabled={isLoading}>
            {isLoading ? (
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            ) : (
              <Bot className="mr-2 h-4 w-4" />
            )}
            {dealNote ? 'Regenerate' : 'Generate Deal Note'}
          </Button>
        </CardTitle>
      </CardHeader>
      <CardContent className="min-h-[200px] pt-0">
        {isLoading && (
          <div className="space-y-2">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-3/4" />
            <Skeleton className="h-4 w-full mt-4" />
            <Skeleton className="h-4 w-5/6" />
          </div>
        )}
        {dealNote && <p className="text-muted-foreground whitespace-pre-wrap">{dealNote}</p>}
        {!isLoading && !dealNote && (
          <div className="flex flex-col items-center justify-center text-center text-muted-foreground h-full min-h-[150px]">
            <p>Click "Generate Deal Note" to create a structured investment memo.</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
