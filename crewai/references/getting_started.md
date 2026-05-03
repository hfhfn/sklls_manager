# Crewai - Getting Started

**Pages:** 5

---

## CrewAI Documentation

**URL:** llms-txt#crewai-documentation

**Contents:**
- Get started
- Build the basics
- Enterprise journey
- What’s new
- Stay connected

Source: https://docs.crewai.com/index

Build collaborative AI agents, crews, and flows — production ready from day one.

<div>
  <img alt="CrewAI" />

<div>
    <h1>Ship multi‑agent systems with confidence</h1>

<p>
      Design agents, orchestrate crews, and automate flows with guardrails, memory, knowledge, and observability baked in.
    </p>
  </div>

<div>
    <a href="/en/quickstart">Get started</a>
    <a href="/en/changelog">View changelog</a>
    <a href="/en/api-reference/introduction">API Reference</a>
  </div>
</div>

<CardGroup>
  <Card title="Introduction" href="/en/introduction" icon="sparkles">
    Overview of CrewAI concepts, architecture, and what you can build with agents, crews, and flows.
  </Card>

<Card title="Installation" href="/en/installation" icon="wrench">
    Install via `uv`, configure API keys, and set up the CLI for local development.
  </Card>

<Card title="Quickstart" href="/en/quickstart" icon="rocket">
    Spin up your first crew in minutes. Learn the core runtime, project layout, and dev loop.
  </Card>
</CardGroup>

<CardGroup>
  <Card title="Agents" href="/en/concepts/agents" icon="users">
    Compose agents with tools, memory, knowledge, and structured outputs using Pydantic. Includes templates and best practices.
  </Card>

<Card title="Flows" href="/en/concepts/flows" icon="arrow-progress">
    Orchestrate start/listen/router steps, manage state, persist execution, and resume long-running workflows.
  </Card>

<Card title="Tasks & Processes" href="/en/concepts/tasks" icon="check">
    Define sequential, hierarchical, or hybrid processes with guardrails, callbacks, and human-in-the-loop triggers.
  </Card>
</CardGroup>

## Enterprise journey

<CardGroup>
  <Card title="Deploy automations" href="/en/enterprise/features/automations" icon="server">
    Manage environments, redeploy safely, and monitor live runs directly from the Enterprise console.
  </Card>

<Card title="Triggers & Flows" href="/en/enterprise/guides/automation-triggers" icon="bolt">
    Connect Gmail, Slack, Salesforce, and more. Pass trigger payloads into crews and flows automatically.
  </Card>

<Card title="Team management" href="/en/enterprise/guides/team-management" icon="users-gear">
    Invite teammates, configure RBAC, and control access to production automations.
  </Card>
</CardGroup>

<CardGroup>
  <Card title="Triggers overview" href="/en/enterprise/guides/automation-triggers" icon="sparkles">
    Unified overview for Gmail, Drive, Outlook, Teams, OneDrive, HubSpot, and more — now with sample payloads and crews.
  </Card>

<Card title="Integration tools" href="/en/tools/integration/overview" icon="plug">
    Call existing CrewAI automations or Amazon Bedrock Agents directly from your crews using the updated integration toolkit.
  </Card>
</CardGroup>

<Callout title="Explore real-world patterns" icon="github">
  Browse the <a href="/en/examples/cookbooks">examples and cookbooks</a> for end-to-end reference implementations across agents, flows, and enterprise automations.
</Callout>

<CardGroup>
  <Card title="Star us on GitHub" href="https://github.com/crewAIInc/crewAI" icon="star">
    If CrewAI helps you ship faster, give us a star and share your builds with the community.
  </Card>

<Card title="Join the community" href="https://community.crewai.com" icon="comments">
    Ask questions, showcase workflows, and request features alongside other builders.
  </Card>
</CardGroup>

---

## For custom Ollama installations

**URL:** llms-txt#for-custom-ollama-installations

**Contents:**
  - Cohere Embeddings
  - VoyageAI Embeddings
  - AWS Bedrock Embeddings
  - Hugging Face Embeddings
  - IBM Watson Embeddings
  - Mem0 Provider
  - Choosing the Right Embedding Provider
  - Environment Variable Configuration

