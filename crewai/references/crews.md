# Crewai - Crews

**Pages:** 74

---

## Accessing the crew output

**URL:** llms-txt#accessing-the-crew-output

**Contents:**
- Accessing Crew Logs

print(f"Raw Output: {crew_output.raw}")
if crew_output.json_dict:
    print(f"JSON Output: {json.dumps(crew_output.json_dict, indent=2)}")
if crew_output.pydantic:
    print(f"Pydantic Output: {crew_output.pydantic}")
print(f"Tasks Output: {crew_output.tasks_output}")
print(f"Token Usage: {crew_output.token_usage}")
python Code theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## Accessing Crew Logs

You can see real time log of the crew execution, by setting `output_log_file` as a `True(Boolean)` or a `file_name(str)`. Supports logging of events as both `file_name.txt` and `file_name.json`.
In case of `True(Boolean)` will save as `logs.txt`.

In case of `output_log_file` is set as `False(Boolean)` or `None`, the logs will not be populated.
```

---

## Access final result

**URL:** llms-txt#access-final-result

**Contents:**
  - Using the CLI

result = streaming.result
shell theme={null}
crewai run
shell theme={null}
crewai flow kickoff
```

However, the `crewai run` command is now the preferred method as it works for both crews and flows.

**Examples:**

Example 1 (unknown):
```unknown
Learn more about streaming in the [Streaming Flow Execution](/en/learn/streaming-flow-execution) guide.

### Using the CLI

Starting from version 0.103.0, you can run flows using the `crewai run` command:
```

Example 2 (unknown):
```unknown
This command automatically detects if your project is a flow (based on the `type = "flow"` setting in your pyproject.toml) and runs it accordingly. This is the recommended way to run flows from the command line.

For backward compatibility, you can also use:
```

---

## Automations

**URL:** llms-txt#automations

**Contents:**
- Overview
- Deployment Methods
  - Deploy from GitHub
  - Deploy from ZIP
- Automations Dashboard
- Best Practices
- Related

Source: https://docs.crewai.com/en/enterprise/features/automations

Manage, deploy, and monitor your live crews (automations) in one place.

Automations is the live operations hub for your deployed crews. Use it to deploy from GitHub or a ZIP file, manage environment variables, re‑deploy when needed, and monitor the status of each automation.

<Frame>
  <img alt="Automations Overview" />
</Frame>

## Deployment Methods

### Deploy from GitHub

Use this for version‑controlled projects and continuous deployment.

<Steps>
  <Step title="Connect GitHub">
    Click <b>Configure GitHub</b> and authorize access.
  </Step>

<Step title="Select Repository & Branch">
    Choose the <b>Repository</b> and <b>Branch</b> you want to deploy from.
  </Step>

<Step title="Enable Auto‑deploy (optional)">
    Turn on <b>Automatically deploy new commits</b> to ship updates on every push.
  </Step>

<Step title="Add Environment Variables">
    Add secrets individually or use <b>Bulk View</b> for multiple variables.
  </Step>

<Step title="Deploy">
    Click <b>Deploy</b> to create your live automation.
  </Step>
</Steps>

<Frame>
  <img alt="GitHub Deployment" />
</Frame>

Ship quickly without Git—upload a compressed package of your project.

<Steps>
  <Step title="Choose File">
    Select the ZIP archive from your computer.
  </Step>

<Step title="Add Environment Variables">
    Provide any required variables or keys.
  </Step>

<Step title="Deploy">
    Click <b>Deploy</b> to create your live automation.
  </Step>
</Steps>

<Frame>
  <img alt="ZIP Deployment" />
</Frame>

## Automations Dashboard

The table lists all live automations with key details:

* **CREW**: Automation name
* **STATUS**: Online / Failed / In Progress
* **URL**: Endpoint for kickoff/status
* **TOKEN**: Automation token
* **ACTIONS**: Re‑deploy, delete, and more

Use the top‑right controls to filter and search:

* Search by name
* Filter by <b>Status</b>
* Filter by <b>Source</b> (GitHub / Studio / ZIP)

Once deployed, you can view the automation details and have the **Options** dropdown menu to `chat with this crew`, `Export React Component` and `Export as MCP`.

<Frame>
  <img alt="Automations Table" />
</Frame>

* Prefer GitHub deployments for version control and CI/CD
* Use re‑deploy to roll forward after code or config updates or set it to auto-deploy on every push

<CardGroup>
  <Card title="Deploy a Crew" href="/en/enterprise/guides/deploy-crew" icon="rocket">
    Deploy a Crew from GitHub or ZIP file.
  </Card>

<Card title="Automation Triggers" href="/en/enterprise/guides/automation-triggers" icon="trigger">
    Trigger automations via webhooks or API.
  </Card>

<Card title="Webhook Automation" href="/en/enterprise/guides/webhook-automation" icon="webhook">
    Stream real-time events and updates to your systems.
  </Card>
</CardGroup>

---

## Build Your First Flow

**URL:** llms-txt#build-your-first-flow

**Contents:**
- Taking Control of AI Workflows with Flows
  - What Makes Flows Powerful
  - What You'll Build and Learn
- Prerequisites
- Step 1: Create a New CrewAI Flow Project
- Step 2: Understanding the Project Structure
- Step 3: Add a Content Writer Crew
- Step 4: Configure the Content Writer Crew

Source: https://docs.crewai.com/en/guides/flows/first-flow

Learn how to create structured, event-driven workflows with precise control over execution.

## Taking Control of AI Workflows with Flows

CrewAI Flows represent the next level in AI orchestration - combining the collaborative power of AI agent crews with the precision and flexibility of procedural programming. While crews excel at agent collaboration, flows give you fine-grained control over exactly how and when different components of your AI system interact.

In this guide, we'll walk through creating a powerful CrewAI Flow that generates a comprehensive learning guide on any topic. This tutorial will demonstrate how Flows provide structured, event-driven control over your AI workflows by combining regular code, direct LLM calls, and crew-based processing.

### What Makes Flows Powerful

1. **Combine different AI interaction patterns** - Use crews for complex collaborative tasks, direct LLM calls for simpler operations, and regular code for procedural logic
2. **Build event-driven systems** - Define how components respond to specific events and data changes
3. **Maintain state across components** - Share and transform data between different parts of your application
4. **Integrate with external systems** - Seamlessly connect your AI workflow with databases, APIs, and user interfaces
5. **Create complex execution paths** - Design conditional branches, parallel processing, and dynamic workflows

### What You'll Build and Learn

By the end of this guide, you'll have:

1. **Created a sophisticated content generation system** that combines user input, AI planning, and multi-agent content creation
2. **Orchestrated the flow of information** between different components of your system
3. **Implemented event-driven architecture** where each step responds to the completion of previous steps
4. **Built a foundation for more complex AI applications** that you can expand and customize

This guide creator flow demonstrates fundamental patterns that can be applied to create much more advanced applications, such as:

* Interactive AI assistants that combine multiple specialized subsystems
* Complex data processing pipelines with AI-enhanced transformations
* Autonomous agents that integrate with external services and APIs
* Multi-stage decision-making systems with human-in-the-loop processes

Let's dive in and build your first flow!

Before starting, make sure you have:

