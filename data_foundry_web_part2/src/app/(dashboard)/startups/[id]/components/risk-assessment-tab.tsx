'use client';
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Bot, ShieldAlert, Loader2, AlertCircle } from 'lucide-react';
import type { Startup } from '@/lib/types';
import { Skeleton } from '@/components/ui/skeleton';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { assessStartupRisks } from '@/ai/flows/assess-startup-risks';

export function RiskAssessmentTab({
  startup,
}: {
  startup: Startup;
}) {
  const [isLoading, setIsLoading] = useState(false);
  const [risk, setRisk] = useState<Startup['analysis']['risk'] | null>(null);

  const handleGenerate = async () => {
    setIsLoading(true);
    setRisk(null);
    
    const result = await assessStartupRisks({
        pitchDeckSummary: startup.data.pitchDeck,
        founderUpdates: startup.data.founderUpdates,
        marketSize: 'Market size not provided',
        financialMetrics: 'Financial metrics not provided',
        tractionSignals: startup.data.publicData
    });

    setRisk({
        assessment: result.riskAssessment,
        redFlags: result.redFlags
    });

    setIsLoading(false);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ShieldAlert className="h-5 w-5" />
            <span>Risk Assessment</span>
          </div>
          <Button onClick={handleGenerate} disabled={isLoading}>
            {isLoading ? (
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            ) : (
              <Bot className="mr-2 h-4 w-4" />
            )}
            {risk ? 'Regenerate' : 'Assess Risks'}
          </Button>
        </CardTitle>
      </CardHeader>
      <CardContent className="min-h-[200px] pt-0">
        {isLoading && (
          <div className="space-y-4">
            <div className="space-y-2">
              <Skeleton className="h-4 w-1/4" />
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-3/4" />
            </div>
            <div className="space-y-2">
              <Skeleton className="h-4 w-1/4" />
              <Skeleton className="h-8 w-full" />
              <Skeleton className="h-8 w-full" />
            </div>
          </div>
        )}
        {risk && (
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <h3 className="font-semibold mb-2">Assessment Details</h3>
              <p className="text-muted-foreground whitespace-pre-wrap">{risk.assessment}</p>
            </div>
            <div className="space-y-3">
              <h3 className="font-semibold">Potential Red Flags</h3>
              {risk.redFlags.map((flag, index) => (
                <Alert key={index} variant="destructive">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>{flag}</AlertDescription>
                </Alert>
              ))}
            </div>
          </div>
        )}
        {!isLoading && !risk && (
           <div className="flex flex-col items-center justify-center text-center text-muted-foreground h-full min-h-[150px]">
             <p>Click "Assess Risks" to identify potential red flags and other issues.</p>
           </div>
        )}
      </CardContent>
    </Card>
  );
}
