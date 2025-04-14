import { createGroq } from '@ai-sdk/groq';

export const apiKey = import.meta.env.VITE_GROQ_API_KEY;
export const groq = createGroq({
  apiKey: apiKey,
});