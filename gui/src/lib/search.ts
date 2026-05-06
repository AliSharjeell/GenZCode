import { DocEntry, genzDocs } from "@/data/docs";

export function searchDocs(query: string): DocEntry[] {
  const normalizedQuery = query.toLowerCase().trim();
  
  if (!normalizedQuery) {
    return genzDocs; // Return all if no query
  }

  // Calculate a relevance score for each doc
  const scoredDocs = genzDocs.map(doc => {
    let score = 0;
    const title = doc.title.toLowerCase();
    
    // 1. Exact title match (Highest)
    if (title === normalizedQuery) score += 100;
    // 2. Partial title match
    else if (title.includes(normalizedQuery)) score += 50;
    
    // 3. Exact alias match (High)
    if (doc.aliases.some(alias => alias.toLowerCase() === normalizedQuery)) {
      score += 80;
    } 
    // 4. Partial alias match
    else if (doc.aliases.some(alias => alias.toLowerCase().includes(normalizedQuery))) {
      score += 40;
    }

    // 5. Description match (Medium)
    if (doc.description.toLowerCase().includes(normalizedQuery)) {
      score += 20;
    }

    return { doc, score };
  });

  // Filter out zero scores and sort by descending score
  return scoredDocs
    .filter(item => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .map(item => item.doc);
}
