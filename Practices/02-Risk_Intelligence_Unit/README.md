## ✅ Practice 2: 🕵️‍♀️ AI Risk Intelligence Unit – Threat Scenario Simulation

### 📘 Scenario:

You’re designing a cyber risk assessment agent system for an enterprise security team. Your agents must:

- Break down a given threat (e.g., zero-day, phishing)
- Evaluate risk across vectors (infra, data, human)
- Propose mitigations
- Simulate financial and reputational impact
- Generate a formal threat advisory

### 📌 Your tasks:

1. **Define each agent’s expected structure**

   - `ThreatModeler`: Must output a table with:
     \| Attack Vector | Risk Level | Likely Entry Point |
   - `MitigationStrategist`: Must suggest 3+ defenses with cost-benefit notes.
   - `ImpactSimulator`: Must estimate financial loss, brand damage, legal risk (use ranges).

2. **Design output enforcement**
   Implement logic (e.g., via message inspection or memory tracking) to **enforce format compliance**.

3. **Generate a final executive report**
   Let an additional agent `ReportWriter` summarize all input into a threat intelligence memo with headline + structured content.

4. **Bonus challenge**:
   Add a scenario randomizer — let the user choose from a dropdown (or cycle through) different scenarios: insider leak, credential stuffing, cloud misconfig, etc.
