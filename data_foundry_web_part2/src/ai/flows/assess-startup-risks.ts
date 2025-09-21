// Assess Startup Risks
'use server';

/**
 * @fileOverview This file defines a Genkit flow for assessing startup risks based on provided data.
 *
 * - assessStartupRisks - An async function that takes startup data as input and returns a risk assessment.
 * - AssessStartupRisksInput - The input type for the assessStartupRisks function.
 * - AssessStartupRisksOutput - The return type for the assessStartupRisks function.
 */

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

const AssessStartupRisksInputSchema = z.object({
  pitchDeckSummary: z
    .string()
    .describe('A summary of the startup pitch deck.'),
  founderUpdates: z
    .string()
    .describe('A summary of the startup founder updates.'),
  marketSize: z
    .string()
    .describe('A description of the startup market size.'),
  financialMetrics: z
    .string()
    .describe('A summary of the startup financial metrics.'),
  tractionSignals: z
    .string()
    .describe('A summary of the startup traction signals.'),
});
export type AssessStartupRisksInput = z.infer<typeof AssessStartupRisksInputSchema>;

const AssessStartupRisksOutputSchema = z.object({
  riskAssessment: z.string().describe('A detailed risk assessment of the startup.'),
  redFlags: z.array(z.string()).describe('A list of potential red flags identified.'),
});
export type AssessStartupRisksOutput = z.infer<typeof AssessStartupRisksOutputSchema>;

export async function assessStartupRisks(input: AssessStartupRisksInput): Promise<AssessStartupRisksOutput> {
  return assessStartupRisksFlow(input);
}

const assessStartupRisksPrompt = ai.definePrompt({
  name: 'assessStartupRisksPrompt',
  input: {schema: AssessStartupRisksInputSchema},
  output: {schema: AssessStartupRisksOutputSchema},
  prompt: `You are an AI-powered risk assessment tool for evaluating startups. Analyze the provided information and identify potential risks and red flags.

  Pitch Deck Summary: {{{pitchDeckSummary}}}
  Founder Updates: {{{founderUpdates}}}
  Market Size: {{{marketSize}}}
  Financial Metrics: {{{financialMetrics}}}
  Traction Signals: {{{tractionSignals}}}

  Based on the information above, provide a detailed risk assessment and list any potential red flags.

  Format your response as follows:

  Risk Assessment: [Detailed risk assessment]
  Red Flags: [List of red flags]`,
});

const assessStartupRisksFlow = ai.defineFlow(
  {
    name: 'assessStartupRisksFlow',
    inputSchema: AssessStartupRisksInputSchema,
    outputSchema: AssessStartupRisksOutputSchema,
  },
  async input => {
    const {output} = await assessStartupRisksPrompt(input);
    return output!;
  }
);