crew = Crew(
    memory=True,
    embedder={
        "provider": "ollama",
        "config": {
            "model": "mxbai-embed-large",
            "url": "http://your-ollama-server:11434/api/embeddings"
        }
    }
)
python theme={null}
crew = Crew(
    memory=True,
    embedder={
        "provider": "cohere",
        "config": {
            "api_key": "your-cohere-api-key",
            "model_name": "embed-english-v3.0"  # or "embed-multilingual-v3.0"
        }
    }
)
python theme={null}
crew = Crew(
    memory=True,
    embedder={
        "provider": "voyageai",
        "config": {
            "api_key": "your-voyage-api-key",
            "model": "voyage-3",  # or "voyage-3-lite", "voyage-code-3"
            "input_type": "document"  # or "query"
        }
    }
)
python theme={null}
crew = Crew(
    memory=True,
    embedder={
        "provider": "bedrock",
        "config": {
            "aws_access_key_id": "your-access-key",
            "aws_secret_access_key": "your-secret-key",
            "region_name": "us-east-1",
            "model": "amazon.titan-embed-text-v1"
        }
    }
)
python theme={null}
crew = Crew(
    memory=True,
    embedder={
        "provider": "huggingface",
        "config": {
            "api_key": "your-hf-token",  # Optional for public models
            "model": "sentence-transformers/all-MiniLM-L6-v2"
        }
    }
)
python theme={null}
crew = Crew(
    memory=True,
    embedder={
        "provider": "watson",
        "config": {
            "api_key": "your-watson-api-key",
            "url": "your-watson-instance-url",
            "model": "ibm/slate-125m-english-rtrvr"
        }
    }
)
python theme={null}
from crewai.memory.short_term.short_term_memory import ShortTermMemory
from crewai.memory.entity_entity_memory import EntityMemory

mem0_oss_embedder_config = {
        "provider": "mem0",
        "config": {
            "user_id": "john",
            "local_mem0_config": {
                "vector_store": {"provider": "qdrant","config": {"host": "localhost", "port": 6333}},
                "llm": {"provider": "openai","config": {"api_key": "your-api-key", "model": "gpt-4"}},
                "embedder": {"provider": "openai","config": {"api_key": "your-api-key", "model": "text-embedding-3-small"}}
            },
            "infer": True # Optional defaults to True
        },
    }

mem0_client_embedder_config = {
        "provider": "mem0",
        "config": {
            "user_id": "john",
            "org_id": "my_org_id",        # Optional
            "project_id": "my_project_id", # Optional
            "api_key": "custom-api-key"    # Optional - overrides env var
            "run_id": "my_run_id",        # Optional - for short-term memory
            "includes": "include1",       # Optional 
            "excludes": "exclude1",       # Optional
            "infer": True                 # Optional defaults to True
            "custom_categories": new_categories  # Optional - custom categories for user memory
        },
    }

short_term_memory_mem0_oss = ShortTermMemory(embedder_config=mem0_oss_embedder_config) # Short Term Memory with Mem0 OSS
short_term_memory_mem0_client = ShortTermMemory(embedder_config=mem0_client_embedder_config) # Short Term Memory with Mem0 Client
entity_memory_mem0_oss = EntityMemory(embedder_config=mem0_oss_embedder_config) # Entity Memory with Mem0 OSS
entity_memory_mem0_client = EntityMemory(embedder_config=mem0_client_embedder_config) # Short Term Memory with Mem0 Client

crew = Crew(
    memory=True,
    short_term_memory=short_term_memory_mem0_oss, # or short_term_memory_mem0_client
    entity_memory=entity_memory_mem0_oss # or entity_memory_mem0_client
)
python theme={null}
import os

**Examples:**

Example 1 (unknown):
```unknown
### Cohere Embeddings

Use Cohere's embedding models for multilingual support.
```

Example 2 (unknown):
```unknown
### VoyageAI Embeddings

High-performance embeddings optimized for retrieval tasks.
```

Example 3 (unknown):
```unknown
### AWS Bedrock Embeddings

For AWS users with Bedrock access.
```

Example 4 (unknown):
```unknown
### Hugging Face Embeddings

Use open-source models from Hugging Face.
```

---

## Installation

**URL:** llms-txt#installation

**Contents:**
- Video Tutorial
- Text Tutorial

Source: https://docs.crewai.com/en/installation

Get started with CrewAI - Install, configure, and build your first AI crew

Watch this video tutorial for a step-by-step demonstration of the installation process:

<iframe title="CrewAI Installation Guide" />

<Note>
  **Python Version Requirements**

CrewAI requires `Python >=3.10 and <3.14`. Here's how to check your version:

