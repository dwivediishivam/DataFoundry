'use client';
import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Bot, FileText, Loader2 } from 'lucide-react';
import type { Startup } from '@/lib/types';
import { Skeleton } from '@/components/ui/skeleton';
import { generateStartupSummary } from '@/ai/flows/generate-startup-summary';

export function SummaryTab({
  analysis,
}: {
  analysis: Startup['analysis'];
}) {
  const [isLoading, setIsLoading] = useState(false);
  const [summary, setSummary] = useState<string | null>(null);

  useEffect(() => {
    if (analysis.summary) {
      setSummary(analysis.summary);
    }
  }, [analysis.summary]);


  const handleGenerate = () => {
    setIsLoading(true);
    setSummary(null);
    setTimeout(() => {
      setSummary(analysis.summary);
      setIsLoading(false);
    }, 1500);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <FileText className="h-5 w-5" />
            <span>AI-Generated Summary</span>
          </div>
          <Button onClick={handleGenerate} disabled={isLoading || !analysis.summary}>
            {isLoading ? (
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            ) : (
              <Bot className="mr-2 h-4 w-4" />
            )}
            {summary ? 'Regenerate' : 'Generate Summary'}
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
        {summary && <p className="text-muted-foreground whitespace-pre-wrap">{summary}</p>}
        {!isLoading && !summary && (
          <div className="flex flex-col items-center justify-center text-center text-muted-foreground h-full min-h-[150px]">
            <p>Click "Generate Summary" to get an AI-powered overview of the startup.</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
