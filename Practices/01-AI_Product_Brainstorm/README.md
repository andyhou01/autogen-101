# ✅ Practice 1: 🧠 AI Product Brainstorming Board

## 📘 Scenario:

You are building an AI brainstorming system for a venture builder. The user provides a vague domain (e.g., “healthcare” or “finance”), and a team of agents work together to:

- Generate multiple product ideas
- Evaluate feasibility (tech & data)
- Score business potential
- Suggest a next action plan

## 📌 Your tasks:

1. **Customize each agent's system message**
   Define clear behavioral constraints:

   - `CreativeAgent`: Must output **3 product ideas**, each with 1-line description.
   - `FeasibilityExpert`: Must score each idea for feasibility (0–10) and explain.
   - `BusinessAnalyst`: Must provide a SWOT-style breakdown and suggest “Go / Pivot / Drop” per idea.

2. **Implement message filtering**
   Add logic so only structured replies are accepted (no hallucinated narratives).

3. **Aggregate outputs**
   Combine all agents' responses into a single **ranked recommendation table** at the end.

4. **Bonus challenge**:
   Add a `ResearchAgent` who uses tool calls (if available) to look up market data (e.g., search trends, TAM) to validate one idea.
