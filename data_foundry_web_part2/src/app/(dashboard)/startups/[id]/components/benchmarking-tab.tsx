'use client';
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Bot, Scale, Loader2 } from 'lucide-react';
import type { Startup } from '@/lib/types';
import { Skeleton } from '@/components/ui/skeleton';
import { compareStartupToBenchmark } from '@/ai/flows/compare-startup-to-benchmark';

export function BenchmarkingTab({
  startup,
}: {
  startup: Startup;
}) {
  const [isLoading, setIsLoading] = useState(false);
  const [benchmarkAnalysis, setBenchmarkAnalysis] = useState<string | null>(null);

  const handleGenerate = async () => {
    setIsLoading(true);
    setBenchmarkAnalysis(null);

    const result = await compareStartupToBenchmark({
        startupDescription: `Name: ${startup.name}\nDescription: ${startup.description}\nSummary: ${startup.analysis.summary}`,
        industryBenchmarks: 'Generic early-stage SaaS benchmarks: Focus on team, product, and initial traction signals.'
    });
    
    setBenchmarkAnalysis(result.analysis);
    setIsLoading(false);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Scale className="h-5 w-5" />
            <span>Benchmarking Analysis</span>
          </div>
          <Button onClick={handleGenerate} disabled={isLoading}>
            {isLoading ? (
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            ) : (
              <Bot className="mr-2 h-4 w-4" />
            )}
            {benchmarkAnalysis ? 'Regenerate' : 'Run Comparison'}
          </Button>
        </CardTitle>
      </CardHeader>
      <CardContent className="min-h-[200px] pt-0">
        {isLoading && (
          <div className="space-y-2">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-3/4" />
          </div>
        )}
        {benchmarkAnalysis && <p className="text-muted-foreground whitespace-pre-wrap">{benchmarkAnalysis}</p>}
        {!isLoading && !benchmarkAnalysis && (
           <div className="flex flex-col items-center justify-center text-center text-muted-foreground h-full min-h-[150px]">
             <p>Click "Run Comparison" to benchmark this startup against industry peers.</p>
           </div>
        )}
      </CardContent>
    </Card>
  );
}
