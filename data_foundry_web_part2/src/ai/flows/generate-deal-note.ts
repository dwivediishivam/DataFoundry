'use server';

/**
 * @fileOverview Generates a structured deal note summarizing a startup's key attributes,
 * benchmarks, risk assessment, and investment recommendation.
 *
 * - generateDealNote - A function that generates the deal note.
 * - GenerateDealNoteInput - The input type for the generateDealNote function.
 * - GenerateDealNoteOutput - The return type for the generateDealNote function.
 */

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

const GenerateDealNoteInputSchema = z.object({
  companyName: z.string().describe('The name of the startup company.'),
  businessModelSummary: z.string().describe('A summary of the startup business model.'),
  tractionSummary: z.string().describe('A summary of the startup traction.'),
  marketOpportunitySummary: z.string().describe('A summary of the startup market opportunity.'),
  industryBenchmarks: z.string().describe('The industry benchmarks for similar companies.'),
  riskAssessment: z.string().describe('The risk assessment for the startup.'),
  growthPotentialSummary: z.string().describe('An executive summary of growth potential.'),
  customizableWeightages: z.string().describe('Customizable weightages given to different factors.'),
});
export type GenerateDealNoteInput = z.infer<typeof GenerateDealNoteInputSchema>;

const GenerateDealNoteOutputSchema = z.object({
  dealNote: z.string().describe('A structured deal note summarizing the startup.'),
});
export type GenerateDealNoteOutput = z.infer<typeof GenerateDealNoteOutputSchema>;

export async function generateDealNote(input: GenerateDealNoteInput): Promise<GenerateDealNoteOutput> {
  return generateDealNoteFlow(input);
}

const prompt = ai.definePrompt({
  name: 'generateDealNotePrompt',
  input: {schema: GenerateDealNoteInputSchema},
  output: {schema: GenerateDealNoteOutputSchema},
  prompt: `You are an experienced venture capital analyst. You will generate a deal note for a startup based on the following information:

  Company Name: {{{companyName}}}
  Business Model Summary: {{{businessModelSummary}}}
  Traction Summary: {{{tractionSummary}}}
  Market Opportunity Summary: {{{marketOpportunitySummary}}}
  Industry Benchmarks: {{{industryBenchmarks}}}
  Risk Assessment: {{{riskAssessment}}}
  Growth Potential Summary: {{{growthPotentialSummary}}}
  Customizable Weightages: {{{customizableWeightages}}}

  Generate a structured deal note that includes the following sections:

  1.  Executive Summary
  2.  Company Description
  3.  Investment Highlights
  4.  Risks
  5.  Recommendation
  6.  Appendix
  `,
});

const generateDealNoteFlow = ai.defineFlow(
  {
    name: 'generateDealNoteFlow',
    inputSchema: GenerateDealNoteInputSchema,
    outputSchema: GenerateDealNoteOutputSchema,
  },
  async input => {
    const {output} = await prompt(input);
    return output!;
  }
);
