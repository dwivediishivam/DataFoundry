'use server';

/**
 * @fileOverview A flow that generates a concise summary of a startup's business model, traction, and market opportunity.
 *
 * - generateStartupSummary - A function that generates the startup summary.
 * - GenerateStartupSummaryInput - The input type for the generateStartupSummary function.
 * - GenerateStartupSummaryOutput - The return type for the generateStartupSummary function.
 */

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

const GenerateStartupSummaryInputSchema = z.object({
  pitchDeck: z.string().describe('The content of the pitch deck.'),
  founderUpdates: z.string().describe('The content of the founder updates.'),
  publicData: z.string().describe('The content of the public data.'),
});
export type GenerateStartupSummaryInput = z.infer<
  typeof GenerateStartupSummaryInputSchema
>;

const GenerateStartupSummaryOutputSchema = z.object({
  summary: z.string().describe('A concise summary of the startup.'),
});
export type GenerateStartupSummaryOutput = z.infer<
  typeof GenerateStartupSummaryOutputSchema
>;

export async function generateStartupSummary(
  input: GenerateStartupSummaryInput
): Promise<GenerateStartupSummaryOutput> {
  return generateStartupSummaryFlow(input);
}

const prompt = ai.definePrompt({
  name: 'generateStartupSummaryPrompt',
  input: {schema: GenerateStartupSummaryInputSchema},
  output: {schema: GenerateStartupSummaryOutputSchema},
  prompt: `You are an expert analyst evaluating startups. Based on the
  provided information, generate a concise summary of the startup's
  business model, traction, and market opportunity.

  Pitch Deck: {{{pitchDeck}}}
  Founder Updates: {{{founderUpdates}}}
  Public Data: {{{publicData}}}
  `,
});

const generateStartupSummaryFlow = ai.defineFlow(
  {
    name: 'generateStartupSummaryFlow',
    inputSchema: GenerateStartupSummaryInputSchema,
    outputSchema: GenerateStartupSummaryOutputSchema,
  },
  async input => {
    const {output} = await prompt(input);
    return output!;
  }
);
