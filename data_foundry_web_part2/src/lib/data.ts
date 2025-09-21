import type { Startup } from './types';
import { revalidatePath } from 'next/cache';

let startups: Startup[] = [
  {
    id: 'innovatech-solutions',
    name: 'Innovatech Solutions',
    logoUrl: 'https://picsum.photos/seed/1/200/200',
    imageHint: 'tech logo',
    description: 'Pioneering AI-driven solutions for enterprise automation.',
    data: {
      pitchDeck:
        'Innovatech Solutions is revolutionizing enterprise workflow with our proprietary AI engine, "Prometheus." We target Fortune 500 companies struggling with legacy systems. Our projections show a 5x increase in efficiency for our clients. The team consists of PhDs from top universities with deep domain expertise in machine learning.',
      founderUpdates:
        'Q2 was a huge success. We onboarded two major clients, Acme Corp and Globex Inc., adding $500k in ARR. Our product team shipped v2.5 of the platform, which includes advanced analytics dashboards. We are currently raising a Series A to scale our sales team.',
      publicData:
        'TechCrunch article: "Innovatech Solutions quietly gains traction in the competitive AI automation space." | Glassdoor reviews show high employee satisfaction. | LinkedIn shows key hires from major tech companies.',
    },
    analysis: {
      summary:
        'Innovatech Solutions provides an AI-powered automation platform for large enterprises. Their business model is B2B SaaS. The company has demonstrated strong early traction by securing two major clients, resulting in $500k in new ARR. The market opportunity is substantial, as many large corporations are looking to modernize their legacy systems. The team has a strong technical background.',
      benchmarking:
        'Compared to peers in the enterprise AI space, Innovatech\'s current ARR of $500k is promising for a seed-stage company. Their Customer Acquisition Cost (CAC) appears to be high, a common trait for early-stage enterprise sales, but needs monitoring. The reported 5x efficiency gain is an outlier and requires validation. Their team composition, with a high density of PhDs, is stronger than many competitors.',
      risk: {
        assessment:
          'The primary risks for Innovatech are market competition and a long sales cycle. The AI automation market is crowded with both startups and established players. The reliance on a few large clients poses a concentration risk. The claimed 5x efficiency gain is a bold projection and may be difficult to achieve, potentially leading to churn if client expectations are not met.',
        redFlags: [
          'High customer concentration (2 clients make up most of the ARR).',
          'Potentially inflated market-size claims in the pitch deck.',
          'Unusually high efficiency gain projection (5x) that may not be sustainable or provable.',
        ],
      },
      dealNote:
        '**Executive Summary:** Innovatech Solutions presents a compelling investment opportunity in the enterprise AI automation market. The company has a strong technical team and has achieved initial product-market fit, as evidenced by recent high-value customer acquisitions. \n\n**Investment Highlights:** \n- Strong founding team with deep technical expertise. \n- Secured $500k in ARR from two Fortune 500 clients. \n- Large and growing market for enterprise automation. \n\n**Risks:** \n- Intense competition from established players. \n- Customer concentration risk. \n- Long enterprise sales cycles could slow growth. \n\n**Recommendation:** Recommend investment, contingent on further due diligence into the sales pipeline and validation of their technology claims. The requested valuation is in line with market standards.',
    },
    weightages: {
      marketSize: 80,
      teamExperience: 90,
      traction: 70,
    },
  },
  {
    id: 'ecowave-solutions',
    name: 'EcoWave Solutions',
    logoUrl: 'https://picsum.photos/seed/3/200/200',
    imageHint: 'nature logo',
    description: 'Sustainable packaging solutions using biodegradable materials.',
    data: {
      pitchDeck:
        'EcoWave is tackling the plastic crisis with our plant-based, fully compostable packaging materials. Our target market includes CPG companies and e-commerce businesses. We project capturing 5% of the $1T packaging market within 10 years.',
      founderUpdates:
        'We have finalized our patent for the v3 material, which is 30% cheaper to produce. We have pilot programs with 10 local businesses and are seeing positive feedback. We are raising a seed round to build our first micro-factory.',
      publicData:
        'Featured in a local news story about green startups. Won a university-level venture competition.',
    },
    analysis: {
      summary:
        'EcoWave Solutions has developed a proprietary biodegradable material for packaging to combat plastic pollution. Their business model is B2B, selling sustainable materials to CPG and e-commerce companies. They have early validation through 10 pilot programs and have secured a patent for their cost-effective material. The market for sustainable packaging is massive and growing, driven by consumer demand and regulations.',
      benchmarking:
        'EcoWave is pre-revenue, which is typical for a hard-tech company at this stage. Competitors in the space often struggle with scaling production and achieving price parity with traditional plastics. EcoWave\'s claim of a 30% cost reduction is a significant potential advantage if it can be maintained at scale. The pilot programs are a good sign of traction, but lack of larger commercial contracts is a gap compared to more mature competitors.',
      risk: {
        assessment:
          'The main risks are technical and manufacturing-related. Scaling from a lab to a micro-factory, and then to full-scale production, is capital-intensive and fraught with challenges. The 5% market share projection is highly ambitious and lacks a clear, data-backed roadmap. The company is also dependent on the successful defense of its patent.',
        redFlags: [
          'Pre-revenue with high capital expenditure required for growth.',
          'Highly optimistic market share projection without a clear strategy.',
          'Manufacturing and scaling risks are not fully addressed.',
        ],
      },
      dealNote:
        '**Executive Summary:** EcoWave Solutions is an early-stage, high-potential company addressing a critical environmental problem. Their patented technology could be a game-changer if they can successfully navigate the challenges of manufacturing at scale. \n\n**Investment Highlights:** \n- Strong mission-driven focus. \n- Patented, cost-disruptive technology. \n- Massive total addressable market (TAM). \n\n**Risks:** \n- Significant capital required to scale manufacturing. \n- Technical risk in scaling production. \n- Competition from other bioplastic companies. \n\n**Recommendation:** Pass for now, but request to be kept updated on their progress. The risk profile is too high for our fund at this pre-revenue, pre-production stage. We would reconsider after they have a functioning micro-factory and initial commercial orders.',
    },
    weightages: {
      marketSize: 90,
      teamExperience: 60,
      traction: 40,
    },
  },
];


export async function getStartups() {
    return startups;
}

export async function getStartup(id: string) {
    return startups.find(s => s.id === id);
}

export async function addStartup(startup: Startup) {
    startups.unshift(startup);
    revalidatePath('/');
}
