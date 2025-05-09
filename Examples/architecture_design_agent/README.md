# Architecture Design Agent

This example demonstrates a multi-agent system for architecture design using AutoGen. The system consists of specialized agents working together to design an architecture based on client requirements.

## Running the Agent

### Direct Execution

You can directly run the agent using:

```bash
python ai_agents.py
```

This will start the architecture design session in the terminal with the default task.

### Visualization UI

For a better view of the multi-agent conversation, a visualization UI is also provided:

1. Install the required dependencies:

   ```bash
   uv pip install -r requirements.txt
   ```

2. Start the visualization server:

   ```bash
   python app.py
   ```

3. Open your browser and navigate to:

   ```
   http://localhost:5000
   ```

4. Enter your task requirements in the provided interface and click "Start Conversation" to begin the architecture design process.
