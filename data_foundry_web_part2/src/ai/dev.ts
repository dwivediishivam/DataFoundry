import { config } from 'dotenv';
config();

import '@/ai/flows/assess-startup-risks.ts';
import '@/ai/flows/generate-deal-note.ts';
import '@/ai/flows/generate-startup-summary.ts';
import '@/ai/flows/compare-startup-to-benchmark.ts';