# Crewai - Agents

**Pages:** 404

---

## Accessing the type-safe output

**URL:** llms-txt#accessing-the-type-safe-output

**Contents:**
  - Note:
  - Workflow in Action
- Advanced Features
  - Task Delegation
  - Asynchronous Execution
  - Memory and Caching
  - Callbacks
  - Usage Metrics
- Best Practices for Sequential Processes

task_output: TaskOutput = result.tasks[0].output
crew_output: CrewOutput = result.output
```

Each task in a sequential process **must** have an agent assigned. Ensure that every `Task` includes an `agent` parameter.

### Workflow in Action

1. **Initial Task**: In a sequential process, the first agent completes their task and signals completion.
2. **Subsequent Tasks**: Agents pick up their tasks based on the process type, with outcomes of preceding tasks or directives guiding their execution.
3. **Completion**: The process concludes once the final task is executed, leading to project completion.

In sequential processes, if an agent has `allow_delegation` set to `True`, they can delegate tasks to other agents in the crew.
This feature is automatically set up when there are multiple agents in the crew.

### Asynchronous Execution

Tasks can be executed asynchronously, allowing for parallel processing when appropriate.
To create an asynchronous task, set `async_execution=True` when defining the task.

### Memory and Caching

CrewAI supports both memory and caching features:

* **Memory**: Enable by setting `memory=True` when creating the Crew. This allows agents to retain information across tasks.
* **Caching**: By default, caching is enabled. Set `cache=False` to disable it.

You can set callbacks at both the task and step level:

* `task_callback`: Executed after each task completion.
* `step_callback`: Executed after each step in an agent's execution.

CrewAI tracks token usage across all tasks and agents. You can access these metrics after execution.

## Best Practices for Sequential Processes

1. **Order Matters**: Arrange tasks in a logical sequence where each task builds upon the previous one.
2. **Clear Task Descriptions**: Provide detailed descriptions for each task to guide the agents effectively.
3. **Appropriate Agent Selection**: Match agents' skills and roles to the requirements of each task.
4. **Use Context**: Leverage the context from previous tasks to inform subsequent ones.

This updated documentation ensures that details accurately reflect the latest changes in the codebase and clearly describes how to leverage new features and configurations.
The content is kept simple and direct to ensure easy understanding.

---

## Access the crew's usage metrics

**URL:** llms-txt#access-the-crew's-usage-metrics

**Contents:**
- Crew Execution Process
  - Kicking Off a Crew

crew = Crew(agents=[agent1, agent2], tasks=[task1, task2])
crew.kickoff()
print(crew.usage_metrics)
python Code theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## Crew Execution Process

* **Sequential Process**: Tasks are executed one after another, allowing for a linear flow of work.
* **Hierarchical Process**: A manager agent coordinates the crew, delegating tasks and validating outcomes before proceeding. **Note**: A `manager_llm` or `manager_agent` is required for this process and it's essential for validating the process flow.

### Kicking Off a Crew

Once your crew is assembled, initiate the workflow with the `kickoff()` method. This starts the execution process according to the defined process flow.
```

---

## Add metadata to the agent's fingerprint

**URL:** llms-txt#add-metadata-to-the-agent's-fingerprint

agent.security_config.fingerprint.metadata = {
    "version": "1.0",
    "department": "Data Science",
    "project": "Customer Analysis"
}

---

## Add tools to agent

**URL:** llms-txt#add-tools-to-agent

**Contents:**
- Agent Memory and Context
- Context Window Management
  - How Context Window Management Works
  - Automatic Context Handling (`respect_context_window=True`)

researcher = Agent(
    role="AI Technology Researcher",
    goal="Research the latest AI developments",
    tools=[search_tool, wiki_tool],
    verbose=True
)
python Code theme={null}
from crewai import Agent

analyst = Agent(
    role="Data Analyst",
    goal="Analyze and remember complex data patterns",
    memory=True,  # Enable memory
    verbose=True
)
python Code theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## Agent Memory and Context

Agents can maintain memory of their interactions and use context from previous tasks. This is particularly useful for complex workflows where information needs to be retained across multiple tasks.
```

Example 2 (unknown):
```unknown
<Note>
  When `memory` is enabled, the agent will maintain context across multiple interactions, improving its ability to handle complex, multi-step tasks.
</Note>

## Context Window Management

CrewAI includes sophisticated automatic context window management to handle situations where conversations exceed the language model's token limits. This powerful feature is controlled by the `respect_context_window` parameter.

### How Context Window Management Works

When an agent's conversation history grows too large for the LLM's context window, CrewAI automatically detects this situation and can either:

1. **Automatically summarize content** (when `respect_context_window=True`)
2. **Stop execution with an error** (when `respect_context_window=False`)

### Automatic Context Handling (`respect_context_window=True`)

This is the **default and recommended setting** for most use cases. When enabled, CrewAI will:
```

---

## Add tools to your agent

**URL:** llms-txt#add-tools-to-your-agent

**Contents:**
- **Max Usage Count**

agent = Agent(
    role="Research Analyst",
    tools=[FileReadTool(), SerperDevTool()],
    # ... other configuration
)
python theme={null}
from crewai_tools import FileReadTool

tool = FileReadTool(max_usage_count=5, ...)
```

Ready to explore? Pick a category above to discover tools that fit your use case!

**Examples:**

Example 1 (unknown):
```unknown
## **Max Usage Count**

You can set a maximum usage count for a tool to prevent it from being used more than a certain number of times.
By default, the max usage count is unlimited.
```

---

## Add to your agent

**URL:** llms-txt#add-to-your-agent

**Contents:**
- **Integration Benefits**

agent = Agent(
    role="Automation Specialist",
    tools=[apify_automation, platform_integration, browser_automation],
    goal="Automate workflows and integrate systems"
)
```

## **Integration Benefits**

* **Efficiency**: Reduce manual work through automation
* **Scalability**: Handle increased workloads automatically
* **Reliability**: Consistent execution of workflows
* **Connectivity**: Bridge different systems and platforms
* **Productivity**: Focus on high-value tasks while automation handles routine work

---

## Agents

**URL:** llms-txt#agents

**Contents:**
- Overview of an Agent
- Agent Attributes
- Creating Agents
  - YAML Configuration (Recommended)

Source: https://docs.crewai.com/en/concepts/agents

Detailed guide on creating and managing agents within the CrewAI framework.

## Overview of an Agent

In the CrewAI framework, an `Agent` is an autonomous unit that can:

* Perform specific tasks
* Make decisions based on its role and goal
* Use tools to accomplish objectives
* Communicate and collaborate with other agents
* Maintain memory of interactions
* Delegate tasks when allowed

<Tip>
  Think of an agent as a specialized team member with specific skills, expertise, and responsibilities. For example, a `Researcher` agent might excel at gathering and analyzing information, while a `Writer` agent might be better at creating content.
</Tip>

<Note type="info" title="Enterprise Enhancement: Visual Agent Builder">
  CrewAI AOP includes a Visual Agent Builder that simplifies agent creation and configuration without writing code. Design your agents visually and test them in real-time.

<img alt="Visual Agent Builder Screenshot" />

The Visual Agent Builder enables:

* Intuitive agent configuration with form-based interfaces
  * Real-time testing and validation
  * Template library with pre-configured agent types
  * Easy customization of agent attributes and behaviors
</Note>

| Attribute                               | Parameter                | Type                                  | Description                                                                                              |
| :-------------------------------------- | :----------------------- | :------------------------------------ | :------------------------------------------------------------------------------------------------------- |
| **Role**                                | `role`                   | `str`                                 | Defines the agent's function and expertise within the crew.                                              |
| **Goal**                                | `goal`                   | `str`                                 | The individual objective that guides the agent's decision-making.                                        |
| **Backstory**                           | `backstory`              | `str`                                 | Provides context and personality to the agent, enriching interactions.                                   |
| **LLM** *(optional)*                    | `llm`                    | `Union[str, LLM, Any]`                | Language model that powers the agent. Defaults to the model specified in `OPENAI_MODEL_NAME` or "gpt-4". |
| **Tools** *(optional)*                  | `tools`                  | `List[BaseTool]`                      | Capabilities or functions available to the agent. Defaults to an empty list.                             |
| **Function Calling LLM** *(optional)*   | `function_calling_llm`   | `Optional[Any]`                       | Language model for tool calling, overrides crew's LLM if specified.                                      |
| **Max Iterations** *(optional)*         | `max_iter`               | `int`                                 | Maximum iterations before the agent must provide its best answer. Default is 20.                         |
| **Max RPM** *(optional)*                | `max_rpm`                | `Optional[int]`                       | Maximum requests per minute to avoid rate limits.                                                        |
| **Max Execution Time** *(optional)*     | `max_execution_time`     | `Optional[int]`                       | Maximum time (in seconds) for task execution.                                                            |
| **Verbose** *(optional)*                | `verbose`                | `bool`                                | Enable detailed execution logs for debugging. Default is False.                                          |
| **Allow Delegation** *(optional)*       | `allow_delegation`       | `bool`                                | Allow the agent to delegate tasks to other agents. Default is False.                                     |
| **Step Callback** *(optional)*          | `step_callback`          | `Optional[Any]`                       | Function called after each agent step, overrides crew callback.                                          |
| **Cache** *(optional)*                  | `cache`                  | `bool`                                | Enable caching for tool usage. Default is True.                                                          |
| **System Template** *(optional)*        | `system_template`        | `Optional[str]`                       | Custom system prompt template for the agent.                                                             |
| **Prompt Template** *(optional)*        | `prompt_template`        | `Optional[str]`                       | Custom prompt template for the agent.                                                                    |
| **Response Template** *(optional)*      | `response_template`      | `Optional[str]`                       | Custom response template for the agent.                                                                  |
| **Allow Code Execution** *(optional)*   | `allow_code_execution`   | `Optional[bool]`                      | Enable code execution for the agent. Default is False.                                                   |
| **Max Retry Limit** *(optional)*        | `max_retry_limit`        | `int`                                 | Maximum number of retries when an error occurs. Default is 2.                                            |
| **Respect Context Window** *(optional)* | `respect_context_window` | `bool`                                | Keep messages under context window size by summarizing. Default is True.                                 |
| **Code Execution Mode** *(optional)*    | `code_execution_mode`    | `Literal["safe", "unsafe"]`           | Mode for code execution: 'safe' (using Docker) or 'unsafe' (direct). Default is 'safe'.                  |
| **Multimodal** *(optional)*             | `multimodal`             | `bool`                                | Whether the agent supports multimodal capabilities. Default is False.                                    |
| **Inject Date** *(optional)*            | `inject_date`            | `bool`                                | Whether to automatically inject the current date into tasks. Default is False.                           |
| **Date Format** *(optional)*            | `date_format`            | `str`                                 | Format string for date when inject\_date is enabled. Default is "%Y-%m-%d" (ISO format).                 |
| **Reasoning** *(optional)*              | `reasoning`              | `bool`                                | Whether the agent should reflect and create a plan before executing a task. Default is False.            |
| **Max Reasoning Attempts** *(optional)* | `max_reasoning_attempts` | `Optional[int]`                       | Maximum number of reasoning attempts before executing the task. If None, will try until ready.           |
| **Embedder** *(optional)*               | `embedder`               | `Optional[Dict[str, Any]]`            | Configuration for the embedder used by the agent.                                                        |
| **Knowledge Sources** *(optional)*      | `knowledge_sources`      | `Optional[List[BaseKnowledgeSource]]` | Knowledge sources available to the agent.                                                                |
| **Use System Prompt** *(optional)*      | `use_system_prompt`      | `Optional[bool]`                      | Whether to use system prompt (for o1 model support). Default is True.                                    |

There are two ways to create agents in CrewAI: using **YAML configuration (recommended)** or defining them **directly in code**.

### YAML Configuration (Recommended)

Using YAML configuration provides a cleaner, more maintainable way to define agents. We strongly recommend using this approach in your CrewAI projects.

After creating your CrewAI project as outlined in the [Installation](/en/installation) section, navigate to the `src/latest_ai_development/config/agents.yaml` file and modify the template to match your requirements.

<Note>
  Variables in your YAML files (like `{topic}`) will be replaced with values from your inputs when running the crew:

Here's an example of how to configure agents using YAML:

```yaml agents.yaml theme={null}

**Examples:**

Example 1 (unknown):
```unknown
</Note>

Here's an example of how to configure agents using YAML:
```

---

## Agents are defined with attributes for backstory, cache, and verbose mode

**URL:** llms-txt#agents-are-defined-with-attributes-for-backstory,-cache,-and-verbose-mode

researcher = Agent(
    role='Researcher',
    goal='Conduct in-depth analysis',
    backstory='Experienced data analyst with a knack for uncovering hidden trends.',
)
writer = Agent(
    role='Writer',
    goal='Create engaging content',
    backstory='Creative writer passionate about storytelling in technical domains.',
)

---

## Agents can now collaborate automatically

**URL:** llms-txt#agents-can-now-collaborate-automatically

**Contents:**
- How Agent Collaboration Works
  - 1. **Delegate Work Tool**

crew = Crew(
    agents=[researcher, writer],
    tasks=[...],
    verbose=True
)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## How Agent Collaboration Works

When `allow_delegation=True`, CrewAI automatically provides agents with two powerful tools:

### 1. **Delegate Work Tool**

Allows agents to assign tasks to teammates with specific expertise.
```

---

## Agent automatically gets this tool:

**URL:** llms-txt#agent-automatically-gets-this-tool:

---

## Agent creation is fast - no MCP connections made yet

**URL:** llms-txt#agent-creation-is-fast---no-mcp-connections-made-yet

agent = Agent(
    role="On-Demand Agent",
    goal="Use tools efficiently",
    backstory="Efficient agent that connects only when needed",
    mcps=["https://api.example.com/mcp"]
)

---

## Agent knowledge storage

**URL:** llms-txt#agent-knowledge-storage

agent_collection_name = agent.role  # e.g., "Technical Specialist"

---

## Agent Repositories

**URL:** llms-txt#agent-repositories

**Contents:**
- Benefits of Agent Repositories
- Creating and Use Agent Repositories
  - Loading Agents from Repositories

Source: https://docs.crewai.com/en/enterprise/features/agent-repositories

Learn how to use Agent Repositories to share and reuse your agents across teams and projects

Agent Repositories allow enterprise users to store, share, and reuse agent definitions across teams and projects. This feature enables organizations to maintain a centralized library of standardized agents, promoting consistency and reducing duplication of effort.

<Frame>
  <img alt="Agent Repositories" />
</Frame>

## Benefits of Agent Repositories

* **Standardization**: Maintain consistent agent definitions across your organization
* **Reusability**: Create an agent once and use it in multiple crews and projects
* **Governance**: Implement organization-wide policies for agent configurations
* **Collaboration**: Enable teams to share and build upon each other's work

## Creating and Use Agent Repositories

1. You must have an account at CrewAI, try the [free plan](https://app.crewai.com).
2. Create agents with specific roles and goals for your workflows.
3. Configure tools and capabilities for each specialized assistant.
4. Deploy agents across projects via visual interface or API integration.

<Frame>
  <img alt="Agent Repositories" />
</Frame>

### Loading Agents from Repositories

You can load agents from repositories in your code using the `from_repository` parameter to run locally:

```python theme={null}
from crewai import Agent

---

## Agent-specific knowledge

**URL:** llms-txt#agent-specific-knowledge

specialist_knowledge = StringKnowledgeSource(
    content="Technical specifications only the specialist needs"
)

specialist = Agent(
    role="Technical Specialist",
    goal="Provide technical expertise",
    backstory="Technical expert",
    knowledge_sources=[specialist_knowledge]  # Agent-specific
)

generalist = Agent(
    role="General Assistant", 
    goal="Provide general assistance",
    backstory="General helper"
    # No agent-specific knowledge
)

crew = Crew(
    agents=[specialist, generalist],
    tasks=[...],
    knowledge_sources=[crew_knowledge]  # Crew-wide knowledge
)

---

## Agent will:

**URL:** llms-txt#agent-will:

---

## Agent will need to provide the CSV path at runtime.

**URL:** llms-txt#agent-will-need-to-provide-the-csv-path-at-runtime.

**Contents:**
- Arguments
- Custom model and embeddings

tool = CSVSearchTool()
python Code theme={null}
from chromadb.config import Settings

tool = CSVSearchTool(
    config={
        "embedding_model": {
            "provider": "openai",
            "config": {
                "model": "text-embedding-3-small",
                # "api_key": "sk-...",
            },
        },
        "vectordb": {
            "provider": "chromadb",  # or "qdrant"
            "config": {
                # "settings": Settings(persist_directory="/content/chroma", allow_reset=True, is_persistent=True),
                # from qdrant_client.models import VectorParams, Distance
                # "vectors_config": VectorParams(size=384, distance=Distance.COSINE),
            }
        },
    }
)
```

**Examples:**

Example 1 (unknown):
```unknown
## Arguments

The following parameters can be used to customize the `CSVSearchTool`'s behavior:

| Argument | Type     | Description                                                                                                                                                               |
| :------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **csv**  | `string` | *Optional*. The path to the CSV file you want to search. This is a mandatory argument if the tool was initialized without a specific CSV file; otherwise, it is optional. |

## Custom model and embeddings

By default, the tool uses OpenAI for both embeddings and summarization. To customize the model, you can use a config dictionary as follows:
```

---

## Agent will use these parameters when calling the tool

**URL:** llms-txt#agent-will-use-these-parameters-when-calling-the-tool

---

## Agent will use tools from working servers and log warnings for failing ones

**URL:** llms-txt#agent-will-use-tools-from-working-servers-and-log-warnings-for-failing-ones

**Contents:**
- Advanced: MCPServerAdapter
- Connection Configuration

**Examples:**

Example 1 (unknown):
```unknown
All connection errors are handled gracefully:

* **Connection failures**: Logged as warnings, agent continues with available tools
* **Timeout errors**: Connections timeout after 30 seconds (configurable)
* **Authentication errors**: Logged clearly for debugging
* **Invalid configurations**: Validation errors are raised at agent creation time

## Advanced: MCPServerAdapter

For complex scenarios requiring manual connection management, use the `MCPServerAdapter` class from `crewai-tools`. Using a Python context manager (`with` statement) is the recommended approach as it automatically handles starting and stopping the connection to the MCP server.

## Connection Configuration

The `MCPServerAdapter` supports several configuration options to customize the connection behavior:

* **`connect_timeout`** (optional): Maximum time in seconds to wait for establishing a connection to the MCP server. Defaults to 30 seconds if not specified. This is particularly useful for remote servers that may have variable response times.
```

---

## Agent with automatic context management (default)

**URL:** llms-txt#agent-with-automatic-context-management-(default)

**Contents:**
  - Strict Context Limits (`respect_context_window=False`)

smart_agent = Agent(
    role="Research Analyst",
    goal="Analyze large documents and datasets",
    backstory="Expert at processing extensive information",
    respect_context_window=True,  # 🔑 Default: auto-handle context limits
    verbose=True
)
python Code theme={null}

**Examples:**

Example 1 (unknown):
```unknown
**What happens when context limits are exceeded:**

* ⚠️ **Warning message**: `"Context length exceeded. Summarizing content to fit the model context window."`
* 🔄 **Automatic summarization**: CrewAI intelligently summarizes the conversation history
* ✅ **Continued execution**: Task execution continues seamlessly with the summarized context
* 📝 **Preserved information**: Key information is retained while reducing token count

### Strict Context Limits (`respect_context_window=False`)

When you need precise control and prefer execution to stop rather than lose any information:
```

---

## Agent with its own knowledge - NO crew knowledge needed

**URL:** llms-txt#agent-with-its-own-knowledge---no-crew-knowledge-needed

specialist_knowledge = StringKnowledgeSource(
    content="Specialized technical information for this agent only"
)

specialist_agent = Agent(
    role="Technical Specialist",
    goal="Provide technical expertise",
    backstory="Expert in specialized technical domains",
    knowledge_sources=[specialist_knowledge]  # Agent-specific knowledge
)

task = Task(
    description="Answer technical questions",
    agent=specialist_agent,
    expected_output="Technical answer"
)

---

## Agent with strict context limits

**URL:** llms-txt#agent-with-strict-context-limits

**Contents:**
  - Choosing the Right Setting

strict_agent = Agent(
    role="Legal Document Reviewer",
    goal="Provide precise legal analysis without information loss",
    backstory="Legal expert requiring complete context for accurate analysis",
    respect_context_window=False,  # ❌ Stop execution on context limit
    verbose=True
)
python Code theme={null}

**Examples:**

Example 1 (unknown):
```unknown
**What happens when context limits are exceeded:**

* ❌ **Error message**: `"Context length exceeded. Consider using smaller text or RAG tools from crewai_tools."`
* 🛑 **Execution stops**: Task execution halts immediately
* 🔧 **Manual intervention required**: You need to modify your approach

### Choosing the Right Setting

#### Use `respect_context_window=True` (Default) when:

* **Processing large documents** that might exceed context limits
* **Long-running conversations** where some summarization is acceptable
* **Research tasks** where general context is more important than exact details
* **Prototyping and development** where you want robust execution
```

---

## Allow agents to search within any XML file's content

**URL:** llms-txt#allow-agents-to-search-within-any-xml-file's-content

#as it learns about their paths during execution
tool = XMLSearchTool()

---

## All knowledge will now be stored in ./my_project_storage/knowledge/

**URL:** llms-txt#all-knowledge-will-now-be-stored-in-./my_project_storage/knowledge/

crew = Crew(
    agents=[...],
    tasks=[...],
    knowledge_sources=[...]
)
python theme={null}
from crewai.knowledge.storage.knowledge_storage import KnowledgeStorage
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

**Examples:**

Example 1 (unknown):
```unknown
#### Option 2: Custom Knowledge Storage
```

---

## All memory and knowledge will now be stored in ./my_project_storage/

**URL:** llms-txt#all-memory-and-knowledge-will-now-be-stored-in-./my_project_storage/

crew = Crew(
    agents=[...],
    tasks=[...],
    memory=True
)
python theme={null}
import os
from crewai import Crew
from crewai.memory import LongTermMemory
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage

**Examples:**

Example 1 (unknown):
```unknown
#### Option 2: Custom Storage Paths
```

---

## Arize Phoenix Integration

**URL:** llms-txt#arize-phoenix-integration

**Contents:**
- Get Started
  - Step 1: Install Dependencies
  - Step 2: Set Up Environment Variables

This guide demonstrates how to integrate **Arize Phoenix** with **CrewAI** using OpenTelemetry via the [OpenInference](https://github.com/openinference/openinference) SDK. By the end of this guide, you will be able to trace your CrewAI agents and easily debug your agents.

> **What is Arize Phoenix?** [Arize Phoenix](https://phoenix.arize.com) is an LLM observability platform that provides tracing and evaluation for AI applications.

[![Watch a Video Demo of Our Integration with Phoenix](https://storage.googleapis.com/arize-assets/fixtures/setup_crewai.png)](https://www.youtube.com/watch?v=Yc5q3l6F7Ww)

We'll walk through a simple example of using CrewAI and integrating it with Arize Phoenix via OpenTelemetry using OpenInference.

You can also access this guide on [Google Colab](https://colab.research.google.com/github/Arize-ai/phoenix/blob/main/tutorials/tracing/crewai_tracing_tutorial.ipynb).

### Step 1: Install Dependencies

### Step 2: Set Up Environment Variables

Setup Phoenix Cloud API keys and configure OpenTelemetry to send traces to Phoenix. Phoenix Cloud is a hosted version of Arize Phoenix, but it is not required to use this integration.

You can get your free Serper API key [here](https://serper.dev/).

```python theme={null}
import os
from getpass import getpass

**Examples:**

Example 1 (unknown):
```unknown
### Step 2: Set Up Environment Variables

Setup Phoenix Cloud API keys and configure OpenTelemetry to send traces to Phoenix. Phoenix Cloud is a hosted version of Arize Phoenix, but it is not required to use this integration.

You can get your free Serper API key [here](https://serper.dev/).
```

---

## Asana Integration

**URL:** llms-txt#asana-integration

**Contents:**
- Overview
- Prerequisites
- Setting Up Asana Integration
  - 1. Connect Your Asana Account
  - 2. Install Required Package
  - 3. Environment Variable Setup
- Available Actions
- Usage Examples
  - Basic Asana Agent Setup

Source: https://docs.crewai.com/en/enterprise/integrations/asana

Team task and project coordination with Asana integration for CrewAI.

Enable your agents to manage tasks, projects, and team coordination through Asana. Create tasks, update project status, manage assignments, and streamline your team's workflow with AI-powered automation.

Before using the Asana integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* An Asana account with appropriate permissions
* Connected your Asana account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)

## Setting Up Asana Integration

### 1. Connect Your Asana Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Asana** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for task and project management
5. Copy your Enterprise Token from [Integration Settings](https://app.crewai.com/crewai_plus/settings/integrations)

### 2. Install Required Package

### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>

Or add it to your `.env` file:

<AccordionGroup>
  <Accordion title="asana/create_comment">
    **Description:** Create a comment in Asana.

* `task` (string, required): Task ID - The ID of the Task the comment will be added to. The comment will be authored by the currently authenticated user.
    * `text` (string, required): Text (example: "This is a comment.").
  </Accordion>

<Accordion title="asana/create_project">
    **Description:** Create a project in Asana.

* `name` (string, required): Name (example: "Stuff to buy").
    * `workspace` (string, required): Workspace - Use Connect Portal Workflow Settings to allow users to select which Workspace to create Projects in. Defaults to the user's first Workspace if left blank.
    * `team` (string, optional): Team - Use Connect Portal Workflow Settings to allow users to select which Team to share this Project with. Defaults to the user's first Team if left blank.
    * `notes` (string, optional): Notes (example: "These are things we need to purchase.").
  </Accordion>

<Accordion title="asana/get_projects">
    **Description:** Get a list of projects in Asana.

* `archived` (string, optional): Archived - Choose "true" to show archived projects, "false" to display only active projects, or "default" to show both archived and active projects.
      * Options: `default`, `true`, `false`
  </Accordion>

<Accordion title="asana/get_project_by_id">
    **Description:** Get a project by ID in Asana.

* `projectFilterId` (string, required): Project ID.
  </Accordion>

<Accordion title="asana/create_task">
    **Description:** Create a task in Asana.

* `name` (string, required): Name (example: "Task Name").
    * `workspace` (string, optional): Workspace - Use Connect Portal Workflow Settings to allow users to select which Workspace to create Tasks in. Defaults to the user's first Workspace if left blank..
    * `project` (string, optional): Project - Use Connect Portal Workflow Settings to allow users to select which Project to create this Task in.
    * `notes` (string, optional): Notes.
    * `dueOnDate` (string, optional): Due On - The date on which this task is due. Cannot be used together with Due At. (example: "YYYY-MM-DD").
    * `dueAtDate` (string, optional): Due At - The date and time (ISO timestamp) at which this task is due. Cannot be used together with Due On. (example: "2019-09-15T02:06:58.147Z").
    * `assignee` (string, optional): Assignee - The ID of the Asana user this task will be assigned to. Use Connect Portal Workflow Settings to allow users to select an Assignee.
    * `gid` (string, optional): External ID - An ID from your application to associate this task with. You can use this ID to sync updates to this task later.
  </Accordion>

<Accordion title="asana/update_task">
    **Description:** Update a task in Asana.

* `taskId` (string, required): Task ID - The ID of the Task that will be updated.
    * `completeStatus` (string, optional): Completed Status.
      * Options: `true`, `false`
    * `name` (string, optional): Name (example: "Task Name").
    * `notes` (string, optional): Notes.
    * `dueOnDate` (string, optional): Due On - The date on which this task is due. Cannot be used together with Due At. (example: "YYYY-MM-DD").
    * `dueAtDate` (string, optional): Due At - The date and time (ISO timestamp) at which this task is due. Cannot be used together with Due On. (example: "2019-09-15T02:06:58.147Z").
    * `assignee` (string, optional): Assignee - The ID of the Asana user this task will be assigned to. Use Connect Portal Workflow Settings to allow users to select an Assignee.
    * `gid` (string, optional): External ID - An ID from your application to associate this task with. You can use this ID to sync updates to this task later.
  </Accordion>

<Accordion title="asana/get_tasks">
    **Description:** Get a list of tasks in Asana.

* `workspace` (string, optional): Workspace - The ID of the Workspace to filter tasks on. Use Connect Portal Workflow Settings to allow users to select a Workspace.
    * `project` (string, optional): Project - The ID of the Project to filter tasks on. Use Connect Portal Workflow Settings to allow users to select a Project.
    * `assignee` (string, optional): Assignee - The ID of the assignee to filter tasks on. Use Connect Portal Workflow Settings to allow users to select an Assignee.
    * `completedSince` (string, optional): Completed since - Only return tasks that are either incomplete or that have been completed since this time (ISO or Unix timestamp). (example: "2014-04-25T16:15:47-04:00").
  </Accordion>

<Accordion title="asana/get_tasks_by_id">
    **Description:** Get a list of tasks by ID in Asana.

* `taskId` (string, required): Task ID.
  </Accordion>

<Accordion title="asana/get_task_by_external_id">
    **Description:** Get a task by external ID in Asana.

* `gid` (string, required): External ID - The ID that this task is associated or synced with, from your application.
  </Accordion>

<Accordion title="asana/add_task_to_section">
    **Description:** Add a task to a section in Asana.

* `sectionId` (string, required): Section ID - The ID of the section to add this task to.
    * `taskId` (string, required): Task ID - The ID of the task. (example: "1204619611402340").
    * `beforeTaskId` (string, optional): Before Task ID - The ID of a task in this section that this task will be inserted before. Cannot be used with After Task ID. (example: "1204619611402340").
    * `afterTaskId` (string, optional): After Task ID - The ID of a task in this section that this task will be inserted after. Cannot be used with Before Task ID. (example: "1204619611402340").
  </Accordion>

<Accordion title="asana/get_teams">
    **Description:** Get a list of teams in Asana.

* `workspace` (string, required): Workspace - Returns the teams in this workspace visible to the authorized user.
  </Accordion>

<Accordion title="asana/get_workspaces">
    **Description:** Get a list of workspaces in Asana.

**Parameters:** None required.
  </Accordion>
</AccordionGroup>

### Basic Asana Agent Setup

```python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

Example 3 (unknown):
```unknown
## Available Actions

<AccordionGroup>
  <Accordion title="asana/create_comment">
    **Description:** Create a comment in Asana.

    **Parameters:**

    * `task` (string, required): Task ID - The ID of the Task the comment will be added to. The comment will be authored by the currently authenticated user.
    * `text` (string, required): Text (example: "This is a comment.").
  </Accordion>

  <Accordion title="asana/create_project">
    **Description:** Create a project in Asana.

    **Parameters:**

    * `name` (string, required): Name (example: "Stuff to buy").
    * `workspace` (string, required): Workspace - Use Connect Portal Workflow Settings to allow users to select which Workspace to create Projects in. Defaults to the user's first Workspace if left blank.
    * `team` (string, optional): Team - Use Connect Portal Workflow Settings to allow users to select which Team to share this Project with. Defaults to the user's first Team if left blank.
    * `notes` (string, optional): Notes (example: "These are things we need to purchase.").
  </Accordion>

  <Accordion title="asana/get_projects">
    **Description:** Get a list of projects in Asana.

    **Parameters:**

    * `archived` (string, optional): Archived - Choose "true" to show archived projects, "false" to display only active projects, or "default" to show both archived and active projects.
      * Options: `default`, `true`, `false`
  </Accordion>

  <Accordion title="asana/get_project_by_id">
    **Description:** Get a project by ID in Asana.

    **Parameters:**

    * `projectFilterId` (string, required): Project ID.
  </Accordion>

  <Accordion title="asana/create_task">
    **Description:** Create a task in Asana.

    **Parameters:**

    * `name` (string, required): Name (example: "Task Name").
    * `workspace` (string, optional): Workspace - Use Connect Portal Workflow Settings to allow users to select which Workspace to create Tasks in. Defaults to the user's first Workspace if left blank..
    * `project` (string, optional): Project - Use Connect Portal Workflow Settings to allow users to select which Project to create this Task in.
    * `notes` (string, optional): Notes.
    * `dueOnDate` (string, optional): Due On - The date on which this task is due. Cannot be used together with Due At. (example: "YYYY-MM-DD").
    * `dueAtDate` (string, optional): Due At - The date and time (ISO timestamp) at which this task is due. Cannot be used together with Due On. (example: "2019-09-15T02:06:58.147Z").
    * `assignee` (string, optional): Assignee - The ID of the Asana user this task will be assigned to. Use Connect Portal Workflow Settings to allow users to select an Assignee.
    * `gid` (string, optional): External ID - An ID from your application to associate this task with. You can use this ID to sync updates to this task later.
  </Accordion>

  <Accordion title="asana/update_task">
    **Description:** Update a task in Asana.

    **Parameters:**

    * `taskId` (string, required): Task ID - The ID of the Task that will be updated.
    * `completeStatus` (string, optional): Completed Status.
      * Options: `true`, `false`
    * `name` (string, optional): Name (example: "Task Name").
    * `notes` (string, optional): Notes.
    * `dueOnDate` (string, optional): Due On - The date on which this task is due. Cannot be used together with Due At. (example: "YYYY-MM-DD").
    * `dueAtDate` (string, optional): Due At - The date and time (ISO timestamp) at which this task is due. Cannot be used together with Due On. (example: "2019-09-15T02:06:58.147Z").
    * `assignee` (string, optional): Assignee - The ID of the Asana user this task will be assigned to. Use Connect Portal Workflow Settings to allow users to select an Assignee.
    * `gid` (string, optional): External ID - An ID from your application to associate this task with. You can use this ID to sync updates to this task later.
  </Accordion>

  <Accordion title="asana/get_tasks">
    **Description:** Get a list of tasks in Asana.

    **Parameters:**

    * `workspace` (string, optional): Workspace - The ID of the Workspace to filter tasks on. Use Connect Portal Workflow Settings to allow users to select a Workspace.
    * `project` (string, optional): Project - The ID of the Project to filter tasks on. Use Connect Portal Workflow Settings to allow users to select a Project.
    * `assignee` (string, optional): Assignee - The ID of the assignee to filter tasks on. Use Connect Portal Workflow Settings to allow users to select an Assignee.
    * `completedSince` (string, optional): Completed since - Only return tasks that are either incomplete or that have been completed since this time (ISO or Unix timestamp). (example: "2014-04-25T16:15:47-04:00").
  </Accordion>

  <Accordion title="asana/get_tasks_by_id">
    **Description:** Get a list of tasks by ID in Asana.

    **Parameters:**

    * `taskId` (string, required): Task ID.
  </Accordion>

  <Accordion title="asana/get_task_by_external_id">
    **Description:** Get a task by external ID in Asana.

    **Parameters:**

    * `gid` (string, required): External ID - The ID that this task is associated or synced with, from your application.
  </Accordion>

  <Accordion title="asana/add_task_to_section">
    **Description:** Add a task to a section in Asana.

    **Parameters:**

    * `sectionId` (string, required): Section ID - The ID of the section to add this task to.
    * `taskId` (string, required): Task ID - The ID of the task. (example: "1204619611402340").
    * `beforeTaskId` (string, optional): Before Task ID - The ID of a task in this section that this task will be inserted before. Cannot be used with After Task ID. (example: "1204619611402340").
    * `afterTaskId` (string, optional): After Task ID - The ID of a task in this section that this task will be inserted after. Cannot be used with Before Task ID. (example: "1204619611402340").
  </Accordion>

  <Accordion title="asana/get_teams">
    **Description:** Get a list of teams in Asana.

    **Parameters:**

    * `workspace` (string, required): Workspace - Returns the teams in this workspace visible to the authorized user.
  </Accordion>

  <Accordion title="asana/get_workspaces">
    **Description:** Get a list of workspaces in Asana.

    **Parameters:** None required.
  </Accordion>
</AccordionGroup>

## Usage Examples

### Basic Asana Agent Setup
```

---

## Assemble a crew with planning enabled

**URL:** llms-txt#assemble-a-crew-with-planning-enabled

crew = Crew(
    agents=[researcher, writer],
    tasks=[research, write],
    verbose=True,
    planning=True,  # Enable planning feature
)

---

## Basic OpenAI configuration (uses environment OPENAI_API_KEY)

**URL:** llms-txt#basic-openai-configuration-(uses-environment-openai_api_key)

crew = Crew(
    agents=[...],
    tasks=[...],
    memory=True,
    embedder={
        "provider": "openai",
        "config": {
            "model_name": "text-embedding-3-small"  # or "text-embedding-3-large"
        }
    }
)

---

## `BedrockInvokeAgentTool`

**URL:** llms-txt#`bedrockinvokeagenttool`

**Contents:**
- Installation
- Requirements
- Usage

The `BedrockInvokeAgentTool` enables CrewAI agents to invoke Amazon Bedrock Agents and leverage their capabilities within your workflows.

* AWS credentials configured (either through environment variables or AWS CLI)
* `boto3` and `python-dotenv` packages
* Access to Amazon Bedrock Agents

Here's how to use the tool with a CrewAI agent:

```python {2, 4-8} theme={null}
from crewai import Agent, Task, Crew
from crewai_tools.aws.bedrock.agents.invoke_agent_tool import BedrockInvokeAgentTool

**Examples:**

Example 1 (unknown):
```unknown
## Requirements

* AWS credentials configured (either through environment variables or AWS CLI)
* `boto3` and `python-dotenv` packages
* Access to Amazon Bedrock Agents

## Usage

Here's how to use the tool with a CrewAI agent:
```

---

## `BedrockKBRetrieverTool`

**URL:** llms-txt#`bedrockkbretrievertool`

**Contents:**
- Installation
- Requirements
- Usage

The `BedrockKBRetrieverTool` enables CrewAI agents to retrieve information from Amazon Bedrock Knowledge Bases using natural language queries.

* AWS credentials configured (either through environment variables or AWS CLI)
* `boto3` and `python-dotenv` packages
* Access to Amazon Bedrock Knowledge Base

Here's how to use the tool with a CrewAI agent:

```python {2, 4-17} theme={null}
from crewai import Agent, Task, Crew
from crewai_tools.aws.bedrock.knowledge_base.retriever_tool import BedrockKBRetrieverTool

**Examples:**

Example 1 (unknown):
```unknown
## Requirements

* AWS credentials configured (either through environment variables or AWS CLI)
* `boto3` and `python-dotenv` packages
* Access to Amazon Bedrock Knowledge Base

## Usage

Here's how to use the tool with a CrewAI agent:
```

---

## Bedrock Invoke Agent Tool

**URL:** llms-txt#bedrock-invoke-agent-tool

Source: https://docs.crewai.com/en/tools/integration/bedrockinvokeagenttool

Enables CrewAI agents to invoke Amazon Bedrock Agents and leverage their capabilities within your workflows

---

## Box Integration

**URL:** llms-txt#box-integration

**Contents:**
- Overview
- Prerequisites
- Setting Up Box Integration
  - 1. Connect Your Box Account
  - 2. Install Required Package
  - 3. Environment Variable Setup
- Available Actions
- Usage Examples
  - Basic Box Agent Setup

Source: https://docs.crewai.com/en/enterprise/integrations/box

File storage and document management with Box integration for CrewAI.

Enable your agents to manage files, folders, and documents through Box. Upload files, organize folder structures, search content, and streamline your team's document management with AI-powered automation.

Before using the Box integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A Box account with appropriate permissions
* Connected your Box account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)

## Setting Up Box Integration

### 1. Connect Your Box Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Box** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for file and folder management
5. Copy your Enterprise Token from [Integration Settings](https://app.crewai.com/crewai_plus/settings/integrations)

### 2. Install Required Package

### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>

Or add it to your `.env` file:

<AccordionGroup>
  <Accordion title="box/save_file">
    **Description:** Save a file from URL in Box.

* `fileAttributes` (object, required): Attributes - File metadata including name, parent folder, and timestamps.
      
    * `file` (string, required): File URL - Files must be smaller than 50MB in size. (example: "[https://picsum.photos/200/300](https://picsum.photos/200/300)").
  </Accordion>

<Accordion title="box/save_file_from_object">
    **Description:** Save a file in Box.

* `file` (string, required): File - Accepts a File Object containing file data. Files must be smaller than 50MB in size.
    * `fileName` (string, required): File Name (example: "qwerty.png").
    * `folder` (string, optional): Folder - Use Connect Portal Workflow Settings to allow users to select the File's Folder destination. Defaults to the user's root folder if left blank.
  </Accordion>

<Accordion title="box/get_file_by_id">
    **Description:** Get a file by ID in Box.

* `fileId` (string, required): File ID - The unique identifier that represents a file. (example: "12345").
  </Accordion>

<Accordion title="box/list_files">
    **Description:** List files in Box.

* `folderId` (string, required): Folder ID - The unique identifier that represents a folder. (example: "0").
    * `filterFormula` (object, optional): A filter in disjunctive normal form - OR of AND groups of single conditions.
      
  </Accordion>

<Accordion title="box/create_folder">
    **Description:** Create a folder in Box.

* `folderName` (string, required): Name - The name for the new folder. (example: "New Folder").
    * `folderParent` (object, required): Parent Folder - The parent folder where the new folder will be created.
      
  </Accordion>

<Accordion title="box/move_folder">
    **Description:** Move a folder in Box.

* `folderId` (string, required): Folder ID - The unique identifier that represents a folder. (example: "0").
    * `folderName` (string, required): Name - The name for the folder. (example: "New Folder").
    * `folderParent` (object, required): Parent Folder - The new parent folder destination.
      
  </Accordion>

<Accordion title="box/get_folder_by_id">
    **Description:** Get a folder by ID in Box.

* `folderId` (string, required): Folder ID - The unique identifier that represents a folder. (example: "0").
  </Accordion>

<Accordion title="box/search_folders">
    **Description:** Search folders in Box.

* `folderId` (string, required): Folder ID - The folder to search within.
    * `filterFormula` (object, optional): A filter in disjunctive normal form - OR of AND groups of single conditions.
      
  </Accordion>

<Accordion title="box/delete_folder">
    **Description:** Delete a folder in Box.

* `folderId` (string, required): Folder ID - The unique identifier that represents a folder. (example: "0").
    * `recursive` (boolean, optional): Recursive - Delete a folder that is not empty by recursively deleting the folder and all of its content.
  </Accordion>
</AccordionGroup>

### Basic Box Agent Setup

```python theme={null}
from crewai import Agent, Task, Crew
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

Example 3 (unknown):
```unknown
## Available Actions

<AccordionGroup>
  <Accordion title="box/save_file">
    **Description:** Save a file from URL in Box.

    **Parameters:**

    * `fileAttributes` (object, required): Attributes - File metadata including name, parent folder, and timestamps.
```

Example 4 (unknown):
```unknown
* `file` (string, required): File URL - Files must be smaller than 50MB in size. (example: "[https://picsum.photos/200/300](https://picsum.photos/200/300)").
  </Accordion>

  <Accordion title="box/save_file_from_object">
    **Description:** Save a file in Box.

    **Parameters:**

    * `file` (string, required): File - Accepts a File Object containing file data. Files must be smaller than 50MB in size.
    * `fileName` (string, required): File Name (example: "qwerty.png").
    * `folder` (string, optional): Folder - Use Connect Portal Workflow Settings to allow users to select the File's Folder destination. Defaults to the user's root folder if left blank.
  </Accordion>

  <Accordion title="box/get_file_by_id">
    **Description:** Get a file by ID in Box.

    **Parameters:**

    * `fileId` (string, required): File ID - The unique identifier that represents a file. (example: "12345").
  </Accordion>

  <Accordion title="box/list_files">
    **Description:** List files in Box.

    **Parameters:**

    * `folderId` (string, required): Folder ID - The unique identifier that represents a folder. (example: "0").
    * `filterFormula` (object, optional): A filter in disjunctive normal form - OR of AND groups of single conditions.
```

---

## Braintrust Integration

**URL:** llms-txt#braintrust-integration

**Contents:**
- Get Started
  - Step 1: Install Dependencies
  - Step 2: Set Up Environment Variables

This guide demonstrates how to integrate **Braintrust** with **CrewAI** using OpenTelemetry for comprehensive tracing and evaluation. By the end of this guide, you will be able to trace your CrewAI agents, monitor their performance, and evaluate their outputs using Braintrust's powerful observability platform.

> **What is Braintrust?** [Braintrust](https://www.braintrust.dev) is an AI evaluation and observability platform that provides comprehensive tracing, evaluation, and monitoring for AI applications with built-in experiment tracking and performance analytics.

We'll walk through a simple example of using CrewAI and integrating it with Braintrust via OpenTelemetry for comprehensive observability and evaluation.

### Step 1: Install Dependencies

### Step 2: Set Up Environment Variables

Setup Braintrust API keys and configure OpenTelemetry to send traces to Braintrust. You'll need a Braintrust API key and your OpenAI API key.

```python theme={null}
import os
from getpass import getpass

**Examples:**

Example 1 (unknown):
```unknown
### Step 2: Set Up Environment Variables

Setup Braintrust API keys and configure OpenTelemetry to send traces to Braintrust. You'll need a Braintrust API key and your OpenAI API key.
```

---

## Build Crew

**URL:** llms-txt#build-crew

**Contents:**
- Overview
- Getting Started
  - Installation and Setup
  - Building Your Crew
- Support and Resources

Source: https://docs.crewai.com/en/enterprise/guides/build-crew

A Crew is a group of agents that work together to complete a task.

[CrewAI AOP](https://app.crewai.com) streamlines the process of **creating**, **deploying**, and **managing** your AI agents in production environments.

<iframe title="Building crews with the CrewAI CLI" />

### Installation and Setup

<Card title="Follow Standard Installation" icon="wrench" href="/en/installation">
  Follow our standard installation guide to set up CrewAI CLI and create your first project.
</Card>

### Building Your Crew

<Card title="Quickstart Tutorial" icon="rocket" href="/en/quickstart">
  Follow our quickstart guide to create your first agent crew using YAML configuration.
</Card>

## Support and Resources

For Enterprise-specific support or questions, contact our dedicated support team at [support@crewai.com](mailto:support@crewai.com).

<Card title="Schedule a Demo" icon="calendar" href="mailto:support@crewai.com">
  Book time with our team to learn more about Enterprise features and how they can benefit your organization.
</Card>

---

## Build Your First Crew

**URL:** llms-txt#build-your-first-crew

**Contents:**
- Unleashing the Power of Collaborative AI
  - What You'll Build and Learn
  - Prerequisites
- Step 1: Create a New CrewAI Project
- Step 2: Explore the Project Structure
- Step 3: Configure Your Agents

Source: https://docs.crewai.com/en/guides/crews/first-crew

Step-by-step tutorial to create a collaborative AI team that works together to solve complex problems.

## Unleashing the Power of Collaborative AI

Imagine having a team of specialized AI agents working together seamlessly to solve complex problems, each contributing their unique skills to achieve a common goal. This is the power of CrewAI - a framework that enables you to create collaborative AI systems that can accomplish tasks far beyond what a single AI could achieve alone.

In this guide, we'll walk through creating a research crew that will help us research and analyze a topic, then create a comprehensive report. This practical example demonstrates how AI agents can collaborate to accomplish complex tasks, but it's just the beginning of what's possible with CrewAI.

### What You'll Build and Learn

By the end of this guide, you'll have:

1. **Created a specialized AI research team** with distinct roles and responsibilities
2. **Orchestrated collaboration** between multiple AI agents
3. **Automated a complex workflow** that involves gathering information, analysis, and report generation
4. **Built foundational skills** that you can apply to more ambitious projects

While we're building a simple research crew in this guide, the same patterns and techniques can be applied to create much more sophisticated teams for tasks like:

* Multi-stage content creation with specialized writers, editors, and fact-checkers
* Complex customer service systems with tiered support agents
* Autonomous business analysts that gather data, create visualizations, and generate insights
* Product development teams that ideate, design, and plan implementation

Let's get started building your first crew!

Before starting, make sure you have:

1. Installed CrewAI following the [installation guide](/en/installation)
2. Set up your LLM API key in your environment, following the [LLM setup
   guide](/en/concepts/llms#setting-up-your-llm)
3. Basic understanding of Python

## Step 1: Create a New CrewAI Project

First, let's create a new CrewAI project using the CLI. This command will set up a complete project structure with all the necessary files, allowing you to focus on defining your agents and their tasks rather than setting up boilerplate code.

This will generate a project with the basic structure needed for your crew. The CLI automatically creates:

* A project directory with the necessary files
* Configuration files for agents and tasks
* A basic crew implementation
* A main script to run the crew

<Frame>
  <img alt="CrewAI Framework Overview" />
</Frame>

## Step 2: Explore the Project Structure

Let's take a moment to understand the project structure created by the CLI. CrewAI follows best practices for Python projects, making it easy to maintain and extend your code as your crews become more complex.

This structure follows best practices for Python projects and makes it easy to organize your code. The separation of configuration files (in YAML) from implementation code (in Python) makes it easy to modify your crew's behavior without changing the underlying code.

## Step 3: Configure Your Agents

Now comes the fun part - defining your AI agents! In CrewAI, agents are specialized entities with specific roles, goals, and backstories that shape their behavior. Think of them as characters in a play, each with their own personality and purpose.

For our research crew, we'll create two agents:

1. A **researcher** who excels at finding and organizing information
2. An **analyst** who can interpret research findings and create insightful reports

Let's modify the `agents.yaml` file to define these specialized agents. Be sure
to set `llm` to the provider you are using.

**Examples:**

Example 1 (unknown):
```unknown
This will generate a project with the basic structure needed for your crew. The CLI automatically creates:

* A project directory with the necessary files
* Configuration files for agents and tasks
* A basic crew implementation
* A main script to run the crew

<Frame>
  <img alt="CrewAI Framework Overview" />
</Frame>

## Step 2: Explore the Project Structure

Let's take a moment to understand the project structure created by the CLI. CrewAI follows best practices for Python projects, making it easy to maintain and extend your code as your crews become more complex.
```

Example 2 (unknown):
```unknown
This structure follows best practices for Python projects and makes it easy to organize your code. The separation of configuration files (in YAML) from implementation code (in Python) makes it easy to modify your crew's behavior without changing the underlying code.

## Step 3: Configure Your Agents

Now comes the fun part - defining your AI agents! In CrewAI, agents are specialized entities with specific roles, goals, and backstories that shape their behavior. Think of them as characters in a play, each with their own personality and purpose.

For our research crew, we'll create two agents:

1. A **researcher** who excels at finding and organizing information
2. An **analyst** who can interpret research findings and create insightful reports

Let's modify the `agents.yaml` file to define these specialized agents. Be sure
to set `llm` to the provider you are using.
```

---

## Check if API keys are set

**URL:** llms-txt#check-if-api-keys-are-set

required_keys = ["OPENAI_API_KEY", "GOOGLE_API_KEY", "COHERE_API_KEY"]
for key in required_keys:
    if os.getenv(key):
        print(f"✅ {key} is set")
    else:
        print(f"❌ {key} is not set")
python theme={null}
import time

def test_embedding_performance(embedder_config, test_text="This is a test document"):
    start_time = time.time()

crew = Crew(
        agents=[...],
        tasks=[...],
        memory=True,
        embedder=embedder_config
    )

# Simulate memory operation
    crew.kickoff()

end_time = time.time()
    return end_time - start_time

**Examples:**

Example 1 (unknown):
```unknown
**Performance comparison:**
```

---

## Choose which LLM to use for each agent based on your needs

**URL:** llms-txt#choose-which-llm-to-use-for-each-agent-based-on-your-needs

**Contents:**
- Set Up Enterprise Governance for CrewAI
- Frequently Asked Questions
- Resources

researcher = Agent(
    role="Senior Research Scientist",
    goal="Discover groundbreaking insights about the assigned topic",
    backstory="You are an expert researcher with deep domain knowledge.",
    verbose=True,
    llm=openai_llm  # Use anthropic_llm for Anthropic
)
json theme={null}
       {
           "virtual_key": "YOUR_VIRTUAL_KEY_FROM_STEP1",
          	"override_params": {
             "model": "gpt-4o" // Your preferred model name
           }
       }
       python theme={null}
    from crewai import Agent, LLM
    from portkey_ai import PORTKEY_GATEWAY_URL

# Configure LLM with your API key
    portkey_llm = LLM(
        model="gpt-4o",
        base_url=PORTKEY_GATEWAY_URL,
        api_key="YOUR_PORTKEY_API_KEY"
    )

# Create agent with Portkey-enabled LLM
    researcher = Agent(
        role="Senior Research Scientist",
        goal="Discover groundbreaking insights about the assigned topic",
        backstory="You are an expert researcher with deep domain knowledge.",
        verbose=True,
        llm=portkey_llm
    )
    json theme={null}
    {
    	"strategy": {
    		"mode": "single"
    	},
    	"targets": [
    		{
    			"virtual_key": "YOUR_OPENAI_VIRTUAL_KEY",
    			"override_params": {
    				"model": "gpt-4o"
    			}
    		}
    	]
    }
    python theme={null}
    from portkey_ai import Portkey

portkey = Portkey(api_key="YOUR_ADMIN_API_KEY")

api_key = portkey.api_keys.create(
        name="engineering-team",
        type="organisation",
        workspace_id="YOUR_WORKSPACE_ID",
        defaults={
            "config_id": "your-config-id",
            "metadata": {
                "environment": "production",
                "department": "engineering"
            }
        },
        scopes=["logs.view", "configs.read"]
    )
    ```

For detailed key management instructions, see the [Portkey documentation](https://portkey.ai/docs).
  </Accordion>

<Accordion title="Step 4: Deploy & Monitor">
    ### Step 4: Deploy & Monitor

After distributing API keys to your team members, your enterprise-ready CrewAI setup is ready to go. Each team member can now use their designated API keys with appropriate access levels and budget controls.

Monitor usage in Portkey dashboard:

* Cost tracking by department
    * Model usage patterns
    * Request volumes
    * Error rates
  </Accordion>
</AccordionGroup>

<Note>
  ### Enterprise Features Now Available

**Your CrewAI integration now has:**

* Departmental budget controls
  * Model access governance
  * Usage tracking & attribution
  * Security guardrails
  * Reliability features
</Note>

## Frequently Asked Questions

<AccordionGroup>
  <Accordion title="How does Portkey enhance CrewAI?">
    Portkey adds production-readiness to CrewAI through comprehensive observability (traces, logs, metrics), reliability features (fallbacks, retries, caching), and access to 200+ LLMs through a unified interface. This makes it easier to debug, optimize, and scale your agent applications.
  </Accordion>

<Accordion title="Can I use Portkey with existing CrewAI applications?">
    Yes! Portkey integrates seamlessly with existing CrewAI applications. You just need to update your LLM configuration code with the Portkey-enabled version. The rest of your agent and crew code remains unchanged.
  </Accordion>

<Accordion title="Does Portkey work with all CrewAI features?">
    Portkey supports all CrewAI features, including agents, tools, human-in-the-loop workflows, and all task process types (sequential, hierarchical, etc.). It adds observability and reliability without limiting any of the framework's functionality.
  </Accordion>

<Accordion title="Can I track usage across multiple agents in a crew?">
    Yes, Portkey allows you to use a consistent `trace_id` across multiple agents in a crew to track the entire workflow. This is especially useful for complex crews where you want to understand the full execution path across multiple agents.
  </Accordion>

<Accordion title="How do I filter logs and traces for specific crew runs?">
    Portkey allows you to add custom metadata to your LLM configuration, which you can then use for filtering. Add fields like `crew_name`, `crew_type`, or `session_id` to easily find and analyze specific crew executions.
  </Accordion>

<Accordion title="Can I use my own API keys with Portkey?">
    Yes! Portkey uses your own API keys for the various LLM providers. It securely stores them as virtual keys, allowing you to easily manage and rotate keys without changing your code.
  </Accordion>
</AccordionGroup>

<CardGroup>
  <Card title="CrewAI Docs" icon="book" href="https://docs.crewai.com/">
    <p>Official CrewAI documentation</p>
  </Card>

<Card title="Book a Demo" icon="calendar" href="https://calendly.com/portkey-ai">
    <p>Get personalized guidance on implementing this integration</p>
  </Card>
</CardGroup>

**Examples:**

Example 1 (unknown):
```unknown
Portkey provides access to LLMs from providers including:

* OpenAI (GPT-4o, GPT-4 Turbo, etc.)
* Anthropic (Claude 3.5 Sonnet, Claude 3 Opus, etc.)
* Mistral AI (Mistral Large, Mistral Medium, etc.)
* Google Vertex AI (Gemini 1.5 Pro, etc.)
* Cohere (Command, Command-R, etc.)
* AWS Bedrock (Claude, Titan, etc.)
* Local/Private Models

<Card title="Supported Providers" icon="server" href="https://portkey.ai/docs/integrations/llms">
  See the full list of LLM providers supported by Portkey
</Card>

## Set Up Enterprise Governance for CrewAI

**Why Enterprise Governance?**
If you are using CrewAI inside your organization, you need to consider several governance aspects:

* **Cost Management**: Controlling and tracking AI spending across teams
* **Access Control**: Managing which teams can use specific models
* **Usage Analytics**: Understanding how AI is being used across the organization
* **Security & Compliance**: Maintaining enterprise security standards
* **Reliability**: Ensuring consistent service across all users

Portkey adds a comprehensive governance layer to address these enterprise needs. Let's implement these controls step by step.

<Steps>
  <Step title="Create Virtual Key">
    Virtual Keys are Portkey's secure way to manage your LLM provider API keys. They provide essential controls like:

    * Budget limits for API usage
    * Rate limiting capabilities
    * Secure API key storage

    To create a virtual key:
    Go to [Virtual Keys](https://app.portkey.ai/virtual-keys) in the Portkey App. Save and copy the virtual key ID

    <Frame>
      <img />
    </Frame>

    <Note>
      Save your virtual key ID - you'll need it for the next step.
    </Note>
  </Step>

  <Step title="Create Default Config">
    Configs in Portkey define how your requests are routed, with features like advanced routing, fallbacks, and retries.

    To create your config:

    1. Go to [Configs](https://app.portkey.ai/configs) in Portkey dashboard
    2. Create new config with:
```

Example 2 (unknown):
```unknown
3. Save and note the Config name for the next step

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Configure Portkey API Key">
    Now create a Portkey API key and attach the config you created in Step 2:

    1. Go to [API Keys](https://app.portkey.ai/api-keys) in Portkey and Create new API key
    2. Select your config from `Step 2`
    3. Generate and save your API key

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Connect to CrewAI">
    After setting up your Portkey API key with the attached config, connect it to your CrewAI agents:
```

Example 3 (unknown):
```unknown
</Step>
</Steps>

<AccordionGroup>
  <Accordion title="Step 1: Implement Budget Controls & Rate Limits">
    ### Step 1: Implement Budget Controls & Rate Limits

    Virtual Keys enable granular control over LLM access at the team/department level. This helps you:

    * Set up [budget limits](https://portkey.ai/docs/product/ai-gateway/virtual-keys/budget-limits)
    * Prevent unexpected usage spikes using Rate limits
    * Track departmental spending

    #### Setting Up Department-Specific Controls:

    1. Navigate to [Virtual Keys](https://app.portkey.ai/virtual-keys) in Portkey dashboard
    2. Create new Virtual Key for each department with budget limits and rate limits
    3. Configure department-specific limits

    <Frame>
      <img />
    </Frame>
  </Accordion>

  <Accordion title="Step 2: Define Model Access Rules">
    ### Step 2: Define Model Access Rules

    As your AI usage scales, controlling which teams can access specific models becomes crucial. Portkey Configs provide this control layer with features like:

    #### Access Control Features:

    * **Model Restrictions**: Limit access to specific models
    * **Data Protection**: Implement guardrails for sensitive data
    * **Reliability Controls**: Add fallbacks and retry logic

    #### Example Configuration:

    Here's a basic configuration to route requests to OpenAI, specifically using GPT-4o:
```

Example 4 (unknown):
```unknown
Create your config on the [Configs page](https://app.portkey.ai/configs) in your Portkey dashboard.

    <Note>
      Configs can be updated anytime to adjust controls without affecting running applications.
    </Note>
  </Accordion>

  <Accordion title="Step 3: Implement Access Controls">
    ### Step 3: Implement Access Controls

    Create User-specific API keys that automatically:

    * Track usage per user/team with the help of virtual keys
    * Apply appropriate configs to route requests
    * Collect relevant metadata to filter logs
    * Enforce access permissions

    Create API keys through the [Portkey App](https://app.portkey.ai/)

    Example using Python SDK:
```

---

## ClickUp Integration

**URL:** llms-txt#clickup-integration

**Contents:**
- Overview
- Prerequisites
- Setting Up ClickUp Integration
  - 1. Connect Your ClickUp Account
  - 2. Install Required Package
  - 3. Environment Variable Setup
- Available Actions
- Usage Examples
  - Basic ClickUp Agent Setup

Source: https://docs.crewai.com/en/enterprise/integrations/clickup

Task and productivity management with ClickUp integration for CrewAI.

Enable your agents to manage tasks, projects, and productivity workflows through ClickUp. Create and update tasks, organize projects, manage team assignments, and streamline your productivity management with AI-powered automation.

Before using the ClickUp integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A ClickUp account with appropriate permissions
* Connected your ClickUp account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)

## Setting Up ClickUp Integration

### 1. Connect Your ClickUp Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **ClickUp** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for task and project management
5. Copy your Enterprise Token from [Integration Settings](https://app.crewai.com/crewai_plus/settings/integrations)

### 2. Install Required Package

### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>

Or add it to your `.env` file:

<AccordionGroup>
  <Accordion title="clickup/search_tasks">
    **Description:** Search for tasks in ClickUp using advanced filters.

* `taskFilterFormula` (object, optional): A filter in disjunctive normal form - OR of AND groups of single conditions.
      
      Available fields: `space_ids%5B%5D`, `project_ids%5B%5D`, `list_ids%5B%5D`, `statuses%5B%5D`, `include_closed`, `assignees%5B%5D`, `tags%5B%5D`, `due_date_gt`, `due_date_lt`, `date_created_gt`, `date_created_lt`, `date_updated_gt`, `date_updated_lt`
  </Accordion>

<Accordion title="clickup/get_task_in_list">
    **Description:** Get tasks in a specific list in ClickUp.

* `listId` (string, required): List - Select a List to get tasks from. Use Connect Portal User Settings to allow users to select a ClickUp List.
    * `taskFilterFormula` (string, optional): Search for tasks that match specified filters. For example: name=task1.
  </Accordion>

<Accordion title="clickup/create_task">
    **Description:** Create a task in ClickUp.

* `listId` (string, required): List - Select a List to create this task in. Use Connect Portal User Settings to allow users to select a ClickUp List.
    * `name` (string, required): Name - The task name.
    * `description` (string, optional): Description - Task description.
    * `status` (string, optional): Status - Select a Status for this task. Use Connect Portal User Settings to allow users to select a ClickUp Status.
    * `assignees` (string, optional): Assignees - Select a Member (or an array of member IDs) to be assigned to this task. Use Connect Portal User Settings to allow users to select a ClickUp Member.
    * `dueDate` (string, optional): Due Date - Specify a date for this task to be due on.
    * `additionalFields` (string, optional): Additional Fields - Specify additional fields to include on this task as JSON.
  </Accordion>

<Accordion title="clickup/update_task">
    **Description:** Update a task in ClickUp.

* `taskId` (string, required): Task ID - The ID of the task to update.
    * `listId` (string, required): List - Select a List to create this task in. Use Connect Portal User Settings to allow users to select a ClickUp List.
    * `name` (string, optional): Name - The task name.
    * `description` (string, optional): Description - Task description.
    * `status` (string, optional): Status - Select a Status for this task. Use Connect Portal User Settings to allow users to select a ClickUp Status.
    * `assignees` (string, optional): Assignees - Select a Member (or an array of member IDs) to be assigned to this task. Use Connect Portal User Settings to allow users to select a ClickUp Member.
    * `dueDate` (string, optional): Due Date - Specify a date for this task to be due on.
    * `additionalFields` (string, optional): Additional Fields - Specify additional fields to include on this task as JSON.
  </Accordion>

<Accordion title="clickup/delete_task">
    **Description:** Delete a task in ClickUp.

* `taskId` (string, required): Task ID - The ID of the task to delete.
  </Accordion>

<Accordion title="clickup/get_list">
    **Description:** Get List information in ClickUp.

* `spaceId` (string, required): Space ID - The ID of the space containing the lists.
  </Accordion>

<Accordion title="clickup/get_custom_fields_in_list">
    **Description:** Get Custom Fields in a List in ClickUp.

* `listId` (string, required): List ID - The ID of the list to get custom fields from.
  </Accordion>

<Accordion title="clickup/get_all_fields_in_list">
    **Description:** Get All Fields in a List in ClickUp.

* `listId` (string, required): List ID - The ID of the list to get all fields from.
  </Accordion>

<Accordion title="clickup/get_space">
    **Description:** Get Space information in ClickUp.

* `spaceId` (string, optional): Space ID - The ID of the space to retrieve.
  </Accordion>

<Accordion title="clickup/get_folders">
    **Description:** Get Folders in ClickUp.

* `spaceId` (string, required): Space ID - The ID of the space containing the folders.
  </Accordion>

<Accordion title="clickup/get_member">
    **Description:** Get Member information in ClickUp.

**Parameters:** None required.
  </Accordion>
</AccordionGroup>

### Basic ClickUp Agent Setup

```python theme={null}
from crewai import Agent, Task, Crew
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

Example 3 (unknown):
```unknown
## Available Actions

<AccordionGroup>
  <Accordion title="clickup/search_tasks">
    **Description:** Search for tasks in ClickUp using advanced filters.

    **Parameters:**

    * `taskFilterFormula` (object, optional): A filter in disjunctive normal form - OR of AND groups of single conditions.
```

Example 4 (unknown):
```unknown
Available fields: `space_ids%5B%5D`, `project_ids%5B%5D`, `list_ids%5B%5D`, `statuses%5B%5D`, `include_closed`, `assignees%5B%5D`, `tags%5B%5D`, `due_date_gt`, `due_date_lt`, `date_created_gt`, `date_created_lt`, `date_updated_gt`, `date_updated_lt`
  </Accordion>

  <Accordion title="clickup/get_task_in_list">
    **Description:** Get tasks in a specific list in ClickUp.

    **Parameters:**

    * `listId` (string, required): List - Select a List to get tasks from. Use Connect Portal User Settings to allow users to select a ClickUp List.
    * `taskFilterFormula` (string, optional): Search for tasks that match specified filters. For example: name=task1.
  </Accordion>

  <Accordion title="clickup/create_task">
    **Description:** Create a task in ClickUp.

    **Parameters:**

    * `listId` (string, required): List - Select a List to create this task in. Use Connect Portal User Settings to allow users to select a ClickUp List.
    * `name` (string, required): Name - The task name.
    * `description` (string, optional): Description - Task description.
    * `status` (string, optional): Status - Select a Status for this task. Use Connect Portal User Settings to allow users to select a ClickUp Status.
    * `assignees` (string, optional): Assignees - Select a Member (or an array of member IDs) to be assigned to this task. Use Connect Portal User Settings to allow users to select a ClickUp Member.
    * `dueDate` (string, optional): Due Date - Specify a date for this task to be due on.
    * `additionalFields` (string, optional): Additional Fields - Specify additional fields to include on this task as JSON.
  </Accordion>

  <Accordion title="clickup/update_task">
    **Description:** Update a task in ClickUp.

    **Parameters:**

    * `taskId` (string, required): Task ID - The ID of the task to update.
    * `listId` (string, required): List - Select a List to create this task in. Use Connect Portal User Settings to allow users to select a ClickUp List.
    * `name` (string, optional): Name - The task name.
    * `description` (string, optional): Description - Task description.
    * `status` (string, optional): Status - Select a Status for this task. Use Connect Portal User Settings to allow users to select a ClickUp Status.
    * `assignees` (string, optional): Assignees - Select a Member (or an array of member IDs) to be assigned to this task. Use Connect Portal User Settings to allow users to select a ClickUp Member.
    * `dueDate` (string, optional): Due Date - Specify a date for this task to be due on.
    * `additionalFields` (string, optional): Additional Fields - Specify additional fields to include on this task as JSON.
  </Accordion>

  <Accordion title="clickup/delete_task">
    **Description:** Delete a task in ClickUp.

    **Parameters:**

    * `taskId` (string, required): Task ID - The ID of the task to delete.
  </Accordion>

  <Accordion title="clickup/get_list">
    **Description:** Get List information in ClickUp.

    **Parameters:**

    * `spaceId` (string, required): Space ID - The ID of the space containing the lists.
  </Accordion>

  <Accordion title="clickup/get_custom_fields_in_list">
    **Description:** Get Custom Fields in a List in ClickUp.

    **Parameters:**

    * `listId` (string, required): List ID - The ID of the list to get custom fields from.
  </Accordion>

  <Accordion title="clickup/get_all_fields_in_list">
    **Description:** Get All Fields in a List in ClickUp.

    **Parameters:**

    * `listId` (string, required): List ID - The ID of the list to get all fields from.
  </Accordion>

  <Accordion title="clickup/get_space">
    **Description:** Get Space information in ClickUp.

    **Parameters:**

    * `spaceId` (string, optional): Space ID - The ID of the space to retrieve.
  </Accordion>

  <Accordion title="clickup/get_folders">
    **Description:** Get Folders in ClickUp.

    **Parameters:**

    * `spaceId` (string, required): Space ID - The ID of the space containing the folders.
  </Accordion>

  <Accordion title="clickup/get_member">
    **Description:** Get Member information in ClickUp.

    **Parameters:** None required.
  </Accordion>
</AccordionGroup>

## Usage Examples

### Basic ClickUp Agent Setup
```

---

## `CodeInterpreterTool`

**URL:** llms-txt#`codeinterpretertool`

**Contents:**
- Description
  - Docker Container (Recommended)
  - Sandbox environment
  - Unsafe Execution
- Logging
- Installation
- Example

The `CodeInterpreterTool` enables CrewAI agents to execute Python 3 code that they generate autonomously. This functionality is particularly valuable as it allows agents to create code, execute it, obtain the results, and utilize that information to inform subsequent decisions and actions.

There are several ways to use this tool:

### Docker Container (Recommended)

This is the primary option. The code runs in a secure, isolated Docker container, ensuring safety regardless of its content.
Make sure Docker is installed and running on your system. If you don’t have it, you can install it from [here](https://docs.docker.com/get-docker/).

### Sandbox environment

If Docker is unavailable — either not installed or not accessible for any reason — the code will be executed in a restricted Python environment - called sandbox.
This environment is very limited, with strict restrictions on many modules and built-in functions.

**NOT RECOMMENDED FOR PRODUCTION**
This mode allows execution of any Python code, including dangerous calls to `sys, os..` and similar modules. [Check out](/en/tools/ai-ml/codeinterpretertool#enabling-unsafe-mode) how to enable this mode

The `CodeInterpreterTool` logs the selected execution strategy to STDOUT

To use this tool, you need to install the CrewAI tools package:

The following example demonstrates how to use the `CodeInterpreterTool` with a CrewAI agent:

```python Code theme={null}
from crewai import Agent, Task, Crew, Process
from crewai_tools import CodeInterpreterTool

**Examples:**

Example 1 (unknown):
```unknown
## Example

The following example demonstrates how to use the `CodeInterpreterTool` with a CrewAI agent:
```

---

## Coding Agents

**URL:** llms-txt#coding-agents

**Contents:**
- Introduction
- Enabling Code Execution
- Important Considerations
- Code Execution Process
- Example Usage

Source: https://docs.crewai.com/en/learn/coding-agents

Learn how to enable your CrewAI Agents to write and execute code, and explore advanced features for enhanced functionality.

CrewAI Agents now have the powerful ability to write and execute code, significantly enhancing their problem-solving capabilities. This feature is particularly useful for tasks that require computational or programmatic solutions.

## Enabling Code Execution

To enable code execution for an agent, set the `allow_code_execution` parameter to `True` when creating the agent.

<Note>
  Note that `allow_code_execution` parameter defaults to `False`.
</Note>

## Important Considerations

1. **Model Selection**: It is strongly recommended to use more capable models like Claude 3.5 Sonnet and GPT-4 when enabling code execution.
   These models have a better understanding of programming concepts and are more likely to generate correct and efficient code.

2. **Error Handling**: The code execution feature includes error handling. If executed code raises an exception, the agent will receive the error message and can attempt to correct the code or
   provide alternative solutions. The `max_retry_limit` parameter, which defaults to 2, controls the maximum number of retries for a task.

3. **Dependencies**: To use the code execution feature, you need to install the `crewai_tools` package. If not installed, the agent will log an info message:
   "Coding tools not available. Install crewai\_tools."

## Code Execution Process

When an agent with code execution enabled encounters a task requiring programming:

<Steps>
  <Step title="Task Analysis">
    The agent analyzes the task and determines that code execution is necessary.
  </Step>

<Step title="Code Formulation">
    It formulates the Python code needed to solve the problem.
  </Step>

<Step title="Code Execution">
    The code is sent to the internal code execution tool (`CodeInterpreterTool`).
  </Step>

<Step title="Result Interpretation">
    The agent interprets the result and incorporates it into its response or uses it for further problem-solving.
  </Step>
</Steps>

Here's a detailed example of creating an agent with code execution capabilities and using it in a task:

```python Code theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
<Note>
  Note that `allow_code_execution` parameter defaults to `False`.
</Note>

## Important Considerations

1. **Model Selection**: It is strongly recommended to use more capable models like Claude 3.5 Sonnet and GPT-4 when enabling code execution.
   These models have a better understanding of programming concepts and are more likely to generate correct and efficient code.

2. **Error Handling**: The code execution feature includes error handling. If executed code raises an exception, the agent will receive the error message and can attempt to correct the code or
   provide alternative solutions. The `max_retry_limit` parameter, which defaults to 2, controls the maximum number of retries for a task.

3. **Dependencies**: To use the code execution feature, you need to install the `crewai_tools` package. If not installed, the agent will log an info message:
   "Coding tools not available. Install crewai\_tools."

## Code Execution Process

When an agent with code execution enabled encounters a task requiring programming:

<Steps>
  <Step title="Task Analysis">
    The agent analyzes the task and determines that code execution is necessary.
  </Step>

  <Step title="Code Formulation">
    It formulates the Python code needed to solve the problem.
  </Step>

  <Step title="Code Execution">
    The code is sent to the internal code execution tool (`CodeInterpreterTool`).
  </Step>

  <Step title="Result Interpretation">
    The agent interprets the result and incorporates it into its response or uses it for further problem-solving.
  </Step>
</Steps>

## Example Usage

Here's a detailed example of creating an agent with code execution capabilities and using it in a task:
```

---

## Collaboration

**URL:** llms-txt#collaboration

**Contents:**
- Overview
- Quick Start: Enable Collaboration

Source: https://docs.crewai.com/en/concepts/collaboration

How to enable agents to work together, delegate tasks, and communicate effectively within CrewAI teams.

Collaboration in CrewAI enables agents to work together as a team by delegating tasks and asking questions to leverage each other's expertise. When `allow_delegation=True`, agents automatically gain access to powerful collaboration tools.

## Quick Start: Enable Collaboration

```python theme={null}
from crewai import Agent, Crew, Task

---

## Complex communication automation task

**URL:** llms-txt#complex-communication-automation-task

**Contents:**
- Troubleshooting
  - Common Issues
  - Getting Help

automation_task = Task(
    description="""
    1. List all workspace users and identify team roles
    2. Get specific user information for project stakeholders
    3. Create automated status update comments on key project pages
    4. Facilitate team communication through targeted comments
    """,
    agent=communication_automator,
    expected_output="Automated communication workflow completed with user management and comments"
)

crew = Crew(
    agents=[communication_automator],
    tasks=[automation_task]
)

**Permission Errors**

* Ensure your Notion account has appropriate permissions to read user information
* Verify that the OAuth connection includes required scopes for user access and comment creation
* Check that you have permissions to comment on the target pages or discussions

**User Access Issues**

* Ensure you have workspace admin permissions to list all users
* Verify that user IDs are correct and users exist in the workspace
* Check that the workspace allows API access to user information

**Comment Creation Issues**

* Verify that page IDs or discussion IDs are correct and accessible
* Ensure that rich text content follows Notion's API format specifications
* Check that you have comment permissions on the target pages or discussions

* Be mindful of Notion's API rate limits when making multiple requests
* Implement appropriate delays between requests if needed
* Consider pagination for large user lists

**Parent Object Specification**

* Ensure parent object type is correctly specified (page\_id or discussion\_id)
* Verify that the parent page or discussion exists and is accessible
* Check that the parent object ID format is correct

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with Notion integration setup or troubleshooting.
</Card>

---

## Complex task involving analytics and reporting

**URL:** llms-txt#complex-task-involving-analytics-and-reporting

analytics_task = Task(
    description="""
    1. Search for all open tickets from the last 30 days
    2. Analyze ticket resolution times and customer satisfaction
    3. Identify common issues and support patterns
    4. Generate weekly support performance report
    """,
    agent=support_analyst,
    expected_output="Comprehensive support analytics report with performance insights and recommendations"
)

crew = Crew(
    agents=[support_analyst],
    tasks=[analytics_task]
)

---

## Complex task involving financial analysis

**URL:** llms-txt#complex-task-involving-financial-analysis

**Contents:**
- Subscription Status Reference
- Metadata Usage

analytics_task = Task(
    description="""
    1. Retrieve balance transactions for the current month
    2. Analyze customer payment patterns and subscription trends
    3. Identify high-value customers and subscription performance
    4. Generate monthly financial performance report
    """,
    agent=financial_analyst,
    expected_output="Comprehensive financial analysis with payment insights and recommendations"
)

crew = Crew(
    agents=[financial_analyst],
    tasks=[analytics_task]
)

crew.kickoff()
json theme={null}
{
  "customer_segment": "enterprise",
  "acquisition_source": "google_ads",
  "lifetime_value": "high",
  "custom_field_1": "value1"
}
```

This integration enables comprehensive payment and subscription management automation, allowing your AI agents to handle billing operations seamlessly within your Stripe ecosystem.

**Examples:**

Example 1 (unknown):
```unknown
## Subscription Status Reference

Understanding subscription statuses:

* **incomplete** - Subscription requires payment method or payment confirmation
* **incomplete\_expired** - Subscription expired before payment was confirmed
* **trialing** - Subscription is in trial period
* **active** - Subscription is active and current
* **past\_due** - Payment failed but subscription is still active
* **canceled** - Subscription has been canceled
* **unpaid** - Payment failed and subscription is no longer active

## Metadata Usage

Metadata allows you to store additional information about customers, subscriptions, and products:
```

---

## Complex task involving multiple Asana operations

**URL:** llms-txt#complex-task-involving-multiple-asana-operations

coordination_task = Task(
    description="""
    1. Get all active projects in the workspace
    2. For each project, get the list of incomplete tasks
    3. Create a summary report task in the 'Management Reports' project
    4. Add comments to overdue tasks to request status updates
    """,
    agent=project_coordinator,
    expected_output="Summary report created and status update requests sent for overdue tasks"
)

crew = Crew(
    agents=[project_coordinator],
    tasks=[coordination_task]
)

---

## Complex task involving multiple Box operations

**URL:** llms-txt#complex-task-involving-multiple-box-operations

management_task = Task(
    description="""
    1. List all files in the root folder
    2. Create monthly archive folders for the current year
    3. Move old files to appropriate archive folders
    4. Generate a summary report of the file organization
    """,
    agent=file_manager,
    expected_output="Files organized into archive structure with summary report"
)

crew = Crew(
    agents=[file_manager],
    tasks=[management_task]
)

---

## Complex task involving multiple ClickUp operations

**URL:** llms-txt#complex-task-involving-multiple-clickup-operations

**Contents:**
  - Task Search and Management

project_coordination = Task(
    description="""
    1. Get all open tasks in the current space
    2. Identify overdue tasks and update their status
    3. Create a weekly report task summarizing project progress
    4. Assign the report task to the team lead
    """,
    agent=project_manager,
    expected_output="Project status updated and weekly report task created and assigned"
)

crew = Crew(
    agents=[project_manager],
    tasks=[project_coordination]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

task_analyst = Agent(
    role="Task Analyst",
    goal="Analyze task patterns and optimize team productivity",
    backstory="An AI assistant that analyzes task data to improve team efficiency.",
    apps=['clickup']
)

**Examples:**

Example 1 (unknown):
```unknown
### Task Search and Management
```

---

## Complex task involving multiple GitHub operations

**URL:** llms-txt#complex-task-involving-multiple-github-operations

**Contents:**
  - Getting Help

coordination_task = Task(
    description="""
    1. Search for all open issues assigned to the current milestone
    2. Identify overdue issues and update their priority labels
    3. Create a weekly progress report issue
    4. Lock resolved issues that have been inactive for 30 days
    """,
    agent=project_coordinator,
    expected_output="Project coordination completed with progress report and issue management"
)

crew = Crew(
    agents=[project_coordinator],
    tasks=[coordination_task]
)

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with GitHub integration setup or troubleshooting.
</Card>

---

## Complex task involving multiple operations

**URL:** llms-txt#complex-task-involving-multiple-operations

**Contents:**
  - Getting Help

analytics_task = Task(
    description="""
    1. Retrieve recent customer data and order history
    2. Identify abandoned carts from the last 7 days
    3. Analyze product performance and inventory levels
    4. Generate recommendations for customer retention
    """,
    agent=analytics_agent,
    expected_output="Comprehensive e-commerce analytics report with actionable insights"
)

crew = Crew(
    agents=[analytics_agent],
    tasks=[analytics_task]
)

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with Shopify integration setup or troubleshooting.
</Card>

---

## Complex task involving search and analysis

**URL:** llms-txt#complex-task-involving-search-and-analysis

**Contents:**
- Contact Support

analysis_task = Task(
    description="""
    1. Search for recent project-related messages across all channels
    2. Find users by email to identify team members
    3. Analyze communication patterns and response times
    4. Generate weekly team communication summary
    """,
    agent=analytics_agent,
    expected_output="Comprehensive communication analysis with team insights and recommendations"
)

crew = Crew(
    agents=[analytics_agent],
    tasks=[analysis_task]
)

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with Slack integration setup or troubleshooting.
</Card>

---

## Complex task involving SOQL queries and data analysis

**URL:** llms-txt#complex-task-involving-soql-queries-and-data-analysis

**Contents:**
  - Getting Help

analysis_task = Task(
    description="""
    1. Execute a SOQL query to find all opportunities closing this quarter
    2. Search for contacts at companies with opportunities over $100K
    3. Create a summary report of the sales pipeline status
    4. Update high-value opportunities with next steps
    """,
    agent=data_analyst,
    expected_output="Comprehensive sales pipeline analysis with actionable insights"
)

crew = Crew(
    agents=[data_analyst],
    tasks=[analysis_task]
)

This comprehensive documentation covers all the Salesforce tools organized by functionality, making it easy for users to find the specific operations they need for their CRM automation tasks.

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with Salesforce integration setup or troubleshooting.
</Card>

---

## Complex workflow task

**URL:** llms-txt#complex-workflow-task

**Contents:**
- Troubleshooting
  - Common Issues
  - Getting Help

workflow_task = Task(
    description="""
    1. Get all customer data from the main customer spreadsheet
    2. Create a new monthly summary spreadsheet
    3. Append summary data to the new spreadsheet
    4. Update customer status based on activity metrics
    5. Generate reports with proper formatting
    """,
    agent=workflow_manager,
    expected_output="Monthly customer workflow completed with new spreadsheet and updated data"
)

crew = Crew(
    agents=[workflow_manager],
    tasks=[workflow_task]
)

**Permission Errors**

* Ensure your Google account has edit access to the target spreadsheets
* Verify that the OAuth connection includes required scopes for Google Sheets API
* Check that spreadsheets are shared with the authenticated account

**Spreadsheet Structure Issues**

* Ensure worksheets have proper column headers before creating or updating rows
* Verify that range notation (A1 format) is correct for the target cells
* Check that the specified spreadsheet ID exists and is accessible

**Data Type and Format Issues**

* Ensure data values match the expected format for each column
* Use proper date formats for date columns (ISO format recommended)
* Verify that numeric values are properly formatted for number columns

**Range and Cell Reference Issues**

* Use proper A1 notation for ranges (e.g., "A1:C10", "Sheet1!A1:B5")
* Ensure range references don't exceed the actual spreadsheet dimensions
* Verify that sheet names in range references match actual sheet names

**Value Input and Rendering Options**

* Choose appropriate `valueInputOption` (RAW vs USER\_ENTERED) for your data
* Select proper `valueRenderOption` based on how you want data formatted
* Consider `dateTimeRenderOption` for consistent date/time handling

**Spreadsheet Creation Issues**

* Ensure spreadsheet titles are unique and follow naming conventions
* Verify that sheet properties are properly structured when creating sheets
* Check that you have permissions to create new spreadsheets in your account

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with Google Sheets integration setup or troubleshooting.
</Card>

---

## `ComposioToolSet`

**URL:** llms-txt#`composiotoolset`

**Contents:**
- Description
- Installation
- Example

Composio is an integration platform that allows you to connect your AI agents to 250+ tools. Key features include:

* **Enterprise-Grade Authentication**: Built-in support for OAuth, API Keys, JWT with automatic token refresh
* **Full Observability**: Detailed tool usage logs, execution timestamps, and more

To incorporate Composio tools into your project, follow the instructions below:

After the installation is complete, either run `composio login` or export your composio API key as `COMPOSIO_API_KEY`. Get your Composio API key from [here](https://app.composio.dev)

The following example demonstrates how to initialize the tool and execute a github action:

1. Initialize Composio toolset

2. Connect your GitHub account

* Retrieving all the tools from an app (not recommended for production):

* Filtering tools based on tags:

* Filtering tools based on use case:

<Tip>Set `advanced` to True to get actions for complex use cases</Tip>

* Using specific tools:

In this demo, we will use the `GITHUB_STAR_A_REPOSITORY_FOR_THE_AUTHENTICATED_USER` action from the GitHub app.

Learn more about filtering actions [here](https://docs.composio.dev/patterns/tools/use-tools/use-specific-actions)

* More detailed list of tools can be found [here](https://app.composio.dev)

**Examples:**

Example 1 (unknown):
```unknown
After the installation is complete, either run `composio login` or export your composio API key as `COMPOSIO_API_KEY`. Get your Composio API key from [here](https://app.composio.dev)

## Example

The following example demonstrates how to initialize the tool and execute a github action:

1. Initialize Composio toolset
```

Example 2 (unknown):
```unknown
2. Connect your GitHub account

<CodeGroup>
```

Example 3 (unknown):
```unknown

```

Example 4 (unknown):
```unknown
</CodeGroup>

3. Get Tools

* Retrieving all the tools from an app (not recommended for production):
```

---

## Composio Tool

**URL:** llms-txt#composio-tool

Source: https://docs.crewai.com/en/tools/automation/composiotool

Composio provides 250+ production-ready tools for AI agents with flexible authentication management.

---

## Configure and run the crew

**URL:** llms-txt#configure-and-run-the-crew

**Contents:**
- Viewing Your Traces
- Troubleshooting
  - Common Issues
- Resources

crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    verbose=True
)

try:
    result = crew.kickoff()
finally:
    maxim.cleanup()  # Ensure cleanup happens even if errors occur
python theme={null}
  instrument_crewai(logger, debug=True)
  python theme={null}
  agent = CrewAgent(..., verbose=True)
  ```
* Double-check that `instrument_crewai()` is called **before** creating or executing agents. This might be obvious, but it's a common oversight.

<CardGroup>
  <Card title="CrewAI Docs" icon="book" href="https://docs.crewai.com/">
    Official CrewAI documentation
  </Card>

<Card title="Maxim Docs" icon="book" href="https://getmaxim.ai/docs">
    Official Maxim documentation
  </Card>

<Card title="Maxim Github" icon="github" href="https://github.com/maximhq">
    Maxim Github
  </Card>
</CardGroup>

**Examples:**

Example 1 (unknown):
```unknown
That's it! All your CrewAI agent interactions will now be logged and available in your Maxim dashboard.

Check this Google Colab Notebook for a quick reference - [Notebook](https://colab.research.google.com/drive/1ZKIZWsmgQQ46n8TH9zLsT1negKkJA6K8?usp=sharing)

## Viewing Your Traces

After running your CrewAI application:

1. Log in to your [Maxim Dashboard](https://app.getmaxim.ai/login)
2. Navigate to your repository
3. View detailed agent traces, including:

   * Agent conversations
   * Tool usage patterns
   * Performance metrics
   * Cost analytics

   <img />

## Troubleshooting

### Common Issues

* **No traces appearing**: Ensure your API key and repository ID are correct
* Ensure you've **`called instrument_crewai()`** ***before*** running your crew. This initializes logging hooks correctly.
* Set `debug=True` in your `instrument_crewai()` call to surface any internal errors:
```

Example 2 (unknown):
```unknown
* Configure your agents with `verbose=True` to capture detailed logs:
```

---

## Connecting to Multiple MCP Servers

**URL:** llms-txt#connecting-to-multiple-mcp-servers

**Contents:**
- Overview
- Configuration

Source: https://docs.crewai.com/en/mcp/multiple-servers

Learn how to use MCPServerAdapter in CrewAI to connect to multiple MCP servers simultaneously and aggregate their tools.

`MCPServerAdapter` in `crewai-tools` allows you to connect to multiple MCP servers concurrently. This is useful when your agents need to access tools distributed across different services or environments. The adapter aggregates tools from all specified servers, making them available to your CrewAI agents.

To connect to multiple servers, you provide a list of server parameter dictionaries to `MCPServerAdapter`. Each dictionary in the list should define the parameters for one MCP server.

Supported transport types for each server in the list include `stdio`, `sse`, and `streamable-http`.

```python theme={null}
from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters # Needed for Stdio example

---

## Crafting Effective Agents

**URL:** llms-txt#crafting-effective-agents

**Contents:**
- The Art and Science of Agent Design
  - Why Agent Design Matters
- The 80/20 Rule: Focus on Tasks Over Agents
- Core Principles of Effective Agent Design
  - 1. The Role-Goal-Backstory Framework
  - 2. Specialists Over Generalists
  - 3. Balancing Specialization and Versatility
  - 4. Setting Appropriate Expertise Levels
- Practical Examples: Before and After
  - Example 1: Content Creation Agent

Source: https://docs.crewai.com/en/guides/agents/crafting-effective-agents

Learn best practices for designing powerful, specialized AI agents that collaborate effectively to solve complex problems.

## The Art and Science of Agent Design

At the heart of CrewAI lies the agent - a specialized AI entity designed to perform specific roles within a collaborative framework. While creating basic agents is simple, crafting truly effective agents that produce exceptional results requires understanding key design principles and best practices.

This guide will help you master the art of agent design, enabling you to create specialized AI personas that collaborate effectively, think critically, and produce high-quality outputs tailored to your specific needs.

### Why Agent Design Matters

The way you define your agents significantly impacts:

1. **Output quality**: Well-designed agents produce more relevant, high-quality results
2. **Collaboration effectiveness**: Agents with complementary skills work together more efficiently
3. **Task performance**: Agents with clear roles and goals execute tasks more effectively
4. **System scalability**: Thoughtfully designed agents can be reused across multiple crews and contexts

Let's explore best practices for creating agents that excel in these dimensions.

## The 80/20 Rule: Focus on Tasks Over Agents

When building effective AI systems, remember this crucial principle: **80% of your effort should go into designing tasks, and only 20% into defining agents**.

Why? Because even the most perfectly defined agent will fail with poorly designed tasks, but well-designed tasks can elevate even a simple agent. This means:

* Spend most of your time writing clear task instructions
* Define detailed inputs and expected outputs
* Add examples and context to guide execution
* Dedicate the remaining time to agent role, goal, and backstory

This doesn't mean agent design isn't important - it absolutely is. But task design is where most execution failures occur, so prioritize accordingly.

## Core Principles of Effective Agent Design

### 1. The Role-Goal-Backstory Framework

The most powerful agents in CrewAI are built on a strong foundation of three key elements:

#### Role: The Agent's Specialized Function

The role defines what the agent does and their area of expertise. When crafting roles:

* **Be specific and specialized**: Instead of "Writer," use "Technical Documentation Specialist" or "Creative Storyteller"
* **Align with real-world professions**: Base roles on recognizable professional archetypes
* **Include domain expertise**: Specify the agent's field of knowledge (e.g., "Financial Analyst specializing in market trends")

**Examples of effective roles:**

#### Goal: The Agent's Purpose and Motivation

The goal directs the agent's efforts and shapes their decision-making process. Effective goals should:

* **Be clear and outcome-focused**: Define what the agent is trying to achieve
* **Emphasize quality standards**: Include expectations about the quality of work
* **Incorporate success criteria**: Help the agent understand what "good" looks like

**Examples of effective goals:**

#### Backstory: The Agent's Experience and Perspective

The backstory gives depth to the agent, influencing how they approach problems and interact with others. Good backstories:

* **Establish expertise and experience**: Explain how the agent gained their skills
* **Define working style and values**: Describe how the agent approaches their work
* **Create a cohesive persona**: Ensure all elements of the backstory align with the role and goal

**Examples of effective backstories:**

### 2. Specialists Over Generalists

Agents perform significantly better when given specialized roles rather than general ones. A highly focused agent delivers more precise, relevant outputs:

**Generic (Less Effective):**

**Specialized (More Effective):**

**Specialist Benefits:**

* Clearer understanding of expected output
* More consistent performance
* Better alignment with specific tasks
* Improved ability to make domain-specific judgments

### 3. Balancing Specialization and Versatility

Effective agents strike the right balance between specialization (doing one thing extremely well) and versatility (being adaptable to various situations):

* **Specialize in role, versatile in application**: Create agents with specialized skills that can be applied across multiple contexts
* **Avoid overly narrow definitions**: Ensure agents can handle variations within their domain of expertise
* **Consider the collaborative context**: Design agents whose specializations complement the other agents they'll work with

### 4. Setting Appropriate Expertise Levels

The expertise level you assign to your agent shapes how they approach tasks:

* **Novice agents**: Good for straightforward tasks, brainstorming, or initial drafts
* **Intermediate agents**: Suitable for most standard tasks with reliable execution
* **Expert agents**: Best for complex, specialized tasks requiring depth and nuance
* **World-class agents**: Reserved for critical tasks where exceptional quality is needed

Choose the appropriate expertise level based on task complexity and quality requirements. For most collaborative crews, a mix of expertise levels often works best, with higher expertise assigned to core specialized functions.

## Practical Examples: Before and After

Let's look at some examples of agent definitions before and after applying these best practices:

### Example 1: Content Creation Agent

### Example 2: Research Agent

## Crafting Effective Tasks for Your Agents

While agent design is important, task design is critical for successful execution. Here are best practices for designing tasks that set your agents up for success:

### The Anatomy of an Effective Task

A well-designed task has two key components that serve different purposes:

#### Task Description: The Process

The description should focus on what to do and how to do it, including:

* Detailed instructions for execution
* Context and background information
* Scope and constraints
* Process steps to follow

#### Expected Output: The Deliverable

The expected output should define what the final result should look like:

* Format specifications (markdown, JSON, etc.)
* Structure requirements
* Quality criteria
* Examples of good outputs (when possible)

### Task Design Best Practices

#### 1. Single Purpose, Single Output

Tasks perform best when focused on one clear objective:

**Bad Example (Too Broad):**

**Good Example (Focused):**

**Examples:**

Example 1 (unknown):
```unknown
#### Goal: The Agent's Purpose and Motivation

The goal directs the agent's efforts and shapes their decision-making process. Effective goals should:

* **Be clear and outcome-focused**: Define what the agent is trying to achieve
* **Emphasize quality standards**: Include expectations about the quality of work
* **Incorporate success criteria**: Help the agent understand what "good" looks like

**Examples of effective goals:**
```

Example 2 (unknown):
```unknown
#### Backstory: The Agent's Experience and Perspective

The backstory gives depth to the agent, influencing how they approach problems and interact with others. Good backstories:

* **Establish expertise and experience**: Explain how the agent gained their skills
* **Define working style and values**: Describe how the agent approaches their work
* **Create a cohesive persona**: Ensure all elements of the backstory align with the role and goal

**Examples of effective backstories:**
```

Example 3 (unknown):
```unknown
### 2. Specialists Over Generalists

Agents perform significantly better when given specialized roles rather than general ones. A highly focused agent delivers more precise, relevant outputs:

**Generic (Less Effective):**
```

Example 4 (unknown):
```unknown
**Specialized (More Effective):**
```

---

## Create agents

**URL:** llms-txt#create-agents

researcher = Agent(
    role='Research Analyst',
    goal='Conduct detailed market research',
    backstory='Expert market analyst with attention to detail',
    llm=llm,
    verbose=True
)

writer = Agent(
    role='Content Writer', 
    goal='Create comprehensive reports',
    backstory='Experienced technical writer',
    llm=llm,
    verbose=True
)

---

## Create agents and tasks as normal

**URL:** llms-txt#create-agents-and-tasks-as-normal

researcher = Agent(
    role="Research Specialist",
    goal="Find information on quantum computing",
    backstory="You are a quantum physics expert",
    verbose=True
)

research_task = Task(
    description="Research quantum computing applications",
    expected_output="A summary of practical applications",
    agent=researcher
)

---

## Create agents for different stages

**URL:** llms-txt#create-agents-for-different-stages

researcher = Agent(
    role='AWS Service Researcher',
    goal='Gather information about AWS services',
    backstory='I am specialized in finding detailed AWS service information.',
    tools=[initial_tool]
)

analyst = Agent(
    role='Service Compatibility Analyst',
    goal='Analyze service compatibility and requirements',
    backstory='I analyze AWS services for compatibility and integration possibilities.',
    tools=[followup_tool]
)

summarizer = Agent(
    role='Technical Documentation Writer',
    goal='Create clear technical summaries',
    backstory='I specialize in creating clear, concise technical documentation.',
    tools=[final_tool]
)

---

## Create agent with Gmail search and analysis capabilities

**URL:** llms-txt#create-agent-with-gmail-search-and-analysis-capabilities

email_analyst = Agent(
    role="Email Analyst",
    goal="Analyze email patterns and provide insights",
    backstory="An AI assistant that analyzes email data to provide actionable insights.",
    apps=['gmail/fetch_emails', 'gmail/get_message']  # Specific actions for email analysis
)

---

## Create agent with Gmail thread management capabilities

**URL:** llms-txt#create-agent-with-gmail-thread-management-capabilities

thread_manager = Agent(
    role="Thread Manager",
    goal="Organize and manage email threads efficiently",
    backstory="An AI assistant that specializes in email thread organization and management.",
    apps=[
        'gmail/fetch_thread',
        'gmail/modify_thread',
        'gmail/trash_thread'
    ]
)

---

## Create agent with guardrailed LLM

**URL:** llms-txt#create-agent-with-guardrailed-llm

**Contents:**
  - 5. User Tracking with Metadata

researcher = Agent(
    role="Senior Research Scientist",
    goal="Discover groundbreaking insights about the assigned topic",
    backstory="You are an expert researcher with deep domain knowledge.",
    verbose=True,
    llm=portkey_llm
)
python theme={null}
from crewai import Agent, LLM
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL

**Examples:**

Example 1 (unknown):
```unknown
Portkey's guardrails can:

* Detect and redact PII in both inputs and outputs
* Filter harmful or inappropriate content
* Validate response formats against schemas
* Check for hallucinations against ground truth
* Apply custom business logic and rules

<Card title="Learn More About Guardrails" icon="shield-check" href="https://portkey.ai/docs/product/guardrails">
  Explore Portkey's guardrail features to enhance agent safety
</Card>

### 5. User Tracking with Metadata

Track individual users through your CrewAI agents using Portkey's metadata system.

**What is Metadata in Portkey?**

Metadata allows you to associate custom data with each request, enabling filtering, segmentation, and analytics. The special `_user` field is specifically designed for user tracking.
```

---

## Create agent with HubSpot contact management capabilities

**URL:** llms-txt#create-agent-with-hubspot-contact-management-capabilities

crm_manager = Agent(
    role="CRM Manager",
    goal="Manage and organize HubSpot contacts efficiently.",
    backstory="An experienced CRM manager who maintains an organized contact database.",
    apps=['hubspot']  # All HubSpot actions including contact management
)

---

## Create agent with MCP tools using string references

**URL:** llms-txt#create-agent-with-mcp-tools-using-string-references

research_agent = Agent(
    role="Research Analyst",
    goal="Find and analyze information using advanced search tools",
    backstory="Expert researcher with access to multiple data sources",
    mcps=[
        "https://mcp.exa.ai/mcp?api_key=your_key&profile=your_profile",
        "crewai-amp:weather-service#current_conditions"
    ]
)

---

## Create agent with multiple MCP sources

**URL:** llms-txt#create-agent-with-multiple-mcp-sources

multi_source_agent = Agent(
    role="Multi-Source Research Analyst",
    goal="Conduct comprehensive research using multiple data sources",
    backstory="""Expert researcher with access to web search, weather data,
    financial information, and academic research tools""",
    mcps=[
        # External MCP servers
        "https://mcp.exa.ai/mcp?api_key=your_exa_key&profile=research",
        "https://weather.api.com/mcp#get_current_conditions",

# CrewAI AOP marketplace
        "crewai-amp:financial-insights",
        "crewai-amp:academic-research#pubmed_search",
        "crewai-amp:market-intelligence#competitor_analysis"
    ]
)

---

## Create agent with Slack messaging capabilities

**URL:** llms-txt#create-agent-with-slack-messaging-capabilities

notification_agent = Agent(
    role="Notification Manager",
    goal="Create rich, interactive notifications and manage workspace communication",
    backstory="An AI assistant that specializes in creating engaging team notifications and updates.",
    apps=['slack/send_message']  # Specific action for sending messages
)

---

## Create agent with Slack search and user management capabilities

**URL:** llms-txt#create-agent-with-slack-search-and-user-management-capabilities

analytics_agent = Agent(
    role="Communication Analyst",
    goal="Analyze team communication patterns and extract insights from conversations",
    backstory="An analytical AI that excels at understanding team dynamics through communication data.",
    apps=[
        'slack/search_messages',
        'slack/get_user_by_email',
        'slack/list_members'
    ]  # Using canonical action names from canonical_integrations.yml
)

---

## Create agent with specific Asana actions only

**URL:** llms-txt#create-agent-with-specific-asana-actions-only

task_manager_agent = Agent(
    role="Task Manager",
    goal="Create and manage tasks efficiently",
    backstory="An AI assistant that focuses on task creation and management.",
    apps=[
        'asana/create_task',
        'asana/update_task',
        'asana/get_tasks'
    ]  # Specific Asana actions
)

---

## Create agent with specific Box actions only

**URL:** llms-txt#create-agent-with-specific-box-actions-only

file_organizer_agent = Agent(
    role="File Organizer",
    goal="Organize and manage file storage efficiently",
    backstory="An AI assistant that focuses on file organization and storage management.",
    apps=['box/create_folder', 'box/save_file', 'box/list_files']  # Specific Box actions
)

---

## Create agent with specific Gmail actions only

**URL:** llms-txt#create-agent-with-specific-gmail-actions-only

email_coordinator = Agent(
    role="Email Coordinator",
    goal="Coordinate email communications and manage drafts",
    backstory="An AI assistant that focuses on email coordination and draft management.",
    apps=[
        'gmail/send_email',
        'gmail/fetch_emails',
        'gmail/create_draft'
    ]
)

---

## Create agent with specific Google Drive actions only

**URL:** llms-txt#create-agent-with-specific-google-drive-actions-only

file_manager_agent = Agent(
    role="Document Manager",
    goal="Upload and manage documents efficiently",
    backstory="An AI assistant that focuses on document upload and organization.",
    apps=[
        'google_drive/upload_file',
        'google_drive/create_folder',
        'google_drive/share_file'
    ]  # Specific Google Drive actions
)

---

## Create agent with specific Google Sheets actions only

**URL:** llms-txt#create-agent-with-specific-google-sheets-actions-only

data_collector = Agent(
    role="Data Collector",
    goal="Collect and organize data in spreadsheets",
    backstory="An AI assistant that focuses on data collection and organization.",
    apps=[
        'google_sheets/get_values',
        'google_sheets/update_values'
    ]
)

---

## Create agent with specific HubSpot actions only

**URL:** llms-txt#create-agent-with-specific-hubspot-actions-only

contact_creator = Agent(
    role="Contact Creator",
    goal="Create new contacts in HubSpot",
    backstory="An AI assistant that focuses on creating new contact entries in the CRM.",
    apps=['hubspot/create_contact']  # Only contact creation action
)

---

## Create agent with specific Slack actions only

**URL:** llms-txt#create-agent-with-specific-slack-actions-only

communication_manager = Agent(
    role="Communication Coordinator",
    goal="Manage team communications and ensure important messages reach the right people",
    backstory="An experienced communication coordinator who handles team messaging and notifications.",
    apps=[
        'slack/send_message',
        'slack/send_direct_message',
        'slack/search_messages'
    ]  # Using canonical action names from canonical_integrations.yml
)

---

## Create agent with specific Zendesk actions only

**URL:** llms-txt#create-agent-with-specific-zendesk-actions-only

support_agent = Agent(
    role="Customer Support Agent",
    goal="Handle customer inquiries and resolve support issues efficiently",
    backstory="An experienced support agent who specializes in ticket resolution and customer communication.",
    apps=['zendesk/create_ticket']  # Specific Zendesk actions
)

---

## Create agent with structured MCP configurations

**URL:** llms-txt#create-agent-with-structured-mcp-configurations

research_agent = Agent(
    role="Research Analyst",
    goal="Find and analyze information using advanced search tools",
    backstory="Expert researcher with access to multiple data sources",
    mcps=[
        # Local stdio server
        MCPServerStdio(
            command="python",
            args=["local_server.py"],
            env={"API_KEY": "your_key"},
        ),
        # Remote HTTP server
        MCPServerHTTP(
            url="https://api.research.com/mcp",
            headers={"Authorization": "Bearer your_token"},
        ),
    ]
)

---

## Create agent with tracked LLM

**URL:** llms-txt#create-agent-with-tracked-llm

**Contents:**
  - 6. Caching for Efficient Crews
  - 7. Model Interoperability

researcher = Agent(
    role="Senior Research Scientist",
    goal="Discover groundbreaking insights about the assigned topic",
    backstory="You are an expert researcher with deep domain knowledge.",
    verbose=True,
    llm=portkey_llm
)
python theme={null}
    from crewai import Agent, LLM
    from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL

# Configure LLM with simple caching
    portkey_llm = LLM(
        model="gpt-4o",
        base_url=PORTKEY_GATEWAY_URL,
        api_key="dummy",
        extra_headers=createHeaders(
            api_key="YOUR_PORTKEY_API_KEY",
            virtual_key="YOUR_OPENAI_VIRTUAL_KEY",
            config={
                "cache": {
                    "mode": "simple"
                }
            }
        )
    )

# Create agent with cached LLM
    researcher = Agent(
        role="Senior Research Scientist",
        goal="Discover groundbreaking insights about the assigned topic",
        backstory="You are an expert researcher with deep domain knowledge.",
        verbose=True,
        llm=portkey_llm
    )
    python theme={null}
    from crewai import Agent, LLM
    from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL

# Configure LLM with semantic caching
    portkey_llm = LLM(
        model="gpt-4o",
        base_url=PORTKEY_GATEWAY_URL,
        api_key="dummy",
        extra_headers=createHeaders(
            api_key="YOUR_PORTKEY_API_KEY",
            virtual_key="YOUR_OPENAI_VIRTUAL_KEY",
            config={
                "cache": {
                    "mode": "semantic"
                }
            }
        )
    )

# Create agent with semantically cached LLM
    researcher = Agent(
        role="Senior Research Scientist",
        goal="Discover groundbreaking insights about the assigned topic",
        backstory="You are an expert researcher with deep domain knowledge.",
        verbose=True,
        llm=portkey_llm
    )
    python theme={null}
from crewai import Agent, LLM
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL

**Examples:**

Example 1 (unknown):
```unknown
**Filter Analytics by User**

With metadata in place, you can filter analytics by user and analyze performance metrics on a per-user basis:

<Frame>
  <img />
</Frame>

This enables:

* Per-user cost tracking and budgeting
* Personalized user analytics
* Team or organization-level metrics
* Environment-specific monitoring (staging vs. production)

<Card title="Learn More About Metadata" icon="tags" href="https://portkey.ai/docs/product/observability/metadata">
  Explore how to use custom metadata to enhance your analytics
</Card>

### 6. Caching for Efficient Crews

Implement caching to make your CrewAI agents more efficient and cost-effective:

<Tabs>
  <Tab title="Simple Caching">
```

Example 2 (unknown):
```unknown
Simple caching performs exact matches on input prompts, caching identical requests to avoid redundant model executions.
  </Tab>

  <Tab title="Semantic Caching">
```

Example 3 (unknown):
```unknown
Semantic caching considers the contextual similarity between input requests, caching responses for semantically similar inputs.
  </Tab>
</Tabs>

### 7. Model Interoperability

CrewAI supports multiple LLM providers, and Portkey extends this capability by providing access to over 200 LLMs through a unified interface. You can easily switch between different models without changing your core agent logic:
```

---

## Create and execute a task with custom parameters

**URL:** llms-txt#create-and-execute-a-task-with-custom-parameters

**Contents:**
  - Multi-Stage Automation Workflow

research_task = Task(
    description="Conduct market research on AI tools market for 2024 in North America with detailed format",
    agent=research_agent,
    expected_output="Comprehensive market research report"
)

crew = Crew(
    agents=[research_agent],
    tasks=[research_task]
)

result = crew.kickoff()
python {2, 4-35} theme={null}
from crewai import Agent, Task, Crew, Process
from crewai_tools import InvokeCrewAIAutomationTool

**Examples:**

Example 1 (unknown):
```unknown
### Multi-Stage Automation Workflow
```

---

## Create and execute crew

**URL:** llms-txt#create-and-execute-crew

**Contents:**
  - Observability and Governance
- Tracing

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    verbose=True
)

result = crew.kickoff()
bash theme={null}
pip install traceloop-sdk
python theme={null}
from traceloop.sdk import Traceloop

**Examples:**

Example 1 (unknown):
```unknown
### Observability and Governance

Monitor your CrewAI agents through TrueFoundry's metrics tab:

<img alt="TrueFoundry metrics" />

With Truefoundry's AI gateway, you can monitor and analyze:

* **Performance Metrics**: Track key latency metrics like Request Latency, Time to First Token (TTFS), and Inter-Token Latency (ITL) with P99, P90, and P50 percentiles
* **Cost and Token Usage**: Gain visibility into your application's costs with detailed breakdowns of input/output tokens and the associated expenses for each model
* **Usage Patterns**: Understand how your application is being used with detailed analytics on user activity, model distribution, and team-based usage
* **Rate limit and Load balancing**: You can set up rate limiting, load balancing and fallback for your models

## Tracing

For a more detailed understanding on tracing, please see [getting-started-tracing](https://docs.truefoundry.com/docs/tracing/tracing-getting-started).For tracing, you can add the Traceloop SDK:
For tracing, you can add the Traceloop SDK:
```

Example 2 (unknown):
```unknown

```

---

## Create and execute tasks

**URL:** llms-txt#create-and-execute-tasks

**Contents:**
- Required Methods
  - Constructor: `__init__()`
  - Abstract Method: `call()`
  - Optional Methods
- Common Patterns
  - Error Handling
  - Custom Authentication
  - Stop Words Support
- Function Calling
- Troubleshooting

task = Task(
    description="Research the latest developments in AI",
    expected_output="A comprehensive summary",
    agent=agent
)

crew = Crew(agents=[agent], tasks=[task])
result = crew.kickoff()
python theme={null}
def __init__(self, model: str, api_key: str, temperature: Optional[float] = None):
    # REQUIRED: Call parent constructor with model and temperature
    super().__init__(model=model, temperature=temperature)
    
    # Your custom initialization
    self.api_key = api_key
python theme={null}
def supports_function_calling(self) -> bool:
    """Return True if your LLM supports function calling."""
    return True  # Default is True

def supports_stop_words(self) -> bool:
    """Return True if your LLM supports stop sequences."""
    return True  # Default is True

def get_context_window_size(self) -> int:
    """Return the context window size."""
    return 4096  # Default is 4096
python theme={null}
import requests

def call(self, messages, tools=None, callbacks=None, available_functions=None):
    try:
        response = requests.post(
            self.endpoint,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
        
    except requests.Timeout:
        raise TimeoutError("LLM request timed out")
    except requests.RequestException as e:
        raise RuntimeError(f"LLM request failed: {str(e)}")
    except (KeyError, IndexError) as e:
        raise ValueError(f"Invalid response format: {str(e)}")
python theme={null}
from crewai import BaseLLM
from typing import Optional

class CustomAuthLLM(BaseLLM):
    def __init__(self, model: str, auth_token: str, endpoint: str, temperature: Optional[float] = None):
        super().__init__(model=model, temperature=temperature)
        self.auth_token = auth_token
        self.endpoint = endpoint
    
    def call(self, messages, tools=None, callbacks=None, available_functions=None):
        headers = {
            "Authorization": f"Custom {self.auth_token}",  # Custom auth format
            "Content-Type": "application/json"
        }
        # Rest of implementation...
python theme={null}
def call(self, messages, tools=None, callbacks=None, available_functions=None):
    payload = {
        "model": self.model,
        "messages": messages,
        "stop": self.stop  # Include stop words in API call
    }
    # Make API call...

def supports_stop_words(self) -> bool:
    return True  # Your LLM supports stop sequences
python theme={null}
def call(self, messages, tools=None, callbacks=None, available_functions=None):
    response = self._make_api_call(messages, tools)
    content = response["choices"][0]["message"]["content"]
    
    # Manually truncate at stop words
    if self.stop:
        for stop_word in self.stop:
            if stop_word in content:
                content = content.split(stop_word)[0]
                break
    
    return content

def supports_stop_words(self) -> bool:
    return False  # Tell CrewAI we handle stop words manually
python theme={null}
import json

def call(self, messages, tools=None, callbacks=None, available_functions=None):
    # Convert string to message format
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]
    
    # Make API call
    response = self._make_api_call(messages, tools)
    message = response["choices"][0]["message"]
    
    # Check for function calls
    if "tool_calls" in message and available_functions:
        return self._handle_function_calls(
            message["tool_calls"], messages, tools, available_functions
        )
    
    return message["content"]

def _handle_function_calls(self, tool_calls, messages, tools, available_functions):
    """Handle function calling with proper message flow."""
    for tool_call in tool_calls:
        function_name = tool_call["function"]["name"]
        
        if function_name in available_functions:
            # Parse and execute function
            function_args = json.loads(tool_call["function"]["arguments"])
            function_result = available_functions[function_name](**function_args)
            
            # Add function call and result to message history
            messages.append({
                "role": "assistant",
                "content": None,
                "tool_calls": [tool_call]
            })
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "name": function_name,
                "content": str(function_result)
            })
            
            # Call LLM again with updated context
            return self.call(messages, tools, None, available_functions)
    
    return "Function call failed"
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## Required Methods

### Constructor: `__init__()`

**Critical**: You must call `super().__init__(model, temperature)` with the required parameters:
```

Example 2 (unknown):
```unknown
### Abstract Method: `call()`

The `call()` method is the heart of your LLM implementation. It must:

* Accept messages (string or list of dicts with 'role' and 'content')
* Return a string response
* Handle tools and function calling if supported
* Raise appropriate exceptions for errors

### Optional Methods
```

Example 3 (unknown):
```unknown
## Common Patterns

### Error Handling
```

Example 4 (unknown):
```unknown
### Custom Authentication
```

---

## Create and run crew

**URL:** llms-txt#create-and-run-crew

**Contents:**
- MCP Reference Formats
  - String-Based References
  - Structured Configurations
  - Mixed References
  - Tool Filtering

crew = Crew(agents=[research_agent], tasks=[research_task])
result = crew.kickoff()
python theme={null}
mcps=[
    # Full server - get all available tools
    "https://mcp.example.com/api",

# Specific tool from server using # syntax
    "https://api.weather.com/mcp#get_current_weather",

# Server with authentication parameters
    "https://mcp.exa.ai/mcp?api_key=your_key&profile=your_profile"
]
python theme={null}
mcps=[
    # Full AMP MCP service - get all available tools
    "crewai-amp:financial-data",

# Specific tool from AMP service using # syntax
    "crewai-amp:research-tools#pubmed_search",

# Multiple AMP services
    "crewai-amp:weather-service",
    "crewai-amp:market-analysis"
]
python theme={null}
from crewai.mcp import MCPServerStdio
from crewai.mcp.filters import create_static_tool_filter

mcps=[
    MCPServerStdio(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem"],
        env={"API_KEY": "your_key"},
        tool_filter=create_static_tool_filter(
            allowed_tool_names=["read_file", "write_file"]
        ),
        cache_tools_list=True,
    ),
    # Python-based server
    MCPServerStdio(
        command="python",
        args=["path/to/server.py"],
        env={"UV_PYTHON": "3.12", "API_KEY": "your_key"},
    ),
]
python theme={null}
from crewai.mcp import MCPServerHTTP

mcps=[
    # Streamable HTTP (default)
    MCPServerHTTP(
        url="https://api.example.com/mcp",
        headers={"Authorization": "Bearer your_token"},
        streamable=True,
        cache_tools_list=True,
    ),
    # Standard HTTP
    MCPServerHTTP(
        url="https://api.example.com/mcp",
        headers={"Authorization": "Bearer your_token"},
        streamable=False,
    ),
]
python theme={null}
from crewai.mcp import MCPServerSSE

mcps=[
    MCPServerSSE(
        url="https://stream.example.com/mcp/sse",
        headers={"Authorization": "Bearer your_token"},
        cache_tools_list=True,
    ),
]
python theme={null}
from crewai.mcp import MCPServerStdio, MCPServerHTTP

mcps=[
    # String references
    "https://external-api.com/mcp",              # External server
    "crewai-amp:financial-insights",             # AMP service

# Structured configurations
    MCPServerStdio(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem"],
    ),
    MCPServerHTTP(
        url="https://api.example.com/mcp",
        headers={"Authorization": "Bearer token"},
    ),
]
python theme={null}
from crewai.mcp import MCPServerStdio
from crewai.mcp.filters import create_static_tool_filter, create_dynamic_tool_filter, ToolFilterContext

**Examples:**

Example 1 (unknown):
```unknown
That's it! The MCP tools are automatically discovered and available to your agent.

## MCP Reference Formats

The `mcps` field supports both **string references** (for quick setup) and **structured configurations** (for full control). You can mix both formats in the same list.

### String-Based References

#### External MCP Servers
```

Example 2 (unknown):
```unknown
#### CrewAI AOP Marketplace
```

Example 3 (unknown):
```unknown
### Structured Configurations

#### Stdio Transport (Local Servers)

Perfect for local MCP servers that run as processes:
```

Example 4 (unknown):
```unknown
#### HTTP/Streamable HTTP Transport (Remote Servers)

For remote MCP servers over HTTP/HTTPS:
```

---

## Create and run the crew

**URL:** llms-txt#create-and-run-the-crew

**Contents:**
- Parameters
- Usage

crew = Crew(agents=[browser_agent], tasks=[browse_task])
result = crew.kickoff()
python Code theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## Parameters

The `MultiOnTool` accepts the following parameters during initialization:

* **api\_key**: Optional. Specifies the MultiOn API key. If not provided, it will look for the `MULTION_API_KEY` environment variable.
* **local**: Optional. Set to `True` to run the agent locally on your browser. Make sure the MultiOn browser extension is installed and API Enabled is checked. Default is `False`.
* **max\_steps**: Optional. Sets the maximum number of steps the MultiOn agent can take for a command. Default is `3`.

## Usage

When using the `MultiOnTool`, the agent will provide natural language instructions that the tool translates into web browsing actions. The tool returns the results of the browsing session along with a status.
```

---

## Create an agent

**URL:** llms-txt#create-an-agent

coding_agent = Agent(
    role="Python Data Analyst",
    goal="Analyze data and provide insights using Python",
    backstory="You are an experienced data analyst with strong Python skills.",
    allow_code_execution=True
)

---

## Create an agent by loading it from a repository

**URL:** llms-txt#create-an-agent-by-loading-it-from-a-repository

---

## Create an agent focused on document operations

**URL:** llms-txt#create-an-agent-focused-on-document-operations

document_reader = Agent(
    role="Document Reader",
    goal="Retrieve and analyze document content and properties",
    backstory="An AI assistant skilled in reading and analyzing document content.",
    apps=['microsoft_word/get_documents', 'microsoft_word/get_document_content', 'microsoft_word/get_document_properties']
)

---

## Create an agent focused on email management

**URL:** llms-txt#create-an-agent-focused-on-email-management

email_manager = Agent(
    role="Email Manager",
    goal="Retrieve, search, and organize email messages",
    backstory="An AI assistant skilled in email organization and management.",
    apps=['microsoft_outlook/get_messages']
)

---

## Create an agent focused on file operations

**URL:** llms-txt#create-an-agent-focused-on-file-operations

file_operator = Agent(
    role="File Operator",
    goal="Upload, download, and manage files with precision",
    backstory="An AI assistant skilled in file handling and content management.",
    apps=['microsoft_onedrive/upload_file', 'microsoft_onedrive/download_file', 'microsoft_onedrive/get_file_info']
)

---

## Create an agent focused on messaging

**URL:** llms-txt#create-an-agent-focused-on-messaging

messenger = Agent(
    role="Teams Messenger",
    goal="Send and retrieve messages in Teams channels",
    backstory="An AI assistant skilled in team communication and message management.",
    apps=['microsoft_teams/send_message', 'microsoft_teams/get_messages']
)

---

## Create an agent focused on text editing

**URL:** llms-txt#create-an-agent-focused-on-text-editing

text_editor = Agent(
    role="Document Editor",
    goal="Edit and update content in Google Docs documents",
    backstory="An AI assistant skilled in precise text editing and content management.",
    apps=['google_docs/insert_text', 'google_docs/replace_text', 'google_docs/delete_content_range']
)

---

## Create an agent for advanced document operations

**URL:** llms-txt#create-an-agent-for-advanced-document-operations

document_formatter = Agent(
    role="Document Formatter",
    goal="Apply advanced formatting and structure to Google Docs",
    backstory="An AI assistant that handles complex document formatting and organization.",
    apps=['google_docs/batch_update', 'google_docs/insert_page_break', 'google_docs/create_named_range']
)

---

## Create an agent for calendar and contact management

**URL:** llms-txt#create-an-agent-for-calendar-and-contact-management

scheduler = Agent(
    role="Calendar and Contact Manager",
    goal="Manage calendar events and maintain contact information",
    backstory="An AI assistant that handles scheduling and contact organization.",
    apps=['microsoft_outlook/create_calendar_event', 'microsoft_outlook/get_calendar_events', 'microsoft_outlook/create_contact']
)

---

## Create an agent for document management

**URL:** llms-txt#create-an-agent-for-document-management

document_organizer = Agent(
    role="Document Organizer",
    goal="Organize and clean up document collections",
    backstory="An AI assistant that helps maintain organized document libraries.",
    apps=['microsoft_word/get_documents', 'microsoft_word/get_document_properties', 'microsoft_word/delete_document']
)

---

## Create an agent for file organization and sharing

**URL:** llms-txt#create-an-agent-for-file-organization-and-sharing

file_organizer = Agent(
    role="File Organizer",
    goal="Organize files and create sharing links for collaboration",
    backstory="An AI assistant that excels at organizing files and managing sharing permissions.",
    apps=['microsoft_onedrive/search_files', 'microsoft_onedrive/move_item', 'microsoft_onedrive/share_item', 'microsoft_onedrive/create_folder']
)

---

## Create an agent for meeting management

**URL:** llms-txt#create-an-agent-for-meeting-management

meeting_scheduler = Agent(
    role="Meeting Scheduler",
    goal="Create and manage Teams meetings",
    backstory="An AI assistant that handles meeting scheduling and organization.",
    apps=['microsoft_teams/create_meeting', 'microsoft_teams/search_online_meetings_by_join_url']
)

---

## Create an agent that uses the tool

**URL:** llms-txt#create-an-agent-that-uses-the-tool

researcher = Agent(
    role='Market Researcher',
    goal='Find information about the latest AI trends',
    backstory='An expert market researcher specializing in technology.',
    tools=[tavily_tool],
    verbose=True
)

---

## Create an Agent using Llama-specific layouts

**URL:** llms-txt#create-an-agent-using-llama-specific-layouts

principal_engineer = Agent(
    role="Principal Engineer",
    goal="Oversee AI architecture and make high-level decisions",
    backstory="You are the lead engineer responsible for critical AI systems",
    verbose=True,
    llm="groq/llama-3.3-70b-versatile",  # Using the Llama 3 model
    system_template=system_template,
    prompt_template=prompt_template,
    response_template=response_template,
    tools=[DirectoryReadTool(), FileReadTool()]
)

---

## Create an agent with access to all tools

**URL:** llms-txt#create-an-agent-with-access-to-all-tools

**Contents:**
  - Loading Specific Tools Only

automation_expert = Agent(
    role='Automation Expert',
    goal='Automate workflows across multiple platforms',
    backstory='I can work with any tool in the toolbox to get things done.',
    tools=tools,
    verbose=True
)

automation_task = Task(
    description="Check for any high-priority issues in Linear and post a summary to Slack.",
    agent=automation_expert
)

crew = Crew(
    agents=[automation_expert],
    tasks=[automation_task],
    verbose=True
)

result = crew.kickoff()
python {2, 4-10} theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import MergeAgentHandlerTool

**Examples:**

Example 1 (unknown):
```unknown
### Loading Specific Tools Only

Load only the tools you need:
```

---

## Create an agent with all available parameters

**URL:** llms-txt#create-an-agent-with-all-available-parameters

**Contents:**
  - Parameter Details
- Agent Tools

agent = Agent(
    role="Senior Data Scientist",
    goal="Analyze and interpret complex datasets to provide actionable insights",
    backstory="With over 10 years of experience in data science and machine learning, "
              "you excel at finding patterns in complex datasets.",
    llm="gpt-4",  # Default: OPENAI_MODEL_NAME or "gpt-4"
    function_calling_llm=None,  # Optional: Separate LLM for tool calling
    verbose=False,  # Default: False
    allow_delegation=False,  # Default: False
    max_iter=20,  # Default: 20 iterations
    max_rpm=None,  # Optional: Rate limit for API calls
    max_execution_time=None,  # Optional: Maximum execution time in seconds
    max_retry_limit=2,  # Default: 2 retries on error
    allow_code_execution=False,  # Default: False
    code_execution_mode="safe",  # Default: "safe" (options: "safe", "unsafe")
    respect_context_window=True,  # Default: True
    use_system_prompt=True,  # Default: True
    multimodal=False,  # Default: False
    inject_date=False,  # Default: False
    date_format="%Y-%m-%d",  # Default: ISO format
    reasoning=False,  # Default: False
    max_reasoning_attempts=None,  # Default: None
    tools=[SerperDevTool()],  # Optional: List of tools
    knowledge_sources=None,  # Optional: List of knowledge sources
    embedder=None,  # Optional: Custom embedder configuration
    system_template=None,  # Optional: Custom system prompt template
    prompt_template=None,  # Optional: Custom prompt template
    response_template=None,  # Optional: Custom response template
    step_callback=None,  # Optional: Callback function for monitoring
)
python Code theme={null}
research_agent = Agent(
    role="Research Analyst",
    goal="Find and summarize information about specific topics",
    backstory="You are an experienced researcher with attention to detail",
    tools=[SerperDevTool()],
    verbose=True  # Enable logging for debugging
)
python Code theme={null}
dev_agent = Agent(
    role="Senior Python Developer",
    goal="Write and debug Python code",
    backstory="Expert Python developer with 10 years of experience",
    allow_code_execution=True,
    code_execution_mode="safe",  # Uses Docker for safety
    max_execution_time=300,  # 5-minute timeout
    max_retry_limit=3  # More retries for complex code tasks
)
python Code theme={null}
analysis_agent = Agent(
    role="Data Analyst",
    goal="Perform deep analysis of large datasets",
    backstory="Specialized in big data analysis and pattern recognition",
    memory=True,
    respect_context_window=True,
    max_rpm=10,  # Limit API calls
    function_calling_llm="gpt-4o-mini"  # Cheaper model for tool calls
)
python Code theme={null}
custom_agent = Agent(
    role="Customer Service Representative",
    goal="Assist customers with their inquiries",
    backstory="Experienced in customer support with a focus on satisfaction",
    system_template="""<|start_header_id|>system<|end_header_id|>
                        {{ .System }}<|eot_id|>""",
    prompt_template="""<|start_header_id|>user<|end_header_id|>
                        {{ .Prompt }}<|eot_id|>""",
    response_template="""<|start_header_id|>assistant<|end_header_id|>
                        {{ .Response }}<|eot_id|>""",
)
python Code theme={null}
strategic_agent = Agent(
    role="Market Analyst",
    goal="Track market movements with precise date references and strategic planning",
    backstory="Expert in time-sensitive financial analysis and strategic reporting",
    inject_date=True,  # Automatically inject current date into tasks
    date_format="%B %d, %Y",  # Format as "May 21, 2025"
    reasoning=True,  # Enable strategic planning
    max_reasoning_attempts=2,  # Limit planning iterations
    verbose=True
)
python Code theme={null}
reasoning_agent = Agent(
    role="Strategic Planner",
    goal="Analyze complex problems and create detailed execution plans",
    backstory="Expert strategic planner who methodically breaks down complex challenges",
    reasoning=True,  # Enable reasoning and planning
    max_reasoning_attempts=3,  # Limit reasoning attempts
    max_iter=30,  # Allow more iterations for complex planning
    verbose=True
)
python Code theme={null}
multimodal_agent = Agent(
    role="Visual Content Analyst",
    goal="Analyze and process both text and visual content",
    backstory="Specialized in multimodal analysis combining text and image understanding",
    multimodal=True,  # Enable multimodal capabilities
    verbose=True
)
python Code theme={null}
from crewai import Agent
from crewai_tools import SerperDevTool, WikipediaTools

**Examples:**

Example 1 (unknown):
```unknown
Let's break down some key parameter combinations for common use cases:

#### Basic Research Agent
```

Example 2 (unknown):
```unknown
#### Code Development Agent
```

Example 3 (unknown):
```unknown
#### Long-Running Analysis Agent
```

Example 4 (unknown):
```unknown
#### Custom Template Agent
```

---

## Create an agent with Asana capabilities

**URL:** llms-txt#create-an-agent-with-asana-capabilities

asana_agent = Agent(
    role="Project Manager",
    goal="Manage tasks and projects in Asana efficiently",
    backstory="An AI assistant specialized in project management and task coordination.",
    apps=['asana']  # All Asana actions will be available
)

---

## Create an agent with Box capabilities

**URL:** llms-txt#create-an-agent-with-box-capabilities

box_agent = Agent(
    role="Document Manager",
    goal="Manage files and folders in Box efficiently",
    backstory="An AI assistant specialized in document management and file organization.",
    apps=['box']  # All Box actions will be available
)

---

## Create an agent with Clickup capabilities

**URL:** llms-txt#create-an-agent-with-clickup-capabilities

clickup_agent = Agent(
    role="Task Manager",
    goal="Manage tasks and projects in ClickUp efficiently",
    backstory="An AI assistant specialized in task management and productivity coordination.",
    apps=['clickup']  # All Clickup actions will be available
)

---

## Create an agent with code execution enabled

**URL:** llms-txt#create-an-agent-with-code-execution-enabled

coding_agent = Agent(
    role="Python Data Analyst",
    goal="Analyze data and provide insights using Python",
    backstory="You are an experienced data analyst with strong Python skills.",
    allow_code_execution=True
)

---

## Create an agent with Excel capabilities

**URL:** llms-txt#create-an-agent-with-excel-capabilities

excel_agent = Agent(
    role="Excel Data Manager",
    goal="Manage Excel workbooks and data efficiently",
    backstory="An AI assistant specialized in Excel data management and analysis.",
    apps=['microsoft_excel']  # All Excel actions will be available
)

---

## Create an agent with Github capabilities

**URL:** llms-txt#create-an-agent-with-github-capabilities

github_agent = Agent(
    role="Repository Manager",
    goal="Manage GitHub repositories, issues, and releases efficiently",
    backstory="An AI assistant specialized in repository management and issue tracking.",
    apps=['github']  # All Github actions will be available
)

---

## Create an agent with Gmail capabilities

**URL:** llms-txt#create-an-agent-with-gmail-capabilities

gmail_agent = Agent(
    role="Email Manager",
    goal="Manage email communications and messages efficiently",
    backstory="An AI assistant specialized in email management and communication.",
    apps=['gmail']  # All Gmail actions will be available
)

---

## Create an agent with Google Calendar capabilities

**URL:** llms-txt#create-an-agent-with-google-calendar-capabilities

calendar_agent = Agent(
    role="Schedule Manager",
    goal="Manage calendar events and scheduling efficiently",
    backstory="An AI assistant specialized in calendar management and scheduling coordination.",
    apps=['google_calendar']  # All Google Calendar actions will be available
)

---

## Create an agent with Google Contacts capabilities

**URL:** llms-txt#create-an-agent-with-google-contacts-capabilities

contacts_agent = Agent(
    role="Contact Manager",
    goal="Manage contacts and directory information efficiently",
    backstory="An AI assistant specialized in contact management and directory operations.",
    apps=['google_contacts']  # All Google Contacts actions will be available
)

---

## Create an agent with Google Docs capabilities

**URL:** llms-txt#create-an-agent-with-google-docs-capabilities

docs_agent = Agent(
    role="Document Creator",
    goal="Create and manage Google Docs documents efficiently",
    backstory="An AI assistant specialized in Google Docs document creation and editing.",
    apps=['google_docs']  # All Google Docs actions will be available
)

---

## Create an agent with Google Drive capabilities

**URL:** llms-txt#create-an-agent-with-google-drive-capabilities

drive_agent = Agent(
    role="File Manager",
    goal="Manage files and folders in Google Drive efficiently",
    backstory="An AI assistant specialized in document and file management.",
    apps=['google_drive']  # All Google Drive actions will be available
)

---

## Create an agent with Google Sheets capabilities

**URL:** llms-txt#create-an-agent-with-google-sheets-capabilities

sheets_agent = Agent(
    role="Data Manager",
    goal="Manage spreadsheet data and track information efficiently",
    backstory="An AI assistant specialized in data management and spreadsheet operations.",
    apps=['google_sheets']
)

---

## Create an agent with Google Slides capabilities

**URL:** llms-txt#create-an-agent-with-google-slides-capabilities

slides_agent = Agent(
    role="Presentation Manager",
    goal="Create and manage presentations efficiently",
    backstory="An AI assistant specialized in presentation creation and content management.",
    apps=['google_slides']  # All Google Slides actions will be available
)

---

## Create an agent with HubSpot capabilities

**URL:** llms-txt#create-an-agent-with-hubspot-capabilities

hubspot_agent = Agent(
    role="CRM Manager",
    goal="Manage company and contact records in HubSpot",
    backstory="An AI assistant specialized in CRM management.",
    apps=['hubspot']  # All HubSpot actions will be available
)

---

## Create an agent with Jira capabilities

**URL:** llms-txt#create-an-agent-with-jira-capabilities

jira_agent = Agent(
    role="Issue Manager",
    goal="Manage Jira issues and track project progress efficiently",
    backstory="An AI assistant specialized in issue tracking and project management.",
    apps=['jira']  # All Jira actions will be available
)

---

## Create an agent with Linear capabilities

**URL:** llms-txt#create-an-agent-with-linear-capabilities

linear_agent = Agent(
    role="Development Manager",
    goal="Manage Linear issues and track development progress efficiently",
    backstory="An AI assistant specialized in software development project management.",
    apps=['linear']  # All Linear actions will be available
)

---

## Create an agent with Microsoft OneDrive capabilities

**URL:** llms-txt#create-an-agent-with-microsoft-onedrive-capabilities

onedrive_agent = Agent(
    role="File Manager",
    goal="Manage files and folders in OneDrive efficiently",
    backstory="An AI assistant specialized in Microsoft OneDrive file operations and organization.",
    apps=['microsoft_onedrive']  # All OneDrive actions will be available
)

---

## Create an agent with Microsoft Outlook capabilities

**URL:** llms-txt#create-an-agent-with-microsoft-outlook-capabilities

outlook_agent = Agent(
    role="Email Assistant",
    goal="Manage emails, calendar events, and contacts efficiently",
    backstory="An AI assistant specialized in Microsoft Outlook operations and communication management.",
    apps=['microsoft_outlook']  # All Outlook actions will be available
)

---

## Create an agent with Microsoft Teams capabilities

**URL:** llms-txt#create-an-agent-with-microsoft-teams-capabilities

teams_agent = Agent(
    role="Teams Coordinator",
    goal="Manage Teams communication and meetings efficiently",
    backstory="An AI assistant specialized in Microsoft Teams operations and team collaboration.",
    apps=['microsoft_teams']  # All Teams actions will be available
)

---

## Create an agent with Microsoft Word capabilities

**URL:** llms-txt#create-an-agent-with-microsoft-word-capabilities

word_agent = Agent(
    role="Document Manager",
    goal="Manage Word documents and text files efficiently",
    backstory="An AI assistant specialized in Microsoft Word document operations and content management.",
    apps=['microsoft_word']  # All Word actions will be available
)

---

## Create an agent with Notion capabilities

**URL:** llms-txt#create-an-agent-with-notion-capabilities

notion_agent = Agent(
    role="Workspace Manager",
    goal="Manage workspace users and facilitate collaboration through comments",
    backstory="An AI assistant specialized in user management and team collaboration.",
    apps=['notion']  # All Notion actions will be available
)

---

## Create an agent with reasoning enabled

**URL:** llms-txt#create-an-agent-with-reasoning-enabled

agent = Agent(
    role="Data Analyst",
    goal="Analyze data and provide insights",
    reasoning=True,
    max_reasoning_attempts=3
)

---

## Create an agent with Salesforce capabilities

**URL:** llms-txt#create-an-agent-with-salesforce-capabilities

salesforce_agent = Agent(
    role="CRM Manager",
    goal="Manage customer relationships and sales processes efficiently",
    backstory="An AI assistant specialized in CRM operations and sales automation.",
    apps=['salesforce']  # All Salesforce actions will be available
)

---

## Create an agent with SharePoint capabilities

**URL:** llms-txt#create-an-agent-with-sharepoint-capabilities

sharepoint_agent = Agent(
    role="SharePoint Manager",
    goal="Manage SharePoint sites, lists, and documents efficiently",
    backstory="An AI assistant specialized in SharePoint content management and collaboration.",
    apps=['microsoft_sharepoint']  # All SharePoint actions will be available
)

---

## Create an agent with Shopify capabilities

**URL:** llms-txt#create-an-agent-with-shopify-capabilities

shopify_agent = Agent(
    role="E-commerce Manager",
    goal="Manage online store operations and customer relationships efficiently",
    backstory="An AI assistant specialized in e-commerce operations and online store management.",
    apps=['shopify']  # All Shopify actions will be available
)

---

## Create an agent with Slack capabilities

**URL:** llms-txt#create-an-agent-with-slack-capabilities

slack_agent = Agent(
    role="Team Communication Manager",
    goal="Facilitate team communication and coordinate collaboration efficiently",
    backstory="An AI assistant specialized in team communication and workspace coordination.",
    apps=['slack']  # All Slack actions will be available
)

---

## Create an agent with Stripe capabilities

**URL:** llms-txt#create-an-agent-with-stripe-capabilities

stripe_agent = Agent(
    role="Payment Manager",
    goal="Manage customer payments, subscriptions, and billing operations efficiently",
    backstory="An AI assistant specialized in payment processing and subscription management.",
    apps=['stripe']  # All Stripe actions will be available
)

---

## Create an agent with the knowledge store

**URL:** llms-txt#create-an-agent-with-the-knowledge-store

**Contents:**
- Supported Knowledge Sources
  - Text File Knowledge Source
  - PDF Knowledge Source
  - CSV Knowledge Source
  - Excel Knowledge Source
  - JSON Knowledge Source
- Agent vs Crew Knowledge: Complete Guide
  - How Knowledge Initialization Actually Works

agent = Agent(
    role="About papers",
    goal="You know everything about the papers.",
    backstory="You are a master at understanding papers and their content.",
    verbose=True,
    allow_delegation=False,
    llm=llm,
)

task = Task(
    description="Answer the following questions about the papers: {question}",
    expected_output="An answer to the question.",
    agent=agent,
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True,
    process=Process.sequential,
    knowledge_sources=[content_source],
)

result = crew.kickoff(
    inputs={"question": "What is the reward hacking paper about? Be sure to provide sources."}
)
python theme={null}
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource

text_source = TextFileKnowledgeSource(
    file_paths=["document.txt", "another.txt"]
)
python theme={null}
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource

pdf_source = PDFKnowledgeSource(
    file_paths=["document.pdf", "another.pdf"]
)
python theme={null}
from crewai.knowledge.source.csv_knowledge_source import CSVKnowledgeSource

csv_source = CSVKnowledgeSource(
    file_paths=["data.csv"]
)
python theme={null}
from crewai.knowledge.source.excel_knowledge_source import ExcelKnowledgeSource

excel_source = ExcelKnowledgeSource(
    file_paths=["spreadsheet.xlsx"]
)
python theme={null}
from crewai.knowledge.source.json_knowledge_source import JSONKnowledgeSource

json_source = JSONKnowledgeSource(
    file_paths=["data.json"]
)
python theme={null}
from crewai import Agent, Task, Crew
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

**Examples:**

Example 1 (unknown):
```unknown
## Supported Knowledge Sources

CrewAI supports various types of knowledge sources out of the box:

<CardGroup>
  <Card title="Text Sources" icon="text">
    * Raw strings
    * Text files (.txt)
    * PDF documents
  </Card>

  <Card title="Structured Data" icon="table">
    * CSV files
    * Excel spreadsheets
    * JSON documents
  </Card>
</CardGroup>

### Text File Knowledge Source
```

Example 2 (unknown):
```unknown
### PDF Knowledge Source
```

Example 3 (unknown):
```unknown
### CSV Knowledge Source
```

Example 4 (unknown):
```unknown
### Excel Knowledge Source
```

---

## Create an agent with the tool

**URL:** llms-txt#create-an-agent-with-the-tool

research_agent = Agent(
    role="Research Coordinator",
    goal="Coordinate and execute market research tasks",
    backstory="You are an expert at coordinating research tasks and leveraging automation tools.",
    tools=[market_research_tool],
    verbose=True
)

---

## Create an agent with Zendesk capabilities

**URL:** llms-txt#create-an-agent-with-zendesk-capabilities

zendesk_agent = Agent(
    role="Support Manager",
    goal="Manage customer support tickets and provide excellent customer service",
    backstory="An AI assistant specialized in customer support operations and ticket management.",
    apps=['zendesk']  # All Zendesk actions will be available
)

---

## Create a coding agent with the custom tool

**URL:** llms-txt#create-a-coding-agent-with-the-custom-tool

coding_agent = Agent(
        role="Data Scientist",
        goal="Produce amazing reports on AI",
        backstory="You work with data and AI",
        tools=[MyCustomTool(result_as_answer=True)],
    )

---

## Create a CrewAI agent that uses the tool

**URL:** llms-txt#create-a-crewai-agent-that-uses-the-tool

project_manager = Agent(
    role='Project Manager',
    goal='Manage project tasks and issues efficiently',
    backstory='I am an expert at tracking project work and creating actionable tasks.',
    tools=[linear_create_tool],
    verbose=True
)

---

## Create a crew

**URL:** llms-txt#create-a-crew

analysis_crew = Crew(
    agents=[coding_agent],
    tasks=[data_analysis_task]
)

---

## Create a crew and add the task

**URL:** llms-txt#create-a-crew-and-add-the-task

analysis_crew = Crew(
    agents=[coding_agent],
    tasks=[data_analysis_task],
    verbose=True,
    memory=False
)

datasets = [
  { "ages": [25, 30, 35, 40, 45] },
  { "ages": [20, 25, 30, 35, 40] },
  { "ages": [30, 35, 40, 45, 50] }
]

---

## Create a crew and run the task

**URL:** llms-txt#create-a-crew-and-run-the-task

**Contents:**
- Error Handling

crew = Crew(agents=[analyst], tasks=[analysis_task])
result = crew.kickoff()

print(result)
python theme={null}
from crewai import Agent, Task
import logging

**Examples:**

Example 1 (unknown):
```unknown
## Error Handling

The reasoning process is designed to be robust, with error handling built in. If an error occurs during reasoning, the agent will proceed with executing the task without the reasoning plan. This ensures that tasks can still be executed even if the reasoning process fails.

Here's how to handle potential errors in your code:
```

---

## Create a Crew for the task

**URL:** llms-txt#create-a-crew-for-the-task

llama_crew = Crew(
    agents=[principal_engineer],
    tasks=[engineering_task],
    process=Process.sequential,
    verbose=True
)

---

## Create a crew with sequential processing

**URL:** llms-txt#create-a-crew-with-sequential-processing

**Contents:**
  - Custom Session Management

crew = Crew(
    agents=[code_reviewer, task_manager, communicator],
    tasks=[review_task, update_task, notify_task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff()
python {2, 4-17} theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import MergeAgentHandlerTool

**Examples:**

Example 1 (unknown):
```unknown
### Custom Session Management

Maintain context across multiple tool calls using session IDs:
```

---

## Create a crew with the agents and tasks

**URL:** llms-txt#create-a-crew-with-the-agents-and-tasks

crew = Crew(
    agents=[researcher, analyst, summarizer],
    tasks=[research_task, analysis_task, summary_task],
    process=Process.sequential,
    verbose=2
)

---

## Create a crew with the agent

**URL:** llms-txt#create-a-crew-with-the-agent

crew = Crew(
    agents=[project_manager],
    tasks=[create_issue_task],
    verbose=True
)

---

## Create a crew with the tasks

**URL:** llms-txt#create-a-crew-with-the-tasks

crew = Crew(
    agents=[data_fetcher_agent, data_processor_agent, summary_generator_agent],
    tasks=[task1, conditional_task, task3],
    verbose=True,
    planning=True
)

---

## Create a crew with your custom prompt file

**URL:** llms-txt#create-a-crew-with-your-custom-prompt-file

crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    prompt_file="path/to/custom_prompts.json",
    verbose=True
)

---

## Create a multimodal agent

**URL:** llms-txt#create-a-multimodal-agent

image_analyst = Agent(
    role="Product Analyst",
    goal="Analyze product images and provide detailed descriptions",
    backstory="Expert in visual product analysis with deep knowledge of design and features",
    multimodal=True
)

---

## Create a multimodal agent for detailed analysis

**URL:** llms-txt#create-a-multimodal-agent-for-detailed-analysis

expert_analyst = Agent(
    role="Visual Quality Inspector",
    goal="Perform detailed quality analysis of product images",
    backstory="Senior quality control expert with expertise in visual inspection",
    multimodal=True  # AddImageTool is automatically included
)

---

## Create a task for the agent

**URL:** llms-txt#create-a-task-for-the-agent

create_issue_task = Task(
    description="Create a new high-priority issue in Linear titled 'Implement user authentication' with a detailed description of the requirements.",
    agent=project_manager,
    expected_output="Confirmation that the issue was created with its ID"
)

---

## Create a task for the agent to extract specific content

**URL:** llms-txt#create-a-task-for-the-agent-to-extract-specific-content

extract_task = Task(
    description="Extract the main heading and summary from example.com",
    expected_output="The main heading and summary from the website",
    agent=web_scraper_agent,
)

---

## Create a task for the agent to extract specific elements

**URL:** llms-txt#create-a-task-for-the-agent-to-extract-specific-elements

extract_task = Task(
    description="""
    Extract all product titles from the featured products section on example.com.
    Use the CSS selector '.product-title' to target the title elements.
    """,
    expected_output="A list of product titles from the website",
    agent=web_scraper_agent,
)

---

## Create a task for the agent to read a specific file

**URL:** llms-txt#create-a-task-for-the-agent-to-read-a-specific-file

read_config_task = Task(
    description="Read the application configuration file from {my_bucket} and extract the database connection settings.",
    expected_output="The database connection settings from the configuration file.",
    agent=file_reader_agent,
)

---

## Create a task for the agent to write a specific file

**URL:** llms-txt#create-a-task-for-the-agent-to-write-a-specific-file

write_config_task = Task(
    description="""
    Create a configuration file with the following database settings:
    - host: db.example.com
    - port: 5432
    - username: app_user
    - password: secure_password
    
    Save this configuration as JSON to {my_bucket}.
    """,
    expected_output="Confirmation that the configuration file was successfully saved to S3.",
    agent=file_writer_agent,
)

---

## Create a task that instructs the agent to handle errors

**URL:** llms-txt#create-a-task-that-instructs-the-agent-to-handle-errors

**Contents:**
- Implementation Details
- Conclusion

error_handling_task = Task(
    description="""
    Extract content from a potentially problematic website and make sure to handle any 
    scraping failures gracefully by setting ignore_scrape_failures to True.
    """,
    expected_output="Either the extracted content or a graceful error message",
    agent=web_scraper_agent,
)
python Code theme={null}
class ScrapflyScrapeWebsiteTool(BaseTool):
    name: str = "Scrapfly web scraping API tool"
    description: str = (
        "Scrape a webpage url using Scrapfly and return its content as markdown or text"
    )
    
    # Implementation details...
    
    def _run(
        self,
        url: str,
        scrape_format: str = "markdown",
        scrape_config: Optional[Dict[str, Any]] = None,
        ignore_scrape_failures: Optional[bool] = None,
    ):
        from scrapfly import ScrapeApiResponse, ScrapeConfig

scrape_config = scrape_config if scrape_config is not None else {}
        try:
            response: ScrapeApiResponse = self.scrapfly.scrape(
                ScrapeConfig(url, format=scrape_format, **scrape_config)
            )
            return response.scrape_result["content"]
        except Exception as e:
            if ignore_scrape_failures:
                logger.error(f"Error fetching data from {url}, exception: {e}")
                return None
            else:
                raise e
```

The `ScrapflyScrapeWebsiteTool` provides a powerful way to extract content from websites using Scrapfly's advanced web scraping capabilities. With features like headless browser support, proxies, and anti-bot bypass, it can handle complex websites and extract content in various formats. This tool is particularly useful for data extraction, content monitoring, and research tasks where reliable web scraping is required.

**Examples:**

Example 1 (unknown):
```unknown
## Implementation Details

The `ScrapflyScrapeWebsiteTool` uses the Scrapfly SDK to interact with the Scrapfly API:
```

---

## Create collaborative agents

**URL:** llms-txt#create-collaborative-agents

researcher = Agent(
    role="Research Specialist",
    goal="Find accurate, up-to-date information on any topic",
    backstory="""You're a meticulous researcher with expertise in finding 
    reliable sources and fact-checking information across various domains.""",
    allow_delegation=True,
    verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="Create engaging, well-structured content",
    backstory="""You're a skilled content writer who excels at transforming 
    research into compelling, readable content for different audiences.""",
    allow_delegation=True,
    verbose=True
)

editor = Agent(
    role="Content Editor",
    goal="Ensure content quality and consistency",
    backstory="""You're an experienced editor with an eye for detail, 
    ensuring content meets high standards for clarity and accuracy.""",
    allow_delegation=True,
    verbose=True
)

---

## Create collaborative crew

**URL:** llms-txt#create-collaborative-crew

**Contents:**
- Collaboration Patterns
  - Pattern 1: Research → Write → Edit
  - Pattern 2: Collaborative Single Task
- Hierarchical Collaboration

crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[article_task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff()
python theme={null}
research_task = Task(
    description="Research the latest developments in quantum computing",
    expected_output="Comprehensive research summary with key findings and sources",
    agent=researcher
)

writing_task = Task(
    description="Write an article based on the research findings",
    expected_output="Engaging 800-word article about quantum computing",
    agent=writer,
    context=[research_task]  # Gets research output as context
)

editing_task = Task(
    description="Edit and polish the article for publication",
    expected_output="Publication-ready article with improved clarity and flow",
    agent=editor,
    context=[writing_task]  # Gets article draft as context
)
python theme={null}
collaborative_task = Task(
    description="""Create a marketing strategy for a new AI product.
    
    Writer: Focus on messaging and content strategy
    Researcher: Provide market analysis and competitor insights
    
    Work together to create a comprehensive strategy.""",
    expected_output="Complete marketing strategy with research backing",
    agent=writer  # Lead agent, but can delegate to researcher
)
python theme={null}
from crewai import Agent, Crew, Task, Process

**Examples:**

Example 1 (unknown):
```unknown
## Collaboration Patterns

### Pattern 1: Research → Write → Edit
```

Example 2 (unknown):
```unknown
### Pattern 2: Collaborative Single Task
```

Example 3 (unknown):
```unknown
## Hierarchical Collaboration

For complex projects, use a hierarchical process with a manager agent:
```

---

## Create components - fingerprints are automatically generated

**URL:** llms-txt#create-components---fingerprints-are-automatically-generated

agent = Agent(
    role="Data Scientist",
    goal="Analyze data",
    backstory="Expert in data analysis"
)

crew = Crew(
    agents=[agent],
    tasks=[]
)

task = Task(
    description="Analyze customer data",
    expected_output="Insights from data analysis",
    agent=agent
)

---

## Create comprehensive research task

**URL:** llms-txt#create-comprehensive-research-task

research_task = Task(
    description="""Research the impact of AI agents on business productivity.
    Include current weather impacts on remote work, financial market trends,
    and recent academic publications on AI agent frameworks.""",
    expected_output="""Comprehensive report covering:
    1. AI agent business impact analysis
    2. Weather considerations for remote work
    3. Financial market trends related to AI
    4. Academic research citations and insights
    5. Competitive landscape analysis""",
    agent=multi_source_agent
)

---

## Create CrewAI agents

**URL:** llms-txt#create-crewai-agents

search_agent = Agent(
    role="Senior Semantic Search Agent",
    goal="Find and analyze documents based on semantic search",
    backstory="""You are an expert research assistant who can find relevant
    information using semantic search in a Qdrant database.""",
    tools=[qdrant_tool],
    verbose=True
)

answer_agent = Agent(
    role="Senior Answer Assistant",
    goal="Generate answers to questions based on the context provided",
    backstory="""You are an expert answer assistant who can generate
    answers to questions based on the context provided.""",
    tools=[qdrant_tool],
    verbose=True
)

---

## Create specialized agents

**URL:** llms-txt#create-specialized-agents

code_reviewer = Agent(
    role='Code Reviewer',
    goal='Review pull requests and ensure code quality',
    backstory='I am an expert at reviewing code changes and providing constructive feedback.',
    tools=github_tools
)

task_manager = Agent(
    role='Task Manager',
    goal='Track and update project tasks based on code changes',
    backstory='I keep the project board up to date with the latest development progress.',
    tools=linear_tools
)

communicator = Agent(
    role='Team Communicator',
    goal='Keep the team informed about important updates',
    backstory='I make sure everyone knows what is happening in the project.',
    tools=[slack_tool]
)

---

## Create specialized tools for different agents

**URL:** llms-txt#create-specialized-tools-for-different-agents

github_tools = MergeAgentHandlerTool.from_tool_pack(
    tool_pack_id="134e0111-0f67-44f6-98f0-597000290bb3",
    registered_user_id="91b2b905-e866-40c8-8be2-efe53827a0aa",
    tool_names=["github__create_pull_request", "github__get_pull_requests"]
)

linear_tools = MergeAgentHandlerTool.from_tool_pack(
    tool_pack_id="134e0111-0f67-44f6-98f0-597000290bb3",
    registered_user_id="91b2b905-e866-40c8-8be2-efe53827a0aa",
    tool_names=["linear__create_issue", "linear__update_issue"]
)

slack_tool = MergeAgentHandlerTool.from_tool_name(
    tool_name="slack__post_message",
    tool_pack_id="134e0111-0f67-44f6-98f0-597000290bb3",
    registered_user_id="91b2b905-e866-40c8-8be2-efe53827a0aa"
)

---

## Create tasks for your agents

**URL:** llms-txt#create-tasks-for-your-agents

research_task = Task(
    description="""Conduct a comprehensive analysis of the latest advancements in AI in 2024.
    Identify key trends, breakthrough technologies, and potential industry impacts.""",
    expected_output="Full analysis report in bullet points",
    agent=researcher,
)

writing_task = Task(
    description="""Using the insights provided, develop an engaging blog
    post that highlights the most significant AI advancements.
    Your post should be informative yet accessible, catering to a tech-savvy audience.""",
    expected_output="Full blog post of at least 4 paragraphs",
    agent=writer,
)

---

## Create the crew

**URL:** llms-txt#create-the-crew

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    verbose=True
)

---

## Create your agent

**URL:** llms-txt#create-your-agent

researcher = Agent(
    role='Senior Research Analyst',
    goal='Uncover cutting-edge developments in AI',
    backstory="You are an expert researcher at a tech think tank...",
    verbose=True,
    llm=llm
)

---

## Creating a CrewAI Project

**URL:** llms-txt#creating-a-crewai-project

**Contents:**
- Enterprise Installation Options
- Next Steps

We recommend using the `YAML` template scaffolding for a structured approach to defining agents and tasks. Here's how to get started:

<Steps>
  <Step title="Generate Project Scaffolding">
    * Run the `crewai` CLI command:

* This creates a new project with the following structure:
      
  </Step>

<Step title="Customize Your Project">
    * Your project will contain these essential files:
      | File          | Purpose                                  |
      | ------------- | ---------------------------------------- |
      | `agents.yaml` | Define your AI agents and their roles    |
      | `tasks.yaml`  | Set up agent tasks and workflows         |
      | `.env`        | Store API keys and environment variables |
      | `main.py`     | Project entry point and execution flow   |
      | `crew.py`     | Crew orchestration and coordination      |
      | `tools/`      | Directory for custom agent tools         |
      | `knowledge/`  | Directory for knowledge base             |

* Start by editing `agents.yaml` and `tasks.yaml` to define your crew's behavior.

* Keep sensitive information like API keys in `.env`.
  </Step>

<Step title="Run your Crew">
    * Before you run your crew, make sure to run:
      
    * If you need to install additional packages, use:
      
    * To run your crew, execute the following command in the root of your project:
      
  </Step>
</Steps>

## Enterprise Installation Options

<Note type="info">
  For teams and organizations, CrewAI offers enterprise deployment options that eliminate setup complexity:

### CrewAI AOP (SaaS)

* Zero installation required - just sign up for free at [app.crewai.com](https://app.crewai.com)
  * Automatic updates and maintenance
  * Managed infrastructure and scaling
  * Build Crews with no Code

### CrewAI Factory (Self-hosted)

* Containerized deployment for your infrastructure
  * Supports any hyperscaler including on prem deployments
  * Integration with your existing security systems

<Card title="Explore Enterprise Options" icon="building" href="https://crewai.com/enterprise">
    Learn about CrewAI's enterprise offerings and schedule a demo
  </Card>
</Note>

<CardGroup>
  <Card title="Build Your First Agent" icon="code" href="/en/quickstart">
    Follow our quickstart guide to create your first CrewAI agent and get hands-on experience.
  </Card>

<Card title="Join the Community" icon="comments" href="https://community.crewai.com">
    Connect with other developers, get help, and share your CrewAI experiences.
  </Card>
</CardGroup>

**Examples:**

Example 1 (unknown):
```unknown
* This creates a new project with the following structure:
```

Example 2 (unknown):
```unknown
</Step>

  <Step title="Customize Your Project">
    * Your project will contain these essential files:
      | File          | Purpose                                  |
      | ------------- | ---------------------------------------- |
      | `agents.yaml` | Define your AI agents and their roles    |
      | `tasks.yaml`  | Set up agent tasks and workflows         |
      | `.env`        | Store API keys and environment variables |
      | `main.py`     | Project entry point and execution flow   |
      | `crew.py`     | Crew orchestration and coordination      |
      | `tools/`      | Directory for custom agent tools         |
      | `knowledge/`  | Directory for knowledge base             |

    * Start by editing `agents.yaml` and `tasks.yaml` to define your crew's behavior.

    * Keep sensitive information like API keys in `.env`.
  </Step>

  <Step title="Run your Crew">
    * Before you run your crew, make sure to run:
```

Example 3 (unknown):
```unknown
* If you need to install additional packages, use:
```

Example 4 (unknown):
```unknown
* To run your crew, execute the following command in the root of your project:
```

---

## crewai_agent.py

**URL:** llms-txt#crewai_agent.py

**Contents:**
  - Run the Application with Datadog Auto-Instrumentation
  - View the Traces in Datadog
- References

from crewai import Agent, Task, Crew

from crewai_tools import (
    WebsiteSearchTool
)

web_rag_tool = WebsiteSearchTool()

writer = Agent(
    role="Writer",
    goal="You make math engaging and understandable for young children through poetry",
    backstory="You're an expert in writing haikus but you know nothing of math.",
    tools=[web_rag_tool],
)

task = Task(
    description=("What is {multiplication}?"),
    expected_output=("Compose a haiku that includes the answer."),
    agent=writer
)

crew = Crew(
    agents=[writer],
    tasks=[task],
    share_crew=False
)

output = crew.kickoff(dict(multiplication="2 * 2"))
shell theme={null}
ddtrace-run python crewai_agent.py
```

### View the Traces in Datadog

After running the application, you can view the traces in [Datadog LLM Observability's Traces View](https://app.datadoghq.com/llm/traces), selecting the ML Application name you chose from the top-left dropdown.

Clicking on a trace will show you the details of the trace, including total tokens used, number of LLM calls, models used, and estimated cost. Clicking into a specific span will narrow down these details, and show related input, output, and metadata.

<Frame>
  <img alt="Datadog LLM Observability Trace View" />
</Frame>

Additionally, you can view the execution graph view of the trace, which shows the control and data flow of the trace, which will scale with larger agents to show handoffs and relationships between LLM calls, tool calls, and agent interactions.

<Frame>
  <img alt="Datadog LLM Observability Agent Execution Flow View" />
</Frame>

* [Datadog LLM Observability](https://www.datadoghq.com/product/llm-observability/)
* [Datadog LLM Observability CrewAI Auto-Instrumentation](https://docs.datadoghq.com/llm_observability/instrumentation/auto_instrumentation?tab=python#crew-ai)

**Examples:**

Example 1 (unknown):
```unknown
### Run the Application with Datadog Auto-Instrumentation

With the [environment variables](#set-environment-variables) set, you can now run the application with Datadog auto-instrumentation.
```

---

## CrewAI AOP

**URL:** llms-txt#crewai-aop

**Contents:**
- Introduction
- Key Features
- Deployment Options
- Getting Started

Source: https://docs.crewai.com/en/enterprise/introduction

Deploy, monitor, and scale your AI agent workflows

CrewAI AOP(Agent Operations Platform) provides a platform for deploying, monitoring, and scaling your crews and agents in a production environment.

<Frame>
  <img alt="CrewAI AOP Dashboard" />
</Frame>

CrewAI AOP extends the power of the open-source framework with features designed for production deployments, collaboration, and scalability. Deploy your crews to a managed infrastructure and monitor their execution in real-time.

<CardGroup>
  <Card title="Crew Deployments" icon="rocket">
    Deploy your crews to a managed infrastructure with a few clicks
  </Card>

<Card title="API Access" icon="code">
    Access your deployed crews via REST API for integration with existing systems
  </Card>

<Card title="Observability" icon="chart-line">
    Monitor your crews with detailed execution traces and logs
  </Card>

<Card title="Tool Repository" icon="toolbox">
    Publish and install tools to enhance your crews' capabilities
  </Card>

<Card title="Webhook Streaming" icon="webhook">
    Stream real-time events and updates to your systems
  </Card>

<Card title="Crew Studio" icon="paintbrush">
    Create and customize crews using a no-code/low-code interface
  </Card>
</CardGroup>

## Deployment Options

<CardGroup>
  <Card title="GitHub Integration" icon="github">
    Connect directly to your GitHub repositories to deploy code
  </Card>

<Card title="Crew Studio" icon="palette">
    Deploy crews created through the no-code Crew Studio interface
  </Card>

<Card title="CLI Deployment" icon="terminal">
    Use the CrewAI CLI for more advanced deployment workflows
  </Card>
</CardGroup>

<Steps>
  <Step title="Sign up for an account">
    Create your account at [app.crewai.com](https://app.crewai.com)

<Card title="Sign Up" icon="user" href="https://app.crewai.com/signup">
      Sign Up
    </Card>
  </Step>

<Step title="Build your first crew">
    Use code or Crew Studio to build your crew

<Card title="Build Crew" icon="paintbrush" href="/en/enterprise/guides/build-crew">
      Build Crew
    </Card>
  </Step>

<Step title="Deploy your crew">
    Deploy your crew to the Enterprise platform

<Card title="Deploy Crew" icon="rocket" href="/en/enterprise/guides/deploy-crew">
      Deploy Crew
    </Card>
  </Step>

<Step title="Access your crew">
    Integrate with your crew via the generated API endpoints

<Card title="API Access" icon="code" href="/en/enterprise/guides/kickoff-crew">
      Use the Crew API
    </Card>
  </Step>
</Steps>

For detailed instructions, check out our [deployment guide](/en/enterprise/guides/deploy-crew) or click the button below to get started.

---

## CrewAI Built-in Tracing

**URL:** llms-txt#crewai-built-in-tracing

**Contents:**
- Prerequisites
- Setup Instructions
  - Step 1: Create Your CrewAI AOP Account
  - Step 2: Install CrewAI CLI and Authenticate
  - Step 3: Enable Tracing in Your Crew

CrewAI provides built-in tracing capabilities that allow you to monitor and debug your Crews and Flows in real-time. This guide demonstrates how to enable tracing for both **Crews** and **Flows** using CrewAI's integrated observability platform.

> **What is CrewAI Tracing?** CrewAI's built-in tracing provides comprehensive observability for your AI agents, including agent decisions, task execution timelines, tool usage, and LLM calls - all accessible through the [CrewAI AOP platform](https://app.crewai.com).

<img alt="CrewAI Tracing Interface" />

Before you can use CrewAI tracing, you need:

1. **CrewAI AOP Account**: Sign up for a free account at [app.crewai.com](https://app.crewai.com)
2. **CLI Authentication**: Use the CrewAI CLI to authenticate your local environment

## Setup Instructions

### Step 1: Create Your CrewAI AOP Account

Visit [app.crewai.com](https://app.crewai.com) and create your free account. This will give you access to the CrewAI AOP platform where you can view traces, metrics, and manage your crews.

### Step 2: Install CrewAI CLI and Authenticate

If you haven't already, install CrewAI with the CLI tools:

Then authenticate your CLI with your CrewAI AOP account:

1. Open your browser to the authentication page
2. Prompt you to enter a device code
3. Authenticate your local environment with your CrewAI AOP account
4. Enable tracing capabilities for your local development

### Step 3: Enable Tracing in Your Crew

You can enable tracing for your Crew by setting the `tracing` parameter to `True`:

```python theme={null}
from crewai import Agent, Crew, Process, Task
from crewai_tools import SerperDevTool

**Examples:**

Example 1 (unknown):
```unknown
## Setup Instructions

### Step 1: Create Your CrewAI AOP Account

Visit [app.crewai.com](https://app.crewai.com) and create your free account. This will give you access to the CrewAI AOP platform where you can view traces, metrics, and manage your crews.

### Step 2: Install CrewAI CLI and Authenticate

If you haven't already, install CrewAI with the CLI tools:
```

Example 2 (unknown):
```unknown
Then authenticate your CLI with your CrewAI AOP account:
```

Example 3 (unknown):
```unknown
This command will:

1. Open your browser to the authentication page
2. Prompt you to enter a device code
3. Authenticate your local environment with your CrewAI AOP account
4. Enable tracing capabilities for your local development

### Step 3: Enable Tracing in Your Crew

You can enable tracing for your Crew by setting the `tracing` parameter to `True`:
```

---

## CrewAI Cookbooks

**URL:** llms-txt#crewai-cookbooks

**Contents:**
- Quickstarts & Demos

Source: https://docs.crewai.com/en/examples/cookbooks

Feature-focused quickstarts and notebooks for learning patterns fast.

## Quickstarts & Demos

<CardGroup>
  <Card title="Collaboration" icon="people-arrows" href="https://github.com/crewAIInc/crewAI-quickstarts/blob/main/Collaboration/crewai_collaboration.ipynb">
    Coordinate multiple agents on shared tasks. Includes notebook with end-to-end collaboration pattern.
  </Card>

<Card title="Planning" icon="timeline" href="https://github.com/crewAIInc/crewAI-quickstarts/blob/main/Planning/crewai_planning.ipynb">
    Teach agents to reason about multi-step plans before execution using the planning toolkit.
  </Card>

<Card title="Reasoning" icon="lightbulb" href="https://github.com/crewAIInc/crewAI-quickstarts/blob/main/Reasoning/crewai_reasoning.ipynb">
    Explore self-reflection loops, critique prompts, and structured thinking patterns.
  </Card>
</CardGroup>

<CardGroup>
  <Card title="Structured Guardrails" icon="shield-check" href="https://github.com/crewAIInc/crewAI-quickstarts/blob/main/Guardrails/task_guardrails.ipynb">
    Apply task-level guardrails with retries, validation functions, and safe fallbacks.
  </Card>

<Card title="Gemini Search & Grounding" icon="magnifying-glass" href="https://github.com/crewAIInc/crewAI-quickstarts/blob/main/Custom%20LLM/gemini_search_grounding_crewai.ipynb">
    Connect CrewAI to Gemini with search grounding for factual, citation-rich outputs.
  </Card>

<Card title="Gemini Video Summaries" icon="video" href="https://github.com/crewAIInc/crewAI-quickstarts/blob/main/Custom%20LLM/summarize_video_gemini_crewai.ipynb">
    Generate video recaps using Gemini multimodal LLM and CrewAI orchestration.
  </Card>
</CardGroup>

<CardGroup>
  <Card title="Browse Quickstarts" icon="bolt" href="https://github.com/crewAIInc/crewAI-quickstarts">
    View all notebooks and feature demos showcasing specific CrewAI capabilities.
  </Card>

<Card title="Request a cookbook" icon="message-plus" href="https://community.crewai.com">
    Missing a pattern? Drop a request in the community forum and we’ll expand the library.
  </Card>
</CardGroup>

<Tip>
  Use Cookbooks to learn a pattern quickly, then jump to Full Examples for production‑grade implementations.
</Tip>

---

## crewai reset-memories --agent-knowledge  # Agent knowledge only

**URL:** llms-txt#crewai-reset-memories---agent-knowledge--#-agent-knowledge-only

---

## crewai reset-memories --knowledge        # All knowledge

**URL:** llms-txt#crewai-reset-memories---knowledge--------#-all-knowledge

**Contents:**
  - Clearing Knowledge
- Best Practices

bash Command theme={null}
crewai reset-memories --knowledge
```

This is useful when you've updated your knowledge sources and want to ensure that the agents are using the most recent information.

<AccordionGroup>
  <Accordion title="Content Organization">
    * Keep chunk sizes appropriate for your content type
    * Consider content overlap for context preservation
    * Organize related information into separate knowledge sources
  </Accordion>

<Accordion title="Performance Tips">
    * Adjust chunk sizes based on content complexity
    * Configure appropriate embedding models
    * Consider using local embedding providers for faster processing
  </Accordion>

<Accordion title="One Time Knowledge">
    * With the typical file structure provided by CrewAI, knowledge sources are embedded every time the kickoff is triggered.
    * If the knowledge sources are large, this leads to inefficiency and increased latency, as the same data is embedded each time.
    * To resolve this, directly initialize the knowledge parameter instead of the knowledge\_sources parameter.
    * Link to the issue to get complete idea [Github Issue](https://github.com/crewAIInc/crewAI/issues/2755)
  </Accordion>

<Accordion title="Knowledge Management">
    * Use agent-level knowledge for role-specific information
    * Use crew-level knowledge for shared information all agents need
    * Set embedders at agent level if you need different embedding strategies
    * Use consistent collection naming by keeping agent roles descriptive
    * Test knowledge initialization by checking agent.knowledge after kickoff
    * Monitor storage locations to understand where knowledge is stored
    * Reset knowledge appropriately using the correct command types
  </Accordion>

<Accordion title="Production Best Practices">
    * Set `CREWAI_STORAGE_DIR` to a known location in production
    * Choose explicit embedding providers to match your LLM setup and avoid API key conflicts
    * Monitor knowledge storage size as it grows with document additions
    * Organize knowledge sources by domain or purpose using collection names
    * Include knowledge directories in your backup and deployment strategies
    * Set appropriate file permissions for knowledge files and storage directories
    * Use environment variables for API keys and sensitive configuration
  </Accordion>
</AccordionGroup>

**Examples:**

Example 1 (unknown):
```unknown
### Clearing Knowledge

If you need to clear the knowledge stored in CrewAI, you can use the `crewai reset-memories` command with the `--knowledge` option.
```

---

## CrewAI Run Automation Tool

**URL:** llms-txt#crewai-run-automation-tool

Source: https://docs.crewai.com/en/tools/integration/crewaiautomationtool

Enables CrewAI agents to invoke CrewAI Platform automations and leverage external crew services within your workflows.

---

## Crews

**URL:** llms-txt#crews

**Contents:**
- Overview
- Crew Attributes
- Creating Crews
  - YAML Configuration (Recommended)
  - Direct Code Definition (Alternative)
- Crew Output
  - Crew Output Attributes
  - Crew Output Methods and Properties
  - Accessing Crew Outputs

Source: https://docs.crewai.com/en/concepts/crews

Understanding and utilizing crews in the crewAI framework with comprehensive attributes and functionalities.

A crew in crewAI represents a collaborative group of agents working together to achieve a set of tasks. Each crew defines the strategy for task execution, agent collaboration, and the overall workflow.

| Attribute                             | Parameters             | Description                                                                                                                                                                                           |   |
| :------------------------------------ | :--------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | - |
| **Tasks**                             | `tasks`                | A list of tasks assigned to the crew.                                                                                                                                                                 |   |
| **Agents**                            | `agents`               | A list of agents that are part of the crew.                                                                                                                                                           |   |
| **Process** *(optional)*              | `process`              | The process flow (e.g., sequential, hierarchical) the crew follows. Default is `sequential`.                                                                                                          |   |
| **Verbose** *(optional)*              | `verbose`              | The verbosity level for logging during execution. Defaults to `False`.                                                                                                                                |   |
| **Manager LLM** *(optional)*          | `manager_llm`          | The language model used by the manager agent in a hierarchical process. **Required when using a hierarchical process.**                                                                               |   |
| **Function Calling LLM** *(optional)* | `function_calling_llm` | If passed, the crew will use this LLM to do function calling for tools for all agents in the crew. Each agent can have its own LLM, which overrides the crew's LLM for function calling.              |   |
| **Config** *(optional)*               | `config`               | Optional configuration settings for the crew, in `Json` or `Dict[str, Any]` format.                                                                                                                   |   |
| **Max RPM** *(optional)*              | `max_rpm`              | Maximum requests per minute the crew adheres to during execution. Defaults to `None`.                                                                                                                 |   |
| **Memory** *(optional)*               | `memory`               | Utilized for storing execution memories (short-term, long-term, entity memory).                                                                                                                       |   |
| **Cache** *(optional)*                | `cache`                | Specifies whether to use a cache for storing the results of tools' execution. Defaults to `True`.                                                                                                     |   |
| **Embedder** *(optional)*             | `embedder`             | Configuration for the embedder to be used by the crew. Mostly used by memory for now. Default is `{"provider": "openai"}`.                                                                            |   |
| **Step Callback** *(optional)*        | `step_callback`        | A function that is called after each step of every agent. This can be used to log the agent's actions or to perform other operations; it won't override the agent-specific `step_callback`.           |   |
| **Task Callback** *(optional)*        | `task_callback`        | A function that is called after the completion of each task. Useful for monitoring or additional operations post-task execution.                                                                      |   |
| **Share Crew** *(optional)*           | `share_crew`           | Whether you want to share the complete crew information and execution with the crewAI team to make the library better, and allow us to train models.                                                  |   |
| **Output Log File** *(optional)*      | `output_log_file`      | Set to True to save logs as logs.txt in the current directory or provide a file path. Logs will be in JSON format if the filename ends in .json, otherwise .txt. Defaults to `None`.                  |   |
| **Manager Agent** *(optional)*        | `manager_agent`        | `manager` sets a custom agent that will be used as a manager.                                                                                                                                         |   |
| **Prompt File** *(optional)*          | `prompt_file`          | Path to the prompt JSON file to be used for the crew.                                                                                                                                                 |   |
| **Planning** *(optional)*             | `planning`             | Adds planning ability to the Crew. When activated before each Crew iteration, all Crew data is sent to an AgentPlanner that will plan the tasks and this plan will be added to each task description. |   |
| **Planning LLM** *(optional)*         | `planning_llm`         | The language model used by the AgentPlanner in a planning process.                                                                                                                                    |   |
| **Knowledge Sources** *(optional)*    | `knowledge_sources`    | Knowledge sources available at the crew level, accessible to all the agents.                                                                                                                          |   |
| **Stream** *(optional)*               | `stream`               | Enable streaming output to receive real-time updates during crew execution. Returns a `CrewStreamingOutput` object that can be iterated for chunks. Defaults to `False`.                              |   |

<Tip>
  **Crew Max RPM**: The `max_rpm` attribute sets the maximum number of requests per minute the crew can perform to avoid rate limits and will override individual agents' `max_rpm` settings if you set it.
</Tip>

There are two ways to create crews in CrewAI: using **YAML configuration (recommended)** or defining them **directly in code**.

### YAML Configuration (Recommended)

Using YAML configuration provides a cleaner, more maintainable way to define crews and is consistent with how agents and tasks are defined in CrewAI projects.

After creating your CrewAI project as outlined in the [Installation](/en/installation) section, you can define your crew in a class that inherits from `CrewBase` and uses decorators to define agents, tasks, and the crew itself.

#### Example Crew Class with Decorators

How to run the above code:

<Note>
  Tasks will be executed in the order they are defined.
</Note>

The `CrewBase` class, along with these decorators, automates the collection of agents and tasks, reducing the need for manual management.

#### Decorators overview from `annotations.py`

CrewAI provides several decorators in the `annotations.py` file that are used to mark methods within your crew class for special handling:

* `@CrewBase`: Marks the class as a crew base class.
* `@agent`: Denotes a method that returns an `Agent` object.
* `@task`: Denotes a method that returns a `Task` object.
* `@crew`: Denotes the method that returns the `Crew` object.
* `@before_kickoff`: (Optional) Marks a method to be executed before the crew starts.
* `@after_kickoff`: (Optional) Marks a method to be executed after the crew finishes.

These decorators help in organizing your crew's structure and automatically collecting agents and tasks without manually listing them.

### Direct Code Definition (Alternative)

Alternatively, you can define the crew directly in code without using YAML configuration files.

How to run the above code:

* Agents and tasks are defined directly within the class without decorators.
* We manually create and manage the list of agents and tasks.
* This approach provides more control but can be less maintainable for larger projects.

The output of a crew in the CrewAI framework is encapsulated within the `CrewOutput` class.
This class provides a structured way to access results of the crew's execution, including various formats such as raw strings, JSON, and Pydantic models.
The `CrewOutput` includes the results from the final task output, token usage, and individual task outputs.

### Crew Output Attributes

| Attribute        | Parameters     | Type                       | Description                                                                                          |
| :--------------- | :------------- | :------------------------- | :--------------------------------------------------------------------------------------------------- |
| **Raw**          | `raw`          | `str`                      | The raw output of the crew. This is the default format for the output.                               |
| **Pydantic**     | `pydantic`     | `Optional[BaseModel]`      | A Pydantic model object representing the structured output of the crew.                              |
| **JSON Dict**    | `json_dict`    | `Optional[Dict[str, Any]]` | A dictionary representing the JSON output of the crew.                                               |
| **Tasks Output** | `tasks_output` | `List[TaskOutput]`         | A list of `TaskOutput` objects, each representing the output of a task in the crew.                  |
| **Token Usage**  | `token_usage`  | `Dict[str, Any]`           | A summary of token usage, providing insights into the language model's performance during execution. |

### Crew Output Methods and Properties

| Method/Property | Description                                                                                       |
| :-------------- | :------------------------------------------------------------------------------------------------ |
| **json**        | Returns the JSON string representation of the crew output if the output format is JSON.           |
| **to\_dict**    | Converts the JSON and Pydantic outputs to a dictionary.                                           |
| \***\*str\*\*** | Returns the string representation of the crew output, prioritizing Pydantic, then JSON, then raw. |

### Accessing Crew Outputs

Once a crew has been executed, its output can be accessed through the `output` attribute of the `Crew` object. The `CrewOutput` class provides various ways to interact with and present this output.

```python Code theme={null}

**Examples:**

Example 1 (unknown):
```unknown
How to run the above code:
```

Example 2 (unknown):
```unknown
<Note>
  Tasks will be executed in the order they are defined.
</Note>

The `CrewBase` class, along with these decorators, automates the collection of agents and tasks, reducing the need for manual management.

#### Decorators overview from `annotations.py`

CrewAI provides several decorators in the `annotations.py` file that are used to mark methods within your crew class for special handling:

* `@CrewBase`: Marks the class as a crew base class.
* `@agent`: Denotes a method that returns an `Agent` object.
* `@task`: Denotes a method that returns a `Task` object.
* `@crew`: Denotes the method that returns the `Crew` object.
* `@before_kickoff`: (Optional) Marks a method to be executed before the crew starts.
* `@after_kickoff`: (Optional) Marks a method to be executed after the crew finishes.

These decorators help in organizing your crew's structure and automatically collecting agents and tasks without manually listing them.

### Direct Code Definition (Alternative)

Alternatively, you can define the crew directly in code without using YAML configuration files.
```

Example 3 (unknown):
```unknown
How to run the above code:
```

Example 4 (unknown):
```unknown
In this example:

* Agents and tasks are defined directly within the class without decorators.
* We manually create and manage the list of agents and tasks.
* This approach provides more control but can be less maintainable for larger projects.

## Crew Output

The output of a crew in the CrewAI framework is encapsulated within the `CrewOutput` class.
This class provides a structured way to access results of the crew's execution, including various formats such as raw strings, JSON, and Pydantic models.
The `CrewOutput` includes the results from the final task output, token usage, and individual task outputs.

### Crew Output Attributes

| Attribute        | Parameters     | Type                       | Description                                                                                          |
| :--------------- | :------------- | :------------------------- | :--------------------------------------------------------------------------------------------------- |
| **Raw**          | `raw`          | `str`                      | The raw output of the crew. This is the default format for the output.                               |
| **Pydantic**     | `pydantic`     | `Optional[BaseModel]`      | A Pydantic model object representing the structured output of the crew.                              |
| **JSON Dict**    | `json_dict`    | `Optional[Dict[str, Any]]` | A dictionary representing the JSON output of the crew.                                               |
| **Tasks Output** | `tasks_output` | `List[TaskOutput]`         | A list of `TaskOutput` objects, each representing the output of a task in the crew.                  |
| **Token Usage**  | `token_usage`  | `Dict[str, Any]`           | A summary of token usage, providing insights into the language model's performance during execution. |

### Crew Output Methods and Properties

| Method/Property | Description                                                                                       |
| :-------------- | :------------------------------------------------------------------------------------------------ |
| **json**        | Returns the JSON string representation of the crew output if the output format is JSON.           |
| **to\_dict**    | Converts the JSON and Pydantic outputs to a dictionary.                                           |
| \***\*str\*\*** | Returns the string representation of the crew output, prioritizing Pydantic, then JSON, then raw. |

### Accessing Crew Outputs

Once a crew has been executed, its output can be accessed through the `output` attribute of the `Crew` object. The `CrewOutput` class provides various ways to interact with and present this output.

#### Example
```

---

## Crew Studio

**URL:** llms-txt#crew-studio

**Contents:**
- Overview
- Prompt‑based Creation
- Visual Editor
- Execution & Debugging
- Publish & Export
- Best Practices
- Related

Source: https://docs.crewai.com/en/enterprise/features/crew-studio

Build new automations with AI assistance, a visual editor, and integrated testing.

Crew Studio is an interactive, AI‑assisted workspace for creating new automations from scratch using natural language and a visual workflow editor.

<Frame>
  <img alt="Crew Studio Overview" />
</Frame>

## Prompt‑based Creation

* Describe the automation you want; the AI generates agents, tasks, and tools.
* Use voice input via the microphone icon if preferred.
* Start from built‑in prompts for common use cases.

<Frame>
  <img alt="Prompt Builder" />
</Frame>

The canvas reflects the workflow as nodes and edges with three supporting panels that allow you to configure the workflow easily without writing code; a.k.a. "**vibe coding AI Agents**".

You can use the drag-and-drop functionality to add agents, tasks, and tools to the canvas or you can use the chat section to build the agents. Both approaches share state and can be used interchangeably.

* **AI Thoughts (left)**: streaming reasoning as the workflow is designed
* **Canvas (center)**: agents and tasks as connected nodes
* **Resources (right)**: drag‑and‑drop components (agents, tasks, tools)

<Frame>
  <img alt="Visual Canvas" />
</Frame>

## Execution & Debugging

Switch to the <b>Execution</b> view to run and observe the workflow:

* Event timeline
* Detailed logs (Details, Messages, Raw Data)
* Local test runs before publishing

<Frame>
  <img alt="Execution View" />
</Frame>

* <b>Publish</b> to deploy a live automation
* <b>Download</b> source as a ZIP for local development or customization

<Frame>
  <img alt="Publish & Download" />
</Frame>

Once published, you can view the automation details and have the **Options** dropdown menu to `chat with this crew`, `Export React Component` and `Export as MCP`.

<Frame>
  <img alt="Published Automation" />
</Frame>

* Iterate quickly in Studio; publish only when stable
* Keep tools constrained to minimum permissions needed
* Use Traces to validate behavior and performance

<CardGroup>
  <Card title="Enable Crew Studio" href="/en/enterprise/guides/enable-crew-studio" icon="palette">
    Enable Crew Studio.
  </Card>

<Card title="Build a Crew" href="/en/enterprise/guides/build-crew" icon="paintbrush">
    Build a Crew.
  </Card>

<Card title="Deploy a Crew" href="/en/enterprise/guides/deploy-crew" icon="rocket">
    Deploy a Crew from GitHub or ZIP file.
  </Card>

<Card title="Export a React Component" href="/en/enterprise/guides/react-component-export" icon="download">
    Export a React Component.
  </Card>
</CardGroup>

---

## Crew-wide knowledge (shared by all agents)

**URL:** llms-txt#crew-wide-knowledge-(shared-by-all-agents)

crew_knowledge = StringKnowledgeSource(
    content="Company policies and general information for all agents"
)

---

## Customize Agents

**URL:** llms-txt#customize-agents

**Contents:**
- Customizable Attributes
  - Key Attributes for Customization
- Advanced Customization Options
  - Language Model Customization
- Performance and Debugging Settings
  - Verbose Mode and RPM Limit
  - Maximum Iterations for Task Execution
- Customizing Agents and Tools
  - Example: Assigning Tools to an Agent

Source: https://docs.crewai.com/en/learn/customizing-agents

A comprehensive guide to tailoring agents for specific roles, tasks, and advanced customizations within the CrewAI framework.

## Customizable Attributes

Crafting an efficient CrewAI team hinges on the ability to dynamically tailor your AI agents to meet the unique requirements of any project. This section covers the foundational attributes you can customize.

### Key Attributes for Customization

| Attribute                           | Description                                                                                                         |
| :---------------------------------- | :------------------------------------------------------------------------------------------------------------------ |
| **Role**                            | Specifies the agent's job within the crew, such as 'Analyst' or 'Customer Service Rep'.                             |
| **Goal**                            | Defines the agent’s objectives, aligned with its role and the crew’s overarching mission.                           |
| **Backstory**                       | Provides depth to the agent's persona, enhancing motivations and engagements within the crew.                       |
| **Tools** *(Optional)*              | Represents the capabilities or methods the agent uses for tasks, from simple functions to complex integrations.     |
| **Cache** *(Optional)*              | Determines if the agent should use a cache for tool usage.                                                          |
| **Max RPM**                         | Sets the maximum requests per minute (`max_rpm`). Can be set to `None` for unlimited requests to external services. |
| **Verbose** *(Optional)*            | Enables detailed logging for debugging and optimization, providing insights into execution processes.               |
| **Allow Delegation** *(Optional)*   | Controls task delegation to other agents, default is `False`.                                                       |
| **Max Iter** *(Optional)*           | Limits the maximum number of iterations (`max_iter`) for a task to prevent infinite loops, with a default of 25.    |
| **Max Execution Time** *(Optional)* | Sets the maximum time allowed for an agent to complete a task.                                                      |
| **System Template** *(Optional)*    | Defines the system format for the agent.                                                                            |
| **Prompt Template** *(Optional)*    | Defines the prompt format for the agent.                                                                            |
| **Response Template** *(Optional)*  | Defines the response format for the agent.                                                                          |
| **Use System Prompt** *(Optional)*  | Controls whether the agent will use a system prompt during task execution.                                          |
| **Respect Context Window**          | Enables a sliding context window by default, maintaining context size.                                              |
| **Max Retry Limit**                 | Sets the maximum number of retries (`max_retry_limit`) for an agent in case of errors.                              |

## Advanced Customization Options

Beyond the basic attributes, CrewAI allows for deeper customization to enhance an agent's behavior and capabilities significantly.

### Language Model Customization

Agents can be customized with specific language models (`llm`) and function-calling language models (`function_calling_llm`), offering advanced control over their processing and decision-making abilities.
It's important to note that setting the `function_calling_llm` allows for overriding the default crew function-calling language model, providing a greater degree of customization.

## Performance and Debugging Settings

Adjusting an agent's performance and monitoring its operations are crucial for efficient task execution.

### Verbose Mode and RPM Limit

* **Verbose Mode**: Enables detailed logging of an agent's actions, useful for debugging and optimization. Specifically, it provides insights into agent execution processes, aiding in the optimization of performance.
* **RPM Limit**: Sets the maximum number of requests per minute (`max_rpm`). This attribute is optional and can be set to `None` for no limit, allowing for unlimited queries to external services if needed.

### Maximum Iterations for Task Execution

The `max_iter` attribute allows users to define the maximum number of iterations an agent can perform for a single task, preventing infinite loops or excessively long executions.
The default value is set to 25, providing a balance between thoroughness and efficiency. Once the agent approaches this number, it will try its best to give a good answer.

## Customizing Agents and Tools

Agents are customized by defining their attributes and tools during initialization. Tools are critical for an agent's functionality, enabling them to perform specialized tasks.
The `tools` attribute should be an array of tools the agent can utilize, and it's initialized as an empty list by default. Tools can be added or modified post-agent initialization to adapt to new requirements.

### Example: Assigning Tools to an Agent

```python Code theme={null}
import os
from crewai import Agent
from crewai_tools import SerperDevTool

**Examples:**

Example 1 (unknown):
```unknown
### Example: Assigning Tools to an Agent
```

---

## Custom Manager Agent

**URL:** llms-txt#custom-manager-agent

Source: https://docs.crewai.com/en/learn/custom-manager-agent

Learn how to set a custom agent as the manager in CrewAI, providing more control over task management and coordination.

---

## Define an agent that uses the tool

**URL:** llms-txt#define-an-agent-that-uses-the-tool

browser_agent = Agent(
    role="Browser Agent",
    goal="Control web browsers using natural language",
    backstory="An expert browsing agent.",
    tools=[multion_tool],
    verbose=True,
)

---

## Define an agent with the AIMindTool

**URL:** llms-txt#define-an-agent-with-the-aimindtool

**Contents:**
- Conclusion

@agent
def data_analyst(self) -> Agent:
    return Agent(
        config=self.agents_config["data_analyst"],
        allow_delegation=False,
        tools=[aimind_tool]
    )
```

The `AIMindTool` provides a powerful way to query your data sources using natural language, making it easier to extract insights without writing complex SQL queries. By connecting to various data sources and leveraging AI-Minds technology, this tool enables agents to access and analyze data efficiently.

---

## Define an agent with the BraveSearchTool

**URL:** llms-txt#define-an-agent-with-the-bravesearchtool

**Contents:**
- Conclusion

@agent
def researcher(self) -> Agent:
    return Agent(
        config=self.agents_config["researcher"],
        allow_delegation=False,
        tools=[brave_search_tool]
    )
```

By integrating the `BraveSearchTool` into Python projects, users gain the ability to conduct real-time, relevant searches across the internet directly from their applications. The tool provides a simple interface to the powerful Brave Search API, making it easy to retrieve and process search results programmatically. By adhering to the setup and usage guidelines provided, incorporating this tool into projects is streamlined and straightforward.

---

## Define an agent with the RagTool

**URL:** llms-txt#define-an-agent-with-the-ragtool

**Contents:**
- Advanced Configuration

@agent
def knowledge_expert(self) -> Agent:
    return Agent(
        config=self.agents_config["knowledge_expert"],
        allow_delegation=False,
        tools=[rag_tool]
    )
python Code theme={null}
from crewai_tools import RagTool
from crewai_tools.tools.rag import RagToolConfig, VectorDbConfig, ProviderSpec

**Examples:**

Example 1 (unknown):
```unknown
## Advanced Configuration

You can customize the behavior of the `RagTool` by providing a configuration dictionary:
```

---

## Define a custom manager agent

**URL:** llms-txt#define-a-custom-manager-agent

manager = Agent(
    role="Project Manager",
    goal="Efficiently manage the crew and ensure high-quality task completion",
    backstory="You're an experienced project manager, skilled in overseeing complex projects and guiding teams to success.",
    allow_delegation=True,
)

---

## Define a task for the agent

**URL:** llms-txt#define-a-task-for-the-agent

extract_task = Task(
    description='Extract the main content from the URL https://example.com using basic extraction depth.',
    expected_output='A JSON string containing the extracted content from the URL.',
    agent=extractor_agent
)

---

## Define the agents

**URL:** llms-txt#define-the-agents

data_fetcher_agent = Agent(
    role="Data Fetcher",
    goal="Fetch data online using Serper tool",
    backstory="Backstory 1",
    verbose=True,
    tools=[SerperDevTool()]
)

data_processor_agent = Agent(
    role="Data Processor",
    goal="Process fetched data",
    backstory="Backstory 2",
    verbose=True
)

summary_generator_agent = Agent(
    role="Summary Generator",
    goal="Generate summary from fetched data",
    backstory="Backstory 3",
    verbose=True
)

class EventOutput(BaseModel):
    events: List[str]

task1 = Task(
    description="Fetch data about events in San Francisco using Serper tool",
    expected_output="List of 10 things to do in SF this week",
    agent=data_fetcher_agent,
    output_pydantic=EventOutput,
)

conditional_task = ConditionalTask(
    description="""
        Check if data is missing. If we have less than 10 events,
        fetch more events using Serper tool so that
        we have a total of 10 events in SF this week..
        """,
    expected_output="List of 10 Things to do in SF this week",
    condition=is_data_missing,
    agent=data_processor_agent,
)

task3 = Task(
    description="Generate summary of events in San Francisco from fetched data",
    expected_output="A complete report on the customer and their customers and competitors, including their demographics, preferences, market positioning and audience engagement.",
    agent=summary_generator_agent,
)

---

## Define the agent

**URL:** llms-txt#define-the-agent

blog_agent = Agent(
    role="Blog Content Generator Agent",
    goal="Generate a blog title and content",
    backstory="""You are an expert content creator, skilled in crafting engaging and informative blog posts.""",
    verbose=False,
    allow_delegation=False,
    llm="gpt-4o",
)

---

## Define the manager agent

**URL:** llms-txt#define-the-manager-agent

manager = Agent(
    role="Project Manager",
    goal="Efficiently manage the crew and ensure high-quality task completion",
    backstory="You're an experienced project manager, skilled in overseeing complex projects and guiding teams to success. Your role is to coordinate the efforts of the crew members, ensuring that each task is completed on time and to the highest standard.",
    allow_delegation=True,
)

---

## Define your agents

**URL:** llms-txt#define-your-agents

researcher = Agent(
    role="Senior Research Analyst",
    goal="Uncover cutting-edge developments in AI and data science",
    backstory="""You work at a leading tech think tank.
    Your expertise lies in identifying emerging trends.
    You have a knack for dissecting complex data and presenting actionable insights.""",
    verbose=True,
    tools=[SerperDevTool()],
)

writer = Agent(
    role="Tech Content Strategist",
    goal="Craft compelling content on tech advancements",
    backstory="""You are a renowned Content Strategist, known for your insightful and engaging articles.
    You transform complex concepts into compelling narratives.""",
    verbose=True,
)

---

## Define your agents with roles and goals

**URL:** llms-txt#define-your-agents-with-roles-and-goals

researcher = Agent(
    role="Senior Research Analyst",
    goal="Uncover cutting-edge developments in AI and data science",
    backstory="""You work at a leading tech think tank.
    Your expertise lies in identifying emerging trends.
    You have a knack for dissecting complex data and presenting actionable insights.""",
    verbose=True,
    allow_delegation=False,
    # You can pass an optional llm attribute specifying what model you wanna use.
    # llm=ChatOpenAI(model_name="gpt-3.5", temperature=0.7),
    tools=[search_tool],
)
writer = Agent(
    role="Tech Content Strategist",
    goal="Craft compelling content on tech advancements",
    backstory="""You are a renowned Content Strategist, known for your insightful and engaging articles.
    You transform complex concepts into compelling narratives.""",
    verbose=True,
    allow_delegation=True,
)

---

## Define your agents with roles, goals, tools, and additional attributes

**URL:** llms-txt#define-your-agents-with-roles,-goals,-tools,-and-additional-attributes

researcher = Agent(
    role='Senior Research Analyst',
    goal='Uncover cutting-edge developments in AI and data science',
    backstory=(
        "You are a Senior Research Analyst at a leading tech think tank. "
        "Your expertise lies in identifying emerging trends and technologies in AI and data science. "
        "You have a knack for dissecting complex data and presenting actionable insights."
    ),
    verbose=True,
    allow_delegation=False,
    tools=[search_tool]
)
writer = Agent(
    role='Tech Content Strategist',
    goal='Craft compelling content on tech advancements',
    backstory=(
        "You are a renowned Tech Content Strategist, known for your insightful and engaging articles on technology and innovation. "
        "With a deep understanding of the tech industry, you transform complex concepts into compelling narratives."
    ),
    verbose=True,
    allow_delegation=True,
    tools=[search_tool],
    cache=False,  # Disable cache for this agent
)

---

## Define your agent

**URL:** llms-txt#define-your-agent

researcher = Agent(
    role="Research Specialist",
    goal="Research topics thoroughly",
    backstory="Expert researcher with skills in finding information",
    llm=create_llm("openai/gpt-4o"), # Replace with the model you want to use
    verbose=True
)

---

## Different knowledge for different agents

**URL:** llms-txt#different-knowledge-for-different-agents

sales_knowledge = StringKnowledgeSource(content="Sales procedures and pricing")
tech_knowledge = StringKnowledgeSource(content="Technical documentation")
support_knowledge = StringKnowledgeSource(content="Support procedures")

sales_agent = Agent(
    role="Sales Representative",
    knowledge_sources=[sales_knowledge],
    embedder={"provider": "openai", "config": {"model": "text-embedding-3-small"}}
)

tech_agent = Agent(
    role="Technical Expert", 
    knowledge_sources=[tech_knowledge],
    embedder={"provider": "ollama", "config": {"model": "mxbai-embed-large"}}
)

support_agent = Agent(
    role="Support Specialist",
    knowledge_sources=[support_knowledge]
    # Will use crew embedder as fallback
)

crew = Crew(
    agents=[sales_agent, tech_agent, support_agent],
    tasks=[...],
    embedder={  # Fallback embedder for agents without their own
        "provider": "google-generativeai",
        "config": {"model_name": "gemini-embedding-001"}
    }
)

---

## During kickoff

**URL:** llms-txt#during-kickoff

for agent in self.agents:
    agent.crew = self  # Agent gets reference to crew
    agent.set_knowledge(crew_embedder=self.embedder)  # Agent knowledge initialized
    agent.create_agent_executor()
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
#### Storage Independence

Each knowledge level uses independent storage collections:
```

---

## Each agent gets only their specific knowledge

**URL:** llms-txt#each-agent-gets-only-their-specific-knowledge

---

## Editor Agent

**URL:** llms-txt#editor-agent

**Contents:**
  - Creating Specialized Tool Users
  - Tailoring Agents to LLM Capabilities

role: "Content Quality Editor"
goal: "Ensure content is accurate, well-structured, and polished while maintaining consistency"
backstory: "With years of experience in publishing, you have a keen eye for detail..."
yaml theme={null}
role: "Data Analysis Specialist"
goal: "Derive meaningful insights from complex datasets through statistical analysis"
backstory: "With a background in data science, you excel at working with structured and unstructured data..."
tools: [PythonREPLTool, DataVisualizationTool, CSVAnalysisTool]
yaml theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### Creating Specialized Tool Users

Some agents can be designed specifically to leverage certain tools effectively:
```

Example 2 (unknown):
```unknown
### Tailoring Agents to LLM Capabilities

Different LLMs have different strengths. Design your agents with these capabilities in mind:
```

---

## Enable basic memory system

**URL:** llms-txt#enable-basic-memory-system

**Contents:**
  - How It Works
- Storage Location Transparency
  - Where CrewAI Stores Files
  - Finding Your Storage Location

crew = Crew(
    agents=[...],
    tasks=[...],
    process=Process.sequential,
    memory=True,  # Enables short-term, long-term, and entity memory
    verbose=True
)

~/Library/Application Support/CrewAI/{project_name}/
├── knowledge/           # Knowledge base ChromaDB files
├── short_term_memory/   # Short-term memory ChromaDB files
├── long_term_memory/    # Long-term memory ChromaDB files
├── entities/            # Entity memory ChromaDB files
└── long_term_memory_storage.db  # SQLite database

~/.local/share/CrewAI/{project_name}/
├── knowledge/
├── short_term_memory/
├── long_term_memory/
├── entities/
└── long_term_memory_storage.db

C:\Users\{username}\AppData\Local\CrewAI\{project_name}\
├── knowledge\
├── short_term_memory\
├── long_term_memory\
├── entities\
└── long_term_memory_storage.db
python theme={null}
from crewai.utilities.paths import db_storage_path
import os

**Examples:**

Example 1 (unknown):
```unknown
### How It Works

* **Short-Term Memory**: Uses ChromaDB with RAG for current context
* **Long-Term Memory**: Uses SQLite3 to store task results across sessions
* **Entity Memory**: Uses RAG to track entities (people, places, concepts)
* **Storage Location**: Platform-specific location via `appdirs` package
* **Custom Storage Directory**: Set `CREWAI_STORAGE_DIR` environment variable

## Storage Location Transparency

<Info>
  **Understanding Storage Locations**: CrewAI uses platform-specific directories to store memory and knowledge files following OS conventions. Understanding these locations helps with production deployments, backups, and debugging.
</Info>

### Where CrewAI Stores Files

By default, CrewAI uses the `appdirs` library to determine storage locations following platform conventions. Here's exactly where your files are stored:

#### Default Storage Locations by Platform

**macOS:**
```

Example 2 (unknown):
```unknown
**Linux:**
```

Example 3 (unknown):
```unknown
**Windows:**
```

Example 4 (unknown):
```unknown
### Finding Your Storage Location

To see exactly where CrewAI is storing files on your system:
```

---

## Enable collaboration for agents

**URL:** llms-txt#enable-collaboration-for-agents

researcher = Agent(
    role="Research Specialist",
    goal="Conduct thorough research on any topic",
    backstory="Expert researcher with access to various sources",
    allow_delegation=True,  # 🔑 Key setting for collaboration
    verbose=True
)

writer = Agent(
    role="Content Writer", 
    goal="Create engaging content based on research",
    backstory="Skilled writer who transforms research into compelling content",
    allow_delegation=True,  # 🔑 Enables asking questions to other agents
    verbose=True
)

---

## Enable streaming

**URL:** llms-txt#enable-streaming

crew = Crew(
    agents=[researcher],
    tasks=[task],
    stream=True
)

---

## Enable tracing in your crew

**URL:** llms-txt#enable-tracing-in-your-crew

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
    tracing=True,  # Enable built-in tracing
    verbose=True
)

---

## Ensure to provide a manager_llm or manager_agent

**URL:** llms-txt#ensure-to-provide-a-manager_llm-or-manager_agent

**Contents:**
- Sequential Process
- Hierarchical Process
- Process Class: Detailed Overview
- Conclusion

crew = Crew(
    agents=my_agents,
    tasks=my_tasks,
    process=Process.hierarchical,
    manager_llm="gpt-4o"
    # or
    # manager_agent=my_manager_agent
)
```

**Note:** Ensure `my_agents` and `my_tasks` are defined prior to creating a `Crew` object, and for the hierarchical process, either `manager_llm` or `manager_agent` is also required.

## Sequential Process

This method mirrors dynamic team workflows, progressing through tasks in a thoughtful and systematic manner. Task execution follows the predefined order in the task list, with the output of one task serving as context for the next.

To customize task context, utilize the `context` parameter in the `Task` class to specify outputs that should be used as context for subsequent tasks.

## Hierarchical Process

Emulates a corporate hierarchy, CrewAI allows specifying a custom manager agent or automatically creates one, requiring the specification of a manager language model (`manager_llm`). This agent oversees task execution, including planning, delegation, and validation. Tasks are not pre-assigned; the manager allocates tasks to agents based on their capabilities, reviews outputs, and assesses task completion.

## Process Class: Detailed Overview

The `Process` class is implemented as an enumeration (`Enum`), ensuring type safety and restricting process values to the defined types (`sequential`, `hierarchical`). The consensual process is planned for future inclusion, emphasizing our commitment to continuous development and innovation.

The structured collaboration facilitated by processes within CrewAI is crucial for enabling systematic teamwork among agents.
This documentation has been updated to reflect the latest features, enhancements, and the planned integration of the Consensual Process, ensuring users have access to the most current and comprehensive information.

---

## Establishing the crew with a hierarchical process and additional configurations

**URL:** llms-txt#establishing-the-crew-with-a-hierarchical-process-and-additional-configurations

**Contents:**
  - Using a Custom Manager Agent

project_crew = Crew(
    tasks=[...],  # Tasks to be delegated and executed under the manager's supervision
    agents=[researcher, writer],
    manager_llm="gpt-4o",  # Specify which LLM the manager should use
    process=Process.hierarchical,  
    planning=True, 
)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### Using a Custom Manager Agent

Alternatively, you can create a custom manager agent with specific attributes tailored to your project's management needs. This gives you more control over the manager's behavior and capabilities.
```

---

## Example: Creating a crew with a sequential process

**URL:** llms-txt#example:-creating-a-crew-with-a-sequential-process

crew = Crew(
    agents=my_agents,
    tasks=my_tasks,
    process=Process.sequential
)

---

## Example crew execution

**URL:** llms-txt#example-crew-execution

crew = Crew(
    agents=[research_agent, writer_agent],
    tasks=[research_task, write_article_task],
    verbose=True
)

crew_output = crew.kickoff()

---

## Example of initiating tool that agents can use

**URL:** llms-txt#example-of-initiating-tool-that-agents-can-use

---

## Example of using the tool with an agent

**URL:** llms-txt#example-of-using-the-tool-with-an-agent

browser_agent = Agent(
    role="Web Browser Agent",
    goal="Search for and summarize information from the web",
    backstory="An expert at finding and extracting information from websites.",
    tools=[multion_tool],
    verbose=True,
)

---

## Example operations (same API for any provider)

**URL:** llms-txt#example-operations-(same-api-for-any-provider)

**Contents:**
  - Basic String Knowledge Example

client = qdrant_client  # or chromadb_client
client.create_collection(collection_name="docs")
client.add_documents(
    collection_name="docs",
    documents=[{"id": "1", "content": "CrewAI enables collaborative AI agents."}],
)
results = client.search(collection_name="docs", query="collaborative agents", limit=3)

clear_rag_config()  # optional reset
python Code theme={null}
from crewai import Agent, Task, Crew, Process, LLM
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

**Examples:**

Example 1 (unknown):
```unknown
This RAG client is separate from Knowledge’s built-in storage. Use it when you need direct vector-store control or custom retrieval pipelines.

### Basic String Knowledge Example
```

---

## Example: Technical Documentation Agent

**URL:** llms-txt#example:-technical-documentation-agent

**Contents:**
- Practical Implementation Checklist
  - When to Use Different Model Types
- Common CrewAI Model Selection Pitfalls
- Testing and Iteration Strategy
  - Enterprise-Grade Model Validation
- Key Principles Summary
- Current Model Landscape (June 2025)
  - Leading Models by Category
  - Selection Framework for Current Models
  - Key Considerations for Model Selection

tech_writer = Agent(
    role="API Documentation Specialist",  # Specific role for clear LLM requirements
    goal="Create comprehensive, developer-friendly API documentation",
    backstory="""
    You're a technical writer with 8+ years documenting REST APIs, GraphQL endpoints,
    and SDK integration guides. You've worked with developer tools companies and
    understand what developers need: clear examples, comprehensive error handling,
    and practical use cases. You prioritize accuracy and usability over marketing fluff.
    """,
    llm=LLM(
        model="claude-3-5-sonnet",  # Excellent for technical writing
        temperature=0.1  # Low temperature for accuracy
    ),
    tools=[code_analyzer_tool, api_scanner_tool],
    verbose=True
)
python theme={null}
    # Start with a reliable default for the crew
    default_crew_llm = LLM(model="gpt-4o-mini")  # Cost-effective baseline

crew = Crew(
        agents=[...],
        tasks=[...],
        memory=True
    )
    python theme={null}
    # Manager or coordination agents
    manager_agent = Agent(
        role="Project Manager",
        llm=LLM(model="gemini-2.5-flash-preview-05-20"),  # Premium for coordination
        # ... rest of config
    )

# Creative or customer-facing agents
    content_agent = Agent(
        role="Content Creator",
        llm=LLM(model="claude-3-5-sonnet"),  # Best for writing
        # ... rest of config
    )
    python theme={null}
    # Strategic agent gets premium model
    manager = Agent(role="Strategy Manager", llm=LLM(model="gpt-4o"))

# Processing agent gets efficient model
    processor = Agent(role="Data Processor", llm=LLM(model="gpt-4o-mini"))
    python theme={null}
    crew = Crew(
        agents=[agent1, agent2],
        tasks=[task1, task2],
        manager_llm=LLM(model="gpt-4o"),  # For crew coordination
        process=Process.hierarchical  # When using manager_llm
    )

# Agents inherit crew LLM unless specifically overridden
    agent1 = Agent(llm=LLM(model="claude-3-5-sonnet"))  # Override for specific needs
    python theme={null}
    # For agents that use many tools
    tool_agent = Agent(
        role="API Integration Specialist",
        tools=[search_tool, api_tool, data_tool],
        llm=LLM(model="gpt-4o"),  # Excellent function calling
        # OR
        llm=LLM(model="claude-3-5-sonnet")  # Also strong with tools
    )
    python theme={null}
    # Start with this
    crew = Crew(agents=[...], tasks=[...], llm=LLM(model="gpt-4o-mini"))

# Test performance, then optimize specific agents as needed
    # Use Enterprise platform testing to validate improvements
    ```
  </Accordion>

<Accordion title="Overlooking Context and Memory Limitations" icon="brain">
    **The Problem**: Not considering how model context windows interact with CrewAI's memory and context sharing between agents.

**Real Example**: Using a short-context model for agents that need to maintain conversation history across multiple task iterations, or in crews with extensive agent-to-agent communication.

**CrewAI Solution**: Match context capabilities to crew communication patterns.
  </Accordion>
</AccordionGroup>

## Testing and Iteration Strategy

<Steps>
  <Step title="Start Simple" icon="play">
    Begin with reliable, general-purpose models that are well-understood and widely supported. This provides a stable foundation for understanding your specific requirements and performance expectations before optimizing for specialized needs.
  </Step>

<Step title="Measure What Matters" icon="chart-line">
    Develop metrics that align with your specific use case and business requirements rather than relying solely on general benchmarks. Focus on measuring outcomes that directly impact your success rather than theoretical performance indicators.
  </Step>

<Step title="Iterate Based on Results" icon="arrows-rotate">
    Make model changes based on observed performance in your specific context rather than theoretical considerations or general recommendations. Real-world performance often differs significantly from benchmark results or general reputation.
  </Step>

<Step title="Consider Total Cost" icon="calculator">
    Evaluate the complete cost of ownership including model costs, development time, maintenance overhead, and operational complexity. The cheapest model per token may not be the most cost-effective choice when considering all factors.
  </Step>
</Steps>

<Tip>
  Focus on understanding your requirements first, then select models that best match those needs. The best LLM choice is the one that consistently delivers the results you need within your operational constraints.
</Tip>

### Enterprise-Grade Model Validation

For teams serious about optimizing their LLM selection, the **CrewAI AOP platform** provides sophisticated testing capabilities that go far beyond basic CLI testing. The platform enables comprehensive model evaluation that helps you make data-driven decisions about your LLM strategy.

<Frame>
  <img alt="Enterprise Testing Interface" />
</Frame>

**Advanced Testing Features:**

* **Multi-Model Comparison**: Test multiple LLMs simultaneously across the same tasks and inputs. Compare performance between GPT-4o, Claude, Llama, Groq, Cerebras, and other leading models in parallel to identify the best fit for your specific use case.

* **Statistical Rigor**: Configure multiple iterations with consistent inputs to measure reliability and performance variance. This helps identify models that not only perform well but do so consistently across runs.

* **Real-World Validation**: Use your actual crew inputs and scenarios rather than synthetic benchmarks. The platform allows you to test with your specific industry context, company information, and real use cases for more accurate evaluation.

* **Comprehensive Analytics**: Access detailed performance metrics, execution times, and cost analysis across all tested models. This enables data-driven decision making rather than relying on general model reputation or theoretical capabilities.

* **Team Collaboration**: Share testing results and model performance data across your team, enabling collaborative decision-making and consistent model selection strategies across projects.

Go to [app.crewai.com](https://app.crewai.com) to get started!

<Info>
  The Enterprise platform transforms model selection from guesswork into a data-driven process, enabling you to validate the principles in this guide with your actual use cases and requirements.
</Info>

## Key Principles Summary

<CardGroup>
  <Card title="Task-Driven Selection" icon="bullseye">
    Choose models based on what the task actually requires, not theoretical capabilities or general reputation.
  </Card>

<Card title="Capability Matching" icon="puzzle-piece">
    Align model strengths with agent roles and responsibilities for optimal performance.
  </Card>

<Card title="Strategic Consistency" icon="link">
    Maintain coherent model selection strategy across related components and workflows.
  </Card>

<Card title="Practical Testing" icon="flask">
    Validate choices through real-world usage rather than benchmarks alone.
  </Card>

<Card title="Iterative Improvement" icon="arrow-up">
    Start simple and optimize based on actual performance and needs.
  </Card>

<Card title="Operational Balance" icon="scale-balanced">
    Balance performance requirements with cost and complexity constraints.
  </Card>
</CardGroup>

<Check>
  Remember: The best LLM choice is the one that consistently delivers the results you need within your operational constraints. Focus on understanding your requirements first, then select models that best match those needs.
</Check>

## Current Model Landscape (June 2025)

<Warning>
  **Snapshot in Time**: The following model rankings represent current leaderboard standings as of June 2025, compiled from [LMSys Arena](https://arena.lmsys.org/), [Artificial Analysis](https://artificialanalysis.ai/), and other leading benchmarks. LLM performance, availability, and pricing change rapidly. Always conduct your own evaluations with your specific use cases and data.
</Warning>

### Leading Models by Category

The tables below show a representative sample of current top-performing models across different categories, with guidance on their suitability for CrewAI agents:

<Note>
  These tables/metrics showcase selected leading models in each category and are not exhaustive. Many excellent models exist beyond those listed here. The goal is to illustrate the types of capabilities to look for rather than provide a complete catalog.
</Note>

<Tabs>
  <Tab title="Reasoning & Planning">
    **Best for Manager LLMs and Complex Analysis**

| Model                      | Intelligence Score | Cost (\$/M tokens) | Speed    | Best Use in CrewAI                                  |
    | :------------------------- | :----------------- | :----------------- | :------- | :-------------------------------------------------- |
    | **o3**                     | 70                 | \$17.50            | Fast     | Manager LLM for complex multi-agent coordination    |
    | **Gemini 2.5 Pro**         | 69                 | \$3.44             | Fast     | Strategic planning agents, research coordination    |
    | **DeepSeek R1**            | 68                 | \$0.96             | Moderate | Cost-effective reasoning for budget-conscious crews |
    | **Claude 4 Sonnet**        | 53                 | \$6.00             | Fast     | Analysis agents requiring nuanced understanding     |
    | **Qwen3 235B (Reasoning)** | 62                 | \$2.63             | Moderate | Open-source alternative for reasoning tasks         |

These models excel at multi-step reasoning and are ideal for agents that need to develop strategies, coordinate other agents, or analyze complex information.
  </Tab>

<Tab title="Coding & Technical">
    **Best for Development and Tool-Heavy Workflows**

| Model                 | Coding Performance | Tool Use Score | Cost (\$/M tokens) | Best Use in CrewAI                            |
    | :-------------------- | :----------------- | :------------- | :----------------- | :-------------------------------------------- |
    | **Claude 4 Sonnet**   | Excellent          | 72.7%          | \$6.00             | Primary coding agent, technical documentation |
    | **Claude 4 Opus**     | Excellent          | 72.5%          | \$30.00            | Complex software architecture, code review    |
    | **DeepSeek V3**       | Very Good          | High           | \$0.48             | Cost-effective coding for routine development |
    | **Qwen2.5 Coder 32B** | Very Good          | Medium         | \$0.15             | Budget-friendly coding agent                  |
    | **Llama 3.1 405B**    | Good               | 81.1%          | \$3.50             | Function calling LLM for tool-heavy workflows |

These models are optimized for code generation, debugging, and technical problem-solving, making them ideal for development-focused crews.
  </Tab>

<Tab title="Speed & Efficiency">
    **Best for High-Throughput and Real-Time Applications**

| Model                   | Speed (tokens/s) | Latency (TTFT) | Cost (\$/M tokens) | Best Use in CrewAI                   |
    | :---------------------- | :--------------- | :------------- | :----------------- | :----------------------------------- |
    | **Llama 4 Scout**       | 2,600            | 0.33s          | \$0.27             | High-volume processing agents        |
    | **Gemini 2.5 Flash**    | 376              | 0.30s          | \$0.26             | Real-time response agents            |
    | **DeepSeek R1 Distill** | 383              | Variable       | \$0.04             | Cost-optimized high-speed processing |
    | **Llama 3.3 70B**       | 2,500            | 0.52s          | \$0.60             | Balanced speed and capability        |
    | **Nova Micro**          | High             | 0.30s          | \$0.04             | Simple, fast task execution          |

These models prioritize speed and efficiency, perfect for agents handling routine operations or requiring quick responses. **Pro tip**: Pairing these models with fast inference providers like Groq can achieve even better performance, especially for open-source models like Llama.
  </Tab>

<Tab title="Balanced Performance">
    **Best All-Around Models for General Crews**

| Model                 | Overall Score | Versatility | Cost (\$/M tokens) | Best Use in CrewAI                |
    | :-------------------- | :------------ | :---------- | :----------------- | :-------------------------------- |
    | **GPT-4.1**           | 53            | Excellent   | \$3.50             | General-purpose crew LLM          |
    | **Claude 3.7 Sonnet** | 48            | Very Good   | \$6.00             | Balanced reasoning and creativity |
    | **Gemini 2.0 Flash**  | 48            | Good        | \$0.17             | Cost-effective general use        |
    | **Llama 4 Maverick**  | 51            | Good        | \$0.37             | Open-source general purpose       |
    | **Qwen3 32B**         | 44            | Good        | \$1.23             | Budget-friendly versatility       |

These models offer good performance across multiple dimensions, suitable for crews with diverse task requirements.
  </Tab>
</Tabs>

### Selection Framework for Current Models

<AccordionGroup>
  <Accordion title="High-Performance Crews" icon="rocket">
    **When performance is the priority**: Use top-tier models like **o3**, **Gemini 2.5 Pro**, or **Claude 4 Sonnet** for manager LLMs and critical agents. These models excel at complex reasoning and coordination but come with higher costs.

**Strategy**: Implement a multi-model approach where premium models handle strategic thinking while efficient models handle routine operations.
  </Accordion>

<Accordion title="Cost-Conscious Crews" icon="dollar-sign">
    **When budget is a primary constraint**: Focus on models like **DeepSeek R1**, **Llama 4 Scout**, or **Gemini 2.0 Flash**. These provide strong performance at significantly lower costs.

**Strategy**: Use cost-effective models for most agents, reserving premium models only for the most critical decision-making roles.
  </Accordion>

<Accordion title="Specialized Workflows" icon="screwdriver-wrench">
    **For specific domain expertise**: Choose models optimized for your primary use case. **Claude 4** series for coding, **Gemini 2.5 Pro** for research, **Llama 405B** for function calling.

**Strategy**: Select models based on your crew's primary function, ensuring the core capability aligns with model strengths.
  </Accordion>

<Accordion title="Enterprise & Privacy" icon="shield">
    **For data-sensitive operations**: Consider open-source models like **Llama 4** series, **DeepSeek V3**, or **Qwen3** that can be deployed locally while maintaining competitive performance.

**Strategy**: Deploy open-source models on private infrastructure, accepting potential performance trade-offs for data control.
  </Accordion>
</AccordionGroup>

### Key Considerations for Model Selection

* **Performance Trends**: The current landscape shows strong competition between reasoning-focused models (o3, Gemini 2.5 Pro) and balanced models (Claude 4, GPT-4.1). Specialized models like DeepSeek R1 offer excellent cost-performance ratios.

* **Speed vs. Intelligence Trade-offs**: Models like Llama 4 Scout prioritize speed (2,600 tokens/s) while maintaining reasonable intelligence, whereas models like o3 maximize reasoning capability at the cost of speed and price.

* **Open Source Viability**: The gap between open-source and proprietary models continues to narrow, with models like Llama 4 Maverick and DeepSeek V3 offering competitive performance at attractive price points. Fast inference providers particularly shine with open-source models, often delivering better speed-to-cost ratios than proprietary alternatives.

<Info>
  **Testing is Essential**: Leaderboard rankings provide general guidance, but your specific use case, prompting style, and evaluation criteria may produce different results. Always test candidate models with your actual tasks and data before making final decisions.
</Info>

### Practical Implementation Strategy

<Steps>
  <Step title="Start with Proven Models">
    Begin with well-established models like **GPT-4.1**, **Claude 3.7 Sonnet**, or **Gemini 2.0 Flash** that offer good performance across multiple dimensions and have extensive real-world validation.
  </Step>

<Step title="Identify Specialized Needs">
    Determine if your crew has specific requirements (coding, reasoning, speed) that would benefit from specialized models like **Claude 4 Sonnet** for development or **o3** for complex analysis. For speed-critical applications, consider fast inference providers like **Groq** alongside model selection.
  </Step>

<Step title="Implement Multi-Model Strategy">
    Use different models for different agents based on their roles. High-capability models for managers and complex tasks, efficient models for routine operations.
  </Step>

<Step title="Monitor and Optimize">
    Track performance metrics relevant to your use case and be prepared to adjust model selections as new models are released or pricing changes.
  </Step>
</Steps>

**Examples:**

Example 1 (unknown):
```unknown
**Alignment Checklist:**

* ✅ **Role Specificity**: Clear domain and responsibilities
* ✅ **LLM Match**: Model strengths align with role requirements
* ✅ **Backstory Depth**: Provides domain context the LLM can leverage
* ✅ **Tool Integration**: Tools support the agent's specialized function
* ✅ **Parameter Tuning**: Temperature and settings optimize for role needs

The key is creating agents where every configuration choice reinforces your LLM selection strategy, maximizing performance while optimizing costs.

## Practical Implementation Checklist

Rather than repeating the strategic framework, here's a tactical checklist for implementing your LLM selection decisions in CrewAI:

<Steps>
  <Step title="Audit Your Current Setup" icon="clipboard-check">
    **What to Review:**

    * Are all agents using the same LLM by default?
    * Which agents handle the most complex reasoning tasks?
    * Which agents primarily do data processing or formatting?
    * Are any agents heavily tool-dependent?

    **Action**: Document current agent roles and identify optimization opportunities.
  </Step>

  <Step title="Implement Crew-Level Strategy" icon="users-gear">
    **Set Your Baseline:**
```

Example 2 (unknown):
```unknown
**Action**: Establish your crew's default LLM before optimizing individual agents.
  </Step>

  <Step title="Optimize High-Impact Agents" icon="star">
    **Identify and Upgrade Key Agents:**
```

Example 3 (unknown):
```unknown
**Action**: Upgrade 20% of your agents that handle 80% of the complexity.
  </Step>

  <Step title="Validate with Enterprise Testing" icon="test-tube">
    **Once you deploy your agents to production:**

    * Use [CrewAI AOP platform](https://app.crewai.com) to A/B test your model selections
    * Run multiple iterations with real inputs to measure consistency and performance
    * Compare cost vs. performance across your optimized setup
    * Share results with your team for collaborative decision-making

    **Action**: Replace guesswork with data-driven validation using the testing platform.
  </Step>
</Steps>

### When to Use Different Model Types

<Tabs>
  <Tab title="Reasoning Models">
    Reasoning models become essential when tasks require genuine multi-step logical thinking, strategic planning, or high-level decision making that benefits from systematic analysis. These models excel when problems need to be broken down into components and analyzed systematically rather than handled through pattern matching or simple instruction following.

    Consider reasoning models for business strategy development, complex data analysis that requires drawing insights from multiple sources, multi-step problem solving where each step depends on previous analysis, and strategic planning tasks that require considering multiple variables and their interactions.

    However, reasoning models often come with higher costs and slower response times, so they're best reserved for tasks where their sophisticated capabilities provide genuine value rather than being used for simple operations that don't require complex reasoning.
  </Tab>

  <Tab title="Creative Models">
    Creative models become valuable when content generation is the primary output and the quality, style, and engagement level of that content directly impact success. These models excel when writing quality and style matter significantly, creative ideation or brainstorming is needed, or brand voice and tone are important considerations.

    Use creative models for blog post writing and article creation, marketing copy that needs to engage and persuade, creative storytelling and narrative development, and brand communications where voice and tone are crucial. These models often understand nuance and context better than general purpose alternatives.

    Creative models may be less suitable for technical or analytical tasks where precision and factual accuracy are more important than engagement and style. They're best used when the creative and communicative aspects of the output are primary success factors.
  </Tab>

  <Tab title="Efficient Models">
    Efficient models are ideal for high-frequency, routine operations where speed and cost optimization are priorities. These models work best when tasks have clear, well-defined parameters and don't require sophisticated reasoning or creative capabilities.

    Consider efficient models for data processing and transformation tasks, simple formatting and organization operations, function calling and tool usage where precision matters more than sophistication, and high-volume operations where cost per operation is a significant factor.

    The key with efficient models is ensuring that their capabilities align with task requirements. They can handle many routine operations effectively but may struggle with tasks requiring nuanced understanding, complex reasoning, or sophisticated content generation.
  </Tab>

  <Tab title="Open Source Models">
    Open source models become attractive when budget constraints are significant, data privacy requirements exist, customization needs are important, or local deployment is required for operational or compliance reasons.

    Consider open source models for internal company tools where data privacy is paramount, privacy-sensitive applications that can't use external APIs, cost-optimized deployments where per-token pricing is prohibitive, and situations requiring custom model modifications or fine-tuning.

    However, open source models require more technical expertise to deploy and maintain effectively. Consider the total cost of ownership including infrastructure, technical overhead, and ongoing maintenance when evaluating open source options.
  </Tab>
</Tabs>

## Common CrewAI Model Selection Pitfalls

<AccordionGroup>
  <Accordion title="The 'One Model Fits All' Trap" icon="triangle-exclamation">
    **The Problem**: Using the same LLM for all agents in a crew, regardless of their specific roles and responsibilities. This is often the default approach but rarely optimal.

    **Real Example**: Using GPT-4o for both a strategic planning manager and a data extraction agent. The manager needs reasoning capabilities worth the premium cost, but the data extractor could perform just as well with GPT-4o-mini at a fraction of the price.

    **CrewAI Solution**: Leverage agent-specific LLM configuration to match model capabilities with agent roles:
```

Example 4 (unknown):
```unknown
</Accordion>

  <Accordion title="Ignoring Crew-Level vs Agent-Level LLM Hierarchy" icon="shuffle">
    **The Problem**: Not understanding how CrewAI's LLM hierarchy works - crew LLM, manager LLM, and agent LLM settings can conflict or be poorly coordinated.

    **Real Example**: Setting a crew to use Claude, but having agents configured with GPT models, creating inconsistent behavior and unnecessary model switching overhead.

    **CrewAI Solution**: Plan your LLM hierarchy strategically:
```

---

## Execution Hooks Overview

**URL:** llms-txt#execution-hooks-overview

**Contents:**
- Types of Execution Hooks
  - 1. [LLM Call Hooks](/learn/llm-hooks)
  - 2. [Tool Call Hooks](/learn/tool-hooks)
- Hook Registration Methods
  - 1. Decorator-Based Hooks (Recommended)
  - 2. Crew-Scoped Hooks
- Hook Execution Flow
  - LLM Call Flow
  - Tool Call Flow
- Hook Context Objects

Source: https://docs.crewai.com/en/learn/execution-hooks

Understanding and using execution hooks in CrewAI for fine-grained control over agent operations

Execution Hooks provide fine-grained control over the runtime behavior of your CrewAI agents. Unlike kickoff hooks that run before and after crew execution, execution hooks intercept specific operations during agent execution, allowing you to modify behavior, implement safety checks, and add comprehensive monitoring.

## Types of Execution Hooks

CrewAI provides two main categories of execution hooks:

### 1. [LLM Call Hooks](/learn/llm-hooks)

Control and monitor language model interactions:

* **Before LLM Call**: Modify prompts, validate inputs, implement approval gates
* **After LLM Call**: Transform responses, sanitize outputs, update conversation history

* Iteration limiting
* Cost tracking and token usage monitoring
* Response sanitization and content filtering
* Human-in-the-loop approval for LLM calls
* Adding safety guidelines or context
* Debug logging and request/response inspection

[View LLM Hooks Documentation →](/learn/llm-hooks)

### 2. [Tool Call Hooks](/learn/tool-hooks)

Control and monitor tool execution:

* **Before Tool Call**: Modify inputs, validate parameters, block dangerous operations
* **After Tool Call**: Transform results, sanitize outputs, log execution details

* Safety guardrails for destructive operations
* Human approval for sensitive actions
* Input validation and sanitization
* Result caching and rate limiting
* Tool usage analytics
* Debug logging and monitoring

[View Tool Hooks Documentation →](/learn/tool-hooks)

## Hook Registration Methods

### 1. Decorator-Based Hooks (Recommended)

The cleanest and most Pythonic way to register hooks:

### 2. Crew-Scoped Hooks

Apply hooks only to specific crew instances:

## Hook Execution Flow

## Hook Context Objects

### LLMCallHookContext

Provides access to LLM execution state:

### ToolCallHookContext

Provides access to tool execution state:

### Safety and Validation

### Human-in-the-Loop

### Monitoring and Analytics

```python theme={null}
from collections import defaultdict
import time

metrics = defaultdict(lambda: {'count': 0, 'total_time': 0})

@before_tool_call
def start_timer(context):
    context.tool_input['_start'] = time.time()
    return None

@after_tool_call
def track_metrics(context):
    start = context.tool_input.get('_start', time.time())
    duration = time.time() - start

metrics[context.tool_name]['count'] += 1
    metrics[context.tool_name]['total_time'] += duration

**Examples:**

Example 1 (unknown):
```unknown
### 2. Crew-Scoped Hooks

Apply hooks only to specific crew instances:
```

Example 2 (unknown):
```unknown
## Hook Execution Flow

### LLM Call Flow
```

Example 3 (unknown):
```unknown
### Tool Call Flow
```

Example 4 (unknown):
```unknown
## Hook Context Objects

### LLMCallHookContext

Provides access to LLM execution state:
```

---

## FAQs

**URL:** llms-txt#faqs

Source: https://docs.crewai.com/en/enterprise/resources/frequently-asked-questions

Frequently asked questions about CrewAI AOP

<AccordionGroup>
  <Accordion title="How is task execution handled in the hierarchical process?">
    In the hierarchical process, a manager agent is automatically created and coordinates the workflow, delegating tasks and validating outcomes for streamlined and effective execution. The manager agent utilizes tools to facilitate task delegation and execution by agents under the manager's guidance. The manager LLM is crucial for the hierarchical process and must be set up correctly for proper function.
  </Accordion>

<Accordion title="Where can I get the latest CrewAI documentation?">
    The most up-to-date documentation for CrewAI is available on our official documentation website: [https://docs.crewai.com/](https://docs.crewai.com/)
    <Card href="https://docs.crewai.com/" icon="books">CrewAI Docs</Card>
  </Accordion>

<Accordion title="What are the key differences between Hierarchical and Sequential Processes in CrewAI?">
    #### Hierarchical Process:

* Tasks are delegated and executed based on a structured chain of command
    * A manager language model (`manager_llm`) must be specified for the manager agent
    * Manager agent oversees task execution, planning, delegation, and validation
    * Tasks are not pre-assigned; the manager allocates tasks to agents based on their capabilities

#### Sequential Process:

* Tasks are executed one after another, ensuring tasks are completed in an orderly progression
    * Output of one task serves as context for the next
    * Task execution follows the predefined order in the task list

#### Which Process is Better for Complex Projects?

The hierarchical process is better suited for complex projects because it allows for:

* **Dynamic task allocation and delegation**: Manager agent can assign tasks based on agent capabilities
    * **Structured validation and oversight**: Manager agent reviews task outputs and ensures completion
    * **Complex task management**: Precise control over tool availability at the agent level
  </Accordion>

<Accordion title="What are the benefits of using memory in the CrewAI framework?">
    * **Adaptive Learning**: Crews become more efficient over time, adapting to new information and refining their approach to tasks
    * **Enhanced Personalization**: Memory enables agents to remember user preferences and historical interactions, leading to personalized experiences
    * **Improved Problem Solving**: Access to a rich memory store aids agents in making more informed decisions, drawing on past learnings and contextual insights
  </Accordion>

<Accordion title="What is the purpose of setting a maximum RPM limit for an agent?">
    Setting a maximum RPM limit for an agent prevents the agent from making too many requests to external services, which can help to avoid rate limits and improve performance.
  </Accordion>

<Accordion title="What role does human input play in the execution of tasks within a CrewAI crew?">
    Human input allows agents to request additional information or clarification when necessary. This feature is crucial in complex decision-making processes or when agents require more details to complete a task effectively.

To integrate human input into agent execution, set the `human_input` flag in the task definition. When enabled, the agent prompts the user for input before delivering its final answer. This input can provide extra context, clarify ambiguities, or validate the agent's output.

For detailed implementation guidance, see our [Human-in-the-Loop guide](/en/enterprise/guides/human-in-the-loop).
  </Accordion>

<Accordion title="What advanced customization options are available for tailoring and enhancing agent behavior and capabilities in CrewAI?">
    CrewAI provides a range of advanced customization options:

* **Language Model Customization**: Agents can be customized with specific language models (`llm`) and function-calling language models (`function_calling_llm`)
    * **Performance and Debugging Settings**: Adjust an agent's performance and monitor its operations
    * **Verbose Mode**: Enables detailed logging of an agent's actions, useful for debugging and optimization
    * **RPM Limit**: Sets the maximum number of requests per minute (`max_rpm`)
    * **Maximum Iterations**: The `max_iter` attribute allows users to define the maximum number of iterations an agent can perform for a single task
    * **Delegation and Autonomy**: Control an agent's ability to delegate or ask questions with the `allow_delegation` attribute (default: True)
    * **Human Input Integration**: Agents can request additional information or clarification when necessary
  </Accordion>

<Accordion title="In what scenarios is human input particularly useful in agent execution?">
    Human input is particularly useful when:

* **Agents require additional information or clarification**: When agents encounter ambiguity or incomplete data
    * **Agents need to make complex or sensitive decisions**: Human input can assist in ethical or nuanced decision-making
    * **Oversight and validation of agent output**: Human input can help validate results and prevent errors
    * **Customizing agent behavior**: Human input can provide feedback to refine agent responses over time
    * **Identifying and resolving errors or limitations**: Human input helps address agent capability gaps
  </Accordion>

<Accordion title="What are the different types of memory that are available in crewAI?">
    The different types of memory available in CrewAI are:

* **Short-term memory**: Temporary storage for immediate context
    * **Long-term memory**: Persistent storage for learned patterns and information
    * **Entity memory**: Focused storage for specific entities and their attributes
    * **Contextual memory**: Memory that maintains context across interactions

Learn more about the different types of memory:
    <Card href="https://docs.crewai.com/concepts/memory" icon="brain">CrewAI Memory</Card>
  </Accordion>

<Accordion title="How do I use Output Pydantic in a Task?">
    To use Output Pydantic in a task, you need to define the expected output of the task as a Pydantic model. Here's a quick example:

<Steps>
      <Step title="Define a Pydantic model">
        
      </Step>

<Step title="Create a task with Output Pydantic">
        
      </Step>

<Step title="Set the output_pydantic attribute in your agent">
        
      </Step>
    </Steps>

Here's a tutorial on how to consistently get structured outputs from your agents:

<iframe title="Structured outputs in CrewAI" />
  </Accordion>

<Accordion title="How can I create custom tools for my CrewAI agents?">
    You can create custom tools by subclassing the `BaseTool` class provided by CrewAI or by using the tool decorator. Subclassing involves defining a new class that inherits from `BaseTool`, specifying the name, description, and the `_run` method for operational logic. The tool decorator allows you to create a `Tool` object directly with the required attributes and a functional logic.

<Card href="/en/learn/create-custom-tools" icon="code">CrewAI Tools Guide</Card>
  </Accordion>

<Accordion title="How can you control the maximum number of requests per minute that the entire crew can perform?">
    The `max_rpm` attribute sets the maximum number of requests per minute the crew can perform to avoid rate limits and will override individual agents' `max_rpm` settings if you set it.
  </Accordion>
</AccordionGroup>

**Examples:**

Example 1 (unknown):
```unknown
</Step>

      <Step title="Create a task with Output Pydantic">
```

Example 2 (unknown):
```unknown
</Step>

      <Step title="Set the output_pydantic attribute in your agent">
```

---

## First agent creation - discovers tools from server

**URL:** llms-txt#first-agent-creation---discovers-tools-from-server

agent1 = Agent(role="First", goal="Test", backstory="Test",
               mcps=["https://api.example.com/mcp"])

---

## Form the crew and kick it off

**URL:** llms-txt#form-the-crew-and-kick-it-off

**Contents:**
- Configuration Options
- Advanced Usage

crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    verbose=2
)

result = crew.kickoff()
print(result)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## Configuration Options

The `TavilySearchTool` accepts the following arguments during initialization or when calling the `run` method:

* `query` (str): **Required**. The search query string.
* `search_depth` (Literal\["basic", "advanced"], optional): The depth of the search. Defaults to `"basic"`.
* `topic` (Literal\["general", "news", "finance"], optional): The topic to focus the search on. Defaults to `"general"`.
* `time_range` (Literal\["day", "week", "month", "year"], optional): The time range for the search. Defaults to `None`.
* `days` (int, optional): The number of days to search back. Relevant if `time_range` is not set. Defaults to `7`.
* `max_results` (int, optional): The maximum number of search results to return. Defaults to `5`.
* `include_domains` (Sequence\[str], optional): A list of domains to prioritize in the search. Defaults to `None`.
* `exclude_domains` (Sequence\[str], optional): A list of domains to exclude from the search. Defaults to `None`.
* `include_answer` (Union\[bool, Literal\["basic", "advanced"]], optional): Whether to include a direct answer synthesized from the search results. Defaults to `False`.
* `include_raw_content` (bool, optional): Whether to include the raw HTML content of the searched pages. Defaults to `False`.
* `include_images` (bool, optional): Whether to include image results. Defaults to `False`.
* `timeout` (int, optional): The request timeout in seconds. Defaults to `60`.

## Advanced Usage

You can configure the tool with custom parameters:
```

---

## Form the crew with a sequential process

**URL:** llms-txt#form-the-crew-with-a-sequential-process

report_crew = Crew(
  agents=[researcher, analyst, writer],
  tasks=[research_task, analysis_task, writing_task],
  process=Process.sequential
)

---

## Get current hooks

**URL:** llms-txt#get-current-hooks

**Contents:**
- Advanced Patterns
  - Conditional Hook Execution
  - Context-Aware Input Modification
  - Tool Chain Monitoring
- Best Practices
- Error Handling
- Type Safety

before_hooks = get_before_tool_call_hooks()
after_hooks = get_after_tool_call_hooks()

print(f"Registered: {len(before_hooks)} before, {len(after_hooks)} after")
python theme={null}
@before_tool_call
def conditional_blocking(context: ToolCallHookContext) -> bool | None:
    # Only block for specific agents
    if context.agent and context.agent.role == "junior_agent":
        if context.tool_name in ['delete_file', 'send_email']:
            print(f"❌ Junior agents cannot use {context.tool_name}")
            return False

# Only block during specific tasks
    if context.task and "sensitive" in context.task.description.lower():
        if context.tool_name == 'web_search':
            print("❌ Web search blocked for sensitive tasks")
            return False

return None
python theme={null}
@before_tool_call
def enhance_tool_inputs(context: ToolCallHookContext) -> None:
    # Add context based on agent role
    if context.agent and context.agent.role == "researcher":
        if context.tool_name == 'web_search':
            # Add domain restrictions for researchers
            context.tool_input['domains'] = ['edu', 'gov', 'org']

# Add context based on task
    if context.task and "urgent" in context.task.description.lower():
        if context.tool_name == 'send_email':
            context.tool_input['priority'] = 'high'

return None
python theme={null}
tool_call_chain = []

@before_tool_call
def track_tool_chain(context: ToolCallHookContext) -> None:
    tool_call_chain.append({
        'tool': context.tool_name,
        'timestamp': time.time(),
        'agent': context.agent.role if context.agent else 'Unknown'
    })

# Detect potential infinite loops
    recent_calls = tool_call_chain[-5:]
    if len(recent_calls) == 5 and all(c['tool'] == context.tool_name for c in recent_calls):
        print(f"⚠️  Warning: {context.tool_name} called 5 times in a row")

return None
python theme={null}
@before_tool_call
def safe_validation(context: ToolCallHookContext) -> bool | None:
    try:
        # Your validation logic
        if not validate_input(context.tool_input):
            return False
    except Exception as e:
        print(f"⚠️ Hook error: {e}")
        # Decide: allow or block on error
        return None  # Allow execution despite error
python theme={null}
from crewai.hooks import ToolCallHookContext, BeforeToolCallHookType, AfterToolCallHookType

**Examples:**

Example 1 (unknown):
```unknown
## Advanced Patterns

### Conditional Hook Execution
```

Example 2 (unknown):
```unknown
### Context-Aware Input Modification
```

Example 3 (unknown):
```unknown
### Tool Chain Monitoring
```

Example 4 (unknown):
```unknown
## Best Practices

1. **Keep Hooks Focused**: Each hook should have a single responsibility
2. **Avoid Heavy Computation**: Hooks execute on every tool call
3. **Handle Errors Gracefully**: Use try-except to prevent hook failures
4. **Use Type Hints**: Leverage `ToolCallHookContext` for better IDE support
5. **Document Blocking Conditions**: Make it clear when/why tools are blocked
6. **Test Hooks Independently**: Unit test hooks before using in production
7. **Clear Hooks in Tests**: Use `clear_all_tool_call_hooks()` between test runs
8. **Modify In-Place**: Always modify `context.tool_input` in-place, never replace
9. **Log Important Decisions**: Especially when blocking tool execution
10. **Consider Performance**: Cache expensive validations when possible

## Error Handling
```

---

## Get your crew to work!

**URL:** llms-txt#get-your-crew-to-work!

**Contents:**
  - Step 5: View Traces in Phoenix
  - Version Compatibility Information
  - References

result = crew.kickoff()

print("######################")
print(result)
```

### Step 5: View Traces in Phoenix

After running the agent, you can view the traces generated by your CrewAI application in Phoenix. You should see detailed steps of the agent interactions and LLM calls, which can help you debug and optimize your AI agents.

Log into your Phoenix Cloud account and navigate to the project you specified in the `project_name` parameter. You'll see a timeline view of your trace with all the agent interactions, tool usages, and LLM calls.

![Example trace in Phoenix showing agent interactions](https://storage.googleapis.com/arize-assets/fixtures/crewai_traces.png)

### Version Compatibility Information

* Python 3.8+
* CrewAI >= 0.86.0
* Arize Phoenix >= 7.0.1
* OpenTelemetry SDK >= 1.31.0

* [Phoenix Documentation](https://docs.arize.com/phoenix/) - Overview of the Phoenix platform.
* [CrewAI Documentation](https://docs.crewai.com/) - Overview of the CrewAI framework.
* [OpenTelemetry Docs](https://opentelemetry.io/docs/) - OpenTelemetry guide
* [OpenInference GitHub](https://github.com/openinference/openinference) - Source code for OpenInference SDK.

---

## GitHub Integration

**URL:** llms-txt#github-integration

**Contents:**
- Overview
- Prerequisites
- Setting Up GitHub Integration
  - 1. Connect Your GitHub Account
  - 2. Install Required Package
  - 3. Environment Variable Setup
- Available Actions
- Usage Examples
  - Basic GitHub Agent Setup

Source: https://docs.crewai.com/en/enterprise/integrations/github

Repository and issue management with GitHub integration for CrewAI.

Enable your agents to manage repositories, issues, and releases through GitHub. Create and update issues, manage releases, track project development, and streamline your software development workflow with AI-powered automation.

Before using the GitHub integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A GitHub account with appropriate repository permissions
* Connected your GitHub account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)

## Setting Up GitHub Integration

### 1. Connect Your GitHub Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **GitHub** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for repository and issue management
5. Copy your Enterprise Token from [Integration Settings](https://app.crewai.com/crewai_plus/settings/integrations)

### 2. Install Required Package

### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>

Or add it to your `.env` file:

<AccordionGroup>
  <Accordion title="github/create_issue">
    **Description:** Create an issue in GitHub.

* `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Issue. (example: "abc").
    * `repo` (string, required): Repository - Specify the name of the associated repository for this Issue.
    * `title` (string, required): Issue Title - Specify the title of the issue to create.
    * `body` (string, optional): Issue Body - Specify the body contents of the issue to create.
    * `assignees` (string, optional): Assignees - Specify the assignee(s)' GitHub login as an array of strings for this issue. (example: `["octocat"]`).
  </Accordion>

<Accordion title="github/update_issue">
    **Description:** Update an issue in GitHub.

* `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Issue. (example: "abc").
    * `repo` (string, required): Repository - Specify the name of the associated repository for this Issue.
    * `issue_number` (string, required): Issue Number - Specify the number of the issue to update.
    * `title` (string, required): Issue Title - Specify the title of the issue to update.
    * `body` (string, optional): Issue Body - Specify the body contents of the issue to update.
    * `assignees` (string, optional): Assignees - Specify the assignee(s)' GitHub login as an array of strings for this issue. (example: `["octocat"]`).
    * `state` (string, optional): State - Specify the updated state of the issue.
      * Options: `open`, `closed`
  </Accordion>

<Accordion title="github/get_issue_by_number">
    **Description:** Get an issue by number in GitHub.

* `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Issue. (example: "abc").
    * `repo` (string, required): Repository - Specify the name of the associated repository for this Issue.
    * `issue_number` (string, required): Issue Number - Specify the number of the issue to fetch.
  </Accordion>

<Accordion title="github/lock_issue">
    **Description:** Lock an issue in GitHub.

* `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Issue. (example: "abc").
    * `repo` (string, required): Repository - Specify the name of the associated repository for this Issue.
    * `issue_number` (string, required): Issue Number - Specify the number of the issue to lock.
    * `lock_reason` (string, required): Lock Reason - Specify a reason for locking the issue or pull request conversation.
      * Options: `off-topic`, `too heated`, `resolved`, `spam`
  </Accordion>

<Accordion title="github/search_issue">
    **Description:** Search for issues in GitHub.

* `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Issue. (example: "abc").
    * `repo` (string, required): Repository - Specify the name of the associated repository for this Issue.
    * `filter` (object, required): A filter in disjunctive normal form - OR of AND groups of single conditions.
      
      Available fields: `assignee`, `creator`, `mentioned`, `labels`
  </Accordion>

<Accordion title="github/create_release">
    **Description:** Create a release in GitHub.

* `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Release. (example: "abc").
    * `repo` (string, required): Repository - Specify the name of the associated repository for this Release.
    * `tag_name` (string, required): Name - Specify the name of the release tag to be created. (example: "v1.0.0").
    * `target_commitish` (string, optional): Target - Specify the target of the release. This can either be a branch name or a commit SHA. Defaults to the main branch. (example: "master").
    * `body` (string, optional): Body - Specify a description for this release.
    * `draft` (string, optional): Draft - Specify whether the created release should be a draft (unpublished) release.
      * Options: `true`, `false`
    * `prerelease` (string, optional): Prerelease - Specify whether the created release should be a prerelease.
      * Options: `true`, `false`
    * `discussion_category_name` (string, optional): Discussion Category Name - If specified, a discussion of the specified category is created and linked to the release. The value must be a category that already exists in the repository.
    * `generate_release_notes` (string, optional): Release Notes - Specify whether the created release should automatically create release notes using the provided name and body specified.
      * Options: `true`, `false`
  </Accordion>

<Accordion title="github/update_release">
    **Description:** Update a release in GitHub.

* `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Release. (example: "abc").
    * `repo` (string, required): Repository - Specify the name of the associated repository for this Release.
    * `id` (string, required): Release ID - Specify the ID of the release to update.
    * `tag_name` (string, optional): Name - Specify the name of the release tag to be updated. (example: "v1.0.0").
    * `target_commitish` (string, optional): Target - Specify the target of the release. This can either be a branch name or a commit SHA. Defaults to the main branch. (example: "master").
    * `body` (string, optional): Body - Specify a description for this release.
    * `draft` (string, optional): Draft - Specify whether the created release should be a draft (unpublished) release.
      * Options: `true`, `false`
    * `prerelease` (string, optional): Prerelease - Specify whether the created release should be a prerelease.
      * Options: `true`, `false`
    * `discussion_category_name` (string, optional): Discussion Category Name - If specified, a discussion of the specified category is created and linked to the release. The value must be a category that already exists in the repository.
    * `generate_release_notes` (string, optional): Release Notes - Specify whether the created release should automatically create release notes using the provided name and body specified.
      * Options: `true`, `false`
  </Accordion>

<Accordion title="github/get_release_by_id">
    **Description:** Get a release by ID in GitHub.

* `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Release. (example: "abc").
    * `repo` (string, required): Repository - Specify the name of the associated repository for this Release.
    * `id` (string, required): Release ID - Specify the release ID of the release to fetch.
  </Accordion>

<Accordion title="github/get_release_by_tag_name">
    **Description:** Get a release by tag name in GitHub.

* `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Release. (example: "abc").
    * `repo` (string, required): Repository - Specify the name of the associated repository for this Release.
    * `tag_name` (string, required): Name - Specify the tag of the release to fetch. (example: "v1.0.0").
  </Accordion>

<Accordion title="github/delete_release">
    **Description:** Delete a release in GitHub.

* `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Release. (example: "abc").
    * `repo` (string, required): Repository - Specify the name of the associated repository for this Release.
    * `id` (string, required): Release ID - Specify the ID of the release to delete.
  </Accordion>
</AccordionGroup>

### Basic GitHub Agent Setup

```python theme={null}
from crewai import Agent, Task, Crew
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

Example 3 (unknown):
```unknown
## Available Actions

<AccordionGroup>
  <Accordion title="github/create_issue">
    **Description:** Create an issue in GitHub.

    **Parameters:**

    * `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Issue. (example: "abc").
    * `repo` (string, required): Repository - Specify the name of the associated repository for this Issue.
    * `title` (string, required): Issue Title - Specify the title of the issue to create.
    * `body` (string, optional): Issue Body - Specify the body contents of the issue to create.
    * `assignees` (string, optional): Assignees - Specify the assignee(s)' GitHub login as an array of strings for this issue. (example: `["octocat"]`).
  </Accordion>

  <Accordion title="github/update_issue">
    **Description:** Update an issue in GitHub.

    **Parameters:**

    * `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Issue. (example: "abc").
    * `repo` (string, required): Repository - Specify the name of the associated repository for this Issue.
    * `issue_number` (string, required): Issue Number - Specify the number of the issue to update.
    * `title` (string, required): Issue Title - Specify the title of the issue to update.
    * `body` (string, optional): Issue Body - Specify the body contents of the issue to update.
    * `assignees` (string, optional): Assignees - Specify the assignee(s)' GitHub login as an array of strings for this issue. (example: `["octocat"]`).
    * `state` (string, optional): State - Specify the updated state of the issue.
      * Options: `open`, `closed`
  </Accordion>

  <Accordion title="github/get_issue_by_number">
    **Description:** Get an issue by number in GitHub.

    **Parameters:**

    * `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Issue. (example: "abc").
    * `repo` (string, required): Repository - Specify the name of the associated repository for this Issue.
    * `issue_number` (string, required): Issue Number - Specify the number of the issue to fetch.
  </Accordion>

  <Accordion title="github/lock_issue">
    **Description:** Lock an issue in GitHub.

    **Parameters:**

    * `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Issue. (example: "abc").
    * `repo` (string, required): Repository - Specify the name of the associated repository for this Issue.
    * `issue_number` (string, required): Issue Number - Specify the number of the issue to lock.
    * `lock_reason` (string, required): Lock Reason - Specify a reason for locking the issue or pull request conversation.
      * Options: `off-topic`, `too heated`, `resolved`, `spam`
  </Accordion>

  <Accordion title="github/search_issue">
    **Description:** Search for issues in GitHub.

    **Parameters:**

    * `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Issue. (example: "abc").
    * `repo` (string, required): Repository - Specify the name of the associated repository for this Issue.
    * `filter` (object, required): A filter in disjunctive normal form - OR of AND groups of single conditions.
```

Example 4 (unknown):
```unknown
Available fields: `assignee`, `creator`, `mentioned`, `labels`
  </Accordion>

  <Accordion title="github/create_release">
    **Description:** Create a release in GitHub.

    **Parameters:**

    * `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Release. (example: "abc").
    * `repo` (string, required): Repository - Specify the name of the associated repository for this Release.
    * `tag_name` (string, required): Name - Specify the name of the release tag to be created. (example: "v1.0.0").
    * `target_commitish` (string, optional): Target - Specify the target of the release. This can either be a branch name or a commit SHA. Defaults to the main branch. (example: "master").
    * `body` (string, optional): Body - Specify a description for this release.
    * `draft` (string, optional): Draft - Specify whether the created release should be a draft (unpublished) release.
      * Options: `true`, `false`
    * `prerelease` (string, optional): Prerelease - Specify whether the created release should be a prerelease.
      * Options: `true`, `false`
    * `discussion_category_name` (string, optional): Discussion Category Name - If specified, a discussion of the specified category is created and linked to the release. The value must be a category that already exists in the repository.
    * `generate_release_notes` (string, optional): Release Notes - Specify whether the created release should automatically create release notes using the provided name and body specified.
      * Options: `true`, `false`
  </Accordion>

  <Accordion title="github/update_release">
    **Description:** Update a release in GitHub.

    **Parameters:**

    * `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Release. (example: "abc").
    * `repo` (string, required): Repository - Specify the name of the associated repository for this Release.
    * `id` (string, required): Release ID - Specify the ID of the release to update.
    * `tag_name` (string, optional): Name - Specify the name of the release tag to be updated. (example: "v1.0.0").
    * `target_commitish` (string, optional): Target - Specify the target of the release. This can either be a branch name or a commit SHA. Defaults to the main branch. (example: "master").
    * `body` (string, optional): Body - Specify a description for this release.
    * `draft` (string, optional): Draft - Specify whether the created release should be a draft (unpublished) release.
      * Options: `true`, `false`
    * `prerelease` (string, optional): Prerelease - Specify whether the created release should be a prerelease.
      * Options: `true`, `false`
    * `discussion_category_name` (string, optional): Discussion Category Name - If specified, a discussion of the specified category is created and linked to the release. The value must be a category that already exists in the repository.
    * `generate_release_notes` (string, optional): Release Notes - Specify whether the created release should automatically create release notes using the provided name and body specified.
      * Options: `true`, `false`
  </Accordion>

  <Accordion title="github/get_release_by_id">
    **Description:** Get a release by ID in GitHub.

    **Parameters:**

    * `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Release. (example: "abc").
    * `repo` (string, required): Repository - Specify the name of the associated repository for this Release.
    * `id` (string, required): Release ID - Specify the release ID of the release to fetch.
  </Accordion>

  <Accordion title="github/get_release_by_tag_name">
    **Description:** Get a release by tag name in GitHub.

    **Parameters:**

    * `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Release. (example: "abc").
    * `repo` (string, required): Repository - Specify the name of the associated repository for this Release.
    * `tag_name` (string, required): Name - Specify the tag of the release to fetch. (example: "v1.0.0").
  </Accordion>

  <Accordion title="github/delete_release">
    **Description:** Delete a release in GitHub.

    **Parameters:**

    * `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Release. (example: "abc").
    * `repo` (string, required): Repository - Specify the name of the associated repository for this Release.
    * `id` (string, required): Release ID - Specify the ID of the release to delete.
  </Accordion>
</AccordionGroup>

## Usage Examples

### Basic GitHub Agent Setup
```

---

## Gmail Integration

**URL:** llms-txt#gmail-integration

**Contents:**
- Overview
- Prerequisites
- Setting Up Gmail Integration
  - 1. Connect Your Gmail Account
  - 2. Install Required Package
  - 3. Environment Variable Setup
- Available Actions
- Usage Examples
  - Basic Gmail Agent Setup

Source: https://docs.crewai.com/en/enterprise/integrations/gmail

Email and contact management with Gmail integration for CrewAI.

Enable your agents to manage emails, contacts, and drafts through Gmail. Send emails, search messages, manage contacts, create drafts, and streamline your email communications with AI-powered automation.

Before using the Gmail integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A Gmail account with appropriate permissions
* Connected your Gmail account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)

## Setting Up Gmail Integration

### 1. Connect Your Gmail Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Gmail** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for email and contact management
5. Copy your Enterprise Token from [Integration Settings](https://app.crewai.com/crewai_plus/settings/integrations)

### 2. Install Required Package

### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>

Or add it to your `.env` file:

<AccordionGroup>
  <Accordion title="gmail/fetch_emails">
    **Description:** Retrieve a list of messages.

* `userId` (string, required): The user's email address or 'me' for the authenticated user. (default: "me")
    * `q` (string, optional): Search query to filter messages (e.g., 'from:[someone@example.com](mailto:someone@example.com) is:unread').
    * `maxResults` (integer, optional): Maximum number of messages to return (1-500). (default: 100)
    * `pageToken` (string, optional): Page token to retrieve a specific page of results.
    * `labelIds` (array, optional): Only return messages with labels that match all of the specified label IDs.
    * `includeSpamTrash` (boolean, optional): Include messages from SPAM and TRASH in the results. (default: false)
  </Accordion>

<Accordion title="gmail/send_email">
    **Description:** Send an email.

* `to` (string, required): Recipient email address.
    * `subject` (string, required): Email subject line.
    * `body` (string, required): Email message content.
    * `userId` (string, optional): The user's email address or 'me' for the authenticated user. (default: "me")
    * `cc` (string, optional): CC email addresses (comma-separated).
    * `bcc` (string, optional): BCC email addresses (comma-separated).
    * `from` (string, optional): Sender email address (if different from authenticated user).
    * `replyTo` (string, optional): Reply-to email address.
    * `threadId` (string, optional): Thread ID if replying to an existing conversation.
  </Accordion>

<Accordion title="gmail/delete_email">
    **Description:** Delete an email by ID.

* `userId` (string, required): The user's email address or 'me' for the authenticated user.
    * `id` (string, required): The ID of the message to delete.
  </Accordion>

<Accordion title="gmail/create_draft">
    **Description:** Create a new draft email.

* `userId` (string, required): The user's email address or 'me' for the authenticated user.
    * `message` (object, required): Message object containing the draft content.
      * `raw` (string, required): Base64url encoded email message.
  </Accordion>

<Accordion title="gmail/get_message">
    **Description:** Retrieve a specific message by ID.

* `userId` (string, required): The user's email address or 'me' for the authenticated user. (default: "me")
    * `id` (string, required): The ID of the message to retrieve.
    * `format` (string, optional): The format to return the message in. Options: "full", "metadata", "minimal", "raw". (default: "full")
    * `metadataHeaders` (array, optional): When given and format is METADATA, only include headers specified.
  </Accordion>

<Accordion title="gmail/get_attachment">
    **Description:** Retrieve a message attachment.

* `userId` (string, required): The user's email address or 'me' for the authenticated user. (default: "me")
    * `messageId` (string, required): The ID of the message containing the attachment.
    * `id` (string, required): The ID of the attachment to retrieve.
  </Accordion>

<Accordion title="gmail/fetch_thread">
    **Description:** Retrieve a specific email thread by ID.

* `userId` (string, required): The user's email address or 'me' for the authenticated user. (default: "me")
    * `id` (string, required): The ID of the thread to retrieve.
    * `format` (string, optional): The format to return the messages in. Options: "full", "metadata", "minimal". (default: "full")
    * `metadataHeaders` (array, optional): When given and format is METADATA, only include headers specified.
  </Accordion>

<Accordion title="gmail/modify_thread">
    **Description:** Modify the labels applied to a thread.

* `userId` (string, required): The user's email address or 'me' for the authenticated user. (default: "me")
    * `id` (string, required): The ID of the thread to modify.
    * `addLabelIds` (array, optional): A list of IDs of labels to add to this thread.
    * `removeLabelIds` (array, optional): A list of IDs of labels to remove from this thread.
  </Accordion>

<Accordion title="gmail/trash_thread">
    **Description:** Move a thread to the trash.

* `userId` (string, required): The user's email address or 'me' for the authenticated user. (default: "me")
    * `id` (string, required): The ID of the thread to trash.
  </Accordion>

<Accordion title="gmail/untrash_thread">
    **Description:** Remove a thread from the trash.

* `userId` (string, required): The user's email address or 'me' for the authenticated user. (default: "me")
    * `id` (string, required): The ID of the thread to untrash.
  </Accordion>
</AccordionGroup>

### Basic Gmail Agent Setup

```python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

Example 3 (unknown):
```unknown
## Available Actions

<AccordionGroup>
  <Accordion title="gmail/fetch_emails">
    **Description:** Retrieve a list of messages.

    **Parameters:**

    * `userId` (string, required): The user's email address or 'me' for the authenticated user. (default: "me")
    * `q` (string, optional): Search query to filter messages (e.g., 'from:[someone@example.com](mailto:someone@example.com) is:unread').
    * `maxResults` (integer, optional): Maximum number of messages to return (1-500). (default: 100)
    * `pageToken` (string, optional): Page token to retrieve a specific page of results.
    * `labelIds` (array, optional): Only return messages with labels that match all of the specified label IDs.
    * `includeSpamTrash` (boolean, optional): Include messages from SPAM and TRASH in the results. (default: false)
  </Accordion>

  <Accordion title="gmail/send_email">
    **Description:** Send an email.

    **Parameters:**

    * `to` (string, required): Recipient email address.
    * `subject` (string, required): Email subject line.
    * `body` (string, required): Email message content.
    * `userId` (string, optional): The user's email address or 'me' for the authenticated user. (default: "me")
    * `cc` (string, optional): CC email addresses (comma-separated).
    * `bcc` (string, optional): BCC email addresses (comma-separated).
    * `from` (string, optional): Sender email address (if different from authenticated user).
    * `replyTo` (string, optional): Reply-to email address.
    * `threadId` (string, optional): Thread ID if replying to an existing conversation.
  </Accordion>

  <Accordion title="gmail/delete_email">
    **Description:** Delete an email by ID.

    **Parameters:**

    * `userId` (string, required): The user's email address or 'me' for the authenticated user.
    * `id` (string, required): The ID of the message to delete.
  </Accordion>

  <Accordion title="gmail/create_draft">
    **Description:** Create a new draft email.

    **Parameters:**

    * `userId` (string, required): The user's email address or 'me' for the authenticated user.
    * `message` (object, required): Message object containing the draft content.
      * `raw` (string, required): Base64url encoded email message.
  </Accordion>

  <Accordion title="gmail/get_message">
    **Description:** Retrieve a specific message by ID.

    **Parameters:**

    * `userId` (string, required): The user's email address or 'me' for the authenticated user. (default: "me")
    * `id` (string, required): The ID of the message to retrieve.
    * `format` (string, optional): The format to return the message in. Options: "full", "metadata", "minimal", "raw". (default: "full")
    * `metadataHeaders` (array, optional): When given and format is METADATA, only include headers specified.
  </Accordion>

  <Accordion title="gmail/get_attachment">
    **Description:** Retrieve a message attachment.

    **Parameters:**

    * `userId` (string, required): The user's email address or 'me' for the authenticated user. (default: "me")
    * `messageId` (string, required): The ID of the message containing the attachment.
    * `id` (string, required): The ID of the attachment to retrieve.
  </Accordion>

  <Accordion title="gmail/fetch_thread">
    **Description:** Retrieve a specific email thread by ID.

    **Parameters:**

    * `userId` (string, required): The user's email address or 'me' for the authenticated user. (default: "me")
    * `id` (string, required): The ID of the thread to retrieve.
    * `format` (string, optional): The format to return the messages in. Options: "full", "metadata", "minimal". (default: "full")
    * `metadataHeaders` (array, optional): When given and format is METADATA, only include headers specified.
  </Accordion>

  <Accordion title="gmail/modify_thread">
    **Description:** Modify the labels applied to a thread.

    **Parameters:**

    * `userId` (string, required): The user's email address or 'me' for the authenticated user. (default: "me")
    * `id` (string, required): The ID of the thread to modify.
    * `addLabelIds` (array, optional): A list of IDs of labels to add to this thread.
    * `removeLabelIds` (array, optional): A list of IDs of labels to remove from this thread.
  </Accordion>

  <Accordion title="gmail/trash_thread">
    **Description:** Move a thread to the trash.

    **Parameters:**

    * `userId` (string, required): The user's email address or 'me' for the authenticated user. (default: "me")
    * `id` (string, required): The ID of the thread to trash.
  </Accordion>

  <Accordion title="gmail/untrash_thread">
    **Description:** Remove a thread from the trash.

    **Parameters:**

    * `userId` (string, required): The user's email address or 'me' for the authenticated user. (default: "me")
    * `id` (string, required): The ID of the thread to untrash.
  </Accordion>
</AccordionGroup>

## Usage Examples

### Basic Gmail Agent Setup
```

---

## Google Calendar Integration

**URL:** llms-txt#google-calendar-integration

**Contents:**
- Overview
- Prerequisites
- Setting Up Google Calendar Integration
  - 1. Connect Your Google Account
  - 2. Install Required Package
  - 3. Environment Variable Setup
- Available Actions
- Usage Examples
  - Basic Calendar Agent Setup

Source: https://docs.crewai.com/en/enterprise/integrations/google_calendar

Event and schedule management with Google Calendar integration for CrewAI.

Enable your agents to manage calendar events, schedules, and availability through Google Calendar. Create and update events, manage attendees, check availability, and streamline your scheduling workflows with AI-powered automation.

Before using the Google Calendar integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A Google account with Google Calendar access
* Connected your Google account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)

## Setting Up Google Calendar Integration

### 1. Connect Your Google Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Google Calendar** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for calendar access
5. Copy your Enterprise Token from [Integration Settings](https://app.crewai.com/crewai_plus/settings/integrations)

### 2. Install Required Package

### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>

Or add it to your `.env` file:

<AccordionGroup>
  <Accordion title="google_calendar/get_availability">
    **Description:** Get calendar availability (free/busy information).

* `timeMin` (string, required): Start time (RFC3339 format)
    * `timeMax` (string, required): End time (RFC3339 format)
    * `items` (array, required): Calendar IDs to check
      
    * `timeZone` (string, optional): Time zone used in the response. The default is UTC.
    * `groupExpansionMax` (integer, optional): Maximal number of calendar identifiers to be provided for a single group. Maximum: 100
    * `calendarExpansionMax` (integer, optional): Maximal number of calendars for which FreeBusy information is to be provided. Maximum: 50
  </Accordion>

<Accordion title="google_calendar/create_event">
    **Description:** Create a new event in the specified calendar.

* `calendarId` (string, required): Calendar ID (use 'primary' for main calendar)
    * `summary` (string, required): Event title/summary
    * `start_dateTime` (string, required): Start time in RFC3339 format (e.g., 2024-01-20T10:00:00-07:00)
    * `end_dateTime` (string, required): End time in RFC3339 format
    * `description` (string, optional): Event description
    * `timeZone` (string, optional): Time zone (e.g., America/Los\_Angeles)
    * `location` (string, optional): Geographic location of the event as free-form text.
    * `attendees` (array, optional): List of attendees for the event.
      
    * `reminders` (object, optional): Information about the event's reminders.
      
    * `conferenceData` (object, optional): The conference-related information, such as details of a Google Meet conference.
      
    * `visibility` (string, optional): Visibility of the event. Options: default, public, private, confidential. Default: default
    * `transparency` (string, optional): Whether the event blocks time on the calendar. Options: opaque, transparent. Default: opaque
  </Accordion>

<Accordion title="google_calendar/view_events">
    **Description:** Retrieve events for the specified calendar.

* `calendarId` (string, required): Calendar ID (use 'primary' for main calendar)
    * `timeMin` (string, optional): Lower bound for events (RFC3339)
    * `timeMax` (string, optional): Upper bound for events (RFC3339)
    * `maxResults` (integer, optional): Maximum number of events (default 10). Minimum: 1, Maximum: 2500
    * `orderBy` (string, optional): The order of the events returned in the result. Options: startTime, updated. Default: startTime
    * `singleEvents` (boolean, optional): Whether to expand recurring events into instances and only return single one-off events and instances of recurring events. Default: true
    * `showDeleted` (boolean, optional): Whether to include deleted events (with status equals cancelled) in the result. Default: false
    * `showHiddenInvitations` (boolean, optional): Whether to include hidden invitations in the result. Default: false
    * `q` (string, optional): Free text search terms to find events that match these terms in any field.
    * `pageToken` (string, optional): Token specifying which result page to return.
    * `timeZone` (string, optional): Time zone used in the response.
    * `updatedMin` (string, optional): Lower bound for an event's last modification time (RFC3339) to filter by.
    * `iCalUID` (string, optional): Specifies an event ID in the iCalendar format to be provided in the response.
  </Accordion>

<Accordion title="google_calendar/update_event">
    **Description:** Update an existing event.

* `calendarId` (string, required): Calendar ID
    * `eventId` (string, required): Event ID to update
    * `summary` (string, optional): Updated event title
    * `description` (string, optional): Updated event description
    * `start_dateTime` (string, optional): Updated start time
    * `end_dateTime` (string, optional): Updated end time
  </Accordion>

<Accordion title="google_calendar/delete_event">
    **Description:** Delete a specified event.

* `calendarId` (string, required): Calendar ID
    * `eventId` (string, required): Event ID to delete
  </Accordion>

<Accordion title="google_calendar/view_calendar_list">
    **Description:** Retrieve user's calendar list.

* `maxResults` (integer, optional): Maximum number of entries returned on one result page. Minimum: 1
    * `pageToken` (string, optional): Token specifying which result page to return.
    * `showDeleted` (boolean, optional): Whether to include deleted calendar list entries in the result. Default: false
    * `showHidden` (boolean, optional): Whether to show hidden entries. Default: false
    * `minAccessRole` (string, optional): The minimum access role for the user in the returned entries. Options: freeBusyReader, owner, reader, writer
  </Accordion>
</AccordionGroup>

### Basic Calendar Agent Setup

```python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

Example 3 (unknown):
```unknown
## Available Actions

<AccordionGroup>
  <Accordion title="google_calendar/get_availability">
    **Description:** Get calendar availability (free/busy information).

    **Parameters:**

    * `timeMin` (string, required): Start time (RFC3339 format)
    * `timeMax` (string, required): End time (RFC3339 format)
    * `items` (array, required): Calendar IDs to check
```

Example 4 (unknown):
```unknown
* `timeZone` (string, optional): Time zone used in the response. The default is UTC.
    * `groupExpansionMax` (integer, optional): Maximal number of calendar identifiers to be provided for a single group. Maximum: 100
    * `calendarExpansionMax` (integer, optional): Maximal number of calendars for which FreeBusy information is to be provided. Maximum: 50
  </Accordion>

  <Accordion title="google_calendar/create_event">
    **Description:** Create a new event in the specified calendar.

    **Parameters:**

    * `calendarId` (string, required): Calendar ID (use 'primary' for main calendar)
    * `summary` (string, required): Event title/summary
    * `start_dateTime` (string, required): Start time in RFC3339 format (e.g., 2024-01-20T10:00:00-07:00)
    * `end_dateTime` (string, required): End time in RFC3339 format
    * `description` (string, optional): Event description
    * `timeZone` (string, optional): Time zone (e.g., America/Los\_Angeles)
    * `location` (string, optional): Geographic location of the event as free-form text.
    * `attendees` (array, optional): List of attendees for the event.
```

---

## Google Contacts Integration

**URL:** llms-txt#google-contacts-integration

**Contents:**
- Overview
- Prerequisites
- Setting Up Google Contacts Integration
  - 1. Connect Your Google Account
  - 2. Install Required Package
  - 3. Environment Variable Setup
- Available Actions
- Usage Examples
  - Basic Google Contacts Agent Setup

Source: https://docs.crewai.com/en/enterprise/integrations/google_contacts

Contact and directory management with Google Contacts integration for CrewAI.

Enable your agents to manage contacts and directory information through Google Contacts. Access personal contacts, search directory people, create and update contact information, and manage contact groups with AI-powered automation.

Before using the Google Contacts integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A Google account with Google Contacts access
* Connected your Google account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)

## Setting Up Google Contacts Integration

### 1. Connect Your Google Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Google Contacts** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for contacts and directory access
5. Copy your Enterprise Token from [Integration Settings](https://app.crewai.com/crewai_plus/settings/integrations)

### 2. Install Required Package

### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>

Or add it to your `.env` file:

<AccordionGroup>
  <Accordion title="google_contacts/get_contacts">
    **Description:** Retrieve user's contacts from Google Contacts.

* `pageSize` (integer, optional): Number of contacts to return (max 1000). Minimum: 1, Maximum: 1000
    * `pageToken` (string, optional): The token of the page to retrieve.
    * `personFields` (string, optional): Fields to include (e.g., 'names,emailAddresses,phoneNumbers'). Default: names,emailAddresses,phoneNumbers
    * `requestSyncToken` (boolean, optional): Whether the response should include a sync token. Default: false
    * `sortOrder` (string, optional): The order in which the connections should be sorted. Options: LAST\_MODIFIED\_ASCENDING, LAST\_MODIFIED\_DESCENDING, FIRST\_NAME\_ASCENDING, LAST\_NAME\_ASCENDING
  </Accordion>

<Accordion title="google_contacts/search_contacts">
    **Description:** Search for contacts using a query string.

* `query` (string, required): Search query string
    * `readMask` (string, required): Fields to read (e.g., 'names,emailAddresses,phoneNumbers')
    * `pageSize` (integer, optional): Number of results to return. Minimum: 1, Maximum: 30
    * `pageToken` (string, optional): Token specifying which result page to return.
    * `sources` (array, optional): The sources to search in. Options: READ\_SOURCE\_TYPE\_CONTACT, READ\_SOURCE\_TYPE\_PROFILE. Default: READ\_SOURCE\_TYPE\_CONTACT
  </Accordion>

<Accordion title="google_contacts/list_directory_people">
    **Description:** List people in the authenticated user's directory.

* `sources` (array, required): Directory sources to search within. Options: DIRECTORY\_SOURCE\_TYPE\_DOMAIN\_PROFILE, DIRECTORY\_SOURCE\_TYPE\_DOMAIN\_CONTACT. Default: DIRECTORY\_SOURCE\_TYPE\_DOMAIN\_PROFILE
    * `pageSize` (integer, optional): Number of people to return. Minimum: 1, Maximum: 1000
    * `pageToken` (string, optional): Token specifying which result page to return.
    * `readMask` (string, optional): Fields to read (e.g., 'names,emailAddresses')
    * `requestSyncToken` (boolean, optional): Whether the response should include a sync token. Default: false
    * `mergeSources` (array, optional): Additional data to merge into the directory people responses. Options: CONTACT
  </Accordion>

<Accordion title="google_contacts/search_directory_people">
    **Description:** Search for people in the directory.

* `query` (string, required): Search query
    * `sources` (string, required): Directory sources (use 'DIRECTORY\_SOURCE\_TYPE\_DOMAIN\_PROFILE')
    * `pageSize` (integer, optional): Number of results to return
    * `readMask` (string, optional): Fields to read
  </Accordion>

<Accordion title="google_contacts/list_other_contacts">
    **Description:** List other contacts (not in user's personal contacts).

* `pageSize` (integer, optional): Number of contacts to return. Minimum: 1, Maximum: 1000
    * `pageToken` (string, optional): Token specifying which result page to return.
    * `readMask` (string, optional): Fields to read
    * `requestSyncToken` (boolean, optional): Whether the response should include a sync token. Default: false
  </Accordion>

<Accordion title="google_contacts/search_other_contacts">
    **Description:** Search other contacts.

* `query` (string, required): Search query
    * `readMask` (string, required): Fields to read (e.g., 'names,emailAddresses')
    * `pageSize` (integer, optional): Number of results
  </Accordion>

<Accordion title="google_contacts/get_person">
    **Description:** Get a single person's contact information by resource name.

* `resourceName` (string, required): The resource name of the person to get (e.g., 'people/c123456789')
    * `personFields` (string, optional): Fields to include (e.g., 'names,emailAddresses,phoneNumbers'). Default: names,emailAddresses,phoneNumbers
  </Accordion>

<Accordion title="google_contacts/create_contact">
    **Description:** Create a new contact in the user's address book.

* `names` (array, optional): Person's names
      
    * `emailAddresses` (array, optional): Email addresses
      
    * `phoneNumbers` (array, optional): Phone numbers
      
    * `addresses` (array, optional): Postal addresses
      
    * `organizations` (array, optional): Organizations/companies
      
  </Accordion>

<Accordion title="google_contacts/update_contact">
    **Description:** Update an existing contact's information.

* `resourceName` (string, required): The resource name of the person to update (e.g., 'people/c123456789')
    * `updatePersonFields` (string, required): Fields to update (e.g., 'names,emailAddresses,phoneNumbers')
    * `names` (array, optional): Person's names
    * `emailAddresses` (array, optional): Email addresses
    * `phoneNumbers` (array, optional): Phone numbers
  </Accordion>

<Accordion title="google_contacts/delete_contact">
    **Description:** Delete a contact from the user's address book.

* `resourceName` (string, required): The resource name of the person to delete (e.g., 'people/c123456789')
  </Accordion>

<Accordion title="google_contacts/batch_get_people">
    **Description:** Get information about multiple people in a single request.

* `resourceNames` (array, required): Resource names of people to get. Maximum: 200 items
    * `personFields` (string, optional): Fields to include (e.g., 'names,emailAddresses,phoneNumbers'). Default: names,emailAddresses,phoneNumbers
  </Accordion>

<Accordion title="google_contacts/list_contact_groups">
    **Description:** List the user's contact groups (labels).

* `pageSize` (integer, optional): Number of contact groups to return. Minimum: 1, Maximum: 1000
    * `pageToken` (string, optional): Token specifying which result page to return.
    * `groupFields` (string, optional): Fields to include (e.g., 'name,memberCount,clientData'). Default: name,memberCount
  </Accordion>
</AccordionGroup>

### Basic Google Contacts Agent Setup

```python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

Example 3 (unknown):
```unknown
## Available Actions

<AccordionGroup>
  <Accordion title="google_contacts/get_contacts">
    **Description:** Retrieve user's contacts from Google Contacts.

    **Parameters:**

    * `pageSize` (integer, optional): Number of contacts to return (max 1000). Minimum: 1, Maximum: 1000
    * `pageToken` (string, optional): The token of the page to retrieve.
    * `personFields` (string, optional): Fields to include (e.g., 'names,emailAddresses,phoneNumbers'). Default: names,emailAddresses,phoneNumbers
    * `requestSyncToken` (boolean, optional): Whether the response should include a sync token. Default: false
    * `sortOrder` (string, optional): The order in which the connections should be sorted. Options: LAST\_MODIFIED\_ASCENDING, LAST\_MODIFIED\_DESCENDING, FIRST\_NAME\_ASCENDING, LAST\_NAME\_ASCENDING
  </Accordion>

  <Accordion title="google_contacts/search_contacts">
    **Description:** Search for contacts using a query string.

    **Parameters:**

    * `query` (string, required): Search query string
    * `readMask` (string, required): Fields to read (e.g., 'names,emailAddresses,phoneNumbers')
    * `pageSize` (integer, optional): Number of results to return. Minimum: 1, Maximum: 30
    * `pageToken` (string, optional): Token specifying which result page to return.
    * `sources` (array, optional): The sources to search in. Options: READ\_SOURCE\_TYPE\_CONTACT, READ\_SOURCE\_TYPE\_PROFILE. Default: READ\_SOURCE\_TYPE\_CONTACT
  </Accordion>

  <Accordion title="google_contacts/list_directory_people">
    **Description:** List people in the authenticated user's directory.

    **Parameters:**

    * `sources` (array, required): Directory sources to search within. Options: DIRECTORY\_SOURCE\_TYPE\_DOMAIN\_PROFILE, DIRECTORY\_SOURCE\_TYPE\_DOMAIN\_CONTACT. Default: DIRECTORY\_SOURCE\_TYPE\_DOMAIN\_PROFILE
    * `pageSize` (integer, optional): Number of people to return. Minimum: 1, Maximum: 1000
    * `pageToken` (string, optional): Token specifying which result page to return.
    * `readMask` (string, optional): Fields to read (e.g., 'names,emailAddresses')
    * `requestSyncToken` (boolean, optional): Whether the response should include a sync token. Default: false
    * `mergeSources` (array, optional): Additional data to merge into the directory people responses. Options: CONTACT
  </Accordion>

  <Accordion title="google_contacts/search_directory_people">
    **Description:** Search for people in the directory.

    **Parameters:**

    * `query` (string, required): Search query
    * `sources` (string, required): Directory sources (use 'DIRECTORY\_SOURCE\_TYPE\_DOMAIN\_PROFILE')
    * `pageSize` (integer, optional): Number of results to return
    * `readMask` (string, optional): Fields to read
  </Accordion>

  <Accordion title="google_contacts/list_other_contacts">
    **Description:** List other contacts (not in user's personal contacts).

    **Parameters:**

    * `pageSize` (integer, optional): Number of contacts to return. Minimum: 1, Maximum: 1000
    * `pageToken` (string, optional): Token specifying which result page to return.
    * `readMask` (string, optional): Fields to read
    * `requestSyncToken` (boolean, optional): Whether the response should include a sync token. Default: false
  </Accordion>

  <Accordion title="google_contacts/search_other_contacts">
    **Description:** Search other contacts.

    **Parameters:**

    * `query` (string, required): Search query
    * `readMask` (string, required): Fields to read (e.g., 'names,emailAddresses')
    * `pageSize` (integer, optional): Number of results
  </Accordion>

  <Accordion title="google_contacts/get_person">
    **Description:** Get a single person's contact information by resource name.

    **Parameters:**

    * `resourceName` (string, required): The resource name of the person to get (e.g., 'people/c123456789')
    * `personFields` (string, optional): Fields to include (e.g., 'names,emailAddresses,phoneNumbers'). Default: names,emailAddresses,phoneNumbers
  </Accordion>

  <Accordion title="google_contacts/create_contact">
    **Description:** Create a new contact in the user's address book.

    **Parameters:**

    * `names` (array, optional): Person's names
```

Example 4 (unknown):
```unknown
* `emailAddresses` (array, optional): Email addresses
```

---

## Google Docs Integration

**URL:** llms-txt#google-docs-integration

**Contents:**
- Overview
- Prerequisites
- Setting Up Google Docs Integration
  - 1. Connect Your Google Account
  - 2. Install Required Package
  - 3. Environment Variable Setup
- Available Actions
- Usage Examples
  - Basic Google Docs Agent Setup

Source: https://docs.crewai.com/en/enterprise/integrations/google_docs

Document creation and editing with Google Docs integration for CrewAI.

Enable your agents to create, edit, and manage Google Docs documents with text manipulation and formatting. Automate document creation, insert and replace text, manage content ranges, and streamline your document workflows with AI-powered automation.

Before using the Google Docs integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A Google account with Google Docs access
* Connected your Google account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)

## Setting Up Google Docs Integration

### 1. Connect Your Google Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Google Docs** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for document access
5. Copy your Enterprise Token from [Integration Settings](https://app.crewai.com/crewai_plus/settings/integrations)

### 2. Install Required Package

### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>

Or add it to your `.env` file:

<AccordionGroup>
  <Accordion title="google_docs/create_document">
    **Description:** Create a new Google Document.

* `title` (string, optional): The title for the new document.
  </Accordion>

<Accordion title="google_docs/get_document">
    **Description:** Get the contents and metadata of a Google Document.

* `documentId` (string, required): The ID of the document to retrieve.
    * `includeTabsContent` (boolean, optional): Whether to include tab content. Default is `false`.
    * `suggestionsViewMode` (string, optional): The suggestions view mode to apply to the document. Enum: `DEFAULT_FOR_CURRENT_ACCESS`, `PREVIEW_SUGGESTIONS_ACCEPTED`, `PREVIEW_WITHOUT_SUGGESTIONS`. Default is `DEFAULT_FOR_CURRENT_ACCESS`.
  </Accordion>

<Accordion title="google_docs/batch_update">
    **Description:** Apply one or more updates to a Google Document.

* `documentId` (string, required): The ID of the document to update.
    * `requests` (array, required): A list of updates to apply to the document. Each item is an object representing a request.
    * `writeControl` (object, optional): Provides control over how write requests are executed. Contains `requiredRevisionId` (string) and `targetRevisionId` (string).
  </Accordion>

<Accordion title="google_docs/insert_text">
    **Description:** Insert text into a Google Document at a specific location.

* `documentId` (string, required): The ID of the document to update.
    * `text` (string, required): The text to insert.
    * `index` (integer, optional): The zero-based index where to insert the text. Default is `1`.
  </Accordion>

<Accordion title="google_docs/replace_text">
    **Description:** Replace all instances of text in a Google Document.

* `documentId` (string, required): The ID of the document to update.
    * `containsText` (string, required): The text to find and replace.
    * `replaceText` (string, required): The text to replace it with.
    * `matchCase` (boolean, optional): Whether the search should respect case. Default is `false`.
  </Accordion>

<Accordion title="google_docs/delete_content_range">
    **Description:** Delete content from a specific range in a Google Document.

* `documentId` (string, required): The ID of the document to update.
    * `startIndex` (integer, required): The start index of the range to delete.
    * `endIndex` (integer, required): The end index of the range to delete.
  </Accordion>

<Accordion title="google_docs/insert_page_break">
    **Description:** Insert a page break at a specific location in a Google Document.

* `documentId` (string, required): The ID of the document to update.
    * `index` (integer, optional): The zero-based index where to insert the page break. Default is `1`.
  </Accordion>

<Accordion title="google_docs/create_named_range">
    **Description:** Create a named range in a Google Document.

* `documentId` (string, required): The ID of the document to update.
    * `name` (string, required): The name for the named range.
    * `startIndex` (integer, required): The start index of the range.
    * `endIndex` (integer, required): The end index of the range.
  </Accordion>
</AccordionGroup>

### Basic Google Docs Agent Setup

```python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

Example 3 (unknown):
```unknown
## Available Actions

<AccordionGroup>
  <Accordion title="google_docs/create_document">
    **Description:** Create a new Google Document.

    **Parameters:**

    * `title` (string, optional): The title for the new document.
  </Accordion>

  <Accordion title="google_docs/get_document">
    **Description:** Get the contents and metadata of a Google Document.

    **Parameters:**

    * `documentId` (string, required): The ID of the document to retrieve.
    * `includeTabsContent` (boolean, optional): Whether to include tab content. Default is `false`.
    * `suggestionsViewMode` (string, optional): The suggestions view mode to apply to the document. Enum: `DEFAULT_FOR_CURRENT_ACCESS`, `PREVIEW_SUGGESTIONS_ACCEPTED`, `PREVIEW_WITHOUT_SUGGESTIONS`. Default is `DEFAULT_FOR_CURRENT_ACCESS`.
  </Accordion>

  <Accordion title="google_docs/batch_update">
    **Description:** Apply one or more updates to a Google Document.

    **Parameters:**

    * `documentId` (string, required): The ID of the document to update.
    * `requests` (array, required): A list of updates to apply to the document. Each item is an object representing a request.
    * `writeControl` (object, optional): Provides control over how write requests are executed. Contains `requiredRevisionId` (string) and `targetRevisionId` (string).
  </Accordion>

  <Accordion title="google_docs/insert_text">
    **Description:** Insert text into a Google Document at a specific location.

    **Parameters:**

    * `documentId` (string, required): The ID of the document to update.
    * `text` (string, required): The text to insert.
    * `index` (integer, optional): The zero-based index where to insert the text. Default is `1`.
  </Accordion>

  <Accordion title="google_docs/replace_text">
    **Description:** Replace all instances of text in a Google Document.

    **Parameters:**

    * `documentId` (string, required): The ID of the document to update.
    * `containsText` (string, required): The text to find and replace.
    * `replaceText` (string, required): The text to replace it with.
    * `matchCase` (boolean, optional): Whether the search should respect case. Default is `false`.
  </Accordion>

  <Accordion title="google_docs/delete_content_range">
    **Description:** Delete content from a specific range in a Google Document.

    **Parameters:**

    * `documentId` (string, required): The ID of the document to update.
    * `startIndex` (integer, required): The start index of the range to delete.
    * `endIndex` (integer, required): The end index of the range to delete.
  </Accordion>

  <Accordion title="google_docs/insert_page_break">
    **Description:** Insert a page break at a specific location in a Google Document.

    **Parameters:**

    * `documentId` (string, required): The ID of the document to update.
    * `index` (integer, optional): The zero-based index where to insert the page break. Default is `1`.
  </Accordion>

  <Accordion title="google_docs/create_named_range">
    **Description:** Create a named range in a Google Document.

    **Parameters:**

    * `documentId` (string, required): The ID of the document to update.
    * `name` (string, required): The name for the named range.
    * `startIndex` (integer, required): The start index of the range.
    * `endIndex` (integer, required): The end index of the range.
  </Accordion>
</AccordionGroup>

## Usage Examples

### Basic Google Docs Agent Setup
```

---

## Google Drive Integration

**URL:** llms-txt#google-drive-integration

**Contents:**
- Overview
- Prerequisites
- Setting Up Google Drive Integration
  - 1. Connect Your Google Account
  - 2. Install Required Package
  - 3. Environment Variable Setup
- Available Actions
- Usage Examples
  - Basic Google Drive Agent Setup

Source: https://docs.crewai.com/en/enterprise/integrations/google_drive

File storage and management with Google Drive integration for CrewAI.

Enable your agents to manage files and folders through Google Drive. Upload, download, organize, and share files, create folders, and streamline your document management workflows with AI-powered automation.

Before using the Google Drive integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A Google account with Google Drive access
* Connected your Google account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)

## Setting Up Google Drive Integration

### 1. Connect Your Google Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Google Drive** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for file and folder management
5. Copy your Enterprise Token from [Integration Settings](https://app.crewai.com/crewai_plus/settings/integrations)

### 2. Install Required Package

### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>

Or add it to your `.env` file:

<AccordionGroup>
  <Accordion title="google_drive/get_file">
    **Description:** Get a file by ID from Google Drive.

* `file_id` (string, required): The ID of the file to retrieve.
  </Accordion>

<Accordion title="google_drive/list_files">
    **Description:** List files in Google Drive.

* `q` (string, optional): Query string to filter files (example: "name contains 'report'").
    * `page_size` (integer, optional): Maximum number of files to return (default: 100, max: 1000).
    * `page_token` (string, optional): Token for retrieving the next page of results.
    * `order_by` (string, optional): Sort order (example: "name", "createdTime desc", "modifiedTime").
    * `spaces` (string, optional): Comma-separated list of spaces to query (drive, appDataFolder, photos).
  </Accordion>

<Accordion title="google_drive/upload_file">
    **Description:** Upload a file to Google Drive.

* `name` (string, required): Name of the file to create.
    * `content` (string, required): Content of the file to upload.
    * `mime_type` (string, optional): MIME type of the file (example: "text/plain", "application/pdf").
    * `parent_folder_id` (string, optional): ID of the parent folder where the file should be created.
    * `description` (string, optional): Description of the file.
  </Accordion>

<Accordion title="google_drive/download_file">
    **Description:** Download a file from Google Drive.

* `file_id` (string, required): The ID of the file to download.
    * `mime_type` (string, optional): MIME type for export (required for Google Workspace documents).
  </Accordion>

<Accordion title="google_drive/create_folder">
    **Description:** Create a new folder in Google Drive.

* `name` (string, required): Name of the folder to create.
    * `parent_folder_id` (string, optional): ID of the parent folder where the new folder should be created.
    * `description` (string, optional): Description of the folder.
  </Accordion>

<Accordion title="google_drive/delete_file">
    **Description:** Delete a file from Google Drive.

* `file_id` (string, required): The ID of the file to delete.
  </Accordion>

<Accordion title="google_drive/share_file">
    **Description:** Share a file in Google Drive with specific users or make it public.

* `file_id` (string, required): The ID of the file to share.
    * `role` (string, required): The role granted by this permission (reader, writer, commenter, owner).
    * `type` (string, required): The type of the grantee (user, group, domain, anyone).
    * `email_address` (string, optional): The email address of the user or group to share with (required for user/group types).
    * `domain` (string, optional): The domain to share with (required for domain type).
    * `send_notification_email` (boolean, optional): Whether to send a notification email (default: true).
    * `email_message` (string, optional): A plain text custom message to include in the notification email.
  </Accordion>

<Accordion title="google_drive/update_file">
    **Description:** Update an existing file in Google Drive.

* `file_id` (string, required): The ID of the file to update.
    * `name` (string, optional): New name for the file.
    * `content` (string, optional): New content for the file.
    * `mime_type` (string, optional): New MIME type for the file.
    * `description` (string, optional): New description for the file.
    * `add_parents` (string, optional): Comma-separated list of parent folder IDs to add.
    * `remove_parents` (string, optional): Comma-separated list of parent folder IDs to remove.
  </Accordion>
</AccordionGroup>

### Basic Google Drive Agent Setup

```python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

Example 3 (unknown):
```unknown
## Available Actions

<AccordionGroup>
  <Accordion title="google_drive/get_file">
    **Description:** Get a file by ID from Google Drive.

    **Parameters:**

    * `file_id` (string, required): The ID of the file to retrieve.
  </Accordion>

  <Accordion title="google_drive/list_files">
    **Description:** List files in Google Drive.

    **Parameters:**

    * `q` (string, optional): Query string to filter files (example: "name contains 'report'").
    * `page_size` (integer, optional): Maximum number of files to return (default: 100, max: 1000).
    * `page_token` (string, optional): Token for retrieving the next page of results.
    * `order_by` (string, optional): Sort order (example: "name", "createdTime desc", "modifiedTime").
    * `spaces` (string, optional): Comma-separated list of spaces to query (drive, appDataFolder, photos).
  </Accordion>

  <Accordion title="google_drive/upload_file">
    **Description:** Upload a file to Google Drive.

    **Parameters:**

    * `name` (string, required): Name of the file to create.
    * `content` (string, required): Content of the file to upload.
    * `mime_type` (string, optional): MIME type of the file (example: "text/plain", "application/pdf").
    * `parent_folder_id` (string, optional): ID of the parent folder where the file should be created.
    * `description` (string, optional): Description of the file.
  </Accordion>

  <Accordion title="google_drive/download_file">
    **Description:** Download a file from Google Drive.

    **Parameters:**

    * `file_id` (string, required): The ID of the file to download.
    * `mime_type` (string, optional): MIME type for export (required for Google Workspace documents).
  </Accordion>

  <Accordion title="google_drive/create_folder">
    **Description:** Create a new folder in Google Drive.

    **Parameters:**

    * `name` (string, required): Name of the folder to create.
    * `parent_folder_id` (string, optional): ID of the parent folder where the new folder should be created.
    * `description` (string, optional): Description of the folder.
  </Accordion>

  <Accordion title="google_drive/delete_file">
    **Description:** Delete a file from Google Drive.

    **Parameters:**

    * `file_id` (string, required): The ID of the file to delete.
  </Accordion>

  <Accordion title="google_drive/share_file">
    **Description:** Share a file in Google Drive with specific users or make it public.

    **Parameters:**

    * `file_id` (string, required): The ID of the file to share.
    * `role` (string, required): The role granted by this permission (reader, writer, commenter, owner).
    * `type` (string, required): The type of the grantee (user, group, domain, anyone).
    * `email_address` (string, optional): The email address of the user or group to share with (required for user/group types).
    * `domain` (string, optional): The domain to share with (required for domain type).
    * `send_notification_email` (boolean, optional): Whether to send a notification email (default: true).
    * `email_message` (string, optional): A plain text custom message to include in the notification email.
  </Accordion>

  <Accordion title="google_drive/update_file">
    **Description:** Update an existing file in Google Drive.

    **Parameters:**

    * `file_id` (string, required): The ID of the file to update.
    * `name` (string, optional): New name for the file.
    * `content` (string, optional): New content for the file.
    * `mime_type` (string, optional): New MIME type for the file.
    * `description` (string, optional): New description for the file.
    * `add_parents` (string, optional): Comma-separated list of parent folder IDs to add.
    * `remove_parents` (string, optional): Comma-separated list of parent folder IDs to remove.
  </Accordion>
</AccordionGroup>

## Usage Examples

### Basic Google Drive Agent Setup
```

---

## Google Sheets Integration

**URL:** llms-txt#google-sheets-integration

**Contents:**
- Overview
- Prerequisites
- Setting Up Google Sheets Integration
  - 1. Connect Your Google Account
  - 2. Install Required Package
  - 3. Environment Variable Setup
- Available Actions
- Usage Examples
  - Basic Google Sheets Agent Setup

Source: https://docs.crewai.com/en/enterprise/integrations/google_sheets

Spreadsheet data synchronization with Google Sheets integration for CrewAI.

Enable your agents to manage spreadsheet data through Google Sheets. Read rows, create new entries, update existing data, and streamline your data management workflows with AI-powered automation. Perfect for data tracking, reporting, and collaborative data management.

Before using the Google Sheets integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A Google account with Google Sheets access
* Connected your Google account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)
* Spreadsheets with proper column headers for data operations

## Setting Up Google Sheets Integration

### 1. Connect Your Google Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Google Sheets** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for spreadsheet access
5. Copy your Enterprise Token from [Integration Settings](https://app.crewai.com/crewai_plus/settings/integrations)

### 2. Install Required Package

### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>

Or add it to your `.env` file:

<AccordionGroup>
  <Accordion title="google_sheets/get_spreadsheet">
    **Description:** Retrieve properties and data of a spreadsheet.

* `spreadsheetId` (string, required): The ID of the spreadsheet to retrieve.
    * `ranges` (array, optional): The ranges to retrieve from the spreadsheet.
    * `includeGridData` (boolean, optional): True if grid data should be returned. Default: false
    * `fields` (string, optional): The fields to include in the response. Use this to improve performance by only returning needed data.
  </Accordion>

<Accordion title="google_sheets/get_values">
    **Description:** Returns a range of values from a spreadsheet.

* `spreadsheetId` (string, required): The ID of the spreadsheet to retrieve data from.
    * `range` (string, required): The A1 notation or R1C1 notation of the range to retrieve values from.
    * `valueRenderOption` (string, optional): How values should be represented in the output. Options: FORMATTED\_VALUE, UNFORMATTED\_VALUE, FORMULA. Default: FORMATTED\_VALUE
    * `dateTimeRenderOption` (string, optional): How dates, times, and durations should be represented in the output. Options: SERIAL\_NUMBER, FORMATTED\_STRING. Default: SERIAL\_NUMBER
    * `majorDimension` (string, optional): The major dimension that results should use. Options: ROWS, COLUMNS. Default: ROWS
  </Accordion>

<Accordion title="google_sheets/update_values">
    **Description:** Sets values in a range of a spreadsheet.

* `spreadsheetId` (string, required): The ID of the spreadsheet to update.
    * `range` (string, required): The A1 notation of the range to update.
    * `values` (array, required): The data to be written. Each array represents a row.
      
    * `valueInputOption` (string, optional): How the input data should be interpreted. Options: RAW, USER\_ENTERED. Default: USER\_ENTERED
  </Accordion>

<Accordion title="google_sheets/append_values">
    **Description:** Appends values to a spreadsheet.

* `spreadsheetId` (string, required): The ID of the spreadsheet to update.
    * `range` (string, required): The A1 notation of a range to search for a logical table of data.
    * `values` (array, required): The data to append. Each array represents a row.
      
    * `valueInputOption` (string, optional): How the input data should be interpreted. Options: RAW, USER\_ENTERED. Default: USER\_ENTERED
    * `insertDataOption` (string, optional): How the input data should be inserted. Options: OVERWRITE, INSERT\_ROWS. Default: INSERT\_ROWS
  </Accordion>

<Accordion title="google_sheets/create_spreadsheet">
    **Description:** Creates a new spreadsheet.

* `title` (string, required): The title of the new spreadsheet.
    * `sheets` (array, optional): The sheets that are part of the spreadsheet.
      
  </Accordion>
</AccordionGroup>

### Basic Google Sheets Agent Setup

```python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

Example 3 (unknown):
```unknown
## Available Actions

<AccordionGroup>
  <Accordion title="google_sheets/get_spreadsheet">
    **Description:** Retrieve properties and data of a spreadsheet.

    **Parameters:**

    * `spreadsheetId` (string, required): The ID of the spreadsheet to retrieve.
    * `ranges` (array, optional): The ranges to retrieve from the spreadsheet.
    * `includeGridData` (boolean, optional): True if grid data should be returned. Default: false
    * `fields` (string, optional): The fields to include in the response. Use this to improve performance by only returning needed data.
  </Accordion>

  <Accordion title="google_sheets/get_values">
    **Description:** Returns a range of values from a spreadsheet.

    **Parameters:**

    * `spreadsheetId` (string, required): The ID of the spreadsheet to retrieve data from.
    * `range` (string, required): The A1 notation or R1C1 notation of the range to retrieve values from.
    * `valueRenderOption` (string, optional): How values should be represented in the output. Options: FORMATTED\_VALUE, UNFORMATTED\_VALUE, FORMULA. Default: FORMATTED\_VALUE
    * `dateTimeRenderOption` (string, optional): How dates, times, and durations should be represented in the output. Options: SERIAL\_NUMBER, FORMATTED\_STRING. Default: SERIAL\_NUMBER
    * `majorDimension` (string, optional): The major dimension that results should use. Options: ROWS, COLUMNS. Default: ROWS
  </Accordion>

  <Accordion title="google_sheets/update_values">
    **Description:** Sets values in a range of a spreadsheet.

    **Parameters:**

    * `spreadsheetId` (string, required): The ID of the spreadsheet to update.
    * `range` (string, required): The A1 notation of the range to update.
    * `values` (array, required): The data to be written. Each array represents a row.
```

Example 4 (unknown):
```unknown
* `valueInputOption` (string, optional): How the input data should be interpreted. Options: RAW, USER\_ENTERED. Default: USER\_ENTERED
  </Accordion>

  <Accordion title="google_sheets/append_values">
    **Description:** Appends values to a spreadsheet.

    **Parameters:**

    * `spreadsheetId` (string, required): The ID of the spreadsheet to update.
    * `range` (string, required): The A1 notation of a range to search for a logical table of data.
    * `values` (array, required): The data to append. Each array represents a row.
```

---

## Google Slides Integration

**URL:** llms-txt#google-slides-integration

**Contents:**
- Overview
- Prerequisites
- Setting Up Google Slides Integration
  - 1. Connect Your Google Account
  - 2. Install Required Package
  - 3. Environment Variable Setup
- Available Actions
- Usage Examples
  - Basic Google Slides Agent Setup

Source: https://docs.crewai.com/en/enterprise/integrations/google_slides

Presentation creation and management with Google Slides integration for CrewAI.

Enable your agents to create, edit, and manage Google Slides presentations. Create presentations, update content, import data from Google Sheets, manage pages and thumbnails, and streamline your presentation workflows with AI-powered automation.

Before using the Google Slides integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A Google account with Google Slides access
* Connected your Google account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)

## Setting Up Google Slides Integration

### 1. Connect Your Google Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Google Slides** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for presentations, spreadsheets, and drive access
5. Copy your Enterprise Token from [Integration Settings](https://app.crewai.com/crewai_plus/settings/integrations)

### 2. Install Required Package

### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>

Or add it to your `.env` file:

<AccordionGroup>
  <Accordion title="google_slides/create_blank_presentation">
    **Description:** Creates a blank presentation with no content.

* `title` (string, required): The title of the presentation.
  </Accordion>

<Accordion title="google_slides/get_presentation">
    **Description:** Retrieves a presentation by ID.

* `presentationId` (string, required): The ID of the presentation to retrieve.
    * `fields` (string, optional): The fields to include in the response. Use this to improve performance by only returning needed data.
  </Accordion>

<Accordion title="google_slides/batch_update_presentation">
    **Description:** Applies updates, add content, or remove content from a presentation.

* `presentationId` (string, required): The ID of the presentation to update.
    * `requests` (array, required): A list of updates to apply to the presentation.
      
    * `writeControl` (object, optional): Provides control over how write requests are executed.
      
  </Accordion>

<Accordion title="google_slides/get_page">
    **Description:** Retrieves a specific page by its ID.

* `presentationId` (string, required): The ID of the presentation.
    * `pageObjectId` (string, required): The ID of the page to retrieve.
  </Accordion>

<Accordion title="google_slides/get_thumbnail">
    **Description:** Generates a page thumbnail.

* `presentationId` (string, required): The ID of the presentation.
    * `pageObjectId` (string, required): The ID of the page for thumbnail generation.
  </Accordion>

<Accordion title="google_slides/import_data_from_sheet">
    **Description:** Imports data from a Google Sheet into a presentation.

* `presentationId` (string, required): The ID of the presentation.
    * `sheetId` (string, required): The ID of the Google Sheet to import from.
    * `dataRange` (string, required): The range of data to import from the sheet.
  </Accordion>

<Accordion title="google_slides/upload_file_to_drive">
    **Description:** Uploads a file to Google Drive associated with the presentation.

* `file` (string, required): The file data to upload.
    * `presentationId` (string, required): The ID of the presentation to link the uploaded file.
  </Accordion>

<Accordion title="google_slides/link_file_to_presentation">
    **Description:** Links a file in Google Drive to a presentation.

* `presentationId` (string, required): The ID of the presentation.
    * `fileId` (string, required): The ID of the file to link.
  </Accordion>

<Accordion title="google_slides/get_all_presentations">
    **Description:** Lists all presentations accessible to the user.

* `pageSize` (integer, optional): The number of presentations to return per page.
    * `pageToken` (string, optional): A token for pagination.
  </Accordion>

<Accordion title="google_slides/delete_presentation">
    **Description:** Deletes a presentation by ID.

* `presentationId` (string, required): The ID of the presentation to delete.
  </Accordion>
</AccordionGroup>

### Basic Google Slides Agent Setup

```python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

Example 3 (unknown):
```unknown
## Available Actions

<AccordionGroup>
  <Accordion title="google_slides/create_blank_presentation">
    **Description:** Creates a blank presentation with no content.

    **Parameters:**

    * `title` (string, required): The title of the presentation.
  </Accordion>

  <Accordion title="google_slides/get_presentation">
    **Description:** Retrieves a presentation by ID.

    **Parameters:**

    * `presentationId` (string, required): The ID of the presentation to retrieve.
    * `fields` (string, optional): The fields to include in the response. Use this to improve performance by only returning needed data.
  </Accordion>

  <Accordion title="google_slides/batch_update_presentation">
    **Description:** Applies updates, add content, or remove content from a presentation.

    **Parameters:**

    * `presentationId` (string, required): The ID of the presentation to update.
    * `requests` (array, required): A list of updates to apply to the presentation.
```

Example 4 (unknown):
```unknown
* `writeControl` (object, optional): Provides control over how write requests are executed.
```

---

## Hierarchical crew

**URL:** llms-txt#hierarchical-crew

**Contents:**
- Best Practices for Collaboration
  - 1. **Clear Role Definition**

crew = Crew(
    agents=[manager, researcher, writer],
    tasks=[project_task],
    process=Process.hierarchical,  # Manager coordinates everything
    manager_llm="gpt-4o",  # Specify LLM for manager
    verbose=True
)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## Best Practices for Collaboration

### 1. **Clear Role Definition**
```

---

## HubSpot Integration

**URL:** llms-txt#hubspot-integration

**Contents:**
- Overview
- Prerequisites
- Setting Up HubSpot Integration
  - 1. Connect Your HubSpot Account
  - 2. Install Required Package
  - 3. Environment Variable Setup
- Available Actions
- Usage Examples
  - Basic HubSpot Agent Setup

Source: https://docs.crewai.com/en/enterprise/integrations/hubspot

Manage companies and contacts in HubSpot with CrewAI.

Enable your agents to manage companies and contacts within HubSpot. Create new records and streamline your CRM processes with AI-powered automation.

Before using the HubSpot integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription.
* A HubSpot account with appropriate permissions.
* Connected your HubSpot account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors).

## Setting Up HubSpot Integration

### 1. Connect Your HubSpot Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors).
2. Find **HubSpot** in the Authentication Integrations section.
3. Click **Connect** and complete the OAuth flow.
4. Grant the necessary permissions for company and contact management.
5. Copy your Enterprise Token from [Integration Settings](https://app.crewai.com/crewai_plus/settings/integrations)

### 2. Install Required Package

### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>

Or add it to your `.env` file:

<AccordionGroup>
  <Accordion title="hubspot/create_company">
    **Description:** Create a new company record in HubSpot.

* `name` (string, required): Name of the company.
    * `domain` (string, optional): Company Domain Name.
    * `industry` (string, optional): Industry. Must be one of the predefined values from HubSpot.
    * `phone` (string, optional): Phone Number.
    * `hubspot_owner_id` (string, optional): Company owner ID.
    * `type` (string, optional): Type of the company. Available values: `PROSPECT`, `PARTNER`, `RESELLER`, `VENDOR`, `OTHER`.
    * `city` (string, optional): City.
    * `state` (string, optional): State/Region.
    * `zip` (string, optional): Postal Code.
    * `numberofemployees` (number, optional): Number of Employees.
    * `annualrevenue` (number, optional): Annual Revenue.
    * `timezone` (string, optional): Time Zone.
    * `description` (string, optional): Description.
    * `linkedin_company_page` (string, optional): LinkedIn Company Page URL.
    * `company_email` (string, optional): Company Email.
    * `first_name` (string, optional): First Name of a contact at the company.
    * `last_name` (string, optional): Last Name of a contact at the company.
    * `about_us` (string, optional): About Us.
    * `hs_csm_sentiment` (string, optional): CSM Sentiment. Available values: `at_risk`, `neutral`, `healthy`.
    * `closedate` (string, optional): Close Date.
    * `hs_keywords` (string, optional): Company Keywords. Must be one of the predefined values.
    * `country` (string, optional): Country/Region.
    * `hs_country_code` (string, optional): Country/Region Code.
    * `hs_employee_range` (string, optional): Employee range.
    * `facebook_company_page` (string, optional): Facebook Company Page URL.
    * `facebookfans` (number, optional): Number of Facebook Fans.
    * `hs_gps_coordinates` (string, optional): GPS Coordinates.
    * `hs_gps_error` (string, optional): GPS Error.
    * `googleplus_page` (string, optional): Google Plus Page URL.
    * `owneremail` (string, optional): HubSpot Owner Email.
    * `ownername` (string, optional): HubSpot Owner Name.
    * `hs_ideal_customer_profile` (string, optional): Ideal Customer Profile Tier. Available values: `tier_1`, `tier_2`, `tier_3`.
    * `hs_industry_group` (string, optional): Industry group.
    * `is_public` (boolean, optional): Is Public.
    * `hs_last_metered_enrichment_timestamp` (string, optional): Last Metered Enrichment Timestamp.
    * `hs_lead_status` (string, optional): Lead Status. Available values: `NEW`, `OPEN`, `IN_PROGRESS`, `OPEN_DEAL`, `UNQUALIFIED`, `ATTEMPTED_TO_CONTACT`, `CONNECTED`, `BAD_TIMING`.
    * `lifecyclestage` (string, optional): Lifecycle Stage. Available values: `subscriber`, `lead`, `marketingqualifiedlead`, `salesqualifiedlead`, `opportunity`, `customer`, `evangelist`, `other`.
    * `linkedinbio` (string, optional): LinkedIn Bio.
    * `hs_linkedin_handle` (string, optional): LinkedIn handle.
    * `hs_live_enrichment_deadline` (string, optional): Live enrichment deadline.
    * `hs_logo_url` (string, optional): Logo URL.
    * `hs_analytics_source` (string, optional): Original Traffic Source.
    * `hs_pinned_engagement_id` (number, optional): Pinned Engagement ID.
    * `hs_quick_context` (string, optional): Quick context.
    * `hs_revenue_range` (string, optional): Revenue range.
    * `hs_state_code` (string, optional): State/Region Code.
    * `address` (string, optional): Street Address.
    * `address2` (string, optional): Street Address 2.
    * `hs_is_target_account` (boolean, optional): Target Account.
    * `hs_target_account` (string, optional): Target Account Tier. Available values: `tier_1`, `tier_2`, `tier_3`.
    * `hs_target_account_recommendation_snooze_time` (string, optional): Target Account Recommendation Snooze Time.
    * `hs_target_account_recommendation_state` (string, optional): Target Account Recommendation State. Available values: `DISMISSED`, `NONE`, `SNOOZED`.
    * `total_money_raised` (string, optional): Total Money Raised.
    * `twitterbio` (string, optional): Twitter Bio.
    * `twitterfollowers` (number, optional): Twitter Followers.
    * `twitterhandle` (string, optional): Twitter Handle.
    * `web_technologies` (string, optional): Web Technologies used. Must be one of the predefined values.
    * `website` (string, optional): Website URL.
    * `founded_year` (string, optional): Year Founded.
  </Accordion>

<Accordion title="hubspot/create_contact">
    **Description:** Create a new contact record in HubSpot.

* `email` (string, required): Email address of the contact.
    * `firstname` (string, optional): First Name.
    * `lastname` (string, optional): Last Name.
    * `phone` (string, optional): Phone Number.
    * `hubspot_owner_id` (string, optional): Contact owner.
    * `lifecyclestage` (string, optional): Lifecycle Stage. Available values: `subscriber`, `lead`, `marketingqualifiedlead`, `salesqualifiedlead`, `opportunity`, `customer`, `evangelist`, `other`.
    * `hs_lead_status` (string, optional): Lead Status. Available values: `NEW`, `OPEN`, `IN_PROGRESS`, `OPEN_DEAL`, `UNQUALIFIED`, `ATTEMPTED_TO_CONTACT`, `CONNECTED`, `BAD_TIMING`.
    * `annualrevenue` (string, optional): Annual Revenue.
    * `hs_buying_role` (string, optional): Buying Role.
    * `cc_emails` (string, optional): CC Emails.
    * `ch_customer_id` (string, optional): Chargify Customer ID.
    * `ch_customer_reference` (string, optional): Chargify Customer Reference.
    * `chargify_sites` (string, optional): Chargify Site(s).
    * `city` (string, optional): City.
    * `hs_facebook_ad_clicked` (boolean, optional): Clicked Facebook ad.
    * `hs_linkedin_ad_clicked` (string, optional): Clicked LinkedIn Ad.
    * `hs_clicked_linkedin_ad` (string, optional): Clicked on a LinkedIn Ad.
    * `closedate` (string, optional): Close Date.
    * `company` (string, optional): Company Name.
    * `company_size` (string, optional): Company size.
    * `country` (string, optional): Country/Region.
    * `hs_country_region_code` (string, optional): Country/Region Code.
    * `date_of_birth` (string, optional): Date of birth.
    * `degree` (string, optional): Degree.
    * `hs_email_customer_quarantined_reason` (string, optional): Email address quarantine reason.
    * `hs_role` (string, optional): Employment Role. Must be one of the predefined values.
    * `hs_seniority` (string, optional): Employment Seniority. Must be one of the predefined values.
    * `hs_sub_role` (string, optional): Employment Sub Role. Must be one of the predefined values.
    * `hs_employment_change_detected_date` (string, optional): Employment change detected date.
    * `hs_enriched_email_bounce_detected` (boolean, optional): Enriched Email Bounce Detected.
    * `hs_facebookid` (string, optional): Facebook ID.
    * `hs_facebook_click_id` (string, optional): Facebook click id.
    * `fax` (string, optional): Fax Number.
    * `field_of_study` (string, optional): Field of study.
    * `followercount` (number, optional): Follower Count.
    * `gender` (string, optional): Gender.
    * `hs_google_click_id` (string, optional): Google ad click id.
    * `graduation_date` (string, optional): Graduation date.
    * `owneremail` (string, optional): HubSpot Owner Email (legacy).
    * `ownername` (string, optional): HubSpot Owner Name (legacy).
    * `industry` (string, optional): Industry.
    * `hs_inferred_language_codes` (string, optional): Inferred Language Codes. Must be one of the predefined values.
    * `jobtitle` (string, optional): Job Title.
    * `hs_job_change_detected_date` (string, optional): Job change detected date.
    * `job_function` (string, optional): Job function.
    * `hs_journey_stage` (string, optional): Journey Stage. Must be one of the predefined values.
    * `kloutscoregeneral` (number, optional): Klout Score.
    * `hs_last_metered_enrichment_timestamp` (string, optional): Last Metered Enrichment Timestamp.
    * `hs_latest_source` (string, optional): Latest Traffic Source.
    * `hs_latest_source_timestamp` (string, optional): Latest Traffic Source Date.
    * `hs_legal_basis` (string, optional): Legal basis for processing contact's data.
    * `linkedinbio` (string, optional): LinkedIn Bio.
    * `linkedinconnections` (number, optional): LinkedIn Connections.
    * `hs_linkedin_url` (string, optional): LinkedIn URL.
    * `hs_linkedinid` (string, optional): Linkedin ID.
    * `hs_live_enrichment_deadline` (string, optional): Live enrichment deadline.
    * `marital_status` (string, optional): Marital Status.
    * `hs_content_membership_email` (string, optional): Member email.
    * `hs_content_membership_notes` (string, optional): Membership Notes.
    * `message` (string, optional): Message.
    * `military_status` (string, optional): Military status.
    * `mobilephone` (string, optional): Mobile Phone Number.
    * `numemployees` (string, optional): Number of Employees.
    * `hs_analytics_source` (string, optional): Original Traffic Source.
    * `photo` (string, optional): Photo.
    * `hs_pinned_engagement_id` (number, optional): Pinned engagement ID.
    * `zip` (string, optional): Postal Code.
    * `hs_language` (string, optional): Preferred language. Must be one of the predefined values.
    * `associatedcompanyid` (number, optional): Primary Associated Company ID.
    * `hs_email_optout_survey_reason` (string, optional): Reason for opting out of email.
    * `relationship_status` (string, optional): Relationship Status.
    * `hs_returning_to_office_detected_date` (string, optional): Returning to office detected date.
    * `salutation` (string, optional): Salutation.
    * `school` (string, optional): School.
    * `seniority` (string, optional): Seniority.
    * `hs_feedback_show_nps_web_survey` (boolean, optional): Should be shown an NPS web survey.
    * `start_date` (string, optional): Start date.
    * `state` (string, optional): State/Region.
    * `hs_state_code` (string, optional): State/Region Code.
    * `hs_content_membership_status` (string, optional): Status.
    * `address` (string, optional): Street Address.
    * `tax_exempt` (string, optional): Tax Exempt.
    * `hs_timezone` (string, optional): Time Zone. Must be one of the predefined values.
    * `twitterbio` (string, optional): Twitter Bio.
    * `hs_twitterid` (string, optional): Twitter ID.
    * `twitterprofilephoto` (string, optional): Twitter Profile Photo.
    * `twitterhandle` (string, optional): Twitter Username.
    * `vat_number` (string, optional): VAT Number.
    * `ch_verified` (string, optional): Verified for ACH/eCheck Payments.
    * `website` (string, optional): Website URL.
    * `hs_whatsapp_phone_number` (string, optional): WhatsApp Phone Number.
    * `work_email` (string, optional): Work email.
    * `hs_googleplusid` (string, optional): googleplus ID.
  </Accordion>

<Accordion title="hubspot/create_deal">
    **Description:** Create a new deal record in HubSpot.

* `dealname` (string, required): Name of the deal.
    * `amount` (number, optional): The value of the deal.
    * `dealstage` (string, optional): The pipeline stage of the deal.
    * `pipeline` (string, optional): The pipeline the deal belongs to.
    * `closedate` (string, optional): The date the deal is expected to close.
    * `hubspot_owner_id` (string, optional): The owner of the deal.
    * `dealtype` (string, optional): The type of deal. Available values: `newbusiness`, `existingbusiness`.
    * `description` (string, optional): A description of the deal.
    * `hs_priority` (string, optional): The priority of the deal. Available values: `low`, `medium`, `high`.
  </Accordion>

<Accordion title="hubspot/create_record_engagements">
    **Description:** Create a new engagement (e.g., note, email, call, meeting, task) in HubSpot.

* `engagementType` (string, required): The type of engagement. Available values: `NOTE`, `EMAIL`, `CALL`, `MEETING`, `TASK`.
    * `hubspot_owner_id` (string, optional): The user the activity is assigned to.
    * `hs_timestamp` (string, optional): The date and time of the activity.
    * `hs_note_body` (string, optional): The body of the note. (Used for `NOTE`)
    * `hs_task_subject` (string, optional): The title of the task. (Used for `TASK`)
    * `hs_task_body` (string, optional): The notes for the task. (Used for `TASK`)
    * `hs_task_status` (string, optional): The status of the task. (Used for `TASK`)
    * `hs_meeting_title` (string, optional): The title of the meeting. (Used for `MEETING`)
    * `hs_meeting_body` (string, optional): The description for the meeting. (Used for `MEETING`)
    * `hs_meeting_start_time` (string, optional): The start time of the meeting. (Used for `MEETING`)
    * `hs_meeting_end_time` (string, optional): The end time of the meeting. (Used for `MEETING`)
  </Accordion>

<Accordion title="hubspot/update_company">
    **Description:** Update an existing company record in HubSpot.

* `recordId` (string, required): The ID of the company to update.
    * `name` (string, optional): Name of the company.
    * `domain` (string, optional): Company Domain Name.
    * `industry` (string, optional): Industry.
    * `phone` (string, optional): Phone Number.
    * `city` (string, optional): City.
    * `state` (string, optional): State/Region.
    * `zip` (string, optional): Postal Code.
    * `numberofemployees` (number, optional): Number of Employees.
    * `annualrevenue` (number, optional): Annual Revenue.
    * `description` (string, optional): Description.
  </Accordion>

<Accordion title="hubspot/create_record_any">
    **Description:** Create a record for a specified object type in HubSpot.

* `recordType` (string, required): The object type ID of the custom object.
    * Additional parameters depend on the custom object's schema.
  </Accordion>

<Accordion title="hubspot/update_contact">
    **Description:** Update an existing contact record in HubSpot.

* `recordId` (string, required): The ID of the contact to update.
    * `firstname` (string, optional): First Name.
    * `lastname` (string, optional): Last Name.
    * `email` (string, optional): Email address.
    * `phone` (string, optional): Phone Number.
    * `company` (string, optional): Company Name.
    * `jobtitle` (string, optional): Job Title.
    * `lifecyclestage` (string, optional): Lifecycle Stage.
  </Accordion>

<Accordion title="hubspot/update_deal">
    **Description:** Update an existing deal record in HubSpot.

* `recordId` (string, required): The ID of the deal to update.
    * `dealname` (string, optional): Name of the deal.
    * `amount` (number, optional): The value of the deal.
    * `dealstage` (string, optional): The pipeline stage of the deal.
    * `pipeline` (string, optional): The pipeline the deal belongs to.
    * `closedate` (string, optional): The date the deal is expected to close.
    * `dealtype` (string, optional): The type of deal.
  </Accordion>

<Accordion title="hubspot/update_record_engagements">
    **Description:** Update an existing engagement in HubSpot.

* `recordId` (string, required): The ID of the engagement to update.
    * `hs_note_body` (string, optional): The body of the note.
    * `hs_task_subject` (string, optional): The title of the task.
    * `hs_task_body` (string, optional): The notes for the task.
    * `hs_task_status` (string, optional): The status of the task.
  </Accordion>

<Accordion title="hubspot/update_record_any">
    **Description:** Update a record for a specified object type in HubSpot.

* `recordId` (string, required): The ID of the record to update.
    * `recordType` (string, required): The object type ID of the custom object.
    * Additional parameters depend on the custom object's schema.
  </Accordion>

<Accordion title="hubspot/list_companies">
    **Description:** Get a list of company records from HubSpot.

* `paginationParameters` (object, optional): Use `pageCursor` to fetch subsequent pages.
  </Accordion>

<Accordion title="hubspot/list_contacts">
    **Description:** Get a list of contact records from HubSpot.

* `paginationParameters` (object, optional): Use `pageCursor` to fetch subsequent pages.
  </Accordion>

<Accordion title="hubspot/list_deals">
    **Description:** Get a list of deal records from HubSpot.

* `paginationParameters` (object, optional): Use `pageCursor` to fetch subsequent pages.
  </Accordion>

<Accordion title="hubspot/get_records_engagements">
    **Description:** Get a list of engagement records from HubSpot.

* `objectName` (string, required): The type of engagement to fetch (e.g., "notes").
    * `paginationParameters` (object, optional): Use `pageCursor` to fetch subsequent pages.
  </Accordion>

<Accordion title="hubspot/get_records_any">
    **Description:** Get a list of records for any specified object type in HubSpot.

* `recordType` (string, required): The object type ID of the custom object.
    * `paginationParameters` (object, optional): Use `pageCursor` to fetch subsequent pages.
  </Accordion>

<Accordion title="hubspot/get_company">
    **Description:** Get a single company record by its ID.

* `recordId` (string, required): The ID of the company to retrieve.
  </Accordion>

<Accordion title="hubspot/get_contact">
    **Description:** Get a single contact record by its ID.

* `recordId` (string, required): The ID of the contact to retrieve.
  </Accordion>

<Accordion title="hubspot/get_deal">
    **Description:** Get a single deal record by its ID.

* `recordId` (string, required): The ID of the deal to retrieve.
  </Accordion>

<Accordion title="hubspot/get_record_by_id_engagements">
    **Description:** Get a single engagement record by its ID.

* `recordId` (string, required): The ID of the engagement to retrieve.
  </Accordion>

<Accordion title="hubspot/get_record_by_id_any">
    **Description:** Get a single record of any specified object type by its ID.

* `recordType` (string, required): The object type ID of the custom object.
    * `recordId` (string, required): The ID of the record to retrieve.
  </Accordion>

<Accordion title="hubspot/search_companies">
    **Description:** Search for company records in HubSpot using a filter formula.

* `filterFormula` (object, optional): A filter in disjunctive normal form (OR of ANDs).
    * `paginationParameters` (object, optional): Use `pageCursor` to fetch subsequent pages.
  </Accordion>

<Accordion title="hubspot/search_contacts">
    **Description:** Search for contact records in HubSpot using a filter formula.

* `filterFormula` (object, optional): A filter in disjunctive normal form (OR of ANDs).
    * `paginationParameters` (object, optional): Use `pageCursor` to fetch subsequent pages.
  </Accordion>

<Accordion title="hubspot/search_deals">
    **Description:** Search for deal records in HubSpot using a filter formula.

* `filterFormula` (object, optional): A filter in disjunctive normal form (OR of ANDs).
    * `paginationParameters` (object, optional): Use `pageCursor` to fetch subsequent pages.
  </Accordion>

<Accordion title="hubspot/search_records_engagements">
    **Description:** Search for engagement records in HubSpot using a filter formula.

* `engagementFilterFormula` (object, optional): A filter for engagements.
    * `paginationParameters` (object, optional): Use `pageCursor` to fetch subsequent pages.
  </Accordion>

<Accordion title="hubspot/search_records_any">
    **Description:** Search for records of any specified object type in HubSpot.

* `recordType` (string, required): The object type ID to search.
    * `filterFormula` (string, optional): The filter formula to apply.
    * `paginationParameters` (object, optional): Use `pageCursor` to fetch subsequent pages.
  </Accordion>

<Accordion title="hubspot/delete_record_companies">
    **Description:** Delete a company record by its ID.

* `recordId` (string, required): The ID of the company to delete.
  </Accordion>

<Accordion title="hubspot/delete_record_contacts">
    **Description:** Delete a contact record by its ID.

* `recordId` (string, required): The ID of the contact to delete.
  </Accordion>

<Accordion title="hubspot/delete_record_deals">
    **Description:** Delete a deal record by its ID.

* `recordId` (string, required): The ID of the deal to delete.
  </Accordion>

<Accordion title="hubspot/delete_record_engagements">
    **Description:** Delete an engagement record by its ID.

* `recordId` (string, required): The ID of the engagement to delete.
  </Accordion>

<Accordion title="hubspot/delete_record_any">
    **Description:** Delete a record of any specified object type by its ID.

* `recordType` (string, required): The object type ID of the custom object.
    * `recordId` (string, required): The ID of the record to delete.
  </Accordion>

<Accordion title="hubspot/get_contacts_by_list_id">
    **Description:** Get contacts from a specific list by its ID.

* `listId` (string, required): The ID of the list to get contacts from.
    * `paginationParameters` (object, optional): Use `pageCursor` for subsequent pages.
  </Accordion>

<Accordion title="hubspot/describe_action_schema">
    **Description:** Get the expected schema for a given object type and operation.

* `recordType` (string, required): The object type ID (e.g., 'companies').
    * `operation` (string, required): The operation type (e.g., 'CREATE\_RECORD').
  </Accordion>
</AccordionGroup>

### Basic HubSpot Agent Setup

```python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

Example 3 (unknown):
```unknown
## Available Actions

<AccordionGroup>
  <Accordion title="hubspot/create_company">
    **Description:** Create a new company record in HubSpot.

    **Parameters:**

    * `name` (string, required): Name of the company.
    * `domain` (string, optional): Company Domain Name.
    * `industry` (string, optional): Industry. Must be one of the predefined values from HubSpot.
    * `phone` (string, optional): Phone Number.
    * `hubspot_owner_id` (string, optional): Company owner ID.
    * `type` (string, optional): Type of the company. Available values: `PROSPECT`, `PARTNER`, `RESELLER`, `VENDOR`, `OTHER`.
    * `city` (string, optional): City.
    * `state` (string, optional): State/Region.
    * `zip` (string, optional): Postal Code.
    * `numberofemployees` (number, optional): Number of Employees.
    * `annualrevenue` (number, optional): Annual Revenue.
    * `timezone` (string, optional): Time Zone.
    * `description` (string, optional): Description.
    * `linkedin_company_page` (string, optional): LinkedIn Company Page URL.
    * `company_email` (string, optional): Company Email.
    * `first_name` (string, optional): First Name of a contact at the company.
    * `last_name` (string, optional): Last Name of a contact at the company.
    * `about_us` (string, optional): About Us.
    * `hs_csm_sentiment` (string, optional): CSM Sentiment. Available values: `at_risk`, `neutral`, `healthy`.
    * `closedate` (string, optional): Close Date.
    * `hs_keywords` (string, optional): Company Keywords. Must be one of the predefined values.
    * `country` (string, optional): Country/Region.
    * `hs_country_code` (string, optional): Country/Region Code.
    * `hs_employee_range` (string, optional): Employee range.
    * `facebook_company_page` (string, optional): Facebook Company Page URL.
    * `facebookfans` (number, optional): Number of Facebook Fans.
    * `hs_gps_coordinates` (string, optional): GPS Coordinates.
    * `hs_gps_error` (string, optional): GPS Error.
    * `googleplus_page` (string, optional): Google Plus Page URL.
    * `owneremail` (string, optional): HubSpot Owner Email.
    * `ownername` (string, optional): HubSpot Owner Name.
    * `hs_ideal_customer_profile` (string, optional): Ideal Customer Profile Tier. Available values: `tier_1`, `tier_2`, `tier_3`.
    * `hs_industry_group` (string, optional): Industry group.
    * `is_public` (boolean, optional): Is Public.
    * `hs_last_metered_enrichment_timestamp` (string, optional): Last Metered Enrichment Timestamp.
    * `hs_lead_status` (string, optional): Lead Status. Available values: `NEW`, `OPEN`, `IN_PROGRESS`, `OPEN_DEAL`, `UNQUALIFIED`, `ATTEMPTED_TO_CONTACT`, `CONNECTED`, `BAD_TIMING`.
    * `lifecyclestage` (string, optional): Lifecycle Stage. Available values: `subscriber`, `lead`, `marketingqualifiedlead`, `salesqualifiedlead`, `opportunity`, `customer`, `evangelist`, `other`.
    * `linkedinbio` (string, optional): LinkedIn Bio.
    * `hs_linkedin_handle` (string, optional): LinkedIn handle.
    * `hs_live_enrichment_deadline` (string, optional): Live enrichment deadline.
    * `hs_logo_url` (string, optional): Logo URL.
    * `hs_analytics_source` (string, optional): Original Traffic Source.
    * `hs_pinned_engagement_id` (number, optional): Pinned Engagement ID.
    * `hs_quick_context` (string, optional): Quick context.
    * `hs_revenue_range` (string, optional): Revenue range.
    * `hs_state_code` (string, optional): State/Region Code.
    * `address` (string, optional): Street Address.
    * `address2` (string, optional): Street Address 2.
    * `hs_is_target_account` (boolean, optional): Target Account.
    * `hs_target_account` (string, optional): Target Account Tier. Available values: `tier_1`, `tier_2`, `tier_3`.
    * `hs_target_account_recommendation_snooze_time` (string, optional): Target Account Recommendation Snooze Time.
    * `hs_target_account_recommendation_state` (string, optional): Target Account Recommendation State. Available values: `DISMISSED`, `NONE`, `SNOOZED`.
    * `total_money_raised` (string, optional): Total Money Raised.
    * `twitterbio` (string, optional): Twitter Bio.
    * `twitterfollowers` (number, optional): Twitter Followers.
    * `twitterhandle` (string, optional): Twitter Handle.
    * `web_technologies` (string, optional): Web Technologies used. Must be one of the predefined values.
    * `website` (string, optional): Website URL.
    * `founded_year` (string, optional): Year Founded.
  </Accordion>

  <Accordion title="hubspot/create_contact">
    **Description:** Create a new contact record in HubSpot.

    **Parameters:**

    * `email` (string, required): Email address of the contact.
    * `firstname` (string, optional): First Name.
    * `lastname` (string, optional): Last Name.
    * `phone` (string, optional): Phone Number.
    * `hubspot_owner_id` (string, optional): Contact owner.
    * `lifecyclestage` (string, optional): Lifecycle Stage. Available values: `subscriber`, `lead`, `marketingqualifiedlead`, `salesqualifiedlead`, `opportunity`, `customer`, `evangelist`, `other`.
    * `hs_lead_status` (string, optional): Lead Status. Available values: `NEW`, `OPEN`, `IN_PROGRESS`, `OPEN_DEAL`, `UNQUALIFIED`, `ATTEMPTED_TO_CONTACT`, `CONNECTED`, `BAD_TIMING`.
    * `annualrevenue` (string, optional): Annual Revenue.
    * `hs_buying_role` (string, optional): Buying Role.
    * `cc_emails` (string, optional): CC Emails.
    * `ch_customer_id` (string, optional): Chargify Customer ID.
    * `ch_customer_reference` (string, optional): Chargify Customer Reference.
    * `chargify_sites` (string, optional): Chargify Site(s).
    * `city` (string, optional): City.
    * `hs_facebook_ad_clicked` (boolean, optional): Clicked Facebook ad.
    * `hs_linkedin_ad_clicked` (string, optional): Clicked LinkedIn Ad.
    * `hs_clicked_linkedin_ad` (string, optional): Clicked on a LinkedIn Ad.
    * `closedate` (string, optional): Close Date.
    * `company` (string, optional): Company Name.
    * `company_size` (string, optional): Company size.
    * `country` (string, optional): Country/Region.
    * `hs_country_region_code` (string, optional): Country/Region Code.
    * `date_of_birth` (string, optional): Date of birth.
    * `degree` (string, optional): Degree.
    * `hs_email_customer_quarantined_reason` (string, optional): Email address quarantine reason.
    * `hs_role` (string, optional): Employment Role. Must be one of the predefined values.
    * `hs_seniority` (string, optional): Employment Seniority. Must be one of the predefined values.
    * `hs_sub_role` (string, optional): Employment Sub Role. Must be one of the predefined values.
    * `hs_employment_change_detected_date` (string, optional): Employment change detected date.
    * `hs_enriched_email_bounce_detected` (boolean, optional): Enriched Email Bounce Detected.
    * `hs_facebookid` (string, optional): Facebook ID.
    * `hs_facebook_click_id` (string, optional): Facebook click id.
    * `fax` (string, optional): Fax Number.
    * `field_of_study` (string, optional): Field of study.
    * `followercount` (number, optional): Follower Count.
    * `gender` (string, optional): Gender.
    * `hs_google_click_id` (string, optional): Google ad click id.
    * `graduation_date` (string, optional): Graduation date.
    * `owneremail` (string, optional): HubSpot Owner Email (legacy).
    * `ownername` (string, optional): HubSpot Owner Name (legacy).
    * `industry` (string, optional): Industry.
    * `hs_inferred_language_codes` (string, optional): Inferred Language Codes. Must be one of the predefined values.
    * `jobtitle` (string, optional): Job Title.
    * `hs_job_change_detected_date` (string, optional): Job change detected date.
    * `job_function` (string, optional): Job function.
    * `hs_journey_stage` (string, optional): Journey Stage. Must be one of the predefined values.
    * `kloutscoregeneral` (number, optional): Klout Score.
    * `hs_last_metered_enrichment_timestamp` (string, optional): Last Metered Enrichment Timestamp.
    * `hs_latest_source` (string, optional): Latest Traffic Source.
    * `hs_latest_source_timestamp` (string, optional): Latest Traffic Source Date.
    * `hs_legal_basis` (string, optional): Legal basis for processing contact's data.
    * `linkedinbio` (string, optional): LinkedIn Bio.
    * `linkedinconnections` (number, optional): LinkedIn Connections.
    * `hs_linkedin_url` (string, optional): LinkedIn URL.
    * `hs_linkedinid` (string, optional): Linkedin ID.
    * `hs_live_enrichment_deadline` (string, optional): Live enrichment deadline.
    * `marital_status` (string, optional): Marital Status.
    * `hs_content_membership_email` (string, optional): Member email.
    * `hs_content_membership_notes` (string, optional): Membership Notes.
    * `message` (string, optional): Message.
    * `military_status` (string, optional): Military status.
    * `mobilephone` (string, optional): Mobile Phone Number.
    * `numemployees` (string, optional): Number of Employees.
    * `hs_analytics_source` (string, optional): Original Traffic Source.
    * `photo` (string, optional): Photo.
    * `hs_pinned_engagement_id` (number, optional): Pinned engagement ID.
    * `zip` (string, optional): Postal Code.
    * `hs_language` (string, optional): Preferred language. Must be one of the predefined values.
    * `associatedcompanyid` (number, optional): Primary Associated Company ID.
    * `hs_email_optout_survey_reason` (string, optional): Reason for opting out of email.
    * `relationship_status` (string, optional): Relationship Status.
    * `hs_returning_to_office_detected_date` (string, optional): Returning to office detected date.
    * `salutation` (string, optional): Salutation.
    * `school` (string, optional): School.
    * `seniority` (string, optional): Seniority.
    * `hs_feedback_show_nps_web_survey` (boolean, optional): Should be shown an NPS web survey.
    * `start_date` (string, optional): Start date.
    * `state` (string, optional): State/Region.
    * `hs_state_code` (string, optional): State/Region Code.
    * `hs_content_membership_status` (string, optional): Status.
    * `address` (string, optional): Street Address.
    * `tax_exempt` (string, optional): Tax Exempt.
    * `hs_timezone` (string, optional): Time Zone. Must be one of the predefined values.
    * `twitterbio` (string, optional): Twitter Bio.
    * `hs_twitterid` (string, optional): Twitter ID.
    * `twitterprofilephoto` (string, optional): Twitter Profile Photo.
    * `twitterhandle` (string, optional): Twitter Username.
    * `vat_number` (string, optional): VAT Number.
    * `ch_verified` (string, optional): Verified for ACH/eCheck Payments.
    * `website` (string, optional): Website URL.
    * `hs_whatsapp_phone_number` (string, optional): WhatsApp Phone Number.
    * `work_email` (string, optional): Work email.
    * `hs_googleplusid` (string, optional): googleplus ID.
  </Accordion>

  <Accordion title="hubspot/create_deal">
    **Description:** Create a new deal record in HubSpot.

    **Parameters:**

    * `dealname` (string, required): Name of the deal.
    * `amount` (number, optional): The value of the deal.
    * `dealstage` (string, optional): The pipeline stage of the deal.
    * `pipeline` (string, optional): The pipeline the deal belongs to.
    * `closedate` (string, optional): The date the deal is expected to close.
    * `hubspot_owner_id` (string, optional): The owner of the deal.
    * `dealtype` (string, optional): The type of deal. Available values: `newbusiness`, `existingbusiness`.
    * `description` (string, optional): A description of the deal.
    * `hs_priority` (string, optional): The priority of the deal. Available values: `low`, `medium`, `high`.
  </Accordion>

  <Accordion title="hubspot/create_record_engagements">
    **Description:** Create a new engagement (e.g., note, email, call, meeting, task) in HubSpot.

    **Parameters:**

    * `engagementType` (string, required): The type of engagement. Available values: `NOTE`, `EMAIL`, `CALL`, `MEETING`, `TASK`.
    * `hubspot_owner_id` (string, optional): The user the activity is assigned to.
    * `hs_timestamp` (string, optional): The date and time of the activity.
    * `hs_note_body` (string, optional): The body of the note. (Used for `NOTE`)
    * `hs_task_subject` (string, optional): The title of the task. (Used for `TASK`)
    * `hs_task_body` (string, optional): The notes for the task. (Used for `TASK`)
    * `hs_task_status` (string, optional): The status of the task. (Used for `TASK`)
    * `hs_meeting_title` (string, optional): The title of the meeting. (Used for `MEETING`)
    * `hs_meeting_body` (string, optional): The description for the meeting. (Used for `MEETING`)
    * `hs_meeting_start_time` (string, optional): The start time of the meeting. (Used for `MEETING`)
    * `hs_meeting_end_time` (string, optional): The end time of the meeting. (Used for `MEETING`)
  </Accordion>

  <Accordion title="hubspot/update_company">
    **Description:** Update an existing company record in HubSpot.

    **Parameters:**

    * `recordId` (string, required): The ID of the company to update.
    * `name` (string, optional): Name of the company.
    * `domain` (string, optional): Company Domain Name.
    * `industry` (string, optional): Industry.
    * `phone` (string, optional): Phone Number.
    * `city` (string, optional): City.
    * `state` (string, optional): State/Region.
    * `zip` (string, optional): Postal Code.
    * `numberofemployees` (number, optional): Number of Employees.
    * `annualrevenue` (number, optional): Annual Revenue.
    * `description` (string, optional): Description.
  </Accordion>

  <Accordion title="hubspot/create_record_any">
    **Description:** Create a record for a specified object type in HubSpot.

    **Parameters:**

    * `recordType` (string, required): The object type ID of the custom object.
    * Additional parameters depend on the custom object's schema.
  </Accordion>

  <Accordion title="hubspot/update_contact">
    **Description:** Update an existing contact record in HubSpot.

    **Parameters:**

    * `recordId` (string, required): The ID of the contact to update.
    * `firstname` (string, optional): First Name.
    * `lastname` (string, optional): Last Name.
    * `email` (string, optional): Email address.
    * `phone` (string, optional): Phone Number.
    * `company` (string, optional): Company Name.
    * `jobtitle` (string, optional): Job Title.
    * `lifecyclestage` (string, optional): Lifecycle Stage.
  </Accordion>

  <Accordion title="hubspot/update_deal">
    **Description:** Update an existing deal record in HubSpot.

    **Parameters:**

    * `recordId` (string, required): The ID of the deal to update.
    * `dealname` (string, optional): Name of the deal.
    * `amount` (number, optional): The value of the deal.
    * `dealstage` (string, optional): The pipeline stage of the deal.
    * `pipeline` (string, optional): The pipeline the deal belongs to.
    * `closedate` (string, optional): The date the deal is expected to close.
    * `dealtype` (string, optional): The type of deal.
  </Accordion>

  <Accordion title="hubspot/update_record_engagements">
    **Description:** Update an existing engagement in HubSpot.

    **Parameters:**

    * `recordId` (string, required): The ID of the engagement to update.
    * `hs_note_body` (string, optional): The body of the note.
    * `hs_task_subject` (string, optional): The title of the task.
    * `hs_task_body` (string, optional): The notes for the task.
    * `hs_task_status` (string, optional): The status of the task.
  </Accordion>

  <Accordion title="hubspot/update_record_any">
    **Description:** Update a record for a specified object type in HubSpot.

    **Parameters:**

    * `recordId` (string, required): The ID of the record to update.
    * `recordType` (string, required): The object type ID of the custom object.
    * Additional parameters depend on the custom object's schema.
  </Accordion>

  <Accordion title="hubspot/list_companies">
    **Description:** Get a list of company records from HubSpot.

    **Parameters:**

    * `paginationParameters` (object, optional): Use `pageCursor` to fetch subsequent pages.
  </Accordion>

  <Accordion title="hubspot/list_contacts">
    **Description:** Get a list of contact records from HubSpot.

    **Parameters:**

    * `paginationParameters` (object, optional): Use `pageCursor` to fetch subsequent pages.
  </Accordion>

  <Accordion title="hubspot/list_deals">
    **Description:** Get a list of deal records from HubSpot.

    **Parameters:**

    * `paginationParameters` (object, optional): Use `pageCursor` to fetch subsequent pages.
  </Accordion>

  <Accordion title="hubspot/get_records_engagements">
    **Description:** Get a list of engagement records from HubSpot.

    **Parameters:**

    * `objectName` (string, required): The type of engagement to fetch (e.g., "notes").
    * `paginationParameters` (object, optional): Use `pageCursor` to fetch subsequent pages.
  </Accordion>

  <Accordion title="hubspot/get_records_any">
    **Description:** Get a list of records for any specified object type in HubSpot.

    **Parameters:**

    * `recordType` (string, required): The object type ID of the custom object.
    * `paginationParameters` (object, optional): Use `pageCursor` to fetch subsequent pages.
  </Accordion>

  <Accordion title="hubspot/get_company">
    **Description:** Get a single company record by its ID.

    **Parameters:**

    * `recordId` (string, required): The ID of the company to retrieve.
  </Accordion>

  <Accordion title="hubspot/get_contact">
    **Description:** Get a single contact record by its ID.

    **Parameters:**

    * `recordId` (string, required): The ID of the contact to retrieve.
  </Accordion>

  <Accordion title="hubspot/get_deal">
    **Description:** Get a single deal record by its ID.

    **Parameters:**

    * `recordId` (string, required): The ID of the deal to retrieve.
  </Accordion>

  <Accordion title="hubspot/get_record_by_id_engagements">
    **Description:** Get a single engagement record by its ID.

    **Parameters:**

    * `recordId` (string, required): The ID of the engagement to retrieve.
  </Accordion>

  <Accordion title="hubspot/get_record_by_id_any">
    **Description:** Get a single record of any specified object type by its ID.

    **Parameters:**

    * `recordType` (string, required): The object type ID of the custom object.
    * `recordId` (string, required): The ID of the record to retrieve.
  </Accordion>

  <Accordion title="hubspot/search_companies">
    **Description:** Search for company records in HubSpot using a filter formula.

    **Parameters:**

    * `filterFormula` (object, optional): A filter in disjunctive normal form (OR of ANDs).
    * `paginationParameters` (object, optional): Use `pageCursor` to fetch subsequent pages.
  </Accordion>

  <Accordion title="hubspot/search_contacts">
    **Description:** Search for contact records in HubSpot using a filter formula.

    **Parameters:**

    * `filterFormula` (object, optional): A filter in disjunctive normal form (OR of ANDs).
    * `paginationParameters` (object, optional): Use `pageCursor` to fetch subsequent pages.
  </Accordion>

  <Accordion title="hubspot/search_deals">
    **Description:** Search for deal records in HubSpot using a filter formula.

    **Parameters:**

    * `filterFormula` (object, optional): A filter in disjunctive normal form (OR of ANDs).
    * `paginationParameters` (object, optional): Use `pageCursor` to fetch subsequent pages.
  </Accordion>

  <Accordion title="hubspot/search_records_engagements">
    **Description:** Search for engagement records in HubSpot using a filter formula.

    **Parameters:**

    * `engagementFilterFormula` (object, optional): A filter for engagements.
    * `paginationParameters` (object, optional): Use `pageCursor` to fetch subsequent pages.
  </Accordion>

  <Accordion title="hubspot/search_records_any">
    **Description:** Search for records of any specified object type in HubSpot.

    **Parameters:**

    * `recordType` (string, required): The object type ID to search.
    * `filterFormula` (string, optional): The filter formula to apply.
    * `paginationParameters` (object, optional): Use `pageCursor` to fetch subsequent pages.
  </Accordion>

  <Accordion title="hubspot/delete_record_companies">
    **Description:** Delete a company record by its ID.

    **Parameters:**

    * `recordId` (string, required): The ID of the company to delete.
  </Accordion>

  <Accordion title="hubspot/delete_record_contacts">
    **Description:** Delete a contact record by its ID.

    **Parameters:**

    * `recordId` (string, required): The ID of the contact to delete.
  </Accordion>

  <Accordion title="hubspot/delete_record_deals">
    **Description:** Delete a deal record by its ID.

    **Parameters:**

    * `recordId` (string, required): The ID of the deal to delete.
  </Accordion>

  <Accordion title="hubspot/delete_record_engagements">
    **Description:** Delete an engagement record by its ID.

    **Parameters:**

    * `recordId` (string, required): The ID of the engagement to delete.
  </Accordion>

  <Accordion title="hubspot/delete_record_any">
    **Description:** Delete a record of any specified object type by its ID.

    **Parameters:**

    * `recordType` (string, required): The object type ID of the custom object.
    * `recordId` (string, required): The ID of the record to delete.
  </Accordion>

  <Accordion title="hubspot/get_contacts_by_list_id">
    **Description:** Get contacts from a specific list by its ID.

    **Parameters:**

    * `listId` (string, required): The ID of the list to get contacts from.
    * `paginationParameters` (object, optional): Use `pageCursor` for subsequent pages.
  </Accordion>

  <Accordion title="hubspot/describe_action_schema">
    **Description:** Get the expected schema for a given object type and operation.

    **Parameters:**

    * `recordType` (string, required): The object type ID (e.g., 'companies').
    * `operation` (string, required): The operation type (e.g., 'CREATE\_RECORD').
  </Accordion>
</AccordionGroup>

## Usage Examples

### Basic HubSpot Agent Setup
```

---

## Human Input on Execution

**URL:** llms-txt#human-input-on-execution

**Contents:**
- Human input in agent execution
- Using human input with CrewAI
  - Example:

Source: https://docs.crewai.com/en/learn/human-input-on-execution

Integrating CrewAI with human input during execution in complex decision-making processes and leveraging the full capabilities of the agent's attributes and tools.

## Human input in agent execution

Human input is critical in several agent execution scenarios, allowing agents to request additional information or clarification when necessary.
This feature is especially useful in complex decision-making processes or when agents require more details to complete a task effectively.

## Using human input with CrewAI

To integrate human input into agent execution, set the `human_input` flag in the task definition. When enabled, the agent prompts the user for input before delivering its final answer.
This input can provide extra context, clarify ambiguities, or validate the agent's output.

```python Code theme={null}
import os
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool

os.environ["SERPER_API_KEY"] = "Your Key"  # serper.dev API key
os.environ["OPENAI_API_KEY"] = "Your Key"

**Examples:**

Example 1 (unknown):
```unknown

```

---

## Image Generation with DALL-E

**URL:** llms-txt#image-generation-with-dall-e

**Contents:**
- Prerequisites
- Setting Up the DALL-E Tool
- Using the DALL-E Tool
  - Example Agent Configuration
  - Expected Output
- Best Practices
- Troubleshooting

Source: https://docs.crewai.com/en/learn/dalle-image-generation

Learn how to use DALL-E for AI-powered image generation in your CrewAI projects

CrewAI supports integration with OpenAI's DALL-E, allowing your AI agents to generate images as part of their tasks. This guide will walk you through how to set up and use the DALL-E tool in your CrewAI projects.

* crewAI installed (latest version)
* OpenAI API key with access to DALL-E

## Setting Up the DALL-E Tool

<Steps>
  <Step title="Import the DALL-E tool">
    
  </Step>

<Step title="Add the DALL-E tool to your agent configuration">
    
  </Step>
</Steps>

## Using the DALL-E Tool

Once you've added the DALL-E tool to your agent, it can generate images based on text prompts. The tool will return a URL to the generated image, which can be used in the agent's output or passed to other agents for further processing.

### Example Agent Configuration

The agent with the DALL-E tool will be able to generate the image and provide a URL in its response. You can then download the image.

<Frame>
  <img alt="DALL-E Image" />
</Frame>

1. **Be specific in your image generation prompts** to get the best results.
2. **Consider generation time** - Image generation can take some time, so factor this into your task planning.
3. **Follow usage policies** - Always comply with OpenAI's usage policies when generating images.

1. **Check API access** - Ensure your OpenAI API key has access to DALL-E.
2. **Version compatibility** - Check that you're using the latest version of crewAI and crewai-tools.
3. **Tool configuration** - Verify that the DALL-E tool is correctly added to the agent's tool list.

**Examples:**

Example 1 (unknown):
```unknown
</Step>

  <Step title="Add the DALL-E tool to your agent configuration">
```

Example 2 (unknown):
```unknown
</Step>
</Steps>

## Using the DALL-E Tool

Once you've added the DALL-E tool to your agent, it can generate images based on text prompts. The tool will return a URL to the generated image, which can be used in the agent's output or passed to other agents for further processing.

### Example Agent Configuration
```

---

## Initialize the agent with advanced options

**URL:** llms-txt#initialize-the-agent-with-advanced-options

**Contents:**
- Delegation and Autonomy
  - Example: Disabling Delegation for an Agent
- Conclusion

agent = Agent(
  role='Research Analyst',
  goal='Provide up-to-date market analysis',
  backstory='An expert analyst with a keen eye for market trends.',
  tools=[search_tool],
  memory=True, # Enable memory
  verbose=True,
  max_rpm=None, # No limit on requests per minute
  max_iter=25, # Default value for maximum iterations
)
python Code theme={null}
agent = Agent(
  role='Content Writer',
  goal='Write engaging content on market trends',
  backstory='A seasoned writer with expertise in market analysis.',
  allow_delegation=True # Enabling delegation
)
```

Customizing agents in CrewAI by setting their roles, goals, backstories, and tools, alongside advanced options like language model customization, memory, performance settings, and delegation preferences,
equips a nuanced and capable AI team ready for complex challenges.

**Examples:**

Example 1 (unknown):
```unknown
## Delegation and Autonomy

Controlling an agent's ability to delegate tasks or ask questions is vital for tailoring its autonomy and collaborative dynamics within the CrewAI framework. By default,
the `allow_delegation` attribute is now set to `False`, disabling agents to seek assistance or delegate tasks as needed. This default behavior can be changed to promote collaborative problem-solving and
efficiency within the CrewAI ecosystem. If needed, delegation can be enabled to suit specific operational requirements.

### Example: Disabling Delegation for an Agent
```

---

## Initialize the tool for semantic searches within a specific GitHub repository, so the agent can search any repository if it learns about during its execution

**URL:** llms-txt#initialize-the-tool-for-semantic-searches-within-a-specific-github-repository,-so-the-agent-can-search-any-repository-if-it-learns-about-during-its-execution

**Contents:**
- Arguments
- Custom model and embeddings

tool = GithubSearchTool(
	gh_token='your_github_personal_access_token',
	content_types=['code', 'issue'] # Options: code, repo, pr, issue
)
python Code theme={null}
tool = GithubSearchTool(
    config=dict(
        llm=dict(
            provider="ollama", # or google, openai, anthropic, llama2, ...
            config=dict(
                model="llama2",
                # temperature=0.5,
                # top_p=1,
                # stream=true,
            ),
        ),
        embedder=dict(
            provider="google-generativeai", # or openai, ollama, ...
            config=dict(
                model_name="gemini-embedding-001",
                task_type="RETRIEVAL_DOCUMENT",
                # title="Embeddings",
            ),
        ),
    )
)
```

**Examples:**

Example 1 (unknown):
```unknown
## Arguments

* `github_repo` : The URL of the GitHub repository where the search will be conducted. This is a mandatory field and specifies the target repository for your search.
* `gh_token` : Your GitHub Personal Access Token (PAT) required for authentication. You can create one in your GitHub account settings under Developer Settings > Personal Access Tokens.
* `content_types` : Specifies the types of content to include in your search. You must provide a list of content types from the following options: `code` for searching within the code,
  `repo` for searching within the repository's general information, `pr` for searching within pull requests, and `issue` for searching within issues.
  This field is mandatory and allows tailoring the search to specific content types within the GitHub repository.

## Custom model and embeddings

By default, the tool uses OpenAI for both embeddings and summarization. To customize the model, you can use a config dictionary as follows:
```

---

## Initialize the tool so the agent can read any directory's content

**URL:** llms-txt#initialize-the-tool-so-the-agent-can-read-any-directory's-content

---

## Initialize the tool to read any files the agents knows or lean the path for

**URL:** llms-txt#initialize-the-tool-to-read-any-files-the-agents-knows-or-lean-the-path-for

file_read_tool = FileReadTool()

---

## Initialize the tool with a specific file path, so the agent can only read the content of the specified file

**URL:** llms-txt#initialize-the-tool-with-a-specific-file-path,-so-the-agent-can-only-read-the-content-of-the-specified-file

**Contents:**
- Arguments

file_read_tool = FileReadTool(file_path='path/to/your/file.txt')
```

* `file_path`: The path to the file you want to read. It accepts both absolute and relative paths. Ensure the file exists and you have the necessary permissions to access it.

---

## Instantiate the crew with a sequential process

**URL:** llms-txt#instantiate-the-crew-with-a-sequential-process

crew = Crew(
    agents=[blog_agent],
    tasks=[task1],
    verbose=True,
    process=Process.sequential,
)

---

## Instantiate your crew with a custom manager

**URL:** llms-txt#instantiate-your-crew-with-a-custom-manager

crew = Crew(
    agents=[researcher, writer],
    tasks=[task],
    manager_agent=manager,
    process=Process.hierarchical,
)

---

## Instantiate your crew with a sequential process

**URL:** llms-txt#instantiate-your-crew-with-a-sequential-process

crew = Crew(
    agents=[researcher, writer], tasks=[task1, task2], verbose=1, process=Process.sequential
)

---

## `InvokeCrewAIAutomationTool`

**URL:** llms-txt#`invokecrewaiautomationtool`

**Contents:**
- Installation
- Requirements
- Usage

The `InvokeCrewAIAutomationTool` provides CrewAI Platform API integration with external crew services. This tool allows you to invoke and interact with CrewAI Platform automations from within your CrewAI agents, enabling seamless integration between different crew workflows.

* CrewAI Platform API access
* Valid bearer token for authentication
* Network access to CrewAI Platform automation endpoints

Here's how to use the tool with a CrewAI agent:

```python {2, 4-9} theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import InvokeCrewAIAutomationTool

**Examples:**

Example 1 (unknown):
```unknown
## Requirements

* CrewAI Platform API access
* Valid bearer token for authentication
* Network access to CrewAI Platform automation endpoints

## Usage

Here's how to use the tool with a CrewAI agent:
```

---

## In Flow

**URL:** llms-txt#in-flow

**Contents:**
  - Utilizing the `tool` Decorator
  - Custom Caching Mechanism
- Conclusion

class MyFlow(Flow):
    @start()
    async def begin(self):
        crew = Crew(agents=[agent])
        result = await crew.kickoff_async()
        return result
python Code theme={null}
from crewai.tools import tool
@tool("Name of my tool")
def my_tool(question: str) -> str:
    """Clear description for what this tool is useful for, your agent will need this information to use it."""
    # Function logic here
    return "Result from your custom tool"
python Code theme={null}
from crewai.tools import tool

@tool
def multiplication_tool(first_number: int, second_number: int) -> str:
    """Useful for when you need to multiply two numbers together."""
    return first_number * second_number

def cache_func(args, result):
    # In this case, we only cache the result if it's a multiple of 2
    cache = result % 2 == 0
    return cache

multiplication_tool.cache_function = cache_func

writer1 = Agent(
        role="Writer",
        goal="You write lessons of math for kids.",
        backstory="You're an expert in writing and you love to teach kids but you know nothing of math.",
        tools=[multiplication_tool],
        allow_delegation=False,
    )
    #...
```

Tools are pivotal in extending the capabilities of CrewAI agents, enabling them to undertake a broad spectrum of tasks and collaborate effectively.
When building solutions with CrewAI, leverage both custom and existing tools to empower your agents and enhance the AI ecosystem. Consider utilizing error handling,
caching mechanisms, and the flexibility of tool arguments to optimize your agents' performance and capabilities.

**Examples:**

Example 1 (unknown):
```unknown
The CrewAI framework automatically handles the execution of both synchronous and asynchronous tools, so you don't need to worry about how to call them differently.

### Utilizing the `tool` Decorator
```

Example 2 (unknown):
```unknown
### Custom Caching Mechanism

<Tip>
  Tools can optionally implement a `cache_function` to fine-tune caching
  behavior. This function determines when to cache results based on specific
  conditions, offering granular control over caching logic.
</Tip>
```

---

## Jira Integration

**URL:** llms-txt#jira-integration

**Contents:**
- Overview
- Prerequisites
- Setting Up Jira Integration
  - 1. Connect Your Jira Account
  - 2. Install Required Package
  - 3. Environment Variable Setup
- Available Actions
- Usage Examples
  - Basic Jira Agent Setup

Source: https://docs.crewai.com/en/enterprise/integrations/jira

Issue tracking and project management with Jira integration for CrewAI.

Enable your agents to manage issues, projects, and workflows through Jira. Create and update issues, track project progress, manage assignments, and streamline your project management with AI-powered automation.

Before using the Jira integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A Jira account with appropriate project permissions
* Connected your Jira account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)

## Setting Up Jira Integration

### 1. Connect Your Jira Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Jira** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for issue and project management
5. Copy your Enterprise Token from [Integration Settings](https://app.crewai.com/crewai_plus/settings/integrations)

### 2. Install Required Package

### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>

Or add it to your `.env` file:

<AccordionGroup>
  <Accordion title="jira/create_issue">
    **Description:** Create an issue in Jira.

* `summary` (string, required): Summary - A brief one-line summary of the issue. (example: "The printer stopped working").
    * `project` (string, optional): Project - The project which the issue belongs to. Defaults to the user's first project if not provided. Use Connect Portal Workflow Settings to allow users to select a Project.
    * `issueType` (string, optional): Issue type - Defaults to Task if not provided.
    * `jiraIssueStatus` (string, optional): Status - Defaults to the project's first status if not provided.
    * `assignee` (string, optional): Assignee - Defaults to the authenticated user if not provided.
    * `descriptionType` (string, optional): Description Type - Select the Description Type.
      * Options: `description`, `descriptionJSON`
    * `description` (string, optional): Description - A detailed description of the issue. This field appears only when 'descriptionType' = 'description'.
    * `additionalFields` (string, optional): Additional Fields - Specify any other fields that should be included in JSON format. Use Connect Portal Workflow Settings to allow users to select which Issue Fields to update.
      
  </Accordion>

<Accordion title="jira/update_issue">
    **Description:** Update an issue in Jira.

* `issueKey` (string, required): Issue Key (example: "TEST-1234").
    * `summary` (string, optional): Summary - A brief one-line summary of the issue. (example: "The printer stopped working").
    * `issueType` (string, optional): Issue type - Use Connect Portal Workflow Settings to allow users to select an Issue Type.
    * `jiraIssueStatus` (string, optional): Status - Use Connect Portal Workflow Settings to allow users to select a Status.
    * `assignee` (string, optional): Assignee - Use Connect Portal Workflow Settings to allow users to select an Assignee.
    * `descriptionType` (string, optional): Description Type - Select the Description Type.
      * Options: `description`, `descriptionJSON`
    * `description` (string, optional): Description - A detailed description of the issue. This field appears only when 'descriptionType' = 'description'.
    * `additionalFields` (string, optional): Additional Fields - Specify any other fields that should be included in JSON format.
  </Accordion>

<Accordion title="jira/get_issue_by_key">
    **Description:** Get an issue by key in Jira.

* `issueKey` (string, required): Issue Key (example: "TEST-1234").
  </Accordion>

<Accordion title="jira/filter_issues">
    **Description:** Search issues in Jira using filters.

* `jqlQuery` (object, optional): A filter in disjunctive normal form - OR of AND groups of single conditions.
      
      Available operators: `$stringExactlyMatches`, `$stringDoesNotExactlyMatch`, `$stringIsIn`, `$stringIsNotIn`, `$stringContains`, `$stringDoesNotContain`, `$stringGreaterThan`, `$stringLessThan`
    * `limit` (string, optional): Limit results - Limit the maximum number of issues to return. Defaults to 10 if left blank.
  </Accordion>

<Accordion title="jira/search_by_jql">
    **Description:** Search issues by JQL in Jira.

* `jqlQuery` (string, required): JQL Query (example: "project = PROJECT").
    * `paginationParameters` (object, optional): Pagination parameters for paginated results.
      
  </Accordion>

<Accordion title="jira/update_issue_any">
    **Description:** Update any issue in Jira. Use DESCRIBE\_ACTION\_SCHEMA to get properties schema for this function.

**Parameters:** No specific parameters - use JIRA\_DESCRIBE\_ACTION\_SCHEMA first to get the expected schema.
  </Accordion>

<Accordion title="jira/describe_action_schema">
    **Description:** Get the expected schema for an issue type. Use this function first if no other function matches the issue type you want to operate on.

* `issueTypeId` (string, required): Issue Type ID.
    * `projectKey` (string, required): Project key.
    * `operation` (string, required): Operation Type value, for example CREATE\_ISSUE or UPDATE\_ISSUE.
  </Accordion>

<Accordion title="jira/get_projects">
    **Description:** Get Projects in Jira.

* `paginationParameters` (object, optional): Pagination Parameters.
      
  </Accordion>

<Accordion title="jira/get_issue_types_by_project">
    **Description:** Get Issue Types by project in Jira.

* `project` (string, required): Project key.
  </Accordion>

<Accordion title="jira/get_issue_types">
    **Description:** Get all Issue Types in Jira.

**Parameters:** None required.
  </Accordion>

<Accordion title="jira/get_issue_status_by_project">
    **Description:** Get issue statuses for a given project.

* `project` (string, required): Project key.
  </Accordion>

<Accordion title="jira/get_all_assignees_by_project">
    **Description:** Get assignees for a given project.

* `project` (string, required): Project key.
  </Accordion>
</AccordionGroup>

### Basic Jira Agent Setup

```python theme={null}
from crewai import Agent, Task, Crew
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

Example 3 (unknown):
```unknown
## Available Actions

<AccordionGroup>
  <Accordion title="jira/create_issue">
    **Description:** Create an issue in Jira.

    **Parameters:**

    * `summary` (string, required): Summary - A brief one-line summary of the issue. (example: "The printer stopped working").
    * `project` (string, optional): Project - The project which the issue belongs to. Defaults to the user's first project if not provided. Use Connect Portal Workflow Settings to allow users to select a Project.
    * `issueType` (string, optional): Issue type - Defaults to Task if not provided.
    * `jiraIssueStatus` (string, optional): Status - Defaults to the project's first status if not provided.
    * `assignee` (string, optional): Assignee - Defaults to the authenticated user if not provided.
    * `descriptionType` (string, optional): Description Type - Select the Description Type.
      * Options: `description`, `descriptionJSON`
    * `description` (string, optional): Description - A detailed description of the issue. This field appears only when 'descriptionType' = 'description'.
    * `additionalFields` (string, optional): Additional Fields - Specify any other fields that should be included in JSON format. Use Connect Portal Workflow Settings to allow users to select which Issue Fields to update.
```

Example 4 (unknown):
```unknown
</Accordion>

  <Accordion title="jira/update_issue">
    **Description:** Update an issue in Jira.

    **Parameters:**

    * `issueKey` (string, required): Issue Key (example: "TEST-1234").
    * `summary` (string, optional): Summary - A brief one-line summary of the issue. (example: "The printer stopped working").
    * `issueType` (string, optional): Issue type - Use Connect Portal Workflow Settings to allow users to select an Issue Type.
    * `jiraIssueStatus` (string, optional): Status - Use Connect Portal Workflow Settings to allow users to select a Status.
    * `assignee` (string, optional): Assignee - Use Connect Portal Workflow Settings to allow users to select an Assignee.
    * `descriptionType` (string, optional): Description Type - Select the Description Type.
      * Options: `description`, `descriptionJSON`
    * `description` (string, optional): Description - A detailed description of the issue. This field appears only when 'descriptionType' = 'description'.
    * `additionalFields` (string, optional): Additional Fields - Specify any other fields that should be included in JSON format.
  </Accordion>

  <Accordion title="jira/get_issue_by_key">
    **Description:** Get an issue by key in Jira.

    **Parameters:**

    * `issueKey` (string, required): Issue Key (example: "TEST-1234").
  </Accordion>

  <Accordion title="jira/filter_issues">
    **Description:** Search issues in Jira using filters.

    **Parameters:**

    * `jqlQuery` (object, optional): A filter in disjunctive normal form - OR of AND groups of single conditions.
```

---

## Knowledge

**URL:** llms-txt#knowledge

**Contents:**
- Overview
- Quickstart Examples
  - Vector store (RAG) client configuration

Source: https://docs.crewai.com/en/concepts/knowledge

What is knowledge in CrewAI and how to use it.

Knowledge in CrewAI is a powerful system that allows AI agents to access and utilize external information sources during their tasks.
Think of it as giving your agents a reference library they can consult while working.

<Info>
  Key benefits of using Knowledge:

* Enhance agents with domain-specific information
  * Support decisions with real-world data
  * Maintain context across conversations
  * Ground responses in factual information
</Info>

## Quickstart Examples

<Tip>
  For file-based Knowledge Sources, make sure to place your files in a `knowledge` directory at the root of your project.
  Also, use relative paths from the `knowledge` directory when creating the source.
</Tip>

### Vector store (RAG) client configuration

CrewAI exposes a provider-neutral RAG client abstraction for vector stores. The default provider is ChromaDB, and Qdrant is supported as well. You can switch providers using configuration utilities.

* ChromaDB (default)
* Qdrant

```python Code theme={null}
from crewai.rag.config.utils import set_rag_config, get_rag_client, clear_rag_config

---

## Langtrace Integration

**URL:** llms-txt#langtrace-integration

Source: https://docs.crewai.com/en/observability/langtrace

How to monitor cost, latency, and performance of CrewAI Agents using Langtrace, an external observability tool.

---

## Langtrace Overview

**URL:** llms-txt#langtrace-overview

**Contents:**
- Setup Instructions
  - Features and Their Application to CrewAI

Langtrace is an open-source, external tool that helps you set up observability and evaluations for Large Language Models (LLMs), LLM frameworks, and Vector Databases.
While not built directly into CrewAI, Langtrace can be used alongside CrewAI to gain deep visibility into the cost, latency, and performance of your CrewAI Agents.
This integration allows you to log hyperparameters, monitor performance regressions, and establish a process for continuous improvement of your Agents.

<img alt="Overview of a select series of agent session runs" />

<img alt="Overview of agent traces" />

<img alt="Overview of llm traces in details" />

## Setup Instructions

<Steps>
  <Step title="Sign up for Langtrace">
    Sign up by visiting [https://langtrace.ai/signup](https://langtrace.ai/signup).
  </Step>

<Step title="Create a project">
    Set the project type to `CrewAI` and generate an API key.
  </Step>

<Step title="Install Langtrace in your CrewAI project">
    Use the following command:

<Step title="Import Langtrace">
    Import and initialize Langtrace at the beginning of your script, before any CrewAI imports:

### Features and Their Application to CrewAI

1. **LLM Token and Cost Tracking**

* Monitor the token usage and associated costs for each CrewAI agent interaction.

2. **Trace Graph for Execution Steps**

* Visualize the execution flow of your CrewAI tasks, including latency and logs.
   * Useful for identifying bottlenecks in your agent workflows.

3. **Dataset Curation with Manual Annotation**

* Create datasets from your CrewAI task outputs for future training or evaluation.

4. **Prompt Versioning and Management**

* Keep track of different versions of prompts used in your CrewAI agents.
   * Useful for A/B testing and optimizing agent performance.

5. **Prompt Playground with Model Comparisons**

* Test and compare different prompts and models for your CrewAI agents before deployment.

6. **Testing and Evaluations**

* Set up automated tests for your CrewAI agents and tasks.

**Examples:**

Example 1 (unknown):
```unknown
</Step>

  <Step title="Import Langtrace">
    Import and initialize Langtrace at the beginning of your script, before any CrewAI imports:
```

---

## Linear Integration

**URL:** llms-txt#linear-integration

**Contents:**
- Overview
- Prerequisites
- Setting Up Linear Integration
  - 1. Connect Your Linear Account
  - 2. Install Required Package
  - 3. Environment Variable Setup
- Available Actions
- Usage Examples
  - Basic Linear Agent Setup

Source: https://docs.crewai.com/en/enterprise/integrations/linear

Software project and bug tracking with Linear integration for CrewAI.

Enable your agents to manage issues, projects, and development workflows through Linear. Create and update issues, manage project timelines, organize teams, and streamline your software development process with AI-powered automation.

Before using the Linear integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A Linear account with appropriate workspace permissions
* Connected your Linear account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)

## Setting Up Linear Integration

### 1. Connect Your Linear Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Linear** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for issue and project management
5. Copy your Enterprise Token from [Integration Settings](https://app.crewai.com/crewai_plus/settings/integrations)

### 2. Install Required Package

### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>

Or add it to your `.env` file:

<AccordionGroup>
  <Accordion title="linear/create_issue">
    **Description:** Create a new issue in Linear.

* `teamId` (string, required): Team ID - Specify the Team ID of the parent for this new issue. Use Connect Portal Workflow Settings to allow users to select a Team ID. (example: "a70bdf0f-530a-4887-857d-46151b52b47c").
    * `title` (string, required): Title - Specify a title for this issue.
    * `description` (string, optional): Description - Specify a description for this issue.
    * `statusId` (string, optional): Status - Specify the state or status of this issue.
    * `priority` (string, optional): Priority - Specify the priority of this issue as an integer.
    * `dueDate` (string, optional): Due Date - Specify the due date of this issue in ISO 8601 format.
    * `cycleId` (string, optional): Cycle ID - Specify the cycle associated with this issue.
    * `additionalFields` (object, optional): Additional Fields.
      
  </Accordion>

<Accordion title="linear/update_issue">
    **Description:** Update an issue in Linear.

* `issueId` (string, required): Issue ID - Specify the Issue ID of the issue to update. (example: "90fbc706-18cd-42c9-ae66-6bd344cc8977").
    * `title` (string, optional): Title - Specify a title for this issue.
    * `description` (string, optional): Description - Specify a description for this issue.
    * `statusId` (string, optional): Status - Specify the state or status of this issue.
    * `priority` (string, optional): Priority - Specify the priority of this issue as an integer.
    * `dueDate` (string, optional): Due Date - Specify the due date of this issue in ISO 8601 format.
    * `cycleId` (string, optional): Cycle ID - Specify the cycle associated with this issue.
    * `additionalFields` (object, optional): Additional Fields.
      
  </Accordion>

<Accordion title="linear/get_issue_by_id">
    **Description:** Get an issue by ID in Linear.

* `issueId` (string, required): Issue ID - Specify the record ID of the issue to fetch. (example: "90fbc706-18cd-42c9-ae66-6bd344cc8977").
  </Accordion>

<Accordion title="linear/get_issue_by_issue_identifier">
    **Description:** Get an issue by issue identifier in Linear.

* `externalId` (string, required): External ID - Specify the human-readable Issue identifier of the issue to fetch. (example: "ABC-1").
  </Accordion>

<Accordion title="linear/search_issue">
    **Description:** Search issues in Linear.

* `queryTerm` (string, required): Query Term - The search term to look for.
    * `issueFilterFormula` (object, optional): A filter in disjunctive normal form - OR of AND groups of single conditions.
      
      Available fields: `title`, `number`, `project`, `createdAt`
      Available operators: `$stringExactlyMatches`, `$stringDoesNotExactlyMatch`, `$stringIsIn`, `$stringIsNotIn`, `$stringStartsWith`, `$stringDoesNotStartWith`, `$stringEndsWith`, `$stringDoesNotEndWith`, `$stringContains`, `$stringDoesNotContain`, `$stringGreaterThan`, `$stringLessThan`, `$numberGreaterThanOrEqualTo`, `$numberLessThanOrEqualTo`, `$numberGreaterThan`, `$numberLessThan`, `$dateTimeAfter`, `$dateTimeBefore`
  </Accordion>

<Accordion title="linear/delete_issue">
    **Description:** Delete an issue in Linear.

* `issueId` (string, required): Issue ID - Specify the record ID of the issue to delete. (example: "90fbc706-18cd-42c9-ae66-6bd344cc8977").
  </Accordion>

<Accordion title="linear/archive_issue">
    **Description:** Archive an issue in Linear.

* `issueId` (string, required): Issue ID - Specify the record ID of the issue to archive. (example: "90fbc706-18cd-42c9-ae66-6bd344cc8977").
  </Accordion>

<Accordion title="linear/create_sub_issue">
    **Description:** Create a sub-issue in Linear.

* `parentId` (string, required): Parent ID - Specify the Issue ID for the parent of this new issue.
    * `teamId` (string, required): Team ID - Specify the Team ID of the parent for this new sub-issue. Use Connect Portal Workflow Settings to allow users to select a Team ID. (example: "a70bdf0f-530a-4887-857d-46151b52b47c").
    * `title` (string, required): Title - Specify a title for this issue.
    * `description` (string, optional): Description - Specify a description for this issue.
    * `additionalFields` (object, optional): Additional Fields.
      
  </Accordion>

<Accordion title="linear/create_project">
    **Description:** Create a new project in Linear.

* `teamIds` (object, required): Team ID - Specify the team ID(s) this project is associated with as a string or a JSON array. Use Connect Portal User Settings to allow your user to select a Team ID.
      
    * `projectName` (string, required): Project Name - Specify the name of the project. (example: "My Linear Project").
    * `description` (string, optional): Project Description - Specify a description for this project.
    * `additionalFields` (object, optional): Additional Fields.
      
  </Accordion>

<Accordion title="linear/update_project">
    **Description:** Update a project in Linear.

* `projectId` (string, required): Project ID - Specify the ID of the project to update. (example: "a6634484-6061-4ac7-9739-7dc5e52c796b").
    * `projectName` (string, optional): Project Name - Specify the name of the project to update. (example: "My Linear Project").
    * `description` (string, optional): Project Description - Specify a description for this project.
    * `additionalFields` (object, optional): Additional Fields.
      
  </Accordion>

<Accordion title="linear/get_project_by_id">
    **Description:** Get a project by ID in Linear.

* `projectId` (string, required): Project ID - Specify the Project ID of the project to fetch. (example: "a6634484-6061-4ac7-9739-7dc5e52c796b").
  </Accordion>

<Accordion title="linear/delete_project">
    **Description:** Delete a project in Linear.

* `projectId` (string, required): Project ID - Specify the Project ID of the project to delete. (example: "a6634484-6061-4ac7-9739-7dc5e52c796b").
  </Accordion>

<Accordion title="linear/search_teams">
    **Description:** Search teams in Linear.

* `teamFilterFormula` (object, optional): A filter in disjunctive normal form - OR of AND groups of single conditions.
      
      Available fields: `id`, `name`
  </Accordion>
</AccordionGroup>

### Basic Linear Agent Setup

```python theme={null}
from crewai import Agent, Task, Crew
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

Example 3 (unknown):
```unknown
## Available Actions

<AccordionGroup>
  <Accordion title="linear/create_issue">
    **Description:** Create a new issue in Linear.

    **Parameters:**

    * `teamId` (string, required): Team ID - Specify the Team ID of the parent for this new issue. Use Connect Portal Workflow Settings to allow users to select a Team ID. (example: "a70bdf0f-530a-4887-857d-46151b52b47c").
    * `title` (string, required): Title - Specify a title for this issue.
    * `description` (string, optional): Description - Specify a description for this issue.
    * `statusId` (string, optional): Status - Specify the state or status of this issue.
    * `priority` (string, optional): Priority - Specify the priority of this issue as an integer.
    * `dueDate` (string, optional): Due Date - Specify the due date of this issue in ISO 8601 format.
    * `cycleId` (string, optional): Cycle ID - Specify the cycle associated with this issue.
    * `additionalFields` (object, optional): Additional Fields.
```

Example 4 (unknown):
```unknown
</Accordion>

  <Accordion title="linear/update_issue">
    **Description:** Update an issue in Linear.

    **Parameters:**

    * `issueId` (string, required): Issue ID - Specify the Issue ID of the issue to update. (example: "90fbc706-18cd-42c9-ae66-6bd344cc8977").
    * `title` (string, optional): Title - Specify a title for this issue.
    * `description` (string, optional): Description - Specify a description for this issue.
    * `statusId` (string, optional): Status - Specify the state or status of this issue.
    * `priority` (string, optional): Priority - Specify the priority of this issue as an integer.
    * `dueDate` (string, optional): Due Date - Specify the due date of this issue in ISO 8601 format.
    * `cycleId` (string, optional): Cycle ID - Specify the cycle associated with this issue.
    * `additionalFields` (object, optional): Additional Fields.
```

---

## `LinkupSearchTool`

**URL:** llms-txt#`linkupsearchtool`

**Contents:**
- Description
- Installation
- Steps to Get Started
- Example

The `LinkupSearchTool` provides the ability to query the Linkup API for contextual information and retrieve structured results. This tool is ideal for enriching workflows with up-to-date and reliable information from Linkup, allowing agents to access relevant data during their tasks.

To use this tool, you need to install the Linkup SDK:

## Steps to Get Started

To effectively use the `LinkupSearchTool`, follow these steps:

1. **API Key**: Obtain a Linkup API key.
2. **Environment Setup**: Set up your environment with the API key.
3. **Install SDK**: Install the Linkup SDK using the command above.

The following example demonstrates how to initialize the tool and use it in an agent:

```python Code theme={null}
from crewai_tools import LinkupSearchTool
from crewai import Agent
import os

**Examples:**

Example 1 (unknown):
```unknown
## Steps to Get Started

To effectively use the `LinkupSearchTool`, follow these steps:

1. **API Key**: Obtain a Linkup API key.
2. **Environment Setup**: Set up your environment with the API key.
3. **Install SDK**: Install the Linkup SDK using the command above.

## Example

The following example demonstrates how to initialize the tool and use it in an agent:
```

---

## List all available organizations

**URL:** llms-txt#list-all-available-organizations

<Note>
  When loading agents from repositories, you must be authenticated and switched to the correct organization. If you receive errors, check your authentication status and organization settings using the CLI commands above.
</Note>

---

## `LlamaIndexTool`

**URL:** llms-txt#`llamaindextool`

**Contents:**
- Description
- Installation
- Steps to Get Started
- Example
  - From a LlamaIndex Tool

The `LlamaIndexTool` is designed to be a general wrapper around LlamaIndex tools and query engines, enabling you to leverage LlamaIndex resources in terms of RAG/agentic pipelines as tools to plug into CrewAI agents. This tool allows you to seamlessly integrate LlamaIndex's powerful data processing and retrieval capabilities into your CrewAI workflows.

To use this tool, you need to install LlamaIndex:

## Steps to Get Started

To effectively use the `LlamaIndexTool`, follow these steps:

1. **Install LlamaIndex**: Install the LlamaIndex package using the command above.
2. **Set Up LlamaIndex**: Follow the [LlamaIndex documentation](https://docs.llamaindex.ai/) to set up a RAG/agent pipeline.
3. **Create a Tool or Query Engine**: Create a LlamaIndex tool or query engine that you want to use with CrewAI.

The following examples demonstrate how to initialize the tool from different LlamaIndex components:

### From a LlamaIndex Tool

```python Code theme={null}
from crewai_tools import LlamaIndexTool
from crewai import Agent
from llama_index.core.tools import FunctionTool

**Examples:**

Example 1 (unknown):
```unknown
## Steps to Get Started

To effectively use the `LlamaIndexTool`, follow these steps:

1. **Install LlamaIndex**: Install the LlamaIndex package using the command above.
2. **Set Up LlamaIndex**: Follow the [LlamaIndex documentation](https://docs.llamaindex.ai/) to set up a RAG/agent pipeline.
3. **Create a Tool or Query Engine**: Create a LlamaIndex tool or query engine that you want to use with CrewAI.

## Example

The following examples demonstrate how to initialize the tool from different LlamaIndex components:

### From a LlamaIndex Tool
```

---

## LLMs

**URL:** llms-txt#llms

**Contents:**
- Overview
- What are LLMs?
- Setting up your LLM
- Provider Configuration Examples
- Streaming Responses
- Async LLM Calls
- Structured LLM Calls

Source: https://docs.crewai.com/en/concepts/llms

A comprehensive guide to configuring and using Large Language Models (LLMs) in your CrewAI projects

CrewAI integrates with multiple LLM providers through providers native sdks, giving you the flexibility to choose the right model for your specific use case. This guide will help you understand how to configure and use different LLM providers in your CrewAI projects.

Large Language Models (LLMs) are the core intelligence behind CrewAI agents. They enable agents to understand context, make decisions, and generate human-like responses. Here's what you need to know:

<CardGroup>
  <Card title="LLM Basics" icon="brain">
    Large Language Models are AI systems trained on vast amounts of text data. They power the intelligence of your CrewAI agents, enabling them to understand and generate human-like text.
  </Card>

<Card title="Context Window" icon="window">
    The context window determines how much text an LLM can process at once. Larger windows (e.g., 128K tokens) allow for more context but may be more expensive and slower.
  </Card>

<Card title="Temperature" icon="temperature-three-quarters">
    Temperature (0.0 to 1.0) controls response randomness. Lower values (e.g., 0.2) produce more focused, deterministic outputs, while higher values (e.g., 0.8) increase creativity and variability.
  </Card>

<Card title="Provider Selection" icon="server">
    Each LLM provider (e.g., OpenAI, Anthropic, Google) offers different models with varying capabilities, pricing, and features. Choose based on your needs for accuracy, speed, and cost.
  </Card>
</CardGroup>

## Setting up your LLM

There are different places in CrewAI code where you can specify the model to use. Once you specify the model you are using, you will need to provide the configuration (like an API key) for each of the model providers you use. See the [provider configuration examples](#provider-configuration-examples) section for your provider.

<Tabs>
  <Tab title="1. Environment Variables">
    The simplest way to get started. Set the model in your environment directly, through an `.env` file or in your app code. If you used `crewai create` to bootstrap your project, it will be set already.

<Warning>
      Never commit API keys to version control. Use environment files (.env) or your system's secret management.
    </Warning>
  </Tab>

<Tab title="2. YAML Configuration">
    Create a YAML file to define your agent configurations. This method is great for version control and team collaboration:

<Info>
      The YAML configuration allows you to:

* Version control your agent settings
      * Easily switch between different models
      * Share configurations across team members
      * Document model choices and their purposes
    </Info>
  </Tab>

<Tab title="3. Direct Code">
    For maximum flexibility, configure LLMs directly in your Python code:

<Info>
      Parameter explanations:

* `temperature`: Controls randomness (0.0-1.0)
      * `timeout`: Maximum wait time for response
      * `max_tokens`: Limits response length
      * `top_p`: Alternative to temperature for sampling
      * `frequency_penalty`: Reduces word repetition
      * `presence_penalty`: Encourages new topics
      * `response_format`: Specifies output structure
      * `seed`: Ensures consistent outputs
    </Info>
  </Tab>
</Tabs>

## Provider Configuration Examples

CrewAI supports a multitude of LLM providers, each offering unique features, authentication methods, and model capabilities.
In this section, you'll find detailed examples that help you select, configure, and optimize the LLM that best fits your project's needs.

<AccordionGroup>
  <Accordion title="OpenAI">
    CrewAI provides native integration with OpenAI through the OpenAI Python SDK.

**Advanced Configuration:**

**Structured Outputs:**

**Supported Environment Variables:**

* `OPENAI_API_KEY`: Your OpenAI API key (required)
    * `OPENAI_BASE_URL`: Custom base URL for OpenAI API (optional)

* Native function calling support (except o1 models)
    * Structured outputs with JSON schema
    * Streaming support for real-time responses
    * Token usage tracking
    * Stop sequences support (except o1 models)
    * Log probabilities for token-level insights
    * Reasoning effort control for o1 models

**Supported Models:**

| Model        | Context Window | Best For                                    |
    | ------------ | -------------- | ------------------------------------------- |
    | gpt-4.1      | 1M tokens      | Latest model with enhanced capabilities     |
    | gpt-4.1-mini | 1M tokens      | Efficient version with large context        |
    | gpt-4.1-nano | 1M tokens      | Ultra-efficient variant                     |
    | gpt-4o       | 128,000 tokens | Optimized for speed and intelligence        |
    | gpt-4o-mini  | 200,000 tokens | Cost-effective with large context           |
    | gpt-4-turbo  | 128,000 tokens | Long-form content, document analysis        |
    | gpt-4        | 8,192 tokens   | High-accuracy tasks, complex reasoning      |
    | o1           | 200,000 tokens | Advanced reasoning, complex problem-solving |
    | o1-preview   | 128,000 tokens | Preview of reasoning capabilities           |
    | o1-mini      | 128,000 tokens | Efficient reasoning model                   |
    | o3-mini      | 200,000 tokens | Lightweight reasoning model                 |
    | o4-mini      | 200,000 tokens | Next-gen efficient reasoning                |

**Note:** To use OpenAI, install the required dependencies:

<Accordion title="Meta-Llama">
    Meta's Llama API provides access to Meta's family of large language models.
    The API is available through the [Meta Llama API](https://llama.developer.meta.com?utm_source=partner-crewai\&utm_medium=website).
    Set the following environment variables in your `.env` file:

Example usage in your CrewAI project:

All models listed here [https://llama.developer.meta.com/docs/models/](https://llama.developer.meta.com/docs/models/) are supported.

| Model ID                                            | Input context length | Output context length | Input Modalities | Output Modalities |
    | --------------------------------------------------- | -------------------- | --------------------- | ---------------- | ----------------- |
    | `meta_llama/Llama-4-Scout-17B-16E-Instruct-FP8`     | 128k                 | 4028                  | Text, Image      | Text              |
    | `meta_llama/Llama-4-Maverick-17B-128E-Instruct-FP8` | 128k                 | 4028                  | Text, Image      | Text              |
    | `meta_llama/Llama-3.3-70B-Instruct`                 | 128k                 | 4028                  | Text             | Text              |
    | `meta_llama/Llama-3.3-8B-Instruct`                  | 128k                 | 4028                  | Text             | Text              |
  </Accordion>

<Accordion title="Anthropic">
    CrewAI provides native integration with Anthropic through the Anthropic Python SDK.

**Advanced Configuration:**

**Extended Thinking (Claude Sonnet 4 and Beyond):**

CrewAI supports Anthropic's Extended Thinking feature, which allows Claude to think through problems in a more human-like way before responding. This is particularly useful for complex reasoning, analysis, and problem-solving tasks.

**Thinking Configuration Options:**

* `type`: Set to `"enabled"` to activate extended thinking mode
    * `budget_tokens` (optional): Maximum tokens to use for thinking (helps control costs)

**Models Supporting Extended Thinking:**

* `claude-sonnet-4` and newer models
    * `claude-3-7-sonnet` (with extended thinking capabilities)

**When to Use Extended Thinking:**

* Complex reasoning and multi-step problem solving
    * Mathematical calculations and proofs
    * Code analysis and debugging
    * Strategic planning and decision making
    * Research and analytical tasks

**Note:** Extended thinking consumes additional tokens but can significantly improve response quality for complex tasks.

**Supported Environment Variables:**

* `ANTHROPIC_API_KEY`: Your Anthropic API key (required)

* Native tool use support for Claude 3+ models
    * Extended Thinking support for Claude Sonnet 4+
    * Streaming support for real-time responses
    * Automatic system message handling
    * Stop sequences for controlled output
    * Token usage tracking
    * Multi-turn tool use conversations

* `max_tokens` is a **required** parameter for all Anthropic models
    * Claude uses `stop_sequences` instead of `stop`
    * System messages are handled separately from conversation messages
    * First message must be from the user (automatically handled)
    * Messages must alternate between user and assistant

**Supported Models:**

| Model                      | Context Window | Best For                                   |
    | -------------------------- | -------------- | ------------------------------------------ |
    | claude-sonnet-4            | 200,000 tokens | Latest with extended thinking capabilities |
    | claude-3-7-sonnet          | 200,000 tokens | Advanced reasoning and agentic tasks       |
    | claude-3-5-sonnet-20241022 | 200,000 tokens | Latest Sonnet with best performance        |
    | claude-3-5-haiku           | 200,000 tokens | Fast, compact model for quick responses    |
    | claude-3-opus              | 200,000 tokens | Most capable for complex tasks             |
    | claude-3-sonnet            | 200,000 tokens | Balanced intelligence and speed            |
    | claude-3-haiku             | 200,000 tokens | Fastest for simple tasks                   |
    | claude-2.1                 | 200,000 tokens | Extended context, reduced hallucinations   |
    | claude-2                   | 100,000 tokens | Versatile model for various tasks          |
    | claude-instant             | 100,000 tokens | Fast, cost-effective for everyday tasks    |

**Note:** To use Anthropic, install the required dependencies:

<Accordion title="Google (Gemini API)">
    CrewAI provides native integration with Google Gemini through the Google Gen AI Python SDK.

Set your API key in your `.env` file. If you need a key, check [AI Studio](https://aistudio.google.com/apikey).

**Advanced Configuration:**

**Vertex AI Configuration:**

**Supported Environment Variables:**

* `GOOGLE_API_KEY` or `GEMINI_API_KEY`: Your Google API key (required for Gemini API)
    * `GOOGLE_CLOUD_PROJECT`: Google Cloud project ID (for Vertex AI)
    * `GOOGLE_CLOUD_LOCATION`: GCP location (defaults to `us-central1`)
    * `GOOGLE_GENAI_USE_VERTEXAI`: Set to `true` to use Vertex AI

* Native function calling support for Gemini 1.5+ and 2.x models
    * Streaming support for real-time responses
    * Multimodal capabilities (text, images, video)
    * Safety settings configuration
    * Support for both Gemini API and Vertex AI
    * Automatic system instruction handling
    * Token usage tracking

Google offers a range of powerful models optimized for different use cases.

| Model                     | Context Window | Best For                                                  |
    | ------------------------- | -------------- | --------------------------------------------------------- |
    | gemini-2.5-flash          | 1M tokens      | Adaptive thinking, cost efficiency                        |
    | gemini-2.5-pro            | 1M tokens      | Enhanced thinking and reasoning, multimodal understanding |
    | gemini-2.0-flash          | 1M tokens      | Next generation features, speed, thinking                 |
    | gemini-2.0-flash-thinking | 32,768 tokens  | Advanced reasoning with thinking process                  |
    | gemini-2.0-flash-lite     | 1M tokens      | Cost efficiency and low latency                           |
    | gemini-1.5-pro            | 2M tokens      | Best performing, logical reasoning, coding                |
    | gemini-1.5-flash          | 1M tokens      | Balanced multimodal model, good for most tasks            |
    | gemini-1.5-flash-8b       | 1M tokens      | Fastest, most cost-efficient                              |
    | gemini-1.0-pro            | 32,768 tokens  | Earlier generation model                                  |

The Gemini API also supports [Gemma models](https://ai.google.dev/gemma/docs) hosted on Google infrastructure.

| Model       | Context Window | Best For                            |
    | ----------- | -------------- | ----------------------------------- |
    | gemma-3-1b  | 32,000 tokens  | Ultra-lightweight tasks             |
    | gemma-3-4b  | 128,000 tokens | Efficient general-purpose tasks     |
    | gemma-3-12b | 128,000 tokens | Balanced performance and efficiency |
    | gemma-3-27b | 128,000 tokens | High-performance tasks              |

**Note:** To use Google Gemini, install the required dependencies:

The full list of models is available in the [Gemini model docs](https://ai.google.dev/gemini-api/docs/models).
  </Accordion>

<Accordion title="Google (Vertex AI)">
    Get credentials from your Google Cloud Console and save it to a JSON file, then load it with the following code:

Example usage in your CrewAI project:

Google offers a range of powerful models optimized for different use cases:

| Model                          | Context Window | Best For                                                                                                         |
    | ------------------------------ | -------------- | ---------------------------------------------------------------------------------------------------------------- |
    | gemini-2.5-flash-preview-04-17 | 1M tokens      | Adaptive thinking, cost efficiency                                                                               |
    | gemini-2.5-pro-preview-05-06   | 1M tokens      | Enhanced thinking and reasoning, multimodal understanding, advanced coding, and more                             |
    | gemini-2.0-flash               | 1M tokens      | Next generation features, speed, thinking, and realtime streaming                                                |
    | gemini-2.0-flash-lite          | 1M tokens      | Cost efficiency and low latency                                                                                  |
    | gemini-1.5-flash               | 1M tokens      | Balanced multimodal model, good for most tasks                                                                   |
    | gemini-1.5-flash-8B            | 1M tokens      | Fastest, most cost-efficient, good for high-frequency tasks                                                      |
    | gemini-1.5-pro                 | 2M tokens      | Best performing, wide variety of reasoning tasks including logical reasoning, coding, and creative collaboration |
  </Accordion>

<Accordion title="Azure">
    CrewAI provides native integration with Azure AI Inference and Azure OpenAI through the Azure AI Inference Python SDK.

**Endpoint URL Formats:**

For Azure OpenAI deployments:

For Azure AI Inference endpoints:

**Advanced Configuration:**

**Supported Environment Variables:**

* `AZURE_API_KEY`: Your Azure API key (required)
    * `AZURE_ENDPOINT`: Your Azure endpoint URL (required, also checks `AZURE_OPENAI_ENDPOINT` and `AZURE_API_BASE`)
    * `AZURE_API_VERSION`: API version (optional, defaults to `2024-06-01`)

* Native function calling support for Azure OpenAI models (gpt-4, gpt-4o, gpt-3.5-turbo, etc.)
    * Streaming support for real-time responses
    * Automatic endpoint URL validation and correction
    * Comprehensive error handling with retry logic
    * Token usage tracking

**Note:** To use Azure AI Inference, install the required dependencies:

<Accordion title="AWS Bedrock">
    CrewAI provides native integration with AWS Bedrock through the boto3 SDK using the Converse API.

**Advanced Configuration:**

**Supported Environment Variables:**

* `AWS_ACCESS_KEY_ID`: AWS access key (required)
    * `AWS_SECRET_ACCESS_KEY`: AWS secret key (required)
    * `AWS_SESSION_TOKEN`: AWS session token for temporary credentials (optional)
    * `AWS_DEFAULT_REGION`: AWS region (defaults to `us-east-1`)

* Native tool calling support via Converse API
    * Streaming and non-streaming responses
    * Comprehensive error handling with retry logic
    * Guardrail configuration for content filtering
    * Model-specific parameters via `additional_model_request_fields`
    * Token usage tracking and stop reason logging
    * Support for all Bedrock foundation models
    * Automatic conversation format handling

* Uses the modern Converse API for unified model access
    * Automatic handling of model-specific conversation requirements
    * System messages are handled separately from conversation
    * First message must be from user (automatically handled)
    * Some models (like Cohere) require conversation to end with user message

[Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html) is a managed service that provides access to multiple foundation models from top AI companies through a unified API.

| Model                   | Context Window     | Best For                                                                                                                              |
    | ----------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
    | Amazon Nova Pro         | Up to 300k tokens  | High-performance, model balancing accuracy, speed, and cost-effectiveness across diverse tasks.                                       |
    | Amazon Nova Micro       | Up to 128k tokens  | High-performance, cost-effective text-only model optimized for lowest latency responses.                                              |
    | Amazon Nova Lite        | Up to 300k tokens  | High-performance, affordable multimodal processing for images, video, and text with real-time capabilities.                           |
    | Claude 3.7 Sonnet       | Up to 128k tokens  | High-performance, best for complex reasoning, coding & AI agents                                                                      |
    | Claude 3.5 Sonnet v2    | Up to 200k tokens  | State-of-the-art model specialized in software engineering, agentic capabilities, and computer interaction at optimized cost.         |
    | Claude 3.5 Sonnet       | Up to 200k tokens  | High-performance model delivering superior intelligence and reasoning across diverse tasks with optimal speed-cost balance.           |
    | Claude 3.5 Haiku        | Up to 200k tokens  | Fast, compact multimodal model optimized for quick responses and seamless human-like interactions                                     |
    | Claude 3 Sonnet         | Up to 200k tokens  | Multimodal model balancing intelligence and speed for high-volume deployments.                                                        |
    | Claude 3 Haiku          | Up to 200k tokens  | Compact, high-speed multimodal model optimized for quick responses and natural conversational interactions                            |
    | Claude 3 Opus           | Up to 200k tokens  | Most advanced multimodal model exceling at complex tasks with human-like reasoning and superior contextual understanding.             |
    | Claude 2.1              | Up to 200k tokens  | Enhanced version with expanded context window, improved reliability, and reduced hallucinations for long-form and RAG applications    |
    | Claude                  | Up to 100k tokens  | Versatile model excelling in sophisticated dialogue, creative content, and precise instruction following.                             |
    | Claude Instant          | Up to 100k tokens  | Fast, cost-effective model for everyday tasks like dialogue, analysis, summarization, and document Q\&A                               |
    | Llama 3.1 405B Instruct | Up to 128k tokens  | Advanced LLM for synthetic data generation, distillation, and inference for chatbots, coding, and domain-specific tasks.              |
    | Llama 3.1 70B Instruct  | Up to 128k tokens  | Powers complex conversations with superior contextual understanding, reasoning and text generation.                                   |
    | Llama 3.1 8B Instruct   | Up to 128k tokens  | Advanced state-of-the-art model with language understanding, superior reasoning, and text generation.                                 |
    | Llama 3 70B Instruct    | Up to 8k tokens    | Powers complex conversations with superior contextual understanding, reasoning and text generation.                                   |
    | Llama 3 8B Instruct     | Up to 8k tokens    | Advanced state-of-the-art LLM with language understanding, superior reasoning, and text generation.                                   |
    | Titan Text G1 - Lite    | Up to 4k tokens    | Lightweight, cost-effective model optimized for English tasks and fine-tuning with focus on summarization and content generation.     |
    | Titan Text G1 - Express | Up to 8k tokens    | Versatile model for general language tasks, chat, and RAG applications with support for English and 100+ languages.                   |
    | Cohere Command          | Up to 4k tokens    | Model specialized in following user commands and delivering practical enterprise solutions.                                           |
    | Jurassic-2 Mid          | Up to 8,191 tokens | Cost-effective model balancing quality and affordability for diverse language tasks like Q\&A, summarization, and content generation. |
    | Jurassic-2 Ultra        | Up to 8,191 tokens | Model for advanced text generation and comprehension, excelling in complex tasks like analysis and content creation.                  |
    | Jamba-Instruct          | Up to 256k tokens  | Model with extended context window optimized for cost-effective text generation, summarization, and Q\&A.                             |
    | Mistral 7B Instruct     | Up to 32k tokens   | This LLM follows instructions, completes requests, and generates creative text.                                                       |
    | Mistral 8x7B Instruct   | Up to 32k tokens   | An MOE LLM that follows instructions, completes requests, and generates creative text.                                                |
    | DeepSeek R1             | 32,768 tokens      | Advanced reasoning model                                                                                                              |

**Note:** To use AWS Bedrock, install the required dependencies:

<Accordion title="Amazon SageMaker">

Example usage in your CrewAI project:

<Accordion title="Mistral">
    Set the following environment variables in your `.env` file:

Example usage in your CrewAI project:

<Accordion title="Nvidia NIM">
    Set the following environment variables in your `.env` file:

Example usage in your CrewAI project:

Nvidia NIM provides a comprehensive suite of models for various use cases, from general-purpose tasks to specialized applications.

| Model                                       | Context Window | Best For                                                                                                                    |
    | ------------------------------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------- |
    | nvidia/mistral-nemo-minitron-8b-8k-instruct | 8,192 tokens   | State-of-the-art small language model delivering superior accuracy for chatbot, virtual assistants, and content generation. |
    | nvidia/nemotron-4-mini-hindi-4b-instruct    | 4,096 tokens   | A bilingual Hindi-English SLM for on-device inference, tailored specifically for Hindi Language.                            |
    | nvidia/llama-3.1-nemotron-70b-instruct      | 128k tokens    | Customized for enhanced helpfulness in responses                                                                            |
    | nvidia/llama3-chatqa-1.5-8b                 | 128k tokens    | Advanced LLM to generate high-quality, context-aware responses for chatbots and search engines.                             |
    | nvidia/llama3-chatqa-1.5-70b                | 128k tokens    | Advanced LLM to generate high-quality, context-aware responses for chatbots and search engines.                             |
    | nvidia/vila                                 | 128k tokens    | Multi-modal vision-language model that understands text/img/video and creates informative responses                         |
    | nvidia/neva-22                              | 4,096 tokens   | Multi-modal vision-language model that understands text/images and generates informative responses                          |
    | nvidia/nemotron-mini-4b-instruct            | 8,192 tokens   | General-purpose tasks                                                                                                       |
    | nvidia/usdcode-llama3-70b-instruct          | 128k tokens    | State-of-the-art LLM that answers OpenUSD knowledge queries and generates USD-Python code.                                  |
    | nvidia/nemotron-4-340b-instruct             | 4,096 tokens   | Creates diverse synthetic data that mimics the characteristics of real-world data.                                          |
    | meta/codellama-70b                          | 100k tokens    | LLM capable of generating code from natural language and vice versa.                                                        |
    | meta/llama2-70b                             | 4,096 tokens   | Cutting-edge large language AI model capable of generating text and code in response to prompts.                            |
    | meta/llama3-8b-instruct                     | 8,192 tokens   | Advanced state-of-the-art LLM with language understanding, superior reasoning, and text generation.                         |
    | meta/llama3-70b-instruct                    | 8,192 tokens   | Powers complex conversations with superior contextual understanding, reasoning and text generation.                         |
    | meta/llama-3.1-8b-instruct                  | 128k tokens    | Advanced state-of-the-art model with language understanding, superior reasoning, and text generation.                       |
    | meta/llama-3.1-70b-instruct                 | 128k tokens    | Powers complex conversations with superior contextual understanding, reasoning and text generation.                         |
    | meta/llama-3.1-405b-instruct                | 128k tokens    | Advanced LLM for synthetic data generation, distillation, and inference for chatbots, coding, and domain-specific tasks.    |
    | meta/llama-3.2-1b-instruct                  | 128k tokens    | Advanced state-of-the-art small language model with language understanding, superior reasoning, and text generation.        |
    | meta/llama-3.2-3b-instruct                  | 128k tokens    | Advanced state-of-the-art small language model with language understanding, superior reasoning, and text generation.        |
    | meta/llama-3.2-11b-vision-instruct          | 128k tokens    | Advanced state-of-the-art small language model with language understanding, superior reasoning, and text generation.        |
    | meta/llama-3.2-90b-vision-instruct          | 128k tokens    | Advanced state-of-the-art small language model with language understanding, superior reasoning, and text generation.        |
    | google/gemma-7b                             | 8,192 tokens   | Cutting-edge text generation model text understanding, transformation, and code generation.                                 |
    | google/gemma-2b                             | 8,192 tokens   | Cutting-edge text generation model text understanding, transformation, and code generation.                                 |
    | google/codegemma-7b                         | 8,192 tokens   | Cutting-edge model built on Google's Gemma-7B specialized for code generation and code completion.                          |
    | google/codegemma-1.1-7b                     | 8,192 tokens   | Advanced programming model for code generation, completion, reasoning, and instruction following.                           |
    | google/recurrentgemma-2b                    | 8,192 tokens   | Novel recurrent architecture based language model for faster inference when generating long sequences.                      |
    | google/gemma-2-9b-it                        | 8,192 tokens   | Cutting-edge text generation model text understanding, transformation, and code generation.                                 |
    | google/gemma-2-27b-it                       | 8,192 tokens   | Cutting-edge text generation model text understanding, transformation, and code generation.                                 |
    | google/gemma-2-2b-it                        | 8,192 tokens   | Cutting-edge text generation model text understanding, transformation, and code generation.                                 |
    | google/deplot                               | 512 tokens     | One-shot visual language understanding model that translates images of plots into tables.                                   |
    | google/paligemma                            | 8,192 tokens   | Vision language model adept at comprehending text and visual inputs to produce informative responses.                       |
    | mistralai/mistral-7b-instruct-v0.2          | 32k tokens     | This LLM follows instructions, completes requests, and generates creative text.                                             |
    | mistralai/mixtral-8x7b-instruct-v0.1        | 8,192 tokens   | An MOE LLM that follows instructions, completes requests, and generates creative text.                                      |
    | mistralai/mistral-large                     | 4,096 tokens   | Creates diverse synthetic data that mimics the characteristics of real-world data.                                          |
    | mistralai/mixtral-8x22b-instruct-v0.1       | 8,192 tokens   | Creates diverse synthetic data that mimics the characteristics of real-world data.                                          |
    | mistralai/mistral-7b-instruct-v0.3          | 32k tokens     | This LLM follows instructions, completes requests, and generates creative text.                                             |
    | nv-mistralai/mistral-nemo-12b-instruct      | 128k tokens    | Most advanced language model for reasoning, code, multilingual tasks; runs on a single GPU.                                 |
    | mistralai/mamba-codestral-7b-v0.1           | 256k tokens    | Model for writing and interacting with code across a wide range of programming languages and tasks.                         |
    | microsoft/phi-3-mini-128k-instruct          | 128K tokens    | Lightweight, state-of-the-art open LLM with strong math and logical reasoning skills.                                       |
    | microsoft/phi-3-mini-4k-instruct            | 4,096 tokens   | Lightweight, state-of-the-art open LLM with strong math and logical reasoning skills.                                       |
    | microsoft/phi-3-small-8k-instruct           | 8,192 tokens   | Lightweight, state-of-the-art open LLM with strong math and logical reasoning skills.                                       |
    | microsoft/phi-3-small-128k-instruct         | 128K tokens    | Lightweight, state-of-the-art open LLM with strong math and logical reasoning skills.                                       |
    | microsoft/phi-3-medium-4k-instruct          | 4,096 tokens   | Lightweight, state-of-the-art open LLM with strong math and logical reasoning skills.                                       |
    | microsoft/phi-3-medium-128k-instruct        | 128K tokens    | Lightweight, state-of-the-art open LLM with strong math and logical reasoning skills.                                       |
    | microsoft/phi-3.5-mini-instruct             | 128K tokens    | Lightweight multilingual LLM powering AI applications in latency bound, memory/compute constrained environments             |
    | microsoft/phi-3.5-moe-instruct              | 128K tokens    | Advanced LLM based on Mixture of Experts architecture to deliver compute efficient content generation                       |
    | microsoft/kosmos-2                          | 1,024 tokens   | Groundbreaking multimodal model designed to understand and reason about visual elements in images.                          |
    | microsoft/phi-3-vision-128k-instruct        | 128k tokens    | Cutting-edge open multimodal model exceling in high-quality reasoning from images.                                          |
    | microsoft/phi-3.5-vision-instruct           | 128k tokens    | Cutting-edge open multimodal model exceling in high-quality reasoning from images.                                          |
    | databricks/dbrx-instruct                    | 12k tokens     | A general-purpose LLM with state-of-the-art performance in language understanding, coding, and RAG.                         |
    | snowflake/arctic                            | 1,024 tokens   | Delivers high efficiency inference for enterprise applications focused on SQL generation and coding.                        |
    | aisingapore/sea-lion-7b-instruct            | 4,096 tokens   | LLM to represent and serve the linguistic and cultural diversity of Southeast Asia                                          |
    | ibm/granite-8b-code-instruct                | 4,096 tokens   | Software programming LLM for code generation, completion, explanation, and multi-turn conversion.                           |
    | ibm/granite-34b-code-instruct               | 8,192 tokens   | Software programming LLM for code generation, completion, explanation, and multi-turn conversion.                           |
    | ibm/granite-3.0-8b-instruct                 | 4,096 tokens   | Advanced Small Language Model supporting RAG, summarization, classification, code, and agentic AI                           |
    | ibm/granite-3.0-3b-a800m-instruct           | 4,096 tokens   | Highly efficient Mixture of Experts model for RAG, summarization, entity extraction, and classification                     |
    | mediatek/breeze-7b-instruct                 | 4,096 tokens   | Creates diverse synthetic data that mimics the characteristics of real-world data.                                          |
    | upstage/solar-10.7b-instruct                | 4,096 tokens   | Excels in NLP tasks, particularly in instruction-following, reasoning, and mathematics.                                     |
    | writer/palmyra-med-70b-32k                  | 32k tokens     | Leading LLM for accurate, contextually relevant responses in the medical domain.                                            |
    | writer/palmyra-med-70b                      | 32k tokens     | Leading LLM for accurate, contextually relevant responses in the medical domain.                                            |
    | writer/palmyra-fin-70b-32k                  | 32k tokens     | Specialized LLM for financial analysis, reporting, and data processing                                                      |
    | 01-ai/yi-large                              | 32k tokens     | Powerful model trained on English and Chinese for diverse tasks including chatbot and creative writing.                     |
    | deepseek-ai/deepseek-coder-6.7b-instruct    | 2k tokens      | Powerful coding model offering advanced capabilities in code generation, completion, and infilling                          |
    | rakuten/rakutenai-7b-instruct               | 1,024 tokens   | Advanced state-of-the-art LLM with language understanding, superior reasoning, and text generation.                         |
    | rakuten/rakutenai-7b-chat                   | 1,024 tokens   | Advanced state-of-the-art LLM with language understanding, superior reasoning, and text generation.                         |
    | baichuan-inc/baichuan2-13b-chat             | 4,096 tokens   | Support Chinese and English chat, coding, math, instruction following, solving quizzes                                      |
  </Accordion>

<Accordion title="Local NVIDIA NIM Deployed using WSL2">
    NVIDIA NIM enables you to run powerful LLMs locally on your Windows machine using WSL2 (Windows Subsystem for Linux).
    This approach allows you to leverage your NVIDIA GPU for private, secure, and cost-effective AI inference without relying on cloud services.
    Perfect for development, testing, or production scenarios where data privacy or offline capabilities are required.

Here is a step-by-step guide to setting up a local NVIDIA NIM model:

1. Follow installation instructions from [NVIDIA Website](https://docs.nvidia.com/nim/wsl2/latest/getting-started.html)

2. Install the local model. For Llama 3.1-8b follow [instructions](https://build.nvidia.com/meta/llama-3_1-8b-instruct/deploy)

3. Configure your crewai local models:

<Accordion title="Groq">
    Set the following environment variables in your `.env` file:

Example usage in your CrewAI project:

| Model            | Context Window | Best For                              |
    | ---------------- | -------------- | ------------------------------------- |
    | Llama 3.1 70B/8B | 131,072 tokens | High-performance, large context tasks |
    | Llama 3.2 Series | 8,192 tokens   | General-purpose tasks                 |
    | Mixtral 8x7B     | 32,768 tokens  | Balanced performance and context      |
  </Accordion>

<Accordion title="IBM watsonx.ai">
    Set the following environment variables in your `.env` file:

Example usage in your CrewAI project:

<Accordion title="Ollama (Local LLMs)">
    1. Install Ollama: [ollama.ai](https://ollama.ai/)
    2. Run a model: `ollama run llama3`
    3. Configure:

<Accordion title="Fireworks AI">
    Set the following environment variables in your `.env` file:

Example usage in your CrewAI project:

<Accordion title="Perplexity AI">
    Set the following environment variables in your `.env` file:

Example usage in your CrewAI project:

<Accordion title="Hugging Face">
    Set the following environment variables in your `.env` file:

Example usage in your CrewAI project:

<Accordion title="SambaNova">
    Set the following environment variables in your `.env` file:

Example usage in your CrewAI project:

| Model            | Context Window       | Best For                              |
    | ---------------- | -------------------- | ------------------------------------- |
    | Llama 3.1 70B/8B | Up to 131,072 tokens | High-performance, large context tasks |
    | Llama 3.1 405B   | 8,192 tokens         | High-performance and output quality   |
    | Llama 3.2 Series | 8,192 tokens         | General-purpose, multimodal tasks     |
    | Llama 3.3 70B    | Up to 131,072 tokens | High-performance and output quality   |
    | Qwen2 familly    | 8,192 tokens         | High-performance and output quality   |
  </Accordion>

<Accordion title="Cerebras">
    Set the following environment variables in your `.env` file:

Example usage in your CrewAI project:

<Info>
      Cerebras features:

* Fast inference speeds
      * Competitive pricing
      * Good balance of speed and quality
      * Support for long context windows
    </Info>
  </Accordion>

<Accordion title="Open Router">
    Set the following environment variables in your `.env` file:

Example usage in your CrewAI project:

<Info>
      Open Router models:

* openrouter/deepseek/deepseek-r1
      * openrouter/deepseek/deepseek-chat
    </Info>
  </Accordion>

<Accordion title="Nebius AI Studio">
    Set the following environment variables in your `.env` file:

Example usage in your CrewAI project:

<Info>
      Nebius AI Studio features:

* Large collection of open source models
      * Higher rate limits
      * Competitive pricing
      * Good balance of speed and quality
    </Info>
  </Accordion>
</AccordionGroup>

## Streaming Responses

CrewAI supports streaming responses from LLMs, allowing your application to receive and process outputs in real-time as they're generated.

<Tabs>
  <Tab title="Basic Setup">
    Enable streaming by setting the `stream` parameter to `True` when initializing your LLM:

When streaming is enabled, responses are delivered in chunks as they're generated, creating a more responsive user experience.
  </Tab>

<Tab title="Event Handling">
    CrewAI emits events for each chunk received during streaming:

<Tip>
      [Click here](/en/concepts/event-listener#event-listeners) for more details
    </Tip>
  </Tab>

<Tab title="Agent & Task Tracking">
    All LLM events in CrewAI include agent and task information, allowing you to track and filter LLM interactions by specific agents or tasks:

<Info>
      This feature is particularly useful for:

* Debugging specific agent behaviors
      * Logging LLM usage by task type
      * Auditing which agents are making what types of LLM calls
      * Performance monitoring of specific tasks
    </Info>
  </Tab>
</Tabs>

CrewAI supports asynchronous LLM calls for improved performance and concurrency in your AI workflows. Async calls allow you to run multiple LLM requests concurrently without blocking, making them ideal for high-throughput applications and parallel agent operations.

<Tabs>
  <Tab title="Basic Usage">
    Use the `acall` method for asynchronous LLM requests:

The `acall` method supports all the same parameters as the synchronous `call` method, including messages, tools, and callbacks.
  </Tab>

<Tab title="With Streaming">
    Combine async calls with streaming for real-time concurrent responses:

## Structured LLM Calls

CrewAI supports structured responses from LLM calls by allowing you to define a `response_format` using a Pydantic model. This enables the framework to automatically parse and validate the output, making it easier to integrate the response into your application without manual post-processing.

For example, you can define a Pydantic model to represent the expected response structure and pass it as the `response_format` when instantiating the LLM. The model will then be used to convert the LLM output into a structured Python object.

```python Code theme={null}
from crewai import LLM

class Dog(BaseModel):
    name: str
    age: int
    breed: str

llm = LLM(model="gpt-4o", response_format=Dog)

response = llm.call(
    "Analyze the following messages and return the name, age, and breed. "
    "Meet Kona! She is 3 years old and is a black german shepherd."
)
print(response)

**Examples:**

Example 1 (unknown):
```unknown
<Warning>
      Never commit API keys to version control. Use environment files (.env) or your system's secret management.
    </Warning>
  </Tab>

  <Tab title="2. YAML Configuration">
    Create a YAML file to define your agent configurations. This method is great for version control and team collaboration:
```

Example 2 (unknown):
```unknown
<Info>
      The YAML configuration allows you to:

      * Version control your agent settings
      * Easily switch between different models
      * Share configurations across team members
      * Document model choices and their purposes
    </Info>
  </Tab>

  <Tab title="3. Direct Code">
    For maximum flexibility, configure LLMs directly in your Python code:
```

Example 3 (unknown):
```unknown
<Info>
      Parameter explanations:

      * `temperature`: Controls randomness (0.0-1.0)
      * `timeout`: Maximum wait time for response
      * `max_tokens`: Limits response length
      * `top_p`: Alternative to temperature for sampling
      * `frequency_penalty`: Reduces word repetition
      * `presence_penalty`: Encourages new topics
      * `response_format`: Specifies output structure
      * `seed`: Ensures consistent outputs
    </Info>
  </Tab>
</Tabs>

## Provider Configuration Examples

CrewAI supports a multitude of LLM providers, each offering unique features, authentication methods, and model capabilities.
In this section, you'll find detailed examples that help you select, configure, and optimize the LLM that best fits your project's needs.

<AccordionGroup>
  <Accordion title="OpenAI">
    CrewAI provides native integration with OpenAI through the OpenAI Python SDK.
```

Example 4 (unknown):
```unknown
**Basic Usage:**
```

---

## Load agents from repositories

**URL:** llms-txt#load-agents-from-repositories

researcher = Agent(
    from_repository="market-research-agent"
)

writer = Agent(
    from_repository="content-writer-agent"
)

---

## Load an agent from repository

**URL:** llms-txt#load-an-agent-from-repository

analyst = Agent(
    from_repository="market-analyst-agent",
    verbose=True
)

---

## Managed agent on Bedrock

**URL:** llms-txt#managed-agent-on-bedrock

**Contents:**
- **Best Practices**

knowledge_router = BedrockInvokeAgentTool(
    agent_id="bedrock-agent-id",
    agent_alias_id="prod",
)

automation_strategist = Agent(
    role="Automation Strategist",
    goal="Orchestrate external automations and summarise their output",
    backstory="You coordinate enterprise workflows and know when to delegate tasks to specialised services.",
    tools=[analysis_automation, knowledge_router],
    verbose=True,
)

execute_playbook = Task(
    description="Run the analysis automation and ask the Bedrock agent for executive talking points.",
    agent=automation_strategist,
)

Crew(agents=[automation_strategist], tasks=[execute_playbook]).kickoff()
```

## **Best Practices**

* **Secure credentials**: Store API keys and bearer tokens in environment variables or a secrets manager
* **Plan for latency**: External automations may take longer—set appropriate polling intervals and timeouts
* **Reuse sessions**: Bedrock Agents support session IDs so you can maintain context across multiple tool calls
* **Validate responses**: Normalise remote output (JSON, text, status codes) before forwarding it to downstream tasks
* **Monitor usage**: Track audit logs in CrewAI Platform or AWS CloudWatch to stay ahead of quota limits and failures

---

## Manager agent coordinates the team

**URL:** llms-txt#manager-agent-coordinates-the-team

manager = Agent(
    role="Project Manager",
    goal="Coordinate team efforts and ensure project success",
    backstory="Experienced project manager skilled at delegation and quality control",
    allow_delegation=True,
    verbose=True
)

---

## Maxim Overview

**URL:** llms-txt#maxim-overview

**Contents:**
- Features
  - Prompt Management
  - Observability & Evals
- Getting Started
  - Prerequisites
  - Installation
  - Basic Setup
  - 1. Set up environment variables
  - Environment Variables Setup

Maxim AI provides comprehensive agent monitoring, evaluation, and observability for your CrewAI applications. With Maxim's one-line integration, you can easily trace and analyse agent interactions, performance metrics, and more.

### Prompt Management

Maxim's Prompt Management capabilities enable you to create, organize, and optimize prompts for your CrewAI agents. Rather than hardcoding instructions, leverage Maxim’s SDK to dynamically retrieve and apply version-controlled prompts.

<Tabs>
  <Tab title="Prompt Playground">
    Create, refine, experiment and deploy your prompts via the playground. Organize of your prompts using folders and versions, experimenting with the real world cases by linking tools and context, and deploying based on custom logic.

Easily experiment across models by [**configuring models**](https://www.getmaxim.ai/docs/introduction/quickstart/setting-up-workspace#add-model-api-keys) and selecting the relevant model from the dropdown at the top of the prompt playground.

<Tab title="Prompt Versions">
    As teams build their AI applications, a big part of experimentation is iterating on the prompt structure. In order to collaborate effectively and organize your changes clearly, Maxim allows prompt versioning and comparison runs across versions.

<Tab title="Prompt Comparisons">
    Iterating on Prompts as you evolve your AI application would need experiments across models, prompt structures, etc. In order to compare versions and make informed decisions about changes, the comparison playground allows a side by side view of results.

## **Why use Prompt comparison?**

Prompt comparison combines multiple single Prompts into one view, enabling a streamlined approach for various workflows:

1. **Model comparison**: Evaluate the performance of different models on the same Prompt.
    2. **Prompt optimization**: Compare different versions of a Prompt to identify the most effective formulation.
    3. **Cross-Model consistency**: Ensure consistent outputs across various models for the same Prompt.
    4. **Performance benchmarking**: Analyze metrics like latency, cost, and token count across different models and Prompts.
  </Tab>
</Tabs>

### Observability & Evals

Maxim AI provides comprehensive observability & evaluation for your CrewAI agents, helping you understand exactly what's happening during each execution.

<Tabs>
  <Tab title="Agent Tracing">
    Track your agent’s complete lifecycle, including tool calls, agent trajectories, and decision flows effortlessly.

<Tab title="Analytics + Evals">
    Run detailed evaluations on full traces or individual nodes with support for:

* Multi-step interactions and granular trace analysis
    * Session Level Evaluations
    * Simulations for real-world testing

<CardGroup>
      <Card title="Auto Evals on Logs" icon="e" href="https://www.getmaxim.ai/docs/observe/how-to/evaluate-logs/auto-evaluation">
        <p>
          Evaluate captured logs automatically from the UI based on filters and sampling
        </p>
      </Card>

<Card title="Human Evals on Logs" icon="hand" href="https://www.getmaxim.ai/docs/observe/how-to/evaluate-logs/human-evaluation">
        <p>
          Use human evaluation or rating to assess the quality of your logs and evaluate them.
        </p>
      </Card>

<Card title="Node Level Evals" icon="road" href="https://www.getmaxim.ai/docs/observe/how-to/evaluate-logs/node-level-evaluation">
        <p>
          Evaluate any component of your trace or log to gain insights into your agent’s behavior.
        </p>
      </Card>
    </CardGroup>

<Tab title="Alerting">
    Set thresholds on **error**, **cost, token usage, user feedback, latency** and get real-time alerts via Slack or PagerDuty.

<Tab title="Dashboards">
    Visualize Traces over time, usage metrics, latency & error rates with ease.

<img />
  </Tab>
</Tabs>

* Python version >=3.10
* A Maxim account ([sign up here](https://getmaxim.ai/))
* Generate Maxim API Key
* A CrewAI project

Install the Maxim SDK via pip:

Or add it to your `requirements.txt`:

### 1. Set up environment variables

```python theme={null}
### Environment Variables Setup

**Examples:**

Example 1 (unknown):
```unknown
Or add it to your `requirements.txt`:
```

Example 2 (unknown):
```unknown
### Basic Setup

### 1. Set up environment variables
```

---

## MCP DSL Integration

**URL:** llms-txt#mcp-dsl-integration

**Contents:**
- Overview
- Basic Usage

Source: https://docs.crewai.com/en/mcp/dsl-integration

Learn how to use CrewAI's simple DSL syntax to integrate MCP servers directly with your agents using the mcps field.

CrewAI's MCP DSL (Domain Specific Language) integration provides the **simplest way** to connect your agents to MCP (Model Context Protocol) servers. Just add an `mcps` field to your agent and CrewAI handles all the complexity automatically.

<Info>
  This is the **recommended approach** for most MCP use cases. For advanced scenarios requiring manual connection management, see [MCPServerAdapter](/en/mcp/overview#advanced-mcpserveradapter).
</Info>

Add MCP servers to your agent using the `mcps` field:

```python theme={null}
from crewai import Agent

agent = Agent(
    role="Research Assistant",
    goal="Help with research and analysis tasks",
    backstory="Expert assistant with access to advanced research tools",
    mcps=[
        "https://mcp.exa.ai/mcp?api_key=your_key&profile=research"
    ]
)

---

## MCP Security Considerations

**URL:** llms-txt#mcp-security-considerations

**Contents:**
- Overview
  - Risks
  - 1. Trusting MCP Servers
  - 2. Secure Prompt Injection via Tool Metadata: The "Model Control Protocol" Risk
  - Stdio Transport Security
  - Confused Deputy Attacks
  - Remote Transport Security (SSE & Streamable HTTP)
  - SSE Security Considerations
  - a. DNS Rebinding Attacks (Especially for SSE)
  - b. Use HTTPS

Source: https://docs.crewai.com/en/mcp/security

Learn about important security best practices when integrating MCP servers with your CrewAI agents.

<Warning>
  The most critical aspect of MCP security is **trust**. You should **only** connect your CrewAI agents to MCP servers that you fully trust.
</Warning>

When integrating external services like MCP (Model Context Protocol) servers into your CrewAI agents, security is paramount.
MCP servers can execute code, access data, or interact with other systems based on the tools they expose.
It's crucial to understand the implications and follow best practices to protect your applications and data.

* Execute arbitrary code on the machine where the agent is running (especially with `Stdio` transport if the server can control the command executed).
* Expose sensitive data from your agent or its environment.
* Manipulate your agent's behavior in unintended ways, including making unauthorized API calls on your behalf.
* Hijack your agent's reasoning process through sophisticated prompt injection techniques (see below).

### 1. Trusting MCP Servers

<Warning>
  **Only connect to MCP servers that you trust.**
</Warning>

Before configuring `MCPServerAdapter` to connect to an MCP server, ensure you know:

* **Who operates the server?** Is it a known, reputable service, or an internal server under your control?
* **What tools does it expose?** Understand the capabilities of the tools. Could they be misused if an attacker gained control or if the server itself is malicious?
* **What data does it access or process?** Be aware of any sensitive information that might be sent to or handled by the MCP server.

Avoid connecting to unknown or unverified MCP servers, especially if your agents handle sensitive tasks or data.

### 2. Secure Prompt Injection via Tool Metadata: The "Model Control Protocol" Risk

A significant and subtle risk is the potential for prompt injection through tool metadata. Here's how it works:

1. When your CrewAI agent connects to an MCP server, it typically requests a list of available tools.
2. The MCP server responds with metadata for each tool, including its name, description, and parameter descriptions.
3. Your agent's underlying Language Model (LLM) uses this metadata to understand how and when to use the tools. This metadata is often incorporated into the LLM's system prompt or context.
4. A malicious MCP server can craft its tool metadata (names, descriptions) to include hidden or overt instructions. These instructions can act as a prompt injection, effectively telling your LLM to behave in a certain way, reveal sensitive information, or perform malicious actions.

**Crucially, this attack can occur simply by connecting to a malicious server and listing its tools, even if your agent never explicitly decides to *use* any of those tools.** The mere exposure to the malicious metadata can be enough to compromise the agent's behavior.

* **Extreme Caution with Untrusted Servers:** Reiterate: *Do not connect to MCP servers you do not fully trust.* The risk of metadata injection makes this paramount.

### Stdio Transport Security

Stdio (Standard Input/Output) transport is typically used for local MCP servers running on the same machine as your CrewAI application.

* **Process Isolation**: While generally safer as it doesn't involve network exposure by default, ensure the script or command run by `StdioServerParameters` is from a trusted source and has appropriate file system permissions. A malicious Stdio server script could still harm your local system.
* **Input Sanitization**: If your Stdio server script takes complex inputs derived from agent interactions, ensure the script itself sanitizes these inputs to prevent command injection or other vulnerabilities within the script's logic.
* **Resource Limits**: Be mindful that a local Stdio server process consumes local resources (CPU, memory). Ensure it's well-behaved and won't exhaust system resources.

### Confused Deputy Attacks

The [Confused Deputy Problem](https://en.wikipedia.org/wiki/Confused_deputy_problem) is a classic security vulnerability that can manifest in MCP integrations, especially when an MCP server acts as a proxy to other third-party services (e.g., Google Calendar, GitHub) that use OAuth 2.0 for authorization.

1. An MCP server (let's call it `MCP-Proxy`) allows your agent to interact with `ThirdPartyAPI`.
2. `MCP-Proxy` uses its own single, static `client_id` when talking to `ThirdPartyAPI`'s authorization server.
3. You, as the user, legitimately authorize `MCP-Proxy` to access `ThirdPartyAPI` on your behalf. During this, `ThirdPartyAPI`'s auth server might set a cookie in your browser indicating your consent for `MCP-Proxy`'s `client_id`.
4. An attacker crafts a malicious link. This link initiates an OAuth flow with `MCP-Proxy`, but is designed to trick `ThirdPartyAPI`'s auth server.
5. If you click this link, and `ThirdPartyAPI`'s auth server sees your existing consent cookie for `MCP-Proxy`'s `client_id`, it might *skip* asking for your consent again.
6. `MCP-Proxy` might then be tricked into forwarding an authorization code (for `ThirdPartyAPI`) to the attacker, or an MCP authorization code that the attacker can use to impersonate you to `MCP-Proxy`.

**Mitigation (Primarily for MCP Server Developers):**

* MCP proxy servers using static client IDs for downstream services **must** obtain explicit user consent for *each client application or agent* connecting to them *before* initiating an OAuth flow with the third-party service. This means `MCP-Proxy` itself should show a consent screen.

**CrewAI User Implication:**

* Be cautious if an MCP server redirects you for multiple OAuth authentications, especially if it seems unexpected or if the permissions requested are overly broad.
* Prefer MCP servers that clearly delineate their own identity versus the third-party services they might proxy.

### Remote Transport Security (SSE & Streamable HTTP)

When connecting to remote MCP servers via Server-Sent Events (SSE) or Streamable HTTP, standard web security practices are essential.

### SSE Security Considerations

### a. DNS Rebinding Attacks (Especially for SSE)

<Critical>
  **Protect against DNS Rebinding Attacks.**
</Critical>

DNS rebinding allows an attacker-controlled website to bypass the same-origin policy and make requests to servers on the user's local network (e.g., `localhost`) or intranet. This is particularly risky if you run an MCP server locally (e.g., for development) and an agent in a browser-like environment (though less common for typical CrewAI backend setups) or if the MCP server is on an internal network.

**Mitigation Strategies for MCP Server Implementers:**

* **Validate `Origin` and `Host` Headers**: MCP servers (especially SSE ones) should validate the `Origin` and/or `Host` HTTP headers to ensure requests are coming from expected domains/clients.
* **Bind to `localhost` (127.0.0.1)**: When running MCP servers locally for development, bind them to `127.0.0.1` instead of `0.0.0.0`. This prevents them from being accessible from other machines on the network.
* **Authentication**: Require authentication for all connections to your MCP server if it's not intended for public anonymous access.

* **Encrypt Data in Transit**: Always use HTTPS (HTTP Secure) for the URLs of remote MCP servers. This encrypts the communication between your CrewAI application and the MCP server, protecting against eavesdropping and man-in-the-middle attacks. `MCPServerAdapter` will respect the scheme (`http` or `https`) provided in the URL.

### c. Token Passthrough (Anti-Pattern)

This is primarily a concern for MCP server developers but understanding it helps in choosing secure servers.

"Token passthrough" is when an MCP server accepts an access token from your CrewAI agent (which might be a token for a *different* service, say `ServiceA`) and simply passes it through to another downstream API (`ServiceB`) without proper validation. Specifically, `ServiceB` (or the MCP server itself) should only accept tokens that were explicitly issued *for them* (i.e., the 'audience' claim in the token matches the server/service).

* Bypasses security controls (like rate limiting or fine-grained permissions) on the MCP server or the downstream API.
* Breaks audit trails and accountability.
* Allows misuse of stolen tokens.

**Mitigation (For MCP Server Developers):**

* MCP servers **MUST NOT** accept tokens that were not explicitly issued for them. They must validate the token's audience claim.

**CrewAI User Implication:**

* While not directly controllable by the user, this highlights the importance of connecting to well-designed MCP servers that adhere to security best practices.

#### Authentication and Authorization

* **Verify Identity**: If the MCP server provides sensitive tools or access to private data, it MUST implement strong authentication mechanisms to verify the identity of the client (your CrewAI application). This could involve API keys, OAuth tokens, or other standard methods.
* **Principle of Least Privilege**: Ensure the credentials used by `MCPServerAdapter` (if any) have only the necessary permissions to access the required tools.

### d. Input Validation and Sanitization

* **Input Validation is Critical**: MCP servers **must** rigorously validate all inputs received from agents *before* processing them or passing them to tools. This is a primary defense against many common vulnerabilities:
  * **Command Injection:** If a tool constructs shell commands, SQL queries, or other interpreted language statements based on input, the server must meticulously sanitize this input to prevent malicious commands from being injected and executed.
  * **Path Traversal:** If a tool accesses files based on input parameters, the server must validate and sanitize these paths to prevent access to unauthorized files or directories (e.g., by blocking `../` sequences).
  * **Data Type & Range Checks:** Servers must ensure that input data conforms to the expected data types (e.g., string, number, boolean) and falls within acceptable ranges or adheres to defined formats (e.g., regex for URLs).
  * **JSON Schema Validation:** All tool parameters should be strictly validated against their defined JSON schema. This helps catch malformed requests early.
* **Client-Side Awareness**: While server-side validation is paramount, as a CrewAI user, be mindful of the data your agents are constructed to send to MCP tools, especially if interacting with less-trusted or new MCP servers.

### e. Rate Limiting and Resource Management

* **Prevent Abuse**: MCP servers should implement rate limiting to prevent abuse, whether intentional (Denial of Service attacks) or unintentional (e.g., a misconfigured agent making too many requests).
* **Client-Side Retries**: Implement sensible retry logic in your CrewAI tasks if transient network issues or server rate limits are expected, but avoid aggressive retries that could exacerbate server load.

## 4. Secure MCP Server Implementation Advice (For Developers)

If you are developing an MCP server that CrewAI agents might connect to, consider these best practices in addition to the points above:

* **Follow Secure Coding Practices**: Adhere to standard secure coding principles for your chosen language and framework (e.g., OWASP Top 10).
* **Principle of Least Privilege**: Ensure the process running the MCP server (especially for `Stdio`) has only the minimum necessary permissions. Tools themselves should also operate with the least privilege required to perform their function.
* **Dependency Management**: Keep all server-side dependencies, including operating system packages, language runtimes, and third-party libraries, up-to-date to patch known vulnerabilities. Use tools to scan for vulnerable dependencies.
* **Secure Defaults**: Design your server and its tools to be secure by default. For example, features that could be risky should be off by default or require explicit opt-in with clear warnings.
* **Access Control for Tools**: Implement robust mechanisms to control which authenticated and authorized agents or users can access specific tools, especially those that are powerful, sensitive, or incur costs.
* **Secure Error Handling**: Servers should not expose detailed internal error messages, stack traces, or debugging information to the client, as these can reveal internal workings or potential vulnerabilities. Log errors comprehensively on the server-side for diagnostics.
* **Comprehensive Logging and Monitoring**: Implement detailed logging of security-relevant events (e.g., authentication attempts, tool invocations, errors, authorization changes). Monitor these logs for suspicious activity or abuse patterns.
* **Adherence to MCP Authorization Spec**: If implementing authentication and authorization, strictly follow the [MCP Authorization specification](https://modelcontextprotocol.io/specification/draft/basic/authorization) and relevant [OAuth 2.0 security best practices](https://datatracker.ietf.org/doc/html/rfc9700).
* **Regular Security Audits**: If your MCP server handles sensitive data, performs critical operations, or is publicly exposed, consider periodic security audits by qualified professionals.

## 5. Further Reading

For more detailed information on MCP security, refer to the official documentation:

* **[MCP Transport Security](https://modelcontextprotocol.io/docs/concepts/transports#security-considerations)**

By understanding these security considerations and implementing best practices, you can safely leverage the power of MCP servers in your CrewAI projects.
These are by no means exhaustive, but they cover the most common and critical security concerns.
The threats will continue to evolve, so it's important to stay informed and adapt your security measures accordingly.

---

## MCP Servers as Tools in CrewAI

**URL:** llms-txt#mcp-servers-as-tools-in-crewai

**Contents:**
- Overview
  - 🚀 **Simple DSL Integration** (Recommended)

Source: https://docs.crewai.com/en/mcp/overview

Learn how to integrate MCP servers as tools in your CrewAI agents using the `crewai-tools` library.

The [Model Context Protocol](https://modelcontextprotocol.io/introduction) (MCP) provides a standardized way for AI agents to provide context to LLMs by communicating with external services, known as MCP Servers.

CrewAI offers **two approaches** for MCP integration:

### 🚀 **Simple DSL Integration** (Recommended)

Use the `mcps` field directly on agents for seamless MCP tool integration. The DSL supports both **string references** (for quick setup) and **structured configurations** (for full control).

#### String-Based References (Quick Setup)

Perfect for remote HTTPS servers and CrewAI AOP marketplace:

```python theme={null}
from crewai import Agent

agent = Agent(
    role="Research Analyst",
    goal="Research and analyze information",
    backstory="Expert researcher with access to external tools",
    mcps=[
        "https://mcp.exa.ai/mcp?api_key=your_key",           # External MCP server
        "https://api.weather.com/mcp#get_forecast",          # Specific tool from server
        "crewai-amp:financial-data",                         # CrewAI AOP marketplace
        "crewai-amp:research-tools#pubmed_search"            # Specific AMP tool
    ]
)

---

## MCP tools are now automatically available to your agent!

**URL:** llms-txt#mcp-tools-are-now-automatically-available-to-your-agent!

**Contents:**
  - 🔧 **Advanced: MCPServerAdapter** (For Complex Scenarios)
- Video Tutorial
- Installation

python theme={null}
from crewai import Agent
from crewai.mcp import MCPServerStdio, MCPServerHTTP, MCPServerSSE
from crewai.mcp.filters import create_static_tool_filter

agent = Agent(
    role="Advanced Research Analyst",
    goal="Research with full control over MCP connections",
    backstory="Expert researcher with advanced tool access",
    mcps=[
        # Stdio transport for local servers
        MCPServerStdio(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem"],
            env={"API_KEY": "your_key"},
            tool_filter=create_static_tool_filter(
                allowed_tool_names=["read_file", "list_directory"]
            ),
            cache_tools_list=True,
        ),
        # HTTP/Streamable HTTP transport for remote servers
        MCPServerHTTP(
            url="https://api.example.com/mcp",
            headers={"Authorization": "Bearer your_token"},
            streamable=True,
            cache_tools_list=True,
        ),
        # SSE transport for real-time streaming
        MCPServerSSE(
            url="https://stream.example.com/mcp/sse",
            headers={"Authorization": "Bearer your_token"},
        ),
    ]
)
shell theme={null}

**Examples:**

Example 1 (unknown):
```unknown
#### Structured Configurations (Full Control)

For complete control over connection settings, tool filtering, and all transport types:
```

Example 2 (unknown):
```unknown
### 🔧 **Advanced: MCPServerAdapter** (For Complex Scenarios)

For advanced use cases requiring manual connection management, the `crewai-tools` library provides the `MCPServerAdapter` class.

We currently support the following transport mechanisms:

* **Stdio**: for local servers (communication via standard input/output between processes on the same machine)
* **Server-Sent Events (SSE)**: for remote servers (unidirectional, real-time data streaming from server to client over HTTP)
* **Streamable HTTPS**: for remote servers (flexible, potentially bi-directional communication over HTTPS, often utilizing SSE for server-to-client streams)

## Video Tutorial

Watch this video tutorial for a comprehensive guide on MCP integration with CrewAI:

<iframe title="CrewAI MCP Integration Guide" />

## Installation

CrewAI MCP integration requires the `mcp` library:
```

---

## `MergeAgentHandlerTool`

**URL:** llms-txt#`mergeagenthandlertool`

**Contents:**
- Installation
- Requirements
- Getting Started with Agent Handler
- Notes
- Usage
  - Single Tool Usage

The `MergeAgentHandlerTool` enables CrewAI agents to securely access third-party integrations through [Merge's Agent Handler](https://www.merge.dev/products/merge-agent-handler) platform. Agent Handler provides pre-built, secure connectors to popular tools like Linear, GitHub, Slack, Notion, and hundreds more—all with built-in authentication, permissions, and monitoring.

* Merge Agent Handler account with a configured Tool Pack
* Agent Handler API key
* At least one registered user linked to your Tool Pack
* Third-party integrations configured in your Tool Pack

## Getting Started with Agent Handler

1. **Sign up** for a Merge Agent Handler account at [ah.merge.dev/signup](https://ah.merge.dev/signup)
2. **Create a Tool Pack** and configure the integrations you need
3. **Register users** who will authenticate with the third-party services
4. **Get your API key** from the Agent Handler dashboard
5. **Set environment variable**: `export AGENT_HANDLER_API_KEY='your-key-here'`
6. **Start building** with the MergeAgentHandlerTool in CrewAI

* Tool Pack IDs and Registered User IDs can be found in your Agent Handler dashboard or created via API
* The tool uses the Model Context Protocol (MCP) for communication with Agent Handler
* Session IDs are automatically generated but can be customized for context persistence
* All tool calls are logged and auditable through the Agent Handler platform
* Tool parameters are dynamically discovered from the Agent Handler API and validated automatically

### Single Tool Usage

Here's how to use a specific tool from your Tool Pack:

```python {2, 4-9} theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import MergeAgentHandlerTool

**Examples:**

Example 1 (unknown):
```unknown
## Requirements

* Merge Agent Handler account with a configured Tool Pack
* Agent Handler API key
* At least one registered user linked to your Tool Pack
* Third-party integrations configured in your Tool Pack

## Getting Started with Agent Handler

1. **Sign up** for a Merge Agent Handler account at [ah.merge.dev/signup](https://ah.merge.dev/signup)
2. **Create a Tool Pack** and configure the integrations you need
3. **Register users** who will authenticate with the third-party services
4. **Get your API key** from the Agent Handler dashboard
5. **Set environment variable**: `export AGENT_HANDLER_API_KEY='your-key-here'`
6. **Start building** with the MergeAgentHandlerTool in CrewAI

## Notes

* Tool Pack IDs and Registered User IDs can be found in your Agent Handler dashboard or created via API
* The tool uses the Model Context Protocol (MCP) for communication with Agent Handler
* Session IDs are automatically generated but can be customized for context persistence
* All tool calls are logged and auditable through the Agent Handler platform
* Tool parameters are dynamically discovered from the Agent Handler API and validated automatically

## Usage

### Single Tool Usage

Here's how to use a specific tool from your Tool Pack:
```

---

## Merge Agent Handler Tool

**URL:** llms-txt#merge-agent-handler-tool

Source: https://docs.crewai.com/en/tools/integration/mergeagenthandlertool

Enables CrewAI agents to securely access third-party integrations like Linear, GitHub, Slack, and more through Merge's Agent Handler platform

---

## Microsoft Excel Integration

**URL:** llms-txt#microsoft-excel-integration

**Contents:**
- Overview
- Prerequisites
- Setting Up Microsoft Excel Integration
  - 1. Connect Your Microsoft Account
  - 2. Install Required Package
  - 3. Environment Variable Setup
- Available Actions
- Usage Examples
  - Basic Excel Agent Setup

Source: https://docs.crewai.com/en/enterprise/integrations/microsoft_excel

Workbook and data management with Microsoft Excel integration for CrewAI.

Enable your agents to create and manage Excel workbooks, worksheets, tables, and charts in OneDrive or SharePoint. Manipulate data ranges, create visualizations, manage tables, and streamline your spreadsheet workflows with AI-powered automation.

Before using the Microsoft Excel integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A Microsoft 365 account with Excel and OneDrive/SharePoint access
* Connected your Microsoft account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)

## Setting Up Microsoft Excel Integration

### 1. Connect Your Microsoft Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Microsoft Excel** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for files and Excel workbook access
5. Copy your Enterprise Token from [Integration Settings](https://app.crewai.com/crewai_plus/settings/integrations)

### 2. Install Required Package

### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>

Or add it to your `.env` file:

<AccordionGroup>
  <Accordion title="microsoft_excel/create_workbook">
    **Description:** Create a new Excel workbook in OneDrive or SharePoint.

* `file_path` (string, required): Path where to create the workbook (e.g., 'MyWorkbook.xlsx')
    * `worksheets` (array, optional): Initial worksheets to create
      
  </Accordion>

<Accordion title="microsoft_excel/get_workbooks">
    **Description:** Get all Excel workbooks from OneDrive or SharePoint.

* `select` (string, optional): Select specific properties to return
    * `filter` (string, optional): Filter results using OData syntax
    * `expand` (string, optional): Expand related resources inline
    * `top` (integer, optional): Number of items to return. Minimum: 1, Maximum: 999
    * `orderby` (string, optional): Order results by specified properties
  </Accordion>

<Accordion title="microsoft_excel/get_worksheets">
    **Description:** Get all worksheets in an Excel workbook.

* `file_id` (string, required): The ID of the Excel file
    * `select` (string, optional): Select specific properties to return (e.g., 'id,name,position')
    * `filter` (string, optional): Filter results using OData syntax
    * `expand` (string, optional): Expand related resources inline
    * `top` (integer, optional): Number of items to return. Minimum: 1, Maximum: 999
    * `orderby` (string, optional): Order results by specified properties
  </Accordion>

<Accordion title="microsoft_excel/create_worksheet">
    **Description:** Create a new worksheet in an Excel workbook.

* `file_id` (string, required): The ID of the Excel file
    * `name` (string, required): Name of the new worksheet
  </Accordion>

<Accordion title="microsoft_excel/get_range_data">
    **Description:** Get data from a specific range in an Excel worksheet.

* `file_id` (string, required): The ID of the Excel file
    * `worksheet_name` (string, required): Name of the worksheet
    * `range` (string, required): Range address (e.g., 'A1:C10')
  </Accordion>

<Accordion title="microsoft_excel/update_range_data">
    **Description:** Update data in a specific range in an Excel worksheet.

* `file_id` (string, required): The ID of the Excel file
    * `worksheet_name` (string, required): Name of the worksheet
    * `range` (string, required): Range address (e.g., 'A1:C10')
    * `values` (array, required): 2D array of values to set in the range
      
  </Accordion>

<Accordion title="microsoft_excel/add_table">
    **Description:** Create a table in an Excel worksheet.

* `file_id` (string, required): The ID of the Excel file
    * `worksheet_name` (string, required): Name of the worksheet
    * `range` (string, required): Range for the table (e.g., 'A1:D10')
    * `has_headers` (boolean, optional): Whether the first row contains headers. Default: true
  </Accordion>

<Accordion title="microsoft_excel/get_tables">
    **Description:** Get all tables in an Excel worksheet.

* `file_id` (string, required): The ID of the Excel file
    * `worksheet_name` (string, required): Name of the worksheet
  </Accordion>

<Accordion title="microsoft_excel/add_table_row">
    **Description:** Add a new row to an Excel table.

* `file_id` (string, required): The ID of the Excel file
    * `worksheet_name` (string, required): Name of the worksheet
    * `table_name` (string, required): Name of the table
    * `values` (array, required): Array of values for the new row
      
  </Accordion>

<Accordion title="microsoft_excel/create_chart">
    **Description:** Create a chart in an Excel worksheet.

* `file_id` (string, required): The ID of the Excel file
    * `worksheet_name` (string, required): Name of the worksheet
    * `chart_type` (string, required): Type of chart (e.g., 'ColumnClustered', 'Line', 'Pie')
    * `source_data` (string, required): Range of data for the chart (e.g., 'A1:B10')
    * `series_by` (string, optional): How to interpret the data ('Auto', 'Columns', or 'Rows'). Default: Auto
  </Accordion>

<Accordion title="microsoft_excel/get_cell">
    **Description:** Get the value of a single cell in an Excel worksheet.

* `file_id` (string, required): The ID of the Excel file
    * `worksheet_name` (string, required): Name of the worksheet
    * `row` (integer, required): Row number (0-based)
    * `column` (integer, required): Column number (0-based)
  </Accordion>

<Accordion title="microsoft_excel/get_used_range">
    **Description:** Get the used range of an Excel worksheet (contains all data).

* `file_id` (string, required): The ID of the Excel file
    * `worksheet_name` (string, required): Name of the worksheet
  </Accordion>

<Accordion title="microsoft_excel/list_charts">
    **Description:** Get all charts in an Excel worksheet.

* `file_id` (string, required): The ID of the Excel file
    * `worksheet_name` (string, required): Name of the worksheet
  </Accordion>

<Accordion title="microsoft_excel/delete_worksheet">
    **Description:** Delete a worksheet from an Excel workbook.

* `file_id` (string, required): The ID of the Excel file
    * `worksheet_name` (string, required): Name of the worksheet to delete
  </Accordion>

<Accordion title="microsoft_excel/delete_table">
    **Description:** Delete a table from an Excel worksheet.

* `file_id` (string, required): The ID of the Excel file
    * `worksheet_name` (string, required): Name of the worksheet
    * `table_name` (string, required): Name of the table to delete
  </Accordion>

<Accordion title="microsoft_excel/list_names">
    **Description:** Get all named ranges in an Excel workbook.

* `file_id` (string, required): The ID of the Excel file
  </Accordion>
</AccordionGroup>

### Basic Excel Agent Setup

```python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

Example 3 (unknown):
```unknown
## Available Actions

<AccordionGroup>
  <Accordion title="microsoft_excel/create_workbook">
    **Description:** Create a new Excel workbook in OneDrive or SharePoint.

    **Parameters:**

    * `file_path` (string, required): Path where to create the workbook (e.g., 'MyWorkbook.xlsx')
    * `worksheets` (array, optional): Initial worksheets to create
```

Example 4 (unknown):
```unknown
</Accordion>

  <Accordion title="microsoft_excel/get_workbooks">
    **Description:** Get all Excel workbooks from OneDrive or SharePoint.

    **Parameters:**

    * `select` (string, optional): Select specific properties to return
    * `filter` (string, optional): Filter results using OData syntax
    * `expand` (string, optional): Expand related resources inline
    * `top` (integer, optional): Number of items to return. Minimum: 1, Maximum: 999
    * `orderby` (string, optional): Order results by specified properties
  </Accordion>

  <Accordion title="microsoft_excel/get_worksheets">
    **Description:** Get all worksheets in an Excel workbook.

    **Parameters:**

    * `file_id` (string, required): The ID of the Excel file
    * `select` (string, optional): Select specific properties to return (e.g., 'id,name,position')
    * `filter` (string, optional): Filter results using OData syntax
    * `expand` (string, optional): Expand related resources inline
    * `top` (integer, optional): Number of items to return. Minimum: 1, Maximum: 999
    * `orderby` (string, optional): Order results by specified properties
  </Accordion>

  <Accordion title="microsoft_excel/create_worksheet">
    **Description:** Create a new worksheet in an Excel workbook.

    **Parameters:**

    * `file_id` (string, required): The ID of the Excel file
    * `name` (string, required): Name of the new worksheet
  </Accordion>

  <Accordion title="microsoft_excel/get_range_data">
    **Description:** Get data from a specific range in an Excel worksheet.

    **Parameters:**

    * `file_id` (string, required): The ID of the Excel file
    * `worksheet_name` (string, required): Name of the worksheet
    * `range` (string, required): Range address (e.g., 'A1:C10')
  </Accordion>

  <Accordion title="microsoft_excel/update_range_data">
    **Description:** Update data in a specific range in an Excel worksheet.

    **Parameters:**

    * `file_id` (string, required): The ID of the Excel file
    * `worksheet_name` (string, required): Name of the worksheet
    * `range` (string, required): Range address (e.g., 'A1:C10')
    * `values` (array, required): 2D array of values to set in the range
```

---

## Microsoft OneDrive Integration

**URL:** llms-txt#microsoft-onedrive-integration

**Contents:**
- Overview
- Prerequisites
- Setting Up Microsoft OneDrive Integration
  - 1. Connect Your Microsoft Account
  - 2. Install Required Package
  - 3. Environment Variable Setup
- Available Actions
- Usage Examples
  - Basic Microsoft OneDrive Agent Setup

Source: https://docs.crewai.com/en/enterprise/integrations/microsoft_onedrive

File and folder management with Microsoft OneDrive integration for CrewAI.

Enable your agents to upload, download, and manage files and folders in Microsoft OneDrive. Automate file operations, organize content, create sharing links, and streamline your cloud storage workflows with AI-powered automation.

Before using the Microsoft OneDrive integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A Microsoft account with OneDrive access
* Connected your Microsoft account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)

## Setting Up Microsoft OneDrive Integration

### 1. Connect Your Microsoft Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Microsoft OneDrive** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for file access
5. Copy your Enterprise Token from [Integration Settings](https://app.crewai.com/crewai_plus/settings/integrations)

### 2. Install Required Package

### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>

Or add it to your `.env` file:

<AccordionGroup>
  <Accordion title="microsoft_onedrive/list_files">
    **Description:** List files and folders in OneDrive.

* `top` (integer, optional): Number of items to retrieve (max 1000). Default is `50`.
    * `orderby` (string, optional): Order by field (e.g., "name asc", "lastModifiedDateTime desc"). Default is "name asc".
    * `filter` (string, optional): OData filter expression.
  </Accordion>

<Accordion title="microsoft_onedrive/get_file_info">
    **Description:** Get information about a specific file or folder.

* `item_id` (string, required): The ID of the file or folder.
  </Accordion>

<Accordion title="microsoft_onedrive/download_file">
    **Description:** Download a file from OneDrive.

* `item_id` (string, required): The ID of the file to download.
  </Accordion>

<Accordion title="microsoft_onedrive/upload_file">
    **Description:** Upload a file to OneDrive.

* `file_name` (string, required): Name of the file to upload.
    * `content` (string, required): Base64 encoded file content.
  </Accordion>

<Accordion title="microsoft_onedrive/create_folder">
    **Description:** Create a new folder in OneDrive.

* `folder_name` (string, required): Name of the folder to create.
  </Accordion>

<Accordion title="microsoft_onedrive/delete_item">
    **Description:** Delete a file or folder from OneDrive.

* `item_id` (string, required): The ID of the file or folder to delete.
  </Accordion>

<Accordion title="microsoft_onedrive/copy_item">
    **Description:** Copy a file or folder in OneDrive.

* `item_id` (string, required): The ID of the file or folder to copy.
    * `parent_id` (string, optional): The ID of the destination folder (optional, defaults to root).
    * `new_name` (string, optional): New name for the copied item (optional).
  </Accordion>

<Accordion title="microsoft_onedrive/move_item">
    **Description:** Move a file or folder in OneDrive.

* `item_id` (string, required): The ID of the file or folder to move.
    * `parent_id` (string, required): The ID of the destination folder.
    * `new_name` (string, optional): New name for the item (optional).
  </Accordion>

<Accordion title="microsoft_onedrive/search_files">
    **Description:** Search for files and folders in OneDrive.

* `query` (string, required): Search query string.
    * `top` (integer, optional): Number of results to return (max 1000). Default is `50`.
  </Accordion>

<Accordion title="microsoft_onedrive/share_item">
    **Description:** Create a sharing link for a file or folder.

* `item_id` (string, required): The ID of the file or folder to share.
    * `type` (string, optional): Type of sharing link. Enum: `view`, `edit`, `embed`. Default is `view`.
    * `scope` (string, optional): Scope of the sharing link. Enum: `anonymous`, `organization`. Default is `anonymous`.
  </Accordion>

<Accordion title="microsoft_onedrive/get_thumbnails">
    **Description:** Get thumbnails for a file.

* `item_id` (string, required): The ID of the file.
  </Accordion>
</AccordionGroup>

### Basic Microsoft OneDrive Agent Setup

```python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

Example 3 (unknown):
```unknown
## Available Actions

<AccordionGroup>
  <Accordion title="microsoft_onedrive/list_files">
    **Description:** List files and folders in OneDrive.

    **Parameters:**

    * `top` (integer, optional): Number of items to retrieve (max 1000). Default is `50`.
    * `orderby` (string, optional): Order by field (e.g., "name asc", "lastModifiedDateTime desc"). Default is "name asc".
    * `filter` (string, optional): OData filter expression.
  </Accordion>

  <Accordion title="microsoft_onedrive/get_file_info">
    **Description:** Get information about a specific file or folder.

    **Parameters:**

    * `item_id` (string, required): The ID of the file or folder.
  </Accordion>

  <Accordion title="microsoft_onedrive/download_file">
    **Description:** Download a file from OneDrive.

    **Parameters:**

    * `item_id` (string, required): The ID of the file to download.
  </Accordion>

  <Accordion title="microsoft_onedrive/upload_file">
    **Description:** Upload a file to OneDrive.

    **Parameters:**

    * `file_name` (string, required): Name of the file to upload.
    * `content` (string, required): Base64 encoded file content.
  </Accordion>

  <Accordion title="microsoft_onedrive/create_folder">
    **Description:** Create a new folder in OneDrive.

    **Parameters:**

    * `folder_name` (string, required): Name of the folder to create.
  </Accordion>

  <Accordion title="microsoft_onedrive/delete_item">
    **Description:** Delete a file or folder from OneDrive.

    **Parameters:**

    * `item_id` (string, required): The ID of the file or folder to delete.
  </Accordion>

  <Accordion title="microsoft_onedrive/copy_item">
    **Description:** Copy a file or folder in OneDrive.

    **Parameters:**

    * `item_id` (string, required): The ID of the file or folder to copy.
    * `parent_id` (string, optional): The ID of the destination folder (optional, defaults to root).
    * `new_name` (string, optional): New name for the copied item (optional).
  </Accordion>

  <Accordion title="microsoft_onedrive/move_item">
    **Description:** Move a file or folder in OneDrive.

    **Parameters:**

    * `item_id` (string, required): The ID of the file or folder to move.
    * `parent_id` (string, required): The ID of the destination folder.
    * `new_name` (string, optional): New name for the item (optional).
  </Accordion>

  <Accordion title="microsoft_onedrive/search_files">
    **Description:** Search for files and folders in OneDrive.

    **Parameters:**

    * `query` (string, required): Search query string.
    * `top` (integer, optional): Number of results to return (max 1000). Default is `50`.
  </Accordion>

  <Accordion title="microsoft_onedrive/share_item">
    **Description:** Create a sharing link for a file or folder.

    **Parameters:**

    * `item_id` (string, required): The ID of the file or folder to share.
    * `type` (string, optional): Type of sharing link. Enum: `view`, `edit`, `embed`. Default is `view`.
    * `scope` (string, optional): Scope of the sharing link. Enum: `anonymous`, `organization`. Default is `anonymous`.
  </Accordion>

  <Accordion title="microsoft_onedrive/get_thumbnails">
    **Description:** Get thumbnails for a file.

    **Parameters:**

    * `item_id` (string, required): The ID of the file.
  </Accordion>
</AccordionGroup>

## Usage Examples

### Basic Microsoft OneDrive Agent Setup
```

---

## Microsoft Outlook Integration

**URL:** llms-txt#microsoft-outlook-integration

**Contents:**
- Overview
- Prerequisites
- Setting Up Microsoft Outlook Integration
  - 1. Connect Your Microsoft Account
  - 2. Install Required Package
  - 3. Environment Variable Setup
- Available Actions
- Usage Examples
  - Basic Microsoft Outlook Agent Setup

Source: https://docs.crewai.com/en/enterprise/integrations/microsoft_outlook

Email, calendar, and contact management with Microsoft Outlook integration for CrewAI.

Enable your agents to access and manage Outlook emails, calendar events, and contacts. Send emails, retrieve messages, manage calendar events, and organize contacts with AI-powered automation.

Before using the Microsoft Outlook integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A Microsoft account with Outlook access
* Connected your Microsoft account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)

## Setting Up Microsoft Outlook Integration

### 1. Connect Your Microsoft Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Microsoft Outlook** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for mail, calendar, and contact access
5. Copy your Enterprise Token from [Integration Settings](https://app.crewai.com/crewai_plus/settings/integrations)

### 2. Install Required Package

### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>

Or add it to your `.env` file:

<AccordionGroup>
  <Accordion title="microsoft_outlook/get_messages">
    **Description:** Get email messages from the user's mailbox.

* `top` (integer, optional): Number of messages to retrieve (max 1000). Default is `10`.
    * `filter` (string, optional): OData filter expression (e.g., "isRead eq false").
    * `search` (string, optional): Search query string.
    * `orderby` (string, optional): Order by field (e.g., "receivedDateTime desc"). Default is "receivedDateTime desc".
    * `select` (string, optional): Select specific properties to return.
    * `expand` (string, optional): Expand related resources inline.
  </Accordion>

<Accordion title="microsoft_outlook/send_email">
    **Description:** Send an email message.

* `to_recipients` (array, required): Array of recipient email addresses.
    * `cc_recipients` (array, optional): Array of CC recipient email addresses.
    * `bcc_recipients` (array, optional): Array of BCC recipient email addresses.
    * `subject` (string, required): Email subject.
    * `body` (string, required): Email body content.
    * `body_type` (string, optional): Body content type. Enum: `Text`, `HTML`. Default is `HTML`.
    * `importance` (string, optional): Message importance level. Enum: `low`, `normal`, `high`. Default is `normal`.
    * `reply_to` (array, optional): Array of reply-to email addresses.
    * `save_to_sent_items` (boolean, optional): Whether to save the message to Sent Items folder. Default is `true`.
  </Accordion>

<Accordion title="microsoft_outlook/get_calendar_events">
    **Description:** Get calendar events from the user's calendar.

* `top` (integer, optional): Number of events to retrieve (max 1000). Default is `10`.
    * `skip` (integer, optional): Number of events to skip. Default is `0`.
    * `filter` (string, optional): OData filter expression (e.g., "start/dateTime ge '2024-01-01T00:00:00Z'").
    * `orderby` (string, optional): Order by field (e.g., "start/dateTime asc"). Default is "start/dateTime asc".
  </Accordion>

<Accordion title="microsoft_outlook/create_calendar_event">
    **Description:** Create a new calendar event.

* `subject` (string, required): Event subject/title.
    * `body` (string, optional): Event body/description.
    * `start_datetime` (string, required): Start date and time in ISO 8601 format (e.g., '2024-01-20T10:00:00').
    * `end_datetime` (string, required): End date and time in ISO 8601 format.
    * `timezone` (string, optional): Time zone (e.g., 'Pacific Standard Time'). Default is `UTC`.
    * `location` (string, optional): Event location.
    * `attendees` (array, optional): Array of attendee email addresses.
  </Accordion>

<Accordion title="microsoft_outlook/get_contacts">
    **Description:** Get contacts from the user's address book.

* `top` (integer, optional): Number of contacts to retrieve (max 1000). Default is `10`.
    * `skip` (integer, optional): Number of contacts to skip. Default is `0`.
    * `filter` (string, optional): OData filter expression.
    * `orderby` (string, optional): Order by field (e.g., "displayName asc"). Default is "displayName asc".
  </Accordion>

<Accordion title="microsoft_outlook/create_contact">
    **Description:** Create a new contact in the user's address book.

* `displayName` (string, required): Contact's display name.
    * `givenName` (string, optional): Contact's first name.
    * `surname` (string, optional): Contact's last name.
    * `emailAddresses` (array, optional): Array of email addresses. Each item is an object with `address` (string) and `name` (string).
    * `businessPhones` (array, optional): Array of business phone numbers.
    * `homePhones` (array, optional): Array of home phone numbers.
    * `jobTitle` (string, optional): Contact's job title.
    * `companyName` (string, optional): Contact's company name.
  </Accordion>
</AccordionGroup>

### Basic Microsoft Outlook Agent Setup

```python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

Example 3 (unknown):
```unknown
## Available Actions

<AccordionGroup>
  <Accordion title="microsoft_outlook/get_messages">
    **Description:** Get email messages from the user's mailbox.

    **Parameters:**

    * `top` (integer, optional): Number of messages to retrieve (max 1000). Default is `10`.
    * `filter` (string, optional): OData filter expression (e.g., "isRead eq false").
    * `search` (string, optional): Search query string.
    * `orderby` (string, optional): Order by field (e.g., "receivedDateTime desc"). Default is "receivedDateTime desc".
    * `select` (string, optional): Select specific properties to return.
    * `expand` (string, optional): Expand related resources inline.
  </Accordion>

  <Accordion title="microsoft_outlook/send_email">
    **Description:** Send an email message.

    **Parameters:**

    * `to_recipients` (array, required): Array of recipient email addresses.
    * `cc_recipients` (array, optional): Array of CC recipient email addresses.
    * `bcc_recipients` (array, optional): Array of BCC recipient email addresses.
    * `subject` (string, required): Email subject.
    * `body` (string, required): Email body content.
    * `body_type` (string, optional): Body content type. Enum: `Text`, `HTML`. Default is `HTML`.
    * `importance` (string, optional): Message importance level. Enum: `low`, `normal`, `high`. Default is `normal`.
    * `reply_to` (array, optional): Array of reply-to email addresses.
    * `save_to_sent_items` (boolean, optional): Whether to save the message to Sent Items folder. Default is `true`.
  </Accordion>

  <Accordion title="microsoft_outlook/get_calendar_events">
    **Description:** Get calendar events from the user's calendar.

    **Parameters:**

    * `top` (integer, optional): Number of events to retrieve (max 1000). Default is `10`.
    * `skip` (integer, optional): Number of events to skip. Default is `0`.
    * `filter` (string, optional): OData filter expression (e.g., "start/dateTime ge '2024-01-01T00:00:00Z'").
    * `orderby` (string, optional): Order by field (e.g., "start/dateTime asc"). Default is "start/dateTime asc".
  </Accordion>

  <Accordion title="microsoft_outlook/create_calendar_event">
    **Description:** Create a new calendar event.

    **Parameters:**

    * `subject` (string, required): Event subject/title.
    * `body` (string, optional): Event body/description.
    * `start_datetime` (string, required): Start date and time in ISO 8601 format (e.g., '2024-01-20T10:00:00').
    * `end_datetime` (string, required): End date and time in ISO 8601 format.
    * `timezone` (string, optional): Time zone (e.g., 'Pacific Standard Time'). Default is `UTC`.
    * `location` (string, optional): Event location.
    * `attendees` (array, optional): Array of attendee email addresses.
  </Accordion>

  <Accordion title="microsoft_outlook/get_contacts">
    **Description:** Get contacts from the user's address book.

    **Parameters:**

    * `top` (integer, optional): Number of contacts to retrieve (max 1000). Default is `10`.
    * `skip` (integer, optional): Number of contacts to skip. Default is `0`.
    * `filter` (string, optional): OData filter expression.
    * `orderby` (string, optional): Order by field (e.g., "displayName asc"). Default is "displayName asc".
  </Accordion>

  <Accordion title="microsoft_outlook/create_contact">
    **Description:** Create a new contact in the user's address book.

    **Parameters:**

    * `displayName` (string, required): Contact's display name.
    * `givenName` (string, optional): Contact's first name.
    * `surname` (string, optional): Contact's last name.
    * `emailAddresses` (array, optional): Array of email addresses. Each item is an object with `address` (string) and `name` (string).
    * `businessPhones` (array, optional): Array of business phone numbers.
    * `homePhones` (array, optional): Array of home phone numbers.
    * `jobTitle` (string, optional): Contact's job title.
    * `companyName` (string, optional): Contact's company name.
  </Accordion>
</AccordionGroup>

## Usage Examples

### Basic Microsoft Outlook Agent Setup
```

---

## Microsoft SharePoint Integration

**URL:** llms-txt#microsoft-sharepoint-integration

**Contents:**
- Overview
- Prerequisites
- Setting Up Microsoft SharePoint Integration
  - 1. Connect Your Microsoft Account
  - 2. Install Required Package
  - 3. Environment Variable Setup
- Available Actions
- Usage Examples
  - Basic SharePoint Agent Setup

Source: https://docs.crewai.com/en/enterprise/integrations/microsoft_sharepoint

Site, list, and document management with Microsoft SharePoint integration for CrewAI.

Enable your agents to access and manage SharePoint sites, lists, and document libraries. Retrieve site information, manage list items, upload and organize files, and streamline your SharePoint workflows with AI-powered automation.

Before using the Microsoft SharePoint integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A Microsoft 365 account with SharePoint access
* Connected your Microsoft account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)

## Setting Up Microsoft SharePoint Integration

### 1. Connect Your Microsoft Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Microsoft SharePoint** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for SharePoint sites and content access
5. Copy your Enterprise Token from [Integration Settings](https://app.crewai.com/crewai_plus/settings/integrations)

### 2. Install Required Package

### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>

Or add it to your `.env` file:

<AccordionGroup>
  <Accordion title="microsoft_sharepoint/get_sites">
    **Description:** Get all SharePoint sites the user has access to.

* `search` (string, optional): Search query to filter sites
    * `select` (string, optional): Select specific properties to return (e.g., 'displayName,id,webUrl')
    * `filter` (string, optional): Filter results using OData syntax
    * `expand` (string, optional): Expand related resources inline
    * `top` (integer, optional): Number of items to return. Minimum: 1, Maximum: 999
    * `skip` (integer, optional): Number of items to skip. Minimum: 0
    * `orderby` (string, optional): Order results by specified properties (e.g., 'displayName desc')
  </Accordion>

<Accordion title="microsoft_sharepoint/get_site">
    **Description:** Get information about a specific SharePoint site.

* `site_id` (string, required): The ID of the SharePoint site
    * `select` (string, optional): Select specific properties to return (e.g., 'displayName,id,webUrl,drives')
    * `expand` (string, optional): Expand related resources inline (e.g., 'drives,lists')
  </Accordion>

<Accordion title="microsoft_sharepoint/get_site_lists">
    **Description:** Get all lists in a SharePoint site.

* `site_id` (string, required): The ID of the SharePoint site
  </Accordion>

<Accordion title="microsoft_sharepoint/get_list">
    **Description:** Get information about a specific list.

* `site_id` (string, required): The ID of the SharePoint site
    * `list_id` (string, required): The ID of the list
  </Accordion>

<Accordion title="microsoft_sharepoint/get_list_items">
    **Description:** Get items from a SharePoint list.

* `site_id` (string, required): The ID of the SharePoint site
    * `list_id` (string, required): The ID of the list
    * `expand` (string, optional): Expand related data (e.g., 'fields')
  </Accordion>

<Accordion title="microsoft_sharepoint/create_list_item">
    **Description:** Create a new item in a SharePoint list.

* `site_id` (string, required): The ID of the SharePoint site
    * `list_id` (string, required): The ID of the list
    * `fields` (object, required): The field values for the new item
      
  </Accordion>

<Accordion title="microsoft_sharepoint/update_list_item">
    **Description:** Update an item in a SharePoint list.

* `site_id` (string, required): The ID of the SharePoint site
    * `list_id` (string, required): The ID of the list
    * `item_id` (string, required): The ID of the item to update
    * `fields` (object, required): The field values to update
      
  </Accordion>

<Accordion title="microsoft_sharepoint/delete_list_item">
    **Description:** Delete an item from a SharePoint list.

* `site_id` (string, required): The ID of the SharePoint site
    * `list_id` (string, required): The ID of the list
    * `item_id` (string, required): The ID of the item to delete
  </Accordion>

<Accordion title="microsoft_sharepoint/upload_file_to_library">
    **Description:** Upload a file to a SharePoint document library.

* `site_id` (string, required): The ID of the SharePoint site
    * `file_path` (string, required): The path where to upload the file (e.g., 'folder/filename.txt')
    * `content` (string, required): The file content to upload
  </Accordion>

<Accordion title="microsoft_sharepoint/get_drive_items">
    **Description:** Get files and folders from a SharePoint document library.

* `site_id` (string, required): The ID of the SharePoint site
  </Accordion>

<Accordion title="microsoft_sharepoint/delete_drive_item">
    **Description:** Delete a file or folder from SharePoint document library.

* `site_id` (string, required): The ID of the SharePoint site
    * `item_id` (string, required): The ID of the file or folder to delete
  </Accordion>
</AccordionGroup>

### Basic SharePoint Agent Setup

```python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

Example 3 (unknown):
```unknown
## Available Actions

<AccordionGroup>
  <Accordion title="microsoft_sharepoint/get_sites">
    **Description:** Get all SharePoint sites the user has access to.

    **Parameters:**

    * `search` (string, optional): Search query to filter sites
    * `select` (string, optional): Select specific properties to return (e.g., 'displayName,id,webUrl')
    * `filter` (string, optional): Filter results using OData syntax
    * `expand` (string, optional): Expand related resources inline
    * `top` (integer, optional): Number of items to return. Minimum: 1, Maximum: 999
    * `skip` (integer, optional): Number of items to skip. Minimum: 0
    * `orderby` (string, optional): Order results by specified properties (e.g., 'displayName desc')
  </Accordion>

  <Accordion title="microsoft_sharepoint/get_site">
    **Description:** Get information about a specific SharePoint site.

    **Parameters:**

    * `site_id` (string, required): The ID of the SharePoint site
    * `select` (string, optional): Select specific properties to return (e.g., 'displayName,id,webUrl,drives')
    * `expand` (string, optional): Expand related resources inline (e.g., 'drives,lists')
  </Accordion>

  <Accordion title="microsoft_sharepoint/get_site_lists">
    **Description:** Get all lists in a SharePoint site.

    **Parameters:**

    * `site_id` (string, required): The ID of the SharePoint site
  </Accordion>

  <Accordion title="microsoft_sharepoint/get_list">
    **Description:** Get information about a specific list.

    **Parameters:**

    * `site_id` (string, required): The ID of the SharePoint site
    * `list_id` (string, required): The ID of the list
  </Accordion>

  <Accordion title="microsoft_sharepoint/get_list_items">
    **Description:** Get items from a SharePoint list.

    **Parameters:**

    * `site_id` (string, required): The ID of the SharePoint site
    * `list_id` (string, required): The ID of the list
    * `expand` (string, optional): Expand related data (e.g., 'fields')
  </Accordion>

  <Accordion title="microsoft_sharepoint/create_list_item">
    **Description:** Create a new item in a SharePoint list.

    **Parameters:**

    * `site_id` (string, required): The ID of the SharePoint site
    * `list_id` (string, required): The ID of the list
    * `fields` (object, required): The field values for the new item
```

Example 4 (unknown):
```unknown
</Accordion>

  <Accordion title="microsoft_sharepoint/update_list_item">
    **Description:** Update an item in a SharePoint list.

    **Parameters:**

    * `site_id` (string, required): The ID of the SharePoint site
    * `list_id` (string, required): The ID of the list
    * `item_id` (string, required): The ID of the item to update
    * `fields` (object, required): The field values to update
```

---

## Microsoft Teams Integration

**URL:** llms-txt#microsoft-teams-integration

**Contents:**
- Overview
- Prerequisites
- Setting Up Microsoft Teams Integration
  - 1. Connect Your Microsoft Account
  - 2. Install Required Package
  - 3. Environment Variable Setup
- Available Actions
- Usage Examples
  - Basic Microsoft Teams Agent Setup

Source: https://docs.crewai.com/en/enterprise/integrations/microsoft_teams

Team collaboration and communication with Microsoft Teams integration for CrewAI.

Enable your agents to access Teams data, send messages, create meetings, and manage channels. Automate team communication, schedule meetings, retrieve messages, and streamline your collaboration workflows with AI-powered automation.

Before using the Microsoft Teams integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A Microsoft account with Teams access
* Connected your Microsoft account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)

## Setting Up Microsoft Teams Integration

### 1. Connect Your Microsoft Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Microsoft Teams** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for Teams access
5. Copy your Enterprise Token from [Integration Settings](https://app.crewai.com/crewai_plus/settings/integrations)

### 2. Install Required Package

### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>

Or add it to your `.env` file:

<AccordionGroup>
  <Accordion title="microsoft_teams/get_teams">
    **Description:** Get all teams the user is a member of.

* No parameters required.
  </Accordion>

<Accordion title="microsoft_teams/get_channels">
    **Description:** Get channels in a specific team.

* `team_id` (string, required): The ID of the team.
  </Accordion>

<Accordion title="microsoft_teams/send_message">
    **Description:** Send a message to a Teams channel.

* `team_id` (string, required): The ID of the team.
    * `channel_id` (string, required): The ID of the channel.
    * `message` (string, required): The message content.
    * `content_type` (string, optional): Content type (html or text). Enum: `html`, `text`. Default is `text`.
  </Accordion>

<Accordion title="microsoft_teams/get_messages">
    **Description:** Get messages from a Teams channel.

* `team_id` (string, required): The ID of the team.
    * `channel_id` (string, required): The ID of the channel.
    * `top` (integer, optional): Number of messages to retrieve (max 50). Default is `20`.
  </Accordion>

<Accordion title="microsoft_teams/create_meeting">
    **Description:** Create a Teams meeting.

* `subject` (string, required): Meeting subject/title.
    * `startDateTime` (string, required): Meeting start time (ISO 8601 format with timezone).
    * `endDateTime` (string, required): Meeting end time (ISO 8601 format with timezone).
  </Accordion>

<Accordion title="microsoft_teams/search_online_meetings_by_join_url">
    **Description:** Search online meetings by Join Web URL.

* `join_web_url` (string, required): The join web URL of the meeting to search for.
  </Accordion>
</AccordionGroup>

### Basic Microsoft Teams Agent Setup

```python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

Example 3 (unknown):
```unknown
## Available Actions

<AccordionGroup>
  <Accordion title="microsoft_teams/get_teams">
    **Description:** Get all teams the user is a member of.

    **Parameters:**

    * No parameters required.
  </Accordion>

  <Accordion title="microsoft_teams/get_channels">
    **Description:** Get channels in a specific team.

    **Parameters:**

    * `team_id` (string, required): The ID of the team.
  </Accordion>

  <Accordion title="microsoft_teams/send_message">
    **Description:** Send a message to a Teams channel.

    **Parameters:**

    * `team_id` (string, required): The ID of the team.
    * `channel_id` (string, required): The ID of the channel.
    * `message` (string, required): The message content.
    * `content_type` (string, optional): Content type (html or text). Enum: `html`, `text`. Default is `text`.
  </Accordion>

  <Accordion title="microsoft_teams/get_messages">
    **Description:** Get messages from a Teams channel.

    **Parameters:**

    * `team_id` (string, required): The ID of the team.
    * `channel_id` (string, required): The ID of the channel.
    * `top` (integer, optional): Number of messages to retrieve (max 50). Default is `20`.
  </Accordion>

  <Accordion title="microsoft_teams/create_meeting">
    **Description:** Create a Teams meeting.

    **Parameters:**

    * `subject` (string, required): Meeting subject/title.
    * `startDateTime` (string, required): Meeting start time (ISO 8601 format with timezone).
    * `endDateTime` (string, required): Meeting end time (ISO 8601 format with timezone).
  </Accordion>

  <Accordion title="microsoft_teams/search_online_meetings_by_join_url">
    **Description:** Search online meetings by Join Web URL.

    **Parameters:**

    * `join_web_url` (string, required): The join web URL of the meeting to search for.
  </Accordion>
</AccordionGroup>

## Usage Examples

### Basic Microsoft Teams Agent Setup
```

---

## Microsoft Word Integration

**URL:** llms-txt#microsoft-word-integration

**Contents:**
- Overview
- Prerequisites
- Setting Up Microsoft Word Integration
  - 1. Connect Your Microsoft Account
  - 2. Install Required Package
  - 3. Environment Variable Setup
- Available Actions
- Usage Examples
  - Basic Microsoft Word Agent Setup

Source: https://docs.crewai.com/en/enterprise/integrations/microsoft_word

Document creation and management with Microsoft Word integration for CrewAI.

Enable your agents to create, read, and manage Word documents and text files in OneDrive or SharePoint. Automate document creation, retrieve content, manage document properties, and streamline your document workflows with AI-powered automation.

Before using the Microsoft Word integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A Microsoft account with Word and OneDrive/SharePoint access
* Connected your Microsoft account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)

## Setting Up Microsoft Word Integration

### 1. Connect Your Microsoft Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Microsoft Word** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for file access
5. Copy your Enterprise Token from [Integration Settings](https://app.crewai.com/crewai_plus/settings/integrations)

### 2. Install Required Package

### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>

Or add it to your `.env` file:

<AccordionGroup>
  <Accordion title="microsoft_word/get_documents">
    **Description:** Get all Word documents from OneDrive or SharePoint.

* `select` (string, optional): Select specific properties to return.
    * `filter` (string, optional): Filter results using OData syntax.
    * `expand` (string, optional): Expand related resources inline.
    * `top` (integer, optional): Number of items to return (min 1, max 999).
    * `orderby` (string, optional): Order results by specified properties.
  </Accordion>

<Accordion title="microsoft_word/create_text_document">
    **Description:** Create a text document (.txt) with content. RECOMMENDED for programmatic content creation that needs to be readable and editable.

* `file_name` (string, required): Name of the text document (should end with .txt).
    * `content` (string, optional): Text content for the document. Default is "This is a new text document created via API."
  </Accordion>

<Accordion title="microsoft_word/get_document_content">
    **Description:** Get the content of a document (works best with text files).

* `file_id` (string, required): The ID of the document.
  </Accordion>

<Accordion title="microsoft_word/get_document_properties">
    **Description:** Get properties and metadata of a document.

* `file_id` (string, required): The ID of the document.
  </Accordion>

<Accordion title="microsoft_word/delete_document">
    **Description:** Delete a document.

* `file_id` (string, required): The ID of the document to delete.
  </Accordion>
</AccordionGroup>

### Basic Microsoft Word Agent Setup

```python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

Example 3 (unknown):
```unknown
## Available Actions

<AccordionGroup>
  <Accordion title="microsoft_word/get_documents">
    **Description:** Get all Word documents from OneDrive or SharePoint.

    **Parameters:**

    * `select` (string, optional): Select specific properties to return.
    * `filter` (string, optional): Filter results using OData syntax.
    * `expand` (string, optional): Expand related resources inline.
    * `top` (integer, optional): Number of items to return (min 1, max 999).
    * `orderby` (string, optional): Order results by specified properties.
  </Accordion>

  <Accordion title="microsoft_word/create_text_document">
    **Description:** Create a text document (.txt) with content. RECOMMENDED for programmatic content creation that needs to be readable and editable.

    **Parameters:**

    * `file_name` (string, required): Name of the text document (should end with .txt).
    * `content` (string, optional): Text content for the document. Default is "This is a new text document created via API."
  </Accordion>

  <Accordion title="microsoft_word/get_document_content">
    **Description:** Get the content of a document (works best with text files).

    **Parameters:**

    * `file_id` (string, required): The ID of the document.
  </Accordion>

  <Accordion title="microsoft_word/get_document_properties">
    **Description:** Get properties and metadata of a document.

    **Parameters:**

    * `file_id` (string, required): The ID of the document.
  </Accordion>

  <Accordion title="microsoft_word/delete_document">
    **Description:** Delete a document.

    **Parameters:**

    * `file_id` (string, required): The ID of the document to delete.
  </Accordion>
</AccordionGroup>

## Usage Examples

### Basic Microsoft Word Agent Setup
```

---

## MLflow Integration

**URL:** llms-txt#mlflow-integration

Source: https://docs.crewai.com/en/observability/mlflow

Quickly start monitoring your Agents with MLflow.

---

## Modify the agent

**URL:** llms-txt#modify-the-agent

agent.goal = "New goal for analysis"

---

## MultiOn Tool

**URL:** llms-txt#multion-tool

**Contents:**
- Overview
- Installation
- Steps to Get Started
- Example

Source: https://docs.crewai.com/en/tools/automation/multiontool

The `MultiOnTool` empowers CrewAI agents with the capability to navigate and interact with the web through natural language instructions.

The `MultiOnTool` is designed to wrap [MultiOn's](https://docs.multion.ai/welcome) web browsing capabilities, enabling CrewAI agents to control web browsers using natural language instructions. This tool facilitates seamless web browsing, making it an essential asset for projects requiring dynamic web data interaction and automation of web-based tasks.

To use this tool, you need to install the MultiOn package:

You'll also need to install the MultiOn browser extension and enable API usage.

## Steps to Get Started

To effectively use the `MultiOnTool`, follow these steps:

1. **Install CrewAI**: Ensure that the `crewai[tools]` package is installed in your Python environment.
2. **Install and use MultiOn**: Follow [MultiOn documentation](https://docs.multion.ai/learn/browser-extension) for installing the MultiOn Browser Extension.
3. **Enable API Usage**: Click on the MultiOn extension in the extensions folder of your browser (not the hovering MultiOn icon on the web page) to open the extension configurations. Click the API Enabled toggle to enable the API.

The following example demonstrates how to initialize the tool and execute a web browsing task:

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import MultiOnTool

**Examples:**

Example 1 (unknown):
```unknown
You'll also need to install the MultiOn browser extension and enable API usage.

## Steps to Get Started

To effectively use the `MultiOnTool`, follow these steps:

1. **Install CrewAI**: Ensure that the `crewai[tools]` package is installed in your Python environment.
2. **Install and use MultiOn**: Follow [MultiOn documentation](https://docs.multion.ai/learn/browser-extension) for installing the MultiOn Browser Extension.
3. **Enable API Usage**: Click on the MultiOn extension in the extensions folder of your browser (not the hovering MultiOn icon on the web page) to open the extension configurations. Click the API Enabled toggle to enable the API.

## Example

The following example demonstrates how to initialize the tool and execute a web browsing task:
```

---

## Notion Integration

**URL:** llms-txt#notion-integration

**Contents:**
- Overview
- Prerequisites
- Setting Up Notion Integration
  - 1. Connect Your Notion Account
  - 2. Install Required Package
  - 3. Environment Variable Setup
- Available Actions
- Usage Examples
  - Basic Notion Agent Setup

Source: https://docs.crewai.com/en/enterprise/integrations/notion

User management and commenting with Notion integration for CrewAI.

Enable your agents to manage users and create comments through Notion. Access workspace user information and create comments on pages and discussions, streamlining your collaboration workflows with AI-powered automation.

Before using the Notion integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A Notion account with appropriate workspace permissions
* Connected your Notion account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)

## Setting Up Notion Integration

### 1. Connect Your Notion Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Notion** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for user access and comment creation
5. Copy your Enterprise Token from [Integration Settings](https://app.crewai.com/crewai_plus/settings/integrations)

### 2. Install Required Package

### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>

Or add it to your `.env` file:

<AccordionGroup>
  <Accordion title="notion/list_users">
    **Description:** List all users in the workspace.

* `page_size` (integer, optional): Number of items returned in the response. Minimum: 1, Maximum: 100, Default: 100
    * `start_cursor` (string, optional): Cursor for pagination. Return results after this cursor.
  </Accordion>

<Accordion title="notion/get_user">
    **Description:** Retrieve a specific user by ID.

* `user_id` (string, required): The ID of the user to retrieve.
  </Accordion>

<Accordion title="notion/create_comment">
    **Description:** Create a comment on a page or discussion.

* `parent` (object, required): The parent page or discussion to comment on.
      
      or
      
    * `rich_text` (array, required): The rich text content of the comment.
      
  </Accordion>
</AccordionGroup>

### Basic Notion Agent Setup

```python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

Example 3 (unknown):
```unknown
## Available Actions

<AccordionGroup>
  <Accordion title="notion/list_users">
    **Description:** List all users in the workspace.

    **Parameters:**

    * `page_size` (integer, optional): Number of items returned in the response. Minimum: 1, Maximum: 100, Default: 100
    * `start_cursor` (string, optional): Cursor for pagination. Return results after this cursor.
  </Accordion>

  <Accordion title="notion/get_user">
    **Description:** Retrieve a specific user by ID.

    **Parameters:**

    * `user_id` (string, required): The ID of the user to retrieve.
  </Accordion>

  <Accordion title="notion/create_comment">
    **Description:** Create a comment on a page or discussion.

    **Parameters:**

    * `parent` (object, required): The parent page or discussion to comment on.
```

Example 4 (unknown):
```unknown
or
```

---

## No crew knowledge needed

**URL:** llms-txt#no-crew-knowledge-needed

crew = Crew(agents=[agent], tasks=[task])
result = crew.kickoff()  # Works perfectly
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
#### Example 2: Both Agent and Crew Knowledge
```

---

## No crew-level knowledge required

**URL:** llms-txt#no-crew-level-knowledge-required

crew = Crew(
    agents=[specialist_agent],
    tasks=[task]
)

result = crew.kickoff()  # Agent knowledge works independently
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
#### What Happens During `crew.kickoff()`

When you call `crew.kickoff()`, here's the exact sequence:
```

---

## OpenLIT Integration

**URL:** llms-txt#openlit-integration

Source: https://docs.crewai.com/en/observability/openlit

Quickly start monitoring your Agents in just a single line of code with OpenTelemetry.

---

## OpenLIT Overview

**URL:** llms-txt#openlit-overview

**Contents:**
  - Features
- Setup Instructions

[OpenLIT](https://github.com/openlit/openlit?src=crewai-docs) is an open-source tool that makes it simple to monitor the performance of AI agents, LLMs, VectorDBs, and GPUs with just **one** line of code.

It provides OpenTelemetry-native tracing and metrics to track important parameters like cost, latency, interactions and task sequences.
This setup enables you to track hyperparameters and monitor for performance issues, helping you find ways to enhance and fine-tune your agents over time.

<Frame>
  <img alt="Overview Agent usage including cost and tokens" />

<img alt="Overview of agent otel traces and metrics" />

<img alt="Overview of agent traces in details" />
</Frame>

* **Analytics Dashboard**: Monitor your Agents health and performance with detailed dashboards that track metrics, costs, and user interactions.
* **OpenTelemetry-native Observability SDK**: Vendor-neutral SDKs to send traces and metrics to your existing observability tools like Grafana, DataDog and more.
* **Cost Tracking for Custom and Fine-Tuned Models**: Tailor cost estimations for specific models using custom pricing files for precise budgeting.
* **Exceptions Monitoring Dashboard**: Quickly spot and resolve issues by tracking common exceptions and errors with a monitoring dashboard.
* **Compliance and Security**: Detect potential threats such as profanity and PII leaks.
* **Prompt Injection Detection**: Identify potential code injection and secret leaks.
* **API Keys and Secrets Management**: Securely handle your LLM API keys and secrets centrally, avoiding insecure practices.
* **Prompt Management**: Manage and version Agent prompts using PromptHub for consistent and easy access across Agents.
* **Model Playground** Test and compare different models for your CrewAI agents before deployment.

## Setup Instructions

<Steps>
  <Step title="Deploy OpenLIT">
    <Steps>
      <Step title="Git Clone OpenLIT Repository">
        
      </Step>

<Step title="Start Docker Compose">
        From the root directory of the [OpenLIT Repo](https://github.com/openlit/openlit), Run the below command:

</Step>
    </Steps>
  </Step>

<Step title="Install OpenLIT SDK">
    
  </Step>

<Step title="Initialize OpenLIT in Your Application">
    Add the following two lines to your application code:

<Tabs>
      <Tab title="Setup using function arguments">

Example Usage for monitoring a CrewAI Agent:

<Tab title="Setup using Environment Variables">
        Add the following two lines to your application code:

Run the following command to configure the OTEL export endpoint:

Example Usage for monitoring a CrewAI Async Agent:

Refer to OpenLIT [Python SDK repository](https://github.com/openlit/openlit/tree/main/sdk/python) for more advanced configurations and use cases.
  </Step>

<Step title="Visualize and Analyze">
    With the Agent Observability data now being collected and sent to OpenLIT, the next step is to visualize and analyze this data to get insights into your Agent's performance, behavior, and identify areas of improvement.

Just head over to OpenLIT at `127.0.0.1:3000` on your browser to start exploring. You can login using the default credentials

* **Email**: `user@openlit.io`
    * **Password**: `openlituser`

<Frame>
      <img alt="Overview Agent usage including cost and tokens" />

<img alt="Overview of agent otel traces and metrics" />
    </Frame>
  </Step>
</Steps>

**Examples:**

Example 1 (unknown):
```unknown
</Step>

      <Step title="Start Docker Compose">
        From the root directory of the [OpenLIT Repo](https://github.com/openlit/openlit), Run the below command:
```

Example 2 (unknown):
```unknown
</Step>
    </Steps>
  </Step>

  <Step title="Install OpenLIT SDK">
```

Example 3 (unknown):
```unknown
</Step>

  <Step title="Initialize OpenLIT in Your Application">
    Add the following two lines to your application code:

    <Tabs>
      <Tab title="Setup using function arguments">
```

Example 4 (unknown):
```unknown
Example Usage for monitoring a CrewAI Agent:
```

---

## Open Telemetry Logs

**URL:** llms-txt#open-telemetry-logs

**Contents:**
- Prerequisites
- How to capture telemetry logs

Source: https://docs.crewai.com/en/enterprise/guides/capture_telemetry_logs

Understand how to capture telemetry logs from your CrewAI AOP deployments

CrewAI AOP provides a powerful way to capture telemetry logs from your deployments. This allows you to monitor the performance of your agents and workflows, and to debug issues that may arise.

<CardGroup>
  <Card title="ENTERPRISE OTEL SETUP enabled" icon="users">
    Your organization should have ENTERPRISE OTEL SETUP enabled
  </Card>

<Card title="OTEL collector setup" icon="server">
    Your organization should have an OTEL collector setup or a provider like Datadog log intake setup
  </Card>
</CardGroup>

## How to capture telemetry logs

1. Go to settings/organization tab
2. Configure your OTEL collector setup
3. Save

Example to setup OTEL log collection capture to Datadog.

<Frame>
  <img alt="Capture Telemetry Logs" />
</Frame>

---

## Option 1: Match your LLM provider

**URL:** llms-txt#option-1:-match-your-llm-provider

crew = Crew(
    agents=[agent],
    tasks=[task],
    memory=True,
    embedder={
        "provider": "anthropic", # Match your LLM provider
        "config": {
            "api_key": "your-anthropic-key",
            "model": "text-embedding-3-small"
        }
    }
)

---

## Option 1: Use Voyage AI (recommended by Anthropic for Claude users)

**URL:** llms-txt#option-1:-use-voyage-ai-(recommended-by-anthropic-for-claude-users)

crew = Crew(
    agents=[agent],
    tasks=[...],
    knowledge_sources=[knowledge_source],
    embedder={
        "provider": "voyageai",  # Recommended for Claude users
        "config": {
            "api_key": "your-voyage-api-key",
            "model": "voyage-3"  # or "voyage-3-large" for best quality
        }
    }
)

---

## Option 2: Use local embeddings (no external API calls)

**URL:** llms-txt#option-2:-use-local-embeddings-(no-external-api-calls)

**Contents:**
  - Debugging Storage Issues

crew = Crew(
    agents=[agent],
    tasks=[task],
    memory=True,
    embedder={
        "provider": "ollama",
        "config": {"model": "mxbai-embed-large"}
    }
)
python theme={null}
import os
from crewai.utilities.paths import db_storage_path

storage_path = db_storage_path()
print(f"Storage path: {storage_path}")
print(f"Path exists: {os.path.exists(storage_path)}")
print(f"Is writable: {os.access(storage_path, os.W_OK) if os.path.exists(storage_path) else 'Path does not exist'}")

**Examples:**

Example 1 (unknown):
```unknown
### Debugging Storage Issues

#### Check Storage Permissions
```

---

## Option 3: Agent-level embedding customization

**URL:** llms-txt#option-3:-agent-level-embedding-customization

**Contents:**
- Advanced Features
  - Query Rewriting

agent = Agent(
    role="Researcher",
    goal="Research topics",
    backstory="Expert researcher",
    knowledge_sources=[knowledge_source],
    embedder={
        "provider": "google-generativeai",
        "config": {
            "model_name": "gemini-embedding-001",
            "api_key": "your-google-key"
        }
    }
)
python theme={null}
agent = Agent(
    role="Researcher",
    goal="Research topics",
    backstory="Expert researcher",
    knowledge_sources=[knowledge_source],
    embedder={
        "provider": "azure",
        "config": {
            "api_key": "your-azure-api-key",
            "model": "text-embedding-ada-002", # change to the model you are using and is deployed in Azure
            "api_base": "https://your-azure-endpoint.openai.azure.com/",
            "api_version": "2024-02-01"
        }
    }
)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
#### Configuring Azure OpenAI Embeddings

When using Azure OpenAI embeddings:

1. Make sure you deploy the embedding model in Azure platform first
2. Then you need to use the following configuration:
```

Example 2 (unknown):
```unknown
## Advanced Features

### Query Rewriting

CrewAI implements an intelligent query rewriting mechanism to optimize knowledge retrieval. When an agent needs to search through knowledge sources, the raw task prompt is automatically transformed into a more effective search query.

#### How Query Rewriting Works

1. When an agent executes a task with knowledge sources available, the `_get_knowledge_search_query` method is triggered
2. The agent's LLM is used to transform the original task prompt into an optimized search query
3. This optimized query is then used to retrieve relevant information from knowledge sources

#### Benefits of Query Rewriting

<CardGroup>
  <Card title="Improved Retrieval Accuracy" icon="bullseye-arrow">
    By focusing on key concepts and removing irrelevant content, query rewriting helps retrieve more relevant information.
  </Card>

  <Card title="Context Awareness" icon="brain">
    The rewritten queries are designed to be more specific and context-aware for vector database retrieval.
  </Card>
</CardGroup>

#### Example
```

---

## Or use consistent embedding providers

**URL:** llms-txt#or-use-consistent-embedding-providers

crew = Crew(
    agents=[...],
    tasks=[...],
    knowledge_sources=[...],
    embedder={"provider": "openai", "config": {"model": "text-embedding-3-small"}}
)
bash theme={null}

**Examples:**

Example 1 (unknown):
```unknown
**"ChromaDB permission denied" errors:**
```

---

## Overview

**URL:** llms-txt#overview

**Contents:**
- **Available Tools**
- **Common Use Cases**
- **Quick Start Example**

Source: https://docs.crewai.com/en/tools/integration/overview

Connect CrewAI agents with external automations and managed AI services

Integration tools let your agents hand off work to other automation platforms and managed AI services. Use them when a workflow needs to invoke an existing CrewAI deployment or delegate specialised tasks to providers such as Amazon Bedrock.

## **Available Tools**

<CardGroup>
  <Card title="Merge Agent Handler Tool" icon="diagram-project" href="/en/tools/integration/mergeagenthandlertool">
    Securely access hundreds of third-party tools like Linear, GitHub, Slack, and more through Merge's unified API.
  </Card>

<Card title="CrewAI Run Automation Tool" icon="robot" href="/en/tools/integration/crewaiautomationtool">
    Invoke live CrewAI Platform automations, pass custom inputs, and poll for results directly from your agent.
  </Card>

<Card title="Bedrock Invoke Agent Tool" icon="aws" href="/en/tools/integration/bedrockinvokeagenttool">
    Call Amazon Bedrock Agents from your crews, reuse AWS guardrails, and stream responses back into the workflow.
  </Card>
</CardGroup>

## **Common Use Cases**

* **Chain automations**: Kick off an existing CrewAI deployment from within another crew or flow
* **Enterprise hand-off**: Route tasks to Bedrock Agents that already encapsulate company logic and guardrails
* **Hybrid workflows**: Combine CrewAI reasoning with downstream systems that expose their own agent APIs
* **Long-running jobs**: Poll external automations and merge the final results back into the current run

## **Quick Start Example**

```python theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import InvokeCrewAIAutomationTool
from crewai_tools.aws.bedrock.agents.invoke_agent_tool import BedrockInvokeAgentTool

---

## Patronus AI Evaluation

**URL:** llms-txt#patronus-ai-evaluation

**Contents:**
- Overview
- Key Features
- Evaluation Tools
- Installation
- Steps to Get Started
- Examples
  - Using PatronusEvalTool

[Patronus AI](https://patronus.ai) provides comprehensive evaluation and monitoring capabilities for CrewAI agents, enabling you to assess model outputs, agent behaviors, and overall system performance. This integration allows you to implement continuous evaluation workflows that help maintain quality and reliability in production environments.

* **Automated Evaluation**: Real-time assessment of agent outputs and behaviors
* **Custom Criteria**: Define specific evaluation criteria tailored to your use cases
* **Performance Monitoring**: Track agent performance metrics over time
* **Quality Assurance**: Ensure consistent output quality across different scenarios
* **Safety & Compliance**: Monitor for potential issues and policy violations

Patronus provides three main evaluation tools for different use cases:

1. **PatronusEvalTool**: Allows agents to select the most appropriate evaluator and criteria for the evaluation task.
2. **PatronusPredefinedCriteriaEvalTool**: Uses predefined evaluator and criteria specified by the user.
3. **PatronusLocalEvaluatorTool**: Uses custom function evaluators defined by the user.

To use these tools, you need to install the Patronus package:

You'll also need to set up your Patronus API key as an environment variable:

## Steps to Get Started

To effectively use the Patronus evaluation tools, follow these steps:

1. **Install Patronus**: Install the Patronus package using the command above.
2. **Set Up API Key**: Set your Patronus API key as an environment variable.
3. **Choose the Right Tool**: Select the appropriate Patronus evaluation tool based on your needs.
4. **Configure the Tool**: Configure the tool with the necessary parameters.

### Using PatronusEvalTool

The following example demonstrates how to use the `PatronusEvalTool`, which allows agents to select the most appropriate evaluator and criteria:

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import PatronusEvalTool

**Examples:**

Example 1 (unknown):
```unknown
You'll also need to set up your Patronus API key as an environment variable:
```

Example 2 (unknown):
```unknown
## Steps to Get Started

To effectively use the Patronus evaluation tools, follow these steps:

1. **Install Patronus**: Install the Patronus package using the command above.
2. **Set Up API Key**: Set your Patronus API key as an environment variable.
3. **Choose the Right Tool**: Select the appropriate Patronus evaluation tool based on your needs.
4. **Configure the Tool**: Configure the tool with the necessary parameters.

## Examples

### Using PatronusEvalTool

The following example demonstrates how to use the `PatronusEvalTool`, which allows agents to select the most appropriate evaluator and criteria:
```

---

## Processes

**URL:** llms-txt#processes

**Contents:**
- Overview
- Process Implementations
- The Role of Processes in Teamwork
- Assigning Processes to a Crew

Source: https://docs.crewai.com/en/concepts/processes

Detailed guide on workflow management through processes in CrewAI, with updated implementation details.

<Tip>
  Processes orchestrate the execution of tasks by agents, akin to project management in human teams.
  These processes ensure tasks are distributed and executed efficiently, in alignment with a predefined strategy.
</Tip>

## Process Implementations

* **Sequential**: Executes tasks sequentially, ensuring tasks are completed in an orderly progression.
* **Hierarchical**: Organizes tasks in a managerial hierarchy, where tasks are delegated and executed based on a structured chain of command. A manager language model (`manager_llm`) or a custom manager agent (`manager_agent`) must be specified in the crew to enable the hierarchical process, facilitating the creation and management of tasks by the manager.
* **Consensual Process (Planned)**: Aiming for collaborative decision-making among agents on task execution, this process type introduces a democratic approach to task management within CrewAI. It is planned for future development and is not currently implemented in the codebase.

## The Role of Processes in Teamwork

Processes enable individual agents to operate as a cohesive unit, streamlining their efforts to achieve common objectives with efficiency and coherence.

## Assigning Processes to a Crew

To assign a process to a crew, specify the process type upon crew creation to set the execution strategy. For a hierarchical process, ensure to define `manager_llm` or `manager_agent` for the manager agent.

```python theme={null}
from crewai import Crew, Process

---

## psycopg2 was installed to run this example with PostgreSQL

**URL:** llms-txt#psycopg2-was-installed-to-run-this-example-with-postgresql

**Contents:**
- Example

nl2sql = NL2SQLTool(db_uri="postgresql://example@localhost:5432/test_db")

@agent
def researcher(self) -> Agent:
    return Agent(
        config=self.agents_config["researcher"],
        allow_delegation=False,
        tools=[nl2sql]
    )
md theme={null}
 DB -> Agent -> ... -> Agent -> DB
```

**Examples:**

Example 1 (unknown):
```unknown
## Example

The primary task goal was:

"Retrieve the average, maximum, and minimum monthly revenue for each city, but only include cities that have more than one user. Also, count the number of user in each city and
sort the results by the average monthly revenue in descending order"

So the Agent tried to get information from the DB, the first one is wrong so the Agent tries again and gets the correct information and passes to the next agent.

![alt text](https://github.com/crewAIInc/crewAI-tools/blob/main/crewai_tools/tools/nl2sql/images/image-2.png?raw=true)
![alt text](https://github.com/crewAIInc/crewAI-tools/raw/main/crewai_tools/tools/nl2sql/images/image-3.png)

The second task goal was:

"Review the data and create a detailed report, and then create the table on the database with the fields based on the data provided.
Include information on the average, maximum, and minimum monthly revenue for each city, but only include cities that have more than one user. Also, count the number of users in each city and sort the results by the average monthly revenue in descending order."

Now things start to get interesting, the Agent generates the SQL query to not only create the table but also insert the data into the table. And in the end the Agent still returns the final report which is exactly what was in the database.

![alt text](https://github.com/crewAIInc/crewAI-tools/raw/main/crewai_tools/tools/nl2sql/images/image-4.png)
![alt text](https://github.com/crewAIInc/crewAI-tools/raw/main/crewai_tools/tools/nl2sql/images/image-5.png)

![alt text](https://github.com/crewAIInc/crewAI-tools/raw/main/crewai_tools/tools/nl2sql/images/image-9.png)
![alt text](https://github.com/crewAIInc/crewAI-tools/raw/main/crewai_tools/tools/nl2sql/images/image-7.png)

This is a simple example of how the NL2SQLTool can be used to interact with the database and generate reports based on the data in the database.

The Tool provides endless possibilities on the logic of the Agent and how it can interact with the database.
```

---

## Qdrant Vector Search Tool

**URL:** llms-txt#qdrant-vector-search-tool

**Contents:**
- Overview
- Installation
- Basic Usage

Source: https://docs.crewai.com/en/tools/database-data/qdrantvectorsearchtool

Semantic search capabilities for CrewAI agents using Qdrant vector database

The Qdrant Vector Search Tool enables semantic search capabilities in your CrewAI agents by leveraging [Qdrant](https://qdrant.tech/), a vector similarity search engine. This tool allows your agents to search through documents stored in a Qdrant collection using semantic similarity.

Install the required packages:

Here's a minimal example of how to use the tool:

```python theme={null}
from crewai import Agent
from crewai_tools import QdrantVectorSearchTool, QdrantConfig

**Examples:**

Example 1 (unknown):
```unknown
## Basic Usage

Here's a minimal example of how to use the tool:
```

---

## Reasoning

**URL:** llms-txt#reasoning

**Contents:**
- Overview
- Usage
- How It Works
- Configuration Options
- Example

Source: https://docs.crewai.com/en/concepts/reasoning

Learn how to enable and use agent reasoning to improve task execution.

Agent reasoning is a feature that allows agents to reflect on a task and create a plan before execution. This helps agents approach tasks more methodically and ensures they're ready to perform the assigned work.

To enable reasoning for an agent, simply set `reasoning=True` when creating the agent:

When reasoning is enabled, before executing a task, the agent will:

1. Reflect on the task and create a detailed plan
2. Evaluate whether it's ready to execute the task
3. Refine the plan as necessary until it's ready or max\_reasoning\_attempts is reached
4. Inject the reasoning plan into the task description before execution

This process helps the agent break down complex tasks into manageable steps and identify potential challenges before starting.

## Configuration Options

<ParamField type="bool">
  Enable or disable reasoning
</ParamField>

<ParamField type="int">
  Maximum number of attempts to refine the plan before proceeding with execution. If None (default), the agent will continue refining until it's ready.
</ParamField>

Here's a complete example:

```python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
## How It Works

When reasoning is enabled, before executing a task, the agent will:

1. Reflect on the task and create a detailed plan
2. Evaluate whether it's ready to execute the task
3. Refine the plan as necessary until it's ready or max\_reasoning\_attempts is reached
4. Inject the reasoning plan into the task description before execution

This process helps the agent break down complex tasks into manageable steps and identify potential challenges before starting.

## Configuration Options

<ParamField type="bool">
  Enable or disable reasoning
</ParamField>

<ParamField type="int">
  Maximum number of attempts to refine the plan before proceeding with execution. If None (default), the agent will continue refining until it's ready.
</ParamField>

## Example

Here's a complete example:
```

---

## Replay from a specific task

**URL:** llms-txt#replay-from-a-specific-task

**Contents:**
- The Art of the Possible: Beyond Your First Crew
  - Expanding Your Crew
  - Adding Tools and Capabilities
  - Creating More Complex Workflows
  - Applying to Different Domains
- Next Steps

crewai replay -t <task_id>
```

## The Art of the Possible: Beyond Your First Crew

What you've built in this guide is just the beginning. The skills and patterns you've learned can be applied to create increasingly sophisticated AI systems. Here are some ways you could extend this basic research crew:

### Expanding Your Crew

You could add more specialized agents to your crew:

* A **fact-checker** to verify research findings
* A **data visualizer** to create charts and graphs
* A **domain expert** with specialized knowledge in a particular area
* A **critic** to identify weaknesses in the analysis

### Adding Tools and Capabilities

You could enhance your agents with additional tools:

* Web browsing tools for real-time research
* CSV/database tools for data analysis
* Code execution tools for data processing
* API connections to external services

### Creating More Complex Workflows

You could implement more sophisticated processes:

* Hierarchical processes where manager agents delegate to worker agents
* Iterative processes with feedback loops for refinement
* Parallel processes where multiple agents work simultaneously
* Dynamic processes that adapt based on intermediate results

### Applying to Different Domains

The same patterns can be applied to create crews for:

* **Content creation**: Writers, editors, fact-checkers, and designers working together
* **Customer service**: Triage agents, specialists, and quality control working together
* **Product development**: Researchers, designers, and planners collaborating
* **Data analysis**: Data collectors, analysts, and visualization specialists

Now that you've built your first crew, you can:

1. Experiment with different agent configurations and personalities
2. Try more complex task structures and workflows
3. Implement custom tools to give your agents new capabilities
4. Apply your crew to different topics or problem domains
5. Explore [CrewAI Flows](/en/guides/flows/first-flow) for more advanced workflows with procedural programming

<Check>
  Congratulations! You've successfully built your first CrewAI crew that can research and analyze any topic you provide. This foundational experience has equipped you with the skills to create increasingly sophisticated AI systems that can tackle complex, multi-stage problems through collaborative intelligence.
</Check>

---

## Replay Tasks from Latest Crew Kickoff

**URL:** llms-txt#replay-tasks-from-latest-crew-kickoff

**Contents:**
- Introduction
  - Replaying from Specific Task Using the CLI
  - Replaying from a Task Programmatically
- Conclusion

Source: https://docs.crewai.com/en/learn/replay-tasks-from-latest-crew-kickoff

Replay tasks from the latest crew.kickoff(...)

CrewAI provides the ability to replay from a task specified from the latest crew kickoff. This feature is particularly useful when you've finished a kickoff and may want to retry certain tasks or don't need to refetch data over and your agents already have the context saved from the kickoff execution so you just need to replay the tasks you want to.

<Note>
  You must run `crew.kickoff()` before you can replay a task.
  Currently, only the latest kickoff is supported, so if you use `kickoff_for_each`, it will only allow you to replay from the most recent crew run.
</Note>

Here's an example of how to replay from a task:

### Replaying from Specific Task Using the CLI

To use the replay feature, follow these steps:

<Steps>
  <Step title="Open your terminal or command prompt." />

<Step title="Navigate to the directory where your CrewAI project is located." />

<Step title="Run the following commands:">
    To view the latest kickoff task\_ids use:

Once you have your `task_id` to replay, use:

<Note>
  Ensure `crewai` is installed and configured correctly in your development environment.
</Note>

### Replaying from a Task Programmatically

To replay from a task programmatically, use the following steps:

<Steps>
  <Step title="Specify the `task_id` and input parameters for the replay process.">
    Specify the `task_id` and input parameters for the replay process.
  </Step>

<Step title="Execute the replay command within a try-except block to handle potential errors.">
    Execute the replay command within a try-except block to handle potential errors.

<CodeGroup>
      
    </CodeGroup>
  </Step>
</Steps>

With the above enhancements and detailed functionality, replaying specific tasks in CrewAI has been made more efficient and robust.
Ensure you follow the commands and steps precisely to make the most of these features.

**Examples:**

Example 1 (unknown):
```unknown
Once you have your `task_id` to replay, use:
```

Example 2 (unknown):
```unknown
</Step>
</Steps>

<Note>
  Ensure `crewai` is installed and configured correctly in your development environment.
</Note>

### Replaying from a Task Programmatically

To replay from a task programmatically, use the following steps:

<Steps>
  <Step title="Specify the `task_id` and input parameters for the replay process.">
    Specify the `task_id` and input parameters for the replay process.
  </Step>

  <Step title="Execute the replay command within a try-except block to handle potential errors.">
    Execute the replay command within a try-except block to handle potential errors.

    <CodeGroup>
```

---

## Research Agent

**URL:** llms-txt#research-agent

role: "Research Specialist for technical topics"
goal: "Gather comprehensive, accurate information from authoritative sources"
backstory: "You are a meticulous researcher with a background in library science..."

---

## Reset all memory storage

**URL:** llms-txt#reset-all-memory-storage

crew = Crew(agents=[...], tasks=[...], memory=True)

---

## Reset both crew and agent knowledge

**URL:** llms-txt#reset-both-crew-and-agent-knowledge

crew.reset_memories(command_type='knowledge')

---

## Reset only agent-specific knowledge

**URL:** llms-txt#reset-only-agent-specific-knowledge

crew.reset_memories(command_type='agent_knowledge')

---

## rest of the code ...

**URL:** llms-txt#rest-of-the-code-...

**Contents:**
- Conclusion

Tools are pivotal in extending the capabilities of CrewAI agents, enabling them to undertake a broad spectrum of tasks and collaborate effectively.
When building solutions with CrewAI, leverage both custom and existing tools to empower your agents and enhance the AI ecosystem. Consider utilizing error handling, caching mechanisms,
and the flexibility of tool arguments to optimize your agents' performance and capabilities.

---

## Run CrewAI workflow

**URL:** llms-txt#run-crewai-workflow

**Contents:**
- Tool Parameters
  - Required Parameters
  - QdrantConfig Parameters
  - Optional Tool Parameters
- Advanced Filtering
  - Dynamic Filtering

crew = Crew(
    agents=[search_agent, answer_agent],
    tasks=[search_task, answer_task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff(
    inputs={"query": "What is the role of X in the document?"}
)
print(result)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## Tool Parameters

### Required Parameters

* `qdrant_config` (QdrantConfig): Configuration object containing all Qdrant settings

### QdrantConfig Parameters

* `qdrant_url` (str): The URL of your Qdrant server
* `qdrant_api_key` (str, optional): API key for authentication with Qdrant
* `collection_name` (str): Name of the Qdrant collection to search
* `limit` (int): Maximum number of results to return (default: 3)
* `score_threshold` (float): Minimum similarity score threshold (default: 0.35)
* `filter` (Any, optional): Qdrant Filter instance for advanced filtering (default: None)

### Optional Tool Parameters

* `custom_embedding_fn` (Callable\[\[str], list\[float]]): Custom function for text vectorization
* `qdrant_package` (str): Base package path for Qdrant (default: "qdrant\_client")
* `client` (Any): Pre-initialized Qdrant client (optional)

## Advanced Filtering

The QdrantVectorSearchTool supports powerful filtering capabilities to refine your search results:

### Dynamic Filtering

Use `filter_by` and `filter_value` parameters in your search to filter results on-the-fly:
```

---

## Run the task

**URL:** llms-txt#run-the-task

**Contents:**
- Implementation Details
- Conclusion

crew = Crew(agents=[browser_agent], tasks=[search_task])
result = crew.kickoff()
python Code theme={null}
class MultiOnTool(BaseTool):
    """Tool to wrap MultiOn Browse Capabilities."""

name: str = "Multion Browse Tool"
    description: str = """Multion gives the ability for LLMs to control web browsers using natural language instructions.
            If the status is 'CONTINUE', reissue the same instruction to continue execution
        """
    
    # Implementation details...
    
    def _run(self, cmd: str, *args: Any, **kwargs: Any) -> str:
        """
        Run the Multion client with the given command.
        
        Args:
            cmd (str): The detailed and specific natural language instruction for web browsing
            *args (Any): Additional arguments to pass to the Multion client
            **kwargs (Any): Additional keyword arguments to pass to the Multion client
        """
        # Implementation details...
```

The `MultiOnTool` provides a powerful way to integrate web browsing capabilities into CrewAI agents. By enabling agents to interact with websites through natural language instructions, it opens up a wide range of possibilities for web-based tasks, from data collection and research to automated interactions with web services.

**Examples:**

Example 1 (unknown):
```unknown
If the status returned is `CONTINUE`, the agent should be instructed to reissue the same instruction to continue execution.

## Implementation Details

The `MultiOnTool` is implemented as a subclass of `BaseTool` from CrewAI. It wraps the MultiOn client to provide web browsing capabilities:
```

---

## Run the task through a crew

**URL:** llms-txt#run-the-task-through-a-crew

**Contents:**
- Implementation Details
- Conclusion

crew = Crew(agents=[web_scraper_agent], tasks=[extract_task])
result = crew.kickoff()
python Code theme={null}
class ScrapeElementFromWebsiteTool(BaseTool):
    name: str = "Read a website content"
    description: str = "A tool that can be used to read a website content."
    
    # Implementation details...
    
    def _run(self, **kwargs: Any) -> Any:
        website_url = kwargs.get("website_url", self.website_url)
        css_element = kwargs.get("css_element", self.css_element)
        page = requests.get(
            website_url,
            headers=self.headers,
            cookies=self.cookies if self.cookies else {},
        )
        parsed = BeautifulSoup(page.content, "html.parser")
        elements = parsed.select(css_element)
        return "\n".join([element.get_text() for element in elements])
```

The `ScrapeElementFromWebsiteTool` provides a powerful way to extract specific elements from websites using CSS selectors. By enabling agents to target only the content they need, it makes web scraping tasks more efficient and focused. This tool is particularly useful for data extraction, content monitoring, and research tasks where specific information needs to be extracted from web pages.

**Examples:**

Example 1 (unknown):
```unknown
## Implementation Details

The `ScrapeElementFromWebsiteTool` uses the `requests` library to fetch the web page and `BeautifulSoup` to parse the HTML and extract the specified elements:
```

---

## `S3ReaderTool`

**URL:** llms-txt#`s3readertool`

**Contents:**
- Description
- Installation
- Steps to Get Started
- Example

The `S3ReaderTool` is designed to read files from Amazon S3 buckets. This tool allows CrewAI agents to access and retrieve content stored in S3, making it ideal for workflows that require reading data, configuration files, or any other content stored in AWS S3 storage.

To use this tool, you need to install the required dependencies:

## Steps to Get Started

To effectively use the `S3ReaderTool`, follow these steps:

1. **Install Dependencies**: Install the required packages using the command above.
2. **Configure AWS Credentials**: Set up your AWS credentials as environment variables.
3. **Initialize the Tool**: Create an instance of the tool.
4. **Specify S3 Path**: Provide the S3 path to the file you want to read.

The following example demonstrates how to use the `S3ReaderTool` to read a file from an S3 bucket:

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools.aws.s3 import S3ReaderTool

**Examples:**

Example 1 (unknown):
```unknown
## Steps to Get Started

To effectively use the `S3ReaderTool`, follow these steps:

1. **Install Dependencies**: Install the required packages using the command above.
2. **Configure AWS Credentials**: Set up your AWS credentials as environment variables.
3. **Initialize the Tool**: Create an instance of the tool.
4. **Specify S3 Path**: Provide the S3 path to the file you want to read.

## Example

The following example demonstrates how to use the `S3ReaderTool` to read a file from an S3 bucket:
```

---

## `S3WriterTool`

**URL:** llms-txt#`s3writertool`

**Contents:**
- Description
- Installation
- Steps to Get Started
- Example

The `S3WriterTool` is designed to write content to files in Amazon S3 buckets. This tool allows CrewAI agents to create or update files in S3, making it ideal for workflows that require storing data, saving configuration files, or persisting any other content to AWS S3 storage.

To use this tool, you need to install the required dependencies:

## Steps to Get Started

To effectively use the `S3WriterTool`, follow these steps:

1. **Install Dependencies**: Install the required packages using the command above.
2. **Configure AWS Credentials**: Set up your AWS credentials as environment variables.
3. **Initialize the Tool**: Create an instance of the tool.
4. **Specify S3 Path and Content**: Provide the S3 path where you want to write the file and the content to be written.

The following example demonstrates how to use the `S3WriterTool` to write content to a file in an S3 bucket:

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools.aws.s3 import S3WriterTool

**Examples:**

Example 1 (unknown):
```unknown
## Steps to Get Started

To effectively use the `S3WriterTool`, follow these steps:

1. **Install Dependencies**: Install the required packages using the command above.
2. **Configure AWS Credentials**: Set up your AWS credentials as environment variables.
3. **Initialize the Tool**: Create an instance of the tool.
4. **Specify S3 Path and Content**: Provide the S3 path where you want to write the file and the content to be written.

## Example

The following example demonstrates how to use the `S3WriterTool` to write content to a file in an S3 bucket:
```

---

## S3 Reader Tool

**URL:** llms-txt#s3-reader-tool

Source: https://docs.crewai.com/en/tools/cloud-storage/s3readertool

The `S3ReaderTool` enables CrewAI agents to read files from Amazon S3 buckets.

---

## S3 Writer Tool

**URL:** llms-txt#s3-writer-tool

Source: https://docs.crewai.com/en/tools/cloud-storage/s3writertool

The `S3WriterTool` enables CrewAI agents to write content to files in Amazon S3 buckets.

---

## Salesforce Integration

**URL:** llms-txt#salesforce-integration

**Contents:**
- Overview
- Prerequisites
- Setting Up Salesforce Integration
  - 1. Connect Your Salesforce Account
  - 2. Install Required Package
  - 3. Environment Variable Setup
- Available Tools
  - **Record Management**
  - **Record Updates**
  - **Record Retrieval**

Source: https://docs.crewai.com/en/enterprise/integrations/salesforce

CRM and sales automation with Salesforce integration for CrewAI.

Enable your agents to manage customer relationships, sales processes, and data through Salesforce. Create and update records, manage leads and opportunities, execute SOQL queries, and streamline your CRM workflows with AI-powered automation.

Before using the Salesforce integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A Salesforce account with appropriate permissions
* Connected your Salesforce account through the [Integrations page](https://app.crewai.com/integrations)

## Setting Up Salesforce Integration

### 1. Connect Your Salesforce Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Salesforce** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for CRM and sales management
5. Copy your Enterprise Token from [Integration Settings](https://app.crewai.com/crewai_plus/settings/integrations)

### 2. Install Required Package

### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>

Or add it to your `.env` file:

### **Record Management**

<AccordionGroup>
  <Accordion title="salesforce/create_record_contact">
    **Description:** Create a new Contact record in Salesforce.

* `FirstName` (string, optional): First Name
    * `LastName` (string, required): Last Name - This field is required
    * `accountId` (string, optional): Account ID - The Account that the Contact belongs to
    * `Email` (string, optional): Email address
    * `Title` (string, optional): Title of the contact, such as CEO or Vice President
    * `Description` (string, optional): A description of the Contact
    * `additionalFields` (object, optional): Additional fields in JSON format for custom Contact fields
  </Accordion>

<Accordion title="salesforce/create_record_lead">
    **Description:** Create a new Lead record in Salesforce.

* `FirstName` (string, optional): First Name
    * `LastName` (string, required): Last Name - This field is required
    * `Company` (string, required): Company - This field is required
    * `Email` (string, optional): Email address
    * `Phone` (string, optional): Phone number
    * `Website` (string, optional): Website URL
    * `Title` (string, optional): Title of the contact, such as CEO or Vice President
    * `Status` (string, optional): Lead Status - Use Connect Portal Workflow Settings to select Lead Status
    * `Description` (string, optional): A description of the Lead
    * `additionalFields` (object, optional): Additional fields in JSON format for custom Lead fields
  </Accordion>

<Accordion title="salesforce/create_record_opportunity">
    **Description:** Create a new Opportunity record in Salesforce.

* `Name` (string, required): The Opportunity name - This field is required
    * `StageName` (string, optional): Opportunity Stage - Use Connect Portal Workflow Settings to select stage
    * `CloseDate` (string, optional): Close Date in YYYY-MM-DD format - Defaults to 30 days from current date
    * `AccountId` (string, optional): The Account that the Opportunity belongs to
    * `Amount` (string, optional): Estimated total sale amount
    * `Description` (string, optional): A description of the Opportunity
    * `OwnerId` (string, optional): The Salesforce user assigned to work on this Opportunity
    * `NextStep` (string, optional): Description of next task in closing Opportunity
    * `additionalFields` (object, optional): Additional fields in JSON format for custom Opportunity fields
  </Accordion>

<Accordion title="salesforce/create_record_task">
    **Description:** Create a new Task record in Salesforce.

* `whatId` (string, optional): Related to ID - The ID of the Account or Opportunity this Task is related to
    * `whoId` (string, optional): Name ID - The ID of the Contact or Lead this Task is related to
    * `subject` (string, required): Subject of the task
    * `activityDate` (string, optional): Activity Date in YYYY-MM-DD format
    * `description` (string, optional): A description of the Task
    * `taskSubtype` (string, required): Task Subtype - Options: task, email, listEmail, call
    * `Status` (string, optional): Status - Options: Not Started, In Progress, Completed
    * `ownerId` (string, optional): Assigned To ID - The Salesforce user assigned to this Task
    * `callDurationInSeconds` (string, optional): Call Duration in seconds
    * `isReminderSet` (boolean, optional): Whether reminder is set
    * `reminderDateTime` (string, optional): Reminder Date/Time in ISO format
    * `additionalFields` (object, optional): Additional fields in JSON format for custom Task fields
  </Accordion>

<Accordion title="salesforce/create_record_account">
    **Description:** Create a new Account record in Salesforce.

* `Name` (string, required): The Account name - This field is required
    * `OwnerId` (string, optional): The Salesforce user assigned to this Account
    * `Website` (string, optional): Website URL
    * `Phone` (string, optional): Phone number
    * `Description` (string, optional): Account description
    * `additionalFields` (object, optional): Additional fields in JSON format for custom Account fields
  </Accordion>

<Accordion title="salesforce/create_record_any">
    **Description:** Create a record of any object type in Salesforce.

**Note:** This is a flexible tool for creating records of custom or unknown object types.
  </Accordion>
</AccordionGroup>

### **Record Updates**

<AccordionGroup>
  <Accordion title="salesforce/update_record_contact">
    **Description:** Update an existing Contact record in Salesforce.

* `recordId` (string, required): The ID of the record to update
    * `FirstName` (string, optional): First Name
    * `LastName` (string, optional): Last Name
    * `accountId` (string, optional): Account ID - The Account that the Contact belongs to
    * `Email` (string, optional): Email address
    * `Title` (string, optional): Title of the contact
    * `Description` (string, optional): A description of the Contact
    * `additionalFields` (object, optional): Additional fields in JSON format for custom Contact fields
  </Accordion>

<Accordion title="salesforce/update_record_lead">
    **Description:** Update an existing Lead record in Salesforce.

* `recordId` (string, required): The ID of the record to update
    * `FirstName` (string, optional): First Name
    * `LastName` (string, optional): Last Name
    * `Company` (string, optional): Company name
    * `Email` (string, optional): Email address
    * `Phone` (string, optional): Phone number
    * `Website` (string, optional): Website URL
    * `Title` (string, optional): Title of the contact
    * `Status` (string, optional): Lead Status
    * `Description` (string, optional): A description of the Lead
    * `additionalFields` (object, optional): Additional fields in JSON format for custom Lead fields
  </Accordion>

<Accordion title="salesforce/update_record_opportunity">
    **Description:** Update an existing Opportunity record in Salesforce.

* `recordId` (string, required): The ID of the record to update
    * `Name` (string, optional): The Opportunity name
    * `StageName` (string, optional): Opportunity Stage
    * `CloseDate` (string, optional): Close Date in YYYY-MM-DD format
    * `AccountId` (string, optional): The Account that the Opportunity belongs to
    * `Amount` (string, optional): Estimated total sale amount
    * `Description` (string, optional): A description of the Opportunity
    * `OwnerId` (string, optional): The Salesforce user assigned to work on this Opportunity
    * `NextStep` (string, optional): Description of next task in closing Opportunity
    * `additionalFields` (object, optional): Additional fields in JSON format for custom Opportunity fields
  </Accordion>

<Accordion title="salesforce/update_record_task">
    **Description:** Update an existing Task record in Salesforce.

* `recordId` (string, required): The ID of the record to update
    * `whatId` (string, optional): Related to ID - The ID of the Account or Opportunity this Task is related to
    * `whoId` (string, optional): Name ID - The ID of the Contact or Lead this Task is related to
    * `subject` (string, optional): Subject of the task
    * `activityDate` (string, optional): Activity Date in YYYY-MM-DD format
    * `description` (string, optional): A description of the Task
    * `Status` (string, optional): Status - Options: Not Started, In Progress, Completed
    * `ownerId` (string, optional): Assigned To ID - The Salesforce user assigned to this Task
    * `callDurationInSeconds` (string, optional): Call Duration in seconds
    * `isReminderSet` (boolean, optional): Whether reminder is set
    * `reminderDateTime` (string, optional): Reminder Date/Time in ISO format
    * `additionalFields` (object, optional): Additional fields in JSON format for custom Task fields
  </Accordion>

<Accordion title="salesforce/update_record_account">
    **Description:** Update an existing Account record in Salesforce.

* `recordId` (string, required): The ID of the record to update
    * `Name` (string, optional): The Account name
    * `OwnerId` (string, optional): The Salesforce user assigned to this Account
    * `Website` (string, optional): Website URL
    * `Phone` (string, optional): Phone number
    * `Description` (string, optional): Account description
    * `additionalFields` (object, optional): Additional fields in JSON format for custom Account fields
  </Accordion>

<Accordion title="salesforce/update_record_any">
    **Description:** Update a record of any object type in Salesforce.

**Note:** This is a flexible tool for updating records of custom or unknown object types.
  </Accordion>
</AccordionGroup>

### **Record Retrieval**

<AccordionGroup>
  <Accordion title="salesforce/get_record_by_id_contact">
    **Description:** Get a Contact record by its ID.

* `recordId` (string, required): Record ID of the Contact
  </Accordion>

<Accordion title="salesforce/get_record_by_id_lead">
    **Description:** Get a Lead record by its ID.

* `recordId` (string, required): Record ID of the Lead
  </Accordion>

<Accordion title="salesforce/get_record_by_id_opportunity">
    **Description:** Get an Opportunity record by its ID.

* `recordId` (string, required): Record ID of the Opportunity
  </Accordion>

<Accordion title="salesforce/get_record_by_id_task">
    **Description:** Get a Task record by its ID.

* `recordId` (string, required): Record ID of the Task
  </Accordion>

<Accordion title="salesforce/get_record_by_id_account">
    **Description:** Get an Account record by its ID.

* `recordId` (string, required): Record ID of the Account
  </Accordion>

<Accordion title="salesforce/get_record_by_id_any">
    **Description:** Get a record of any object type by its ID.

* `recordType` (string, required): Record Type (e.g., "CustomObject\_\_c")
    * `recordId` (string, required): Record ID
  </Accordion>
</AccordionGroup>

### **Record Search**

<AccordionGroup>
  <Accordion title="salesforce/search_records_contact">
    **Description:** Search for Contact records with advanced filtering.

* `filterFormula` (object, optional): Advanced filter in disjunctive normal form with field-specific operators
    * `sortBy` (string, optional): Sort field (e.g., "CreatedDate")
    * `sortDirection` (string, optional): Sort direction - Options: ASC, DESC
    * `includeAllFields` (boolean, optional): Include all fields in results
    * `paginationParameters` (object, optional): Pagination settings with pageCursor
  </Accordion>

<Accordion title="salesforce/search_records_lead">
    **Description:** Search for Lead records with advanced filtering.

* `filterFormula` (object, optional): Advanced filter in disjunctive normal form with field-specific operators
    * `sortBy` (string, optional): Sort field (e.g., "CreatedDate")
    * `sortDirection` (string, optional): Sort direction - Options: ASC, DESC
    * `includeAllFields` (boolean, optional): Include all fields in results
    * `paginationParameters` (object, optional): Pagination settings with pageCursor
  </Accordion>

<Accordion title="salesforce/search_records_opportunity">
    **Description:** Search for Opportunity records with advanced filtering.

* `filterFormula` (object, optional): Advanced filter in disjunctive normal form with field-specific operators
    * `sortBy` (string, optional): Sort field (e.g., "CreatedDate")
    * `sortDirection` (string, optional): Sort direction - Options: ASC, DESC
    * `includeAllFields` (boolean, optional): Include all fields in results
    * `paginationParameters` (object, optional): Pagination settings with pageCursor
  </Accordion>

<Accordion title="salesforce/search_records_task">
    **Description:** Search for Task records with advanced filtering.

* `filterFormula` (object, optional): Advanced filter in disjunctive normal form with field-specific operators
    * `sortBy` (string, optional): Sort field (e.g., "CreatedDate")
    * `sortDirection` (string, optional): Sort direction - Options: ASC, DESC
    * `includeAllFields` (boolean, optional): Include all fields in results
    * `paginationParameters` (object, optional): Pagination settings with pageCursor
  </Accordion>

<Accordion title="salesforce/search_records_account">
    **Description:** Search for Account records with advanced filtering.

* `filterFormula` (object, optional): Advanced filter in disjunctive normal form with field-specific operators
    * `sortBy` (string, optional): Sort field (e.g., "CreatedDate")
    * `sortDirection` (string, optional): Sort direction - Options: ASC, DESC
    * `includeAllFields` (boolean, optional): Include all fields in results
    * `paginationParameters` (object, optional): Pagination settings with pageCursor
  </Accordion>

<Accordion title="salesforce/search_records_any">
    **Description:** Search for records of any object type.

* `recordType` (string, required): Record Type to search
    * `filterFormula` (string, optional): Filter search criteria
    * `includeAllFields` (boolean, optional): Include all fields in results
    * `paginationParameters` (object, optional): Pagination settings with pageCursor
  </Accordion>
</AccordionGroup>

### **List View Retrieval**

<AccordionGroup>
  <Accordion title="salesforce/get_record_by_view_id_contact">
    **Description:** Get Contact records from a specific List View.

* `listViewId` (string, required): List View ID
    * `paginationParameters` (object, optional): Pagination settings with pageCursor
  </Accordion>

<Accordion title="salesforce/get_record_by_view_id_lead">
    **Description:** Get Lead records from a specific List View.

* `listViewId` (string, required): List View ID
    * `paginationParameters` (object, optional): Pagination settings with pageCursor
  </Accordion>

<Accordion title="salesforce/get_record_by_view_id_opportunity">
    **Description:** Get Opportunity records from a specific List View.

* `listViewId` (string, required): List View ID
    * `paginationParameters` (object, optional): Pagination settings with pageCursor
  </Accordion>

<Accordion title="salesforce/get_record_by_view_id_task">
    **Description:** Get Task records from a specific List View.

* `listViewId` (string, required): List View ID
    * `paginationParameters` (object, optional): Pagination settings with pageCursor
  </Accordion>

<Accordion title="salesforce/get_record_by_view_id_account">
    **Description:** Get Account records from a specific List View.

* `listViewId` (string, required): List View ID
    * `paginationParameters` (object, optional): Pagination settings with pageCursor
  </Accordion>

<Accordion title="salesforce/get_record_by_view_id_any">
    **Description:** Get records of any object type from a specific List View.

* `recordType` (string, required): Record Type
    * `listViewId` (string, required): List View ID
    * `paginationParameters` (object, optional): Pagination settings with pageCursor
  </Accordion>
</AccordionGroup>

### **Custom Fields**

<AccordionGroup>
  <Accordion title="salesforce/create_custom_field_contact">
    **Description:** Deploy custom fields for Contact objects.

* `label` (string, required): Field Label for displays and internal reference
    * `type` (string, required): Field Type - Options: Checkbox, Currency, Date, Email, Number, Percent, Phone, Picklist, MultiselectPicklist, Text, TextArea, LongTextArea, Html, Time, Url
    * `defaultCheckboxValue` (boolean, optional): Default value for checkbox fields
    * `length` (string, required): Length for numeric/text fields
    * `decimalPlace` (string, required): Decimal places for numeric fields
    * `pickListValues` (string, required): Values for picklist fields (separated by new lines)
    * `visibleLines` (string, required): Visible lines for multiselect/text area fields
    * `description` (string, optional): Field description
    * `helperText` (string, optional): Helper text shown on hover
    * `defaultFieldValue` (string, optional): Default field value
  </Accordion>

<Accordion title="salesforce/create_custom_field_lead">
    **Description:** Deploy custom fields for Lead objects.

* `label` (string, required): Field Label for displays and internal reference
    * `type` (string, required): Field Type - Options: Checkbox, Currency, Date, Email, Number, Percent, Phone, Picklist, MultiselectPicklist, Text, TextArea, LongTextArea, Html, Time, Url
    * `defaultCheckboxValue` (boolean, optional): Default value for checkbox fields
    * `length` (string, required): Length for numeric/text fields
    * `decimalPlace` (string, required): Decimal places for numeric fields
    * `pickListValues` (string, required): Values for picklist fields (separated by new lines)
    * `visibleLines` (string, required): Visible lines for multiselect/text area fields
    * `description` (string, optional): Field description
    * `helperText` (string, optional): Helper text shown on hover
    * `defaultFieldValue` (string, optional): Default field value
  </Accordion>

<Accordion title="salesforce/create_custom_field_opportunity">
    **Description:** Deploy custom fields for Opportunity objects.

* `label` (string, required): Field Label for displays and internal reference
    * `type` (string, required): Field Type - Options: Checkbox, Currency, Date, Email, Number, Percent, Phone, Picklist, MultiselectPicklist, Text, TextArea, LongTextArea, Html, Time, Url
    * `defaultCheckboxValue` (boolean, optional): Default value for checkbox fields
    * `length` (string, required): Length for numeric/text fields
    * `decimalPlace` (string, required): Decimal places for numeric fields
    * `pickListValues` (string, required): Values for picklist fields (separated by new lines)
    * `visibleLines` (string, required): Visible lines for multiselect/text area fields
    * `description` (string, optional): Field description
    * `helperText` (string, optional): Helper text shown on hover
    * `defaultFieldValue` (string, optional): Default field value
  </Accordion>

<Accordion title="salesforce/create_custom_field_task">
    **Description:** Deploy custom fields for Task objects.

* `label` (string, required): Field Label for displays and internal reference
    * `type` (string, required): Field Type - Options: Checkbox, Currency, Date, Email, Number, Percent, Phone, Picklist, MultiselectPicklist, Text, TextArea, Time, Url
    * `defaultCheckboxValue` (boolean, optional): Default value for checkbox fields
    * `length` (string, required): Length for numeric/text fields
    * `decimalPlace` (string, required): Decimal places for numeric fields
    * `pickListValues` (string, required): Values for picklist fields (separated by new lines)
    * `visibleLines` (string, required): Visible lines for multiselect fields
    * `description` (string, optional): Field description
    * `helperText` (string, optional): Helper text shown on hover
    * `defaultFieldValue` (string, optional): Default field value
  </Accordion>

<Accordion title="salesforce/create_custom_field_account">
    **Description:** Deploy custom fields for Account objects.

* `label` (string, required): Field Label for displays and internal reference
    * `type` (string, required): Field Type - Options: Checkbox, Currency, Date, Email, Number, Percent, Phone, Picklist, MultiselectPicklist, Text, TextArea, LongTextArea, Html, Time, Url
    * `defaultCheckboxValue` (boolean, optional): Default value for checkbox fields
    * `length` (string, required): Length for numeric/text fields
    * `decimalPlace` (string, required): Decimal places for numeric fields
    * `pickListValues` (string, required): Values for picklist fields (separated by new lines)
    * `visibleLines` (string, required): Visible lines for multiselect/text area fields
    * `description` (string, optional): Field description
    * `helperText` (string, optional): Helper text shown on hover
    * `defaultFieldValue` (string, optional): Default field value
  </Accordion>

<Accordion title="salesforce/create_custom_field_any">
    **Description:** Deploy custom fields for any object type.

**Note:** This is a flexible tool for creating custom fields on custom or unknown object types.
  </Accordion>
</AccordionGroup>

### **Advanced Operations**

<AccordionGroup>
  <Accordion title="salesforce/write_soql_query">
    **Description:** Execute custom SOQL queries against your Salesforce data.

* `query` (string, required): SOQL Query (e.g., "SELECT Id, Name FROM Account WHERE Name = 'Example'")
  </Accordion>

<Accordion title="salesforce/create_custom_object">
    **Description:** Deploy a new custom object in Salesforce.

* `label` (string, required): Object Label for tabs, page layouts, and reports
    * `pluralLabel` (string, required): Plural Label (e.g., "Accounts")
    * `description` (string, optional): A description of the Custom Object
    * `recordName` (string, required): Record Name that appears in layouts and searches (e.g., "Account Name")
  </Accordion>

<Accordion title="salesforce/describe_action_schema">
    **Description:** Get the expected schema for operations on specific object types.

* `recordType` (string, required): Record Type to describe
    * `operation` (string, required): Operation Type (e.g., "CREATE\_RECORD" or "UPDATE\_RECORD")

**Note:** Use this function first when working with custom objects to understand their schema before performing operations.
  </Accordion>
</AccordionGroup>

### Basic Salesforce Agent Setup

```python theme={null}
from crewai import Agent, Task, Crew
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

Example 3 (unknown):
```unknown
## Available Tools

### **Record Management**

<AccordionGroup>
  <Accordion title="salesforce/create_record_contact">
    **Description:** Create a new Contact record in Salesforce.

    **Parameters:**

    * `FirstName` (string, optional): First Name
    * `LastName` (string, required): Last Name - This field is required
    * `accountId` (string, optional): Account ID - The Account that the Contact belongs to
    * `Email` (string, optional): Email address
    * `Title` (string, optional): Title of the contact, such as CEO or Vice President
    * `Description` (string, optional): A description of the Contact
    * `additionalFields` (object, optional): Additional fields in JSON format for custom Contact fields
  </Accordion>

  <Accordion title="salesforce/create_record_lead">
    **Description:** Create a new Lead record in Salesforce.

    **Parameters:**

    * `FirstName` (string, optional): First Name
    * `LastName` (string, required): Last Name - This field is required
    * `Company` (string, required): Company - This field is required
    * `Email` (string, optional): Email address
    * `Phone` (string, optional): Phone number
    * `Website` (string, optional): Website URL
    * `Title` (string, optional): Title of the contact, such as CEO or Vice President
    * `Status` (string, optional): Lead Status - Use Connect Portal Workflow Settings to select Lead Status
    * `Description` (string, optional): A description of the Lead
    * `additionalFields` (object, optional): Additional fields in JSON format for custom Lead fields
  </Accordion>

  <Accordion title="salesforce/create_record_opportunity">
    **Description:** Create a new Opportunity record in Salesforce.

    **Parameters:**

    * `Name` (string, required): The Opportunity name - This field is required
    * `StageName` (string, optional): Opportunity Stage - Use Connect Portal Workflow Settings to select stage
    * `CloseDate` (string, optional): Close Date in YYYY-MM-DD format - Defaults to 30 days from current date
    * `AccountId` (string, optional): The Account that the Opportunity belongs to
    * `Amount` (string, optional): Estimated total sale amount
    * `Description` (string, optional): A description of the Opportunity
    * `OwnerId` (string, optional): The Salesforce user assigned to work on this Opportunity
    * `NextStep` (string, optional): Description of next task in closing Opportunity
    * `additionalFields` (object, optional): Additional fields in JSON format for custom Opportunity fields
  </Accordion>

  <Accordion title="salesforce/create_record_task">
    **Description:** Create a new Task record in Salesforce.

    **Parameters:**

    * `whatId` (string, optional): Related to ID - The ID of the Account or Opportunity this Task is related to
    * `whoId` (string, optional): Name ID - The ID of the Contact or Lead this Task is related to
    * `subject` (string, required): Subject of the task
    * `activityDate` (string, optional): Activity Date in YYYY-MM-DD format
    * `description` (string, optional): A description of the Task
    * `taskSubtype` (string, required): Task Subtype - Options: task, email, listEmail, call
    * `Status` (string, optional): Status - Options: Not Started, In Progress, Completed
    * `ownerId` (string, optional): Assigned To ID - The Salesforce user assigned to this Task
    * `callDurationInSeconds` (string, optional): Call Duration in seconds
    * `isReminderSet` (boolean, optional): Whether reminder is set
    * `reminderDateTime` (string, optional): Reminder Date/Time in ISO format
    * `additionalFields` (object, optional): Additional fields in JSON format for custom Task fields
  </Accordion>

  <Accordion title="salesforce/create_record_account">
    **Description:** Create a new Account record in Salesforce.

    **Parameters:**

    * `Name` (string, required): The Account name - This field is required
    * `OwnerId` (string, optional): The Salesforce user assigned to this Account
    * `Website` (string, optional): Website URL
    * `Phone` (string, optional): Phone number
    * `Description` (string, optional): Account description
    * `additionalFields` (object, optional): Additional fields in JSON format for custom Account fields
  </Accordion>

  <Accordion title="salesforce/create_record_any">
    **Description:** Create a record of any object type in Salesforce.

    **Note:** This is a flexible tool for creating records of custom or unknown object types.
  </Accordion>
</AccordionGroup>

### **Record Updates**

<AccordionGroup>
  <Accordion title="salesforce/update_record_contact">
    **Description:** Update an existing Contact record in Salesforce.

    **Parameters:**

    * `recordId` (string, required): The ID of the record to update
    * `FirstName` (string, optional): First Name
    * `LastName` (string, optional): Last Name
    * `accountId` (string, optional): Account ID - The Account that the Contact belongs to
    * `Email` (string, optional): Email address
    * `Title` (string, optional): Title of the contact
    * `Description` (string, optional): A description of the Contact
    * `additionalFields` (object, optional): Additional fields in JSON format for custom Contact fields
  </Accordion>

  <Accordion title="salesforce/update_record_lead">
    **Description:** Update an existing Lead record in Salesforce.

    **Parameters:**

    * `recordId` (string, required): The ID of the record to update
    * `FirstName` (string, optional): First Name
    * `LastName` (string, optional): Last Name
    * `Company` (string, optional): Company name
    * `Email` (string, optional): Email address
    * `Phone` (string, optional): Phone number
    * `Website` (string, optional): Website URL
    * `Title` (string, optional): Title of the contact
    * `Status` (string, optional): Lead Status
    * `Description` (string, optional): A description of the Lead
    * `additionalFields` (object, optional): Additional fields in JSON format for custom Lead fields
  </Accordion>

  <Accordion title="salesforce/update_record_opportunity">
    **Description:** Update an existing Opportunity record in Salesforce.

    **Parameters:**

    * `recordId` (string, required): The ID of the record to update
    * `Name` (string, optional): The Opportunity name
    * `StageName` (string, optional): Opportunity Stage
    * `CloseDate` (string, optional): Close Date in YYYY-MM-DD format
    * `AccountId` (string, optional): The Account that the Opportunity belongs to
    * `Amount` (string, optional): Estimated total sale amount
    * `Description` (string, optional): A description of the Opportunity
    * `OwnerId` (string, optional): The Salesforce user assigned to work on this Opportunity
    * `NextStep` (string, optional): Description of next task in closing Opportunity
    * `additionalFields` (object, optional): Additional fields in JSON format for custom Opportunity fields
  </Accordion>

  <Accordion title="salesforce/update_record_task">
    **Description:** Update an existing Task record in Salesforce.

    **Parameters:**

    * `recordId` (string, required): The ID of the record to update
    * `whatId` (string, optional): Related to ID - The ID of the Account or Opportunity this Task is related to
    * `whoId` (string, optional): Name ID - The ID of the Contact or Lead this Task is related to
    * `subject` (string, optional): Subject of the task
    * `activityDate` (string, optional): Activity Date in YYYY-MM-DD format
    * `description` (string, optional): A description of the Task
    * `Status` (string, optional): Status - Options: Not Started, In Progress, Completed
    * `ownerId` (string, optional): Assigned To ID - The Salesforce user assigned to this Task
    * `callDurationInSeconds` (string, optional): Call Duration in seconds
    * `isReminderSet` (boolean, optional): Whether reminder is set
    * `reminderDateTime` (string, optional): Reminder Date/Time in ISO format
    * `additionalFields` (object, optional): Additional fields in JSON format for custom Task fields
  </Accordion>

  <Accordion title="salesforce/update_record_account">
    **Description:** Update an existing Account record in Salesforce.

    **Parameters:**

    * `recordId` (string, required): The ID of the record to update
    * `Name` (string, optional): The Account name
    * `OwnerId` (string, optional): The Salesforce user assigned to this Account
    * `Website` (string, optional): Website URL
    * `Phone` (string, optional): Phone number
    * `Description` (string, optional): Account description
    * `additionalFields` (object, optional): Additional fields in JSON format for custom Account fields
  </Accordion>

  <Accordion title="salesforce/update_record_any">
    **Description:** Update a record of any object type in Salesforce.

    **Note:** This is a flexible tool for updating records of custom or unknown object types.
  </Accordion>
</AccordionGroup>

### **Record Retrieval**

<AccordionGroup>
  <Accordion title="salesforce/get_record_by_id_contact">
    **Description:** Get a Contact record by its ID.

    **Parameters:**

    * `recordId` (string, required): Record ID of the Contact
  </Accordion>

  <Accordion title="salesforce/get_record_by_id_lead">
    **Description:** Get a Lead record by its ID.

    **Parameters:**

    * `recordId` (string, required): Record ID of the Lead
  </Accordion>

  <Accordion title="salesforce/get_record_by_id_opportunity">
    **Description:** Get an Opportunity record by its ID.

    **Parameters:**

    * `recordId` (string, required): Record ID of the Opportunity
  </Accordion>

  <Accordion title="salesforce/get_record_by_id_task">
    **Description:** Get a Task record by its ID.

    **Parameters:**

    * `recordId` (string, required): Record ID of the Task
  </Accordion>

  <Accordion title="salesforce/get_record_by_id_account">
    **Description:** Get an Account record by its ID.

    **Parameters:**

    * `recordId` (string, required): Record ID of the Account
  </Accordion>

  <Accordion title="salesforce/get_record_by_id_any">
    **Description:** Get a record of any object type by its ID.

    **Parameters:**

    * `recordType` (string, required): Record Type (e.g., "CustomObject\_\_c")
    * `recordId` (string, required): Record ID
  </Accordion>
</AccordionGroup>

### **Record Search**

<AccordionGroup>
  <Accordion title="salesforce/search_records_contact">
    **Description:** Search for Contact records with advanced filtering.

    **Parameters:**

    * `filterFormula` (object, optional): Advanced filter in disjunctive normal form with field-specific operators
    * `sortBy` (string, optional): Sort field (e.g., "CreatedDate")
    * `sortDirection` (string, optional): Sort direction - Options: ASC, DESC
    * `includeAllFields` (boolean, optional): Include all fields in results
    * `paginationParameters` (object, optional): Pagination settings with pageCursor
  </Accordion>

  <Accordion title="salesforce/search_records_lead">
    **Description:** Search for Lead records with advanced filtering.

    **Parameters:**

    * `filterFormula` (object, optional): Advanced filter in disjunctive normal form with field-specific operators
    * `sortBy` (string, optional): Sort field (e.g., "CreatedDate")
    * `sortDirection` (string, optional): Sort direction - Options: ASC, DESC
    * `includeAllFields` (boolean, optional): Include all fields in results
    * `paginationParameters` (object, optional): Pagination settings with pageCursor
  </Accordion>

  <Accordion title="salesforce/search_records_opportunity">
    **Description:** Search for Opportunity records with advanced filtering.

    **Parameters:**

    * `filterFormula` (object, optional): Advanced filter in disjunctive normal form with field-specific operators
    * `sortBy` (string, optional): Sort field (e.g., "CreatedDate")
    * `sortDirection` (string, optional): Sort direction - Options: ASC, DESC
    * `includeAllFields` (boolean, optional): Include all fields in results
    * `paginationParameters` (object, optional): Pagination settings with pageCursor
  </Accordion>

  <Accordion title="salesforce/search_records_task">
    **Description:** Search for Task records with advanced filtering.

    **Parameters:**

    * `filterFormula` (object, optional): Advanced filter in disjunctive normal form with field-specific operators
    * `sortBy` (string, optional): Sort field (e.g., "CreatedDate")
    * `sortDirection` (string, optional): Sort direction - Options: ASC, DESC
    * `includeAllFields` (boolean, optional): Include all fields in results
    * `paginationParameters` (object, optional): Pagination settings with pageCursor
  </Accordion>

  <Accordion title="salesforce/search_records_account">
    **Description:** Search for Account records with advanced filtering.

    **Parameters:**

    * `filterFormula` (object, optional): Advanced filter in disjunctive normal form with field-specific operators
    * `sortBy` (string, optional): Sort field (e.g., "CreatedDate")
    * `sortDirection` (string, optional): Sort direction - Options: ASC, DESC
    * `includeAllFields` (boolean, optional): Include all fields in results
    * `paginationParameters` (object, optional): Pagination settings with pageCursor
  </Accordion>

  <Accordion title="salesforce/search_records_any">
    **Description:** Search for records of any object type.

    **Parameters:**

    * `recordType` (string, required): Record Type to search
    * `filterFormula` (string, optional): Filter search criteria
    * `includeAllFields` (boolean, optional): Include all fields in results
    * `paginationParameters` (object, optional): Pagination settings with pageCursor
  </Accordion>
</AccordionGroup>

### **List View Retrieval**

<AccordionGroup>
  <Accordion title="salesforce/get_record_by_view_id_contact">
    **Description:** Get Contact records from a specific List View.

    **Parameters:**

    * `listViewId` (string, required): List View ID
    * `paginationParameters` (object, optional): Pagination settings with pageCursor
  </Accordion>

  <Accordion title="salesforce/get_record_by_view_id_lead">
    **Description:** Get Lead records from a specific List View.

    **Parameters:**

    * `listViewId` (string, required): List View ID
    * `paginationParameters` (object, optional): Pagination settings with pageCursor
  </Accordion>

  <Accordion title="salesforce/get_record_by_view_id_opportunity">
    **Description:** Get Opportunity records from a specific List View.

    **Parameters:**

    * `listViewId` (string, required): List View ID
    * `paginationParameters` (object, optional): Pagination settings with pageCursor
  </Accordion>

  <Accordion title="salesforce/get_record_by_view_id_task">
    **Description:** Get Task records from a specific List View.

    **Parameters:**

    * `listViewId` (string, required): List View ID
    * `paginationParameters` (object, optional): Pagination settings with pageCursor
  </Accordion>

  <Accordion title="salesforce/get_record_by_view_id_account">
    **Description:** Get Account records from a specific List View.

    **Parameters:**

    * `listViewId` (string, required): List View ID
    * `paginationParameters` (object, optional): Pagination settings with pageCursor
  </Accordion>

  <Accordion title="salesforce/get_record_by_view_id_any">
    **Description:** Get records of any object type from a specific List View.

    **Parameters:**

    * `recordType` (string, required): Record Type
    * `listViewId` (string, required): List View ID
    * `paginationParameters` (object, optional): Pagination settings with pageCursor
  </Accordion>
</AccordionGroup>

### **Custom Fields**

<AccordionGroup>
  <Accordion title="salesforce/create_custom_field_contact">
    **Description:** Deploy custom fields for Contact objects.

    **Parameters:**

    * `label` (string, required): Field Label for displays and internal reference
    * `type` (string, required): Field Type - Options: Checkbox, Currency, Date, Email, Number, Percent, Phone, Picklist, MultiselectPicklist, Text, TextArea, LongTextArea, Html, Time, Url
    * `defaultCheckboxValue` (boolean, optional): Default value for checkbox fields
    * `length` (string, required): Length for numeric/text fields
    * `decimalPlace` (string, required): Decimal places for numeric fields
    * `pickListValues` (string, required): Values for picklist fields (separated by new lines)
    * `visibleLines` (string, required): Visible lines for multiselect/text area fields
    * `description` (string, optional): Field description
    * `helperText` (string, optional): Helper text shown on hover
    * `defaultFieldValue` (string, optional): Default field value
  </Accordion>

  <Accordion title="salesforce/create_custom_field_lead">
    **Description:** Deploy custom fields for Lead objects.

    **Parameters:**

    * `label` (string, required): Field Label for displays and internal reference
    * `type` (string, required): Field Type - Options: Checkbox, Currency, Date, Email, Number, Percent, Phone, Picklist, MultiselectPicklist, Text, TextArea, LongTextArea, Html, Time, Url
    * `defaultCheckboxValue` (boolean, optional): Default value for checkbox fields
    * `length` (string, required): Length for numeric/text fields
    * `decimalPlace` (string, required): Decimal places for numeric fields
    * `pickListValues` (string, required): Values for picklist fields (separated by new lines)
    * `visibleLines` (string, required): Visible lines for multiselect/text area fields
    * `description` (string, optional): Field description
    * `helperText` (string, optional): Helper text shown on hover
    * `defaultFieldValue` (string, optional): Default field value
  </Accordion>

  <Accordion title="salesforce/create_custom_field_opportunity">
    **Description:** Deploy custom fields for Opportunity objects.

    **Parameters:**

    * `label` (string, required): Field Label for displays and internal reference
    * `type` (string, required): Field Type - Options: Checkbox, Currency, Date, Email, Number, Percent, Phone, Picklist, MultiselectPicklist, Text, TextArea, LongTextArea, Html, Time, Url
    * `defaultCheckboxValue` (boolean, optional): Default value for checkbox fields
    * `length` (string, required): Length for numeric/text fields
    * `decimalPlace` (string, required): Decimal places for numeric fields
    * `pickListValues` (string, required): Values for picklist fields (separated by new lines)
    * `visibleLines` (string, required): Visible lines for multiselect/text area fields
    * `description` (string, optional): Field description
    * `helperText` (string, optional): Helper text shown on hover
    * `defaultFieldValue` (string, optional): Default field value
  </Accordion>

  <Accordion title="salesforce/create_custom_field_task">
    **Description:** Deploy custom fields for Task objects.

    **Parameters:**

    * `label` (string, required): Field Label for displays and internal reference
    * `type` (string, required): Field Type - Options: Checkbox, Currency, Date, Email, Number, Percent, Phone, Picklist, MultiselectPicklist, Text, TextArea, Time, Url
    * `defaultCheckboxValue` (boolean, optional): Default value for checkbox fields
    * `length` (string, required): Length for numeric/text fields
    * `decimalPlace` (string, required): Decimal places for numeric fields
    * `pickListValues` (string, required): Values for picklist fields (separated by new lines)
    * `visibleLines` (string, required): Visible lines for multiselect fields
    * `description` (string, optional): Field description
    * `helperText` (string, optional): Helper text shown on hover
    * `defaultFieldValue` (string, optional): Default field value
  </Accordion>

  <Accordion title="salesforce/create_custom_field_account">
    **Description:** Deploy custom fields for Account objects.

    **Parameters:**

    * `label` (string, required): Field Label for displays and internal reference
    * `type` (string, required): Field Type - Options: Checkbox, Currency, Date, Email, Number, Percent, Phone, Picklist, MultiselectPicklist, Text, TextArea, LongTextArea, Html, Time, Url
    * `defaultCheckboxValue` (boolean, optional): Default value for checkbox fields
    * `length` (string, required): Length for numeric/text fields
    * `decimalPlace` (string, required): Decimal places for numeric fields
    * `pickListValues` (string, required): Values for picklist fields (separated by new lines)
    * `visibleLines` (string, required): Visible lines for multiselect/text area fields
    * `description` (string, optional): Field description
    * `helperText` (string, optional): Helper text shown on hover
    * `defaultFieldValue` (string, optional): Default field value
  </Accordion>

  <Accordion title="salesforce/create_custom_field_any">
    **Description:** Deploy custom fields for any object type.

    **Note:** This is a flexible tool for creating custom fields on custom or unknown object types.
  </Accordion>
</AccordionGroup>

### **Advanced Operations**

<AccordionGroup>
  <Accordion title="salesforce/write_soql_query">
    **Description:** Execute custom SOQL queries against your Salesforce data.

    **Parameters:**

    * `query` (string, required): SOQL Query (e.g., "SELECT Id, Name FROM Account WHERE Name = 'Example'")
  </Accordion>

  <Accordion title="salesforce/create_custom_object">
    **Description:** Deploy a new custom object in Salesforce.

    **Parameters:**

    * `label` (string, required): Object Label for tabs, page layouts, and reports
    * `pluralLabel` (string, required): Plural Label (e.g., "Accounts")
    * `description` (string, optional): A description of the Custom Object
    * `recordName` (string, required): Record Name that appears in layouts and searches (e.g., "Account Name")
  </Accordion>

  <Accordion title="salesforce/describe_action_schema">
    **Description:** Get the expected schema for operations on specific object types.

    **Parameters:**

    * `recordType` (string, required): Record Type to describe
    * `operation` (string, required): Operation Type (e.g., "CREATE\_RECORD" or "UPDATE\_RECORD")

    **Note:** Use this function first when working with custom objects to understand their schema before performing operations.
  </Accordion>
</AccordionGroup>

## Usage Examples

### Basic Salesforce Agent Setup
```

---

## `ScrapeElementFromWebsiteTool`

**URL:** llms-txt#`scrapeelementfromwebsitetool`

**Contents:**
- Description
- Installation
- Steps to Get Started
- Example

The `ScrapeElementFromWebsiteTool` is designed to extract specific elements from websites using CSS selectors. This tool allows CrewAI agents to scrape targeted content from web pages, making it useful for data extraction tasks where only specific parts of a webpage are needed.

To use this tool, you need to install the required dependencies:

## Steps to Get Started

To effectively use the `ScrapeElementFromWebsiteTool`, follow these steps:

1. **Install Dependencies**: Install the required packages using the command above.
2. **Identify CSS Selectors**: Determine the CSS selectors for the elements you want to extract from the website.
3. **Initialize the Tool**: Create an instance of the tool with the necessary parameters.

The following example demonstrates how to use the `ScrapeElementFromWebsiteTool` to extract specific elements from a website:

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import ScrapeElementFromWebsiteTool

**Examples:**

Example 1 (unknown):
```unknown
## Steps to Get Started

To effectively use the `ScrapeElementFromWebsiteTool`, follow these steps:

1. **Install Dependencies**: Install the required packages using the command above.
2. **Identify CSS Selectors**: Determine the CSS selectors for the elements you want to extract from the website.
3. **Initialize the Tool**: Create an instance of the tool with the necessary parameters.

## Example

The following example demonstrates how to use the `ScrapeElementFromWebsiteTool` to extract specific elements from a website:
```

---

## Scrape Element From Website Tool

**URL:** llms-txt#scrape-element-from-website-tool

Source: https://docs.crewai.com/en/tools/web-scraping/scrapeelementfromwebsitetool

The `ScrapeElementFromWebsiteTool` enables CrewAI agents to extract specific elements from websites using CSS selectors.

---

## Second agent creation (within 5 minutes) - uses cached tool schemas

**URL:** llms-txt#second-agent-creation-(within-5-minutes)---uses-cached-tool-schemas

**Contents:**
  - On-Demand Connections

agent2 = Agent(role="Second", goal="Test", backstory="Test",
               mcps=["https://api.example.com/mcp"])  # Much faster!
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### On-Demand Connections

Tool connections are established only when tools are actually used:
```

---

## Setting a Specific Agent as Manager in CrewAI

**URL:** llms-txt#setting-a-specific-agent-as-manager-in-crewai

**Contents:**
- Using the `manager_agent` Attribute
  - Custom Manager Agent
  - Example

CrewAI allows users to set a specific agent as the manager of the crew, providing more control over the management and coordination of tasks.
This feature enables the customization of the managerial role to better fit your project's requirements.

## Using the `manager_agent` Attribute

### Custom Manager Agent

The `manager_agent` attribute allows you to define a custom agent to manage the crew. This agent will oversee the entire process, ensuring that tasks are completed efficiently and to the highest standard.

```python Code theme={null}
import os
from crewai import Agent, Task, Crew, Process

---

## Set specific collaboration guidelines in agent backstory

**URL:** llms-txt#set-specific-collaboration-guidelines-in-agent-backstory

**Contents:**
  - Monitoring Collaboration
- Memory and Learning
- Next Steps

agent = Agent(
    role="Senior Developer",
    backstory="""You lead development projects and coordinate with team members.
    
    Collaboration guidelines:
    - Delegate research tasks to the Research Analyst
    - Ask the Designer for UI/UX guidance  
    - Consult the QA Engineer for testing strategies
    - Only escalate blocking issues to the Project Manager""",
    allow_delegation=True
)
python theme={null}
def track_collaboration(output):
    """Track collaboration patterns"""
    if "Delegate work to coworker" in output.raw:
        print("🤝 Delegation occurred")
    if "Ask question to coworker" in output.raw:
        print("❓ Question asked")

crew = Crew(
    agents=[...],
    tasks=[...],
    step_callback=track_collaboration,  # Monitor collaboration
    verbose=True
)
python theme={null}
agent = Agent(
    role="Content Lead",
    memory=True,  # Remembers past interactions
    allow_delegation=True,
    verbose=True
)
```

With memory enabled, agents learn from previous collaborations and improve their delegation decisions over time.

* **Try the examples**: Start with the basic collaboration example
* **Experiment with roles**: Test different agent role combinations
* **Monitor interactions**: Use `verbose=True` to see collaboration in action
* **Optimize task descriptions**: Clear tasks lead to better collaboration
* **Scale up**: Try hierarchical processes for complex projects

Collaboration transforms individual AI agents into powerful teams that can tackle complex, multi-faceted challenges together.

**Examples:**

Example 1 (unknown):
```unknown
### Monitoring Collaboration
```

Example 2 (unknown):
```unknown
## Memory and Learning

Enable agents to remember past collaborations:
```

---

## Shopify Integration

**URL:** llms-txt#shopify-integration

**Contents:**
- Overview
- Prerequisites
- Setting Up Shopify Integration
  - 1. Connect Your Shopify Store
  - 2. Install Required Package
  - 3. Environment Variable Setup
- Available Tools
  - **Customer Management**
  - **Order Management**
  - **Product Management (REST API)**

Source: https://docs.crewai.com/en/enterprise/integrations/shopify

E-commerce and online store management with Shopify integration for CrewAI.

Enable your agents to manage e-commerce operations through Shopify. Handle customers, orders, products, inventory, and store analytics to streamline your online business with AI-powered automation.

Before using the Shopify integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A Shopify store with appropriate admin permissions
* Connected your Shopify store through the [Integrations page](https://app.crewai.com/integrations)

## Setting Up Shopify Integration

### 1. Connect Your Shopify Store

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Shopify** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for store and product management
5. Copy your Enterprise Token from [Integration Settings](https://app.crewai.com/crewai_plus/settings/integrations)

### 2. Install Required Package

### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>

Or add it to your `.env` file:

### **Customer Management**

<AccordionGroup>
  <Accordion title="shopify/get_customers">
    **Description:** Retrieve a list of customers from your Shopify store.

* `customerIds` (string, optional): Comma-separated list of customer IDs to filter by (example: "207119551, 207119552")
    * `createdAtMin` (string, optional): Only return customers created after this date (ISO or Unix timestamp)
    * `createdAtMax` (string, optional): Only return customers created before this date (ISO or Unix timestamp)
    * `updatedAtMin` (string, optional): Only return customers updated after this date (ISO or Unix timestamp)
    * `updatedAtMax` (string, optional): Only return customers updated before this date (ISO or Unix timestamp)
    * `limit` (string, optional): Maximum number of customers to return (defaults to 250)
  </Accordion>

<Accordion title="shopify/search_customers">
    **Description:** Search for customers using advanced filtering criteria.

* `filterFormula` (object, optional): Advanced filter in disjunctive normal form with field-specific operators
    * `limit` (string, optional): Maximum number of customers to return (defaults to 250)
  </Accordion>

<Accordion title="shopify/create_customer">
    **Description:** Create a new customer in your Shopify store.

* `firstName` (string, required): Customer's first name
    * `lastName` (string, required): Customer's last name
    * `email` (string, required): Customer's email address
    * `company` (string, optional): Company name
    * `streetAddressLine1` (string, optional): Street address
    * `streetAddressLine2` (string, optional): Street address line 2
    * `city` (string, optional): City
    * `state` (string, optional): State or province code
    * `country` (string, optional): Country
    * `zipCode` (string, optional): Zip code
    * `phone` (string, optional): Phone number
    * `tags` (string, optional): Tags as array or comma-separated list
    * `note` (string, optional): Customer note
    * `sendEmailInvite` (boolean, optional): Whether to send email invitation
    * `metafields` (object, optional): Additional metafields in JSON format
  </Accordion>

<Accordion title="shopify/update_customer">
    **Description:** Update an existing customer in your Shopify store.

* `customerId` (string, required): The ID of the customer to update
    * `firstName` (string, optional): Customer's first name
    * `lastName` (string, optional): Customer's last name
    * `email` (string, optional): Customer's email address
    * `company` (string, optional): Company name
    * `streetAddressLine1` (string, optional): Street address
    * `streetAddressLine2` (string, optional): Street address line 2
    * `city` (string, optional): City
    * `state` (string, optional): State or province code
    * `country` (string, optional): Country
    * `zipCode` (string, optional): Zip code
    * `phone` (string, optional): Phone number
    * `tags` (string, optional): Tags as array or comma-separated list
    * `note` (string, optional): Customer note
    * `sendEmailInvite` (boolean, optional): Whether to send email invitation
    * `metafields` (object, optional): Additional metafields in JSON format
  </Accordion>
</AccordionGroup>

### **Order Management**

<AccordionGroup>
  <Accordion title="shopify/get_orders">
    **Description:** Retrieve a list of orders from your Shopify store.

* `orderIds` (string, optional): Comma-separated list of order IDs to filter by (example: "450789469, 450789470")
    * `createdAtMin` (string, optional): Only return orders created after this date (ISO or Unix timestamp)
    * `createdAtMax` (string, optional): Only return orders created before this date (ISO or Unix timestamp)
    * `updatedAtMin` (string, optional): Only return orders updated after this date (ISO or Unix timestamp)
    * `updatedAtMax` (string, optional): Only return orders updated before this date (ISO or Unix timestamp)
    * `limit` (string, optional): Maximum number of orders to return (defaults to 250)
  </Accordion>

<Accordion title="shopify/create_order">
    **Description:** Create a new order in your Shopify store.

* `email` (string, required): Customer email address
    * `lineItems` (object, required): Order line items in JSON format with title, price, quantity, and variant\_id
    * `sendReceipt` (boolean, optional): Whether to send order receipt
    * `fulfillmentStatus` (string, optional): Fulfillment status - Options: fulfilled, null, partial, restocked
    * `financialStatus` (string, optional): Financial status - Options: pending, authorized, partially\_paid, paid, partially\_refunded, refunded, voided
    * `inventoryBehaviour` (string, optional): Inventory behavior - Options: bypass, decrement\_ignoring\_policy, decrement\_obeying\_policy
    * `note` (string, optional): Order note
  </Accordion>

<Accordion title="shopify/update_order">
    **Description:** Update an existing order in your Shopify store.

* `orderId` (string, required): The ID of the order to update
    * `email` (string, optional): Customer email address
    * `lineItems` (object, optional): Updated order line items in JSON format
    * `sendReceipt` (boolean, optional): Whether to send order receipt
    * `fulfillmentStatus` (string, optional): Fulfillment status - Options: fulfilled, null, partial, restocked
    * `financialStatus` (string, optional): Financial status - Options: pending, authorized, partially\_paid, paid, partially\_refunded, refunded, voided
    * `inventoryBehaviour` (string, optional): Inventory behavior - Options: bypass, decrement\_ignoring\_policy, decrement\_obeying\_policy
    * `note` (string, optional): Order note
  </Accordion>

<Accordion title="shopify/get_abandoned_carts">
    **Description:** Retrieve abandoned carts from your Shopify store.

* `createdWithInLast` (string, optional): Restrict results to checkouts created within specified time
    * `createdAfterId` (string, optional): Restrict results to after the specified ID
    * `status` (string, optional): Show checkouts with given status - Options: open, closed (defaults to open)
    * `createdAtMin` (string, optional): Only return carts created after this date (ISO or Unix timestamp)
    * `createdAtMax` (string, optional): Only return carts created before this date (ISO or Unix timestamp)
    * `limit` (string, optional): Maximum number of carts to return (defaults to 250)
  </Accordion>
</AccordionGroup>

### **Product Management (REST API)**

<AccordionGroup>
  <Accordion title="shopify/get_products">
    **Description:** Retrieve a list of products from your Shopify store using REST API.

* `productIds` (string, optional): Comma-separated list of product IDs to filter by (example: "632910392, 632910393")
    * `title` (string, optional): Filter by product title
    * `productType` (string, optional): Filter by product type
    * `vendor` (string, optional): Filter by vendor
    * `status` (string, optional): Filter by status - Options: active, archived, draft
    * `createdAtMin` (string, optional): Only return products created after this date (ISO or Unix timestamp)
    * `createdAtMax` (string, optional): Only return products created before this date (ISO or Unix timestamp)
    * `updatedAtMin` (string, optional): Only return products updated after this date (ISO or Unix timestamp)
    * `updatedAtMax` (string, optional): Only return products updated before this date (ISO or Unix timestamp)
    * `limit` (string, optional): Maximum number of products to return (defaults to 250)
  </Accordion>

<Accordion title="shopify/create_product">
    **Description:** Create a new product in your Shopify store using REST API.

* `title` (string, required): Product title
    * `productType` (string, required): Product type/category
    * `vendor` (string, required): Product vendor
    * `productDescription` (string, optional): Product description (accepts plain text or HTML)
    * `tags` (string, optional): Product tags as array or comma-separated list
    * `price` (string, optional): Product price
    * `inventoryPolicy` (string, optional): Inventory policy - Options: deny, continue
    * `imageUrl` (string, optional): Product image URL
    * `isPublished` (boolean, optional): Whether product is published
    * `publishToPointToSale` (boolean, optional): Whether to publish to point of sale
  </Accordion>

<Accordion title="shopify/update_product">
    **Description:** Update an existing product in your Shopify store using REST API.

* `productId` (string, required): The ID of the product to update
    * `title` (string, optional): Product title
    * `productType` (string, optional): Product type/category
    * `vendor` (string, optional): Product vendor
    * `productDescription` (string, optional): Product description (accepts plain text or HTML)
    * `tags` (string, optional): Product tags as array or comma-separated list
    * `price` (string, optional): Product price
    * `inventoryPolicy` (string, optional): Inventory policy - Options: deny, continue
    * `imageUrl` (string, optional): Product image URL
    * `isPublished` (boolean, optional): Whether product is published
    * `publishToPointToSale` (boolean, optional): Whether to publish to point of sale
  </Accordion>
</AccordionGroup>

### **Product Management (GraphQL)**

<AccordionGroup>
  <Accordion title="shopify/get_products_graphql">
    **Description:** Retrieve products using advanced GraphQL filtering capabilities.

* `productFilterFormula` (object, optional): Advanced filter in disjunctive normal form with support for fields like id, title, vendor, status, handle, tag, created\_at, updated\_at, published\_at
  </Accordion>

<Accordion title="shopify/create_product_graphql">
    **Description:** Create a new product using GraphQL API with enhanced media support.

* `title` (string, required): Product title
    * `productType` (string, required): Product type/category
    * `vendor` (string, required): Product vendor
    * `productDescription` (string, optional): Product description (accepts plain text or HTML)
    * `tags` (string, optional): Product tags as array or comma-separated list
    * `media` (object, optional): Media objects with alt text, content type, and source URL
    * `additionalFields` (object, optional): Additional product fields like status, requiresSellingPlan, giftCard
  </Accordion>

<Accordion title="shopify/update_product_graphql">
    **Description:** Update an existing product using GraphQL API with enhanced media support.

* `productId` (string, required): The GraphQL ID of the product to update (e.g., "gid://shopify/Product/913144112")
    * `title` (string, optional): Product title
    * `productType` (string, optional): Product type/category
    * `vendor` (string, optional): Product vendor
    * `productDescription` (string, optional): Product description (accepts plain text or HTML)
    * `tags` (string, optional): Product tags as array or comma-separated list
    * `media` (object, optional): Updated media objects with alt text, content type, and source URL
    * `additionalFields` (object, optional): Additional product fields like status, requiresSellingPlan, giftCard
  </Accordion>
</AccordionGroup>

### Basic Shopify Agent Setup

```python theme={null}
from crewai import Agent, Task, Crew
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

Example 3 (unknown):
```unknown
## Available Tools

### **Customer Management**

<AccordionGroup>
  <Accordion title="shopify/get_customers">
    **Description:** Retrieve a list of customers from your Shopify store.

    **Parameters:**

    * `customerIds` (string, optional): Comma-separated list of customer IDs to filter by (example: "207119551, 207119552")
    * `createdAtMin` (string, optional): Only return customers created after this date (ISO or Unix timestamp)
    * `createdAtMax` (string, optional): Only return customers created before this date (ISO or Unix timestamp)
    * `updatedAtMin` (string, optional): Only return customers updated after this date (ISO or Unix timestamp)
    * `updatedAtMax` (string, optional): Only return customers updated before this date (ISO or Unix timestamp)
    * `limit` (string, optional): Maximum number of customers to return (defaults to 250)
  </Accordion>

  <Accordion title="shopify/search_customers">
    **Description:** Search for customers using advanced filtering criteria.

    **Parameters:**

    * `filterFormula` (object, optional): Advanced filter in disjunctive normal form with field-specific operators
    * `limit` (string, optional): Maximum number of customers to return (defaults to 250)
  </Accordion>

  <Accordion title="shopify/create_customer">
    **Description:** Create a new customer in your Shopify store.

    **Parameters:**

    * `firstName` (string, required): Customer's first name
    * `lastName` (string, required): Customer's last name
    * `email` (string, required): Customer's email address
    * `company` (string, optional): Company name
    * `streetAddressLine1` (string, optional): Street address
    * `streetAddressLine2` (string, optional): Street address line 2
    * `city` (string, optional): City
    * `state` (string, optional): State or province code
    * `country` (string, optional): Country
    * `zipCode` (string, optional): Zip code
    * `phone` (string, optional): Phone number
    * `tags` (string, optional): Tags as array or comma-separated list
    * `note` (string, optional): Customer note
    * `sendEmailInvite` (boolean, optional): Whether to send email invitation
    * `metafields` (object, optional): Additional metafields in JSON format
  </Accordion>

  <Accordion title="shopify/update_customer">
    **Description:** Update an existing customer in your Shopify store.

    **Parameters:**

    * `customerId` (string, required): The ID of the customer to update
    * `firstName` (string, optional): Customer's first name
    * `lastName` (string, optional): Customer's last name
    * `email` (string, optional): Customer's email address
    * `company` (string, optional): Company name
    * `streetAddressLine1` (string, optional): Street address
    * `streetAddressLine2` (string, optional): Street address line 2
    * `city` (string, optional): City
    * `state` (string, optional): State or province code
    * `country` (string, optional): Country
    * `zipCode` (string, optional): Zip code
    * `phone` (string, optional): Phone number
    * `tags` (string, optional): Tags as array or comma-separated list
    * `note` (string, optional): Customer note
    * `sendEmailInvite` (boolean, optional): Whether to send email invitation
    * `metafields` (object, optional): Additional metafields in JSON format
  </Accordion>
</AccordionGroup>

### **Order Management**

<AccordionGroup>
  <Accordion title="shopify/get_orders">
    **Description:** Retrieve a list of orders from your Shopify store.

    **Parameters:**

    * `orderIds` (string, optional): Comma-separated list of order IDs to filter by (example: "450789469, 450789470")
    * `createdAtMin` (string, optional): Only return orders created after this date (ISO or Unix timestamp)
    * `createdAtMax` (string, optional): Only return orders created before this date (ISO or Unix timestamp)
    * `updatedAtMin` (string, optional): Only return orders updated after this date (ISO or Unix timestamp)
    * `updatedAtMax` (string, optional): Only return orders updated before this date (ISO or Unix timestamp)
    * `limit` (string, optional): Maximum number of orders to return (defaults to 250)
  </Accordion>

  <Accordion title="shopify/create_order">
    **Description:** Create a new order in your Shopify store.

    **Parameters:**

    * `email` (string, required): Customer email address
    * `lineItems` (object, required): Order line items in JSON format with title, price, quantity, and variant\_id
    * `sendReceipt` (boolean, optional): Whether to send order receipt
    * `fulfillmentStatus` (string, optional): Fulfillment status - Options: fulfilled, null, partial, restocked
    * `financialStatus` (string, optional): Financial status - Options: pending, authorized, partially\_paid, paid, partially\_refunded, refunded, voided
    * `inventoryBehaviour` (string, optional): Inventory behavior - Options: bypass, decrement\_ignoring\_policy, decrement\_obeying\_policy
    * `note` (string, optional): Order note
  </Accordion>

  <Accordion title="shopify/update_order">
    **Description:** Update an existing order in your Shopify store.

    **Parameters:**

    * `orderId` (string, required): The ID of the order to update
    * `email` (string, optional): Customer email address
    * `lineItems` (object, optional): Updated order line items in JSON format
    * `sendReceipt` (boolean, optional): Whether to send order receipt
    * `fulfillmentStatus` (string, optional): Fulfillment status - Options: fulfilled, null, partial, restocked
    * `financialStatus` (string, optional): Financial status - Options: pending, authorized, partially\_paid, paid, partially\_refunded, refunded, voided
    * `inventoryBehaviour` (string, optional): Inventory behavior - Options: bypass, decrement\_ignoring\_policy, decrement\_obeying\_policy
    * `note` (string, optional): Order note
  </Accordion>

  <Accordion title="shopify/get_abandoned_carts">
    **Description:** Retrieve abandoned carts from your Shopify store.

    **Parameters:**

    * `createdWithInLast` (string, optional): Restrict results to checkouts created within specified time
    * `createdAfterId` (string, optional): Restrict results to after the specified ID
    * `status` (string, optional): Show checkouts with given status - Options: open, closed (defaults to open)
    * `createdAtMin` (string, optional): Only return carts created after this date (ISO or Unix timestamp)
    * `createdAtMax` (string, optional): Only return carts created before this date (ISO or Unix timestamp)
    * `limit` (string, optional): Maximum number of carts to return (defaults to 250)
  </Accordion>
</AccordionGroup>

### **Product Management (REST API)**

<AccordionGroup>
  <Accordion title="shopify/get_products">
    **Description:** Retrieve a list of products from your Shopify store using REST API.

    **Parameters:**

    * `productIds` (string, optional): Comma-separated list of product IDs to filter by (example: "632910392, 632910393")
    * `title` (string, optional): Filter by product title
    * `productType` (string, optional): Filter by product type
    * `vendor` (string, optional): Filter by vendor
    * `status` (string, optional): Filter by status - Options: active, archived, draft
    * `createdAtMin` (string, optional): Only return products created after this date (ISO or Unix timestamp)
    * `createdAtMax` (string, optional): Only return products created before this date (ISO or Unix timestamp)
    * `updatedAtMin` (string, optional): Only return products updated after this date (ISO or Unix timestamp)
    * `updatedAtMax` (string, optional): Only return products updated before this date (ISO or Unix timestamp)
    * `limit` (string, optional): Maximum number of products to return (defaults to 250)
  </Accordion>

  <Accordion title="shopify/create_product">
    **Description:** Create a new product in your Shopify store using REST API.

    **Parameters:**

    * `title` (string, required): Product title
    * `productType` (string, required): Product type/category
    * `vendor` (string, required): Product vendor
    * `productDescription` (string, optional): Product description (accepts plain text or HTML)
    * `tags` (string, optional): Product tags as array or comma-separated list
    * `price` (string, optional): Product price
    * `inventoryPolicy` (string, optional): Inventory policy - Options: deny, continue
    * `imageUrl` (string, optional): Product image URL
    * `isPublished` (boolean, optional): Whether product is published
    * `publishToPointToSale` (boolean, optional): Whether to publish to point of sale
  </Accordion>

  <Accordion title="shopify/update_product">
    **Description:** Update an existing product in your Shopify store using REST API.

    **Parameters:**

    * `productId` (string, required): The ID of the product to update
    * `title` (string, optional): Product title
    * `productType` (string, optional): Product type/category
    * `vendor` (string, optional): Product vendor
    * `productDescription` (string, optional): Product description (accepts plain text or HTML)
    * `tags` (string, optional): Product tags as array or comma-separated list
    * `price` (string, optional): Product price
    * `inventoryPolicy` (string, optional): Inventory policy - Options: deny, continue
    * `imageUrl` (string, optional): Product image URL
    * `isPublished` (boolean, optional): Whether product is published
    * `publishToPointToSale` (boolean, optional): Whether to publish to point of sale
  </Accordion>
</AccordionGroup>

### **Product Management (GraphQL)**

<AccordionGroup>
  <Accordion title="shopify/get_products_graphql">
    **Description:** Retrieve products using advanced GraphQL filtering capabilities.

    **Parameters:**

    * `productFilterFormula` (object, optional): Advanced filter in disjunctive normal form with support for fields like id, title, vendor, status, handle, tag, created\_at, updated\_at, published\_at
  </Accordion>

  <Accordion title="shopify/create_product_graphql">
    **Description:** Create a new product using GraphQL API with enhanced media support.

    **Parameters:**

    * `title` (string, required): Product title
    * `productType` (string, required): Product type/category
    * `vendor` (string, required): Product vendor
    * `productDescription` (string, optional): Product description (accepts plain text or HTML)
    * `tags` (string, optional): Product tags as array or comma-separated list
    * `media` (object, optional): Media objects with alt text, content type, and source URL
    * `additionalFields` (object, optional): Additional product fields like status, requiresSellingPlan, giftCard
  </Accordion>

  <Accordion title="shopify/update_product_graphql">
    **Description:** Update an existing product using GraphQL API with enhanced media support.

    **Parameters:**

    * `productId` (string, required): The GraphQL ID of the product to update (e.g., "gid://shopify/Product/913144112")
    * `title` (string, optional): Product title
    * `productType` (string, optional): Product type/category
    * `vendor` (string, optional): Product vendor
    * `productDescription` (string, optional): Product description (accepts plain text or HTML)
    * `tags` (string, optional): Product tags as array or comma-separated list
    * `media` (object, optional): Updated media objects with alt text, content type, and source URL
    * `additionalFields` (object, optional): Additional product fields like status, requiresSellingPlan, giftCard
  </Accordion>
</AccordionGroup>

## Usage Examples

### Basic Shopify Agent Setup
```

---

## Slack Integration

**URL:** llms-txt#slack-integration

**Contents:**
- Overview
- Prerequisites
- Setting Up Slack Integration
  - 1. Connect Your Slack Workspace
  - 2. Install Required Package
  - 3. Environment Variable Setup
- Available Tools
  - **User Management**
  - **Channel Management**
  - **Messaging**

Source: https://docs.crewai.com/en/enterprise/integrations/slack

Team communication and collaboration with Slack integration for CrewAI.

Enable your agents to manage team communication through Slack. Send messages, search conversations, manage channels, and coordinate team activities to streamline your collaboration workflows with AI-powered automation.

Before using the Slack integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A Slack workspace with appropriate permissions
* Connected your Slack workspace through the [Integrations page](https://app.crewai.com/integrations)

## Setting Up Slack Integration

### 1. Connect Your Slack Workspace

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Slack** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for team communication
5. Copy your Enterprise Token from [Integration Settings](https://app.crewai.com/crewai_plus/settings/integrations)

### 2. Install Required Package

### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>

Or add it to your `.env` file:

### **User Management**

<AccordionGroup>
  <Accordion title="slack/list_members">
    **Description:** List all members in a Slack channel.

* No parameters required - retrieves all channel members
  </Accordion>

<Accordion title="slack/get_user_by_email">
    **Description:** Find a user in your Slack workspace by their email address.

* `email` (string, required): The email address of a user in the workspace
  </Accordion>

<Accordion title="slack/get_users_by_name">
    **Description:** Search for users by their name or display name.

* `name` (string, required): User's real name to search for
    * `displayName` (string, required): User's display name to search for
    * `paginationParameters` (object, optional): Pagination settings
      * `pageCursor` (string, optional): Page cursor for pagination
  </Accordion>
</AccordionGroup>

### **Channel Management**

<AccordionGroup>
  <Accordion title="slack/list_channels">
    **Description:** List all channels in your Slack workspace.

* No parameters required - retrieves all accessible channels
  </Accordion>
</AccordionGroup>

<AccordionGroup>
  <Accordion title="slack/send_message">
    **Description:** Send a message to a Slack channel.

* `channel` (string, required): Channel name or ID - Use Connect Portal Workflow Settings to allow users to select a channel, or enter a channel name to create a new channel
    * `message` (string, required): The message text to send
    * `botName` (string, required): The name of the bot that sends this message
    * `botIcon` (string, required): Bot icon - Can be either an image URL or an emoji (e.g., ":dog:")
    * `blocks` (object, optional): Slack Block Kit JSON for rich message formatting with attachments and interactive elements
    * `authenticatedUser` (boolean, optional): If true, message appears to come from your authenticated Slack user instead of the application (defaults to false)
  </Accordion>

<Accordion title="slack/send_direct_message">
    **Description:** Send a direct message to a specific user in Slack.

* `memberId` (string, required): Recipient user ID - Use Connect Portal Workflow Settings to allow users to select a workspace member
    * `message` (string, required): The message text to send
    * `botName` (string, required): The name of the bot that sends this message
    * `botIcon` (string, required): Bot icon - Can be either an image URL or an emoji (e.g., ":dog:")
    * `blocks` (object, optional): Slack Block Kit JSON for rich message formatting with attachments and interactive elements
    * `authenticatedUser` (boolean, optional): If true, message appears to come from your authenticated Slack user instead of the application (defaults to false)
  </Accordion>
</AccordionGroup>

### **Search & Discovery**

<AccordionGroup>
  <Accordion title="slack/search_messages">
    **Description:** Search for messages across your Slack workspace.

* `query` (string, required): Search query using Slack search syntax to find messages that match specified criteria

**Search Query Examples:**

* `"project update"` - Search for messages containing "project update"
    * `from:@john in:#general` - Search for messages from John in the #general channel
    * `has:link after:2023-01-01` - Search for messages with links after January 1, 2023
    * `in:@channel before:yesterday` - Search for messages in a specific channel before yesterday
  </Accordion>
</AccordionGroup>

## Block Kit Integration

Slack's Block Kit allows you to create rich, interactive messages. Here are some examples of how to use the `blocks` parameter:

### Simple Text with Attachment

### Rich Formatting with Sections

### Basic Slack Agent Setup

```python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

Example 3 (unknown):
```unknown
## Available Tools

### **User Management**

<AccordionGroup>
  <Accordion title="slack/list_members">
    **Description:** List all members in a Slack channel.

    **Parameters:**

    * No parameters required - retrieves all channel members
  </Accordion>

  <Accordion title="slack/get_user_by_email">
    **Description:** Find a user in your Slack workspace by their email address.

    **Parameters:**

    * `email` (string, required): The email address of a user in the workspace
  </Accordion>

  <Accordion title="slack/get_users_by_name">
    **Description:** Search for users by their name or display name.

    **Parameters:**

    * `name` (string, required): User's real name to search for
    * `displayName` (string, required): User's display name to search for
    * `paginationParameters` (object, optional): Pagination settings
      * `pageCursor` (string, optional): Page cursor for pagination
  </Accordion>
</AccordionGroup>

### **Channel Management**

<AccordionGroup>
  <Accordion title="slack/list_channels">
    **Description:** List all channels in your Slack workspace.

    **Parameters:**

    * No parameters required - retrieves all accessible channels
  </Accordion>
</AccordionGroup>

### **Messaging**

<AccordionGroup>
  <Accordion title="slack/send_message">
    **Description:** Send a message to a Slack channel.

    **Parameters:**

    * `channel` (string, required): Channel name or ID - Use Connect Portal Workflow Settings to allow users to select a channel, or enter a channel name to create a new channel
    * `message` (string, required): The message text to send
    * `botName` (string, required): The name of the bot that sends this message
    * `botIcon` (string, required): Bot icon - Can be either an image URL or an emoji (e.g., ":dog:")
    * `blocks` (object, optional): Slack Block Kit JSON for rich message formatting with attachments and interactive elements
    * `authenticatedUser` (boolean, optional): If true, message appears to come from your authenticated Slack user instead of the application (defaults to false)
  </Accordion>

  <Accordion title="slack/send_direct_message">
    **Description:** Send a direct message to a specific user in Slack.

    **Parameters:**

    * `memberId` (string, required): Recipient user ID - Use Connect Portal Workflow Settings to allow users to select a workspace member
    * `message` (string, required): The message text to send
    * `botName` (string, required): The name of the bot that sends this message
    * `botIcon` (string, required): Bot icon - Can be either an image URL or an emoji (e.g., ":dog:")
    * `blocks` (object, optional): Slack Block Kit JSON for rich message formatting with attachments and interactive elements
    * `authenticatedUser` (boolean, optional): If true, message appears to come from your authenticated Slack user instead of the application (defaults to false)
  </Accordion>
</AccordionGroup>

### **Search & Discovery**

<AccordionGroup>
  <Accordion title="slack/search_messages">
    **Description:** Search for messages across your Slack workspace.

    **Parameters:**

    * `query` (string, required): Search query using Slack search syntax to find messages that match specified criteria

    **Search Query Examples:**

    * `"project update"` - Search for messages containing "project update"
    * `from:@john in:#general` - Search for messages from John in the #general channel
    * `has:link after:2023-01-01` - Search for messages with links after January 1, 2023
    * `in:@channel before:yesterday` - Search for messages in a specific channel before yesterday
  </Accordion>
</AccordionGroup>

## Block Kit Integration

Slack's Block Kit allows you to create rich, interactive messages. Here are some examples of how to use the `blocks` parameter:

### Simple Text with Attachment
```

Example 4 (unknown):
```unknown
### Rich Formatting with Sections
```

---

## `SnowflakeSearchTool`

**URL:** llms-txt#`snowflakesearchtool`

**Contents:**
- Description
- Installation
- Steps to Get Started
- Example

The `SnowflakeSearchTool` is designed to connect to Snowflake data warehouses and execute SQL queries with advanced features like connection pooling, retry logic, and asynchronous execution. This tool allows CrewAI agents to interact with Snowflake databases, making it ideal for data analysis, reporting, and business intelligence tasks that require access to enterprise data stored in Snowflake.

To use this tool, you need to install the required dependencies:

## Steps to Get Started

To effectively use the `SnowflakeSearchTool`, follow these steps:

1. **Install Dependencies**: Install the required packages using one of the commands above.
2. **Configure Snowflake Connection**: Create a `SnowflakeConfig` object with your Snowflake credentials.
3. **Initialize the Tool**: Create an instance of the tool with the necessary configuration.
4. **Execute Queries**: Use the tool to run SQL queries against your Snowflake database.

The following example demonstrates how to use the `SnowflakeSearchTool` to query data from a Snowflake database:

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import SnowflakeSearchTool, SnowflakeConfig

**Examples:**

Example 1 (unknown):
```unknown
Or alternatively:
```

Example 2 (unknown):
```unknown
## Steps to Get Started

To effectively use the `SnowflakeSearchTool`, follow these steps:

1. **Install Dependencies**: Install the required packages using one of the commands above.
2. **Configure Snowflake Connection**: Create a `SnowflakeConfig` object with your Snowflake credentials.
3. **Initialize the Tool**: Create an instance of the tool with the necessary configuration.
4. **Execute Queries**: Use the tool to run SQL queries against your Snowflake database.

## Example

The following example demonstrates how to use the `SnowflakeSearchTool` to query data from a Snowflake database:
```

---

## Snowflake Search Tool

**URL:** llms-txt#snowflake-search-tool

Source: https://docs.crewai.com/en/tools/database-data/snowflakesearchtool

The `SnowflakeSearchTool` enables CrewAI agents to execute SQL queries and perform semantic search on Snowflake data warehouses.

---

## so now agents can only search within that website

**URL:** llms-txt#so-now-agents-can-only-search-within-that-website

**Contents:**
- Arguments
- Customization Options

tool = WebsiteSearchTool(website='https://example.com')
python Code theme={null}
tool = WebsiteSearchTool(
    config=dict(
        llm=dict(
            provider="ollama", # or google, openai, anthropic, llama2, ...
            config=dict(
                model="llama2",
                # temperature=0.5,
                # top_p=1,
                # stream=true,
            ),
        ),
        embedder=dict(
            provider="google-generativeai", # or openai, ollama, ...
            config=dict(
                model_name="gemini-embedding-001",
                task_type="RETRIEVAL_DOCUMENT",
                # title="Embeddings",
            ),
        ),
    )
)
```

**Examples:**

Example 1 (unknown):
```unknown
## Arguments

* `website`: An optional argument intended to specify the website URL for focused searches. This argument is designed to enhance the tool's flexibility by allowing targeted searches when necessary.

## Customization Options

By default, the tool uses OpenAI for both embeddings and summarization. To customize the model, you can use a config dictionary as follows:
```

---

## so the agent can only read the content of the specified directory

**URL:** llms-txt#so-the-agent-can-only-read-the-content-of-the-specified-directory

**Contents:**
- Arguments

tool = DirectoryReadTool(directory='/path/to/your/directory')
```

The following parameters can be used to customize the `DirectoryReadTool`'s behavior:

| Argument      | Type     | Description                                                                                                                                                                                                   |
| :------------ | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **directory** | `string` | *Optional*. An argument that specifies the path to the directory whose contents you wish to list. It accepts both absolute and relative paths, guiding the tool to the desired directory for content listing. |

---

## so the agent can only scrap the content of the specified website

**URL:** llms-txt#so-the-agent-can-only-scrap-the-content-of-the-specified-website

tool = ScrapeWebsiteTool(website_url='https://www.example.com')

---

## so the agent can only search the content of the specified DOCX file

**URL:** llms-txt#so-the-agent-can-only-search-the-content-of-the-specified-docx-file

**Contents:**
- Arguments
- Custom model and embeddings

tool = DOCXSearchTool(docx='path/to/your/document.docx')
python Code theme={null}
from chromadb.config import Settings

tool = DOCXSearchTool(
    config={
        "embedding_model": {
            "provider": "openai",
            "config": {
                "model": "text-embedding-3-small",
                # "api_key": "sk-...",
            },
        },
        "vectordb": {
            "provider": "chromadb",  # or "qdrant"
            "config": {
                # "settings": Settings(persist_directory="/content/chroma", allow_reset=True, is_persistent=True),
                # from qdrant_client.models import VectorParams, Distance
                # "vectors_config": VectorParams(size=384, distance=Distance.COSINE),
            }
        },
    }
)
```

**Examples:**

Example 1 (unknown):
```unknown
## Arguments

The following parameters can be used to customize the `DOCXSearchTool`'s behavior:

| Argument | Type     | Description                                                                                                                                                                                                        |
| :------- | :------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **docx** | `string` | *Optional*. An argument that specifies the path to the DOCX file you want to search. If not provided during initialization, the tool allows for later specification of any DOCX file's content path for searching. |

## Custom model and embeddings

By default, the tool uses OpenAI for both embeddings and summarization. To customize the model, you can use a config dictionary as follows:
```

---

## so the agent can search within the given text file's content

**URL:** llms-txt#so-the-agent-can-search-within-the-given-text-file's-content

**Contents:**
- Arguments
- Custom model and embeddings

tool = TXTSearchTool(txt='path/to/text/file.txt')
python Code theme={null}
from chromadb.config import Settings

tool = TXTSearchTool(
    config={
        # Required: embeddings provider + config
        "embedding_model": {
            "provider": "openai",  # or google-generativeai, cohere, ollama, ...
            "config": {
                "model": "text-embedding-3-small",
                # "api_key": "sk-...",  # optional if env var is set (e.g., OPENAI_API_KEY or EMBEDDINGS_OPENAI_API_KEY)
                # Provider examples:
                # Google → model_name: "gemini-embedding-001", task_type: "RETRIEVAL_DOCUMENT"
                # Cohere → model: "embed-english-v3.0"
                # Ollama → model: "nomic-embed-text"
            },
        },

# Required: vector database config
        "vectordb": {
            "provider": "chromadb",  # or "qdrant"
            "config": {
                # Chroma settings (optional persistence)
                # "settings": Settings(
                #     persist_directory="/content/chroma",
                #     allow_reset=True,
                #     is_persistent=True,
                # ),

# Qdrant vector params example:
                # from qdrant_client.models import VectorParams, Distance
                # "vectors_config": VectorParams(size=384, distance=Distance.COSINE),

# Note: collection name is controlled by the tool (default: "rag_tool_collection").
            }
        },
    }
)
```

**Examples:**

Example 1 (unknown):
```unknown
## Arguments

* `txt` (str): **Optional**. The path to the text file you want to search.
  This argument is only required if the tool was not initialized with a specific text file;
  otherwise, the search will be conducted within the initially provided text file.

## Custom model and embeddings

By default, the tool uses OpenAI for both embeddings and summarization.
To customize the model, you can use a config dictionary as follows:
```

---

## Specialist agents

**URL:** llms-txt#specialist-agents

researcher = Agent(
    role="Researcher",
    goal="Provide accurate research and analysis",
    backstory="Expert researcher with deep analytical skills",
    allow_delegation=False,  # Specialists focus on their expertise
    verbose=True
)

writer = Agent(
    role="Writer", 
    goal="Create compelling content",
    backstory="Skilled writer who creates engaging content",
    allow_delegation=False,
    verbose=True
)

---

## src/guide_creator_flow/crews/content_crew/config/agents.yaml

**URL:** llms-txt#src/guide_creator_flow/crews/content_crew/config/agents.yaml

content_writer:
  role: >
    Educational Content Writer
  goal: >
    Create engaging, informative content that thoroughly explains the assigned topic
    and provides valuable insights to the reader
  backstory: >
    You are a talented educational writer with expertise in creating clear, engaging
    content. You have a gift for explaining complex concepts in accessible language
    and organizing information in a way that helps readers build their understanding.
  llm: provider/model-id  # e.g. openai/gpt-4o, google/gemini-2.0-flash, anthropic/claude...

content_reviewer:
  role: >
    Educational Content Reviewer and Editor
  goal: >
    Ensure content is accurate, comprehensive, well-structured, and maintains
    consistency with previously written sections
  backstory: >
    You are a meticulous editor with years of experience reviewing educational
    content. You have an eye for detail, clarity, and coherence. You excel at
    improving content while maintaining the original author's voice and ensuring
    consistent quality across multiple sections.
  llm: provider/model-id  # e.g. openai/gpt-4o, google/gemini-2.0-flash, anthropic/claude...
yaml theme={null}

**Examples:**

Example 1 (unknown):
```unknown
These agent definitions establish the specialized roles and perspectives that will shape how our AI agents approach content creation. Notice how each agent has a distinct purpose and expertise.

2. Next, update the tasks configuration file to define the specific writing and reviewing tasks:
```

---

## src/guide_creator_flow/crews/content_crew/content_crew.py

**URL:** llms-txt#src/guide_creator_flow/crews/content_crew/content_crew.py

**Contents:**
- Step 5: Create the Flow

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class ContentCrew():
    """Content writing crew"""

agents: List[BaseAgent]
    tasks: List[Task]

@agent
    def content_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['content_writer'], # type: ignore[index]
            verbose=True
        )

@agent
    def content_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['content_reviewer'], # type: ignore[index]
            verbose=True
        )

@task
    def write_section_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_section_task'] # type: ignore[index]
        )

@task
    def review_section_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_section_task'], # type: ignore[index]
            context=[self.write_section_task()]
        )

@crew
    def crew(self) -> Crew:
        """Creates the content writing crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
python theme={null}
#!/usr/bin/env python
import json
import os
from typing import List, Dict
from pydantic import BaseModel, Field
from crewai import LLM
from crewai.flow.flow import Flow, listen, start
from guide_creator_flow.crews.content_crew.content_crew import ContentCrew

**Examples:**

Example 1 (unknown):
```unknown
This crew definition establishes the relationship between our agents and tasks, setting up a sequential process where the content writer creates a draft and then the reviewer improves it. While this crew can function independently, in our flow it will be orchestrated as part of a larger system.

## Step 5: Create the Flow

Now comes the exciting part - creating the flow that will orchestrate the entire guide creation process. This is where we'll combine regular Python code, direct LLM calls, and our content creation crew into a cohesive system.

Our flow will:

1. Get user input for a topic and audience level
2. Make a direct LLM call to create a structured guide outline
3. Process each section sequentially using the content writer crew
4. Combine everything into a final comprehensive document

Let's create our flow in the `main.py` file:
```

---

## src/latest_ai_development/config/agents.yaml

**URL:** llms-txt#src/latest_ai_development/config/agents.yaml

researcher:
  role: >
    {topic} Senior Data Researcher
  goal: >
    Uncover cutting-edge developments in {topic}
  backstory: >
    You're a seasoned researcher with a knack for uncovering the latest
    developments in {topic}. Known for your ability to find the most relevant
    information and present it in a clear and concise manner.

reporting_analyst:
  role: >
    {topic} Reporting Analyst
  goal: >
    Create detailed reports based on {topic} data analysis and research findings
  backstory: >
    You're a meticulous analyst with a keen eye for detail. You're known for
    your ability to turn complex data into clear and concise reports, making
    it easy for others to understand and act on the information you provide.
python Code theme={null}

**Examples:**

Example 1 (unknown):
```unknown
To use this YAML configuration in your code, create a crew class that inherits from `CrewBase`:
```

---

## src/latest_ai_development/crew.py

**URL:** llms-txt#src/latest_ai_development/crew.py

**Contents:**
  - Direct Code Definition (Alternative)
- Task Output
  - Task Output Attributes
  - Task Methods and Properties
  - Accessing Task Outputs

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

@CrewBase
class LatestAiDevelopmentCrew():
  """LatestAiDevelopment crew"""

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
      config=self.tasks_config['research_task'] # type: ignore[index]
    )

@task
  def reporting_task(self) -> Task:
    return Task(
      config=self.tasks_config['reporting_task'] # type: ignore[index]
    )

@crew
  def crew(self) -> Crew:
    return Crew(
      agents=[
        self.researcher(),
        self.reporting_analyst()
      ],
      tasks=[
        self.research_task(),
        self.reporting_task()
      ],
      process=Process.sequential
    )
python task.py theme={null}
from crewai import Task

research_task = Task(
    description="""
        Conduct a thorough research about AI Agents.
        Make sure you find any interesting and relevant information given
        the current year is 2025.
    """,
    expected_output="""
        A list with 10 bullet points of the most relevant information about AI Agents
    """,
    agent=researcher
)

reporting_task = Task(
    description="""
        Review the context you got and expand each topic into a full section for a report.
        Make sure the report is detailed and contains any and all relevant information.
    """,
    expected_output="""
        A fully fledge reports with the mains topics, each with a full section of information.
    """,
    agent=reporting_analyst,
    markdown=True,  # Enable markdown formatting for the final output
    output_file="report.md"
)
python Code theme={null}

**Examples:**

Example 1 (unknown):
```unknown
<Note>
  The names you use in your YAML files (`agents.yaml` and `tasks.yaml`) should match the method names in your Python code.
</Note>

### Direct Code Definition (Alternative)

Alternatively, you can define tasks directly in your code without using YAML configuration:
```

Example 2 (unknown):
```unknown
<Tip>
  Directly specify an `agent` for assignment or let the `hierarchical` CrewAI's process decide based on roles, availability, etc.
</Tip>

## Task Output

Understanding task outputs is crucial for building effective AI workflows. CrewAI provides a structured way to handle task results through the `TaskOutput` class, which supports multiple output formats and can be easily passed between tasks.

The output of a task in CrewAI framework is encapsulated within the `TaskOutput` class. This class provides a structured way to access results of a task, including various formats such as raw output, JSON, and Pydantic models.

By default, the `TaskOutput` will only include the `raw` output. A `TaskOutput` will only include the `pydantic` or `json_dict` output if the original `Task` object was configured with `output_pydantic` or `output_json`, respectively.

### Task Output Attributes

| Attribute         | Parameters      | Type                       | Description                                                                                        |
| :---------------- | :-------------- | :------------------------- | :------------------------------------------------------------------------------------------------- |
| **Description**   | `description`   | `str`                      | Description of the task.                                                                           |
| **Summary**       | `summary`       | `Optional[str]`            | Summary of the task, auto-generated from the first 10 words of the description.                    |
| **Raw**           | `raw`           | `str`                      | The raw output of the task. This is the default format for the output.                             |
| **Pydantic**      | `pydantic`      | `Optional[BaseModel]`      | A Pydantic model object representing the structured output of the task.                            |
| **JSON Dict**     | `json_dict`     | `Optional[Dict[str, Any]]` | A dictionary representing the JSON output of the task.                                             |
| **Agent**         | `agent`         | `str`                      | The agent that executed the task.                                                                  |
| **Output Format** | `output_format` | `OutputFormat`             | The format of the task output, with options including RAW, JSON, and Pydantic. The default is RAW. |
| **Messages**      | `messages`      | `list[LLMMessage]`         | The messages from the last task execution.                                                         |

### Task Methods and Properties

| Method/Property | Description                                                                                       |
| :-------------- | :------------------------------------------------------------------------------------------------ |
| **json**        | Returns the JSON string representation of the task output if the output format is JSON.           |
| **to\_dict**    | Converts the JSON and Pydantic outputs to a dictionary.                                           |
| **str**         | Returns the string representation of the task output, prioritizing Pydantic, then JSON, then raw. |

### Accessing Task Outputs

Once a task has been executed, its output can be accessed through the `output` attribute of the `Task` object. The `TaskOutput` class provides various ways to interact with and present this output.

#### Example
```

---

## src/research_crew/config/agents.yaml

**URL:** llms-txt#src/research_crew/config/agents.yaml

**Contents:**
- Step 4: Define Your Tasks

researcher:
  role: >
    Senior Research Specialist for {topic}
  goal: >
    Find comprehensive and accurate information about {topic}
    with a focus on recent developments and key insights
  backstory: >
    You are an experienced research specialist with a talent for
    finding relevant information from various sources. You excel at
    organizing information in a clear and structured manner, making
    complex topics accessible to others.
  llm: provider/model-id  # e.g. openai/gpt-4o, google/gemini-2.0-flash, anthropic/claude...

analyst:
  role: >
    Data Analyst and Report Writer for {topic}
  goal: >
    Analyze research findings and create a comprehensive, well-structured
    report that presents insights in a clear and engaging way
  backstory: >
    You are a skilled analyst with a background in data interpretation
    and technical writing. You have a talent for identifying patterns
    and extracting meaningful insights from research data, then
    communicating those insights effectively through well-crafted reports.
  llm: provider/model-id  # e.g. openai/gpt-4o, google/gemini-2.0-flash, anthropic/claude...
yaml theme={null}

**Examples:**

Example 1 (unknown):
```unknown
Notice how each agent has a distinct role, goal, and backstory. These elements aren't just descriptive - they actively shape how the agent approaches its tasks. By crafting these carefully, you can create agents with specialized skills and perspectives that complement each other.

## Step 4: Define Your Tasks

With our agents defined, we now need to give them specific tasks to perform. Tasks in CrewAI represent the concrete work that agents will perform, with detailed instructions and expected outputs.

For our research crew, we'll define two main tasks:

1. A **research task** for gathering comprehensive information
2. An **analysis task** for creating an insightful report

Let's modify the `tasks.yaml` file:
```

---

## src/research_crew/crew.py

**URL:** llms-txt#src/research_crew/crew.py

**Contents:**
- Step 6: Set Up Your Main Script

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class ResearchCrew():
    """Research crew for comprehensive topic analysis and reporting"""

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
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['analyst'], # type: ignore[index]
            verbose=True
        )

@task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'] # type: ignore[index]
        )

@task
    def analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['analysis_task'], # type: ignore[index]
            output_file='output/report.md'
        )

@crew
    def crew(self) -> Crew:
        """Creates the research crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
python theme={null}
#!/usr/bin/env python

**Examples:**

Example 1 (unknown):
```unknown
In this code, we're:

1. Creating the researcher agent and equipping it with the SerperDevTool to search the web
2. Creating the analyst agent
3. Setting up the research and analysis tasks
4. Configuring the crew to run tasks sequentially (the analyst will wait for the researcher to finish)

This is where the magic happens - with just a few lines of code, we've defined a collaborative AI system where specialized agents work together in a coordinated process.

## Step 6: Set Up Your Main Script

Now, let's set up the main script that will run our crew. This is where we provide the specific topic we want our crew to research.
```

---

## Start the crew's work

**URL:** llms-txt#start-the-crew's-work

**Contents:**
- Benefits of a Custom Manager Agent
- Setting a Manager LLM

result = crew.kickoff()
python Code theme={null}
from crewai import LLM

manager_llm = LLM(model="gpt-4o")

crew = Crew(
    agents=[researcher, writer],
    tasks=[task],
    process=Process.hierarchical,
    manager_llm=manager_llm
)
```

<Note>
  Either `manager_agent` or `manager_llm` must be set when using the hierarchical process.
</Note>

**Examples:**

Example 1 (unknown):
```unknown
## Benefits of a Custom Manager Agent

* **Enhanced Control**: Tailor the management approach to fit the specific needs of your project.
* **Improved Coordination**: Ensure efficient task coordination and management by an experienced agent.
* **Customizable Management**: Define managerial roles and responsibilities that align with your project's goals.

## Setting a Manager LLM

If you're using the hierarchical process and don't want to set a custom manager agent, you can specify the language model for the manager:
```

---

## Strategic LLM Selection Guide

**URL:** llms-txt#strategic-llm-selection-guide

**Contents:**
- The CrewAI Approach to LLM Selection
- Quick Decision Framework
- Core Selection Framework
  - a. Task-First Thinking
  - b. Model Capability Mapping
- Strategic Configuration Patterns
  - a. Multi-Model Approach

Source: https://docs.crewai.com/en/learn/llm-selection-guide

Strategic framework for choosing the right LLM for your CrewAI AI agents and writing effective task and agent definitions

## The CrewAI Approach to LLM Selection

Rather than prescriptive model recommendations, we advocate for a **thinking framework** that helps you make informed decisions based on your specific use case, constraints, and requirements. The LLM landscape evolves rapidly, with new models emerging regularly and existing ones being updated frequently. What matters most is developing a systematic approach to evaluation that remains relevant regardless of which specific models are available.

<Note>
  This guide focuses on strategic thinking rather than specific model recommendations, as the LLM landscape evolves rapidly.
</Note>

## Quick Decision Framework

<Steps>
  <Step title="Analyze Your Tasks">
    Begin by deeply understanding what your tasks actually require. Consider the cognitive complexity involved, the depth of reasoning needed, the format of expected outputs, and the amount of context the model will need to process. This foundational analysis will guide every subsequent decision.
  </Step>

<Step title="Map Model Capabilities">
    Once you understand your requirements, map them to model strengths. Different model families excel at different types of work; some are optimized for reasoning and analysis, others for creativity and content generation, and others for speed and efficiency.
  </Step>

<Step title="Consider Constraints">
    Factor in your real-world operational constraints including budget limitations, latency requirements, data privacy needs, and infrastructure capabilities. The theoretically best model may not be the practically best choice for your situation.
  </Step>

<Step title="Test and Iterate">
    Start with reliable, well-understood models and optimize based on actual performance in your specific use case. Real-world results often differ from theoretical benchmarks, so empirical testing is crucial.
  </Step>
</Steps>

## Core Selection Framework

### a. Task-First Thinking

The most critical step in LLM selection is understanding what your task actually demands. Too often, teams select models based on general reputation or benchmark scores without carefully analyzing their specific requirements. This approach leads to either over-engineering simple tasks with expensive, complex models, or under-powering sophisticated work with models that lack the necessary capabilities.

<Tabs>
  <Tab title="Reasoning Complexity">
    * **Simple Tasks** represent the majority of everyday AI work and include basic instruction following, straightforward data processing, and simple formatting operations. These tasks typically have clear inputs and outputs with minimal ambiguity. The cognitive load is low, and the model primarily needs to follow explicit instructions rather than engage in complex reasoning.

* **Complex Tasks** require multi-step reasoning, strategic thinking, and the ability to handle ambiguous or incomplete information. These might involve analyzing multiple data sources, developing comprehensive strategies, or solving problems that require breaking down into smaller components. The model needs to maintain context across multiple reasoning steps and often must make inferences that aren't explicitly stated.

* **Creative Tasks** demand a different type of cognitive capability focused on generating novel, engaging, and contextually appropriate content. This includes storytelling, marketing copy creation, and creative problem-solving. The model needs to understand nuance, tone, and audience while producing content that feels authentic and engaging rather than formulaic.
  </Tab>

<Tab title="Output Requirements">
    * **Structured Data** tasks require precision and consistency in format adherence. When working with JSON, XML, or database formats, the model must reliably produce syntactically correct output that can be programmatically processed. These tasks often have strict validation requirements and little tolerance for format errors, making reliability more important than creativity.

* **Creative Content** outputs demand a balance of technical competence and creative flair. The model needs to understand audience, tone, and brand voice while producing content that engages readers and achieves specific communication goals. Quality here is often subjective and requires models that can adapt their writing style to different contexts and purposes.

* **Technical Content** sits between structured data and creative content, requiring both precision and clarity. Documentation, code generation, and technical analysis need to be accurate and comprehensive while remaining accessible to the intended audience. The model must understand complex technical concepts and communicate them effectively.
  </Tab>

<Tab title="Context Needs">
    * **Short Context** scenarios involve focused, immediate tasks where the model needs to process limited information quickly. These are often transactional interactions where speed and efficiency matter more than deep understanding. The model doesn't need to maintain extensive conversation history or process large documents.

* **Long Context** requirements emerge when working with substantial documents, extended conversations, or complex multi-part tasks. The model needs to maintain coherence across thousands of tokens while referencing earlier information accurately. This capability becomes crucial for document analysis, comprehensive research, and sophisticated dialogue systems.

* **Very Long Context** scenarios push the boundaries of what's currently possible, involving massive document processing, extensive research synthesis, or complex multi-session interactions. These use cases require models specifically designed for extended context handling and often involve trade-offs between context length and processing speed.
  </Tab>
</Tabs>

### b. Model Capability Mapping

Understanding model capabilities requires looking beyond marketing claims and benchmark scores to understand the fundamental strengths and limitations of different model architectures and training approaches.

<AccordionGroup>
  <Accordion title="Reasoning Models" icon="brain">
    Reasoning models represent a specialized category designed specifically for complex, multi-step thinking tasks. These models excel when problems require careful analysis, strategic planning, or systematic problem decomposition. They typically employ techniques like chain-of-thought reasoning or tree-of-thought processing to work through complex problems step by step.

The strength of reasoning models lies in their ability to maintain logical consistency across extended reasoning chains and to break down complex problems into manageable components. They're particularly valuable for strategic planning, complex analysis, and situations where the quality of reasoning matters more than speed of response.

However, reasoning models often come with trade-offs in terms of speed and cost. They may also be less suitable for creative tasks or simple operations where their sophisticated reasoning capabilities aren't needed. Consider these models when your tasks involve genuine complexity that benefits from systematic, step-by-step analysis.
  </Accordion>

<Accordion title="General Purpose Models" icon="microchip">
    General purpose models offer the most balanced approach to LLM selection, providing solid performance across a wide range of tasks without extreme specialization in any particular area. These models are trained on diverse datasets and optimized for versatility rather than peak performance in specific domains.

The primary advantage of general purpose models is their reliability and predictability across different types of work. They handle most standard business tasks competently, from research and analysis to content creation and data processing. This makes them excellent choices for teams that need consistent performance across varied workflows.

While general purpose models may not achieve the peak performance of specialized alternatives in specific domains, they offer operational simplicity and reduced complexity in model management. They're often the best starting point for new projects, allowing teams to understand their specific needs before potentially optimizing with more specialized models.
  </Accordion>

<Accordion title="Fast & Efficient Models" icon="bolt">
    Fast and efficient models prioritize speed, cost-effectiveness, and resource efficiency over sophisticated reasoning capabilities. These models are optimized for high-throughput scenarios where quick responses and low operational costs are more important than nuanced understanding or complex reasoning.

These models excel in scenarios involving routine operations, simple data processing, function calling, and high-volume tasks where the cognitive requirements are relatively straightforward. They're particularly valuable for applications that need to process many requests quickly or operate within tight budget constraints.

The key consideration with efficient models is ensuring that their capabilities align with your task requirements. While they can handle many routine operations effectively, they may struggle with tasks requiring nuanced understanding, complex reasoning, or sophisticated content generation. They're best used for well-defined, routine operations where speed and cost matter more than sophistication.
  </Accordion>

<Accordion title="Creative Models" icon="pen">
    Creative models are specifically optimized for content generation, writing quality, and creative thinking tasks. These models typically excel at understanding nuance, tone, and style while producing engaging, contextually appropriate content that feels natural and authentic.

The strength of creative models lies in their ability to adapt writing style to different audiences, maintain consistent voice and tone, and generate content that engages readers effectively. They often perform better on tasks involving storytelling, marketing copy, brand communications, and other content where creativity and engagement are primary goals.

When selecting creative models, consider not just their ability to generate text, but their understanding of audience, context, and purpose. The best creative models can adapt their output to match specific brand voices, target different audience segments, and maintain consistency across extended content pieces.
  </Accordion>

<Accordion title="Open Source Models" icon="code">
    Open source models offer unique advantages in terms of cost control, customization potential, data privacy, and deployment flexibility. These models can be run locally or on private infrastructure, providing complete control over data handling and model behavior.

The primary benefits of open source models include elimination of per-token costs, ability to fine-tune for specific use cases, complete data privacy, and independence from external API providers. They're particularly valuable for organizations with strict data privacy requirements, budget constraints, or specific customization needs.

However, open source models require more technical expertise to deploy and maintain effectively. Teams need to consider infrastructure costs, model management complexity, and the ongoing effort required to keep models updated and optimized. The total cost of ownership may be higher than cloud-based alternatives when factoring in technical overhead.
  </Accordion>
</AccordionGroup>

## Strategic Configuration Patterns

### a. Multi-Model Approach

<Tip>
  Use different models for different purposes within the same crew to optimize both performance and cost.
</Tip>

The most sophisticated CrewAI implementations often employ multiple models strategically, assigning different models to different agents based on their specific roles and requirements. This approach allows teams to optimize for both performance and cost by using the most appropriate model for each type of work.

Planning agents benefit from reasoning models that can handle complex strategic thinking and multi-step analysis. These agents often serve as the "brain" of the operation, developing strategies and coordinating other agents' work. Content agents, on the other hand, perform best with creative models that excel at writing quality and audience engagement. Processing agents handling routine operations can use efficient models that prioritize speed and cost-effectiveness.

**Example: Research and Analysis Crew**

```python theme={null}
from crewai import Agent, Task, Crew, LLM

---

## Stripe Integration

**URL:** llms-txt#stripe-integration

**Contents:**
- Overview
- Prerequisites
- Setting Up Stripe Integration
  - 1. Connect Your Stripe Account
  - 2. Install Required Package
  - 3. Environment Variable Setup
- Available Tools
  - **Customer Management**
  - **Subscription Management**
  - **Product Management**

Source: https://docs.crewai.com/en/enterprise/integrations/stripe

Payment processing and subscription management with Stripe integration for CrewAI.

Enable your agents to manage payments, subscriptions, and customer billing through Stripe. Handle customer data, process subscriptions, manage products, and track financial transactions to streamline your payment workflows with AI-powered automation.

Before using the Stripe integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A Stripe account with appropriate API permissions
* Connected your Stripe account through the [Integrations page](https://app.crewai.com/integrations)

## Setting Up Stripe Integration

### 1. Connect Your Stripe Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Stripe** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for payment processing
5. Copy your Enterprise Token from [Integration Settings](https://app.crewai.com/crewai_plus/settings/integrations)

### 2. Install Required Package

### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>

Or add it to your `.env` file:

### **Customer Management**

<AccordionGroup>
  <Accordion title="stripe/create_customer">
    **Description:** Create a new customer in your Stripe account.

* `emailCreateCustomer` (string, required): Customer's email address
    * `name` (string, optional): Customer's full name
    * `description` (string, optional): Customer description for internal reference
    * `metadataCreateCustomer` (object, optional): Additional metadata as key-value pairs (e.g., `{"field1": 1, "field2": 2}`)
  </Accordion>

<Accordion title="stripe/get_customer_by_id">
    **Description:** Retrieve a specific customer by their Stripe customer ID.

* `idGetCustomer` (string, required): The Stripe customer ID to retrieve
  </Accordion>

<Accordion title="stripe/get_customers">
    **Description:** Retrieve a list of customers with optional filtering.

* `emailGetCustomers` (string, optional): Filter customers by email address
    * `createdAfter` (string, optional): Filter customers created after this date (Unix timestamp)
    * `createdBefore` (string, optional): Filter customers created before this date (Unix timestamp)
    * `limitGetCustomers` (string, optional): Maximum number of customers to return (defaults to 10)
  </Accordion>

<Accordion title="stripe/update_customer">
    **Description:** Update an existing customer's information.

* `customerId` (string, required): The ID of the customer to update
    * `emailUpdateCustomer` (string, optional): Updated email address
    * `name` (string, optional): Updated customer name
    * `description` (string, optional): Updated customer description
    * `metadataUpdateCustomer` (object, optional): Updated metadata as key-value pairs
  </Accordion>
</AccordionGroup>

### **Subscription Management**

<AccordionGroup>
  <Accordion title="stripe/create_subscription">
    **Description:** Create a new subscription for a customer.

* `customerIdCreateSubscription` (string, required): The customer ID for whom the subscription will be created
    * `plan` (string, required): The plan ID for the subscription - Use Connect Portal Workflow Settings to allow users to select a plan
    * `metadataCreateSubscription` (object, optional): Additional metadata for the subscription
  </Accordion>

<Accordion title="stripe/get_subscriptions">
    **Description:** Retrieve subscriptions with optional filtering.

* `customerIdGetSubscriptions` (string, optional): Filter subscriptions by customer ID
    * `subscriptionStatus` (string, optional): Filter by subscription status - Options: incomplete, incomplete\_expired, trialing, active, past\_due, canceled, unpaid
    * `limitGetSubscriptions` (string, optional): Maximum number of subscriptions to return (defaults to 10)
  </Accordion>
</AccordionGroup>

### **Product Management**

<AccordionGroup>
  <Accordion title="stripe/create_product">
    **Description:** Create a new product in your Stripe catalog.

* `productName` (string, required): The product name
    * `description` (string, optional): Product description
    * `metadataProduct` (object, optional): Additional product metadata as key-value pairs
  </Accordion>

<Accordion title="stripe/get_product_by_id">
    **Description:** Retrieve a specific product by its Stripe product ID.

* `productId` (string, required): The Stripe product ID to retrieve
  </Accordion>

<Accordion title="stripe/get_products">
    **Description:** Retrieve a list of products with optional filtering.

* `createdAfter` (string, optional): Filter products created after this date (Unix timestamp)
    * `createdBefore` (string, optional): Filter products created before this date (Unix timestamp)
    * `limitGetProducts` (string, optional): Maximum number of products to return (defaults to 10)
  </Accordion>
</AccordionGroup>

### **Financial Operations**

<AccordionGroup>
  <Accordion title="stripe/get_balance_transactions">
    **Description:** Retrieve balance transactions from your Stripe account.

* `balanceTransactionType` (string, optional): Filter by transaction type - Options: charge, refund, payment, payment\_refund
    * `paginationParameters` (object, optional): Pagination settings
      * `pageCursor` (string, optional): Page cursor for pagination
  </Accordion>

<Accordion title="stripe/get_plans">
    **Description:** Retrieve subscription plans from your Stripe account.

* `isPlanActive` (boolean, optional): Filter by plan status - true for active plans, false for inactive plans
    * `paginationParameters` (object, optional): Pagination settings
      * `pageCursor` (string, optional): Page cursor for pagination
  </Accordion>
</AccordionGroup>

### Basic Stripe Agent Setup

```python theme={null}
from crewai import Agent, Task, Crew
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

Example 3 (unknown):
```unknown
## Available Tools

### **Customer Management**

<AccordionGroup>
  <Accordion title="stripe/create_customer">
    **Description:** Create a new customer in your Stripe account.

    **Parameters:**

    * `emailCreateCustomer` (string, required): Customer's email address
    * `name` (string, optional): Customer's full name
    * `description` (string, optional): Customer description for internal reference
    * `metadataCreateCustomer` (object, optional): Additional metadata as key-value pairs (e.g., `{"field1": 1, "field2": 2}`)
  </Accordion>

  <Accordion title="stripe/get_customer_by_id">
    **Description:** Retrieve a specific customer by their Stripe customer ID.

    **Parameters:**

    * `idGetCustomer` (string, required): The Stripe customer ID to retrieve
  </Accordion>

  <Accordion title="stripe/get_customers">
    **Description:** Retrieve a list of customers with optional filtering.

    **Parameters:**

    * `emailGetCustomers` (string, optional): Filter customers by email address
    * `createdAfter` (string, optional): Filter customers created after this date (Unix timestamp)
    * `createdBefore` (string, optional): Filter customers created before this date (Unix timestamp)
    * `limitGetCustomers` (string, optional): Maximum number of customers to return (defaults to 10)
  </Accordion>

  <Accordion title="stripe/update_customer">
    **Description:** Update an existing customer's information.

    **Parameters:**

    * `customerId` (string, required): The ID of the customer to update
    * `emailUpdateCustomer` (string, optional): Updated email address
    * `name` (string, optional): Updated customer name
    * `description` (string, optional): Updated customer description
    * `metadataUpdateCustomer` (object, optional): Updated metadata as key-value pairs
  </Accordion>
</AccordionGroup>

### **Subscription Management**

<AccordionGroup>
  <Accordion title="stripe/create_subscription">
    **Description:** Create a new subscription for a customer.

    **Parameters:**

    * `customerIdCreateSubscription` (string, required): The customer ID for whom the subscription will be created
    * `plan` (string, required): The plan ID for the subscription - Use Connect Portal Workflow Settings to allow users to select a plan
    * `metadataCreateSubscription` (object, optional): Additional metadata for the subscription
  </Accordion>

  <Accordion title="stripe/get_subscriptions">
    **Description:** Retrieve subscriptions with optional filtering.

    **Parameters:**

    * `customerIdGetSubscriptions` (string, optional): Filter subscriptions by customer ID
    * `subscriptionStatus` (string, optional): Filter by subscription status - Options: incomplete, incomplete\_expired, trialing, active, past\_due, canceled, unpaid
    * `limitGetSubscriptions` (string, optional): Maximum number of subscriptions to return (defaults to 10)
  </Accordion>
</AccordionGroup>

### **Product Management**

<AccordionGroup>
  <Accordion title="stripe/create_product">
    **Description:** Create a new product in your Stripe catalog.

    **Parameters:**

    * `productName` (string, required): The product name
    * `description` (string, optional): Product description
    * `metadataProduct` (object, optional): Additional product metadata as key-value pairs
  </Accordion>

  <Accordion title="stripe/get_product_by_id">
    **Description:** Retrieve a specific product by its Stripe product ID.

    **Parameters:**

    * `productId` (string, required): The Stripe product ID to retrieve
  </Accordion>

  <Accordion title="stripe/get_products">
    **Description:** Retrieve a list of products with optional filtering.

    **Parameters:**

    * `createdAfter` (string, optional): Filter products created after this date (Unix timestamp)
    * `createdBefore` (string, optional): Filter products created before this date (Unix timestamp)
    * `limitGetProducts` (string, optional): Maximum number of products to return (defaults to 10)
  </Accordion>
</AccordionGroup>

### **Financial Operations**

<AccordionGroup>
  <Accordion title="stripe/get_balance_transactions">
    **Description:** Retrieve balance transactions from your Stripe account.

    **Parameters:**

    * `balanceTransactionType` (string, optional): Filter by transaction type - Options: charge, refund, payment, payment\_refund
    * `paginationParameters` (object, optional): Pagination settings
      * `pageCursor` (string, optional): Page cursor for pagination
  </Accordion>

  <Accordion title="stripe/get_plans">
    **Description:** Retrieve subscription plans from your Stripe account.

    **Parameters:**

    * `isPlanActive` (boolean, optional): Filter by plan status - true for active plans, false for inactive plans
    * `paginationParameters` (object, optional): Pagination settings
      * `pageCursor` (string, optional): Page cursor for pagination
  </Accordion>
</AccordionGroup>

## Usage Examples

### Basic Stripe Agent Setup
```

---

## Tasks

**URL:** llms-txt#tasks

**Contents:**
- Overview
  - Task Execution Flow
- Task Attributes
- Creating Tasks
  - YAML Configuration (Recommended)

Source: https://docs.crewai.com/en/concepts/tasks

Detailed guide on managing and creating tasks within the CrewAI framework.

In the CrewAI framework, a `Task` is a specific assignment completed by an `Agent`.

Tasks provide all necessary details for execution, such as a description, the agent responsible, required tools, and more, facilitating a wide range of action complexities.

Tasks within CrewAI can be collaborative, requiring multiple agents to work together. This is managed through the task properties and orchestrated by the Crew's process, enhancing teamwork and efficiency.

<Note type="info" title="Enterprise Enhancement: Visual Task Builder">
  CrewAI AOP includes a Visual Task Builder in Crew Studio that simplifies complex task creation and chaining. Design your task flows visually and test them in real-time without writing code.

<img alt="Task Builder Screenshot" />

The Visual Task Builder enables:

* Drag-and-drop task creation
  * Visual task dependencies and flow
  * Real-time testing and validation
  * Easy sharing and collaboration
</Note>

### Task Execution Flow

Tasks can be executed in two ways:

* **Sequential**: Tasks are executed in the order they are defined
* **Hierarchical**: Tasks are assigned to agents based on their roles and expertise

The execution flow is defined when creating the crew:

| Attribute                              | Parameters              | Type                        | Description                                                                                                     |                                                                            |
| :------------------------------------- | :---------------------- | :-------------------------- | :-------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **Description**                        | `description`           | `str`                       | A clear, concise statement of what the task entails.                                                            |                                                                            |
| **Expected Output**                    | `expected_output`       | `str`                       | A detailed description of what the task's completion looks like.                                                |                                                                            |
| **Name** *(optional)*                  | `name`                  | `Optional[str]`             | A name identifier for the task.                                                                                 |                                                                            |
| **Agent** *(optional)*                 | `agent`                 | `Optional[BaseAgent]`       | The agent responsible for executing the task.                                                                   |                                                                            |
| **Tools** *(optional)*                 | `tools`                 | `List[BaseTool]`            | The tools/resources the agent is limited to use for this task.                                                  |                                                                            |
| **Context** *(optional)*               | `context`               | `Optional[List["Task"]]`    | Other tasks whose outputs will be used as context for this task.                                                |                                                                            |
| **Async Execution** *(optional)*       | `async_execution`       | `Optional[bool]`            | Whether the task should be executed asynchronously. Defaults to False.                                          |                                                                            |
| **Human Input** *(optional)*           | `human_input`           | `Optional[bool]`            | Whether the task should have a human review the final answer of the agent. Defaults to False.                   |                                                                            |
| **Markdown** *(optional)*              | `markdown`              | `Optional[bool]`            | Whether the task should instruct the agent to return the final answer formatted in Markdown. Defaults to False. |                                                                            |
| **Config** *(optional)*                | `config`                | `Optional[Dict[str, Any]]`  | Task-specific configuration parameters.                                                                         |                                                                            |
| **Output File** *(optional)*           | `output_file`           | `Optional[str]`             | File path for storing the task output.                                                                          |                                                                            |
| **Create Directory** *(optional)*      | `create_directory`      | `Optional[bool]`            | Whether to create the directory for output\_file if it doesn't exist. Defaults to True.                         |                                                                            |
| **Output JSON** *(optional)*           | `output_json`           | `Optional[Type[BaseModel]]` | A Pydantic model to structure the JSON output.                                                                  |                                                                            |
| **Output Pydantic** *(optional)*       | `output_pydantic`       | `Optional[Type[BaseModel]]` | A Pydantic model for task output.                                                                               |                                                                            |
| **Callback** *(optional)*              | `callback`              | `Optional[Any]`             | Function/object to be executed after task completion.                                                           |                                                                            |
| **Guardrail** *(optional)*             | `guardrail`             | `Optional[Callable]`        | Function to validate task output before proceeding to next task.                                                |                                                                            |
| **Guardrails** *(optional)*            | `guardrails`            | \`Optional\[List\[Callable] | List\[str]]\`                                                                                                   | List of guardrails to validate task output before proceeding to next task. |
| **Guardrail Max Retries** *(optional)* | `guardrail_max_retries` | `Optional[int]`             | Maximum number of retries when guardrail validation fails. Defaults to 3.                                       |                                                                            |

<Note type="warning" title="Deprecated: max_retries">
  The task attribute `max_retries` is deprecated and will be removed in v1.0.0.
  Use `guardrail_max_retries` instead to control retry attempts when a guardrail fails.
</Note>

There are two ways to create tasks in CrewAI: using **YAML configuration (recommended)** or defining them **directly in code**.

### YAML Configuration (Recommended)

Using YAML configuration provides a cleaner, more maintainable way to define tasks. We strongly recommend using this approach to define tasks in your CrewAI projects.

After creating your CrewAI project as outlined in the [Installation](/en/installation) section, navigate to the `src/latest_ai_development/config/tasks.yaml` file and modify the template to match your specific task requirements.

<Note>
  Variables in your YAML files (like `{topic}`) will be replaced with values from your inputs when running the crew:

Here's an example of how to configure tasks using YAML:

'
  agent: reporting_analyst
  markdown: true
  output_file: report.md
python crew.py theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## Task Attributes

| Attribute                              | Parameters              | Type                        | Description                                                                                                     |                                                                            |
| :------------------------------------- | :---------------------- | :-------------------------- | :-------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **Description**                        | `description`           | `str`                       | A clear, concise statement of what the task entails.                                                            |                                                                            |
| **Expected Output**                    | `expected_output`       | `str`                       | A detailed description of what the task's completion looks like.                                                |                                                                            |
| **Name** *(optional)*                  | `name`                  | `Optional[str]`             | A name identifier for the task.                                                                                 |                                                                            |
| **Agent** *(optional)*                 | `agent`                 | `Optional[BaseAgent]`       | The agent responsible for executing the task.                                                                   |                                                                            |
| **Tools** *(optional)*                 | `tools`                 | `List[BaseTool]`            | The tools/resources the agent is limited to use for this task.                                                  |                                                                            |
| **Context** *(optional)*               | `context`               | `Optional[List["Task"]]`    | Other tasks whose outputs will be used as context for this task.                                                |                                                                            |
| **Async Execution** *(optional)*       | `async_execution`       | `Optional[bool]`            | Whether the task should be executed asynchronously. Defaults to False.                                          |                                                                            |
| **Human Input** *(optional)*           | `human_input`           | `Optional[bool]`            | Whether the task should have a human review the final answer of the agent. Defaults to False.                   |                                                                            |
| **Markdown** *(optional)*              | `markdown`              | `Optional[bool]`            | Whether the task should instruct the agent to return the final answer formatted in Markdown. Defaults to False. |                                                                            |
| **Config** *(optional)*                | `config`                | `Optional[Dict[str, Any]]`  | Task-specific configuration parameters.                                                                         |                                                                            |
| **Output File** *(optional)*           | `output_file`           | `Optional[str]`             | File path for storing the task output.                                                                          |                                                                            |
| **Create Directory** *(optional)*      | `create_directory`      | `Optional[bool]`            | Whether to create the directory for output\_file if it doesn't exist. Defaults to True.                         |                                                                            |
| **Output JSON** *(optional)*           | `output_json`           | `Optional[Type[BaseModel]]` | A Pydantic model to structure the JSON output.                                                                  |                                                                            |
| **Output Pydantic** *(optional)*       | `output_pydantic`       | `Optional[Type[BaseModel]]` | A Pydantic model for task output.                                                                               |                                                                            |
| **Callback** *(optional)*              | `callback`              | `Optional[Any]`             | Function/object to be executed after task completion.                                                           |                                                                            |
| **Guardrail** *(optional)*             | `guardrail`             | `Optional[Callable]`        | Function to validate task output before proceeding to next task.                                                |                                                                            |
| **Guardrails** *(optional)*            | `guardrails`            | \`Optional\[List\[Callable] | List\[str]]\`                                                                                                   | List of guardrails to validate task output before proceeding to next task. |
| **Guardrail Max Retries** *(optional)* | `guardrail_max_retries` | `Optional[int]`             | Maximum number of retries when guardrail validation fails. Defaults to 3.                                       |                                                                            |

<Note type="warning" title="Deprecated: max_retries">
  The task attribute `max_retries` is deprecated and will be removed in v1.0.0.
  Use `guardrail_max_retries` instead to control retry attempts when a guardrail fails.
</Note>

## Creating Tasks

There are two ways to create tasks in CrewAI: using **YAML configuration (recommended)** or defining them **directly in code**.

### YAML Configuration (Recommended)

Using YAML configuration provides a cleaner, more maintainable way to define tasks. We strongly recommend using this approach to define tasks in your CrewAI projects.

After creating your CrewAI project as outlined in the [Installation](/en/installation) section, navigate to the `src/latest_ai_development/config/tasks.yaml` file and modify the template to match your specific task requirements.

<Note>
  Variables in your YAML files (like `{topic}`) will be replaced with values from your inputs when running the crew:
```

Example 2 (unknown):
```unknown
</Note>

Here's an example of how to configure tasks using YAML:
```

Example 3 (unknown):
```unknown
To use this YAML configuration in your code, create a crew class that inherits from `CrewBase`:
```

---

## Task for data integration

**URL:** llms-txt#task-for-data-integration

**Contents:**
- Troubleshooting
  - Common Issues
  - Getting Help

integration_task = Task(
    description="""
    1. Get data from multiple SharePoint lists across different sites
    2. Consolidate information into comprehensive reports
    3. Create new list items with aggregated data
    4. Upload analytical reports to executive document library
    5. Update dashboard lists with key metrics
    """,
    agent=data_integrator,
    expected_output="Data integrated across sites with comprehensive reports and updated dashboards"
)

crew = Crew(
    agents=[data_integrator],
    tasks=[integration_task]
)

**Permission Errors**

* Ensure your Microsoft account has appropriate permissions for SharePoint sites
* Verify that the OAuth connection includes required scopes (Sites.Read.All, Sites.ReadWrite.All)
* Check that you have access to the specific sites and lists you're trying to access

**Site and List ID Issues**

* Verify that site IDs and list IDs are correct and properly formatted
* Ensure that sites and lists exist and are accessible to your account
* Use the get\_sites and get\_site\_lists actions to discover valid IDs

**Field and Schema Issues**

* Ensure field names match exactly with the SharePoint list schema
* Verify that required fields are included when creating or updating list items
* Check that field types and values are compatible with the list column definitions

**File Upload Issues**

* Ensure file paths are properly formatted and don't contain invalid characters
* Verify that you have write permissions to the target document library
* Check that file content is properly encoded for upload

**OData Query Issues**

* Use proper OData syntax for filter, select, expand, and orderby parameters
* Verify that property names used in queries exist in the target resources
* Test simple queries before building complex filter expressions

**Pagination and Performance**

* Use top and skip parameters appropriately for large result sets
* Implement proper pagination for lists with many items
* Consider using select parameters to return only needed properties

**Document Library Operations**

* Ensure you have proper permissions for document library operations
* Verify that drive item IDs are correct when deleting files or folders
* Check that file paths don't conflict with existing content

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with Microsoft SharePoint integration setup or troubleshooting.
</Card>

---

## Task for site administration

**URL:** llms-txt#task-for-site-administration

**Contents:**
  - Automated Content Workflows

admin_task = Task(
    description="""
    1. Get information about all accessible SharePoint sites
    2. Analyze site structure and content organization
    3. Identify sites with low activity or outdated content
    4. Generate recommendations for site optimization
    """,
    agent=site_administrator,
    expected_output="Site analysis completed with optimization recommendations"
)

crew = Crew(
    agents=[site_administrator],
    tasks=[admin_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

workflow_automator = Agent(
    role="Workflow Automator",
    goal="Automate SharePoint content workflows and processes",
    backstory="An AI assistant that automates complex SharePoint workflows and content management processes.",
    apps=['microsoft_sharepoint']
)

**Examples:**

Example 1 (unknown):
```unknown
### Automated Content Workflows
```

---

## Task to analyze and optimize task distribution

**URL:** llms-txt#task-to-analyze-and-optimize-task-distribution

**Contents:**
  - Getting Help

task_analysis = Task(
    description="""
    Search for all tasks assigned to team members in the last 30 days,
    analyze completion patterns, and create optimization recommendations
    """,
    agent=task_analyst,
    expected_output="Task analysis report with optimization recommendations"
)

crew = Crew(
    agents=[task_analyst],
    tasks=[task_analysis]
)

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with ClickUp integration setup or troubleshooting.
</Card>

---

## Task to analyze data and create reports

**URL:** llms-txt#task-to-analyze-data-and-create-reports

**Contents:**
  - Spreadsheet Creation and Management

analysis_task = Task(
    description="""
    1. Retrieve all sales data from the current month's spreadsheet
    2. Analyze the data for trends and patterns
    3. Create a summary report in a new row with key metrics
    """,
    agent=data_analyst,
    expected_output="Sales data analyzed and summary report created with key insights"
)

crew = Crew(
    agents=[data_analyst],
    tasks=[analysis_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

spreadsheet_manager = Agent(
    role="Spreadsheet Manager",
    goal="Create and manage spreadsheets efficiently",
    backstory="An AI assistant that specializes in creating and organizing spreadsheets.",
    apps=['google_sheets']
)

**Examples:**

Example 1 (unknown):
```unknown
### Spreadsheet Creation and Management
```

---

## Task to analyze email patterns

**URL:** llms-txt#task-to-analyze-email-patterns

**Contents:**
  - Thread Management

analysis_task = Task(
    description="""
    Search for all unread emails from the last 7 days,
    categorize them by sender domain,
    and create a summary report of communication patterns
    """,
    agent=email_analyst,
    expected_output="Email analysis report with communication patterns and recommendations"
)

crew = Crew(
    agents=[email_analyst],
    tasks=[analysis_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### Thread Management
```

---

## Task to analyze existing data

**URL:** llms-txt#task-to-analyze-existing-data

**Contents:**
  - Workbook Creation and Structure

analysis_task = Task(
    description="Analyze sales data in existing workbooks and create summary charts and tables",
    agent=data_analyst,
    expected_output="Data analyzed with summary charts and tables created"
)

crew = Crew(
    agents=[data_analyst],
    tasks=[analysis_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

workbook_creator = Agent(
    role="Workbook Creator",
    goal="Create structured Excel workbooks with multiple worksheets and data organization",
    backstory="An AI assistant that creates well-organized Excel workbooks for various business needs.",
    apps=['microsoft_excel']
)

**Examples:**

Example 1 (unknown):
```unknown
### Workbook Creation and Structure
```

---

## Task to analyze project status

**URL:** llms-txt#task-to-analyze-project-status

**Contents:**
  - Automated Issue Management

analysis_task = Task(
    description="""
    1. Get all projects and their issue types
    2. Search for all open issues across projects
    3. Analyze issue distribution by status and assignee
    4. Create a summary report issue with findings
    """,
    agent=project_analyst,
    expected_output="Project analysis completed with summary report created"
)

crew = Crew(
    agents=[project_analyst],
    tasks=[analysis_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

automation_manager = Agent(
    role="Automation Manager",
    goal="Automate issue management and workflow processes",
    backstory="An AI assistant that automates repetitive issue management tasks.",
    apps=['jira']
)

**Examples:**

Example 1 (unknown):
```unknown
### Automated Issue Management
```

---

## Task to automate issue management

**URL:** llms-txt#task-to-automate-issue-management

**Contents:**
  - Advanced Schema-Based Operations

automation_task = Task(
    description="""
    1. Search for all unassigned issues using JQL
    2. Get available assignees for each project
    3. Automatically assign issues based on workload and expertise
    4. Update issue priorities based on age and type
    5. Create weekly sprint planning issues
    """,
    agent=automation_manager,
    expected_output="Issues automatically assigned and sprint planning issues created"
)

crew = Crew(
    agents=[automation_manager],
    tasks=[automation_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

schema_specialist = Agent(
    role="Schema Specialist",
    goal="Handle complex Jira operations using dynamic schemas",
    backstory="An AI assistant that can work with dynamic Jira schemas and custom issue types.",
    apps=['jira']
)

**Examples:**

Example 1 (unknown):
```unknown
### Advanced Schema-Based Operations
```

---

## Task to collect and organize data

**URL:** llms-txt#task-to-collect-and-organize-data

**Contents:**
  - Data Analysis and Reporting

data_collection = Task(
    description="Retrieve current inventory data and add new product entries to the inventory spreadsheet",
    agent=data_collector,
    expected_output="Inventory data retrieved and new products added successfully"
)

crew = Crew(
    agents=[data_collector],
    tasks=[data_collection]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

data_analyst = Agent(
    role="Data Analyst",
    goal="Analyze spreadsheet data and generate insights",
    backstory="An experienced data analyst who extracts insights from spreadsheet data.",
    apps=['google_sheets']
)

**Examples:**

Example 1 (unknown):
```unknown
### Data Analysis and Reporting
```

---

## Task to coordinate availability

**URL:** llms-txt#task-to-coordinate-availability

**Contents:**
  - Automated Scheduling Workflows

availability_task = Task(
    description="""
    1. Get the list of available calendars
    2. Check availability for all calendars next Friday afternoon
    3. Create a team meeting for the first available 2-hour slot
    4. Include Google Meet link and send invitations
    """,
    agent=availability_coordinator,
    expected_output="Team meeting scheduled based on availability with all team members invited"
)

crew = Crew(
    agents=[availability_coordinator],
    tasks=[availability_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

scheduling_automator = Agent(
    role="Scheduling Automator",
    goal="Automate scheduling workflows and calendar management",
    backstory="An AI assistant that automates complex scheduling scenarios and calendar workflows.",
    apps=['google_calendar']
)

**Examples:**

Example 1 (unknown):
```unknown
### Automated Scheduling Workflows
```

---

## Task to coordinate project setup

**URL:** llms-txt#task-to-coordinate-project-setup

**Contents:**
  - Issue Hierarchy and Sub-task Management

project_coordination = Task(
    description="""
    1. Search for engineering teams in Linear
    2. Create a new project for Q2 feature development
    3. Associate the project with relevant teams
    4. Create initial project milestones as issues
    """,
    agent=project_coordinator,
    expected_output="Q2 project created with teams assigned and initial milestones established"
)

crew = Crew(
    agents=[project_coordinator],
    tasks=[project_coordination]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

task_organizer = Agent(
    role="Task Organizer",
    goal="Organize complex issues into manageable sub-tasks",
    backstory="An AI assistant that breaks down complex development work into organized sub-tasks.",
    apps=['linear']
)

**Examples:**

Example 1 (unknown):
```unknown
### Issue Hierarchy and Sub-task Management
```

---

## Task to coordinate team activities

**URL:** llms-txt#task-to-coordinate-team-activities

**Contents:**
  - Collaboration and Communication

coordination_task = Task(
    description="""
    1. List all users in the workspace
    2. Get detailed information for specific team members
    3. Create comments on relevant pages to notify team members about updates
    """,
    agent=team_coordinator,
    expected_output="Team coordination completed with user information gathered and notifications sent"
)

crew = Crew(
    agents=[team_coordinator],
    tasks=[coordination_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

collaboration_facilitator = Agent(
    role="Collaboration Facilitator",
    goal="Facilitate team collaboration through comments and user management",
    backstory="An AI assistant that specializes in team collaboration and communication.",
    apps=['notion']
)

**Examples:**

Example 1 (unknown):
```unknown
### Collaboration and Communication
```

---

## Task to coordinate team communication

**URL:** llms-txt#task-to-coordinate-team-communication

**Contents:**
  - Advanced Messaging with Block Kit

coordination_task = Task(
    description="Send task completion notifications to team members and update project channels",
    agent=communication_manager,
    expected_output="Team notifications sent and project channels updated successfully"
)

crew = Crew(
    agents=[communication_manager],
    tasks=[coordination_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### Advanced Messaging with Block Kit
```

---

## Task to create and assign a task

**URL:** llms-txt#task-to-create-and-assign-a-task

**Contents:**
  - Advanced Project Management

task_management = Task(
    description="Create a task called 'Review quarterly reports' and assign it to the appropriate team member",
    agent=task_manager_agent,
    expected_output="Task created and assigned successfully"
)

crew = Crew(
    agents=[task_manager_agent],
    tasks=[task_management]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

project_coordinator = Agent(
    role="Project Coordinator",
    goal="Coordinate project activities and track progress",
    backstory="An experienced project coordinator who ensures projects run smoothly.",
    apps=['asana']
)

**Examples:**

Example 1 (unknown):
```unknown
### Advanced Project Management
```

---

## Task to create and set up new spreadsheets

**URL:** llms-txt#task-to-create-and-set-up-new-spreadsheets

**Contents:**
  - Automated Data Updates

setup_task = Task(
    description="""
    1. Create a new spreadsheet for quarterly reports
    2. Set up proper headers and structure
    3. Add initial data and formatting
    """,
    agent=spreadsheet_manager,
    expected_output="New quarterly report spreadsheet created and properly structured"
)

crew = Crew(
    agents=[spreadsheet_manager],
    tasks=[setup_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

data_updater = Agent(
    role="Data Updater",
    goal="Automatically update and maintain spreadsheet data",
    backstory="An AI assistant that maintains data accuracy and updates records automatically.",
    apps=['google_sheets']
)

**Examples:**

Example 1 (unknown):
```unknown
### Automated Data Updates
```

---

## Task to create and update contacts

**URL:** llms-txt#task-to-create-and-update-contacts

**Contents:**
  - Contact Group Management

curation_task = Task(
    description="""
    1. Search for existing contacts related to new business partners
    2. Create new contacts for partners not in the system
    3. Update existing contact information with latest details
    4. Organize contacts into appropriate groups
    """,
    agent=contact_curator,
    expected_output="Contact database updated with new partners and organized groups"
)

crew = Crew(
    agents=[contact_curator],
    tasks=[curation_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

group_organizer = Agent(
    role="Contact Group Organizer",
    goal="Organize contacts into meaningful groups and categories",
    backstory="An AI assistant that specializes in contact organization and group management.",
    apps=['google_contacts']
)

**Examples:**

Example 1 (unknown):
```unknown
### Contact Group Management
```

---

## Task to create and update presentations

**URL:** llms-txt#task-to-create-and-update-presentations

**Contents:**
  - Data Integration and Visualization

content_task = Task(
    description="Create a new presentation and add content slides with charts and text",
    agent=content_manager,
    expected_output="Presentation created with updated content and visual elements"
)

crew = Crew(
    agents=[content_manager],
    tasks=[content_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

data_visualizer = Agent(
    role="Data Visualizer",
    goal="Create presentations with data imported from spreadsheets",
    backstory="An AI assistant that specializes in data visualization and presentation integration.",
    apps=['google_slides']
)

**Examples:**

Example 1 (unknown):
```unknown
### Data Integration and Visualization
```

---

## Task to create a contact

**URL:** llms-txt#task-to-create-a-contact

**Contents:**
  - Contact Management

create_contact = Task(
    description="Create a new contact for 'John Doe' with email 'john.doe@example.com'.",
    agent=contact_creator,
    expected_output="Contact created successfully in HubSpot."
)

crew = Crew(
    agents=[contact_creator],
    tasks=[create_contact]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### Contact Management
```

---

## Task to create a meeting

**URL:** llms-txt#task-to-create-a-meeting

**Contents:**
- Troubleshooting
  - Common Issues
  - Getting Help

schedule_meeting_task = Task(
    description="Create a Teams meeting titled 'Weekly Team Sync' scheduled for tomorrow at 10:00 AM lasting for 1 hour (use proper ISO 8601 format with timezone).",
    agent=meeting_scheduler,
    expected_output="Teams meeting created successfully with meeting details."
)

crew = Crew(
    agents=[meeting_scheduler],
    tasks=[schedule_meeting_task]
)

**Authentication Errors**

* Ensure your Microsoft account has the necessary permissions for Teams access.
* Required scopes include: `Team.ReadBasic.All`, `Channel.ReadBasic.All`, `ChannelMessage.Send`, `ChannelMessage.Read.All`, `OnlineMeetings.ReadWrite`, `OnlineMeetings.Read`.
* Verify that the OAuth connection includes all required scopes.

**Team and Channel Access**

* Ensure you are a member of the teams you're trying to access.
* Double-check team IDs and channel IDs for correctness.
* Team and channel IDs can be obtained using the `get_teams` and `get_channels` actions.

**Message Sending Issues**

* Ensure `team_id`, `channel_id`, and `message` are provided for `send_message`.
* Verify that you have permissions to send messages to the specified channel.
* Choose appropriate `content_type` (text or html) based on your message format.

* Ensure `subject`, `startDateTime`, and `endDateTime` are provided.
* Use proper ISO 8601 format with timezone for datetime fields (e.g., '2024-01-20T10:00:00-08:00').
* Verify that the meeting times are in the future.

**Message Retrieval Limitations**

* The `get_messages` action can retrieve a maximum of 50 messages per request.
* Messages are returned in reverse chronological order (newest first).

* For `search_online_meetings_by_join_url`, ensure the join URL is exact and properly formatted.
* The URL should be the complete Teams meeting join URL.

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with Microsoft Teams integration setup or troubleshooting.
</Card>

---

## Task to create a meeting and add a contact

**URL:** llms-txt#task-to-create-a-meeting-and-add-a-contact

**Contents:**
- Troubleshooting
  - Common Issues
  - Getting Help

schedule_task = Task(
    description="Create a calendar event for tomorrow at 2 PM titled 'Team Meeting' with location 'Conference Room A', and create a new contact for 'John Smith' with email 'john.smith@example.com' and job title 'Project Manager'.",
    agent=scheduler,
    expected_output="Calendar event created and new contact added successfully."
)

crew = Crew(
    agents=[scheduler],
    tasks=[schedule_task]
)

**Authentication Errors**

* Ensure your Microsoft account has the necessary permissions for mail, calendar, and contact access.
* Required scopes include: `Mail.Read`, `Mail.Send`, `Calendars.Read`, `Calendars.ReadWrite`, `Contacts.Read`, `Contacts.ReadWrite`.
* Verify that the OAuth connection includes all required scopes.

**Email Sending Issues**

* Ensure `to_recipients`, `subject`, and `body` are provided for `send_email`.
* Check that email addresses are properly formatted.
* Verify that the account has `Mail.Send` permissions.

**Calendar Event Creation**

* Ensure `subject`, `start_datetime`, and `end_datetime` are provided.
* Use proper ISO 8601 format for datetime fields (e.g., '2024-01-20T10:00:00').
* Verify timezone settings if events appear at incorrect times.

**Contact Management**

* For `create_contact`, ensure `displayName` is provided as it's required.
* When providing `emailAddresses`, use the proper object format with `address` and `name` properties.

**Search and Filter Issues**

* Use proper OData syntax for `filter` parameters.
* For date filters, use ISO 8601 format (e.g., "receivedDateTime ge '2024-01-01T00:00:00Z'").

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with Microsoft Outlook integration setup or troubleshooting.
</Card>

---

## Task to create a new release

**URL:** llms-txt#task-to-create-a-new-release

**Contents:**
  - Issue Tracking and Management

release_task = Task(
    description="""
    Create a new release v2.1.0 for the project with:
    - Auto-generated release notes
    - Target the main branch
    - Include a description of new features and bug fixes
    """,
    agent=release_manager,
    expected_output="Release v2.1.0 created successfully with release notes"
)

crew = Crew(
    agents=[release_manager],
    tasks=[release_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

project_coordinator = Agent(
    role="Project Coordinator",
    goal="Track and coordinate project issues and development progress",
    backstory="An AI assistant that helps coordinate development work and track project progress.",
    apps=['github']
)

**Examples:**

Example 1 (unknown):
```unknown
### Issue Tracking and Management
```

---

## Task to create comments on pages

**URL:** llms-txt#task-to-create-comments-on-pages

**Contents:**
  - User Information and Team Management

comment_task = Task(
    description="Create a summary comment on the project status page with key updates",
    agent=comment_manager,
    expected_output="Comment created successfully with project status updates"
)

crew = Crew(
    agents=[comment_manager],
    tasks=[comment_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

team_coordinator = Agent(
    role="Team Coordinator",
    goal="Coordinate team activities and manage user information",
    backstory="An AI assistant that helps coordinate team activities and manages user information.",
    apps=['notion']
)

**Examples:**

Example 1 (unknown):
```unknown
### User Information and Team Management
```

---

## Task to create data-driven presentations

**URL:** llms-txt#task-to-create-data-driven-presentations

**Contents:**
  - Presentation Library Management

visualization_task = Task(
    description="""
    1. Create a new presentation for monthly sales report
    2. Import data from the sales spreadsheet
    3. Create charts and visualizations from the imported data
    4. Generate thumbnails for slide previews
    """,
    agent=data_visualizer,
    expected_output="Data-driven presentation created with imported spreadsheet data and visualizations"
)

crew = Crew(
    agents=[data_visualizer],
    tasks=[visualization_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

library_manager = Agent(
    role="Presentation Library Manager",
    goal="Manage and organize presentation libraries",
    backstory="An AI assistant that manages presentation collections and file organization.",
    apps=['google_slides']
)

**Examples:**

Example 1 (unknown):
```unknown
### Presentation Library Management
```

---

## Task to create issue hierarchy

**URL:** llms-txt#task-to-create-issue-hierarchy

**Contents:**
  - Automated Development Workflow

hierarchy_task = Task(
    description="""
    1. Search for large feature issues that need to be broken down
    2. For each complex issue, create sub-issues for different components
    3. Update the parent issues with proper descriptions and links to sub-issues
    4. Assign sub-issues to appropriate team members based on expertise
    """,
    agent=task_organizer,
    expected_output="Complex issues broken down into manageable sub-tasks with proper assignments"
)

crew = Crew(
    agents=[task_organizer],
    tasks=[hierarchy_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

workflow_automator = Agent(
    role="Workflow Automator",
    goal="Automate development workflow processes in Linear",
    backstory="An AI assistant that automates repetitive development workflow tasks.",
    apps=['linear']
)

**Examples:**

Example 1 (unknown):
```unknown
### Automated Development Workflow
```

---

## Task to create structured workbooks

**URL:** llms-txt#task-to-create-structured-workbooks

**Contents:**
  - Data Manipulation and Updates

creation_task = Task(
    description="""
    1. Create a new quarterly report workbook
    2. Add multiple worksheets for different departments
    3. Create tables with headers for data organization
    4. Set up charts for key metrics visualization
    """,
    agent=workbook_creator,
    expected_output="Structured workbook created with multiple worksheets, tables, and charts"
)

crew = Crew(
    agents=[workbook_creator],
    tasks=[creation_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

data_manipulator = Agent(
    role="Data Manipulator",
    goal="Update and manipulate data in Excel worksheets efficiently",
    backstory="An AI assistant that handles data updates, table management, and range operations.",
    apps=['microsoft_excel']
)

**Examples:**

Example 1 (unknown):
```unknown
### Data Manipulation and Updates
```

---

## Task to create templates

**URL:** llms-txt#task-to-create-templates

**Contents:**
- Troubleshooting
  - Common Issues
  - Getting Help

template_task = Task(
    description="""
    1. Create blank presentation templates for different use cases
    2. Add standard layouts and content placeholders
    3. Create sample presentations with best practices
    4. Generate thumbnails for template previews
    5. Upload template assets to Drive and link appropriately
    """,
    agent=template_creator,
    expected_output="Presentation templates created with standardized layouts and linked assets"
)

crew = Crew(
    agents=[template_creator],
    tasks=[template_task]
)

**Permission Errors**

* Ensure your Google account has appropriate permissions for Google Slides
* Verify that the OAuth connection includes required scopes for presentations, spreadsheets, and drive access
* Check that presentations are shared with the authenticated account

**Presentation ID Issues**

* Verify that presentation IDs are correct and presentations exist
* Ensure you have access permissions to the presentations you're trying to modify
* Check that presentation IDs are properly formatted

**Content Update Issues**

* Ensure batch update requests are properly formatted according to Google Slides API specifications
* Verify that object IDs for slides and elements exist in the presentation
* Check that write control revision IDs are current if using optimistic concurrency

**Data Import Issues**

* Verify that Google Sheet IDs are correct and accessible
* Ensure data ranges are properly specified using A1 notation
* Check that you have read permissions for the source spreadsheets

**File Upload and Linking Issues**

* Ensure file data is properly encoded for upload
* Verify that Drive file IDs are correct when linking files
* Check that you have appropriate Drive permissions for file operations

**Page and Thumbnail Operations**

* Verify that page object IDs exist in the specified presentation
* Ensure presentations have content before attempting to generate thumbnails
* Check that page structure is valid for thumbnail generation

**Pagination and Listing Issues**

* Use appropriate page sizes for listing presentations
* Implement proper pagination using page tokens for large result sets
* Handle empty result sets gracefully

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with Google Slides integration setup or troubleshooting.
</Card>

---

## Task to edit document content

**URL:** llms-txt#task-to-edit-document-content

**Contents:**
  - Advanced Document Operations

edit_content_task = Task(
    description="In document 'your_document_id', insert the text 'Executive Summary: ' at the beginning, then replace all instances of 'TODO' with 'COMPLETED'.",
    agent=text_editor,
    expected_output="Document updated with new text inserted and TODO items replaced."
)

crew = Crew(
    agents=[text_editor],
    tasks=[edit_content_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### Advanced Document Operations
```

---

## Task to facilitate collaboration

**URL:** llms-txt#task-to-facilitate-collaboration

**Contents:**
  - Automated Team Communication

collaboration_task = Task(
    description="""
    1. Identify active users in the workspace
    2. Create contextual comments on project pages to facilitate discussions
    3. Provide status updates and feedback through comments
    """,
    agent=collaboration_facilitator,
    expected_output="Collaboration facilitated with comments created and team members notified"
)

crew = Crew(
    agents=[collaboration_facilitator],
    tasks=[collaboration_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

communication_automator = Agent(
    role="Communication Automator",
    goal="Automate team communication and user management workflows",
    backstory="An AI assistant that automates communication workflows and manages user interactions.",
    apps=['notion']
)

**Examples:**

Example 1 (unknown):
```unknown
### Automated Team Communication
```

---

## Task to format document

**URL:** llms-txt#task-to-format-document

**Contents:**
- Troubleshooting
  - Common Issues
  - Getting Help

format_doc_task = Task(
    description="In document 'your_document_id', insert a page break at position 100, create a named range called 'Introduction' for characters 1-50, and apply batch formatting updates.",
    agent=document_formatter,
    expected_output="Document formatted with page break, named range, and styling applied."
)

crew = Crew(
    agents=[document_formatter],
    tasks=[format_doc_task]
)

**Authentication Errors**

* Ensure your Google account has the necessary permissions for Google Docs access.
* Verify that the OAuth connection includes all required scopes (`https://www.googleapis.com/auth/documents`).

**Document ID Issues**

* Double-check document IDs for correctness.
* Ensure the document exists and is accessible to your account.
* Document IDs can be found in the Google Docs URL.

**Text Insertion and Range Operations**

* When using `insert_text` or `delete_content_range`, ensure index positions are valid.
* Remember that Google Docs uses zero-based indexing.
* The document must have content at the specified index positions.

**Batch Update Request Formatting**

* When using `batch_update`, ensure the `requests` array is correctly formatted according to the Google Docs API documentation.
* Complex updates require specific JSON structures for each request type.

**Replace Text Operations**

* For `replace_text`, ensure the `containsText` parameter exactly matches the text you want to replace.
* Use `matchCase` parameter to control case sensitivity.

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with Google Docs integration setup or troubleshooting.
</Card>

---

## Task to list and read documents

**URL:** llms-txt#task-to-list-and-read-documents

**Contents:**
  - Document Cleanup and Organization

read_docs_task = Task(
    description="List all Word documents in my OneDrive, then get the content and properties of the first document found.",
    agent=document_reader,
    expected_output="List of documents with content and properties of the first document."
)

crew = Crew(
    agents=[document_reader],
    tasks=[read_docs_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### Document Cleanup and Organization
```

---

## Task to manage billing operations

**URL:** llms-txt#task-to-manage-billing-operations

**Contents:**
  - Subscription Management

billing_task = Task(
    description="Create a new customer and set up their premium subscription plan",
    agent=billing_manager,
    expected_output="Customer created and subscription activated successfully"
)

crew = Crew(
    agents=[billing_manager],
    tasks=[billing_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

subscription_manager = Agent(
    role="Subscription Manager",
    goal="Manage customer subscriptions and optimize recurring revenue",
    backstory="An AI assistant that specializes in subscription lifecycle management and customer retention.",
    apps=['stripe']
)

**Examples:**

Example 1 (unknown):
```unknown
### Subscription Management
```

---

## Task to manage contacts

**URL:** llms-txt#task-to-manage-contacts

**Contents:**
  - Getting Help

contact_task = Task(
    description="Create a new contact for 'Jane Smith' at 'Global Tech Inc.' with email 'jane.smith@globaltech.com'.",
    agent=crm_manager,
    expected_output="Contact database updated with the new contact."
)

crew = Crew(
    agents=[crm_manager],
    tasks=[contact_task]
)

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with HubSpot integration setup or troubleshooting.
</Card>

---

## Task to manage customer accounts

**URL:** llms-txt#task-to-manage-customer-accounts

**Contents:**
  - Advanced SOQL Queries and Reporting

account_task = Task(
    description="""
    1. Create a new account for TechCorp Inc.
    2. Add John Doe as the primary contact for this account
    3. Create a follow-up task for next week to check on their project status
    """,
    agent=account_manager,
    expected_output="Account, contact, and follow-up task created successfully"
)

crew = Crew(
    agents=[account_manager],
    tasks=[account_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

data_analyst = Agent(
    role="Sales Data Analyst",
    goal="Generate insights from Salesforce data using SOQL queries",
    backstory="An analytical AI that excels at extracting meaningful insights from CRM data.",
    apps=['salesforce']
)

**Examples:**

Example 1 (unknown):
```unknown
### Advanced SOQL Queries and Reporting
```

---

## Task to manage documents

**URL:** llms-txt#task-to-manage-documents

**Contents:**
  - Site Administration and Analysis

document_task = Task(
    description="""
    1. Get all files from the main document library
    2. Upload new policy documents to the appropriate folders
    3. Organize files by department and date
    4. Remove outdated documents
    """,
    agent=document_manager,
    expected_output="Document library organized with new files uploaded and outdated files removed"
)

crew = Crew(
    agents=[document_manager],
    tasks=[document_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

site_administrator = Agent(
    role="Site Administrator",
    goal="Administer and analyze SharePoint sites",
    backstory="An AI assistant that handles site administration and provides insights on site usage.",
    apps=['microsoft_sharepoint']
)

**Examples:**

Example 1 (unknown):
```unknown
### Site Administration and Analysis
```

---

## Task to manage event updates

**URL:** llms-txt#task-to-manage-event-updates

**Contents:**
  - Availability and Calendar Management

event_management = Task(
    description="""
    1. List all events for this week
    2. Update any events that need location changes to include video conference links
    3. Check availability for upcoming meetings
    """,
    agent=event_manager,
    expected_output="Weekly events updated with proper locations and availability checked"
)

crew = Crew(
    agents=[event_manager],
    tasks=[event_management]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

availability_coordinator = Agent(
    role="Availability Coordinator",
    goal="Coordinate availability and manage calendars for scheduling",
    backstory="An AI assistant that specializes in availability management and calendar coordination.",
    apps=['google_calendar']
)

**Examples:**

Example 1 (unknown):
```unknown
### Availability and Calendar Management
```

---

## Task to manage issue workflow

**URL:** llms-txt#task-to-manage-issue-workflow

**Contents:**
  - Project and Team Management

issue_workflow = Task(
    description="Create a feature request issue and update the status of related issues to reflect current progress",
    agent=issue_manager,
    expected_output="Feature request created and related issues updated"
)

crew = Crew(
    agents=[issue_manager],
    tasks=[issue_workflow]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

project_coordinator = Agent(
    role="Project Coordinator",
    goal="Coordinate projects and teams in Linear efficiently",
    backstory="An experienced project coordinator who manages development cycles and team workflows.",
    apps=['linear']
)

**Examples:**

Example 1 (unknown):
```unknown
### Project and Team Management
```

---

## Task to manage list data

**URL:** llms-txt#task-to-manage-list-data

**Contents:**
  - Document Library Management

list_management_task = Task(
    description="Get all lists from the project site, review items, and update status for completed tasks",
    agent=list_manager,
    expected_output="SharePoint lists reviewed and task statuses updated"
)

crew = Crew(
    agents=[list_manager],
    tasks=[list_management_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

document_manager = Agent(
    role="Document Manager",
    goal="Manage SharePoint document libraries and files",
    backstory="An AI assistant that specializes in document organization and file management.",
    apps=['microsoft_sharepoint']
)

**Examples:**

Example 1 (unknown):
```unknown
### Document Library Management
```

---

## Task to manage presentation library

**URL:** llms-txt#task-to-manage-presentation-library

**Contents:**
  - Automated Presentation Workflows

library_task = Task(
    description="""
    1. List all existing presentations
    2. Generate thumbnails for presentation previews
    3. Upload supporting files to Drive and link to presentations
    4. Organize presentations by topic and date
    """,
    agent=library_manager,
    expected_output="Presentation library organized with thumbnails and linked supporting files"
)

crew = Crew(
    agents=[library_manager],
    tasks=[library_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

presentation_automator = Agent(
    role="Presentation Automator",
    goal="Automate presentation creation and management workflows",
    backstory="An AI assistant that automates complex presentation workflows and content generation.",
    apps=['google_slides']
)

**Examples:**

Example 1 (unknown):
```unknown
### Automated Presentation Workflows
```

---

## Task to manage product catalog

**URL:** llms-txt#task-to-manage-product-catalog

**Contents:**
  - Order and Customer Analytics

catalog_task = Task(
    description="""
    1. Create a new product "Premium Coffee Mug" from Coffee Co vendor
    2. Add high-quality product images and descriptions
    3. Search for similar products from the same vendor
    4. Update product tags and pricing strategy
    """,
    agent=product_manager,
    expected_output="Product created and catalog optimized successfully"
)

crew = Crew(
    agents=[product_manager],
    tasks=[catalog_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

analytics_agent = Agent(
    role="E-commerce Analyst",
    goal="Analyze customer behavior and order patterns to optimize store performance",
    backstory="An analytical AI that excels at extracting insights from e-commerce data.",
    apps=['shopify']
)

**Examples:**

Example 1 (unknown):
```unknown
### Order and Customer Analytics
```

---

## Task to manage sales pipeline

**URL:** llms-txt#task-to-manage-sales-pipeline

**Contents:**
  - Contact and Account Management

pipeline_task = Task(
    description="Create a qualified lead and convert it to an opportunity with $50,000 value",
    agent=sales_manager,
    expected_output="Lead created and opportunity established successfully"
)

crew = Crew(
    agents=[sales_manager],
    tasks=[pipeline_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

account_manager = Agent(
    role="Account Manager",
    goal="Manage customer accounts and maintain strong relationships",
    backstory="An AI assistant that specializes in account management and customer relationship building.",
    apps=['salesforce']
)

**Examples:**

Example 1 (unknown):
```unknown
### Contact and Account Management
```

---

## Task to manage store operations

**URL:** llms-txt#task-to-manage-store-operations

**Contents:**
  - Product Management with GraphQL

store_task = Task(
    description="Create a new customer and process their order for 2 Premium Coffee Mugs",
    agent=store_manager,
    expected_output="Customer created and order processed successfully"
)

crew = Crew(
    agents=[store_manager],
    tasks=[store_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

product_manager = Agent(
    role="Product Manager",
    goal="Manage product catalog and inventory with advanced GraphQL capabilities",
    backstory="An AI assistant that specializes in product management and catalog optimization.",
    apps=['shopify']
)

**Examples:**

Example 1 (unknown):
```unknown
### Product Management with GraphQL
```

---

## Task to manage subscription operations

**URL:** llms-txt#task-to-manage-subscription-operations

**Contents:**
  - Financial Analytics and Reporting

subscription_task = Task(
    description="""
    1. Create a new product "Premium Service Plan" with advanced features
    2. Set up subscription plans with different tiers
    3. Create customers and assign them to appropriate plans
    4. Monitor subscription status and handle billing issues
    """,
    agent=subscription_manager,
    expected_output="Subscription management system configured with customers and active plans"
)

crew = Crew(
    agents=[subscription_manager],
    tasks=[subscription_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

financial_analyst = Agent(
    role="Financial Analyst",
    goal="Analyze payment data and generate financial insights",
    backstory="An analytical AI that excels at extracting insights from payment and subscription data.",
    apps=['stripe']
)

**Examples:**

Example 1 (unknown):
```unknown
### Financial Analytics and Reporting
```

---

## Task to manage support workflow

**URL:** llms-txt#task-to-manage-support-workflow

**Contents:**
  - Advanced Ticket Management

support_task = Task(
    description="Create a ticket for login issues, add troubleshooting comments, and update status to resolved",
    agent=support_agent,
    expected_output="Support ticket managed through complete resolution workflow"
)

crew = Crew(
    agents=[support_agent],
    tasks=[support_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

ticket_manager = Agent(
    role="Ticket Manager",
    goal="Manage support ticket workflows and ensure timely resolution",
    backstory="An AI assistant that specializes in support ticket triage and workflow optimization.",
    apps=['zendesk']
)

**Examples:**

Example 1 (unknown):
```unknown
### Advanced Ticket Management
```

---

## Task to manage task workflow

**URL:** llms-txt#task-to-manage-task-workflow

**Contents:**
  - Advanced Project Management

task_workflow = Task(
    description="Create a task for project planning and assign it to the development team",
    agent=task_coordinator,
    expected_output="Task created and assigned successfully"
)

crew = Crew(
    agents=[task_coordinator],
    tasks=[task_workflow]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

project_manager = Agent(
    role="Project Manager",
    goal="Coordinate project activities and track team productivity",
    backstory="An experienced project manager who ensures projects are delivered on time.",
    apps=['clickup']
)

**Examples:**

Example 1 (unknown):
```unknown
### Advanced Project Management
```

---

## Task to manage ticket lifecycle

**URL:** llms-txt#task-to-manage-ticket-lifecycle

**Contents:**
  - Support Analytics and Reporting

ticket_workflow = Task(
    description="""
    1. Create a new support ticket for account access issues
    2. Add internal notes with troubleshooting steps
    3. Update ticket priority based on customer tier
    4. Add resolution comments and close the ticket
    """,
    agent=ticket_manager,
    expected_output="Complete ticket lifecycle managed from creation to resolution"
)

crew = Crew(
    agents=[ticket_manager],
    tasks=[ticket_workflow]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

support_analyst = Agent(
    role="Support Analyst",
    goal="Analyze support metrics and generate insights for team performance",
    backstory="An analytical AI that excels at extracting insights from support data and ticket patterns.",
    apps=['zendesk']
)

**Examples:**

Example 1 (unknown):
```unknown
### Support Analytics and Reporting
```

---

## Task to manipulate data

**URL:** llms-txt#task-to-manipulate-data

**Contents:**
  - Advanced Excel Automation

manipulation_task = Task(
    description="""
    1. Get data from existing worksheets
    2. Update specific ranges with new information
    3. Add new rows to existing tables
    4. Create additional charts based on updated data
    5. Organize data across multiple worksheets
    """,
    agent=data_manipulator,
    expected_output="Data updated across worksheets with new charts and organized structure"
)

crew = Crew(
    agents=[data_manipulator],
    tasks=[manipulation_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

excel_automator = Agent(
    role="Excel Automator",
    goal="Automate complex Excel workflows and data processing",
    backstory="An AI assistant that automates sophisticated Excel operations and data workflows.",
    apps=['microsoft_excel']
)

**Examples:**

Example 1 (unknown):
```unknown
### Advanced Excel Automation
```

---

## Task to organize and share files

**URL:** llms-txt#task-to-organize-and-share-files

**Contents:**
- Troubleshooting
  - Common Issues
  - Getting Help

organize_share_task = Task(
    description="Search for files containing 'presentation' in the name, create a folder called 'Presentations', move the found files to this folder, and create a view-only sharing link for the folder.",
    agent=file_organizer,
    expected_output="Files organized into 'Presentations' folder and sharing link created."
)

crew = Crew(
    agents=[file_organizer],
    tasks=[organize_share_task]
)

**Authentication Errors**

* Ensure your Microsoft account has the necessary permissions for file access (e.g., `Files.Read`, `Files.ReadWrite`).
* Verify that the OAuth connection includes all required scopes.

**File Upload Issues**

* Ensure `file_name` and `content` are provided for file uploads.
* Content must be Base64 encoded for binary files.
* Check that you have write permissions to OneDrive.

**File/Folder ID Issues**

* Double-check item IDs for correctness when accessing specific files or folders.
* Item IDs are returned by other operations like `list_files` or `search_files`.
* Ensure the referenced items exist and are accessible.

**Search and Filter Operations**

* Use appropriate search terms for `search_files` operations.
* For `filter` parameters, use proper OData syntax.

**File Operations (Copy/Move)**

* For `move_item`, ensure both `item_id` and `parent_id` are provided.
* For `copy_item`, only `item_id` is required; `parent_id` defaults to root if not specified.
* Verify that destination folders exist and are accessible.

**Sharing Link Creation**

* Ensure the item exists before creating sharing links.
* Choose appropriate `type` and `scope` based on your sharing requirements.
* `anonymous` scope allows access without sign-in; `organization` requires organizational account.

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with Microsoft OneDrive integration setup or troubleshooting.
</Card>

---

## Task to organize contact groups

**URL:** llms-txt#task-to-organize-contact-groups

**Contents:**
  - Comprehensive Contact Management

organization_task = Task(
    description="""
    1. List all existing contact groups
    2. Analyze contact distribution across groups
    3. Create new groups for better organization
    4. Move contacts to appropriate groups based on their information
    """,
    agent=group_organizer,
    expected_output="Contacts organized into logical groups with improved structure"
)

crew = Crew(
    agents=[group_organizer],
    tasks=[organization_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

contact_specialist = Agent(
    role="Contact Management Specialist",
    goal="Provide comprehensive contact management across all sources",
    backstory="An AI assistant that handles all aspects of contact management including personal, directory, and other contacts.",
    apps=['google_contacts']
)

**Examples:**

Example 1 (unknown):
```unknown
### Comprehensive Contact Management
```

---

## Task to organize documents

**URL:** llms-txt#task-to-organize-documents

**Contents:**
- Troubleshooting
  - Common Issues
  - Getting Help

organize_task = Task(
    description="List all documents, check their properties, and identify any documents that might be duplicates or outdated for potential cleanup.",
    agent=document_organizer,
    expected_output="Analysis of document library with recommendations for organization."
)

crew = Crew(
    agents=[document_organizer],
    tasks=[organize_task]
)

**Authentication Errors**

* Ensure your Microsoft account has the necessary permissions for file access (e.g., `Files.Read.All`, `Files.ReadWrite.All`).
* Verify that the OAuth connection includes all required scopes.

**File Creation Issues**

* When creating text documents, ensure the `file_name` ends with `.txt` extension.
* Verify that you have write permissions to the target location (OneDrive/SharePoint).

**Document Access Issues**

* Double-check document IDs for correctness when accessing specific documents.
* Ensure the referenced documents exist and are accessible.
* Note that this integration works best with text files (.txt) for content operations.

**Content Retrieval Limitations**

* The `get_document_content` action works best with text files (.txt).
* For complex Word documents (.docx), consider using the document properties action to get metadata.

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with Microsoft Word integration setup or troubleshooting.
</Card>

---

## Task to organize email threads

**URL:** llms-txt#task-to-organize-email-threads

**Contents:**
  - Getting Help

thread_task = Task(
    description="""
    1. Fetch all threads from the last month
    2. Apply appropriate labels to organize threads by project
    3. Archive or trash threads that are no longer relevant
    """,
    agent=thread_manager,
    expected_output="Email threads organized with appropriate labels and cleanup completed"
)

crew = Crew(
    agents=[thread_manager],
    tasks=[thread_task]
)

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with Gmail integration setup or troubleshooting.
</Card>

---

## Task to prepare and send emails

**URL:** llms-txt#task-to-prepare-and-send-emails

**Contents:**
  - Email Search and Analysis

email_coordination = Task(
    description="Search for emails from the marketing team, create a summary draft, and send it to stakeholders",
    agent=email_coordinator,
    expected_output="Summary email sent to stakeholders"
)

crew = Crew(
    agents=[email_coordinator],
    tasks=[email_coordination]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### Email Search and Analysis
```

---

## Task to schedule a meeting with availability check

**URL:** llms-txt#task-to-schedule-a-meeting-with-availability-check

**Contents:**
  - Event Management and Updates

schedule_meeting = Task(
    description="Check availability for next week and schedule a project review meeting with stakeholders",
    agent=meeting_coordinator,
    expected_output="Meeting scheduled after checking availability of all participants"
)

crew = Crew(
    agents=[meeting_coordinator],
    tasks=[schedule_meeting]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

event_manager = Agent(
    role="Event Manager",
    goal="Manage and update calendar events efficiently",
    backstory="An experienced event manager who handles event logistics and updates.",
    apps=['google_calendar']
)

**Examples:**

Example 1 (unknown):
```unknown
### Event Management and Updates
```

---

## Task to search and manage directory

**URL:** llms-txt#task-to-search-and-manage-directory

**Contents:**
  - Contact Creation and Updates

directory_task = Task(
    description="Search for team members in the company directory and create a team contact list",
    agent=directory_manager,
    expected_output="Team directory compiled with contact information"
)

crew = Crew(
    agents=[directory_manager],
    tasks=[directory_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

contact_curator = Agent(
    role="Contact Curator",
    goal="Create and update contact information systematically",
    backstory="An AI assistant that maintains accurate and up-to-date contact information.",
    apps=['google_contacts']
)

**Examples:**

Example 1 (unknown):
```unknown
### Contact Creation and Updates
```

---

## Task to search and retrieve emails

**URL:** llms-txt#task-to-search-and-retrieve-emails

**Contents:**
  - Calendar and Contact Management

search_emails_task = Task(
    description="Get the latest 20 unread emails and provide a summary of the most important ones.",
    agent=email_manager,
    expected_output="Summary of the most important unread emails with key details."
)

crew = Crew(
    agents=[email_manager],
    tasks=[search_emails_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### Calendar and Contact Management
```

---

## Task to send a message and retrieve recent messages

**URL:** llms-txt#task-to-send-a-message-and-retrieve-recent-messages

**Contents:**
  - Meeting Management

messaging_task = Task(
    description="Send a message 'Hello team! This is an automated update from our AI assistant.' to the General channel of team 'your_team_id', then retrieve the last 10 messages from that channel.",
    agent=messenger,
    expected_output="Message sent successfully and recent messages retrieved."
)

crew = Crew(
    agents=[messenger],
    tasks=[messaging_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### Meeting Management
```

---

## Task to send rich notifications

**URL:** llms-txt#task-to-send-rich-notifications

**Contents:**
  - Message Search and Analytics

notification_task = Task(
    description="""
    1. Send a formatted project completion message to #general with progress charts
    2. Send direct messages to team leads with task summaries
    3. Create interactive notification with action buttons for team feedback
    """,
    agent=notification_agent,
    expected_output="Rich notifications sent with interactive elements and formatted content"
)

crew = Crew(
    agents=[notification_agent],
    tasks=[notification_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### Message Search and Analytics
```

---

## Task to update data based on conditions

**URL:** llms-txt#task-to-update-data-based-on-conditions

**Contents:**
  - Complex Data Management Workflow

update_task = Task(
    description="""
    1. Get spreadsheet properties and structure
    2. Read current data from specific ranges
    3. Update values in target ranges with new data
    4. Append new records to the bottom of the sheet
    """,
    agent=data_updater,
    expected_output="Spreadsheet data updated successfully with new values and records"
)

crew = Crew(
    agents=[data_updater],
    tasks=[update_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

workflow_manager = Agent(
    role="Data Workflow Manager",
    goal="Manage complex data workflows across multiple spreadsheets",
    backstory="An AI assistant that orchestrates complex data operations across multiple spreadsheets.",
    apps=['google_sheets']
)

**Examples:**

Example 1 (unknown):
```unknown
### Complex Data Management Workflow
```

---

## Task to upload and manage a file

**URL:** llms-txt#task-to-upload-and-manage-a-file

**Contents:**
  - File Organization and Sharing

file_management_task = Task(
    description="Upload a text file named 'report.txt' with content 'This is a sample report for the project.' Then get information about the uploaded file.",
    agent=file_operator,
    expected_output="File uploaded successfully and file information retrieved."
)

crew = Crew(
    agents=[file_operator],
    tasks=[file_management_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### File Organization and Sharing
```

---

## Task to upload and share documents

**URL:** llms-txt#task-to-upload-and-share-documents

**Contents:**
  - Advanced File Management

document_task = Task(
    description="Upload the quarterly report and share it with the finance team",
    agent=file_manager_agent,
    expected_output="Document uploaded and sharing permissions configured"
)

crew = Crew(
    agents=[file_manager_agent],
    tasks=[document_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

file_organizer = Agent(
    role="File Organizer",
    goal="Maintain organized file structure and manage permissions",
    backstory="An experienced file manager who ensures proper organization and access control.",
    apps=['google_drive']
)

**Examples:**

Example 1 (unknown):
```unknown
### Advanced File Management
```

---

## Task using schema-based operations

**URL:** llms-txt#task-using-schema-based-operations

**Contents:**
- Troubleshooting
  - Common Issues
  - Getting Help

schema_task = Task(
    description="""
    1. Get all projects and their custom issue types
    2. For each custom issue type, describe the action schema
    3. Create issues using the dynamic schema for complex custom fields
    4. Update issues with custom field values based on business rules
    """,
    agent=schema_specialist,
    expected_output="Custom issues created and updated using dynamic schemas"
)

crew = Crew(
    agents=[schema_specialist],
    tasks=[schema_task]
)

**Permission Errors**

* Ensure your Jira account has necessary permissions for the target projects
* Verify that the OAuth connection includes required scopes for Jira API
* Check if you have create/edit permissions for issues in the specified projects

**Invalid Project or Issue Keys**

* Double-check project keys and issue keys for correct format (e.g., "PROJ-123")
* Ensure projects exist and are accessible to your account
* Verify that issue keys reference existing issues

**Issue Type and Status Issues**

* Use JIRA\_GET\_ISSUE\_TYPES\_BY\_PROJECT to get valid issue types for a project
* Use JIRA\_GET\_ISSUE\_STATUS\_BY\_PROJECT to get valid statuses
* Ensure issue types and statuses are available in the target project

**JQL Query Problems**

* Test JQL queries in Jira's issue search before using in API calls
* Ensure field names in JQL are spelled correctly and exist in your Jira instance
* Use proper JQL syntax for complex queries

**Custom Fields and Schema Issues**

* Use JIRA\_DESCRIBE\_ACTION\_SCHEMA to get the correct schema for complex issue types
* Ensure custom field IDs are correct (e.g., "customfield\_10001")
* Verify that custom fields are available in the target project and issue type

**Filter Formula Issues**

* Ensure filter formulas follow the correct JSON structure for disjunctive normal form
* Use valid field names that exist in your Jira configuration
* Test simple filters before building complex multi-condition queries

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with Jira integration setup or troubleshooting.
</Card>

---

## Tavily Extractor Tool

**URL:** llms-txt#tavily-extractor-tool

**Contents:**
- Installation
- Example Usage

Source: https://docs.crewai.com/en/tools/search-research/tavilyextractortool

Extract structured content from web pages using the Tavily API

The `TavilyExtractorTool` allows CrewAI agents to extract structured content from web pages using the Tavily API. It can process single URLs or lists of URLs and provides options for controlling the extraction depth and including images.

To use the `TavilyExtractorTool`, you need to install the `tavily-python` library:

You also need to set your Tavily API key as an environment variable:

Here's how to initialize and use the `TavilyExtractorTool` within a CrewAI agent:

```python theme={null}
import os
from crewai import Agent, Task, Crew
from crewai_tools import TavilyExtractorTool

**Examples:**

Example 1 (unknown):
```unknown
You also need to set your Tavily API key as an environment variable:
```

Example 2 (unknown):
```unknown
## Example Usage

Here's how to initialize and use the `TavilyExtractorTool` within a CrewAI agent:
```

---

## Tavily Search Tool

**URL:** llms-txt#tavily-search-tool

**Contents:**
- Installation
- Environment Variables
- Example Usage

Source: https://docs.crewai.com/en/tools/search-research/tavilysearchtool

Perform comprehensive web searches using the Tavily Search API

The `TavilySearchTool` provides an interface to the Tavily Search API, enabling CrewAI agents to perform comprehensive web searches. It allows for specifying search depth, topics, time ranges, included/excluded domains, and whether to include direct answers, raw content, or images in the results.

To use the `TavilySearchTool`, you need to install the `tavily-python` library:

## Environment Variables

Ensure your Tavily API key is set as an environment variable:

Get an API key at [https://app.tavily.com/](https://app.tavily.com/) (sign up, then create a key).

Here's how to initialize and use the `TavilySearchTool` within a CrewAI agent:

```python theme={null}
import os
from crewai import Agent, Task, Crew
from crewai_tools import TavilySearchTool

**Examples:**

Example 1 (unknown):
```unknown
## Environment Variables

Ensure your Tavily API key is set as an environment variable:
```

Example 2 (unknown):
```unknown
Get an API key at [https://app.tavily.com/](https://app.tavily.com/) (sign up, then create a key).

## Example Usage

Here's how to initialize and use the `TavilySearchTool` within a CrewAI agent:
```

---

## Test agent knowledge retrieval

**URL:** llms-txt#test-agent-knowledge-retrieval

if hasattr(agent, 'knowledge') and agent.knowledge:
    test_query = ["test query"]
    results = agent.knowledge.query(test_query)
    print(f"Agent knowledge results: {len(results)} documents found")
    
    # Test crew knowledge retrieval (if exists)
    if hasattr(crew, 'knowledge') and crew.knowledge:
        crew_results = crew.query_knowledge(test_query)
        print(f"Crew knowledge results: {len(crew_results)} documents found")
python theme={null}
import chromadb
from crewai.utilities.paths import db_storage_path
import os

**Examples:**

Example 1 (unknown):
```unknown
#### Inspect Knowledge Collections
```

---

## The agent is loaded with all its predefined configurations

**URL:** llms-txt#the-agent-is-loaded-with-all-its-predefined-configurations

**Contents:**
  - Overriding Repository Settings
  - Example: Creating a Crew with Repository Agents

researcher = Agent(
    from_repository="market-research-agent"
)
python theme={null}
researcher = Agent(
    from_repository="market-research-agent",
    goal="Research the latest trends in AI development",  # Override the repository goal
    verbose=True  # Add a setting not in the repository
)
python theme={null}
from crewai import Crew, Agent, Task

**Examples:**

Example 1 (unknown):
```unknown
### Overriding Repository Settings

You can override specific settings from the repository by providing them in the configuration:
```

Example 2 (unknown):
```unknown
### Example: Creating a Crew with Repository Agents
```

---

## the agent learns about during its execution

**URL:** llms-txt#the-agent-learns-about-during-its-execution

tool = TXTSearchTool()

---

## The agent will use these defaults

**URL:** llms-txt#the-agent-will-use-these-defaults

**Contents:**
- Features
- Response Format

agent_with_custom_tool = Agent(
    role="Advanced Researcher",
    goal="Conduct detailed research with comprehensive results",
    tools=[custom_tavily_tool]
)
```

* **Comprehensive Search**: Access to Tavily's powerful search index
* **Configurable Depth**: Choose between basic and advanced search modes
* **Topic Filtering**: Focus searches on general, news, or finance topics
* **Time Range Control**: Limit results to specific time periods
* **Domain Control**: Include or exclude specific domains
* **Direct Answers**: Get synthesized answers from search results
* **Content Filtering**: Prevent context window issues with automatic content truncation

The tool returns search results as a JSON string containing:

* Search results with titles, URLs, and content snippets
* Optional direct answers to queries
* Optional image results
* Optional raw HTML content (when enabled)

Content for each result is automatically truncated to prevent context window issues while maintaining the most relevant information.

---

## The agent will use the tool with parameters like:

**URL:** llms-txt#the-agent-will-use-the-tool-with-parameters-like:

---

## This ensures consistency but may not match your LLM provider preference

**URL:** llms-txt#this-ensures-consistency-but-may-not-match-your-llm-provider-preference

knowledge_source = StringKnowledgeSource(content="Research data...")

crew = Crew(
    agents=[agent],
    tasks=[...],
    knowledge_sources=[knowledge_source]
    # Default: Uses OpenAI embeddings even with Claude LLM
)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
#### Customizing Knowledge Embedding Providers
```

---

## This setup allows the agent to only search the given CSV file.

**URL:** llms-txt#this-setup-allows-the-agent-to-only-search-the-given-csv-file.

tool = CSVSearchTool(csv='path/to/your/csvfile.csv')

---

## Tools

**URL:** llms-txt#tools

**Contents:**
- Overview
- What is a Tool?
- Key Characteristics of Tools
- Using CrewAI Tools

Source: https://docs.crewai.com/en/concepts/tools

Understanding and leveraging tools within the CrewAI framework for agent collaboration and task execution.

CrewAI tools empower agents with capabilities ranging from web searching and data analysis to collaboration and delegating tasks among coworkers.
This documentation outlines how to create, integrate, and leverage these tools within the CrewAI framework, including a new focus on collaboration tools.

A tool in CrewAI is a skill or function that agents can utilize to perform various actions.
This includes tools from the [CrewAI Toolkit](https://github.com/joaomdmoura/crewai-tools) and [LangChain Tools](https://python.langchain.com/docs/integrations/tools),
enabling everything from simple searches to complex interactions and effective teamwork among agents.

<Note type="info" title="Enterprise Enhancement: Tools Repository">
  CrewAI AOP provides a comprehensive Tools Repository with pre-built integrations for common business systems and APIs. Deploy agents with enterprise tools in minutes instead of days.

The Enterprise Tools Repository includes:

* Pre-built connectors for popular enterprise systems
  * Custom tool creation interface
  * Version control and sharing capabilities
  * Security and compliance features
</Note>

## Key Characteristics of Tools

* **Utility**: Crafted for tasks such as web searching, data analysis, content generation, and agent collaboration.
* **Integration**: Boosts agent capabilities by seamlessly integrating tools into their workflow.
* **Customizability**: Provides the flexibility to develop custom tools or utilize existing ones, catering to the specific needs of agents.
* **Error Handling**: Incorporates robust error handling mechanisms to ensure smooth operation.
* **Caching Mechanism**: Features intelligent caching to optimize performance and reduce redundant operations.
* **Asynchronous Support**: Handles both synchronous and asynchronous tools, enabling non-blocking operations.

## Using CrewAI Tools

To enhance your agents' capabilities with crewAI tools, begin by installing our extra tools package:

Here's an example demonstrating their use:

```python Code theme={null}
import os
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
Here's an example demonstrating their use:
```

---

## Tools & Integrations

**URL:** llms-txt#tools-&-integrations

**Contents:**
- Overview
- Explore
- Related

Source: https://docs.crewai.com/en/enterprise/features/tools-and-integrations

Connect external apps and manage internal tools your agents can use.

Tools & Integrations is the central hub for connecting third‑party apps and managing internal tools that your agents can use at runtime.

<Frame>
  <img alt="Tools & Integrations Overview" />
</Frame>

<Tabs>
  <Tab title="Integrations" icon="plug">
    ## Agent Apps (Integrations)

Connect enterprise‑grade applications (e.g., Gmail, Google Drive, HubSpot, Slack) via OAuth to enable agent actions.

<Steps>
      <Step title="Connect">
        Click <b>Connect</b> on an app and complete OAuth.
      </Step>

<Step title="Configure">
        Optionally adjust scopes, triggers, and action availability.
      </Step>

<Step title="Use in Agents">
        Connected services become available as tools for your agents.
      </Step>
    </Steps>

<Frame>
      <img alt="Integrations Grid" />
    </Frame>

### Connect your Account

1. Go to <Link href="https://app.crewai.com/crewai_plus/connectors">Integrations</Link>
    2. Click <b>Connect</b> on the desired service
    3. Complete the OAuth flow and grant scopes
    4. Copy your Enterprise Token from <Link href="https://app.crewai.com/crewai_plus/settings/integrations">Integration Settings</Link>

<Frame>
      <img alt="Enterprise Token" />
    </Frame>

### Install Integration Tools

To use the integrations locally, you need to install the latest `crewai-tools` package.

### Environment Variable Setup

<Note>
      To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
    </Note>

Or add it to your `.env` file:

<Tip>
      Use the new streamlined approach to integrate enterprise apps. Simply specify the app and its actions directly in the Agent configuration.
    </Tip>

On a deployed crew, you can specify which actions are available for each integration from the service settings page.

<Frame>
      <img alt="Filter Actions" />
    </Frame>

### Scoped Deployments (multi‑user orgs)

You can scope each integration to a specific user. For example, a crew that connects to Google can use a specific user’s Gmail account.

<Tip>
      Useful when different teams/users must keep data access separated.
    </Tip>

Use the `user_bearer_token` to scope authentication to the requesting user. If the user isn’t logged in, the crew won’t use connected integrations. Otherwise it falls back to the default bearer token configured for the deployment.

<Frame>
      <img alt="User Bearer Token" />
    </Frame>

#### Communication & Collaboration

* Gmail — Manage emails and drafts
    * Slack — Workspace notifications and alerts
    * Microsoft — Office 365 and Teams integration

#### Project Management

* Jira — Issue tracking and project management
    * ClickUp — Task and productivity management
    * Asana — Team task and project coordination
    * Notion — Page and database management
    * Linear — Software project and bug tracking
    * GitHub — Repository and issue management

#### Customer Relationship Management

* Salesforce — CRM account and opportunity management
    * HubSpot — Sales pipeline and contact management
    * Zendesk — Customer support ticket management

#### Business & Finance

* Stripe — Payment processing and customer management
    * Shopify — E‑commerce store and product management

#### Productivity & Storage

* Google Sheets — Spreadsheet data synchronization
    * Google Calendar — Event and schedule management
    * Box — File storage and document management

…and more to come!
  </Tab>

<Tab title="Internal Tools" icon="toolbox">
    ## Internal Tools

Create custom tools locally, publish them on CrewAI AOP Tool Repository and use them in your agents.

<Tip>
      Before running the commands below, make sure you log in to your CrewAI AOP account by running this command:

<Frame>
      <img alt="Internal Tool Detail" />
    </Frame>

<Steps>
      <Step title="Create">
        Create a new tool locally.

<Step title="Publish">
        Publish the tool to the CrewAI AOP Tool Repository.

<Step title="Install">
        Install the tool from the CrewAI AOP Tool Repository.

* Name and description
    * Visibility (Private / Public)
    * Required environment variables
    * Version history and downloads
    * Team and role access

<Frame>
      <img alt="Internal Tool Detail" />
    </Frame>
  </Tab>
</Tabs>

<CardGroup>
  <Card title="Tool Repository" href="/en/enterprise/guides/tool-repository#tool-repository" icon="toolbox">
    Create, publish, and version custom tools for your organization.
  </Card>

<Card title="Webhook Automation" href="/en/enterprise/guides/webhook-automation" icon="bolt">
    Automate workflows and integrate with external platforms and services.
  </Card>
</CardGroup>

**Examples:**

Example 1 (unknown):
```unknown
### Environment Variable Setup

    <Note>
      To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
    </Note>
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

Example 3 (unknown):
```unknown
### Usage Example

    <Tip>
      Use the new streamlined approach to integrate enterprise apps. Simply specify the app and its actions directly in the Agent configuration.
    </Tip>
```

Example 4 (unknown):
```unknown
### Filtering Tools
```

---

## Tools Overview

**URL:** llms-txt#tools-overview

**Contents:**
- **Tool Categories**
- **Quick Access**
- **Getting Started**

Source: https://docs.crewai.com/en/tools/overview

Discover CrewAI's extensive library of 40+ tools to supercharge your AI agents

CrewAI provides an extensive library of pre-built tools to enhance your agents' capabilities. From file processing to web scraping, database queries to AI services - we've got you covered.

## **Tool Categories**

<CardGroup>
  <Card title="File & Document" icon="folder-open" href="/en/tools/file-document/overview">
    Read, write, and search through various file formats including PDF, DOCX, JSON, CSV, and more. Perfect for document processing workflows.
  </Card>

<Card title="Web Scraping & Browsing" icon="globe" href="/en/tools/web-scraping/overview">
    Extract data from websites, automate browser interactions, and scrape content at scale with tools like Firecrawl, Selenium, and more.
  </Card>

<Card title="Search & Research" icon="magnifying-glass" href="/en/tools/search-research/overview">
    Perform web searches, find code repositories, research YouTube content, and discover information across the internet.
  </Card>

<Card title="Database & Data" icon="database" href="/en/tools/database-data/overview">
    Connect to SQL databases, vector stores, and data warehouses. Query MySQL, PostgreSQL, Snowflake, Qdrant, and Weaviate.
  </Card>

<Card title="AI & Machine Learning" icon="brain" href="/en/tools/ai-ml/overview">
    Generate images with DALL-E, process vision tasks, integrate with LangChain, build RAG systems, and leverage code interpreters.
  </Card>

<Card title="Cloud & Storage" icon="cloud" href="/en/tools/cloud-storage/overview">
    Interact with cloud services including AWS S3, Amazon Bedrock, and other cloud storage and AI services.
  </Card>

<Card title="Automation" icon="bolt" href="/en/tools/automation/overview">
    Automate workflows with Apify, Composio, and other platforms to connect your agents with external services.
  </Card>

<Card title="Integrations" icon="plug" href="/en/tools/tool-integrations/overview">
    Integrate CrewAI with external systems like Amazon Bedrock and the CrewAI Automation toolkit.
  </Card>
</CardGroup>

Need a specific tool? Here are some popular choices:

<CardGroup>
  <Card title="RAG Tool" icon="image" href="/en/tools/ai-ml/ragtool">
    Implement Retrieval-Augmented Generation
  </Card>

<Card title="Serper Dev" icon="book-atlas" href="/en/tools/search-research/serperdevtool">
    Google search API
  </Card>

<Card title="File Read" icon="file" href="/en/tools/file-document/filereadtool">
    Read any file type
  </Card>

<Card title="Scrape Website" icon="globe" href="/en/tools/web-scraping/scrapewebsitetool">
    Extract web content
  </Card>

<Card title="Code Interpreter" icon="code" href="/en/tools/ai-ml/codeinterpretertool">
    Execute Python code
  </Card>

<Card title="S3 Reader" icon="cloud" href="/en/tools/cloud-storage/s3readertool">
    Access AWS S3 files
  </Card>
</CardGroup>

## **Getting Started**

To use any tool in your CrewAI project:

1. **Import** the tool in your crew configuration
2. **Add** it to your agent's tools list
3. **Configure** any required API keys or settings

```python theme={null}
from crewai_tools import FileReadTool, SerperDevTool

---

## to perform a semantic search for a specified query from a text's content across the internet

**URL:** llms-txt#to-perform-a-semantic-search-for-a-specified-query-from-a-text's-content-across-the-internet

**Contents:**
- Referring to Other Tasks

search_tool = SerperDevTool()

task = Task(
  description='Find and summarize the latest AI news',
  expected_output='A bullet list summary of the top 5 most important AI news',
  agent=research_agent,
  tools=[search_tool]
)

crew = Crew(
    agents=[research_agent],
    tasks=[task],
    verbose=True
)

result = crew.kickoff()
print(result)
python Code theme={null}

**Examples:**

Example 1 (unknown):
```unknown
This demonstrates how tasks with specific tools can override an agent's default set for tailored task execution.

## Referring to Other Tasks

In CrewAI, the output of one task is automatically relayed into the next one, but you can specifically define what tasks' output, including multiple, should be used as context for another task.

This is useful when you have a task that depends on the output of another task that is not performed immediately after it. This is done through the `context` attribute of the task:
```

---

## Training

**URL:** llms-txt#training

**Contents:**
- Overview
  - Training Your Crew Using the CLI
  - Training your Crew programmatically
- How trained data is used by agents
  - Training data flow
  - During training runs
  - After training completes
  - File summary
- Small Language Model Considerations
  - Limitations of Small Models in Training Evaluation

Source: https://docs.crewai.com/en/concepts/training

Learn how to train your CrewAI agents by giving them feedback early on and get consistent results.

The training feature in CrewAI allows you to train your AI agents using the command-line interface (CLI).
By running the command `crewai train -n <n_iterations>`, you can specify the number of iterations for the training process.

During training, CrewAI utilizes techniques to optimize the performance of your agents along with human feedback.
This helps the agents improve their understanding, decision-making, and problem-solving abilities.

### Training Your Crew Using the CLI

To use the training feature, follow these steps:

1. Open your terminal or command prompt.
2. Navigate to the directory where your CrewAI project is located.
3. Run the following command:

<Tip>
  Replace `<n_iterations>` with the desired number of training iterations and `<filename>` with the appropriate filename ending with `.pkl`.
</Tip>

<Note>
  If you omit `-f`, the output defaults to `trained_agents_data.pkl` in the current working directory. You can pass an absolute path to control where the file is written.
</Note>

### Training your Crew programmatically

To train your crew programmatically, use the following steps:

1. Define the number of iterations for training.
2. Specify the input parameters for the training process.
3. Execute the training command within a try-except block to handle potential errors.

## How trained data is used by agents

CrewAI uses the training artifacts in two ways: during training to incorporate your human feedback, and after training to guide agents with consolidated suggestions.

### Training data flow

### During training runs

* On each iteration, the system records for every agent:
  * `initial_output`: the agent’s first answer
  * `human_feedback`: your inline feedback when prompted
  * `improved_output`: the agent’s follow-up answer after feedback
* This data is stored in a working file named `training_data.pkl` keyed by the agent’s internal ID and iteration.
* While training is active, the agent automatically appends your prior human feedback to its prompt to enforce those instructions on subsequent attempts within the training session.
  Training is interactive: tasks set `human_input = true`, so running in a non-interactive environment will block on user input.

### After training completes

* When `train(...)` finishes, CrewAI evaluates the collected training data per agent and produces a consolidated result containing:
  * `suggestions`: clear, actionable instructions distilled from your feedback and the difference between initial/improved outputs
  * `quality`: a 0–10 score capturing improvement
  * `final_summary`: a step-by-step set of action items for future tasks
* These consolidated results are saved to the filename you pass to `train(...)` (default via CLI is `trained_agents_data.pkl`). Entries are keyed by the agent’s `role` so they can be applied across sessions.
* During normal (non-training) execution, each agent automatically loads its consolidated `suggestions` and appends them to the task prompt as mandatory instructions. This gives you consistent improvements without changing your agent definitions.

* `training_data.pkl` (ephemeral, per-session):
  * Structure: `agent_id -> { iteration_number: { initial_output, human_feedback, improved_output } }`
  * Purpose: capture raw data and human feedback during training
  * Location: saved in the current working directory (CWD)
* `trained_agents_data.pkl` (or your custom filename):
  * Structure: `agent_role -> { suggestions: string[], quality: number, final_summary: string }`
  * Purpose: persist consolidated guidance for future runs
  * Location: written to the CWD by default; use `-f` to set a custom (including absolute) path

## Small Language Model Considerations

<Warning>
  When using smaller language models (≤7B parameters) for training data evaluation, be aware that they may face challenges with generating structured outputs and following complex instructions.
</Warning>

### Limitations of Small Models in Training Evaluation

<CardGroup>
  <Card title="JSON Output Accuracy" icon="triangle-exclamation">
    Smaller models often struggle with producing valid JSON responses needed for structured training evaluations, leading to parsing errors and incomplete data.
  </Card>

<Card title="Evaluation Quality" icon="chart-line">
    Models under 7B parameters may provide less nuanced evaluations with limited reasoning depth compared to larger models.
  </Card>

<Card title="Instruction Following" icon="list-check">
    Complex training evaluation criteria may not be fully followed or considered by smaller models.
  </Card>

<Card title="Consistency" icon="rotate">
    Evaluations across multiple training iterations may lack consistency with smaller models.
  </Card>
</CardGroup>

### Recommendations for Training

<Tabs>
  <Tab title="Best Practice">
    For optimal training quality and reliable evaluations, we strongly recommend using models with at least 7B parameters or larger:

<Tip>
      More powerful models provide higher quality feedback with better reasoning, leading to more effective training iterations.
    </Tip>
  </Tab>

<Tab title="Small Model Usage">
    If you must use smaller models for training evaluation, be aware of these constraints:

<Warning>
      While CrewAI includes optimizations for small models, expect less reliable and less nuanced evaluation results that may require more human intervention during training.
    </Warning>
  </Tab>
</Tabs>

### Key Points to Note

* **Positive Integer Requirement:** Ensure that the number of iterations (`n_iterations`) is a positive integer. The code will raise a `ValueError` if this condition is not met.
* **Filename Requirement:** Ensure that the filename ends with `.pkl`. The code will raise a `ValueError` if this condition is not met.
* **Error Handling:** The code handles subprocess errors and unexpected exceptions, providing error messages to the user.
* Trained guidance is applied at prompt time; it does not modify your Python/YAML agent configuration.
* Agents automatically load trained suggestions from a file named `trained_agents_data.pkl` located in the current working directory. If you trained to a different filename, either rename it to `trained_agents_data.pkl` before running, or adjust the loader in code.
* You can change the output filename when calling `crewai train` with `-f/--filename`. Absolute paths are supported if you want to save outside the CWD.

It is important to note that the training process may take some time, depending on the complexity of your agents and will also require your feedback on each iteration.

Once the training is complete, your agents will be equipped with enhanced capabilities and knowledge, ready to tackle complex tasks and provide more consistent and valuable insights.

Remember to regularly update and retrain your agents to ensure they stay up-to-date with the latest information and advancements in the field.

**Examples:**

Example 1 (unknown):
```unknown
<Tip>
  Replace `<n_iterations>` with the desired number of training iterations and `<filename>` with the appropriate filename ending with `.pkl`.
</Tip>

<Note>
  If you omit `-f`, the output defaults to `trained_agents_data.pkl` in the current working directory. You can pass an absolute path to control where the file is written.
</Note>

### Training your Crew programmatically

To train your crew programmatically, use the following steps:

1. Define the number of iterations for training.
2. Specify the input parameters for the training process.
3. Execute the training command within a try-except block to handle potential errors.
```

Example 2 (unknown):
```unknown
## How trained data is used by agents

CrewAI uses the training artifacts in two ways: during training to incorporate your human feedback, and after training to guide agents with consolidated suggestions.

### Training data flow
```

Example 3 (unknown):
```unknown
### During training runs

* On each iteration, the system records for every agent:
  * `initial_output`: the agent’s first answer
  * `human_feedback`: your inline feedback when prompted
  * `improved_output`: the agent’s follow-up answer after feedback
* This data is stored in a working file named `training_data.pkl` keyed by the agent’s internal ID and iteration.
* While training is active, the agent automatically appends your prior human feedback to its prompt to enforce those instructions on subsequent attempts within the training session.
  Training is interactive: tasks set `human_input = true`, so running in a non-interactive environment will block on user input.

### After training completes

* When `train(...)` finishes, CrewAI evaluates the collected training data per agent and produces a consolidated result containing:
  * `suggestions`: clear, actionable instructions distilled from your feedback and the difference between initial/improved outputs
  * `quality`: a 0–10 score capturing improvement
  * `final_summary`: a step-by-step set of action items for future tasks
* These consolidated results are saved to the filename you pass to `train(...)` (default via CLI is `trained_agents_data.pkl`). Entries are keyed by the agent’s `role` so they can be applied across sessions.
* During normal (non-training) execution, each agent automatically loads its consolidated `suggestions` and appends them to the task prompt as mandatory instructions. This gives you consistent improvements without changing your agent definitions.

### File summary

* `training_data.pkl` (ephemeral, per-session):
  * Structure: `agent_id -> { iteration_number: { initial_output, human_feedback, improved_output } }`
  * Purpose: capture raw data and human feedback during training
  * Location: saved in the current working directory (CWD)
* `trained_agents_data.pkl` (or your custom filename):
  * Structure: `agent_role -> { suggestions: string[], quality: number, final_summary: string }`
  * Purpose: persist consolidated guidance for future runs
  * Location: written to the CWD by default; use `-f` to set a custom (including absolute) path

## Small Language Model Considerations

<Warning>
  When using smaller language models (≤7B parameters) for training data evaluation, be aware that they may face challenges with generating structured outputs and following complex instructions.
</Warning>

### Limitations of Small Models in Training Evaluation

<CardGroup>
  <Card title="JSON Output Accuracy" icon="triangle-exclamation">
    Smaller models often struggle with producing valid JSON responses needed for structured training evaluations, leading to parsing errors and incomplete data.
  </Card>

  <Card title="Evaluation Quality" icon="chart-line">
    Models under 7B parameters may provide less nuanced evaluations with limited reasoning depth compared to larger models.
  </Card>

  <Card title="Instruction Following" icon="list-check">
    Complex training evaluation criteria may not be fully followed or considered by smaller models.
  </Card>

  <Card title="Consistency" icon="rotate">
    Evaluations across multiple training iterations may lack consistency with smaller models.
  </Card>
</CardGroup>

### Recommendations for Training

<Tabs>
  <Tab title="Best Practice">
    For optimal training quality and reliable evaluations, we strongly recommend using models with at least 7B parameters or larger:
```

Example 4 (unknown):
```unknown
<Tip>
      More powerful models provide higher quality feedback with better reasoning, leading to more effective training iterations.
    </Tip>
  </Tab>

  <Tab title="Small Model Usage">
    If you must use smaller models for training evaluation, be aware of these constraints:
```

---

## Use custom storage

**URL:** llms-txt#use-custom-storage

**Contents:**
- 🧠 Memory System Comparison
- Supported Embedding Providers
  - OpenAI (Default)
  - Ollama
  - Google AI
  - Azure OpenAI
  - Vertex AI
- Security Best Practices
  - Environment Variables

external_memory = ExternalMemory(storage=CustomStorage())

crew = Crew(
    agents=[...],
    tasks=[...],
    external_memory=external_memory
)
python theme={null}
crew = Crew(
    memory=True,
    embedder={
        "provider": "openai",
        "config": {"model": "text-embedding-3-small"}
    }
)
python theme={null}
crew = Crew(
    memory=True,
    embedder={
        "provider": "ollama",
        "config": {"model": "mxbai-embed-large"}
    }
)
python theme={null}
crew = Crew(
    memory=True,
    embedder={
        "provider": "google-generativeai",
        "config": {
            "api_key": "your-api-key",
            "model_name": "gemini-embedding-001"
        }
    }
)
python theme={null}
crew = Crew(
    memory=True,
    embedder={
        "provider": "openai",
        "config": {
            "api_key": "your-api-key",
            "api_base": "https://your-resource.openai.azure.com/",
            "api_version": "2023-05-15",
            "model_name": "text-embedding-3-small"
        }
    }
)
python theme={null}
crew = Crew(
    memory=True,
    embedder={
        "provider": "vertexai",
        "config": {
            "project_id": "your-project-id",
            "region": "your-region",
            "api_key": "your-api-key",
            "model_name": "textembedding-gecko"
        }
    }
)
python theme={null}
import os
from crewai import Crew

**Examples:**

Example 1 (unknown):
```unknown
## 🧠 Memory System Comparison

| **Category**        | **Feature**           | **Basic Memory**       | **External Memory**        |
| ------------------- | --------------------- | ---------------------- | -------------------------- |
| **Ease of Use**     | Setup Complexity      | Simple                 | Moderate                   |
|                     | Integration           | Built-in (contextual)  | Standalone                 |
| **Persistence**     | Storage               | Local files            | Custom / Mem0              |
|                     | Cross-session Support | ✅                      | ✅                          |
| **Personalization** | User-specific Memory  | ❌                      | ✅                          |
|                     | Custom Providers      | Limited                | Any provider               |
| **Use Case Fit**    | Recommended For       | Most general use cases | Specialized / custom needs |

## Supported Embedding Providers

### OpenAI (Default)
```

Example 2 (unknown):
```unknown
### Ollama
```

Example 3 (unknown):
```unknown
### Google AI
```

Example 4 (unknown):
```unknown
### Azure OpenAI
```

---

## Use kickoff() to interact directly with the agent

**URL:** llms-txt#use-kickoff()-to-interact-directly-with-the-agent

result = researcher.kickoff("What are the latest developments in language models?")

---

## Use the custom manager in your crew

**URL:** llms-txt#use-the-custom-manager-in-your-crew

**Contents:**
  - Workflow in Action
- Conclusion

project_crew = Crew(
    tasks=[...],
    agents=[researcher, writer],
    manager_agent=manager,  # Use your custom manager agent
    process=Process.hierarchical,
    planning=True,
)
```

<Tip>
  For more details on creating and customizing a manager agent, check out the [Custom Manager Agent documentation](/en/learn/custom-manager-agent).
</Tip>

### Workflow in Action

1. **Task Assignment**: The manager assigns tasks strategically, considering each agent's capabilities and available tools.
2. **Execution and Review**: Agents complete their tasks with the option for asynchronous execution and callback functions for streamlined workflows.
3. **Sequential Task Progression**: Despite being a hierarchical process, tasks follow a logical order for smooth progression, facilitated by the manager's oversight.

Adopting the hierarchical process in CrewAI, with the correct configurations and understanding of the system's capabilities, facilitates an organized and efficient approach to project management.
Utilize the advanced features and customizations to tailor the workflow to your specific needs, ensuring optimal task execution and project success.

---

## Use this LLM configuration with your agents

**URL:** llms-txt#use-this-llm-configuration-with-your-agents

**Contents:**
  - 3. Prompting in CrewAI
  - 4. Guardrails for Safe Crews

python theme={null}
    from crewai import Agent, LLM
    from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL, Portkey

# Initialize Portkey admin client
    portkey_admin = Portkey(api_key="YOUR_PORTKEY_API_KEY")

# Retrieve prompt using the render API
    prompt_data = portkey_client.prompts.render(
        prompt_id="YOUR_PROMPT_ID",
        variables={
            "agent_role": "Senior Research Scientist",
        }
    )

backstory_agent_prompt=prompt_data.data.messages[0]["content"]

# Set up LLM with Portkey integration
    portkey_llm = LLM(
        model="gpt-4o",
        base_url=PORTKEY_GATEWAY_URL,
        api_key="dummy",
        extra_headers=createHeaders(
            api_key="YOUR_PORTKEY_API_KEY",
            virtual_key="YOUR_OPENAI_VIRTUAL_KEY"
        )
    )

# Create agent using the rendered prompt
    researcher = Agent(
        role="Senior Research Scientist",
        goal="Discover groundbreaking insights about the assigned topic",
        backstory=backstory_agent,  # Use the rendered prompt
        verbose=True,
        llm=portkey_llm
    )
    python theme={null}
    # Use a specific prompt version
    prompt_data = portkey_admin.prompts.render(
        prompt_id="YOUR_PROMPT_ID@version_number",
        variables={
            "agent_role": "Senior Research Scientist",
            "agent_goal": "Discover groundbreaking insights"
        }
    )
    
    You are a {{agent_role}} with expertise in {{domain}}.

Your mission is to {{agent_goal}} by leveraging your knowledge
    and experience in the field.

Always maintain a {{tone}} tone and focus on providing {{focus_area}}.
    python theme={null}
    prompt_data = portkey_admin.prompts.render(
        prompt_id="YOUR_PROMPT_ID",
        variables={
            "agent_role": "Senior Research Scientist",
            "domain": "artificial intelligence",
            "agent_goal": "discover groundbreaking insights",
            "tone": "professional",
            "focus_area": "practical applications"
        }
    )
    python theme={null}
from crewai import Agent, LLM
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL

**Examples:**

Example 1 (unknown):
```unknown
This configuration will automatically try Claude if the GPT-4o request fails, ensuring your crew can continue operating.

<CardGroup>
  <Card title="Automatic Retries" icon="rotate" href="https://portkey.ai/docs/product/ai-gateway/automatic-retries">
    Handles temporary failures automatically. If an LLM call fails, Portkey will retry the same request for the specified number of times - perfect for rate limits or network blips.
  </Card>

  <Card title="Request Timeouts" icon="clock" href="https://portkey.ai/docs/product/ai-gateway/request-timeouts">
    Prevent your agents from hanging. Set timeouts to ensure you get responses (or can fail gracefully) within your required timeframes.
  </Card>

  <Card title="Conditional Routing" icon="route" href="https://portkey.ai/docs/product/ai-gateway/conditional-routing">
    Send different requests to different providers. Route complex reasoning to GPT-4, creative tasks to Claude, and quick responses to Gemini based on your needs.
  </Card>

  <Card title="Fallbacks" icon="shield" href="https://portkey.ai/docs/product/ai-gateway/fallbacks">
    Keep running even if your primary provider fails. Automatically switch to backup providers to maintain availability.
  </Card>

  <Card title="Load Balancing" icon="scale-balanced" href="https://portkey.ai/docs/product/ai-gateway/load-balancing">
    Spread requests across multiple API keys or providers. Great for high-volume crew operations and staying within rate limits.
  </Card>
</CardGroup>

### 3. Prompting in CrewAI

Portkey's Prompt Engineering Studio helps you create, manage, and optimize the prompts used in your CrewAI agents. Instead of hardcoding prompts or instructions, use Portkey's prompt rendering API to dynamically fetch and apply your versioned prompts.

<Frame>
  ![Prompt Playground Interface](https://raw.githubusercontent.com/siddharthsambharia-portkey/Portkey-Product-Images/refs/heads/main/CrewAI%20Portkey%20Docs.webp)
</Frame>

<Tabs>
  <Tab title="Prompt Playground">
    Prompt Playground is a place to compare, test and deploy perfect prompts for your AI application. It's where you experiment with different models, test variables, compare outputs, and refine your prompt engineering strategy before deploying to production. It allows you to:

    1. Iteratively develop prompts before using them in your agents
    2. Test prompts with different variables and models
    3. Compare outputs between different prompt versions
    4. Collaborate with team members on prompt development

    This visual environment makes it easier to craft effective prompts for each step in your CrewAI agents' workflow.
  </Tab>

  <Tab title="Using Prompt Templates">
    The Prompt Render API retrieves your prompt templates with all parameters configured:
```

Example 2 (unknown):
```unknown
</Tab>

  <Tab title="Prompt Versioning">
    You can:

    * Create multiple versions of the same prompt
    * Compare performance between versions
    * Roll back to previous versions if needed
    * Specify which version to use in your code:
```

Example 3 (unknown):
```unknown
</Tab>

  <Tab title="Mustache Templating for variables">
    Portkey prompts use Mustache-style templating for easy variable substitution:
```

Example 4 (unknown):
```unknown
When rendering, simply pass the variables:
```

---

## Use with an agent

**URL:** llms-txt#use-with-an-agent

agent = Agent(
    role="Research Assistant",
    goal="Find and analyze information",
    backstory="You are a research assistant.",
    llm=custom_llm
)

---

## Using Annotations in crew.py

**URL:** llms-txt#using-annotations-in-crew.py

**Contents:**
- Introduction
- Available Annotations
- Usage Examples
  - 1. Crew Base Class
  - 2. Tool Definition
  - 3. LLM Definition
  - 4. Agent Definition
  - 5. Task Definition
  - 6. Crew Creation
- YAML Configuration

Source: https://docs.crewai.com/en/learn/using-annotations

Learn how to use annotations to properly structure agents, tasks, and components in CrewAI

This guide explains how to use annotations to properly reference **agents**, **tasks**, and other components in the `crew.py` file.

Annotations in the CrewAI framework are used to decorate classes and methods, providing metadata and functionality to various components of your crew. These annotations help in organizing and structuring your code, making it more readable and maintainable.

## Available Annotations

The CrewAI framework provides the following annotations:

* `@CrewBase`: Used to decorate the main crew class.
* `@agent`: Decorates methods that define and return Agent objects.
* `@task`: Decorates methods that define and return Task objects.
* `@crew`: Decorates the method that creates and returns the Crew object.
* `@llm`: Decorates methods that initialize and return Language Model objects.
* `@tool`: Decorates methods that initialize and return Tool objects.
* `@callback`: Used for defining callback methods.
* `@output_json`: Used for methods that output JSON data.
* `@output_pydantic`: Used for methods that output Pydantic models.
* `@cache_handler`: Used for defining cache handling methods.

Let's go through examples of how to use these annotations:

### 1. Crew Base Class

The `@CrewBase` annotation is used to decorate the main crew class. This class typically contains configurations and methods for creating agents, tasks, and the crew itself.

<Tip>
  `@CrewBase` does more than register the class:

* **Configuration bootstrapping:** looks for `agents_config` and `tasks_config` (defaulting to `config/agents.yaml` and `config/tasks.yaml`) beside the class file, loads them at instantiation, and safely falls back to empty dicts if files are missing.
  * **Decorator orchestration:** keeps memoized references to every method marked with `@agent`, `@task`, `@before_kickoff`, or `@after_kickoff` so they are instantiated once per crew and executed in declaration order.
  * **Hook wiring:** automatically attaches the preserved kickoff hooks to the `Crew` object returned by the `@crew` method, making them run before and after `.kickoff()`.
  * **MCP integration:** when the class defines `mcp_server_params`, `get_mcp_tools()` lazily starts an MCP server adapter, hydrates the declared tools, and an internal after-kickoff hook stops the adapter. See [MCP overview](/en/mcp/overview) for adapter configuration details.
</Tip>

### 2. Tool Definition

The `@tool` annotation is used to decorate methods that return tool objects. These tools can be used by agents to perform specific tasks.

### 3. LLM Definition

The `@llm` annotation is used to decorate methods that initialize and return Language Model objects. These LLMs are used by agents for natural language processing tasks.

### 4. Agent Definition

The `@agent` annotation is used to decorate methods that define and return Agent objects.

### 5. Task Definition

The `@task` annotation is used to decorate methods that define and return Task objects. These methods specify the task configuration and the agent responsible for the task.

The `@crew` annotation is used to decorate the method that creates and returns the `Crew` object. This method assembles all the components (agents and tasks) into a functional crew.

## YAML Configuration

The agent configurations are typically stored in a YAML file. Here's an example of how the `agents.yaml` file might look for the researcher agent:

This YAML configuration corresponds to the researcher agent defined in the `LinkedinProfileCrew` class. The configuration specifies the agent's role, goal, backstory, and other properties such as the LLM and tools it uses.

Note how the `llm` and `tools` in the YAML file correspond to the methods decorated with `@llm` and `@tool` in the Python class.

* **Consistent Naming**: Use clear and consistent naming conventions for your methods. For example, agent methods could be named after their roles (e.g., researcher, reporting\_analyst).
* **Environment Variables**: Use environment variables for sensitive information like API keys.
* **Flexibility**: Design your crew to be flexible by allowing easy addition or removal of agents and tasks.
* **YAML-Code Correspondence**: Ensure that the names and structures in your YAML files correspond correctly to the decorated methods in your Python code.

By following these guidelines and properly using annotations, you can create well-structured and maintainable crews using the CrewAI framework.

**Examples:**

Example 1 (unknown):
```unknown
The `@CrewBase` annotation is used to decorate the main crew class. This class typically contains configurations and methods for creating agents, tasks, and the crew itself.

<Tip>
  `@CrewBase` does more than register the class:

  * **Configuration bootstrapping:** looks for `agents_config` and `tasks_config` (defaulting to `config/agents.yaml` and `config/tasks.yaml`) beside the class file, loads them at instantiation, and safely falls back to empty dicts if files are missing.
  * **Decorator orchestration:** keeps memoized references to every method marked with `@agent`, `@task`, `@before_kickoff`, or `@after_kickoff` so they are instantiated once per crew and executed in declaration order.
  * **Hook wiring:** automatically attaches the preserved kickoff hooks to the `Crew` object returned by the `@crew` method, making them run before and after `.kickoff()`.
  * **MCP integration:** when the class defines `mcp_server_params`, `get_mcp_tools()` lazily starts an MCP server adapter, hydrates the declared tools, and an internal after-kickoff hook stops the adapter. See [MCP overview](/en/mcp/overview) for adapter configuration details.
</Tip>

### 2. Tool Definition
```

Example 2 (unknown):
```unknown
The `@tool` annotation is used to decorate methods that return tool objects. These tools can be used by agents to perform specific tasks.

### 3. LLM Definition
```

Example 3 (unknown):
```unknown
The `@llm` annotation is used to decorate methods that initialize and return Language Model objects. These LLMs are used by agents for natural language processing tasks.

### 4. Agent Definition
```

Example 4 (unknown):
```unknown
The `@agent` annotation is used to decorate methods that define and return Agent objects.

### 5. Task Definition
```

---

## Using Multimodal Agents

**URL:** llms-txt#using-multimodal-agents

**Contents:**
- Using Multimodal Agents
  - Enabling Multimodal Capabilities
  - Working with Images

Source: https://docs.crewai.com/en/learn/multimodal-agents

Learn how to enable and use multimodal capabilities in your agents for processing images and other non-text content within the CrewAI framework.

## Using Multimodal Agents

CrewAI supports multimodal agents that can process both text and non-text content like images. This guide will show you how to enable and use multimodal capabilities in your agents.

### Enabling Multimodal Capabilities

To create a multimodal agent, simply set the `multimodal` parameter to `True` when initializing your agent:

When you set `multimodal=True`, the agent is automatically configured with the necessary tools for handling non-text content, including the `AddImageTool`.

### Working with Images

The multimodal agent comes pre-configured with the `AddImageTool`, which allows it to process images. You don't need to manually add this tool - it's automatically included when you enable multimodal capabilities.

Here's a complete example showing how to use a multimodal agent to analyze an image:

```python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
When you set `multimodal=True`, the agent is automatically configured with the necessary tools for handling non-text content, including the `AddImageTool`.

### Working with Images

The multimodal agent comes pre-configured with the `AddImageTool`, which allows it to process images. You don't need to manually add this tool - it's automatically included when you enable multimodal capabilities.

Here's a complete example showing how to use a multimodal agent to analyze an image:
```

---

## What is CrewAI?

**URL:** llms-txt#what-is-crewai?

**Contents:**
- How Crews Work
  - How It All Works Together
- Key Features
- How Flows Work
  - Key Capabilities
- When to Use Crews vs. Flows
  - Decision Framework
- Why Choose CrewAI?
- Ready to Start Building?

**CrewAI is a lean, lightning-fast Python framework built entirely from scratch—completely independent of LangChain or other agent frameworks.**

CrewAI empowers developers with both high-level simplicity and precise low-level control, ideal for creating autonomous AI agents tailored to any scenario:

* **[CrewAI Crews](/en/guides/crews/first-crew)**: Optimize for autonomy and collaborative intelligence, enabling you to create AI teams where each agent has specific roles, tools, and goals.
* **[CrewAI Flows](/en/guides/flows/first-flow)**: Enable granular, event-driven control, single LLM calls for precise task orchestration and supports Crews natively.

With over 100,000 developers certified through our community courses, CrewAI is rapidly becoming the standard for enterprise-ready AI automation.

<Note>
  Just like a company has departments (Sales, Engineering, Marketing) working together under leadership to achieve business goals, CrewAI helps you create an organization of AI agents with specialized roles collaborating to accomplish complex tasks.
</Note>

<Frame>
  <img alt="CrewAI Framework Overview" />
</Frame>

| Component     |         Description        | Key Features                                                                                                                      |
| :------------ | :------------------------: | :-------------------------------------------------------------------------------------------------------------------------------- |
| **Crew**      | The top-level organization | • Manages AI agent teams<br />• Oversees workflows<br />• Ensures collaboration<br />• Delivers outcomes                          |
| **AI Agents** |  Specialized team members  | • Have specific roles (researcher, writer)<br />• Use designated tools<br />• Can delegate tasks<br />• Make autonomous decisions |
| **Process**   | Workflow management system | • Defines collaboration patterns<br />• Controls task assignments<br />• Manages interactions<br />• Ensures efficient execution  |
| **Tasks**     |   Individual assignments   | • Have clear objectives<br />• Use specific tools<br />• Feed into larger process<br />• Produce actionable results               |

### How It All Works Together

1. The **Crew** organizes the overall operation
2. **AI Agents** work on their specialized tasks
3. The **Process** ensures smooth collaboration
4. **Tasks** get completed to achieve the goal

<CardGroup>
  <Card title="Role-Based Agents" icon="users">
    Create specialized agents with defined roles, expertise, and goals - from researchers to analysts to writers
  </Card>

<Card title="Flexible Tools" icon="screwdriver-wrench">
    Equip agents with custom tools and APIs to interact with external services and data sources
  </Card>

<Card title="Intelligent Collaboration" icon="people-arrows">
    Agents work together, sharing insights and coordinating tasks to achieve complex objectives
  </Card>

<Card title="Task Management" icon="list-check">
    Define sequential or parallel workflows, with agents automatically handling task dependencies
  </Card>
</CardGroup>

<Note>
  While Crews excel at autonomous collaboration, Flows provide structured automations, offering granular control over workflow execution. Flows ensure tasks are executed reliably, securely, and efficiently, handling conditional logic, loops, and dynamic state management with precision. Flows integrate seamlessly with Crews, enabling you to balance high autonomy with exacting control.
</Note>

<Frame>
  <img alt="CrewAI Framework Overview" />
</Frame>

| Component        |            Description            | Key Features                                                                                                                                                         |
| :--------------- | :-------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Flow**         | Structured workflow orchestration | • Manages execution paths<br />• Handles state transitions<br />• Controls task sequencing<br />• Ensures reliable execution                                         |
| **Events**       |   Triggers for workflow actions   | • Initiate specific processes<br />• Enable dynamic responses<br />• Support conditional branching<br />• Allow for real-time adaptation                             |
| **States**       |    Workflow execution contexts    | • Maintain execution data<br />• Enable persistence<br />• Support resumability<br />• Ensure execution integrity                                                    |
| **Crew Support** |    Enhances workflow automation   | • Injects pockets of agency when needed<br />• Complements structured workflows<br />• Balances automation with intelligence<br />• Enables adaptive decision-making |

<CardGroup>
  <Card title="Event-Driven Orchestration" icon="bolt">
    Define precise execution paths responding dynamically to events
  </Card>

<Card title="Fine-Grained Control" icon="sliders">
    Manage workflow states and conditional execution securely and efficiently
  </Card>

<Card title="Native Crew Integration" icon="puzzle-piece">
    Effortlessly combine with Crews for enhanced autonomy and intelligence
  </Card>

<Card title="Deterministic Execution" icon="route">
    Ensure predictable outcomes with explicit control flow and error handling
  </Card>
</CardGroup>

## When to Use Crews vs. Flows

<Note>
  Understanding when to use [Crews](/en/guides/crews/first-crew) versus [Flows](/en/guides/flows/first-flow) is key to maximizing the potential of CrewAI in your applications.
</Note>

| Use Case                | Recommended Approach                 | Why?                                                                                                                                        |
| :---------------------- | :----------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------ |
| **Open-ended research** | [Crews](/en/guides/crews/first-crew) | When tasks require creative thinking, exploration, and adaptation                                                                           |
| **Content generation**  | [Crews](/en/guides/crews/first-crew) | For collaborative creation of articles, reports, or marketing materials                                                                     |
| **Decision workflows**  | [Flows](/en/guides/flows/first-flow) | When you need predictable, auditable decision paths with precise control                                                                    |
| **API orchestration**   | [Flows](/en/guides/flows/first-flow) | For reliable integration with multiple external services in a specific sequence                                                             |
| **Hybrid applications** | Combined approach                    | Use [Flows](/en/guides/flows/first-flow) to orchestrate overall process with [Crews](/en/guides/crews/first-crew) handling complex subtasks |

### Decision Framework

* **Choose [Crews](/en/guides/crews/first-crew) when:** You need autonomous problem-solving, creative collaboration, or exploratory tasks
* **Choose [Flows](/en/guides/flows/first-flow) when:** You require deterministic outcomes, auditability, or precise control over execution
* **Combine both when:** Your application needs both structured processes and pockets of autonomous intelligence

## Why Choose CrewAI?

* 🧠 **Autonomous Operation**: Agents make intelligent decisions based on their roles and available tools
* 📝 **Natural Interaction**: Agents communicate and collaborate like human team members
* 🛠️ **Extensible Design**: Easy to add new tools, roles, and capabilities
* 🚀 **Production Ready**: Built for reliability and scalability in real-world applications
* 🔒 **Security-Focused**: Designed with enterprise security requirements in mind
* 💰 **Cost-Efficient**: Optimized to minimize token usage and API calls

## Ready to Start Building?

<CardGroup>
  <Card title="Build Your First Crew" icon="users-gear" href="/en/guides/crews/first-crew">
    Step-by-step tutorial to create a collaborative AI team that works together to solve complex problems.
  </Card>

<Card title="Build Your First Flow" icon="diagram-project" href="/en/guides/flows/first-flow">
    Learn how to create structured, event-driven workflows with precise control over execution.
  </Card>
</CardGroup>

<CardGroup>
  <Card title="Install CrewAI" icon="wrench" href="/en/installation">
    Get started with CrewAI in your development environment.
  </Card>

<Card title="Quick Start" icon="bolt" href="en/quickstart">
    Follow our quickstart guide to create your first CrewAI agent and get hands-on experience.
  </Card>

<Card title="Join the Community" icon="comments" href="https://community.crewai.com">
    Connect with other developers, get help, and share your CrewAI experiences.
  </Card>
</CardGroup>

---

## Writer Agent

**URL:** llms-txt#writer-agent

role: "Technical Content Writer"
goal: "Transform research into engaging, clear content that educates and informs"
backstory: "You are an experienced writer who excels at explaining complex concepts..."

---

## Write content to a file in a specified directory

**URL:** llms-txt#write-content-to-a-file-in-a-specified-directory

**Contents:**
- Arguments
- Conclusion

result = file_writer_tool._run('example.txt', 'This is a test content.', 'test_directory')
print(result)
```

* `filename`: The name of the file you want to create or overwrite.
* `content`: The content to write into the file.
* `directory` (optional): The path to the directory where the file will be created. Defaults to the current directory (`.`). If the directory does not exist, it will be created.

By integrating the `FileWriterTool` into your crews, the agents can reliably write content to files across different operating systems.
This tool is essential for tasks that require saving output data, creating structured file systems, and handling cross-platform file operations.
It's particularly recommended for Windows users who may encounter file writing issues with standard Python file operations.

By adhering to the setup and usage guidelines provided, incorporating this tool into projects is straightforward and ensures consistent file writing behavior across all platforms.

---

## `ZapierActionsAdapter`

**URL:** llms-txt#`zapieractionsadapter`

**Contents:**
- Description
- Installation
- Environment Variables
- Example
- Notes & limits
- Notes

Use the Zapier adapter to list and call Zapier actions as CrewAI tools. This enables agents to trigger automations across thousands of apps.

This adapter is included with `crewai-tools`. No extra install required.

## Environment Variables

* `ZAPIER_API_KEY` (required): Zapier API key. Get one from the Zapier Actions dashboard at [https://actions.zapier.com/](https://actions.zapier.com/) (create an account, then generate an API key). You can also pass `zapier_api_key` directly when constructing the adapter.

* The adapter lists available actions for your key and creates `BaseTool` wrappers dynamically.
* Handle action‑specific required fields in your task instructions or tool call.
* Rate limits depend on your Zapier plan; see the Zapier Actions docs.

* The adapter fetches available actions and generates `BaseTool` wrappers dynamically.

---

## Zendesk Integration

**URL:** llms-txt#zendesk-integration

**Contents:**
- Overview
- Prerequisites
- Setting Up Zendesk Integration
  - 1. Connect Your Zendesk Account
  - 2. Install Required Package
  - 3. Environment Variable Setup
- Available Tools
  - **Ticket Management**
  - **User Management**
  - **Administrative Tools**

Source: https://docs.crewai.com/en/enterprise/integrations/zendesk

Customer support and helpdesk management with Zendesk integration for CrewAI.

Enable your agents to manage customer support operations through Zendesk. Create and update tickets, manage users, track support metrics, and streamline your customer service workflows with AI-powered automation.

Before using the Zendesk integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A Zendesk account with appropriate API permissions
* Connected your Zendesk account through the [Integrations page](https://app.crewai.com/integrations)

## Setting Up Zendesk Integration

### 1. Connect Your Zendesk Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Zendesk** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for ticket and user management
5. Copy your Enterprise Token from [Integration Settings](https://app.crewai.com/crewai_plus/settings/integrations)

### 2. Install Required Package

### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>

Or add it to your `.env` file:

### **Ticket Management**

<AccordionGroup>
  <Accordion title="zendesk/create_ticket">
    **Description:** Create a new support ticket in Zendesk.

* `ticketSubject` (string, required): Ticket subject line (e.g., "Help, my printer is on fire!")
    * `ticketDescription` (string, required): First comment that appears on the ticket (e.g., "The smoke is very colorful.")
    * `requesterName` (string, required): Name of the user requesting support (e.g., "Jane Customer")
    * `requesterEmail` (string, required): Email of the user requesting support (e.g., "[jane@example.com](mailto:jane@example.com)")
    * `assigneeId` (string, optional): Zendesk Agent ID assigned to this ticket - Use Connect Portal Workflow Settings to allow users to select an assignee
    * `ticketType` (string, optional): Ticket type - Options: problem, incident, question, task
    * `ticketPriority` (string, optional): Priority level - Options: urgent, high, normal, low
    * `ticketStatus` (string, optional): Ticket status - Options: new, open, pending, hold, solved, closed
    * `ticketDueAt` (string, optional): Due date for task-type tickets (ISO 8601 timestamp)
    * `ticketTags` (string, optional): Array of tags to apply (e.g., `["enterprise", "other_tag"]`)
    * `ticketExternalId` (string, optional): External ID to link tickets to local records
    * `ticketCustomFields` (object, optional): Custom field values in JSON format
  </Accordion>

<Accordion title="zendesk/update_ticket">
    **Description:** Update an existing support ticket in Zendesk.

* `ticketId` (string, required): ID of the ticket to update (e.g., "35436")
    * `ticketSubject` (string, optional): Updated ticket subject
    * `requesterName` (string, required): Name of the user who requested this ticket
    * `requesterEmail` (string, required): Email of the user who requested this ticket
    * `assigneeId` (string, optional): Updated assignee ID - Use Connect Portal Workflow Settings
    * `ticketType` (string, optional): Updated ticket type - Options: problem, incident, question, task
    * `ticketPriority` (string, optional): Updated priority - Options: urgent, high, normal, low
    * `ticketStatus` (string, optional): Updated status - Options: new, open, pending, hold, solved, closed
    * `ticketDueAt` (string, optional): Updated due date (ISO 8601 timestamp)
    * `ticketTags` (string, optional): Updated tags array
    * `ticketExternalId` (string, optional): Updated external ID
    * `ticketCustomFields` (object, optional): Updated custom field values
  </Accordion>

<Accordion title="zendesk/get_ticket_by_id">
    **Description:** Retrieve a specific ticket by its ID.

* `ticketId` (string, required): The ticket ID to retrieve (e.g., "35436")
  </Accordion>

<Accordion title="zendesk/add_comment_to_ticket">
    **Description:** Add a comment or internal note to an existing ticket.

* `ticketId` (string, required): ID of the ticket to add comment to (e.g., "35436")
    * `commentBody` (string, required): Comment message (accepts plain text or HTML, e.g., "Thanks for your help!")
    * `isInternalNote` (boolean, optional): Set to true for internal notes instead of public replies (defaults to false)
    * `isPublic` (boolean, optional): True for public comments, false for internal notes
  </Accordion>

<Accordion title="zendesk/search_tickets">
    **Description:** Search for tickets using various filters and criteria.

* `ticketSubject` (string, optional): Filter by text in ticket subject
    * `ticketDescription` (string, optional): Filter by text in ticket description and comments
    * `ticketStatus` (string, optional): Filter by status - Options: new, open, pending, hold, solved, closed
    * `ticketType` (string, optional): Filter by type - Options: problem, incident, question, task, no\_type
    * `ticketPriority` (string, optional): Filter by priority - Options: urgent, high, normal, low, no\_priority
    * `requesterId` (string, optional): Filter by requester user ID
    * `assigneeId` (string, optional): Filter by assigned agent ID
    * `recipientEmail` (string, optional): Filter by original recipient email address
    * `ticketTags` (string, optional): Filter by ticket tags
    * `ticketExternalId` (string, optional): Filter by external ID
    * `createdDate` (object, optional): Filter by creation date with operator (EQUALS, LESS\_THAN\_EQUALS, GREATER\_THAN\_EQUALS) and value
    * `updatedDate` (object, optional): Filter by update date with operator and value
    * `dueDate` (object, optional): Filter by due date with operator and value
    * `sort_by` (string, optional): Sort field - Options: created\_at, updated\_at, priority, status, ticket\_type
    * `sort_order` (string, optional): Sort direction - Options: asc, desc
  </Accordion>
</AccordionGroup>

### **User Management**

<AccordionGroup>
  <Accordion title="zendesk/create_user">
    **Description:** Create a new user in Zendesk.

* `name` (string, required): User's full name
    * `email` (string, optional): User's email address (e.g., "[jane@example.com](mailto:jane@example.com)")
    * `phone` (string, optional): User's phone number
    * `role` (string, optional): User role - Options: admin, agent, end-user
    * `externalId` (string, optional): Unique identifier from another system
    * `details` (string, optional): Additional user details
    * `notes` (string, optional): Internal notes about the user
  </Accordion>

<Accordion title="zendesk/update_user">
    **Description:** Update an existing user's information.

* `userId` (string, required): ID of the user to update
    * `name` (string, optional): Updated user name
    * `email` (string, optional): Updated email (adds as secondary email on update)
    * `phone` (string, optional): Updated phone number
    * `role` (string, optional): Updated role - Options: admin, agent, end-user
    * `externalId` (string, optional): Updated external ID
    * `details` (string, optional): Updated user details
    * `notes` (string, optional): Updated internal notes
  </Accordion>

<Accordion title="zendesk/get_user_by_id">
    **Description:** Retrieve a specific user by their ID.

* `userId` (string, required): The user ID to retrieve
  </Accordion>

<Accordion title="zendesk/search_users">
    **Description:** Search for users using various criteria.

* `name` (string, optional): Filter by user name
    * `email` (string, optional): Filter by user email (e.g., "[jane@example.com](mailto:jane@example.com)")
    * `role` (string, optional): Filter by role - Options: admin, agent, end-user
    * `externalId` (string, optional): Filter by external ID
    * `sort_by` (string, optional): Sort field - Options: created\_at, updated\_at
    * `sort_order` (string, optional): Sort direction - Options: asc, desc
  </Accordion>
</AccordionGroup>

### **Administrative Tools**

<AccordionGroup>
  <Accordion title="zendesk/get_ticket_fields">
    **Description:** Retrieve all standard and custom fields available for tickets.

* `paginationParameters` (object, optional): Pagination settings
      * `pageCursor` (string, optional): Page cursor for pagination
  </Accordion>

<Accordion title="zendesk/get_ticket_audits">
    **Description:** Get audit records (read-only history) for tickets.

* `ticketId` (string, optional): Get audits for specific ticket (if empty, retrieves audits for all non-archived tickets, e.g., "1234")
    * `paginationParameters` (object, optional): Pagination settings
      * `pageCursor` (string, optional): Page cursor for pagination
  </Accordion>
</AccordionGroup>

Custom fields allow you to store additional information specific to your organization:

## Ticket Priority Levels

Understanding priority levels:

* **urgent** - Critical issues requiring immediate attention
* **high** - Important issues that should be addressed quickly
* **normal** - Standard priority for most tickets
* **low** - Minor issues that can be addressed when convenient

## Ticket Status Workflow

Standard ticket status progression:

* **new** - Recently created, not yet assigned
* **open** - Actively being worked on
* **pending** - Waiting for customer response or external action
* **hold** - Temporarily paused
* **solved** - Issue resolved, awaiting customer confirmation
* **closed** - Ticket completed and closed

### Basic Zendesk Agent Setup

```python theme={null}
from crewai import Agent, Task, Crew
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
### 3. Environment Variable Setup

<Note>
  To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.
</Note>
```

Example 2 (unknown):
```unknown
Or add it to your `.env` file:
```

Example 3 (unknown):
```unknown
## Available Tools

### **Ticket Management**

<AccordionGroup>
  <Accordion title="zendesk/create_ticket">
    **Description:** Create a new support ticket in Zendesk.

    **Parameters:**

    * `ticketSubject` (string, required): Ticket subject line (e.g., "Help, my printer is on fire!")
    * `ticketDescription` (string, required): First comment that appears on the ticket (e.g., "The smoke is very colorful.")
    * `requesterName` (string, required): Name of the user requesting support (e.g., "Jane Customer")
    * `requesterEmail` (string, required): Email of the user requesting support (e.g., "[jane@example.com](mailto:jane@example.com)")
    * `assigneeId` (string, optional): Zendesk Agent ID assigned to this ticket - Use Connect Portal Workflow Settings to allow users to select an assignee
    * `ticketType` (string, optional): Ticket type - Options: problem, incident, question, task
    * `ticketPriority` (string, optional): Priority level - Options: urgent, high, normal, low
    * `ticketStatus` (string, optional): Ticket status - Options: new, open, pending, hold, solved, closed
    * `ticketDueAt` (string, optional): Due date for task-type tickets (ISO 8601 timestamp)
    * `ticketTags` (string, optional): Array of tags to apply (e.g., `["enterprise", "other_tag"]`)
    * `ticketExternalId` (string, optional): External ID to link tickets to local records
    * `ticketCustomFields` (object, optional): Custom field values in JSON format
  </Accordion>

  <Accordion title="zendesk/update_ticket">
    **Description:** Update an existing support ticket in Zendesk.

    **Parameters:**

    * `ticketId` (string, required): ID of the ticket to update (e.g., "35436")
    * `ticketSubject` (string, optional): Updated ticket subject
    * `requesterName` (string, required): Name of the user who requested this ticket
    * `requesterEmail` (string, required): Email of the user who requested this ticket
    * `assigneeId` (string, optional): Updated assignee ID - Use Connect Portal Workflow Settings
    * `ticketType` (string, optional): Updated ticket type - Options: problem, incident, question, task
    * `ticketPriority` (string, optional): Updated priority - Options: urgent, high, normal, low
    * `ticketStatus` (string, optional): Updated status - Options: new, open, pending, hold, solved, closed
    * `ticketDueAt` (string, optional): Updated due date (ISO 8601 timestamp)
    * `ticketTags` (string, optional): Updated tags array
    * `ticketExternalId` (string, optional): Updated external ID
    * `ticketCustomFields` (object, optional): Updated custom field values
  </Accordion>

  <Accordion title="zendesk/get_ticket_by_id">
    **Description:** Retrieve a specific ticket by its ID.

    **Parameters:**

    * `ticketId` (string, required): The ticket ID to retrieve (e.g., "35436")
  </Accordion>

  <Accordion title="zendesk/add_comment_to_ticket">
    **Description:** Add a comment or internal note to an existing ticket.

    **Parameters:**

    * `ticketId` (string, required): ID of the ticket to add comment to (e.g., "35436")
    * `commentBody` (string, required): Comment message (accepts plain text or HTML, e.g., "Thanks for your help!")
    * `isInternalNote` (boolean, optional): Set to true for internal notes instead of public replies (defaults to false)
    * `isPublic` (boolean, optional): True for public comments, false for internal notes
  </Accordion>

  <Accordion title="zendesk/search_tickets">
    **Description:** Search for tickets using various filters and criteria.

    **Parameters:**

    * `ticketSubject` (string, optional): Filter by text in ticket subject
    * `ticketDescription` (string, optional): Filter by text in ticket description and comments
    * `ticketStatus` (string, optional): Filter by status - Options: new, open, pending, hold, solved, closed
    * `ticketType` (string, optional): Filter by type - Options: problem, incident, question, task, no\_type
    * `ticketPriority` (string, optional): Filter by priority - Options: urgent, high, normal, low, no\_priority
    * `requesterId` (string, optional): Filter by requester user ID
    * `assigneeId` (string, optional): Filter by assigned agent ID
    * `recipientEmail` (string, optional): Filter by original recipient email address
    * `ticketTags` (string, optional): Filter by ticket tags
    * `ticketExternalId` (string, optional): Filter by external ID
    * `createdDate` (object, optional): Filter by creation date with operator (EQUALS, LESS\_THAN\_EQUALS, GREATER\_THAN\_EQUALS) and value
    * `updatedDate` (object, optional): Filter by update date with operator and value
    * `dueDate` (object, optional): Filter by due date with operator and value
    * `sort_by` (string, optional): Sort field - Options: created\_at, updated\_at, priority, status, ticket\_type
    * `sort_order` (string, optional): Sort direction - Options: asc, desc
  </Accordion>
</AccordionGroup>

### **User Management**

<AccordionGroup>
  <Accordion title="zendesk/create_user">
    **Description:** Create a new user in Zendesk.

    **Parameters:**

    * `name` (string, required): User's full name
    * `email` (string, optional): User's email address (e.g., "[jane@example.com](mailto:jane@example.com)")
    * `phone` (string, optional): User's phone number
    * `role` (string, optional): User role - Options: admin, agent, end-user
    * `externalId` (string, optional): Unique identifier from another system
    * `details` (string, optional): Additional user details
    * `notes` (string, optional): Internal notes about the user
  </Accordion>

  <Accordion title="zendesk/update_user">
    **Description:** Update an existing user's information.

    **Parameters:**

    * `userId` (string, required): ID of the user to update
    * `name` (string, optional): Updated user name
    * `email` (string, optional): Updated email (adds as secondary email on update)
    * `phone` (string, optional): Updated phone number
    * `role` (string, optional): Updated role - Options: admin, agent, end-user
    * `externalId` (string, optional): Updated external ID
    * `details` (string, optional): Updated user details
    * `notes` (string, optional): Updated internal notes
  </Accordion>

  <Accordion title="zendesk/get_user_by_id">
    **Description:** Retrieve a specific user by their ID.

    **Parameters:**

    * `userId` (string, required): The user ID to retrieve
  </Accordion>

  <Accordion title="zendesk/search_users">
    **Description:** Search for users using various criteria.

    **Parameters:**

    * `name` (string, optional): Filter by user name
    * `email` (string, optional): Filter by user email (e.g., "[jane@example.com](mailto:jane@example.com)")
    * `role` (string, optional): Filter by role - Options: admin, agent, end-user
    * `externalId` (string, optional): Filter by external ID
    * `sort_by` (string, optional): Sort field - Options: created\_at, updated\_at
    * `sort_order` (string, optional): Sort direction - Options: asc, desc
  </Accordion>
</AccordionGroup>

### **Administrative Tools**

<AccordionGroup>
  <Accordion title="zendesk/get_ticket_fields">
    **Description:** Retrieve all standard and custom fields available for tickets.

    **Parameters:**

    * `paginationParameters` (object, optional): Pagination settings
      * `pageCursor` (string, optional): Page cursor for pagination
  </Accordion>

  <Accordion title="zendesk/get_ticket_audits">
    **Description:** Get audit records (read-only history) for tickets.

    **Parameters:**

    * `ticketId` (string, optional): Get audits for specific ticket (if empty, retrieves audits for all non-archived tickets, e.g., "1234")
    * `paginationParameters` (object, optional): Pagination settings
      * `pageCursor` (string, optional): Page cursor for pagination
  </Accordion>
</AccordionGroup>

## Custom Fields

Custom fields allow you to store additional information specific to your organization:
```

Example 4 (unknown):
```unknown
## Ticket Priority Levels

Understanding priority levels:

* **urgent** - Critical issues requiring immediate attention
* **high** - Important issues that should be addressed quickly
* **normal** - Standard priority for most tickets
* **low** - Minor issues that can be addressed when convenient

## Ticket Status Workflow

Standard ticket status progression:

* **new** - Recently created, not yet assigned
* **open** - Actively being worked on
* **pending** - Waiting for customer response or external action
* **hold** - Temporarily paused
* **solved** - Issue resolved, awaiting customer confirmation
* **closed** - Ticket completed and closed

## Usage Examples

### Basic Zendesk Agent Setup
```

---

## ...

**URL:** llms-txt#...

task1 = Task(
    description='Find and summarize the latest AI news',
    expected_output='A bullet list summary of the top 5 most important AI news',
    agent=research_agent,
    tools=[search_tool]
)

crew = Crew(
    agents=[research_agent],
    tasks=[task1, task2, task3],
    verbose=True
)

result = crew.kickoff()

---

## └── Another Agent Role/      # Another agent's collection

**URL:** llms-txt#└──-another-agent-role/------#-another-agent's-collection

**Contents:**
  - Complete Working Examples

python theme={null}
from crewai import Agent, Task, Crew
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

**Examples:**

Example 1 (unknown):
```unknown
### Complete Working Examples

#### Example 1: Agent-Only Knowledge
```

---

## ├── Technical Specialist/    # Agent knowledge collection

**URL:** llms-txt#├──-technical-specialist/----#-agent-knowledge-collection

---