1. Installed CrewAI following the [installation guide](/en/installation)
2. Set up your LLM API key in your environment, following the [LLM setup
   guide](/en/concepts/llms#setting-up-your-llm)
3. Basic understanding of Python

## Step 1: Create a New CrewAI Flow Project

First, let's create a new CrewAI Flow project using the CLI. This command sets up a scaffolded project with all the necessary directories and template files for your flow.

This will generate a project with the basic structure needed for your flow.

<Frame>
  <img alt="CrewAI Framework Overview" />
</Frame>

## Step 2: Understanding the Project Structure

The generated project has the following structure. Take a moment to familiarize yourself with it, as understanding this structure will help you create more complex flows in the future.

This structure provides a clear separation between different components of your flow:

* The main flow logic in the `main.py` file
* Specialized crews in the `crews` directory
* Custom tools in the `tools` directory

We'll modify this structure to create our guide creator flow, which will orchestrate the process of generating comprehensive learning guides.

## Step 3: Add a Content Writer Crew

Our flow will need a specialized crew to handle the content creation process. Let's use the CrewAI CLI to add a content writer crew:

This command automatically creates the necessary directories and template files for your crew. The content writer crew will be responsible for writing and reviewing sections of our guide, working within the overall flow orchestrated by our main application.

## Step 4: Configure the Content Writer Crew

Now, let's modify the generated files for the content writer crew. We'll set up two specialized agents - a writer and a reviewer - that will collaborate to create high-quality content for our guide.

1. First, update the agents configuration file to define our content creation team:

Remember to set `llm` to the provider you are using.

**Examples:**

Example 1 (unknown):
```unknown
This will generate a project with the basic structure needed for your flow.

<Frame>
  <img alt="CrewAI Framework Overview" />
</Frame>

## Step 2: Understanding the Project Structure

The generated project has the following structure. Take a moment to familiarize yourself with it, as understanding this structure will help you create more complex flows in the future.
```

Example 2 (unknown):
```unknown
This structure provides a clear separation between different components of your flow:

* The main flow logic in the `main.py` file
* Specialized crews in the `crews` directory
* Custom tools in the `tools` directory

We'll modify this structure to create our guide creator flow, which will orchestrate the process of generating comprehensive learning guides.

## Step 3: Add a Content Writer Crew

Our flow will need a specialized crew to handle the content creation process. Let's use the CrewAI CLI to add a content writer crew:
```

Example 3 (unknown):
```unknown
This command automatically creates the necessary directories and template files for your crew. The content writer crew will be responsible for writing and reviewing sections of our guide, working within the overall flow orchestrated by our main application.

## Step 4: Configure the Content Writer Crew

Now, let's modify the generated files for the content writer crew. We'll set up two specialized agents - a writer and a reviewer - that will collaborate to create high-quality content for our guide.

1. First, update the agents configuration file to define our content creation team:

   Remember to set `llm` to the provider you are using.
```

---

## Conditional Tasks

**URL:** llms-txt#conditional-tasks

**Contents:**
- Introduction
- Example Usage

Source: https://docs.crewai.com/en/learn/conditional-tasks

Learn how to use conditional tasks in a crewAI kickoff

Conditional Tasks in crewAI allow for dynamic workflow adaptation based on the outcomes of previous tasks.
This powerful feature enables crews to make decisions and execute tasks selectively, enhancing the flexibility and efficiency of your AI-driven processes.

```python Code theme={null}
from typing import List
from pydantic import BaseModel
from crewai import Agent, Crew
from crewai.tasks.conditional_task import ConditionalTask
from crewai.tasks.task_output import TaskOutput
from crewai.task import Task
from crewai_tools import SerperDevTool

---

## Connect to CrewAI's ChromaDB

**URL:** llms-txt#connect-to-crewai's-chromadb

storage_path = db_storage_path()
chroma_path = os.path.join(storage_path, "knowledge")

if os.path.exists(chroma_path):
    client = chromadb.PersistentClient(path=chroma_path)
    collections = client.list_collections()

print("ChromaDB Collections:")
    for collection in collections:
        print(f"  - {collection.name}: {collection.count()} documents")
else:
    print("No ChromaDB storage found")
python theme={null}
from crewai import Crew

**Examples:**

Example 1 (unknown):
```unknown
#### Reset Storage (Debugging)
```

---

## Connect to CrewAI's knowledge ChromaDB

**URL:** llms-txt#connect-to-crewai's-knowledge-chromadb

knowledge_path = os.path.join(db_storage_path(), "knowledge")

if os.path.exists(knowledge_path):
    client = chromadb.PersistentClient(path=knowledge_path)
    collections = client.list_collections()
    
    print("Knowledge Collections:")
    for collection in collections:
        print(f"  - {collection.name}: {collection.count()} documents")
        
        # Sample a few documents to verify content
        if collection.count() > 0:
            sample = collection.peek(limit=2)
            print(f"    Sample content: {sample['documents'][0][:100]}...")
else:
    print("No knowledge storage found")
python theme={null}
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

**Examples:**

Example 1 (unknown):
```unknown
#### Check Knowledge Processing
```

---

## Create and run the flow with tracing enabled

**URL:** llms-txt#create-and-run-the-flow-with-tracing-enabled

**Contents:**
  - Step 5: View Traces in the CrewAI AOP Dashboard
  - Alternative: Environment Variable Configuration
- Viewing Your Traces
  - Access the CrewAI AOP Dashboard
  - What You'll See in Traces
  - Trace Features
  - Authentication Issues
  - Traces Not Appearing

flow = ExampleFlow(tracing=True)
result = flow.kickoff()
bash theme={null}
export CREWAI_TRACING_ENABLED=true
env theme={null}
CREWAI_TRACING_ENABLED=true
```

When this environment variable is set, all Crews and Flows will automatically have tracing enabled, even without explicitly setting `tracing=True`.

## Viewing Your Traces

### Access the CrewAI AOP Dashboard

1. Visit [app.crewai.com](https://app.crewai.com) and log in to your account
2. Navigate to your project dashboard
3. Click on the **Traces** tab to view execution details

### What You'll See in Traces

CrewAI tracing provides comprehensive visibility into:

* **Agent Decisions**: See how agents reason through tasks and make decisions
* **Task Execution Timeline**: Visual representation of task sequences and dependencies
* **Tool Usage**: Monitor which tools are called and their results
* **LLM Calls**: Track all language model interactions, including prompts and responses
* **Performance Metrics**: Execution times, token usage, and costs
* **Error Tracking**: Detailed error information and stack traces

* **Execution Timeline**: Click through different stages of execution
* **Detailed Logs**: Access comprehensive logs for debugging
* **Performance Analytics**: Analyze execution patterns and optimize performance
* **Export Capabilities**: Download traces for further analysis

### Authentication Issues

If you encounter authentication problems:

1. Ensure you're logged in: `crewai login`
2. Check your internet connection
3. Verify your account at [app.crewai.com](https://app.crewai.com)

### Traces Not Appearing

If traces aren't showing up in the dashboard:

1. Confirm `tracing=True` is set in your Crew/Flow
2. Check that `CREWAI_TRACING_ENABLED=true` if using environment variables
3. Ensure you're authenticated with `crewai login`
4. Verify your crew/flow is actually executing

**Examples:**

Example 1 (unknown):
```unknown
### Step 5: View Traces in the CrewAI AOP Dashboard

After running the crew or flow, you can view the traces generated by your CrewAI application in the CrewAI AOP dashboard. You should see detailed steps of the agent interactions, tool usages, and LLM calls.
Just click on the link below to view the traces or head over to the traces tab in the dashboard [here](https://app.crewai.com/crewai_plus/trace_batches)

<img alt="CrewAI Tracing Interface" />

### Alternative: Environment Variable Configuration

You can also enable tracing globally by setting an environment variable:
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

---

## CrewAI AOP API

**URL:** llms-txt#crewai-aop-api

**Contents:**
- Quick Start
- Authentication
  - Token Types
- Base URL
- Typical Workflow
- Error Handling
- Interactive Testing
  - **To Test Your Actual API:**
- Need Help?

Welcome to the CrewAI AOP API reference. This API allows you to programmatically interact with your deployed crews, enabling integration with your applications, workflows, and services.

<Steps>
  <Step title="Get Your API Credentials">
    Navigate to your crew's detail page in the CrewAI AOP dashboard and copy your Bearer Token from the Status tab.
  </Step>

<Step title="Discover Required Inputs">
    Use the `GET /inputs` endpoint to see what parameters your crew expects.
  </Step>

<Step title="Start a Crew Execution">
    Call `POST /kickoff` with your inputs to start the crew execution and receive
    a `kickoff_id`.
  </Step>

<Step title="Monitor Progress">
    Use `GET /{kickoff_id}/status` to check execution status and retrieve results.
  </Step>
</Steps>

All API requests require authentication using a Bearer token. Include your token in the `Authorization` header:

| Token Type            | Scope                     | Use Case                                                     |
| :-------------------- | :------------------------ | :----------------------------------------------------------- |
| **Bearer Token**      | Organization-level access | Full crew operations, ideal for server-to-server integration |
| **User Bearer Token** | User-scoped access        | Limited permissions, suitable for user-specific operations   |

<Tip>
  You can find both token types in the Status tab of your crew's detail page in
  the CrewAI AOP dashboard.
</Tip>

Each deployed crew has its own unique API endpoint:

Replace `your-crew-name` with your actual crew's URL from the dashboard.

1. **Discovery**: Call `GET /inputs` to understand what your crew needs
2. **Execution**: Submit inputs via `POST /kickoff` to start processing
3. **Monitoring**: Poll `GET /{kickoff_id}/status` until completion
4. **Results**: Extract the final output from the completed response

The API uses standard HTTP status codes:

| Code  | Meaning                                    |
| ----- | :----------------------------------------- |
| `200` | Success                                    |
| `400` | Bad Request - Invalid input format         |
| `401` | Unauthorized - Invalid bearer token        |
| `404` | Not Found - Resource doesn't exist         |
| `422` | Validation Error - Missing required inputs |
| `500` | Server Error - Contact support             |

## Interactive Testing

<Info>
  **Why no "Send" button?** Since each CrewAI AOP user has their own unique crew
  URL, we use **reference mode** instead of an interactive playground to avoid
  confusion. This shows you exactly what the requests should look like without
  non-functional send buttons.
</Info>

Each endpoint page shows you:

* ✅ **Exact request format** with all parameters
* ✅ **Response examples** for success and error cases
* ✅ **Code samples** in multiple languages (cURL, Python, JavaScript, etc.)
* ✅ **Authentication examples** with proper Bearer token format

### **To Test Your Actual API:**

<CardGroup>
  <Card title="Copy cURL Examples" icon="terminal">
    Copy the cURL examples and replace the URL + token with your real values
  </Card>

<Card title="Use Postman/Insomnia" icon="play">
    Import the examples into your preferred API testing tool
  </Card>
</CardGroup>

**Example workflow:**

1. **Copy this cURL example** from any endpoint page
2. **Replace `your-actual-crew-name.crewai.com`** with your real crew URL
3. **Replace the Bearer token** with your real token from the dashboard
4. **Run the request** in your terminal or API client

<CardGroup>
  <Card title="Enterprise Support" icon="headset" href="mailto:support@crewai.com">
    Get help with API integration and troubleshooting
  </Card>

<Card title="Enterprise Dashboard" icon="chart-line" href="https://app.crewai.com">
    Manage your crews and view execution logs
  </Card>
</CardGroup>

**Examples:**

Example 1 (unknown):
```unknown
### Token Types

| Token Type            | Scope                     | Use Case                                                     |
| :-------------------- | :------------------------ | :----------------------------------------------------------- |
| **Bearer Token**      | Organization-level access | Full crew operations, ideal for server-to-server integration |
| **User Bearer Token** | User-scoped access        | Limited permissions, suitable for user-specific operations   |

<Tip>
  You can find both token types in the Status tab of your crew's detail page in
  the CrewAI AOP dashboard.
</Tip>

## Base URL

Each deployed crew has its own unique API endpoint:
```

---

## CrewAI creates tools: "mcp_exa_ai_search", "mcp_exa_ai_analyze"

**URL:** llms-txt#crewai-creates-tools:-"mcp_exa_ai_search",-"mcp_exa_ai_analyze"

agent = Agent(
    role="Tool Organization Demo",
    goal="Show how tool naming works",
    backstory="Demonstrates automatic tool organization",
    mcps=[
        "https://mcp.exa.ai/mcp?api_key=key",      # Tools: mcp_exa_ai_*
        "https://weather.service.com/mcp",         # Tools: weather_service_com_*
        "crewai-amp:financial-data"                # Tools: financial_data_*
    ]
)

---

## CrewAI Examples

**URL:** llms-txt#crewai-examples

**Contents:**
- Crews
- Flows
- Integrations
- Notebooks

Source: https://docs.crewai.com/en/examples/example

Explore curated examples organized by Crews, Flows, Integrations, and Notebooks.

<CardGroup>
  <Card title="Marketing Strategy" icon="bullhorn" href="https://github.com/crewAIInc/crewAI-examples/tree/main/crews/marketing_strategy">
    Multi‑agent marketing campaign planning.
  </Card>

<Card title="Surprise Trip" icon="plane" href="https://github.com/crewAIInc/crewAI-examples/tree/main/crews/surprise_trip">
    Personalized surprise travel planning.
  </Card>

<Card title="Match Profile to Positions" icon="id-card" href="https://github.com/crewAIInc/crewAI-examples/tree/main/crews/match_profile_to_positions">
    CV‑to‑job matching with vector search.
  </Card>

<Card title="Job Posting" icon="newspaper" href="https://github.com/crewAIInc/crewAI-examples/tree/main/crews/job-posting">
    Automated job description creation.
  </Card>

<Card title="Game Builder Crew" icon="gamepad" href="https://github.com/crewAIInc/crewAI-examples/tree/main/crews/game-builder-crew">
    Multi‑agent team that designs and builds Python games.
  </Card>

<Card title="Recruitment" icon="user-group" href="https://github.com/crewAIInc/crewAI-examples/tree/main/crews/recruitment">
    Candidate sourcing and evaluation.
  </Card>

<Card title="Browse all Crews" icon="users" href="https://github.com/crewAIInc/crewAI-examples/tree/main/crews">
    See the full list of crew examples.
  </Card>
</CardGroup>

<CardGroup>
  <Card title="Content Creator Flow" icon="pen" href="https://github.com/crewAIInc/crewAI-examples/tree/main/flows/content_creator_flow">
    Multi‑crew content generation with routing.
  </Card>

<Card title="Email Auto Responder" icon="envelope" href="https://github.com/crewAIInc/crewAI-examples/tree/main/flows/email_auto_responder_flow">
    Automated email monitoring and replies.
  </Card>

<Card title="Lead Score Flow" icon="chart-line" href="https://github.com/crewAIInc/crewAI-examples/tree/main/flows/lead_score_flow">
    Lead qualification with human‑in‑the‑loop.
  </Card>

<Card title="Meeting Assistant Flow" icon="calendar" href="https://github.com/crewAIInc/crewAI-examples/tree/main/flows/meeting_assistant_flow">
    Notes processing with integrations.
  </Card>

<Card title="Self Evaluation Loop" icon="rotate" href="https://github.com/crewAIInc/crewAI-examples/tree/main/flows/self_evaluation_loop_flow">
    Iterative self‑improvement workflows.
  </Card>

<Card title="Write a Book (Flows)" icon="book" href="https://github.com/crewAIInc/crewAI-examples/tree/main/flows/write_a_book_with_flows">
    Parallel chapter generation.
  </Card>

<Card title="Browse all Flows" icon="diagram-project" href="https://github.com/crewAIInc/crewAI-examples/tree/main/flows">
    See the full list of flow examples.
  </Card>
</CardGroup>

<CardGroup>
  <Card title="CrewAI ↔ LangGraph" icon="link" href="https://github.com/crewAIInc/crewAI-examples/tree/main/integrations/crewai-langgraph">
    Integration with LangGraph framework.
  </Card>

<Card title="Azure OpenAI" icon="cloud" href="https://github.com/crewAIInc/crewAI-examples/tree/main/integrations/azure_model">
    Using CrewAI with Azure OpenAI.
  </Card>

<Card title="NVIDIA Models" icon="microchip" href="https://github.com/crewAIInc/crewAI-examples/tree/main/integrations/nvidia_models">
    NVIDIA ecosystem integrations.
  </Card>

<Card title="Browse Integrations" icon="puzzle-piece" href="https://github.com/crewAIInc/crewAI-examples/tree/main/integrations">
    See all integration examples.
  </Card>
</CardGroup>

<CardGroup>
  <Card title="Simple QA Crew + Flow" icon="book" href="https://github.com/crewAIInc/crewAI-examples/tree/main/Notebooks/Simple%20QA%20Crew%20%2B%20Flow">
    Simple QA Crew + Flow.
  </Card>

<Card title="All Notebooks" icon="book" href="https://github.com/crewAIInc/crewAI-examples/tree/main/Notebooks">
    Interactive examples for learning and experimentation.
  </Card>
</CardGroup>

---

## CrewAI Tracing

**URL:** llms-txt#crewai-tracing

Source: https://docs.crewai.com/en/observability/tracing

Built-in tracing for CrewAI Crews and Flows with the CrewAI AOP platform

---

## CrewAI will log warnings and continue with other servers

**URL:** llms-txt#crewai-will-log-warnings-and-continue-with-other-servers

---

## CrewAI will still use OpenAI embeddings by default for knowledge

**URL:** llms-txt#crewai-will-still-use-openai-embeddings-by-default-for-knowledge

---

## CrewAI will use OpenAI embeddings by default for consistency

**URL:** llms-txt#crewai-will-use-openai-embeddings-by-default-for-consistency

---

## Crew knowledge storage

**URL:** llms-txt#crew-knowledge-storage

crew_collection_name = "crew"

---

## Deploy Crew

**URL:** llms-txt#deploy-crew

**Contents:**
- Prerequisites
- Option 1: Deploy Using CrewAI CLI
- Additional CLI Commands

Source: https://docs.crewai.com/en/enterprise/guides/deploy-crew

Deploying a Crew on CrewAI AOP

<Note>
  After creating a crew locally or through Crew Studio, the next step is deploying it to the CrewAI AOP platform. This guide covers multiple deployment methods to help you choose the best approach for your workflow.
</Note>

<CardGroup>
  <Card title="Crew Ready for Deployment" icon="users">
    You should have a working crew either built locally or created through Crew Studio
  </Card>

<Card title="GitHub Repository" icon="github">
    Your crew code should be in a GitHub repository (for GitHub integration method)
  </Card>
</CardGroup>

## Option 1: Deploy Using CrewAI CLI

The CLI provides the fastest way to deploy locally developed crews to the Enterprise platform.

<Steps>
  <Step title="Install CrewAI CLI">
    If you haven't already, install the CrewAI CLI:

<Tip>
      The CLI comes with the main CrewAI package, but the `[tools]` extra ensures you have all deployment dependencies.
    </Tip>
  </Step>

<Step title="Authenticate with the Enterprise Platform">
    First, you need to authenticate your CLI with the CrewAI AOP platform:

When you run either command, the CLI will:

1. Display a URL and a unique device code
    2. Open your browser to the authentication page
    3. Prompt you to confirm the device
    4. Complete the authentication process

Upon successful authentication, you'll see a confirmation message in your terminal!
  </Step>

<Step title="Create a Deployment">
    From your project directory, run:

1. Detect your GitHub repository information
    2. Identify environment variables in your local `.env` file
    3. Securely transfer these variables to the Enterprise platform
    4. Create a new deployment with a unique identifier

On successful creation, you'll see a message like:

<Step title="Monitor Deployment Progress">
    Track the deployment status with:

For detailed logs of the build process:

<Tip>
      The first deployment typically takes 10-15 minutes as it builds the container images. Subsequent deployments are much faster.
    </Tip>
  </Step>
</Steps>

## Additional CLI Commands

The CrewAI CLI offers several commands to manage your deployments:

**Examples:**

Example 1 (unknown):
```unknown
<Tip>
      The CLI comes with the main CrewAI package, but the `[tools]` extra ensures you have all deployment dependencies.
    </Tip>
  </Step>

  <Step title="Authenticate with the Enterprise Platform">
    First, you need to authenticate your CLI with the CrewAI AOP platform:
```

Example 2 (unknown):
```unknown
When you run either command, the CLI will:

    1. Display a URL and a unique device code
    2. Open your browser to the authentication page
    3. Prompt you to confirm the device
    4. Complete the authentication process

    Upon successful authentication, you'll see a confirmation message in your terminal!
  </Step>

  <Step title="Create a Deployment">
    From your project directory, run:
```

Example 3 (unknown):
```unknown
This command will:

    1. Detect your GitHub repository information
    2. Identify environment variables in your local `.env` file
    3. Securely transfer these variables to the Enterprise platform
    4. Create a new deployment with a unique identifier

    On successful creation, you'll see a message like:
```

Example 4 (unknown):
```unknown
</Step>

  <Step title="Monitor Deployment Progress">
    Track the deployment status with:
```

---

## Disable all OpenTelemetry (including CrewAI)

**URL:** llms-txt#disable-all-opentelemetry-(including-crewai)

**Contents:**
  - Data Explanation:
  - Opt-In Further Telemetry Sharing

os.environ['OTEL_SDK_DISABLED'] = 'true'
```

### Data Explanation:

| Defaulted | Data                                     | Reason and Specifics                                                                                                                                                                                                                                                                                             |
| :-------- | :--------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Yes       | CrewAI and Python Version                | Tracks software versions. Example: CrewAI v1.2.3, Python 3.8.10. No personal data.                                                                                                                                                                                                                               |
| Yes       | Crew Metadata                            | Includes: randomly generated key and ID, process type (e.g., 'sequential', 'parallel'), boolean flag for memory usage (true/false), count of tasks, count of agents. All non-personal.                                                                                                                           |
| Yes       | Agent Data                               | Includes: randomly generated key and ID, role name (should not include personal info), boolean settings (verbose, delegation enabled, code execution allowed), max iterations, max RPM, max retry limit, LLM info (see LLM Attributes), list of tool names (should not include personal info). No personal data. |
| Yes       | Task Metadata                            | Includes: randomly generated key and ID, boolean execution settings (async\_execution, human\_input), associated agent's role and key, list of tool names. All non-personal.                                                                                                                                     |
| Yes       | Tool Usage Statistics                    | Includes: tool name (should not include personal info), number of usage attempts (integer), LLM attributes used. No personal data.                                                                                                                                                                               |
| Yes       | Test Execution Data                      | Includes: crew's randomly generated key and ID, number of iterations, model name used, quality score (float), execution time (in seconds). All non-personal.                                                                                                                                                     |
| Yes       | Task Lifecycle Data                      | Includes: creation and execution start/end times, crew and task identifiers. Stored as spans with timestamps. No personal data.                                                                                                                                                                                  |
| Yes       | LLM Attributes                           | Includes: name, model\_name, model, top\_k, temperature, and class name of the LLM. All technical, non-personal data.                                                                                                                                                                                            |
| Yes       | Crew Deployment attempt using crewAI CLI | Includes: The fact a deploy is being made and crew id, and if it's trying to pull logs, no other data.                                                                                                                                                                                                           |
| No        | Agent's Expanded Data                    | Includes: goal description, backstory text, i18n prompt file identifier. Users should ensure no personal info is included in text fields.                                                                                                                                                                        |
| No        | Detailed Task Information                | Includes: task description, expected output description, context references. Users should ensure no personal info is included in these fields.                                                                                                                                                                   |
| No        | Environment Information                  | Includes: platform, release, system, version, and CPU count. Example: 'Windows 10', 'x86\_64'. No personal data.                                                                                                                                                                                                 |
| No        | Crew and Task Inputs and Outputs         | Includes: input parameters and output results as non-identifiable data. Users should ensure no personal info is included.                                                                                                                                                                                        |
| No        | Comprehensive Crew Execution Data        | Includes: detailed logs of crew operations, all agents and tasks data, final output. All non-personal and technical in nature.                                                                                                                                                                                   |

<Note>
  "No" in the "Defaulted" column indicates that this data is only collected when `share_crew` is set to `true`.
</Note>

### Opt-In Further Telemetry Sharing

Users can choose to share their complete telemetry data by enabling the `share_crew` attribute to `True` in their crew configurations.
Enabling `share_crew` results in the collection of detailed crew and task execution data, including `goal`, `backstory`, `context`, and `output` of tasks.
This enables a deeper insight into usage patterns.

<Warning>
  If you enable `share_crew`, the collected data may include personal information if it has been incorporated into crew configurations, task descriptions, or outputs.
  Users should carefully review their data and ensure compliance with GDPR and other applicable privacy regulations before enabling this feature.
</Warning>

---

## Disable CrewAI telemetry only

**URL:** llms-txt#disable-crewai-telemetry-only

os.environ['CREWAI_DISABLE_TELEMETRY'] = 'true'

---

## Enable Crew Studio

**URL:** llms-txt#enable-crew-studio

**Contents:**
- What is Crew Studio?
- Configuration Steps
- Using Crew Studio
- Example Workflow

Source: https://docs.crewai.com/en/enterprise/guides/enable-crew-studio

Enabling Crew Studio on CrewAI AOP

<Tip>
  Crew Studio is a powerful **no-code/low-code** tool that allows you to quickly scaffold or build Crews through a conversational interface.
</Tip>

## What is Crew Studio?

Crew Studio is an innovative way to create AI agent crews without writing code.

<Frame>
  <img alt="Crew Studio Interface" />
</Frame>

With Crew Studio, you can:

* Chat with the Crew Assistant to describe your problem
* Automatically generate agents and tasks
* Select appropriate tools
* Configure necessary inputs
* Generate downloadable code for customization
* Deploy directly to the CrewAI AOP platform

## Configuration Steps

Before you can start using Crew Studio, you need to configure your LLM connections:

<Steps>
  <Step title="Set Up LLM Connection">
    Go to the **LLM Connections** tab in your CrewAI AOP dashboard and create a new LLM connection.

<Note>
      Feel free to use any LLM provider you want that is supported by CrewAI.
    </Note>

Configure your LLM connection:

* Enter a `Connection Name` (e.g., `OpenAI`)
    * Select your model provider: `openai` or `azure`
    * Select models you'd like to use in your Studio-generated Crews
      * We recommend at least `gpt-4o`, `o1-mini`, and `gpt-4o-mini`
    * Add your API key as an environment variable:
      * For OpenAI: Add `OPENAI_API_KEY` with your API key
      * For Azure OpenAI: Refer to [this article](https://blog.crewai.com/configuring-azure-openai-with-crewai-a-comprehensive-guide/) for configuration details
    * Click `Add Connection` to save your configuration

<Frame>
      <img alt="LLM Connection Configuration" />
    </Frame>
  </Step>

<Step title="Verify Connection Added">
    Once you complete the setup, you'll see your new connection added to the list of available connections.

<Frame>
      <img alt="Connection Added" />
    </Frame>
  </Step>

<Step title="Configure LLM Defaults">
    In the main menu, go to **Settings → Defaults** and configure the LLM Defaults settings:

* Select default models for agents and other components
    * Set default configurations for Crew Studio

Click `Save Settings` to apply your changes.

<Frame>
      <img alt="LLM Defaults Configuration" />
    </Frame>
  </Step>
</Steps>

Now that you've configured your LLM connection and default settings, you're ready to start using Crew Studio!

<Steps>
  <Step title="Access Studio">
    Navigate to the **Studio** section in your CrewAI AOP dashboard.
  </Step>

<Step title="Start a Conversation">
    Start a conversation with the Crew Assistant by describing the problem you want to solve:

The Crew Assistant will ask clarifying questions to better understand your requirements.
  </Step>

<Step title="Review Generated Crew">
    Review the generated crew configuration, including:

* Agents and their roles
    * Tasks to be performed
    * Required inputs
    * Tools to be used

This is your opportunity to refine the configuration before proceeding.
  </Step>

<Step title="Deploy or Download">
    Once you're satisfied with the configuration, you can:

* Download the generated code for local customization
    * Deploy the crew directly to the CrewAI AOP platform
    * Modify the configuration and regenerate the crew
  </Step>

<Step title="Test Your Crew">
    After deployment, test your crew with sample inputs to ensure it performs as expected.
  </Step>
</Steps>

<Tip>
  For best results, provide clear, detailed descriptions of what you want your crew to accomplish. Include specific inputs and expected outputs in your description.
</Tip>

Here's a typical workflow for creating a crew with Crew Studio:

<Steps>
  <Step title="Describe Your Problem">
    Start by describing your problem:

<Step title="Answer Questions">
    Respond to clarifying questions from the Crew Assistant to refine your requirements.
  </Step>

<Step title="Review the Plan">
    Review the generated crew plan, which might include:

* A Research Agent to gather financial news
    * An Analysis Agent to interpret the data
    * A Recommendations Agent to provide investment advice
  </Step>

<Step title="Approve or Modify">
    Approve the plan or request changes if necessary.
  </Step>

<Step title="Download or Deploy">
    Download the code for customization or deploy directly to the platform.
  </Step>

<Step title="Test and Refine">
    Test your crew with sample inputs and refine as needed.
  </Step>
</Steps>

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with Crew Studio or any other CrewAI AOP features.
</Card>

**Examples:**

Example 1 (unknown):
```unknown
The Crew Assistant will ask clarifying questions to better understand your requirements.
  </Step>

  <Step title="Review Generated Crew">
    Review the generated crew configuration, including:

    * Agents and their roles
    * Tasks to be performed
    * Required inputs
    * Tools to be used

    This is your opportunity to refine the configuration before proceeding.
  </Step>

  <Step title="Deploy or Download">
    Once you're satisfied with the configuration, you can:

    * Download the generated code for local customization
    * Deploy the crew directly to the CrewAI AOP platform
    * Modify the configuration and regenerate the crew
  </Step>

  <Step title="Test Your Crew">
    After deployment, test your crew with sample inputs to ensure it performs as expected.
  </Step>
</Steps>

<Tip>
  For best results, provide clear, detailed descriptions of what you want your crew to accomplish. Include specific inputs and expected outputs in your description.
</Tip>

## Example Workflow

Here's a typical workflow for creating a crew with Crew Studio:

<Steps>
  <Step title="Describe Your Problem">
    Start by describing your problem:
```

---

## Ensure only one CrewAI instance accesses storage

**URL:** llms-txt#ensure-only-one-crewai-instance-accesses-storage

import fcntl
import os

storage_path = db_storage_path()
lock_file = os.path.join(storage_path, ".crewai.lock")

with open(lock_file, 'w') as f:
    fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    # Your CrewAI code here
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
**Storage not persisting between runs:**
```

---

## Evaluating Use Cases for CrewAI

**URL:** llms-txt#evaluating-use-cases-for-crewai

**Contents:**
- Understanding the Decision Framework
- The Complexity-Precision Matrix Explained
  - What is Complexity?
  - What is Precision?
  - The Four Quadrants
- Choosing Between Crews and Flows
  - When to Choose Crews

Source: https://docs.crewai.com/en/guides/concepts/evaluating-use-cases

Learn how to assess your AI application needs and choose the right approach between Crews and Flows based on complexity and precision requirements.

## Understanding the Decision Framework

When building AI applications with CrewAI, one of the most important decisions you'll make is choosing the right approach for your specific use case. Should you use a Crew? A Flow? A combination of both? This guide will help you evaluate your requirements and make informed architectural decisions.

At the heart of this decision is understanding the relationship between **complexity** and **precision** in your application:

<Frame>
  <img alt="Complexity vs. Precision Matrix" />
</Frame>

This matrix helps visualize how different approaches align with varying requirements for complexity and precision. Let's explore what each quadrant means and how it guides your architectural choices.

## The Complexity-Precision Matrix Explained

### What is Complexity?

In the context of CrewAI applications, **complexity** refers to:

* The number of distinct steps or operations required
* The diversity of tasks that need to be performed
* The interdependencies between different components
* The need for conditional logic and branching
* The sophistication of the overall workflow

### What is Precision?

**Precision** in this context refers to:

* The accuracy required in the final output
* The need for structured, predictable results
* The importance of reproducibility
* The level of control needed over each step
* The tolerance for variation in outputs

### The Four Quadrants

#### 1. Low Complexity, Low Precision

* Simple, straightforward tasks
* Tolerance for some variation in outputs
* Limited number of steps
* Creative or exploratory applications

**Recommended Approach:** Simple Crews with minimal agents

**Example Use Cases:**

* Basic content generation
* Idea brainstorming
* Simple summarization tasks
* Creative writing assistance

#### 2. Low Complexity, High Precision

* Simple workflows that require exact, structured outputs
* Need for reproducible results
* Limited steps but high accuracy requirements
* Often involves data processing or transformation

**Recommended Approach:** Flows with direct LLM calls or simple Crews with structured outputs

**Example Use Cases:**

* Data extraction and transformation
* Form filling and validation
* Structured content generation (JSON, XML)
* Simple classification tasks

#### 3. High Complexity, Low Precision

* Multi-stage processes with many steps
* Creative or exploratory outputs
* Complex interactions between components
* Tolerance for variation in final results

**Recommended Approach:** Complex Crews with multiple specialized agents

**Example Use Cases:**

* Research and analysis
* Content creation pipelines
* Exploratory data analysis
* Creative problem-solving

#### 4. High Complexity, High Precision

* Complex workflows requiring structured outputs
* Multiple interdependent steps with strict accuracy requirements
* Need for both sophisticated processing and precise results
* Often mission-critical applications

**Recommended Approach:** Flows orchestrating multiple Crews with validation steps

**Example Use Cases:**

* Enterprise decision support systems
* Complex data processing pipelines
* Multi-stage document processing
* Regulated industry applications

## Choosing Between Crews and Flows

### When to Choose Crews

Crews are ideal when:

1. **You need collaborative intelligence** - Multiple agents with different specializations need to work together
2. **The problem requires emergent thinking** - The solution benefits from different perspectives and approaches
3. **The task is primarily creative or analytical** - The work involves research, content creation, or analysis
4. **You value adaptability over strict structure** - The workflow can benefit from agent autonomy
5. **The output format can be somewhat flexible** - Some variation in output structure is acceptable

```python theme={null}

---

## eval_crew.py

**URL:** llms-txt#eval_crew.py

**Contents:**
  - Key Features of Braintrust Integration
  - Version Compatibility Information
  - References

from braintrust import Eval
from autoevals import Levenshtein

def evaluate_crew_task(input_data):
    """Task function that wraps our crew for evaluation."""
    crew = create_crew()
    result = crew.kickoff(inputs={"topic": input_data["topic"]})
    return str(result)

Eval(
    "AI Research Crew",  # Project name
    {
        "data": lambda: [
            {"topic": "artificial intelligence trends 2024"},
            {"topic": "machine learning breakthroughs"},
            {"topic": "AI ethics and governance"},
        ],
        "task": evaluate_crew_task,
        "scores": [Levenshtein],
    },
)
bash theme={null}
export BRAINTRUST_API_KEY="YOUR_API_KEY"
braintrust eval eval_crew.py
```

See the [Braintrust Eval SDK guide](https://www.braintrust.dev/docs/start/eval-sdk) for more details.

### Key Features of Braintrust Integration

* **Comprehensive Tracing**: Track all agent interactions, tool usage, and LLM calls
* **Performance Monitoring**: Monitor execution times, token usage, and success rates
* **Experiment Tracking**: Compare different crew configurations and models
* **Automated Evaluation**: Set up custom evaluation metrics for crew outputs
* **Error Tracking**: Monitor and debug failures across your crew executions
* **Cost Analysis**: Track token usage and associated costs

### Version Compatibility Information

* Python 3.8+
* CrewAI >= 0.86.0
* Braintrust >= 0.1.0
* OpenTelemetry SDK >= 1.31.0

* [Braintrust Documentation](https://www.braintrust.dev/docs) - Overview of the Braintrust platform
* [Braintrust CrewAI Integration](https://www.braintrust.dev/docs/integrations/crew-ai) - Official CrewAI integration guide
* [Braintrust Eval SDK](https://www.braintrust.dev/docs/start/eval-sdk) - Run experiments via the SDK
* [CrewAI Documentation](https://docs.crewai.com/) - Overview of the CrewAI framework
* [OpenTelemetry Docs](https://opentelemetry.io/docs/) - OpenTelemetry guide
* [Braintrust GitHub](https://github.com/braintrustdata/braintrust) - Source code for Braintrust SDK

**Examples:**

Example 1 (unknown):
```unknown
Setup your API key and run:
```

---

## Example: Content Production Pipeline combining Crews and Flows

**URL:** llms-txt#example:-content-production-pipeline-combining-crews-and-flows

from crewai.flow.flow import Flow, listen, start
from crewai import Agent, Crew, Process, Task
from pydantic import BaseModel
from typing import List, Dict

class ContentState(BaseModel):
    topic: str = ""
    target_audience: str = ""
    content_type: str = ""
    outline: Dict = {}
    draft_content: str = ""
    final_content: str = ""
    seo_score: int = 0

class ContentProductionFlow(Flow[ContentState]):
    @start()
    def initialize_project(self):
        # Set initial parameters
        self.state.topic = "Sustainable Investing"
        self.state.target_audience = "Millennial Investors"
        self.state.content_type = "Blog Post"
        return "Project initialized"

@listen(initialize_project)
    def create_outline(self, _):
        # Use a research crew to create an outline
        researcher = Agent(
            role="Content Researcher",
            goal=f"Research {self.state.topic} for {self.state.target_audience}",
            backstory="You are an expert researcher with deep knowledge of content creation."
        )

outliner = Agent(
            role="Content Strategist",
            goal=f"Create an engaging outline for a {self.state.content_type}",
            backstory="You excel at structuring content for maximum engagement."
        )

research_task = Task(
            description=f"Research {self.state.topic} focusing on what would interest {self.state.target_audience}",
            expected_output="Comprehensive research notes with key points and statistics",
            agent=researcher
        )

outline_task = Task(
            description=f"Create an outline for a {self.state.content_type} about {self.state.topic}",
            expected_output="Detailed content outline with sections and key points",
            agent=outliner,
            context=[research_task]
        )

outline_crew = Crew(
            agents=[researcher, outliner],
            tasks=[research_task, outline_task],
            process=Process.sequential,
            verbose=True
        )

# Run the crew and store the result
        result = outline_crew.kickoff()

# Parse the outline (in a real app, you might use a more robust parsing approach)
        import json
        try:
            self.state.outline = json.loads(result.raw)
        except:
            # Fallback if not valid JSON
            self.state.outline = {"sections": result.raw}

return "Outline created"

@listen(create_outline)
    def write_content(self, _):
        # Use a writing crew to create the content
        writer = Agent(
            role="Content Writer",
            goal=f"Write engaging content for {self.state.target_audience}",
            backstory="You are a skilled writer who creates compelling content."
        )

editor = Agent(
            role="Content Editor",
            goal="Ensure content is polished, accurate, and engaging",
            backstory="You have a keen eye for detail and a talent for improving content."
        )

writing_task = Task(
            description=f"Write a {self.state.content_type} about {self.state.topic} following this outline: {self.state.outline}",
            expected_output="Complete draft content in markdown format",
            agent=writer
        )

editing_task = Task(
            description="Edit and improve the draft content for clarity, engagement, and accuracy",
            expected_output="Polished final content in markdown format",
            agent=editor,
            context=[writing_task]
        )

writing_crew = Crew(
            agents=[writer, editor],
            tasks=[writing_task, editing_task],
            process=Process.sequential,
            verbose=True
        )

# Run the crew and store the result
        result = writing_crew.kickoff()
        self.state.final_content = result.raw

return "Content created"

@listen(write_content)
    def optimize_for_seo(self, _):
        # Use a direct LLM call for SEO optimization
        from crewai import LLM
        llm = LLM(model="openai/gpt-4o-mini")

prompt = f"""
        Analyze this content for SEO effectiveness for the keyword "{self.state.topic}".
        Rate it on a scale of 1-100 and provide 3 specific recommendations for improvement.

Content: {self.state.final_content[:1000]}... (truncated for brevity)

Format your response as JSON with the following structure:
        {{
            "score": 85,
            "recommendations": [
                "Recommendation 1",
                "Recommendation 2",
                "Recommendation 3"
            ]
        }}
        """

seo_analysis = llm.call(prompt)

# Parse the SEO analysis
        import json
        try:
            analysis = json.loads(seo_analysis)
            self.state.seo_score = analysis.get("score", 0)
            return analysis
        except:
            self.state.seo_score = 50
            return {"score": 50, "recommendations": ["Unable to parse SEO analysis"]}

---

## Example: Creating a crew with a hierarchical process

**URL:** llms-txt#example:-creating-a-crew-with-a-hierarchical-process

---

## Example: Research Crew for market analysis

**URL:** llms-txt#example:-research-crew-for-market-analysis

from crewai import Agent, Crew, Process, Task

---

## Execute the crew

**URL:** llms-txt#execute-the-crew

result = report_crew.kickoff()

---

## Execute your crew

**URL:** llms-txt#execute-your-crew

**Contents:**
  - Step 4: Enable Tracing in Your Flow

result = crew.kickoff()
python theme={null}
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

class ExampleState(BaseModel):
    counter: int = 0
    message: str = ""

class ExampleFlow(Flow[ExampleState]):
    def __init__(self):
        super().__init__(tracing=True)  # Enable tracing for the flow

@start()
    def first_method(self):
        print("Starting the flow")
        self.state.counter = 1
        self.state.message = "Flow started"
        return "continue"

@listen("continue")
    def second_method(self):
        print("Continuing the flow")
        self.state.counter += 1
        self.state.message = "Flow continued"
        return "finish"

@listen("finish")
    def final_method(self):
        print("Finishing the flow")
        self.state.counter += 1
        self.state.message = "Flow completed"

**Examples:**

Example 1 (unknown):
```unknown
### Step 4: Enable Tracing in Your Flow

Similarly, you can enable tracing for CrewAI Flows:
```

---

## Flows

**URL:** llms-txt#flows

**Contents:**
- Overview
- Getting Started
  - @start()
  - @listen()
  - Flow Output
- Flow State Management
  - Unstructured State Management
  - Structured State Management
  - Choosing Between Unstructured and Structured State Management
- Flow Persistence

Source: https://docs.crewai.com/en/concepts/flows

Learn how to create and manage AI workflows using CrewAI Flows.

CrewAI Flows is a powerful feature designed to streamline the creation and management of AI workflows. Flows allow developers to combine and coordinate coding tasks and Crews efficiently, providing a robust framework for building sophisticated AI automations.

Flows allow you to create structured, event-driven workflows. They provide a seamless way to connect multiple tasks, manage state, and control the flow of execution in your AI applications. With Flows, you can easily design and implement multi-step processes that leverage the full potential of CrewAI's capabilities.

1. **Simplified Workflow Creation**: Easily chain together multiple Crews and tasks to create complex AI workflows.

2. **State Management**: Flows make it super easy to manage and share state between different tasks in your workflow.

3. **Event-Driven Architecture**: Built on an event-driven model, allowing for dynamic and responsive workflows.

4. **Flexible Control Flow**: Implement conditional logic, loops, and branching within your workflows.

Let's create a simple Flow where you will use OpenAI to generate a random city in one task and then use that city to generate a fun fact in another task.

<img alt="Flow Visual image" />

In the above example, we have created a simple Flow that generates a random city using OpenAI and then generates a fun fact about that city. The Flow consists of two tasks: `generate_city` and `generate_fun_fact`. The `generate_city` task is the starting point of the Flow, and the `generate_fun_fact` task listens for the output of the `generate_city` task.

Each Flow instance automatically receives a unique identifier (UUID) in its state, which helps track and manage flow executions. The state can also store additional data (like the generated city and fun fact) that persists throughout the flow's execution.

When you run the Flow, it will:

1. Generate a unique ID for the flow state
2. Generate a random city and store it in the state
3. Generate a fun fact about that city and store it in the state
4. Print the results to the console

The state's unique ID and stored data can be useful for tracking flow executions and maintaining context between tasks.

**Note:** Ensure you have set up your `.env` file to store your `OPENAI_API_KEY`. This key is necessary for authenticating requests to the OpenAI API.

The `@start()` decorator marks entry points for a Flow. You can:

* Declare multiple unconditional starts: `@start()`
* Gate a start on a prior method or router label: `@start("method_or_label")`
* Provide a callable condition to control when a start should fire

All satisfied `@start()` methods will execute (often in parallel) when the Flow begins or resumes.

The `@listen()` decorator is used to mark a method as a listener for the output of another task in the Flow. The method decorated with `@listen()` will be executed when the specified task emits an output. The method can access the output of the task it is listening to as an argument.

The `@listen()` decorator can be used in several ways:

1. **Listening to a Method by Name**: You can pass the name of the method you want to listen to as a string. When that method completes, the listener method will be triggered.

2. **Listening to a Method Directly**: You can pass the method itself. When that method completes, the listener method will be triggered.

Accessing and handling the output of a Flow is essential for integrating your AI workflows into larger applications or systems. CrewAI Flows provide straightforward mechanisms to retrieve the final output, access intermediate results, and manage the overall state of your Flow.

#### Retrieving the Final Output

When you run a Flow, the final output is determined by the last method that completes. The `kickoff()` method returns the output of this final method.

Here's how you can access the final output:

<img alt="Flow Visual image" />

In this example, the `second_method` is the last method to complete, so its output will be the final output of the Flow.
The `kickoff()` method will return the final output, which is then printed to the console. The `plot()` method will generate the HTML file, which will help you understand the flow.

#### Accessing and Updating State

In addition to retrieving the final output, you can also access and update the state within your Flow. The state can be used to store and share data between different methods in the Flow. After the Flow has run, you can access the state to retrieve any information that was added or updated during the execution.

Here's an example of how to update and access the state:

<img alt="Flow Visual image" />

In this example, the state is updated by both `first_method` and `second_method`.
After the Flow has run, you can access the final state to see the updates made by these methods.

By ensuring that the final method's output is returned and providing access to the state, CrewAI Flows make it easy to integrate the results of your AI workflows into larger applications or systems,
while also maintaining and accessing the state throughout the Flow's execution.

## Flow State Management

Managing state effectively is crucial for building reliable and maintainable AI workflows. CrewAI Flows provides robust mechanisms for both unstructured and structured state management,
allowing developers to choose the approach that best fits their application's needs.

### Unstructured State Management

In unstructured state management, all state is stored in the `state` attribute of the `Flow` class.
This approach offers flexibility, enabling developers to add or modify state attributes on the fly without defining a strict schema.
Even with unstructured states, CrewAI Flows automatically generates and maintains a unique identifier (UUID) for each state instance.

<img alt="Flow Visual image" />

**Note:** The `id` field is automatically generated and preserved throughout the flow's execution. You don't need to manage or set it manually, and it will be maintained even when updating the state with new data.

* **Flexibility:** You can dynamically add attributes to `self.state` without predefined constraints.
* **Simplicity:** Ideal for straightforward workflows where state structure is minimal or varies significantly.

### Structured State Management

Structured state management leverages predefined schemas to ensure consistency and type safety across the workflow.
By using models like Pydantic's `BaseModel`, developers can define the exact shape of the state, enabling better validation and auto-completion in development environments.

Each state in CrewAI Flows automatically receives a unique identifier (UUID) to help track and manage state instances. This ID is automatically generated and managed by the Flow system.

<img alt="Flow Visual image" />

* **Defined Schema:** `ExampleState` clearly outlines the state structure, enhancing code readability and maintainability.
* **Type Safety:** Leveraging Pydantic ensures that state attributes adhere to the specified types, reducing runtime errors.
* **Auto-Completion:** IDEs can provide better auto-completion and error checking based on the defined state model.

### Choosing Between Unstructured and Structured State Management

* **Use Unstructured State Management when:**

* The workflow's state is simple or highly dynamic.
  * Flexibility is prioritized over strict state definitions.
  * Rapid prototyping is required without the overhead of defining schemas.

* **Use Structured State Management when:**
  * The workflow requires a well-defined and consistent state structure.
  * Type safety and validation are important for your application's reliability.
  * You want to leverage IDE features like auto-completion and type checking for better developer experience.

By providing both unstructured and structured state management options, CrewAI Flows empowers developers to build AI workflows that are both flexible and robust, catering to a wide range of application requirements.

The @persist decorator enables automatic state persistence in CrewAI Flows, allowing you to maintain flow state across restarts or different workflow executions. This decorator can be applied at either the class level or method level, providing flexibility in how you manage state persistence.

### Class-Level Persistence

When applied at the class level, the @persist decorator automatically persists all flow method states:

### Method-Level Persistence

For more granular control, you can apply @persist to specific methods:

1. **Unique State Identification**
   * Each flow state automatically receives a unique UUID
   * The ID is preserved across state updates and method calls
   * Supports both structured (Pydantic BaseModel) and unstructured (dictionary) states

2. **Default SQLite Backend**
   * SQLiteFlowPersistence is the default storage backend
   * States are automatically saved to a local SQLite database
   * Robust error handling ensures clear messages if database operations fail

3. **Error Handling**
   * Comprehensive error messages for database operations
   * Automatic state validation during save and load
   * Clear feedback when persistence operations encounter issues

### Important Considerations

* **State Types**: Both structured (Pydantic BaseModel) and unstructured (dictionary) states are supported
* **Automatic ID**: The `id` field is automatically added if not present
* **State Recovery**: Failed or restarted flows can automatically reload their previous state
* **Custom Implementation**: You can provide your own FlowPersistence implementation for specialized storage needs

### Technical Advantages

1. **Precise Control Through Low-Level Access**
   * Direct access to persistence operations for advanced use cases
   * Fine-grained control via method-level persistence decorators
   * Built-in state inspection and debugging capabilities
   * Full visibility into state changes and persistence operations

2. **Enhanced Reliability**
   * Automatic state recovery after system failures or restarts
   * Transaction-based state updates for data integrity
   * Comprehensive error handling with clear error messages
   * Robust validation during state save and load operations

3. **Extensible Architecture**
   * Customizable persistence backend through FlowPersistence interface
   * Support for specialized storage solutions beyond SQLite
   * Compatible with both structured (Pydantic) and unstructured (dict) states
   * Seamless integration with existing CrewAI flow patterns

The persistence system's architecture emphasizes technical precision and customization options, allowing developers to maintain full control over state management while benefiting from built-in reliability features.

### Conditional Logic: `or`

The `or_` function in Flows allows you to listen to multiple methods and trigger the listener method when any of the specified methods emit an output.

<img alt="Flow Visual image" />

When you run this Flow, the `logger` method will be triggered by the output of either the `start_method` or the `second_method`.
The `or_` function is used to listen to multiple methods and trigger the listener method when any of the specified methods emit an output.

### Conditional Logic: `and`

The `and_` function in Flows allows you to listen to multiple methods and trigger the listener method only when all the specified methods emit an output.

<img alt="Flow Visual image" />

When you run this Flow, the `logger` method will be triggered only when both the `start_method` and the `second_method` emit an output.
The `and_` function is used to listen to multiple methods and trigger the listener method only when all the specified methods emit an output.

The `@router()` decorator in Flows allows you to define conditional routing logic based on the output of a method.
You can specify different routes based on the output of the method, allowing you to control the flow of execution dynamically.

<img alt="Flow Visual image" />

In the above example, the `start_method` generates a random boolean value and sets it in the state.
The `second_method` uses the `@router()` decorator to define conditional routing logic based on the value of the boolean.
If the boolean is `True`, the method returns `"success"`, and if it is `False`, the method returns `"failed"`.
The `third_method` and `fourth_method` listen to the output of the `second_method` and execute based on the returned value.

When you run this Flow, the output will change based on the random boolean value generated by the `start_method`.

### Human in the Loop (human feedback)

The `@human_feedback` decorator enables human-in-the-loop workflows by pausing flow execution to collect feedback from a human. This is useful for approval gates, quality review, and decision points that require human judgment.

When `emit` is specified, the human's free-form feedback is interpreted by an LLM and collapsed into one of the specified outcomes, which then triggers the corresponding `@listen` decorator.

You can also use `@human_feedback` without routing to simply collect feedback:

Access all feedback collected during a flow via `self.last_human_feedback` (most recent) or `self.human_feedback_history` (all feedback as a list).

For a complete guide on human feedback in flows, including **async/non-blocking feedback** with custom providers (Slack, webhooks, etc.), see [Human Feedback in Flows](/en/learn/human-feedback-in-flows).

## Adding Agents to Flows

Agents can be seamlessly integrated into your flows, providing a lightweight alternative to full Crews when you need simpler, focused task execution. Here's an example of how to use an Agent within a flow to perform market research:

```python theme={null}
import asyncio
from typing import Any, Dict, List

from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field

from crewai.agent import Agent
from crewai.flow.flow import Flow, listen, start

**Examples:**

Example 1 (unknown):
```unknown
<img alt="Flow Visual image" />

In the above example, we have created a simple Flow that generates a random city using OpenAI and then generates a fun fact about that city. The Flow consists of two tasks: `generate_city` and `generate_fun_fact`. The `generate_city` task is the starting point of the Flow, and the `generate_fun_fact` task listens for the output of the `generate_city` task.

Each Flow instance automatically receives a unique identifier (UUID) in its state, which helps track and manage flow executions. The state can also store additional data (like the generated city and fun fact) that persists throughout the flow's execution.

When you run the Flow, it will:

1. Generate a unique ID for the flow state
2. Generate a random city and store it in the state
3. Generate a fun fact about that city and store it in the state
4. Print the results to the console

The state's unique ID and stored data can be useful for tracking flow executions and maintaining context between tasks.

**Note:** Ensure you have set up your `.env` file to store your `OPENAI_API_KEY`. This key is necessary for authenticating requests to the OpenAI API.

### @start()

The `@start()` decorator marks entry points for a Flow. You can:

* Declare multiple unconditional starts: `@start()`
* Gate a start on a prior method or router label: `@start("method_or_label")`
* Provide a callable condition to control when a start should fire

All satisfied `@start()` methods will execute (often in parallel) when the Flow begins or resumes.

### @listen()

The `@listen()` decorator is used to mark a method as a listener for the output of another task in the Flow. The method decorated with `@listen()` will be executed when the specified task emits an output. The method can access the output of the task it is listening to as an argument.

#### Usage

The `@listen()` decorator can be used in several ways:

1. **Listening to a Method by Name**: You can pass the name of the method you want to listen to as a string. When that method completes, the listener method will be triggered.
```

Example 2 (unknown):
```unknown
2. **Listening to a Method Directly**: You can pass the method itself. When that method completes, the listener method will be triggered.
```

Example 3 (unknown):
```unknown
### Flow Output

Accessing and handling the output of a Flow is essential for integrating your AI workflows into larger applications or systems. CrewAI Flows provide straightforward mechanisms to retrieve the final output, access intermediate results, and manage the overall state of your Flow.

#### Retrieving the Final Output

When you run a Flow, the final output is determined by the last method that completes. The `kickoff()` method returns the output of this final method.

Here's how you can access the final output:

<CodeGroup>
```

Example 4 (unknown):
```unknown

```

---

## Gmail Trigger

**URL:** llms-txt#gmail-trigger

**Contents:**
- Overview
- Enabling the Gmail Trigger
- Example: Process new emails
  - Testing Locally

Source: https://docs.crewai.com/en/enterprise/guides/gmail-trigger

Trigger automations when Gmail events occur (e.g., new emails, labels).

Use the Gmail Trigger to kick off your deployed crews when Gmail events happen in connected accounts, such as receiving a new email or messages matching a label/filter.

<Tip>
  Make sure Gmail is connected in Tools & Integrations and the trigger is enabled for your deployment.
</Tip>

## Enabling the Gmail Trigger

1. Open your deployment in CrewAI AOP
2. Go to the **Triggers** tab
3. Locate **Gmail** and switch the toggle to enable

<Frame>
  <img alt="Enable or disable triggers with toggle" />
</Frame>

## Example: Process new emails

When a new email arrives, the Gmail Trigger will send the payload to your Crew or Flow. Below is a Crew example that parses and processes the trigger payload.

The Gmail payload will be available via the standard context mechanisms.

Test your Gmail trigger integration locally using the CrewAI CLI:

**Examples:**

Example 1 (unknown):
```unknown
The Gmail payload will be available via the standard context mechanisms.

### Testing Locally

Test your Gmail trigger integration locally using the CrewAI CLI:
```

---

## Google Calendar Trigger

**URL:** llms-txt#google-calendar-trigger

**Contents:**
- Overview
- Enabling the Google Calendar Trigger
- Example: Summarize meeting details
- Testing Locally

Source: https://docs.crewai.com/en/enterprise/guides/google-calendar-trigger

Kick off crews when Google Calendar events are created, updated, or cancelled

Use the Google Calendar trigger to launch automations whenever calendar events change. Common use cases include briefing a team before a meeting, notifying stakeholders when a critical event is cancelled, or summarizing daily schedules.

<Tip>
  Make sure Google Calendar is connected in **Tools & Integrations** and enabled for the deployment you want to automate.
</Tip>

## Enabling the Google Calendar Trigger

1. Open your deployment in CrewAI AOP
2. Go to the **Triggers** tab
3. Locate **Google Calendar** and switch the toggle to enable

<Frame>
  <img alt="Enable or disable triggers with toggle" />
</Frame>

## Example: Summarize meeting details

The snippet below mirrors the `calendar-event-crew.py` example in the trigger repository. It parses the payload, analyses the attendees and timing, and produces a meeting brief for downstream tools.

Use `crewai_trigger_payload` exactly as it is delivered by the trigger so the crew can extract the proper fields.

Test your Google Calendar trigger integration locally using the CrewAI CLI:

**Examples:**

Example 1 (unknown):
```unknown
Use `crewai_trigger_payload` exactly as it is delivered by the trigger so the crew can extract the proper fields.

## Testing Locally

Test your Google Calendar trigger integration locally using the CrewAI CLI:
```

---

## Google Drive Trigger

**URL:** llms-txt#google-drive-trigger

**Contents:**
- Overview
- Enabling the Google Drive Trigger
- Example: Summarize file activity
- Testing Locally

Source: https://docs.crewai.com/en/enterprise/guides/google-drive-trigger

Respond to Google Drive file events with automated crews

Trigger your automations when files are created, updated, or removed in Google Drive. Typical workflows include summarizing newly uploaded content, enforcing sharing policies, or notifying owners when critical files change.

<Tip>
  Connect Google Drive in **Tools & Integrations** and confirm the trigger is enabled for the automation you want to monitor.
</Tip>

## Enabling the Google Drive Trigger

1. Open your deployment in CrewAI AOP
2. Go to the **Triggers** tab
3. Locate **Google Drive** and switch the toggle to enable

<Frame>
  <img alt="Enable or disable triggers with toggle" />
</Frame>

## Example: Summarize file activity

The drive example crews parse the payload to extract file metadata, evaluate permissions, and publish a summary.

Test your Google Drive trigger integration locally using the CrewAI CLI:

**Examples:**

Example 1 (unknown):
```unknown
## Testing Locally

Test your Google Drive trigger integration locally using the CrewAI CLI:
```

---

## HubSpot Trigger

**URL:** llms-txt#hubspot-trigger

**Contents:**
- Prerequisites
- Setup Steps

Source: https://docs.crewai.com/en/enterprise/guides/hubspot-trigger

Trigger CrewAI crews directly from HubSpot Workflows

This guide provides a step-by-step process to set up HubSpot triggers for CrewAI AOP, enabling you to initiate crews directly from HubSpot Workflows.

* A CrewAI AOP account
* A HubSpot account with the [HubSpot Workflows](https://knowledge.hubspot.com/workflows/create-workflows) feature

<Steps>
  <Step title="Connect your HubSpot account with CrewAI AOP">
    * Log in to your `CrewAI AOP account > Triggers`
    * Select `HubSpot` from the list of available triggers
    * Choose the HubSpot account you want to connect with CrewAI AOP
    * Follow the on-screen prompts to authorize CrewAI AOP access to your HubSpot account
    * A confirmation message will appear once HubSpot is successfully connected with CrewAI AOP
  </Step>

<Step title="Create a HubSpot Workflow">
    * Log in to your `HubSpot account > Automations > Workflows > New workflow`
    * Select the workflow type that fits your needs (e.g., Start from scratch)
    * In the workflow builder, click the Plus (+) icon to add a new action.
    * Choose `Integrated apps > CrewAI > Kickoff a Crew`.
    * Select the Crew you want to initiate.
    * Click `Save` to add the action to your workflow

<Frame>
      <img alt="HubSpot Workflow 1" />
    </Frame>
  </Step>

<Step title="Use Crew results with other actions">
    * After the Kickoff a Crew step, click the Plus (+) icon to add a new action.
    * For example, to send an internal email notification, choose `Communications > Send internal email notification`
    * In the Body field, click `Insert data`, select `View properties or action outputs from > Action outputs > Crew Result` to include Crew data in the email
      <Frame>
        <img alt="HubSpot Workflow 2" />
      </Frame>
    * Configure any additional actions as needed
    * Review your workflow steps to ensure everything is set up correctly
    * Activate the workflow
      <Frame>
        <img alt="HubSpot Workflow 3" />
      </Frame>
  </Step>
</Steps>

For more detailed information on available actions and customization options, refer to the [HubSpot Workflows Documentation](https://knowledge.hubspot.com/workflows/create-workflows).

---

## Importing crewAI tools

**URL:** llms-txt#importing-crewai-tools

from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    SerperDevTool,
    WebsiteSearchTool
)

---

## Initialize LangDB before any CrewAI imports

**URL:** llms-txt#initialize-langdb-before-any-crewai-imports

def create_llm(model):
    return LLM(
        model=model,
        api_key=os.environ.get("LANGDB_API_KEY"),
        base_url=os.environ.get("LANGDB_API_BASE_URL"),
        extra_headers={"x-project-id": os.environ.get("LANGDB_PROJECT_ID")}
    )

---

## Instrument CrewAI with just one line

**URL:** llms-txt#instrument-crewai-with-just-one-line

**Contents:**
  - 4. Create and run your CrewAI application as usual

instrument_crewai(Maxim().logger())
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### 4. Create and run your CrewAI application as usual
```

---

## Integrate Datadog with CrewAI

**URL:** llms-txt#integrate-datadog-with-crewai

**Contents:**
- What is Datadog LLM Observability?
- Getting Started
  - Install Dependencies
  - Set Environment Variables
  - Create a CrewAI Agent Application

This guide will demonstrate how to integrate **[Datadog LLM Observability](https://docs.datadoghq.com/llm_observability/)** with **CrewAI** using [Datadog auto-instrumentation](https://docs.datadoghq.com/llm_observability/instrumentation/auto_instrumentation?tab=python). By the end of this guide, you will be able to submit LLM Observability traces to Datadog and view your CrewAI agent runs in Datadog LLM Observability's [Agentic Execution View](https://docs.datadoghq.com/llm_observability/monitoring/agent_monitoring).

## What is Datadog LLM Observability?

[Datadog LLM Observability](https://www.datadoghq.com/product/llm-observability/) helps AI engineers, data scientists, and application developers quickly develop, evaluate, and monitor LLM applications. Confidently improve output quality, performance, costs, and overall risk with structured experiments, end-to-end tracing across AI agents, and evaluations.

### Install Dependencies

### Set Environment Variables

If you do not have a Datadog API key, you can [create an account](https://www.datadoghq.com/) and [get your API key](https://docs.datadoghq.com/account_management/api-app-keys/#api-keys).

You will also need to specify an ML Application name in the following environment variables. An ML Application is a grouping of LLM Observability traces associated with a specific LLM-based application. See [ML Application Naming Guidelines](https://docs.datadoghq.com/llm_observability/instrumentation/sdk?tab=python#application-naming-guidelines) for more information on limitations with ML Application names.

Additionally, configure any LLM provider API keys

### Create a CrewAI Agent Application

```python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### Set Environment Variables

If you do not have a Datadog API key, you can [create an account](https://www.datadoghq.com/) and [get your API key](https://docs.datadoghq.com/account_management/api-app-keys/#api-keys).

You will also need to specify an ML Application name in the following environment variables. An ML Application is a grouping of LLM Observability traces associated with a specific LLM-based application. See [ML Application Naming Guidelines](https://docs.datadoghq.com/llm_observability/instrumentation/sdk?tab=python#application-naming-guidelines) for more information on limitations with ML Application names.
```

Example 2 (unknown):
```unknown
Additionally, configure any LLM provider API keys
```

Example 3 (unknown):
```unknown
### Create a CrewAI Agent Application
```

---

## Integrate Langfuse with CrewAI

**URL:** llms-txt#integrate-langfuse-with-crewai

**Contents:**
- Get Started
  - Step 1: Install Dependencies
  - Step 2: Set Up Environment Variables

This notebook demonstrates how to integrate **Langfuse** with **CrewAI** using OpenTelemetry via the **OpenLit** SDK. By the end of this notebook, you will be able to trace your CrewAI applications with Langfuse for improved observability and debugging.

> **What is Langfuse?** [Langfuse](https://langfuse.com) is an open-source LLM engineering platform. It provides tracing and monitoring capabilities for LLM applications, helping developers debug, analyze, and optimize their AI systems. Langfuse integrates with various tools and frameworks via native integrations, OpenTelemetry, and APIs/SDKs.

[![Langfuse Overview Video](https://github.com/user-attachments/assets/3926b288-ff61-4b95-8aa1-45d041c70866)](https://langfuse.com/watch-demo)

We'll walk through a simple example of using CrewAI and integrating it with Langfuse via OpenTelemetry using OpenLit.

### Step 1: Install Dependencies

### Step 2: Set Up Environment Variables

Set your Langfuse API keys and configure OpenTelemetry export settings to send traces to Langfuse. Please refer to the [Langfuse OpenTelemetry Docs](https://langfuse.com/docs/opentelemetry/get-started) for more information on the Langfuse OpenTelemetry endpoint `/api/public/otel` and authentication.

```python theme={null}
import os

**Examples:**

Example 1 (unknown):
```unknown
### Step 2: Set Up Environment Variables

Set your Langfuse API keys and configure OpenTelemetry export settings to send traces to Langfuse. Please refer to the [Langfuse OpenTelemetry Docs](https://langfuse.com/docs/opentelemetry/get-started) for more information on the Langfuse OpenTelemetry endpoint `/api/public/otel` and authentication.
```

---

## In standard Crew

**URL:** llms-txt#in-standard-crew

agent = Agent(role="researcher", tools=[async_custom_tool])

---

## In your crew.py file

**URL:** llms-txt#in-your-crew.py-file

from crewai import Agent, Crew, Task
from my_listeners import MyCustomListener

---

## In your crew.py or flow.py file

**URL:** llms-txt#in-your-crew.py-or-flow.py-file

**Contents:**
- Available Event Types
  - Crew Events
  - Agent Events
  - Task Events
  - Tool Usage Events
  - Knowledge Events
  - LLM Guardrail Events
  - Flow Events
  - LLM Events
  - Memory Events

import my_project.listeners  # This loads all your listeners

class MyCustomCrew:
    # Your crew implementation...
python theme={null}
from crewai.events import crewai_event_bus, CrewKickoffStartedEvent

with crewai_event_bus.scoped_handlers():
    @crewai_event_bus.on(CrewKickoffStartedEvent)
    def temp_handler(source, event):
        print("This handler only exists within this context")

# Do something that emits events

**Examples:**

Example 1 (unknown):
```unknown
This is how third-party event listeners are registered in the CrewAI codebase.

## Available Event Types

CrewAI provides a wide range of events that you can listen for:

### Crew Events

* **CrewKickoffStartedEvent**: Emitted when a Crew starts execution
* **CrewKickoffCompletedEvent**: Emitted when a Crew completes execution
* **CrewKickoffFailedEvent**: Emitted when a Crew fails to complete execution
* **CrewTestStartedEvent**: Emitted when a Crew starts testing
* **CrewTestCompletedEvent**: Emitted when a Crew completes testing
* **CrewTestFailedEvent**: Emitted when a Crew fails to complete testing
* **CrewTrainStartedEvent**: Emitted when a Crew starts training
* **CrewTrainCompletedEvent**: Emitted when a Crew completes training
* **CrewTrainFailedEvent**: Emitted when a Crew fails to complete training

### Agent Events

* **AgentExecutionStartedEvent**: Emitted when an Agent starts executing a task
* **AgentExecutionCompletedEvent**: Emitted when an Agent completes executing a task
* **AgentExecutionErrorEvent**: Emitted when an Agent encounters an error during execution

### Task Events

* **TaskStartedEvent**: Emitted when a Task starts execution
* **TaskCompletedEvent**: Emitted when a Task completes execution
* **TaskFailedEvent**: Emitted when a Task fails to complete execution
* **TaskEvaluationEvent**: Emitted when a Task is evaluated

### Tool Usage Events

* **ToolUsageStartedEvent**: Emitted when a tool execution is started
* **ToolUsageFinishedEvent**: Emitted when a tool execution is completed
* **ToolUsageErrorEvent**: Emitted when a tool execution encounters an error
* **ToolValidateInputErrorEvent**: Emitted when a tool input validation encounters an error
* **ToolExecutionErrorEvent**: Emitted when a tool execution encounters an error
* **ToolSelectionErrorEvent**: Emitted when there's an error selecting a tool

### Knowledge Events

* **KnowledgeRetrievalStartedEvent**: Emitted when a knowledge retrieval is started
* **KnowledgeRetrievalCompletedEvent**: Emitted when a knowledge retrieval is completed
* **KnowledgeQueryStartedEvent**: Emitted when a knowledge query is started
* **KnowledgeQueryCompletedEvent**: Emitted when a knowledge query is completed
* **KnowledgeQueryFailedEvent**: Emitted when a knowledge query fails
* **KnowledgeSearchQueryFailedEvent**: Emitted when a knowledge search query fails

### LLM Guardrail Events

* **LLMGuardrailStartedEvent**: Emitted when a guardrail validation starts. Contains details about the guardrail being applied and retry count.
* **LLMGuardrailCompletedEvent**: Emitted when a guardrail validation completes. Contains details about validation success/failure, results, and error messages if any.

### Flow Events

* **FlowCreatedEvent**: Emitted when a Flow is created
* **FlowStartedEvent**: Emitted when a Flow starts execution
* **FlowFinishedEvent**: Emitted when a Flow completes execution
* **FlowPlotEvent**: Emitted when a Flow is plotted
* **MethodExecutionStartedEvent**: Emitted when a Flow method starts execution
* **MethodExecutionFinishedEvent**: Emitted when a Flow method completes execution
* **MethodExecutionFailedEvent**: Emitted when a Flow method fails to complete execution

### LLM Events

* **LLMCallStartedEvent**: Emitted when an LLM call starts
* **LLMCallCompletedEvent**: Emitted when an LLM call completes
* **LLMCallFailedEvent**: Emitted when an LLM call fails
* **LLMStreamChunkEvent**: Emitted for each chunk received during streaming LLM responses

### Memory Events

* **MemoryQueryStartedEvent**: Emitted when a memory query is started. Contains the query, limit, and optional score threshold.
* **MemoryQueryCompletedEvent**: Emitted when a memory query is completed successfully. Contains the query, results, limit, score threshold, and query execution time.
* **MemoryQueryFailedEvent**: Emitted when a memory query fails. Contains the query, limit, score threshold, and error message.
* **MemorySaveStartedEvent**: Emitted when a memory save operation is started. Contains the value to be saved, metadata, and optional agent role.
* **MemorySaveCompletedEvent**: Emitted when a memory save operation is completed successfully. Contains the saved value, metadata, agent role, and save execution time.
* **MemorySaveFailedEvent**: Emitted when a memory save operation fails. Contains the value, metadata, agent role, and error message.
* **MemoryRetrievalStartedEvent**: Emitted when memory retrieval for a task prompt starts. Contains the optional task ID.
* **MemoryRetrievalCompletedEvent**: Emitted when memory retrieval for a task prompt completes successfully. Contains the task ID, memory content, and retrieval execution time.

## Event Handler Structure

Each event handler receives two parameters:

1. **source**: The object that emitted the event
2. **event**: The event instance, containing event-specific data

The structure of the event object depends on the event type, but all events inherit from `BaseEvent` and include:

* **timestamp**: The time when the event was emitted
* **type**: A string identifier for the event type

Additional fields vary by event type. For example, `CrewKickoffCompletedEvent` includes `crew_name` and `output` fields.

## Advanced Usage: Scoped Handlers

For temporary event handling (useful for testing or specific operations), you can use the `scoped_handlers` context manager:
```

---

## Kickoff Crew

**URL:** llms-txt#kickoff-crew

**Contents:**
- Overview
- Method 1: Using the Web Interface
  - Step 1: Navigate to Your Deployed Crew
  - Step 2: Initiate Execution
  - Step 3: Monitor Execution Progress
  - Step 4: Check Execution Status
  - Step 5: View Final Results
- Method 2: Using the API
  - Authentication
  - Checking Crew Health

Source: https://docs.crewai.com/en/enterprise/guides/kickoff-crew

Kickoff a Crew on CrewAI AOP

Once you've deployed your crew to the CrewAI AOP platform, you can kickoff executions through the web interface or the API. This guide covers both approaches.

## Method 1: Using the Web Interface

### Step 1: Navigate to Your Deployed Crew

1. Log in to [CrewAI AOP](https://app.crewai.com)
2. Click on the crew name from your projects list
3. You'll be taken to the crew's detail page

<Frame>
  <img alt="Crew Dashboard" />
</Frame>

### Step 2: Initiate Execution

From your crew's detail page, you have two options to kickoff an execution:

#### Option A: Quick Kickoff

1. Click the `Kickoff` link in the Test Endpoints section
2. Enter the required input parameters for your crew in the JSON editor
3. Click the `Send Request` button

<Frame>
  <img alt="Kickoff Endpoint" />
</Frame>

#### Option B: Using the Visual Interface

1. Click the `Run` tab in the crew detail page
2. Enter the required inputs in the form fields
3. Click the `Run Crew` button

<Frame>
  <img alt="Run Crew" />
</Frame>

### Step 3: Monitor Execution Progress

After initiating the execution:

1. You'll receive a response containing a `kickoff_id` - **copy this ID**
2. This ID is essential for tracking your execution

<Frame>
  <img alt="Copy Task ID" />
</Frame>

### Step 4: Check Execution Status

To monitor the progress of your execution:

1. Click the "Status" endpoint in the Test Endpoints section
2. Paste the `kickoff_id` into the designated field
3. Click the "Get Status" button

<Frame>
  <img alt="Get Status" />
</Frame>

The status response will show:

* Current execution state (`running`, `completed`, etc.)
* Details about which tasks are in progress
* Any outputs produced so far

### Step 5: View Final Results

Once execution is complete:

1. The status will change to `completed`
2. You can view the full execution results and outputs
3. For a more detailed view, check the `Executions` tab in the crew detail page

## Method 2: Using the API

You can also kickoff crews programmatically using the CrewAI AOP REST API.

All API requests require a bearer token for authentication:

Your bearer token is available on the Status tab of your crew's detail page.

### Checking Crew Health

Before executing operations, you can verify that your crew is running properly:

A successful response will return a message indicating the crew is operational:

### Step 1: Retrieve Required Inputs

First, determine what inputs your crew requires:

The response will be a JSON object containing an array of required input parameters, for example:

This example shows that this particular crew requires two inputs: `topic` and `current_year`.

### Step 2: Kickoff Execution

Initiate execution by providing the required inputs:

The response will include a `kickoff_id` that you'll need for tracking:

### Step 3: Check Execution Status

Monitor the execution progress using the kickoff\_id:

## Handling Executions

### Long-Running Executions

For executions that may take a long time:

1. Consider implementing a polling mechanism to check status periodically
2. Use webhooks (if available) for notification when execution completes
3. Implement error handling for potential timeouts

### Execution Context

The execution context includes:

* Inputs provided at kickoff
* Environment variables configured during deployment
* Any state maintained between tasks

### Debugging Failed Executions

If an execution fails:

1. Check the "Executions" tab for detailed logs
2. Review the "Traces" tab for step-by-step execution details
3. Look for LLM responses and tool usage in the trace details

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with execution issues or questions about the Enterprise platform.
</Card>

**Examples:**

Example 1 (unknown):
```unknown
Your bearer token is available on the Status tab of your crew's detail page.

### Checking Crew Health

Before executing operations, you can verify that your crew is running properly:
```

Example 2 (unknown):
```unknown
A successful response will return a message indicating the crew is operational:
```

Example 3 (unknown):
```unknown
### Step 1: Retrieve Required Inputs

First, determine what inputs your crew requires:
```

Example 4 (unknown):
```unknown
The response will be a JSON object containing an array of required input parameters, for example:
```

---

## Kickoff Crew Asynchronously

**URL:** llms-txt#kickoff-crew-asynchronously

**Contents:**
- Introduction
- Native Async Execution with `akickoff()`
  - Method Signature
  - Parameters
  - Returns
  - Example: Native Async Crew Execution

Source: https://docs.crewai.com/en/learn/kickoff-async

Kickoff a Crew Asynchronously

CrewAI provides the ability to kickoff a crew asynchronously, allowing you to start the crew execution in a non-blocking manner.
This feature is particularly useful when you want to run multiple crews concurrently or when you need to perform other tasks while the crew is executing.

CrewAI offers two approaches for async execution:

| Method            | Type         | Description                                            |
| ----------------- | ------------ | ------------------------------------------------------ |
| `akickoff()`      | Native async | True async/await throughout the entire execution chain |
| `kickoff_async()` | Thread-based | Wraps synchronous execution in `asyncio.to_thread`     |

<Note>
  For high-concurrency workloads, `akickoff()` is recommended as it uses native async for task execution, memory operations, and knowledge retrieval.
</Note>

## Native Async Execution with `akickoff()`

The `akickoff()` method provides true native async execution, using async/await throughout the entire execution chain including task execution, memory operations, and knowledge queries.

* `inputs` (dict): A dictionary containing the input data required for the tasks.

* `CrewOutput`: An object representing the result of the crew execution.

### Example: Native Async Crew Execution

```python Code theme={null}
import asyncio
from crewai import Crew, Agent, Task

**Examples:**

Example 1 (unknown):
```unknown
### Parameters

* `inputs` (dict): A dictionary containing the input data required for the tasks.

### Returns

* `CrewOutput`: An object representing the result of the crew execution.

### Example: Native Async Crew Execution
```

---

## Kickoff Crew for Each

**URL:** llms-txt#kickoff-crew-for-each

**Contents:**
- Introduction
- Kicking Off a Crew for Each Item

Source: https://docs.crewai.com/en/learn/kickoff-for-each

Kickoff Crew for Each Item in a List

CrewAI provides the ability to kickoff a crew for each item in a list, allowing you to execute the crew for each item in the list.
This feature is particularly useful when you need to perform the same set of tasks for multiple items.

## Kicking Off a Crew for Each Item

To kickoff a crew for each item in a list, use the `kickoff_for_each()` method.
This method executes the crew for each item in the list, allowing you to process multiple items efficiently.

Here's an example of how to kickoff a crew for each item in a list:

```python Code theme={null}
from crewai import Crew, Agent, Task

---

## Kickoff the crew to execute the task

**URL:** llms-txt#kickoff-the-crew-to-execute-the-task

result = crew.kickoff()

---

## List all CrewAI storage directories

**URL:** llms-txt#list-all-crewai-storage-directories

**Contents:**
  - Controlling Storage Locations

if os.path.exists(storage_path):
    print("\nStored files and directories:")
    for item in os.listdir(storage_path):
        item_path = os.path.join(storage_path, item)
        if os.path.isdir(item_path):
            print(f"📁 {item}/")
            # Show ChromaDB collections
            if os.path.exists(item_path):
                for subitem in os.listdir(item_path):
                    print(f"   └── {subitem}")
        else:
            print(f"📄 {item}")
else:
    print("No CrewAI storage directory found yet.")
python theme={null}
import os
from crewai import Crew

**Examples:**

Example 1 (unknown):
```unknown
### Controlling Storage Locations

#### Option 1: Environment Variable (Recommended)
```

---

## Marketplace

**URL:** llms-txt#marketplace

**Contents:**
- Overview
- Discoverability
- Install & Enable
- Related

Source: https://docs.crewai.com/en/enterprise/features/marketplace

Discover, install, and govern reusable assets for your enterprise crews.

The Marketplace provides a curated surface for discovering integrations, internal tools, and reusable assets that accelerate crew development.

<Frame>
  <img alt="Marketplace Overview" />
</Frame>

* Browse by category and capability
* Search for assets by name or keyword

* One‑click install for approved assets
* Enable or disable per crew as needed
* Configure required environment variables and scopes

<Frame>
  <img alt="Install & Configure" />
</Frame>

You can also download the templates directly from the marketplace by clicking on the `Download` button so
you can use them locally or refine them to your needs.

<CardGroup>
  <Card title="Tools & Integrations" href="/en/enterprise/features/tools-and-integrations" icon="wrench">
    Connect external apps and manage internal tools your agents can use.
  </Card>

<Card title="Tool Repository" href="/en/enterprise/guides/tool-repository#tool-repository" icon="toolbox">
    Publish and install tools to enhance your crews' capabilities.
  </Card>

<Card title="Agents Repository" href="/en/enterprise/features/agent-repositories" icon="people-group">
    Store, share, and reuse agent definitions across teams and projects.
  </Card>
</CardGroup>

---

## Microsoft Teams Trigger

**URL:** llms-txt#microsoft-teams-trigger

**Contents:**
- Overview
- Enabling the Microsoft Teams Trigger
- Example: Summarize a new chat thread
- Testing Locally

Source: https://docs.crewai.com/en/enterprise/guides/microsoft-teams-trigger

Kick off crews from Microsoft Teams chat activity

Use the Microsoft Teams trigger to start automations whenever a new chat is created. Common patterns include summarizing inbound requests, routing urgent messages to support teams, or creating follow-up tasks in other systems.

<Tip>
  Confirm Microsoft Teams is connected under **Tools & Integrations** and enabled in the **Triggers** tab for your deployment.
</Tip>

## Enabling the Microsoft Teams Trigger

1. Open your deployment in CrewAI AOP
2. Go to the **Triggers** tab
3. Locate **Microsoft Teams** and switch the toggle to enable

<Frame>
  <img alt="Enable or disable triggers with toggle" />
</Frame>

## Example: Summarize a new chat thread

The crew parses thread metadata (subject, created time, roster) and generates an action plan for the receiving team.

Test your Microsoft Teams trigger integration locally using the CrewAI CLI:

**Examples:**

Example 1 (unknown):
```unknown
The crew parses thread metadata (subject, created time, roster) and generates an action plan for the receiving team.

## Testing Locally

Test your Microsoft Teams trigger integration locally using the CrewAI CLI:
```

---

## Path: ~/.local/share/CrewAI/{project}/knowledge/

**URL:** llms-txt#path:-~/.local/share/crewai/{project}/knowledge/

---

## Portkey Integration

**URL:** llms-txt#portkey-integration

**Contents:**
- Introduction
  - Installation & Setup
- Production Features
  - 1. Enhanced Observability
  - 2. Reliability - Keep Your Crews Running Smoothly

Source: https://docs.crewai.com/en/observability/portkey

How to use Portkey with CrewAI

<img alt="Portkey CrewAI Header Image" />

Portkey enhances CrewAI with production-readiness features, turning your experimental agent crews into robust systems by providing:

* **Complete observability** of every agent step, tool use, and interaction
* **Built-in reliability** with fallbacks, retries, and load balancing
* **Cost tracking and optimization** to manage your AI spend
* **Access to 200+ LLMs** through a single integration
* **Guardrails** to keep agent behavior safe and compliant
* **Version-controlled prompts** for consistent agent performance

### Installation & Setup

<Steps>
  <Step title="Install the required packages">
    
  </Step>

<Step title="Generate API Key" icon="lock">
    Create a Portkey API key with optional budget/rate limits from the [Portkey dashboard](https://app.portkey.ai/). You can also attach configurations for reliability, caching, and more to this key. More on this later.
  </Step>

<Step title="Configure CrewAI with Portkey">
    The integration is simple - you just need to update the LLM configuration in your CrewAI setup:

<Info>
      **What are Virtual Keys?** Virtual keys in Portkey securely store your LLM provider API keys (OpenAI, Anthropic, etc.) in an encrypted vault. They allow for easier key rotation and budget management. [Learn more about virtual keys here](https://portkey.ai/docs/product/ai-gateway/virtual-keys).
    </Info>
  </Step>
</Steps>

## Production Features

### 1. Enhanced Observability

Portkey provides comprehensive observability for your CrewAI agents, helping you understand exactly what's happening during each execution.

<Tabs>
  <Tab title="Traces">
    <Frame>
      <img />
    </Frame>

Traces provide a hierarchical view of your crew's execution, showing the sequence of LLM calls, tool invocations, and state transitions.

<Tab title="Logs">
    <Frame>
      <img />
    </Frame>

Portkey logs every interaction with LLMs, including:

* Complete request and response payloads
    * Latency and token usage metrics
    * Cost calculations
    * Tool calls and function executions

All logs can be filtered by metadata, trace IDs, models, and more, making it easy to debug specific crew runs.
  </Tab>

<Tab title="Metrics & Dashboards">
    <Frame>
      <img />
    </Frame>

Portkey provides built-in dashboards that help you:

* Track cost and token usage across all crew runs
    * Analyze performance metrics like latency and success rates
    * Identify bottlenecks in your agent workflows
    * Compare different crew configurations and LLMs

You can filter and segment all metrics by custom metadata to analyze specific crew types, user groups, or use cases.
  </Tab>

<Tab title="Metadata Filtering">
    <Frame>
      <img alt="Analytics with metadata filters" />
    </Frame>

Add custom metadata to your CrewAI LLM configuration to enable powerful filtering and segmentation:

This metadata can be used to filter logs, traces, and metrics on the Portkey dashboard, allowing you to analyze specific crew runs, users, or environments.
  </Tab>
</Tabs>

### 2. Reliability - Keep Your Crews Running Smoothly

When running crews in production, things can go wrong - API rate limits, network issues, or provider outages. Portkey's reliability features ensure your agents keep running smoothly even when problems occur.

It's simple to enable fallback in your CrewAI setup by using a Portkey Config:

```python theme={null}
from crewai import LLM
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL

**Examples:**

Example 1 (unknown):
```unknown
</Step>

  <Step title="Generate API Key" icon="lock">
    Create a Portkey API key with optional budget/rate limits from the [Portkey dashboard](https://app.portkey.ai/). You can also attach configurations for reliability, caching, and more to this key. More on this later.
  </Step>

  <Step title="Configure CrewAI with Portkey">
    The integration is simple - you just need to update the LLM configuration in your CrewAI setup:
```

Example 2 (unknown):
```unknown
<Info>
      **What are Virtual Keys?** Virtual keys in Portkey securely store your LLM provider API keys (OpenAI, Anthropic, etc.) in an encrypted vault. They allow for easier key rotation and budget management. [Learn more about virtual keys here](https://portkey.ai/docs/product/ai-gateway/virtual-keys).
    </Info>
  </Step>
</Steps>

## Production Features

### 1. Enhanced Observability

Portkey provides comprehensive observability for your CrewAI agents, helping you understand exactly what's happening during each execution.

<Tabs>
  <Tab title="Traces">
    <Frame>
      <img />
    </Frame>

    Traces provide a hierarchical view of your crew's execution, showing the sequence of LLM calls, tool invocations, and state transitions.
```

Example 3 (unknown):
```unknown
</Tab>

  <Tab title="Logs">
    <Frame>
      <img />
    </Frame>

    Portkey logs every interaction with LLMs, including:

    * Complete request and response payloads
    * Latency and token usage metrics
    * Cost calculations
    * Tool calls and function executions

    All logs can be filtered by metadata, trace IDs, models, and more, making it easy to debug specific crew runs.
  </Tab>

  <Tab title="Metrics & Dashboards">
    <Frame>
      <img />
    </Frame>

    Portkey provides built-in dashboards that help you:

    * Track cost and token usage across all crew runs
    * Analyze performance metrics like latency and success rates
    * Identify bottlenecks in your agent workflows
    * Compare different crew configurations and LLMs

    You can filter and segment all metrics by custom metadata to analyze specific crew types, user groups, or use cases.
  </Tab>

  <Tab title="Metadata Filtering">
    <Frame>
      <img alt="Analytics with metadata filters" />
    </Frame>

    Add custom metadata to your CrewAI LLM configuration to enable powerful filtering and segmentation:
```

Example 4 (unknown):
```unknown
This metadata can be used to filter logs, traces, and metrics on the Portkey dashboard, allowing you to analyze specific crew runs, users, or environments.
  </Tab>
</Tabs>

### 2. Reliability - Keep Your Crews Running Smoothly

When running crews in production, things can go wrong - API rate limits, network issues, or provider outages. Portkey's reliability features ensure your agents keep running smoothly even when problems occur.

It's simple to enable fallback in your CrewAI setup by using a Portkey Config:
```

---

## React Component Export

**URL:** llms-txt#react-component-export

**Contents:**
- Exporting a React Component
- Setting Up Your React Environment
- Customization
- Next Steps

Source: https://docs.crewai.com/en/enterprise/guides/react-component-export

Learn how to export and integrate CrewAI AOP React components into your applications

This guide explains how to export CrewAI AOP crews as React components and integrate them into your own applications.

## Exporting a React Component

<Steps>
  <Step title="Export the Component">
    Click on the ellipsis (three dots on the right of your deployed crew) and select the export option and save the file locally. We will be using `CrewLead.jsx` for our example.

<Frame>
      <img alt="Export React Component" />
    </Frame>
  </Step>
</Steps>

## Setting Up Your React Environment

To run this React component locally, you'll need to set up a React development environment and integrate this component into a React project.

<Steps>
  <Step title="Install Node.js">
    * Download and install Node.js from the official website: [https://nodejs.org/](https://nodejs.org/)
    * Choose the LTS (Long Term Support) version for stability.
  </Step>

<Step title="Create a new React project">
    * Open Command Prompt or PowerShell
    * Navigate to the directory where you want to create your project
    * Run the following command to create a new React project:

* Change into the project directory:

<Step title="Install necessary dependencies">
    
  </Step>

<Step title="Create the CrewLead component">
    * Move the downloaded file `CrewLead.jsx` into the `src` folder of your project,
  </Step>

<Step title="Modify your App.js to use the CrewLead component">
    * Open `src/App.js`
    * Replace its contents with something like this:

* Replace `YOUR_API_BASE_URL` and `YOUR_BEARER_TOKEN` with the actual values for your API.
  </Step>

<Step title="Start the development server">
    * In your project directory, run:

* This will start the development server, and your default web browser should open automatically to [http://localhost:3000](http://localhost:3000), where you'll see your React app running.
  </Step>
</Steps>

You can then customise the `CrewLead.jsx` to add color, title etc

<Frame>
  <img alt="Customise React Component" />
</Frame>

<Frame>
  <img alt="Customise React Component" />
</Frame>

* Customize the component styling to match your application's design
* Add additional props for configuration
* Integrate with your application's state management
* Add error handling and loading states

**Examples:**

Example 1 (unknown):
```unknown
* Change into the project directory:
```

Example 2 (unknown):
```unknown
</Step>

  <Step title="Install necessary dependencies">
```

Example 3 (unknown):
```unknown
</Step>

  <Step title="Create the CrewLead component">
    * Move the downloaded file `CrewLead.jsx` into the `src` folder of your project,
  </Step>

  <Step title="Modify your App.js to use the CrewLead component">
    * Open `src/App.js`
    * Replace its contents with something like this:
```

Example 4 (unknown):
```unknown
* Replace `YOUR_API_BASE_URL` and `YOUR_BEARER_TOKEN` with the actual values for your API.
  </Step>

  <Step title="Start the development server">
    * In your project directory, run:
```

---

## Remove a deployment

**URL:** llms-txt#remove-a-deployment

**Contents:**
- Option 2: Deploy Directly via Web Interface
- Option 3: Redeploy Using API (CI/CD Integration)
- ⚠️ Environment Variable Security Requirements
  - Blocked Environment Variable Patterns
  - Allowed Exceptions
  - How to Fix Naming Issues

crewai deploy remove <deployment_id>
bash theme={null}
    curl -i -X POST \
         -H "Authorization: Bearer YOUR_PERSONAL_ACCESS_TOKEN" \
         https://app.crewai.com/crewai_plus/api/v1/crews/YOUR-AUTOMATION-UUID/deploy

# HTTP/2 200
    # content-type: application/json
    #
    # {
    #   "uuid": "your-automation-uuid",
    #   "status": "Deploy Enqueued",
    #   "public_url": "https://your-crew-deployment.crewai.com",
    #   "token": "your-bearer-token"
    # }
    yaml theme={null}
    name: Deploy CrewAI Automation

on:
      push:
        branches: [ main ]
      pull_request:
        types: [ labeled ]
      release:
        types: [ published ]

jobs:
      deploy:
        runs-on: ubuntu-latest
        if: |
          (github.event_name == 'push' && github.ref == 'refs/heads/main') ||
          (github.event_name == 'pull_request' && contains(github.event.pull_request.labels.*.name, 'deploy')) ||
          (github.event_name == 'release')
        steps:
          - name: Trigger CrewAI Redeployment
            run: |
              curl -X POST \
                   -H "Authorization: Bearer ${{ secrets.CREWAI_PAT }}" \
                   https://app.crewai.com/crewai_plus/api/v1/crews/${{ secrets.CREWAI_AUTOMATION_UUID }}/deploy
    bash theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## Option 2: Deploy Directly via Web Interface

You can also deploy your crews directly through the CrewAI AOP web interface by connecting your GitHub account. This approach doesn't require using the CLI on your local machine.

<Steps>
  <Step title="Pushing to GitHub">
    You need to push your crew to a GitHub repository. If you haven't created a crew yet, you can [follow this tutorial](/en/quickstart).
  </Step>

  <Step title="Connecting GitHub to CrewAI AOP">
    1. Log in to [CrewAI AOP](https://app.crewai.com)
    2. Click on the button "Connect GitHub"

    <Frame>
      <img alt="Connect GitHub Button" />
    </Frame>
  </Step>

  <Step title="Select the Repository">
    After connecting your GitHub account, you'll be able to select which repository to deploy:

    <Frame>
      <img alt="Select Repository" />
    </Frame>
  </Step>

  <Step title="Set Environment Variables">
    Before deploying, you'll need to set up your environment variables to connect to your LLM provider or other services:

    1. You can add variables individually or in bulk
    2. Enter your environment variables in `KEY=VALUE` format (one per line)

    <Frame>
      <img alt="Set Environment Variables" />
    </Frame>
  </Step>

  <Step title="Deploy Your Crew">
    1. Click the "Deploy" button to start the deployment process
    2. You can monitor the progress through the progress bar
    3. The first deployment typically takes around 10-15 minutes; subsequent deployments will be faster

    <Frame>
      <img alt="Deploy Progress" />
    </Frame>

    Once deployment is complete, you'll see:

    * Your crew's unique URL
    * A Bearer token to protect your crew API
    * A "Delete" button if you need to remove the deployment
  </Step>
</Steps>

## Option 3: Redeploy Using API (CI/CD Integration)

For automated deployments in CI/CD pipelines, you can use the CrewAI API to trigger redeployments of existing crews. This is particularly useful for GitHub Actions, Jenkins, or other automation workflows.

<Steps>
  <Step title="Get Your Personal Access Token">
    Navigate to your CrewAI AOP account settings to generate an API token:

    1. Go to [app.crewai.com](https://app.crewai.com)
    2. Click on **Settings** → **Account** → **Personal Access Token**
    3. Generate a new token and copy it securely
    4. Store this token as a secret in your CI/CD system
  </Step>

  <Step title="Find Your Automation UUID">
    Locate the unique identifier for your deployed crew:

    1. Go to **Automations** in your CrewAI AOP dashboard
    2. Select your existing automation/crew
    3. Click on **Additional Details**
    4. Copy the **UUID** - this identifies your specific crew deployment
  </Step>

  <Step title="Trigger Redeployment via API">
    Use the Deploy API endpoint to trigger a redeployment:
```

Example 2 (unknown):
```unknown
<Info>
      If your automation was first created connected to Git, the API will automatically pull the latest changes from your repository before redeploying.
    </Info>
  </Step>

  <Step title="GitHub Actions Integration Example">
    Here's a GitHub Actions workflow with more complex deployment triggers:
```

Example 3 (unknown):
```unknown
<Tip>
      Add `CREWAI_PAT` and `CREWAI_AUTOMATION_UUID` as repository secrets. For PR deployments, add a "deploy" label to trigger the workflow.
    </Tip>
  </Step>
</Steps>

## ⚠️ Environment Variable Security Requirements

<Warning>
  **Important**: CrewAI AOP has security restrictions on environment variable names that can cause deployment failures if not followed.
</Warning>

### Blocked Environment Variable Patterns

For security reasons, the following environment variable naming patterns are **automatically filtered** and will cause deployment issues:

**Blocked Patterns:**

* Variables ending with `_TOKEN` (e.g., `MY_API_TOKEN`)
* Variables ending with `_PASSWORD` (e.g., `DB_PASSWORD`)
* Variables ending with `_SECRET` (e.g., `API_SECRET`)
* Variables ending with `_KEY` in certain contexts

**Specific Blocked Variables:**

* `GITHUB_USER`, `GITHUB_TOKEN`
* `AWS_REGION`, `AWS_DEFAULT_REGION`
* Various internal CrewAI system variables

### Allowed Exceptions

Some variables are explicitly allowed despite matching blocked patterns:

* `AZURE_AD_TOKEN`
* `AZURE_OPENAI_AD_TOKEN`
* `ENTERPRISE_ACTION_TOKEN`
* `CREWAI_ENTEPRISE_TOOLS_TOKEN`

### How to Fix Naming Issues

If your deployment fails due to environment variable restrictions:
```

---

## Reset crew memories

**URL:** llms-txt#reset-crew-memories

crewai reset-memories

---

## Role-Based Access Control (RBAC)

**URL:** llms-txt#role-based-access-control-(rbac)

**Contents:**
- Overview
- Users and Roles
  - Configuration summary
- Automation‑level Access Control
  - Private visibility: access outcomes

Source: https://docs.crewai.com/en/enterprise/features/rbac

Control access to crews, tools, and data with roles, scopes, and granular permissions.

RBAC in CrewAI AOP enables secure, scalable access management through a combination of organization‑level roles and automation‑level visibility controls.

<Frame>
  <img alt="RBAC overview in CrewAI AOP" />
</Frame>

Each member in your CrewAI workspace is assigned a role, which determines their access across various features.

* Use predefined roles (Owner, Member)
* Create custom roles tailored to specific permissions
* Assign roles at any time through the settings panel

You can configure users and roles in Settings → Roles.

<Steps>
  <Step title="Open Roles settings">
    Go to <b>Settings → Roles</b> in CrewAI AOP.
  </Step>

<Step title="Choose a role type">
    Use a predefined role (<b>Owner</b>, <b>Member</b>) or click <b>Create role</b> to define a custom one.
  </Step>

<Step title="Assign to members">
    Select users and assign the role. You can change this anytime.
  </Step>
</Steps>

### Configuration summary

| Area                  | Where to configure                 | Options                                 |
| :-------------------- | :--------------------------------- | :-------------------------------------- |
| Users & Roles         | Settings → Roles                   | Predefined: Owner, Member; Custom roles |
| Automation visibility | Automation → Settings → Visibility | Private; Whitelist users/roles          |

## Automation‑level Access Control

In addition to organization‑wide roles, CrewAI Automations support fine‑grained visibility settings that let you restrict access to specific automations by user or role.

* Keeping sensitive or experimental automations private
* Managing visibility across large teams or external collaborators
* Testing automations in isolated contexts

Deployments can be configured as private, meaning only whitelisted users and roles will be able to:

* View the deployment
* Run it or interact with its API
* Access its logs, metrics, and settings

The organization owner always has access, regardless of visibility settings.

You can configure automation‑level access control in Automation → Settings → Visibility tab.

<Steps>
  <Step title="Open Visibility tab">
    Navigate to <b>Automation → Settings → Visibility</b>.
  </Step>

<Step title="Set visibility">
    Choose <b>Private</b> to restrict access. The organization owner always retains access.
  </Step>

<Step title="Whitelist access">
    Add specific users and roles allowed to view, run, and access logs/metrics/settings.
  </Step>

<Step title="Save and verify">
    Save changes, then confirm that non‑whitelisted users cannot view or run the automation.
  </Step>
</Steps>

### Private visibility: access outcomes

| Action                       | Owner | Whitelisted user/role | Not whitelisted |
| :--------------------------- | :---- | :-------------------- | :-------------- |
| View automation              | ✓     | ✓                     | ✗               |
| Run automation/API           | ✓     | ✓                     | ✗               |
| Access logs/metrics/settings | ✓     | ✓                     | ✗               |

<Tip>
  The organization owner always has access. In private mode, only whitelisted users and roles can view, run, and access logs/metrics/settings.
</Tip>

<Frame>
  <img alt="Automation Visibility settings in CrewAI AOP" />
</Frame>

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with RBAC questions.
</Card>

---

## Run the crew

**URL:** llms-txt#run-the-crew

**Contents:**
  - Loading Multiple Tools from a Tool Pack

result = crew.kickoff()
print(result)
python {2, 4-8} theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import MergeAgentHandlerTool

**Examples:**

Example 1 (unknown):
```unknown
### Loading Multiple Tools from a Tool Pack

You can load all available tools from your Tool Pack at once:
```

---

## Run your crew

**URL:** llms-txt#run-your-crew

**Contents:**
  - Step 5: View Traces in Braintrust
  - Step 6: Evaluate via SDK (Experiments)

if __name__ == "__main__":
    # Instrumentation is already initialized above in this module
    result = run_crew()
    print(result)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### Step 5: View Traces in Braintrust

After running your crew, you can view comprehensive traces in Braintrust through different perspectives:

<Tabs>
  <Tab title="Trace">
    <Frame>
      <img alt="Braintrust Trace View" />
    </Frame>
  </Tab>

  <Tab title="Timeline">
    <Frame>
      <img alt="Braintrust Timeline View" />
    </Frame>
  </Tab>

  <Tab title="Thread">
    <Frame>
      <img alt="Braintrust Thread View" />
    </Frame>
  </Tab>
</Tabs>

### Step 6: Evaluate via SDK (Experiments)

You can also run evaluations using Braintrust's Eval SDK. This is useful for comparing versions or scoring outputs offline. Below is a Python example using the `Eval` class with the crew we created above:
```

---

## Salesforce Trigger

**URL:** llms-txt#salesforce-trigger

**Contents:**
- Overview
- Demo
- Getting Started
- Use Cases
- Next Steps

Source: https://docs.crewai.com/en/enterprise/guides/salesforce-trigger

Trigger CrewAI crews from Salesforce workflows for CRM automation

CrewAI AOP can be triggered from Salesforce to automate customer relationship management workflows and enhance your sales operations.

Salesforce is a leading customer relationship management (CRM) platform that helps businesses streamline their sales, service, and marketing operations. By setting up CrewAI triggers from Salesforce, you can:

* Automate lead scoring and qualification
* Generate personalized sales materials
* Enhance customer service with AI-powered responses
* Streamline data analysis and reporting

<iframe title="CrewAI + Salesforce trigger demo" />

To set up Salesforce triggers:

1. **Contact Support**: Reach out to CrewAI AOP support for assistance with Salesforce trigger setup
2. **Review Requirements**: Ensure you have the necessary Salesforce permissions and API access
3. **Configure Connection**: Work with the support team to establish the connection between CrewAI and your Salesforce instance
4. **Test Triggers**: Verify the triggers work correctly with your specific use cases

Common Salesforce + CrewAI trigger scenarios include:

* **Lead Processing**: Automatically analyze and score incoming leads
* **Proposal Generation**: Create customized proposals based on opportunity data
* **Customer Insights**: Generate analysis reports from customer interaction history
* **Follow-up Automation**: Create personalized follow-up messages and recommendations

For detailed setup instructions and advanced configuration options, please contact CrewAI AOP support who can provide tailored guidance for your specific Salesforce environment and business needs.

---

## Save crew logs

**URL:** llms-txt#save-crew-logs

**Contents:**
- Memory Utilization
- Cache Utilization
- Crew Usage Metrics

crew = Crew(output_log_file = True)  # Logs will be saved as logs.txt
crew = Crew(output_log_file = file_name)  # Logs will be saved as file_name.txt
crew = Crew(output_log_file = file_name.txt)  # Logs will be saved as file_name.txt
crew = Crew(output_log_file = file_name.json)  # Logs will be saved as file_name.json
python Code theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## Memory Utilization

Crews can utilize memory (short-term, long-term, and entity memory) to enhance their execution and learning over time. This feature allows crews to store and recall execution memories, aiding in decision-making and task execution strategies.

## Cache Utilization

Caches can be employed to store the results of tools' execution, making the process more efficient by reducing the need to re-execute identical tasks.

## Crew Usage Metrics

After the crew execution, you can access the `usage_metrics` attribute to view the language model (LLM) usage metrics for all tasks executed by the crew. This provides insights into operational efficiency and areas for improvement.
```

---

## setup monitoring for your crew

**URL:** llms-txt#setup-monitoring-for-your-crew

tracer_provider = register(
    endpoint="http://localhost:6006/v1/traces")
CrewAIInstrumentor().instrument(skip_dep_check=True, tracer_provider=tracer_provider)
search_tool = SerperDevTool()

---

## Set custom storage location for all CrewAI data

**URL:** llms-txt#set-custom-storage-location-for-all-crewai-data

os.environ["CREWAI_STORAGE_DIR"] = "./my_project_storage"

---

## Slack Trigger

**URL:** llms-txt#slack-trigger

**Contents:**
- Prerequisites
- Setup Steps
- Tips

Source: https://docs.crewai.com/en/enterprise/guides/slack-trigger

Trigger CrewAI crews directly from Slack using slash commands

This guide explains how to start a crew directly from Slack using CrewAI triggers.

* CrewAI Slack trigger installed and connected to your Slack workspace
* At least one crew configured in CrewAI

<Steps>
  <Step title="Ensure the CrewAI Slack trigger is set up">
    In the CrewAI dashboard, navigate to the **Triggers** section.

<Frame>
      <img alt="CrewAI Slack Integration" />
    </Frame>

Verify that Slack is listed and is connected.
  </Step>

<Step title="Open your Slack channel">
    * Navigate to the channel where you want to kickoff the crew.
    * Type the slash command "**/kickoff**" to initiate the crew kickoff process.
    * You should see a  "**Kickoff crew**" appear as you type:
      <Frame>
        <img alt="Kickoff crew" />
      </Frame>
    * Press Enter or select the "**Kickoff crew**" option. A dialog box titled "**Kickoff an AI Crew**" will appear.
  </Step>

<Step title="Select the crew you want to start">
    * In the dropdown menu labeled "**Select of the crews online:**", choose the crew you want to start.
    * In the example below, "**prep-for-meeting**" is selected:
      <Frame>
        <img alt="Kickoff crew dropdown" />
      </Frame>
    * If your crew requires any inputs, click the "**Add Inputs**" button to provide them.
      <Note>
        The "**Add Inputs**" button is shown in the example above but is not yet clicked.
      </Note>
  </Step>

<Step title="Click Kickoff and wait for the crew to complete">
    * Once you've selected the crew and added any necessary inputs, click "**Kickoff**" to start the crew.
      <Frame>
        <img alt="Kickoff crew" />
      </Frame>
    * The crew will start executing and you will see the results in the Slack channel.
      <Frame>
        <img alt="Kickoff crew results" />
      </Frame>
  </Step>
</Steps>

* Make sure you have the necessary permissions to use the `/kickoff` command in your Slack workspace.
* If you don't see your desired crew in the dropdown, ensure it's properly configured and online in CrewAI.

---

## src/guide_creator_flow/crews/content_crew/config/tasks.yaml

**URL:** llms-txt#src/guide_creator_flow/crews/content_crew/config/tasks.yaml

write_section_task:
  description: >
    Write a comprehensive section on the topic: "{section_title}"

Section description: {section_description}
    Target audience: {audience_level} level learners

Your content should:
    1. Begin with a brief introduction to the section topic
    2. Explain all key concepts clearly with examples
    3. Include practical applications or exercises where appropriate
    4. End with a summary of key points
    5. Be approximately 500-800 words in length

Format your content in Markdown with appropriate headings, lists, and emphasis.

Previously written sections:
    {previous_sections}

Make sure your content maintains consistency with previously written sections
    and builds upon concepts that have already been explained.
  expected_output: >
    A well-structured, comprehensive section in Markdown format that thoroughly
    explains the topic and is appropriate for the target audience.
  agent: content_writer

review_section_task:
  description: >
    Review and improve the following section on "{section_title}":

Target audience: {audience_level} level learners

Previously written sections:
    {previous_sections}

Your review should:
    1. Fix any grammatical or spelling errors
    2. Improve clarity and readability
    3. Ensure content is comprehensive and accurate
    4. Verify consistency with previously written sections
    5. Enhance the structure and flow
    6. Add any missing key information

Provide the improved version of the section in Markdown format.
  expected_output: >
    An improved, polished version of the section that maintains the original
    structure but enhances clarity, accuracy, and consistency.
  agent: content_reviewer
  context:
    - write_section_task
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
These task definitions provide detailed instructions to our agents, ensuring they produce content that meets our quality standards. Note how the `context` parameter in the review task creates a workflow where the reviewer has access to the writer's output.

3. Now, update the crew implementation file to define how our agents and tasks work together:
```

---

## src/research_crew/config/tasks.yaml

**URL:** llms-txt#src/research_crew/config/tasks.yaml

**Contents:**
- Step 5: Configure Your Crew

research_task:
  description: >
    Conduct thorough research on {topic}. Focus on:
    1. Key concepts and definitions
    2. Historical development and recent trends
    3. Major challenges and opportunities
    4. Notable applications or case studies
    5. Future outlook and potential developments

Make sure to organize your findings in a structured format with clear sections.
  expected_output: >
    A comprehensive research document with well-organized sections covering
    all the requested aspects of {topic}. Include specific facts, figures,
    and examples where relevant.
  agent: researcher

analysis_task:
  description: >
    Analyze the research findings and create a comprehensive report on {topic}.
    Your report should:
    1. Begin with an executive summary
    2. Include all key information from the research
    3. Provide insightful analysis of trends and patterns
    4. Offer recommendations or future considerations
    5. Be formatted in a professional, easy-to-read style with clear headings
  expected_output: >
    A polished, professional report on {topic} that presents the research
    findings with added analysis and insights. The report should be well-structured
    with an executive summary, main sections, and conclusion.
  agent: analyst
  context:
    - research_task
  output_file: output/report.md
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
Note the `context` field in the analysis task - this is a powerful feature that allows the analyst to access the output of the research task. This creates a workflow where information flows naturally between agents, just as it would in a human team.

## Step 5: Configure Your Crew

Now it's time to bring everything together by configuring our crew. The crew is the container that orchestrates how agents work together to complete tasks.

Let's modify the `crew.py` file:
```

---

## src/research_crew/main.py

**URL:** llms-txt#src/research_crew/main.py

import os
from research_crew.crew import ResearchCrew

---

## Start the crew's task execution

**URL:** llms-txt#start-the-crew's-task-execution

result = my_crew.kickoff()
print(result)

---

## Test the crew

**URL:** llms-txt#test-the-crew

---

## Tool Repository

**URL:** llms-txt#tool-repository

**Contents:**
- Overview
- Prerequisites
- Installing Tools
- Adding other packages after installing a tool
- Creating and Publishing Tools
- Updating Tools
- Deleting Tools
- Security Checks

Source: https://docs.crewai.com/en/enterprise/guides/tool-repository

Using the Tool Repository to manage your tools

The Tool Repository is a package manager for CrewAI tools. It allows users to publish, install, and manage tools that integrate with CrewAI crews and flows.

* **Private**: accessible only within your organization (default)
* **Public**: accessible to all CrewAI users if published with the `--public` flag

The repository is not a version control system. Use Git to track code changes and enable collaboration.

Before using the Tool Repository, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account
* [CrewAI CLI](/en/concepts/cli#cli) installed
* uv>=0.5.0 installed. Check out [how to upgrade](https://docs.astral.sh/uv/getting-started/installation/#upgrading-uv)
* [Git](https://git-scm.com) installed and configured
* Access permissions to publish or install tools in your CrewAI AOP organization

This installs the tool and adds it to `pyproject.toml`.

You can use the tool by importing it and adding it to your agents:

## Adding other packages after installing a tool

After installing a tool from the CrewAI AOP Tool Repository, you need to use the `crewai uv` command to add other packages to your project.
Using pure `uv` commands will fail due to authentication to tool repository being handled by the CLI. By using the `crewai uv` command, you can add other packages to your project without having to worry about authentication.
Any `uv` command can be used with the `crewai uv` command, making it a powerful tool for managing your project's dependencies without the hassle of managing authentication through environment variables or other methods.

Say that you have installed a custom tool from the CrewAI AOP Tool Repository called "my-tool":

And now you want to add another package to your project, you can use the following command:

Other commands like `uv sync` or `uv remove` can also be used with the `crewai uv` command:

This will add the package to your project and update `pyproject.toml` accordingly.

## Creating and Publishing Tools

To create a new tool project:

This generates a scaffolded tool project locally.

After making changes, initialize a Git repository and commit the code:

By default, tools are published as private. To make a tool public:

For more details on how to build tools, see [Creating your own tools](/en/concepts/tools#creating-your-own-tools).

To update a published tool:

1. Modify the tool locally
2. Update the version in `pyproject.toml` (e.g., from `0.1.0` to `0.1.1`)
3. Commit the changes and publish

1. Go to [CrewAI AOP](https://app.crewai.com)
2. Navigate to **Tools**
3. Select the tool
4. Click **Delete**

<Warning>
  Deletion is permanent. Deleted tools cannot be restored or re-installed.
</Warning>

Every published version undergoes automated security checks, and are only available to install after they pass.

You can check the security check status of a tool at:

`CrewAI AOP > Tools > Your Tool > Versions`

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with API integration or troubleshooting.
</Card>

**Examples:**

Example 1 (unknown):
```unknown
This installs the tool and adds it to `pyproject.toml`.

You can use the tool by importing it and adding it to your agents:
```

Example 2 (unknown):
```unknown
## Adding other packages after installing a tool

After installing a tool from the CrewAI AOP Tool Repository, you need to use the `crewai uv` command to add other packages to your project.
Using pure `uv` commands will fail due to authentication to tool repository being handled by the CLI. By using the `crewai uv` command, you can add other packages to your project without having to worry about authentication.
Any `uv` command can be used with the `crewai uv` command, making it a powerful tool for managing your project's dependencies without the hassle of managing authentication through environment variables or other methods.

Say that you have installed a custom tool from the CrewAI AOP Tool Repository called "my-tool":
```

Example 3 (unknown):
```unknown
And now you want to add another package to your project, you can use the following command:
```

Example 4 (unknown):
```unknown
Other commands like `uv sync` or `uv remove` can also be used with the `crewai uv` command:
```

---

## Traces

**URL:** llms-txt#traces

**Contents:**
- Overview
- What are Traces?
- Accessing Traces
- Understanding the Trace Interface
  - 1. Execution Summary
  - 2. Tasks & Agents
  - 3. Final Output
  - 4. Execution Timeline
  - 5. Detailed Task View
- Using Traces for Debugging

Source: https://docs.crewai.com/en/enterprise/features/traces

Using Traces to monitor your Crews

Traces provide comprehensive visibility into your crew executions, helping you monitor performance, debug issues, and optimize your AI agent workflows.

Traces in CrewAI AOP are detailed execution records that capture every aspect of your crew's operation, from initial inputs to final outputs. They record:

* Agent thoughts and reasoning
* Task execution details
* Tool usage and outputs
* Token consumption metrics
* Execution times
* Cost estimates

<Frame>
  <img alt="Traces Overview" />
</Frame>

<Steps>
  <Step title="Navigate to the Traces Tab">
    Once in your CrewAI AOP dashboard, click on the **Traces** to view all execution records.
  </Step>

<Step title="Select an Execution">
    You'll see a list of all crew executions, sorted by date. Click on any execution to view its detailed trace.
  </Step>
</Steps>

## Understanding the Trace Interface

The trace interface is divided into several sections, each providing different insights into your crew's execution:

### 1. Execution Summary

The top section displays high-level metrics about the execution:

* **Total Tokens**: Number of tokens consumed across all tasks
* **Prompt Tokens**: Tokens used in prompts to the LLM
* **Completion Tokens**: Tokens generated in LLM responses
* **Requests**: Number of API calls made
* **Execution Time**: Total duration of the crew run
* **Estimated Cost**: Approximate cost based on token usage

<Frame>
  <img alt="Execution Summary" />
</Frame>

### 2. Tasks & Agents

This section shows all tasks and agents that were part of the crew execution:

* Task name and agent assignment
* Agents and LLMs used for each task
* Status (completed/failed)
* Individual execution time of the task

<Frame>
  <img alt="Task List" />
</Frame>

Displays the final result produced by the crew after all tasks are completed.

<Frame>
  <img alt="Final Output" />
</Frame>

### 4. Execution Timeline

A visual representation of when each task started and ended, helping you identify bottlenecks or parallel execution patterns.

<Frame>
  <img alt="Execution Timeline" />
</Frame>

### 5. Detailed Task View

When you click on a specific task in the timeline or task list, you'll see:

<Frame>
  <img alt="Detailed Task View" />
</Frame>

* **Task Key**: Unique identifier for the task
* **Task ID**: Technical identifier in the system
* **Status**: Current state (completed/running/failed)
* **Agent**: Which agent performed the task
* **LLM**: Language model used for this task
* **Start/End Time**: When the task began and completed
* **Execution Time**: Duration of this specific task
* **Task Description**: What the agent was instructed to do
* **Expected Output**: What output format was requested
* **Input**: Any input provided to this task from previous tasks
* **Output**: The actual result produced by the agent

## Using Traces for Debugging

Traces are invaluable for troubleshooting issues with your crews:

<Steps>
  <Step title="Identify Failure Points">
    When a crew execution doesn't produce the expected results, examine the trace to find where things went wrong. Look for:

* Failed tasks
    * Unexpected agent decisions
    * Tool usage errors
    * Misinterpreted instructions

<Frame>
      <img alt="Failure Points" />
    </Frame>
  </Step>

<Step title="Optimize Performance">
    Use execution metrics to identify performance bottlenecks:

* Tasks that took longer than expected
    * Excessive token usage
    * Redundant tool operations
    * Unnecessary API calls
  </Step>

<Step title="Improve Cost Efficiency">
    Analyze token usage and cost estimates to optimize your crew's efficiency:

* Consider using smaller models for simpler tasks
    * Refine prompts to be more concise
    * Cache frequently accessed information
    * Structure tasks to minimize redundant operations
  </Step>
</Steps>

## Performance and batching

CrewAI batches trace uploads to reduce overhead on high-volume runs:

* A TraceBatchManager buffers events and sends them in batches via the Plus API client
* Reduces network chatter and improves reliability on flaky connections
* Automatically enabled in the default trace listener; no configuration needed

This yields more stable tracing under load while preserving detailed task/agent telemetry.

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with trace analysis or any other CrewAI AOP features.
</Card>

---

## Update Crew

**URL:** llms-txt#update-crew

**Contents:**
- Why Update Your Crew?
- 1. Updating Your Crew Code for a Latest Commit
- 2. Resetting Bearer Token
- 3. Updating Environment Variables
- After Updating

Source: https://docs.crewai.com/en/enterprise/guides/update-crew

Updating a Crew on CrewAI AOP

<Note>
  After deploying your crew to CrewAI AOP, you may need to make updates to the code, security settings, or configuration.
  This guide explains how to perform these common update operations.
</Note>

## Why Update Your Crew?

CrewAI won't automatically pick up GitHub updates by default, so you'll need to manually trigger updates, unless you checked the `Auto-update` option when deploying your crew.

There are several reasons you might want to update your crew deployment:

* You want to update the code with a latest commit you pushed to GitHub
* You want to reset the bearer token for security reasons
* You want to update environment variables

## 1. Updating Your Crew Code for a Latest Commit

When you've pushed new commits to your GitHub repository and want to update your deployment:

1. Navigate to your crew in the CrewAI AOP platform
2. Click on the `Re-deploy` button on your crew details page

<Frame>
  <img alt="Re-deploy Button" />
</Frame>

This will trigger an update that you can track using the progress bar. The system will pull the latest code from your repository and rebuild your deployment.

## 2. Resetting Bearer Token

If you need to generate a new bearer token (for example, if you suspect the current token might have been compromised):

1. Navigate to your crew in the CrewAI AOP platform
2. Find the `Bearer Token` section
3. Click the `Reset` button next to your current token

<Frame>
  <img alt="Reset Token" />
</Frame>

<Warning>
  Resetting your bearer token will invalidate the previous token immediately. Make sure to update any applications or scripts that are using the old token.
</Warning>

## 3. Updating Environment Variables

To update the environment variables for your crew:

1. First access the deployment page by clicking on your crew's name

<Frame>
  <img alt="Environment Variables Button" />
</Frame>

2. Locate the `Environment Variables` section (you will need to click the `Settings` icon to access it)
3. Edit the existing variables or add new ones in the fields provided
4. Click the `Update` button next to each variable you modify

<Frame>
  <img alt="Update Environment Variables" />
</Frame>

5. Finally, click the `Update Deployment` button at the bottom of the page to apply the changes

<Note>
  Updating environment variables will trigger a new deployment, but this will only update the environment configuration and not the code itself.
</Note>

After performing any update:

1. The system will rebuild and redeploy your crew
2. You can monitor the deployment progress in real-time
3. Once complete, test your crew to ensure the changes are working as expected

<Tip>
  If you encounter any issues after updating, you can view deployment logs in the platform or contact support for assistance.
</Tip>

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with updating your crew or troubleshooting deployment issues.
</Card>

---

## Webhook Streaming

**URL:** llms-txt#webhook-streaming

**Contents:**
- Overview
- Usage
- Webhook Format
- Supported Events
  - Flow Events:
  - Agent Events:
  - Crew Events:
  - Task Events:
  - Tool Usage Events:
  - LLM Events:

Source: https://docs.crewai.com/en/enterprise/features/webhook-streaming

Using Webhook Streaming to stream events to your webhook

Enterprise Event Streaming lets you receive real-time webhook updates about your crews and flows deployed to
CrewAI AOP, such as model calls, tool usage, and flow steps.

When using the Kickoff API, include a `webhooks` object to your request, for example:

If `realtime` is set to `true`, each event is delivered individually and immediately, at the cost of crew/flow performance.

Each webhook sends a list of events:

The `data` object structure varies by event type. Refer to the [event list](https://github.com/crewAIInc/crewAI/tree/main/src/crewai/utilities/events) on GitHub.

As requests are sent over HTTP, the order of events can't be guaranteed. If you need ordering, use the `timestamp` field.

CrewAI supports both system events and custom events in Enterprise Event Streaming. These events are sent to your configured webhook endpoint during crew and flow execution.

* `flow_created`
* `flow_started`
* `flow_finished`
* `flow_plot`
* `method_execution_started`
* `method_execution_finished`
* `method_execution_failed`

* `agent_execution_started`
* `agent_execution_completed`
* `agent_execution_error`
* `lite_agent_execution_started`
* `lite_agent_execution_completed`
* `lite_agent_execution_error`
* `agent_logs_started`
* `agent_logs_execution`
* `agent_evaluation_started`
* `agent_evaluation_completed`
* `agent_evaluation_failed`

* `crew_kickoff_started`
* `crew_kickoff_completed`
* `crew_kickoff_failed`
* `crew_train_started`
* `crew_train_completed`
* `crew_train_failed`
* `crew_test_started`
* `crew_test_completed`
* `crew_test_failed`
* `crew_test_result`

* `task_started`
* `task_completed`
* `task_failed`
* `task_evaluation`

### Tool Usage Events:

* `tool_usage_started`
* `tool_usage_finished`
* `tool_usage_error`
* `tool_validate_input_error`
* `tool_selection_error`
* `tool_execution_error`

* `llm_call_started`
* `llm_call_completed`
* `llm_call_failed`
* `llm_stream_chunk`

### LLM Guardrail Events:

* `llm_guardrail_started`
* `llm_guardrail_completed`

* `memory_query_started`
* `memory_query_completed`
* `memory_query_failed`
* `memory_save_started`
* `memory_save_completed`
* `memory_save_failed`
* `memory_retrieval_started`
* `memory_retrieval_completed`

### Knowledge Events:

* `knowledge_search_query_started`
* `knowledge_search_query_completed`
* `knowledge_search_query_failed`
* `knowledge_query_started`
* `knowledge_query_completed`
* `knowledge_query_failed`

### Reasoning Events:

* `agent_reasoning_started`
* `agent_reasoning_completed`
* `agent_reasoning_failed`

Event names match the internal event bus. See GitHub for the full list of events.

You can emit your own custom events, and they will be delivered through the webhook stream alongside system events.

<CardGroup>
  <Card title="GitHub" icon="github" href="https://github.com/crewAIInc/crewAI/tree/main/src/crewai/utilities/events">
    Full list of events
  </Card>

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
    Contact our support team for assistance with webhook integration or troubleshooting.
  </Card>
</CardGroup>

**Examples:**

Example 1 (unknown):
```unknown
If `realtime` is set to `true`, each event is delivered individually and immediately, at the cost of crew/flow performance.

## Webhook Format

Each webhook sends a list of events:
```

---

## Zapier Trigger

**URL:** llms-txt#zapier-trigger

**Contents:**
- Prerequisites
- Step-by-Step Setup
- Tips for Success

Source: https://docs.crewai.com/en/enterprise/guides/zapier-trigger

Trigger CrewAI crews from Zapier workflows to automate cross-app workflows

This guide will walk you through the process of setting up Zapier triggers for CrewAI AOP, allowing you to automate workflows between CrewAI AOP and other applications.

* A CrewAI AOP account
* A Zapier account
* A Slack account (for this specific example)

## Step-by-Step Setup

<Steps>
  <Step title="Set Up the Slack Trigger">
    * In Zapier, create a new Zap.

<Frame>
      <img alt="Zapier 1" />
    </Frame>
  </Step>

<Step title="Choose Slack as your trigger app">
    <Frame>
      <img alt="Zapier 2" />
    </Frame>

* Select `New Pushed Message` as the Trigger Event.
    * Connect your Slack account if you haven't already.
  </Step>

<Step title="Configure the CrewAI AOP Action">
    * Add a new action step to your Zap.
    * Choose CrewAI+ as your action app and Kickoff as the Action Event

<Frame>
      <img alt="Zapier 5" />
    </Frame>
  </Step>

<Step title="Connect your CrewAI AOP account">
    * Connect your CrewAI AOP account.
    * Select the appropriate Crew for your workflow.

<Frame>
      <img alt="Zapier 6" />
    </Frame>

* Configure the inputs for the Crew using the data from the Slack message.
  </Step>

<Step title="Format the CrewAI AOP Output">
    * Add another action step to format the text output from CrewAI AOP.
    * Use Zapier's formatting tools to convert the Markdown output to HTML.

<Frame>
      <img alt="Zapier 8" />
    </Frame>

<Frame>
      <img alt="Zapier 9" />
    </Frame>
  </Step>

<Step title="Send the Output via Email">
    * Add a final action step to send the formatted output via email.
    * Choose your preferred email service (e.g., Gmail, Outlook).
    * Configure the email details, including recipient, subject, and body.
    * Insert the formatted CrewAI AOP output into the email body.

<Frame>
      <img alt="Zapier 7" />
    </Frame>
  </Step>

<Step title="Kick Off the crew from Slack">
    * Enter the text in your Slack channel

<Frame>
      <img alt="Zapier 10" />
    </Frame>

* Select the 3 ellipsis button and then chose Push to Zapier

<Frame>
      <img alt="Zapier 11" />
    </Frame>
  </Step>

<Step title="Select the crew and then Push to Kick Off">
    <Frame>
      <img alt="Zapier 12" />
    </Frame>
  </Step>
</Steps>

* Ensure that your CrewAI AOP inputs are correctly mapped from the Slack message.
* Test your Zap thoroughly before turning it on to catch any potential issues.
* Consider adding error handling steps to manage potential failures in the workflow.

By following these steps, you'll have successfully set up Zapier triggers for CrewAI AOP, allowing for automated workflows triggered by Slack messages and resulting in email notifications with CrewAI AOP output.

---

## ├── crew/                    # Crew knowledge collection

**URL:** llms-txt#├──-crew/--------------------#-crew-knowledge-collection

---

## - generalist gets: crew_knowledge only

**URL:** llms-txt#--generalist-gets:-crew_knowledge-only

**Examples:**

Example 1 (unknown):
```unknown
#### Example 3: Multiple Agents with Different Knowledge
```

---

## - specialist gets: crew_knowledge + specialist_knowledge

**URL:** llms-txt#--specialist-gets:-crew_knowledge-+-specialist_knowledge

---
