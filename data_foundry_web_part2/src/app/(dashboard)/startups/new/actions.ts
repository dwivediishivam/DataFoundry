'use server';

import { generateStartupSummary } from '@/ai/flows/generate-startup-summary';
import { addStartup } from '@/lib/data';
import { assessStartupRisks } from '@/ai/flows/assess-startup-risks';
import { compareStartupToBenchmark } from '@/ai/flows/compare-startup-to-benchmark';
import { generateDealNote } from '@/ai/flows/generate-deal-note';

async function fileToDataURI(file: File) {
  if (!file || file.size === 0) return '';
  const buffer = Buffer.from(await file.arrayBuffer());
  return `data:${file.type};base64,${buffer.toString('base64')}`;
}

export async function analyzeStartup(formData: FormData) {
  const name = formData.get('name') as string;
  const description = formData.get('description') as string;

  const pitchDeckFile = formData.get('pitchDeck') as File | null;
  const pitchDeck = pitchDeckFile ? await fileToDataURI(pitchDeckFile) : '';

  const { summary } = await generateStartupSummary({
    pitchDeck,
    founderUpdates: '',
    publicData: '',
  });
  
  const pitchDeckSummaryForRisks = pitchDeck ? "Pitch deck is available for analysis." : "Pitch deck not provided.";
  
  const riskPromise = assessStartupRisks({
    pitchDeckSummary: pitchDeckSummaryForRisks,
    founderUpdates: '',
    marketSize: 'Early stage, not defined',
    financialMetrics: 'Early stage, not defined',
    tractionSignals: '',
  });

  const benchmarkPromise = compareStartupToBenchmark({
      startupDescription: `Name: ${name}\nDescription: ${description}\nSummary: ${summary}`,
      industryBenchmarks: 'Generic early-stage SaaS benchmarks: Focus on team, product, and initial traction signals.'
  });

  const dealNotePromise = generateDealNote({
      companyName: name,
      businessModelSummary: summary,
      tractionSummary: 'Initial pilots and positive feedback.',
      marketOpportunitySummary: 'Large enterprise automation market.',
      industryBenchmarks: 'Comparable to other seed-stage enterprise AI companies.',
      riskAssessment: 'Risks to be determined.',
      growthPotentialSummary: 'High growth potential if execution is successful.',
      customizableWeightages: 'Market: 70%, Team: 70%, Traction: 70%'
  });

  const [riskResult, benchmarkResult, dealNoteResult] = await Promise.all([riskPromise, benchmarkPromise, dealNotePromise]);


  const newStartup = {
    id: name.toLowerCase().replace(/\s+/g, '-'),
    name,
    description,
    logoUrl: `https://picsum.photos/seed/${Math.random()}/200/200`,
    imageHint: 'tech logo',
    data: {
      pitchDeck: pitchDeck ? 'Pitch deck uploaded' : 'Not provided',
      founderUpdates: '',
      publicData: '',
    },
    analysis: {
      summary,
      benchmarking: benchmarkResult.analysis,
      risk: {
        assessment: riskResult.riskAssessment,
        redFlags: riskResult.redFlags,
      },
      dealNote: dealNoteResult.dealNote,
    },
    weightages: {
      marketSize: 70,
      teamExperience: 70,
      traction: 70,
    },
  };

  await addStartup(newStartup);
}
