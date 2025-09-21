'use server';
/**
 * @fileOverview Compares a startup's metrics against industry benchmarks using AI.
 *
 * - compareStartupToBenchmark - A function that compares a startup to benchmarks.
 * - CompareStartupToBenchmarkInput - The input type for the compareStartupToBenchmark function.
 * - CompareStartupToBenchmarkOutput - The return type for the compareStartupToBenchmark function.
 */

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

const CompareStartupToBenchmarkInputSchema = z.object({
  startupDescription: z
    .string()
    .describe('A description of the startup, including its key metrics (e.g., growth rate, customer acquisition cost, burn rate).'),
  industryBenchmarks: z
    .string()
    .describe('Industry benchmarks and data on comparable companies.'),
});
export type CompareStartupToBenchmarkInput = z.infer<
  typeof CompareStartupToBenchmarkInputSchema
>;

const CompareStartupToBenchmarkOutputSchema = z.object({
  analysis: z
    .string()
    .describe(
      'An analysis comparing the startup to industry benchmarks, identifying outliers and potential issues.'
    ),
});
export type CompareStartupToBenchmarkOutput = z.infer<
  typeof CompareStartupToBenchmarkOutputSchema
>;

export async function compareStartupToBenchmark(
  input: CompareStartupToBenchmarkInput
): Promise<CompareStartupToBenchmarkOutput> {
  return compareStartupToBenchmarkFlow(input);
}

const prompt = ai.definePrompt({
  name: 'compareStartupToBenchmarkPrompt',
  input: {schema: CompareStartupToBenchmarkInputSchema},
  output: {schema: CompareStartupToBenchmarkOutputSchema},
  prompt: `You are an expert analyst specializing in comparing startups to industry benchmarks.

You will use the startup description and industry benchmarks to provide an analysis.

Startup Description: {{{startupDescription}}}
Industry Benchmarks: {{{industryBenchmarks}}}

Analyze the startup's metrics against the industry benchmarks and identify any outliers or potential issues.
`,config: {
    safetySettings: [
      {
        category: 'HARM_CATEGORY_HATE_SPEECH',
        threshold: 'BLOCK_ONLY_HIGH',
      },
      {
        category: 'HARM_CATEGORY_DANGEROUS_CONTENT',
        threshold: 'BLOCK_NONE',
      },
      {
        category: 'HARM_CATEGORY_HARASSMENT',
        threshold: 'BLOCK_MEDIUM_AND_ABOVE',
      },
      {
        category: 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
        threshold: 'BLOCK_LOW_AND_ABOVE',
      },
    ],
  },
});

const compareStartupToBenchmarkFlow = ai.defineFlow(
  {
    name: 'compareStartupToBenchmarkFlow',
    inputSchema: CompareStartupToBenchmarkInputSchema,
    outputSchema: CompareStartupToBenchmarkOutputSchema,
  },
  async input => {
    const {output} = await prompt(input);
    return output!;
  }
);
