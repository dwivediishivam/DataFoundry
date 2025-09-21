export type Startup = {
  id: string;
  name: string;
  logoUrl: string;
  imageHint: string;
  description: string;
  data: {
    pitchDeck: string;
    founderUpdates: string;
    publicData: string;
  };
  analysis: {
    summary: string;
    benchmarking: string;
    risk: {
      assessment: string;
      redFlags: string[];
    };
    dealNote: string;
  };
  weightages: {
    marketSize: number;
    teamExperience: number;
    traction: number;
  };
};