If you need to update Python, visit [python.org/downloads](https://python.org/downloads)
</Note>

<Note>
  **OpenAI SDK Requirement**

CrewAI 0.175.0 requires `openai >= 1.13.3`. If you manage dependencies yourself, ensure your environment satisfies this constraint to avoid import/runtime issues.
</Note>

CrewAI uses the `uv` as its dependency management and package handling tool. It simplifies project setup and execution, offering a seamless experience.

If you haven't installed `uv` yet, follow **step 1** to quickly get it set up on your system, else you can skip to **step 2**.

<Steps>
  <Step title="Install uv">
    * **On macOS/Linux:**

Use `curl` to download the script and execute it with `sh`:

If your system doesn't have `curl`, you can use `wget`:

Use `irm` to download the script and `iex` to execute it:

If you run into any issues, refer to [UV's installation guide](https://docs.astral.sh/uv/getting-started/installation/) for more information.
  </Step>

<Step title="Install CrewAI 🚀">
    * Run the following command to install `crewai` CLI:

<Warning>
        If you encounter a `PATH` warning, run this command to update your shell:

<Warning>
        If you encounter the `chroma-hnswlib==0.7.6` build error (`fatal error C1083: Cannot open include file: 'float.h'`) on Windows, install [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/) with *Desktop development with C++*.
      </Warning>

* To verify that `crewai` is installed, run:

* You should see something like:

* If you need to update `crewai`, run:

<Check>Installation successful! You're ready to create your first crew! 🎉</Check>
  </Step>
</Steps>

**Examples:**

Example 1 (unknown):
```unknown
If you need to update Python, visit [python.org/downloads](https://python.org/downloads)
</Note>

<Note>
  **OpenAI SDK Requirement**

  CrewAI 0.175.0 requires `openai >= 1.13.3`. If you manage dependencies yourself, ensure your environment satisfies this constraint to avoid import/runtime issues.
</Note>

CrewAI uses the `uv` as its dependency management and package handling tool. It simplifies project setup and execution, offering a seamless experience.

If you haven't installed `uv` yet, follow **step 1** to quickly get it set up on your system, else you can skip to **step 2**.

<Steps>
  <Step title="Install uv">
    * **On macOS/Linux:**

      Use `curl` to download the script and execute it with `sh`:
```

Example 2 (unknown):
```unknown
If your system doesn't have `curl`, you can use `wget`:
```

Example 3 (unknown):
```unknown
* **On Windows:**

      Use `irm` to download the script and `iex` to execute it:
```

Example 4 (unknown):
```unknown
If you run into any issues, refer to [UV's installation guide](https://docs.astral.sh/uv/getting-started/installation/) for more information.
  </Step>

  <Step title="Install CrewAI 🚀">
    * Run the following command to install `crewai` CLI:
```

---

## Introduction

**URL:** llms-txt#introduction

Source: https://docs.crewai.com/en/api-reference/introduction

Complete reference for the CrewAI AOP REST API

---

## Quickstart

**URL:** llms-txt#quickstart

**Contents:**
- Build your first CrewAI Agent
  - Note on Consistency in Naming
- Deploying Your Crew

Source: https://docs.crewai.com/en/quickstart

Build your first AI agent with CrewAI in under 5 minutes.

## Build your first CrewAI Agent

Let's create a simple crew that will help us `research` and `report` on the `latest AI developments` for a given topic or subject.

Before we proceed, make sure you have finished installing CrewAI.
If you haven't installed them yet, you can do so by following the [installation guide](/en/installation).

Follow the steps below to get Crewing! 🚣‍♂️

<Steps>
  <Step title="Create your crew">
    Create a new crew project by running the following command in your terminal.
    This will create a new directory called `latest-ai-development` with the basic structure for your crew.

<CodeGroup>
      
    </CodeGroup>
  </Step>

<Step title="Navigate to your new crew project">
    <CodeGroup>
      
    </CodeGroup>
  </Step>

<Step title="Modify your `agents.yaml` file">
    <Tip>
      You can also modify the agents as needed to fit your use case or copy and paste as is to your project.
      Any variable interpolated in your `agents.yaml` and `tasks.yaml` files like `{topic}` will be replaced by the value of the variable in the `main.py` file.
    </Tip>

<Step title="Modify your `tasks.yaml` file">
    '
      agent: reporting_analyst
      output_file: report.md
    python crew.py theme={null}
    # src/latest_ai_development/crew.py
    from crewai import Agent, Crew, Process, Task
    from crewai.project import CrewBase, agent, crew, task
    from crewai_tools import SerperDevTool
    from crewai.agents.agent_builder.base_agent import BaseAgent
    from typing import List

@CrewBase
    class LatestAiDevelopmentCrew():
      """LatestAiDevelopment crew"""

agents: List[BaseAgent]
      tasks: List[Task]

@agent
      def researcher(self) -> Agent:
        return Agent(
          config=self.agents_config['researcher'], # type: ignore[index]
          verbose=True,
          tools=[SerperDevTool()]
        )

@agent
      def reporting_analyst(self) -> Agent:
        return Agent(
          config=self.agents_config['reporting_analyst'], # type: ignore[index]
          verbose=True
        )

@task
      def research_task(self) -> Task:
        return Task(
          config=self.tasks_config['research_task'], # type: ignore[index]
        )

@task
      def reporting_task(self) -> Task:
        return Task(
          config=self.tasks_config['reporting_task'], # type: ignore[index]
          output_file='output/report.md' # This is the file that will be contain the final report.
        )

@crew
      def crew(self) -> Crew:
        """Creates the LatestAiDevelopment crew"""
        return Crew(
          agents=self.agents, # Automatically created by the @agent decorator
          tasks=self.tasks, # Automatically created by the @task decorator
          process=Process.sequential,
          verbose=True,
        )
    python crew.py theme={null}
    # src/latest_ai_development/crew.py
    from crewai import Agent, Crew, Process, Task
    from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
    from crewai_tools import SerperDevTool

@CrewBase
    class LatestAiDevelopmentCrew():
      """LatestAiDevelopment crew"""

@before_kickoff
      def before_kickoff_function(self, inputs):
        print(f"Before kickoff function with inputs: {inputs}")
        return inputs # You can return the inputs or modify them as needed

@after_kickoff
      def after_kickoff_function(self, result):
        print(f"After kickoff function with result: {result}")
        return result # You can return the result or modify it as needed

# ... remaining code
    python main.py theme={null}
    #!/usr/bin/env python
    # src/latest_ai_development/main.py
    import sys
    from latest_ai_development.crew import LatestAiDevelopmentCrew

def run():
      """
      Run the crew.
      """
      inputs = {
        'topic': 'AI Agents'
      }
      LatestAiDevelopmentCrew().crew().kickoff(inputs=inputs)
    shell Terminal theme={null}
        crewai install
        shell Terminal theme={null}
        uv add <package-name>
        bash Terminal theme={null}
        crewai run
        markdown output/report.md theme={null}
      # Comprehensive Report on the Rise and Impact of AI Agents in 2025

## 1. Introduction to AI Agents
      In 2025, Artificial Intelligence (AI) agents are at the forefront of innovation across various industries. As intelligent systems that can perform tasks typically requiring human cognition, AI agents are paving the way for significant advancements in operational efficiency, decision-making, and overall productivity within sectors like Human Resources (HR) and Finance. This report aims to detail the rise of AI agents, their frameworks, applications, and potential implications on the workforce.

## 2. Benefits of AI Agents
      AI agents bring numerous advantages that are transforming traditional work environments. Key benefits include:

- **Task Automation**: AI agents can carry out repetitive tasks such as data entry, scheduling, and payroll processing without human intervention, greatly reducing the time and resources spent on these activities.
      - **Improved Efficiency**: By quickly processing large datasets and performing analyses that would take humans significantly longer, AI agents enhance operational efficiency. This allows teams to focus on strategic tasks that require higher-level thinking.
      - **Enhanced Decision-Making**: AI agents can analyze trends and patterns in data, provide insights, and even suggest actions, helping stakeholders make informed decisions based on factual data rather than intuition alone.

## 3. Popular AI Agent Frameworks
      Several frameworks have emerged to facilitate the development of AI agents, each with its own unique features and capabilities. Some of the most popular frameworks include:

- **Autogen**: A framework designed to streamline the development of AI agents through automation of code generation.
      - **Semantic Kernel**: Focuses on natural language processing and understanding, enabling agents to comprehend user intentions better.
      - **Promptflow**: Provides tools for developers to create conversational agents that can navigate complex interactions seamlessly.
      - **Langchain**: Specializes in leveraging various APIs to ensure agents can access and utilize external data effectively.
      - **CrewAI**: Aimed at collaborative environments, CrewAI strengthens teamwork by facilitating communication through AI-driven insights.
      - **MemGPT**: Combines memory-optimized architectures with generative capabilities, allowing for more personalized interactions with users.

These frameworks empower developers to build versatile and intelligent agents that can engage users, perform advanced analytics, and execute various tasks aligned with organizational goals.

## 4. AI Agents in Human Resources
      AI agents are revolutionizing HR practices by automating and optimizing key functions:

- **Recruiting**: AI agents can screen resumes, schedule interviews, and even conduct initial assessments, thus accelerating the hiring process while minimizing biases.
      - **Succession Planning**: AI systems analyze employee performance data and potential, helping organizations identify future leaders and plan appropriate training.
      - **Employee Engagement**: Chatbots powered by AI can facilitate feedback loops between employees and management, promoting an open culture and addressing concerns promptly.

As AI continues to evolve, HR departments leveraging these agents can realize substantial improvements in both efficiency and employee satisfaction.

## 5. AI Agents in Finance
      The finance sector is seeing extensive integration of AI agents that enhance financial practices:

- **Expense Tracking**: Automated systems manage and monitor expenses, flagging anomalies and offering recommendations based on spending patterns.
      - **Risk Assessment**: AI models assess credit risk and uncover potential fraud by analyzing transaction data and behavioral patterns.
      - **Investment Decisions**: AI agents provide stock predictions and analytics based on historical data and current market conditions, empowering investors with informative insights.

The incorporation of AI agents into finance is fostering a more responsive and risk-aware financial landscape.

## 6. Market Trends and Investments
      The growth of AI agents has attracted significant investment, especially amidst the rising popularity of chatbots and generative AI technologies. Companies and entrepreneurs are eager to explore the potential of these systems, recognizing their ability to streamline operations and improve customer engagement.

Conversely, corporations like Microsoft are taking strides to integrate AI agents into their product offerings, with enhancements to their Copilot 365 applications. This strategic move emphasizes the importance of AI literacy in the modern workplace and indicates the stabilizing of AI agents as essential business tools.

## 7. Future Predictions and Implications
      Experts predict that AI agents will transform essential aspects of work life. As we look toward the future, several anticipated changes include:

- Enhanced integration of AI agents across all business functions, creating interconnected systems that leverage data from various departmental silos for comprehensive decision-making.
      - Continued advancement of AI technologies, resulting in smarter, more adaptable agents capable of learning and evolving from user interactions.
      - Increased regulatory scrutiny to ensure ethical use, especially concerning data privacy and employee surveillance as AI agents become more prevalent.

To stay competitive and harness the full potential of AI agents, organizations must remain vigilant about latest developments in AI technology and consider continuous learning and adaptation in their strategic planning.

## 8. Conclusion
      The emergence of AI agents is undeniably reshaping the workplace landscape in 5. With their ability to automate tasks, enhance efficiency, and improve decision-making, AI agents are critical in driving operational success. Organizations must embrace and adapt to AI developments to thrive in an increasingly digital business environment.
      yaml agents.yaml theme={null}
email_summarizer:
    role: >
      Email Summarizer
    goal: >
      Summarize emails into a concise and clear summary
    backstory: >
      You will create a 5 bullet point summary of the report
    llm: provider/model-id  # Add your choice of model here
yaml tasks.yaml theme={null}
email_summarizer_task:
    description: >
      Summarize the email into a 5 bullet point summary
    expected_output: >
      A 5 bullet point summary of the email
    agent: email_summarizer
    context:
      - reporting_task
      - research_task
```

## Deploying Your Crew

The easiest way to deploy your crew to production is through [CrewAI AOP](http://app.crewai.com).

Watch this video tutorial for a step-by-step demonstration of deploying your crew to [CrewAI AOP](http://app.crewai.com) using the CLI.

<iframe title="CrewAI Deployment Guide" />

<CardGroup>
  <Card title="Deploy on Enterprise" icon="rocket" href="http://app.crewai.com">
    Get started with CrewAI AOP and deploy your crew in a production environment with just a few clicks.
  </Card>

<Card title="Join the Community" icon="comments" href="https://community.crewai.com">
    Join our open source community to discuss ideas, share your projects, and connect with other CrewAI developers.
  </Card>
</CardGroup>

**Examples:**

Example 1 (unknown):
```unknown
</CodeGroup>
  </Step>

  <Step title="Navigate to your new crew project">
    <CodeGroup>
```

Example 2 (unknown):
```unknown
</CodeGroup>
  </Step>

  <Step title="Modify your `agents.yaml` file">
    <Tip>
      You can also modify the agents as needed to fit your use case or copy and paste as is to your project.
      Any variable interpolated in your `agents.yaml` and `tasks.yaml` files like `{topic}` will be replaced by the value of the variable in the `main.py` file.
    </Tip>
```

Example 3 (unknown):
```unknown
</Step>

  <Step title="Modify your `tasks.yaml` file">
```

Example 4 (unknown):
```unknown
</Step>

  <Step title="Modify your `crew.py` file">
```

---
