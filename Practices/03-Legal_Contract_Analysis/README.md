# ✅ Practice 3: 📄 Legal Contract Analysis System

## 📘 Scenario:

You are building a multi-agent system for a legal-tech SaaS platform. When a user uploads a draft contract (e.g., vendor agreement), the system should:

1. Extract key clauses and structure
2. Identify risks (e.g., vague terms, missing protections, liabilities)
3. Suggest concrete revision text for risky or missing clauses

This mimics what legal analysts and contract managers do manually — and your AI team will automate it through agent collaboration.

## 📌 Your tasks:

### 1. **Agent Role Design – Fill in the system messages**

- 🔍 `ClauseExtractor`:
  Extract and label major clauses (duration, termination, liability, data handling, etc.)
  → Output format: JSON-like structure

- ⚠️ `RiskAssessor`:
  Analyze extracted clauses and flag:

  - vague terms (e.g., “reasonable efforts”)
  - missing standard protections (e.g., GDPR, SLA)
  - one-sided terms (e.g., unilateral termination)

- 🛠️ `RevisionSuggester`:
  For each flagged issue, propose clear revision text using **legal best practices**
  (e.g., “The Vendor shall comply with GDPR Articles 5–32.”)

### 2. **Force clause structure**

Use examples or validations to ensure `ClauseExtractor` uses this output format:

```json
{
  "duration": "...",
  "termination": "...",
  "liability": "...",
  "data_protection": "...",
  ...
}
```

### 3. **Output Final Recommendation Report**

Implement a final step where one of the agents (or a new one like `LegalAdvisorAgent`) returns a report like:

```
🧾 Summary Report:

- 5 Clauses extracted
- 3 Issues found
- 3 Revision suggestions provided

Action Required: Add data protection clause. Clarify SLA terms. Consider mutual termination clause.
```

### 4. **Bonus Challenge – Chain of Reasoning**

Let `RiskAssessor` **justify** each risk with reasoning based on regulatory requirements or industry standards.

### 5. **Optional Tool Use**

If tools are enabled (e.g., Bing Search, internal vector search), allow `RiskAssessor` to **cite GDPR articles** or sample contracts from legal databases.
