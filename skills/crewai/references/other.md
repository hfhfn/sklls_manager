# Crewai - Other

**Pages:** 342

---

## 1. Stdio Server:

**URL:** llms-txt#1.-stdio-server:

server_params=StdioServerParameters(
    command="python3",
    args=["servers/your_server.py"],
    env={"UV_PYTHON": "3.12", **os.environ},
)

---

## 1. Successfully connect to working servers

**URL:** llms-txt#1.-successfully-connect-to-working-servers

---

## 2. Log warnings for failing servers

**URL:** llms-txt#2.-log-warnings-for-failing-servers

---

## 2. SSE Server:

**URL:** llms-txt#2.-sse-server:

server_params = {
    "url": "http://localhost:8000/sse",
    "transport": "sse"
}

---

## 3. Streamable HTTP Server:

**URL:** llms-txt#3.-streamable-http-server:

server_params = {
    "url": "http://localhost:8001/mcp",
    "transport": "streamable-http"
}

---

## 4. Not crash or hang on server failures

**URL:** llms-txt#4.-not-crash-or-hang-on-server-failures

**Contents:**
  - Timeout Protection

**Examples:**

Example 1 (unknown):
```unknown
### Timeout Protection

All MCP operations have built-in timeouts:

* **Connection timeout**: 10 seconds
* **Tool execution timeout**: 30 seconds
* **Discovery timeout**: 15 seconds
```

---

## Access structured data

**URL:** llms-txt#access-structured-data

**Contents:**
- Best Practices
- Organization Management

print(f"Key Trends: {structured_result.pydantic.key_trends}")
print(f"Recommendation: {structured_result.pydantic.recommendation}")
bash theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## Best Practices

1. **Naming Convention**: Use clear, descriptive names for your repository agents
2. **Documentation**: Include comprehensive descriptions for each agent
3. **Tool Management**: Ensure that tools referenced by repository agents are available in your environment
4. **Access Control**: Manage permissions to ensure only authorized team members can modify repository agents

## Organization Management

To switch between organizations or see your current organization, use the CrewAI CLI:
```

---

## Access the fingerprints

**URL:** llms-txt#access-the-fingerprints

agent_fingerprint = agent.fingerprint
crew_fingerprint = crew.fingerprint
task_fingerprint = task.fingerprint

---

## Access the metadata

**URL:** llms-txt#access-the-metadata

**Contents:**
- Fingerprint Persistence

print(f"Agent metadata: {agent.fingerprint.metadata}")
python theme={null}
original_fingerprint = agent.fingerprint.uuid_str

**Examples:**

Example 1 (unknown):
```unknown
## Fingerprint Persistence

Fingerprints are designed to persist and remain unchanged throughout a component's lifecycle. If you modify a component, the fingerprint remains the same:
```

---

## Access the raw response

**URL:** llms-txt#access-the-raw-response

**Contents:**
  - Parameters and Return Values
  - Structured Output

print(result.raw)
python Code theme={null}
from pydantic import BaseModel
from typing import List

class ResearchFindings(BaseModel):
    main_points: List[str]
    key_technologies: List[str]
    future_predictions: str

**Examples:**

Example 1 (unknown):
```unknown
### Parameters and Return Values

| Parameter         | Type                               | Description                                                               |
| :---------------- | :--------------------------------- | :------------------------------------------------------------------------ |
| `messages`        | `Union[str, List[Dict[str, str]]]` | Either a string query or a list of message dictionaries with role/content |
| `response_format` | `Optional[Type[Any]]`              | Optional Pydantic model for structured output                             |

The method returns a `LiteAgentOutput` object with the following properties:

* `raw`: String containing the raw output text
* `pydantic`: Parsed Pydantic model (if a `response_format` was provided)
* `agent_role`: Role of the agent that produced the output
* `usage_metrics`: Token usage metrics for the execution

### Structured Output

You can get structured output by providing a Pydantic model as the `response_format`:
```

---

## Add a PDF file

**URL:** llms-txt#add-a-pdf-file

rag_tool.add(data_type="file", path="path/to/your/document.pdf")

---

## Add a web page

**URL:** llms-txt#add-a-web-page

rag_tool.add(data_type="web_page", url="https://example.com")

---

## Add a YouTube video

**URL:** llms-txt#add-a-youtube-video

rag_tool.add(data_type="youtube_video", url="https://www.youtube.com/watch?v=VIDEO_ID")

---

## Add content from a file

**URL:** llms-txt#add-content-from-a-file

rag_tool.add(data_type="file", path="path/to/your/document.pdf")

---

## Add content from a web page

**URL:** llms-txt#add-content-from-a-web-page

rag_tool.add(data_type="web_page", url="https://example.com")

---

## Add your provider's API key here too.

**URL:** llms-txt#add-your-provider's-api-key-here-too.

**Contents:**
- Step 8: Install Dependencies
- Step 9: Run Your Crew
- Step 10: Review the Output
- Exploring Other CLI Commands

bash theme={null}
crewai install
bash theme={null}
crewai run
bash theme={null}

**Examples:**

Example 1 (unknown):
```unknown
See the [LLM Setup guide](/en/concepts/llms#setting-up-your-llm) for details on configuring your provider of choice. You can get a Serper API key from [Serper.dev](https://serper.dev/).

## Step 8: Install Dependencies

Install the required dependencies using the CrewAI CLI:
```

Example 2 (unknown):
```unknown
This command will:

1. Read the dependencies from your project configuration
2. Create a virtual environment if needed
3. Install all required packages

## Step 9: Run Your Crew

Now for the exciting moment - it's time to run your crew and see AI collaboration in action!
```

Example 3 (unknown):
```unknown
When you run this command, you'll see your crew spring to life. The researcher will gather information about the specified topic, and the analyst will then create a comprehensive report based on that research. You'll see the agents' thought processes, actions, and outputs in real-time as they work together to complete their tasks.

## Step 10: Review the Output

Once the crew completes its work, you'll find the final report in the `output/report.md` file. The report will include:

1. An executive summary
2. Detailed information about the topic
3. Analysis and insights
4. Recommendations or future considerations

Take a moment to appreciate what you've accomplished - you've created a system where multiple AI agents collaborated on a complex task, each contributing their specialized skills to produce a result that's greater than what any single agent could achieve alone.

## Exploring Other CLI Commands

CrewAI offers several other useful CLI commands for working with crews:
```

---

## Advanced OpenAI configuration

**URL:** llms-txt#advanced-openai-configuration

**Contents:**
  - Azure OpenAI Embeddings
  - Google AI Embeddings
  - Vertex AI Embeddings
  - Ollama Embeddings (Local)

crew = Crew(
    memory=True,
    embedder={
        "provider": "openai",
        "config": {
            "api_key": "your-openai-api-key",  # Optional: override env var
            "model_name": "text-embedding-3-large",
            "dimensions": 1536,  # Optional: reduce dimensions for smaller storage
            "organization_id": "your-org-id"  # Optional: for organization accounts
        }
    }
)
python theme={null}
crew = Crew(
    memory=True,
    embedder={
        "provider": "openai",  # Use openai provider for Azure
        "config": {
            "api_key": "your-azure-api-key",
            "api_base": "https://your-resource.openai.azure.com/",
            "api_type": "azure",
            "api_version": "2023-05-15",
            "model_name": "text-embedding-3-small",
            "deployment_id": "your-deployment-name"  # Azure deployment name
        }
    }
)
python theme={null}
crew = Crew(
    memory=True,
    embedder={
        "provider": "google-generativeai",
        "config": {
            "api_key": "your-google-api-key",
            "model_name": "gemini-embedding-001"  # or "text-embedding-005", "text-multilingual-embedding-002"
        }
    }
)
python theme={null}
crew = Crew(
    memory=True,
    embedder={
        "provider": "vertexai",
        "config": {
            "project_id": "your-gcp-project-id",
            "region": "us-central1",  # or your preferred region
            "api_key": "your-service-account-key",
            "model_name": "textembedding-gecko"
        }
    }
)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### Azure OpenAI Embeddings

For enterprise users with Azure OpenAI deployments.
```

Example 2 (unknown):
```unknown
### Google AI Embeddings

Use Google's text embedding models for integration with Google Cloud services.
```

Example 3 (unknown):
```unknown
### Vertex AI Embeddings

For Google Cloud users with Vertex AI access.
```

Example 4 (unknown):
```unknown
### Ollama Embeddings (Local)

Run embeddings locally for privacy and cost savings.
```

---

## After kickoff - knowledge initialized

**URL:** llms-txt#after-kickoff---knowledge-initialized

print(f"After kickoff - Agent knowledge: {agent.knowledge}")
print(f"Agent knowledge collection: {agent.knowledge.storage.collection_name}")
print(f"Number of sources: {len(agent.knowledge.sources)}")
python theme={null}
import os
from crewai.utilities.paths import db_storage_path

**Examples:**

Example 1 (unknown):
```unknown
#### Verify Knowledge Storage Locations
```

---

## Always include backup options

**URL:** llms-txt#always-include-backup-options

**Contents:**
  - 4. Use Descriptive Agent Roles
- Troubleshooting
  - Common Issues

mcps=[
    "https://primary-api.com/mcp",       # Primary choice
    "https://backup-api.com/mcp",        # Backup option
    "crewai-amp:reliable-service"        # AMP fallback
]
python theme={null}
agent = Agent(
    role="Weather-Enhanced Market Analyst",
    goal="Analyze markets considering weather impacts",
    backstory="Financial analyst with access to weather data for agricultural market insights",
    mcps=[
        "https://weather.service.com/mcp#get_forecast",
        "crewai-amp:financial-data#stock_analysis"
    ]
)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### 4. Use Descriptive Agent Roles
```

Example 2 (unknown):
```unknown
## Troubleshooting

### Common Issues

**No tools discovered:**
```

---

## And the search uses filter_by="year", filter_value=2024

**URL:** llms-txt#and-the-search-uses-filter_by="year",-filter_value=2024

---

## Apply multiple guardrails sequentially

**URL:** llms-txt#apply-multiple-guardrails-sequentially

blog_task = Task(
    description="Write a blog post about AI",
    expected_output="A well-formatted blog post between 100-500 words",
    agent=blog_agent,
    guardrails=[
        validate_word_count,      # First: validate length
        validate_no_profanity,    # Second: check content
        format_output             # Third: format the result
    ],
    guardrail_max_retries=3
)
python Code theme={null}
from typing import Tuple, Any
from crewai import TaskOutput, Task

def validate_word_count(result: TaskOutput) -> Tuple[bool, Any]:
    """Validate word count is within limits."""
    word_count = len(result.raw.split())
    if word_count < 100:
        return (False, f"Content too short: {word_count} words. Need at least 100 words.")
    if word_count > 500:
        return (False, f"Content too long: {word_count} words. Maximum is 500 words.")
    return (True, result.raw)

**Examples:**

Example 1 (unknown):
```unknown
In this example, the guardrails execute in order:

1. `validate_word_count` checks the word count
2. `validate_no_profanity` checks for inappropriate language (using the output from step 1)
3. `format_output` formats the final result (using the output from step 2)

If any guardrail fails, the error is sent back to the agent, and the task is retried up to `guardrail_max_retries` times.

**Mixing function-based and LLM-based guardrails**:

You can combine both function-based and string-based guardrails in the same list:
```

---

## Arize Phoenix

**URL:** llms-txt#arize-phoenix

Source: https://docs.crewai.com/en/observability/arize-phoenix

Arize Phoenix integration for CrewAI with OpenTelemetry and OpenInference

---

## Ask question to coworker(question: str, context: str, coworker: str)

**URL:** llms-txt#ask-question-to-coworker(question:-str,-context:-str,-coworker:-str)

**Contents:**
- Collaboration in Action

python theme={null}
from crewai import Agent, Crew, Task, Process

**Examples:**

Example 1 (unknown):
```unknown
## Collaboration in Action

Here's a complete example showing agents collaborating on a content creation task:
```

---

## "asp": True,  # Bypass scraping blocking solutions, like Cloudflare

**URL:** llms-txt#"asp":-true,--#-bypass-scraping-blocking-solutions,-like-cloudflare

---

## Assuming you have a flow instance

**URL:** llms-txt#assuming-you-have-a-flow-instance

**Contents:**
  - Understanding the Plot
  - Conclusion
- Next Steps
- Running Flows
  - Using the Flow API
  - Streaming Flow Execution

flow.plot("my_flow_plot")
bash theme={null}
crewai flow plot
python theme={null}
flow = ExampleFlow()
result = flow.kickoff()
python theme={null}
class StreamingFlow(Flow):
    stream = True  # Enable streaming

@start()
    def research(self):
        # Your flow implementation
        pass

**Examples:**

Example 1 (unknown):
```unknown
This will generate a file named `my_flow_plot.html` in your current directory. You can open this file in a web browser to view the interactive plot.

#### Option 2: Using the Command Line

If you are working within a structured CrewAI project, you can generate a plot using the command line. This is particularly useful for larger projects where you want to visualize the entire flow setup.
```

Example 2 (unknown):
```unknown
This command will generate an HTML file with the plot of your flow, similar to the `plot()` method. The file will be saved in your project directory, and you can open it in a web browser to explore the flow.

### Understanding the Plot

The generated plot will display nodes representing the tasks in your flow, with directed edges indicating the flow of execution. The plot is interactive, allowing you to zoom in and out, and hover over nodes to see additional details.

By visualizing your flows, you can gain a clearer understanding of the workflow's structure, making it easier to debug, optimize, and communicate your AI processes to others.

### Conclusion

Plotting your flows is a powerful feature of CrewAI that enhances your ability to design and manage complex AI workflows. Whether you choose to use the `plot()` method or the command line, generating plots will provide you with a visual representation of your workflows, aiding in both development and presentation.

## Next Steps

If you're interested in exploring additional examples of flows, we have a variety of recommendations in our examples repository. Here are four specific flow examples, each showcasing unique use cases to help you match your current problem type to a specific example:

1. **Email Auto Responder Flow**: This example demonstrates an infinite loop where a background job continually runs to automate email responses. It's a great use case for tasks that need to be performed repeatedly without manual intervention. [View Example](https://github.com/crewAIInc/crewAI-examples/tree/main/email_auto_responder_flow)

2. **Lead Score Flow**: This flow showcases adding human-in-the-loop feedback and handling different conditional branches using the router. It's an excellent example of how to incorporate dynamic decision-making and human oversight into your workflows. [View Example](https://github.com/crewAIInc/crewAI-examples/tree/main/lead-score-flow)

3. **Write a Book Flow**: This example excels at chaining multiple crews together, where the output of one crew is used by another. Specifically, one crew outlines an entire book, and another crew generates chapters based on the outline. Eventually, everything is connected to produce a complete book. This flow is perfect for complex, multi-step processes that require coordination between different tasks. [View Example](https://github.com/crewAIInc/crewAI-examples/tree/main/write_a_book_with_flows)

4. **Meeting Assistant Flow**: This flow demonstrates how to broadcast one event to trigger multiple follow-up actions. For instance, after a meeting is completed, the flow can update a Trello board, send a Slack message, and save the results. It's a great example of handling multiple outcomes from a single event, making it ideal for comprehensive task management and notification systems. [View Example](https://github.com/crewAIInc/crewAI-examples/tree/main/meeting_assistant_flow)

By exploring these examples, you can gain insights into how to leverage CrewAI Flows for various use cases, from automating repetitive tasks to managing complex, multi-step processes with dynamic decision-making and human feedback.

Also, check out our YouTube video on how to use flows in CrewAI below!

<iframe title="CrewAI Flows overview" />

## Running Flows

There are two ways to run a flow:

### Using the Flow API

You can run a flow programmatically by creating an instance of your flow class and calling the `kickoff()` method:
```

Example 3 (unknown):
```unknown
### Streaming Flow Execution

For real-time visibility into flow execution, you can enable streaming to receive output as it's generated:
```

---

## Assuming you have the CustomLLM class defined above

**URL:** llms-txt#assuming-you-have-the-customllm-class-defined-above

---

## Async handler (FastAPI, aiohttp, etc.):

**URL:** llms-txt#async-handler-(fastapi,-aiohttp,-etc.):

**Contents:**
  - Key Types
  - PendingFeedbackContext
  - Complete Async Flow Example

async def handle_feedback_webhook(flow_id: str, feedback: str):
    flow = ReviewFlow.from_pending(flow_id)
    result = await flow.resume_async(feedback)
    return result
python Code theme={null}
@dataclass
class PendingFeedbackContext:
    flow_id: str           # Unique identifier for this flow execution
    flow_class: str        # Fully qualified class name
    method_name: str       # Method that triggered feedback
    method_output: Any     # Output shown to the human
    message: str           # The request message
    emit: list[str] | None # Possible outcomes for routing
    default_outcome: str | None
    metadata: dict         # Custom metadata
    llm: str | None        # LLM for outcome collapsing
    requested_at: datetime
python Code theme={null}
from crewai.flow import (
    Flow, start, listen, human_feedback,
    HumanFeedbackProvider, HumanFeedbackPending, PendingFeedbackContext
)

class SlackNotificationProvider(HumanFeedbackProvider):
    """Provider that sends Slack notifications and pauses for async feedback."""

def __init__(self, channel: str):
        self.channel = channel

def request_feedback(self, context: PendingFeedbackContext, flow: Flow) -> str:
        # Send Slack notification (implement your own)
        slack_thread_id = self.post_to_slack(
            channel=self.channel,
            message=f"Review needed:\n\n{context.method_output}\n\n{context.message}",
        )

# Pause execution - framework handles persistence automatically
        raise HumanFeedbackPending(
            context=context,
            callback_info={
                "slack_channel": self.channel,
                "thread_id": slack_thread_id,
            }
        )

class ContentPipeline(Flow):
    @start()
    @human_feedback(
        message="Approve this content for publication?",
        emit=["approved", "rejected", "needs_revision"],
        llm="gpt-4o-mini",
        default_outcome="needs_revision",
        provider=SlackNotificationProvider("#content-reviews"),
    )
    def generate_content(self):
        return "AI-generated blog post content..."

@listen("approved")
    def publish(self, result):
        print(f"Publishing! Reviewer said: {result.feedback}")
        return {"status": "published"}

@listen("rejected")
    def archive(self, result):
        print(f"Archived. Reason: {result.feedback}")
        return {"status": "archived"}

@listen("needs_revision")
    def queue_revision(self, result):
        print(f"Queued for revision: {result.feedback}")
        return {"status": "revision_needed"}

**Examples:**

Example 1 (unknown):
```unknown
### Key Types

| Type                     | Description                                              |
| ------------------------ | -------------------------------------------------------- |
| `HumanFeedbackProvider`  | Protocol for custom feedback providers                   |
| `PendingFeedbackContext` | Contains all info needed to resume a paused flow         |
| `HumanFeedbackPending`   | Returned by `kickoff()` when flow is paused for feedback |
| `ConsoleProvider`        | Default blocking console input provider                  |

### PendingFeedbackContext

The context contains everything needed to resume:
```

Example 2 (unknown):
```unknown
### Complete Async Flow Example
```

---

## "auto_scroll": True,  # Auto scroll the page

**URL:** llms-txt#"auto_scroll":-true,--#-auto-scroll-the-page

---

## Azure OpenAI Setup

**URL:** llms-txt#azure-openai-setup

**Contents:**
- Setup Process
- Verification
- Troubleshooting

Source: https://docs.crewai.com/en/enterprise/guides/azure-openai-setup

Configure Azure OpenAI with Crew Studio for enterprise LLM connections

This guide walks you through connecting Azure OpenAI with Crew Studio for seamless enterprise AI operations.

<Steps>
  <Step title="Access Azure AI Foundry">
    1. In Azure, go to [Azure AI Foundry](https://ai.azure.com/) > select your Azure OpenAI deployment.
    2. On the left menu, click `Deployments`. If you don't have one, create a deployment with your desired model.
    3. Once created, select your deployment and locate the `Target URI` and `Key` on the right side of the page. Keep this page open, as you'll need this information.
       <Frame>
         <img alt="Azure AI Foundry" />
       </Frame>
  </Step>

<Step title="Configure CrewAI AOP Connection">
    4. In another tab, open `CrewAI AOP > LLM Connections`. Name your LLM Connection, select Azure as the provider, and choose the same model you selected in Azure.
    5. On the same page, add environment variables from step 3:
       * One named `AZURE_DEPLOYMENT_TARGET_URL` (using the Target URI). The URL should look like this: [https://your-deployment.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview](https://your-deployment.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview)
       * Another named `AZURE_API_KEY` (using the Key).
    6. Click `Add Connection` to save your LLM Connection.
  </Step>

<Step title="Set Default Configuration">
    7. In `CrewAI AOP > Settings > Defaults > Crew Studio LLM Settings`, set the new LLM Connection and model as defaults.
  </Step>

<Step title="Configure Network Access">
    8. Ensure network access settings:
       * In Azure, go to `Azure OpenAI > select your deployment`.
       * Navigate to `Resource Management > Networking`.
       * Ensure that `Allow access from all networks` is enabled. If this setting is restricted, CrewAI may be blocked from accessing your Azure OpenAI endpoint.
  </Step>
</Steps>

You're all set! Crew Studio will now use your Azure OpenAI connection. Test the connection by creating a simple crew or task to ensure everything is working properly.

If you encounter issues:

* Verify the Target URI format matches the expected pattern
* Check that the API key is correct and has proper permissions
* Ensure network access is configured to allow CrewAI connections
* Confirm the deployment model matches what you've configured in CrewAI

---

## Basic HTTPS server

**URL:** llms-txt#basic-https-server

"https://api.example.com/mcp"

---

## Before kickoff - knowledge not initialized

**URL:** llms-txt#before-kickoff---knowledge-not-initialized

print(f"Before kickoff - Agent knowledge: {getattr(agent, 'knowledge', None)}")

---

## Behind the scenes, this might be rewritten as:

**URL:** llms-txt#behind-the-scenes,-this-might-be-rewritten-as:

**Contents:**
  - Knowledge Events

rewritten_query = "What movies did John watch last week?"
python theme={null}
from crewai.events import (
    KnowledgeRetrievalStartedEvent,
    KnowledgeRetrievalCompletedEvent,
    BaseEventListener,
)

class KnowledgeMonitorListener(BaseEventListener):
    def setup_listeners(self, crewai_event_bus):
        @crewai_event_bus.on(KnowledgeRetrievalStartedEvent)
        def on_knowledge_retrieval_started(source, event):
            print(f"Agent '{event.agent.role}' started retrieving knowledge")
            
        @crewai_event_bus.on(KnowledgeRetrievalCompletedEvent)
        def on_knowledge_retrieval_completed(source, event):
            print(f"Agent '{event.agent.role}' completed knowledge retrieval")
            print(f"Query: {event.query}")
            print(f"Retrieved {len(event.retrieved_knowledge)} knowledge chunks")

**Examples:**

Example 1 (unknown):
```unknown
The rewritten query is more focused on the core information need and removes irrelevant instructions about output formatting.

<Tip>
  This mechanism is fully automatic and requires no configuration from users. The agent's LLM is used to perform the query rewriting, so using a more capable LLM can improve the quality of rewritten queries.
</Tip>

### Knowledge Events

CrewAI emits events during the knowledge retrieval process that you can listen for using the event system. These events allow you to monitor, debug, and analyze how knowledge is being retrieved and used by your agents.

#### Available Knowledge Events

* **KnowledgeRetrievalStartedEvent**: Emitted when an agent starts retrieving knowledge from sources
* **KnowledgeRetrievalCompletedEvent**: Emitted when knowledge retrieval is completed, including the query used and the retrieved content
* **KnowledgeQueryStartedEvent**: Emitted when a query to knowledge sources begins
* **KnowledgeQueryCompletedEvent**: Emitted when a query completes successfully
* **KnowledgeQueryFailedEvent**: Emitted when a query to knowledge sources fails
* **KnowledgeSearchQueryFailedEvent**: Emitted when a search query fails

#### Example: Monitoring Knowledge Retrieval
```

---

## Better: Focused state

**URL:** llms-txt#better:-focused-state

**Contents:**
  - 2. Use Structured State for Complex Flows

class FocusedState(BaseModel):
    user_id: str
    preferences: Dict[str, str]
    completion_status: Dict[str, bool]
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### 2. Use Structured State for Complex Flows

As your flows grow in complexity, structured state becomes increasingly valuable:
```

---

## Both filters will be combined (AND logic)

**URL:** llms-txt#both-filters-will-be-combined-(and-logic)

**Contents:**
- Search Parameters
- Return Format
- Default Embedding
- Custom Embeddings

json theme={null}
[
  {
    "metadata": {
      // Any metadata stored with the document
    },
    "context": "The actual text content of the document",
    "distance": 0.95  // Similarity score
  }
]
python theme={null}
from transformers import AutoTokenizer, AutoModel
import torch

**Examples:**

Example 1 (unknown):
```unknown
## Search Parameters

The tool accepts these parameters in its schema:

* `query` (str): The search query to find similar documents
* `filter_by` (str, optional): Metadata field to filter on
* `filter_value` (Any, optional): Value to filter by

## Return Format

The tool returns results in JSON format:
```

Example 2 (unknown):
```unknown
## Default Embedding

By default, the tool uses OpenAI's `text-embedding-3-large` model for vectorization. This requires:

* OpenAI API key set in environment: `OPENAI_API_KEY`

## Custom Embeddings

Instead of using the default embedding model, you might want to use your own embedding function in cases where you:

1. Want to use a different embedding model (e.g., Cohere, HuggingFace, Ollama models)
2. Need to reduce costs by using open-source embedding models
3. Have specific requirements for vector dimensions or embedding quality
4. Want to use domain-specific embeddings (e.g., for medical or legal text)

Here's an example using a HuggingFace model:
```

---

## Both stored in same ChromaDB instance but different collections

**URL:** llms-txt#both-stored-in-same-chromadb-instance-but-different-collections

---

## Braintrust

**URL:** llms-txt#braintrust

Source: https://docs.crewai.com/en/observability/braintrust

Braintrust integration for CrewAI with OpenTelemetry tracing and evaluation

---

## by providing its URL:

**URL:** llms-txt#by-providing-its-url:

**Contents:**
- Arguments
- Custom model and embeddings

tool = CodeDocsSearchTool(docs_url='https://docs.example.com/reference')
python Code theme={null}
tool = CodeDocsSearchTool(
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
<Note>
  Substitute '[https://docs.example.com/reference](https://docs.example.com/reference)' with your target documentation URL
  and 'How to use search tool' with the search query relevant to your needs.
</Note>

## Arguments

The following parameters can be used to customize the `CodeDocsSearchTool`'s behavior:

| Argument      | Type     | Description                                                             |
| :------------ | :------- | :---------------------------------------------------------------------- |
| **docs\_url** | `string` | *Optional*. Specifies the URL of the code documentation to be searched. |

## Custom model and embeddings

By default, the tool uses OpenAI for both embeddings and summarization. To customize the model, you can use a config dictionary as follows:
```

---

## Changelog

**URL:** llms-txt#changelog

Source: https://docs.crewai.com/en/changelog

Product updates, improvements, and bug fixes for CrewAI

<Update label="Sep 30, 2025">
  ## v1.0.0a1

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/1.0.0a1)

### Core Improvements & Fixes

* Fixed permission handling for `actions` in agent configuration
  * Updated CI workflows and release publishing to support the new monorepo structure
  * Bumped Python support to 3.13 and refreshed workspace metadata

### New Features & Enhancements

* Added `apps` and `actions` attributes to `Agent` for richer runtime control
  * Merged the `crewai-tools` repository into the main workspace (monorepo)
  * Bumped all packages to 1.0.0a1 to mark the alpha milestone

### Cleanup & Infrastructure

* Delivered a new CI pipeline with version pinning and publishing strategy
  * Unified internal code to manage multiple packages coherently
</Update>

<Update label="Sep 26, 2025">
  ## v0.201.1

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.201.1)

### Core Improvements & Fixes

* Renamed Watson embedding provider to `watsonx` and refreshed environment variable prefixes
  * Added ChromaDB compatibility for `watsonx` and `voyageai` embedding providers

### Cleanup & Deprecations

* Standardized environment variable prefixes for all embedding providers
  * Bumped CrewAI to 0.201.1 and updated internal dependencies
</Update>

<Update label="Sep 24, 2025">
  ## v0.201.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.201.0)

### Core Improvements & Fixes

* Made the `ready` parameter optional in `_create_reasoning_plan`
  * Fixed nested config handling for embedder configuration
  * Added `batch_size` support to avoid token limit errors
  * Corrected Quickstart documentation directory naming
  * Resolved test duration cache issues and event exports
  * Added fallback logic to crew settings

### New Features & Enhancements

* Introduced thread-safe platform context management
  * Added `crewai uv` wrapper command to run `uv` from the CLI
  * Enabled marking traces as failed for observability workflows
  * Added custom embedding types and provider migration support
  * Upgraded ChromaDB to v1.1.0 with compatibility fixes and type improvements
  * Added Pydantic-compatible import validation and reorganized dependency groups

### Documentation & Guides

* Updated changelog coverage for recent releases (0.193.x series)
  * Documented metadata support for LLM Guardrail events
  * Added guidance for fallback behavior and configuration visibility

### Cleanup & Deprecations

* Resolved Ruff and MyPy issues across modules
  * Improved type annotations and consolidated utilities
  * Deprecated legacy utilities in favor of Pydantic-compatible imports

* @qizwiz (first contribution)
</Update>

<Update label="Sep 20, 2025">
  ## v0.193.2

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.193.2)

* Updated pyproject templates to use the right version
</Update>

<Update label="Sep 20, 2025">
  ## v0.193.1

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.193.1)

* Series of minor fixes and linter improvements
</Update>

<Update label="Sep 19, 2025">
  ## v0.193.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.193.0)

## Core Improvements & Fixes

* Fixed handling of the `model` parameter during OpenAI adapter initialization
  * Resolved test duration cache issues in CI workflows
  * Fixed flaky test related to repeated tool usage by agents
  * Added missing event exports to `__init__.py` for consistent module behavior
  * Dropped message storage from metadata in Mem0 to reduce bloat
  * Fixed L2 distance metric support for backward compatibility in vector search

## New Features & Enhancements

* Introduced thread-safe platform context management
  * Added test duration caching for optimized `pytest-split` runs
  * Added ephemeral trace improvements for better trace control
  * Made search parameters for RAG, knowledge, and memory fully configurable
  * Enabled ChromaDB to use OpenAI API for embedding functions
  * Added deeper observability tools for user-level insights
  * Unified RAG storage system with instance-specific client support

## Documentation & Guides

* Updated `RagTool` references to reflect CrewAI native RAG implementation
  * Improved internal docs for `langgraph` and `openai` agent adapters with type annotations and docstrings
</Update>

<Update label="Sep 11, 2025">
  ## v0.186.1

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.186.1)

* Fixed version not being found and silently failing reversion
  * Bumped CrewAI version to 0.186.1 and updated dependencies in the CLI
</Update>

<Update label="Sep 10, 2025">
  ## v0.186.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.186.0)

* Refer to the GitHub release notes for detailed changes
</Update>

<Update label="Sep 04, 2025">
  ## v0.177.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.177.0)

## Core Improvements & Fixes

* Achieved parity between `rag` package and current implementation
  * Enhanced LLM event handling with task and agent metadata
  * Fixed mutable default arguments by replacing them with `None`
  * Suppressed Pydantic deprecation warnings during initialization
  * Fixed broken example link in `README.md`
  * Removed Python 3.12+ only Ruff rules for compatibility
  * Migrated CI workflows to use `uv` and updated dev tooling

## New Features & Enhancements

* Added tracing improvements and cleanup
  * Centralized event logic by moving `events` module to `crewai.events`

## Documentation & Guides

* Updated Enterprise Action Auth Token section documentation
  * Published documentation updates for `v0.175.0` release

## Cleanup & Refactoring

* Refactored parser into modular functions for better structure
</Update>

<Update label="Aug 28, 2025">
  ## v0.175.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.175.0)

## Core Improvements & Fixes

* Fixed migration of the `tool` section during `crewai update`
  * Reverted OpenAI pin: now requires `openai >=1.13.3` due to fixed import issues
  * Fixed flaky tests and improved test stability
  * Improved `Flow` listener resumability for HITL and cyclic flows
  * Enhanced timeout handling in `PlusAPI` and `TraceBatchManager`
  * Batched entity memory items to reduce redundant operations

## New Features & Enhancements

* Added support for additional parameters in `Flow.start()` methods
  * Displayed task names in verbose CLI output
  * Added centralized embedding types and introduced a base embedding client
  * Introduced generic clients for ChromaDB and Qdrant
  * Added support for `crewai config reset` to clear tokens
  * Enabled `crewai_trigger_payload` auto-injection
  * Simplified RAG client initialization and introduced RAG configuration system
  * Added Qdrant RAG provider support
  * Improved tracing with better event data
  * Added support to remove Auth0 and email entry on `crewai login`

## Documentation & Guides

* Added documentation for automation triggers
  * Fixed API Reference OpenAPI sources and redirects
  * Added hybrid search alpha parameter to the docs

## Cleanup & Deprecations

* Added deprecation notice for `Task.max_retries`
  * Removed Auth0 dependency from login flow
</Update>

<Update label="Aug 19, 2025">
  ## v0.165.1

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.165.1)

## Core Improvements & Fixes

* Fixed compatibility in `XMLSearchTool` by converting config values to strings for `configparser`
  * Fixed flaky Pytest test involving `PytestUnraisableExceptionWarning`
  * Mocked telemetry in test suite for more stable CI runs
  * Moved Chroma lockfile handling to `db_storage_path`
  * Ignored deprecation warnings from `chromadb`
  * Pinned OpenAI version `<1.100.0` due to `ResponseTextConfigParam` import issue

## New Features & Enhancements

* Included exchanged agent messages into `ExternalMemory` metadata
  * Automatically injected `crewai_trigger_payload`
  * Renamed internal flag `inject_trigger_input` to `allow_crewai_trigger_context`
  * Continued tracing improvements and ephemeral tracing logic
  * Consolidated tracing logic conditions
  * Added support for `agent_id`-linked memory entries in `Mem0`

## Documentation & Guides

* Added example to Tool Repository docs
  * Updated Mem0 documentation for Short-Term and Entity Memory integration
  * Revised Korean translations and improved sentence structures

* Removed deprecated AgentOps integration
</Update>

<Update label="Aug 19, 2025">
  ## v0.165.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.165.0)

## Core Improvements & Fixes

* Fixed compatibility in `XMLSearchTool` by converting config values to strings for `configparser`
  * Fixed flaky Pytest test involving `PytestUnraisableExceptionWarning`
  * Mocked telemetry in test suite for more stable CI runs
  * Moved Chroma lockfile handling to `db_storage_path`
  * Ignored deprecation warnings from `chromadb`
  * Pinned OpenAI version `<1.100.0` due to `ResponseTextConfigParam` import issue

## New Features & Enhancements

* Included exchanged agent messages into `ExternalMemory` metadata
  * Automatically injected `crewai_trigger_payload`
  * Renamed internal flag `inject_trigger_input` to `allow_crewai_trigger_context`
  * Continued tracing improvements and ephemeral tracing logic
  * Consolidated tracing logic conditions
  * Added support for `agent_id`-linked memory entries in `Mem0`

## Documentation & Guides

* Added example to Tool Repository docs
  * Updated Mem0 documentation for Short-Term and Entity Memory integration
  * Revised Korean translations and improved sentence structures

* Removed deprecated AgentOps integration
</Update>

<Update label="Aug 13, 2025">
  ## v0.159.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.159.0)

## Core Improvements & Fixes

* Improved LLM message formatting performance for better runtime efficiency
  * Fixed use of incorrect endpoint in enterprise configuration auth/parameters
  * Commented out listener resumability check for stability during partial flow resumption

## New Features & Enhancements

* Added `enterprise configure` command to CLI for streamlined enterprise setup
  * Introduced partial flow resumability support

## Documentation & Guides

* Added documentation for new tools
  * Added Korean translations
  * Updated documentation with TrueFoundry integration details
  * Added RBAC documentation and general cleanup
  * Fixed API reference and revamped examples/cookbooks across EN, PT-BR, and KO
</Update>

<Update label="Aug 06, 2025">
  ## v0.157.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.157.0)

## v0.157.0 What's Changed

## Core Improvements & Fixes

* Enabled word wrapping for long input tool
  * Allowed persisting Flow state with `BaseModel` entries
  * Optimized string operations using `partition()` for performance
  * Dropped support for deprecated User Memory system
  * Bumped LiteLLM version to `1.74.9`
  * Fixed CLI to show missing modules more clearly during import
  * Supported device authorization with Okta

## New Features & Enhancements

* Added `crewai config` CLI command group with tests
  * Added default value support for `crew.name`
  * Introduced initial tracing capabilities
  * Added support for LangDB integration
  * Added support for CLI configuration documentation

## Documentation & Guides

* Updated MCP documentation with `connect_timeout` attribute
  * Added LangDB integration documentation
  * Added CLI config documentation
  * General feature doc updates and cleanup
</Update>

<Update label="Jul 30, 2025">
  ## v0.152.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.152.0)

## Core Improvements & Fixes

* Removed `crewai signup` references and replaced them with `crewai login`
  * Fixed support for adding memories to Mem0 using `agent_id`
  * Changed the default value in Mem0 configuration
  * Updated import error to show missing module files clearly
  * Added timezone support to event timestamps

## New Features & Enhancements

* Enhanced `Flow` class to support custom flow names
  * Refactored RAG components into a dedicated top-level module

## Documentation & Guides

* Fixed incorrect model naming in Google Vertex AI documentation
</Update>

<Update label="Jul 23, 2025">
  ## v0.150.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.150.0)

## Core Improvements & Fixes

* Used file lock around Chroma client initialization
  * Removed workaround related to SQLite without FTS5
  * Dropped unsupported `stop` parameter for LLM models automatically
  * Fixed `save` method and updated related test cases
  * Fixed message handling for Ollama models when last message is from assistant
  * Removed duplicate print on LLM call error
  * Added deprecation notice to `UserMemory`
  * Upgraded LiteLLM to version 1.74.3

## New Features & Enhancements

* Added support for ad-hoc tool calling via internal LLM class
  * Updated Mem0 Storage from v1.1 to v2

## Documentation & Guides

* Fixed neatlogs documentation
  * Added Tavily Search & Extractor tools to the Search-Research suite
  * Added documentation for `SerperScrapeWebsiteTool` and reorganized Serper section
  * General documentation updates and improvements

## crewai-tools v0.58.0

### New Tools / Enhancements

* **SerperScrapeWebsiteTool**: Added a tool for extracting clean content from URLs
  * **Bedrock AgentCore**: Integrated browser and code interpreter toolkits for Bedrock agents
  * **Stagehand Update**: Refactored and updated Stagehand integration

* **FTS5 Support**: Enabled SQLite FTS5 for improved text search in test workflows
  * **Test Speedups**: Parallelized GitHub Actions test suite for faster CI runs
  * **Cleanup**: Removed SQLite workaround due to FTS5 support being available
    **MongoDBVectorSearchTool**: Fixed serialization and schema handling
</Update>

<Update label="Jul 16, 2025">
  ## v0.148.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.148.0)

## Core Improvements & Fixes

* Used production WorkOS environment ID
  * Added SQLite FTS5 support to test workflow
  * Fixed agent knowledge handling
  * Compared using `BaseLLM` class instead of `LLM`
  * Fixed missing `create_directory` parameter in `Task` class

## New Features & Enhancements

* Introduced Agent evaluation functionality
  * Added Evaluator experiment and regression testing methods
  * Implemented thread-safe `AgentEvaluator`
  * Enabled event emission for Agent evaluation
  * Supported evaluation of single `Agent` and `LiteAgent`
  * Added integration with `neatlogs`
  * Added crew context tracking for LLM guardrail events

## Documentation & Guides

* Added documentation for `guardrail` attributes and usage examples
  * Added integration guide for `neatlogs`
  * Updated documentation for Agent repository and `Agent.kickoff` usage
</Update>

<Update label="Jul 09, 2025">
  ## v0.141.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.141.0)

## Core Improvements & Fixes

* Sped up GitHub Actions tests through parallelization

## New Features & Enhancements

* Added crew context tracking for LLM guardrail events

## Documentation & Guides

* Added documentation for Agent repository usage
  * Added documentation for `Agent.kickoff` method
</Update>

<Update label="Jul 02, 2025">
  ## v0.140.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.140.0)

## Core Improvements & Fixes

* Fixed typo in test prompts
  * Fixed project name normalization by stripping trailing slashes during crew creation
  * Ensured environment variables are written in uppercase
  * Updated LiteLLM dependency
  * Refactored collection handling in `RAGStorage`
  * Implemented PEP 621 dynamic versioning

## New Features & Enhancements

* Added capability to track LLM calls by task and agent
  * Introduced `MemoryEvents` to monitor memory usage
  * Added console logging for memory system and LLM guardrail events
  * Improved data training support for models up to 7B parameters
  * Added Scarf and Reo.dev analytics tracking
  * CLI workos login

## Documentation & Guides

* Updated CLI LLM documentation
  * Added Nebius integration to the docs
  * Corrected typos in installation and pt-BR documentation
  * Added docs about `MemoryEvents`
  * Implemented docs redirects and included development tools
</Update>

<Update label="Jun 25, 2025">
  ## v0.134.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.134.0)

## Core Improvements & Fixes

* Fixed tools parameter syntax
  * Fixed type annotation in `Task`
  * Fixed SSL error when retrieving LLM data from GitHub
  * Ensured compatibility with Pydantic 2.7.x
  * Removed `mkdocs` from project dependencies
  * Upgraded Langfuse code examples to use Python SDK v3
  * Added sanitize role feature in `mem0` storage
  * Improved Crew search during memory reset
  * Improved console printer output

## New Features & Enhancements

* Added support for initializing a tool from defined `Tool` attributes
  * Added official way to use MCP Tools within a `CrewBase`
  * Enhanced MCP tools support to allow selecting multiple tools per agent in `CrewBase`
  * Added Oxylabs Web Scraping tools

## Documentation & Guides

* Updated `quickstart.mdx`
  * Added docs on `LLMGuardrail` events
  * Updated documentation with comprehensive service integration details
  * Updated recommendation filters for MCP and Enterprise tools
  * Updated docs for Maxim observability
  * Added pt-BR documentation translation
  * General documentation improvements
</Update>

<Update label="Jun 12, 2025">
  ## v0.130.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.130.0)

## Core Improvements & Fixes

* Removed duplicated message related to Tool result output
  * Fixed missing `manager_agent` tokens in `usage_metrics` from kickoff
  * Fixed telemetry singleton to respect dynamic environment variables
  * Fixed issue where Flow status logs could hide human input
  * Increased default X-axis spacing for flow plotting

## New Features & Enhancements

* Added support for multi-org actions in the CLI
  * Enabled async tool executions for more efficient workflows
  * Introduced `LiteAgent` with Guardrail integration
  * Upgraded `LiteLLM` to support latest OpenAI version

## Documentation & Guides

* Documented minimum `UV` version for Tool repository
  * Improved examples for Hallucination Guardrail
  * Updated planning docs for LLM usage
  * Added documentation for Maxim support in Agent observability
  * Expanded integrations documentation with images for enterprise features
  * Fixed guide on persistence
  * Updated Python version support to support python 3.13.x
</Update>

<Update label="Jun 05, 2025">
  ## v0.126.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.126.0)

#### Core Improvements & Fixes

* Added support for Python 3.13
  * Fixed agent knowledge sources issue
  * Persisted available tools from a Tool repository
  * Enabled tools to be loaded from Agent repository via their own module
  * Logged usage of tools when called by an LLM

#### New Features & Enhancements

* Added streamable-http transport support in MCP integration
  * Added support for community analytics
  * Expanded OpenAI-compatible section with a Gemini example
  * Introduced transparency features for prompts and memory systems
  * Minor enhancements for Tool publishing

#### Documentation & Guides

* Major restructuring of docs for better navigation
  * Expanded MCP integration documentation
  * Updated memory docs and README visuals
  * Fixed missing await keywords in async kickoff examples
  * Updated Portkey and Azure embeddings documentation
  * Added enterprise testing image to the LLM guide
  * General updates to the README
</Update>

<Update label="May 27, 2025">
  ## v0.121.1

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.121.1)

Bug fixes and better docs
</Update>

<Update label="May 22, 2025">
  ## v0.121.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.121.0)

## Core Improvements & Fixes

* Fixed encoding error when creating tools
  * Fixed failing llama test
  * Updated logging configuration for consistency
  * Enhanced telemetry initialization and event handling

## New Features & Enhancements

* Added markdown attribute to the Task class
  * Added reasoning attribute to the Agent class
  * Added inject\_date flag to Agent for automatic date injection
  * Implemented HallucinationGuardrail (no-op with test coverage)

## Documentation & Guides

* Added documentation for StagehandTool and improved MDX structure
  * Added documentation for MCP integration and updated enterprise docs
  * Documented knowledge events and updated reasoning docs
  * Added stop parameter documentation
  * Fixed import references in doc examples (before\_kickoff, after\_kickoff)
  * General docs updates and restructuring for clarity
</Update>

<Update label="May 15, 2025">
  ## v0.120.1

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.120.1)

* Fixes Interpolation with hyphens
</Update>

<Update label="May 14, 2025">
  ## v0.120.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.120.0)

### Core Improvements & Fixes

•	Enabled full Ruff rule set by default for stricter linting
  •	Addressed race condition in FilteredStream using context managers
  •	Fixed agent knowledge reset issue
  •	Refactored agent fetching logic into utility module

### New Features & Enhancements

•	Added support for loading an Agent directly from a repository
  •	Enabled setting an empty context for Task
  •	Enhanced Agent repository feedback and fixed Tool auto-import behavior
  •	Introduced direct initialization of knowledge (bypassing knowledge\_sources)

### Documentation & Guides

•	Updated security.md for current security practices
  •	Cleaned up Google setup section for clarity
  •	Added link to AI Studio when entering Gemini key
  •	Updated Arize Phoenix observability guide
  •	Refreshed flow documentation
</Update>

<Update label="May 08, 2025">
  ## v0.119.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.119.0)

## Core Improvements & Fixes

* Improved test reliability by enhancing pytest handling for flaky tests
  * Fixed memory reset crash when embedding dimensions mismatch
  * Enabled parent flow identification for Crew and LiteAgent
  * Prevented telemetry-related crashes when unavailable
  * Upgraded LiteLLM version for better compatibility
  * Fixed llama converter tests by removing skip\_external\_api

## New Features & Enhancements

* Introduced knowledge retrieval prompt re-writting in Agent for improved tracking and debugging
  * Made LLM setup and quickstart guides model-agnostic

## Documentation & Guides

* Added advanced configuration docs for the RAG tool
  * Updated Windows troubleshooting guide
  * Refined documentation examples for better clarity
  * Fixed typos across docs and config files
</Update>

<Update label="Apr 30, 2025">
  ## v0.118.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.118.0)

### Core Improvements & Fixes

* Fixed issues with missing prompt or system templates.
  * Removed global logging configuration to avoid unintended overrides.
  * Renamed TaskGuardrail to LLMGuardrail for improved clarity.
  * Downgraded litellm to version 1.167.1 for compatibility.
  * Added missing **init**.py files to ensure proper module initialization.

### New Features & Enhancements

* Added support for no-code Guardrail creation to simplify AI behavior controls.

### Documentation & Guides

* Removed CrewStructuredTool from public documentation to reflect internal usage.
  * Updated enterprise documentation and YouTube embed for improved onboarding experience.
</Update>

<Update label="Apr 28, 2025">
  ## v0.117.1

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.117.1)

* build: upgrade crewai-tools
  * upgrade liteLLM to latest version
  * Fix Mem0 OSS
</Update>

<Update label="Apr 28, 2025">
  ## v0.117.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.117.0)

## New Features & Enhancements

* Added `result_as_answer` parameter support in `@tool` decorator.
  * Introduced support for new language models: GPT-4.1, Gemini-2.0, and Gemini-2.5 Pro.
  * Enhanced knowledge management capabilities.
  * Added Huggingface provider option in CLI.
  * Improved compatibility and CI support for Python 3.10+.

## Core Improvements & Fixes

* Fixed issues with incorrect template parameters and missing inputs.
  * Improved asynchronous flow handling with coroutine condition checks.
  * Enhanced memory management with isolated configuration and correct memory object copying.
  * Fixed initialization of lite agents with correct references.
  * Addressed Python type hint issues and removed redundant imports.
  * Updated event placement for improved tool usage tracking.
  * Raised explicit exceptions when flows fail.
  * Removed unused code and redundant comments from various modules.
  * Updated GitHub App token action to v2.

## Documentation & Guides

* Enhanced documentation structure, including enterprise deployment instructions.
  * Automatically create output folders for documentation generation.
  * Fixed broken link in `WeaviateVectorSearchTool` documentation.
  * Fixed guardrail documentation usage and import paths for JSON search tools.
  * Updated documentation for `CodeInterpreterTool`.
  * Improved SEO, contextual navigation, and error handling for documentation pages.
</Update>

<Update label="Apr 10, 2025">
  ## v0.114.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.114.0)

## New Features & Enhancements

* Agents as an atomic unit. (`Agent(...).kickoff()`)
  * Support to Custom LLM implementations.
  * Integrated External Memory and Opik observability.
  * Enhanced YAML extraction.
  * Multimodal agent validation.
  * Added Secure fingerprints for agents and crews.

## Core Improvements & Fixes

* Improved serialization, agent copying, and Python compatibility.
  * Added wildcard support to emit()
  * Added support for additional router calls and context window adjustments.
  * Fixed typing issues, validation, and import statements.
  * Improved method performance.
  * Enhanced agent task handling, event emissions, and memory management.
  * Fixed CLI issues, conditional tasks, cloning behavior, and tool outputs.

## Documentation & Guides

* Improved documentation structure, theme, and organization.
  * Added guides for Local NVIDIA NIM with WSL2, W\&B Weave, and Arize Phoenix.
  * Updated tool configuration examples, prompts, and observability docs.
  * Guide on using singular agents within Flows
</Update>

<Update label="Mar 17, 2025">
  ## v0.108.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.108.0)

* Converted tabs to spaces in crew\.py template in PR #2190
  * Enhanced LLM Streaming Response Handling and Event System in PR #2266
  * Included model\_name in PR #2310
  * Enhanced Event Listener with rich visualization and improved logging in PR #2321
  * Added fingerprints in PR #2332

* Fixed Mistral issues in PR #2308
  * Fixed a bug in documentation in PR #2370
  * Fixed type check error in fingerprint property in PR #2369

# Documentation Updates

* Improved tool documentation in PR #2259
  * Updated installation guide for the uv tool package in PR #2196
  * Added instructions for upgrading crewAI with the uv tool in PR #2363
  * Added documentation for ApifyActorsTool in PR #2254
</Update>

<Update label="Mar 09, 2025">
  ## v0.105.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.105.0)

**Core Improvements & Fixes**

* Fixed issues with missing template variables and user memory configuration.
  * Improved async flow support and addressed agent response formatting.
  * Enhanced memory reset functionality and fixed CLI memory commands.
  * Fixed type issues, tool calling properties, and telemetry decoupling.

**New Features & Enhancements**

* Added Flow state export and improved state utilities.
  * Enhanced agent knowledge setup with optional crew embedder.
  * Introduced event emitter for better observability and LLM call tracking.
  * Added support for Python 3.10 and ChatOllama from langchain\_ollama.
  * Integrated context window size support for the o3-mini model.
  * Added support for multiple router calls.

**Documentation & Guides**

* Improved documentation layout and hierarchical structure.
  * Added QdrantVectorSearchTool guide and clarified event listener usage.
  * Fixed typos in prompts and updated Amazon Bedrock model listings.
</Update>

<Update label="Feb 13, 2025">
  ## v0.102.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.102.0)

### Core Improvements & Fixes

* Enhanced LLM Support: Improved structured LLM output, parameter handling, and formatting for Anthropic models.
  * Crew & Agent Stability: Fixed issues with cloning agents/crews using knowledge sources, multiple task outputs in conditional tasks, and ignored Crew task callbacks.
  * Memory & Storage Fixes: Fixed short-term memory handling with Bedrock, ensured correct embedder initialization, and added a reset memories function in the crew class.
  * Training & Execution Reliability: Fixed broken training and interpolation issues with dict and list input types.

### New Features & Enhancements

* Advanced Knowledge Management: Improved naming conventions and enhanced embedding configuration with custom embedder support.
  * Expanded Logging & Observability: Added JSON format support for logging and integrated MLflow tracing documentation.
  * Data Handling Improvements: Updated excel\_knowledge\_source.py to process multi-tab files.
  * General Performance & Codebase Clean-Up: Streamlined enterprise code alignment and resolved linting issues.
  * Adding new tool QdrantVectorSearchTool

### Documentation & Guides

* Updated AI & Memory Docs: Improved Bedrock, Google AI, and long-term memory documentation.
  * Task & Workflow Clarity: Added "Human Input" row to Task Attributes, Langfuse guide, and FileWriterTool documentation.
  * Fixed Various Typos & Formatting Issues.

### Maintenance & Miscellaneous

* Refined Google Docs integrations and task handling for the current year.
</Update>

<Update label="Jan 28, 2025">
  ## v0.100.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.100.0)

* Feat: Add Composio docs
  * Feat: Add SageMaker as a LLM provider
  * Fix: Overall LLM connection issues
  * Fix: Using safe accessors on training
  * Fix: Add version check to crew\_chat.py
  * Docs: New docs for crewai chat
  * Docs: Improve formatting and clarity in CLI and Composio Tool docs
</Update>

<Update label="Jan 20, 2025">
  ## v0.98.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.98.0)

* Feat: Conversation crew v1
  * Feat: Add unique ID to flow states
  * Feat: Add @persist decorator with FlowPersistence interface
  * Integration: Add SambaNova integration
  * Integration: Add NVIDIA NIM provider in cli
  * Integration: Introducing VoyageAI
  * Chore: Update date to current year in template
  * Fix: Fix API Key Behavior and Entity Handling in Mem0 Integration
  * Fix: Fixed core invoke loop logic and relevant tests
  * Fix: Make tool inputs actual objects and not strings
  * Fix: Add important missing parts to creating tools
  * Fix: Drop litellm version to prevent windows issue
  * Fix: Before kickoff if inputs are none
  * Fix: TYPOS
  * Fix: Nested pydantic model issue
  * Fix: Docling issues
  * Fix: union issue
  * Docs updates
</Update>

<Update label="Jan 04, 2025">
  ## v0.95.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.95.0)

* Feat: Adding Multimodal Abilities to Crew
  * Feat: Programatic Guardrails
  * Feat: HITL multiple rounds
  * Feat: Gemini 2.0 Support
  * Feat: CrewAI Flows Improvements
  * Feat: Add Workflow Permissions
  * Feat: Add support for langfuse with litellm
  * Feat: Portkey Integration with CrewAI
  * Feat: Add interpolate\_only method and improve error handling
  * Feat: Docling Support
  * Feat: Weviate Support
  * Fix: output\_file not respecting system path
  * Fix disk I/O error when resetting short-term memory.
  * Fix: CrewJSONEncoder now accepts enums
  * Fix: Python max version
  * Fix: Interpolation for output\_file in Task
  * Fix: Handle coworker role name case/whitespace properly
  * Fix: Add tiktoken as explicit dependency and document Rust requirement
  * Fix: Include agent knowledge in planning process
  * Fix: Change storage initialization to None for KnowledgeStorage
  * Fix: Fix optional storage checks
  * Fix: include event emitter in flows
  * Fix: Docstring, Error Handling, and Type Hints Improvements
  * Fix: Suppressed userWarnings from litellm pydantic issues
</Update>

<Update label="Dec 05, 2024">
  ## v0.86.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.86.0)

* remove all references to pipeline and pipeline router
  * docs: Add Nvidia NIM as provider in Custom LLM
  * add knowledge demo + improve knowledge docs
  * Brandon/cre 509 hitl multiple rounds of followup
  * New docs about yaml crew with decorators. Simplify template crew
</Update>

<Update label="Dec 04, 2024">
  ## v0.85.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.85.0)

* Added knowledge to agent level
  * Feat/remove langchain
  * Improve typed task outputs
  * Log in to Tool Repository on `crewai login`
  * Fixes issues with result as answer not properly exiting LLM loop
  * fix: missing key name when running with ollama provider
  * fix spelling issue found
  * Update readme for running mypy
  * Add knowledge to mint.json
  * Update Github actions
  * Docs Update Agents docs to include two approaches for creating an agent
  * Documentation Improvements: LLM Configuration and Usage
</Update>

<Update label="Nov 25, 2024">
  ## v0.83.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.83.0)

* New `before_kickoff` and `after_kickoff` crew callbacks
  * Support to pre-seed agents with Knowledge
  * Add support for retrieving user preferences and memories using Mem0
  * Fix Async Execution
  * Upgrade chroma and adjust embedder function generator
  * Update CLI Watson supported models + docs
  * Reduce level for Bandit
  * Fixing all tests
  * Update Docs
</Update>

<Update label="Nov 14, 2024">
  ## v0.80.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.80.0)

* Fixing Tokens callback replacement bug
  * Fixing Step callback issue
  * Add cached prompt tokens info on usage metrics
  * Fix crew\_train\_success test
</Update>

<Update label="Nov 11, 2024">
  ## v0.79.4

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.79.4)

Series of small bug fixes around llms support
</Update>

<Update label="Nov 10, 2024">
  ## v0.79.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.79.0)

* Add inputs to flows
  * Enhance log storage to support more data types
  * Add support to IBM memory
  * Add Watson as an option in CLI
  * Add security.md file
  * Replace .netrc with uv environment variables
  * Move BaseTool to main package and centralize tool description generation
  * Raise an error if an LLM doesnt return a response
  * Fix flows to support cycles and added in test
  * Update how we name crews and fix missing config
  * Update docs
</Update>

<Update label="Oct 30, 2024">
  ## v0.76.9

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.76.9)

* Update plot command for flow to crewai flow plot
  * Add tomli so we can support 3.10
  * Forward install command options to `uv sync`
  * Improve tool text description and args
  * Improve tooling and flow docs
  * Update flows cli to allow you to easily add additional crews to a flow with crewai flow add-crew
  * Fixed flows bug when using multiple start and listen(and\_(..., ..., ...))
</Update>

<Update label="Oct 23, 2024">
  ## v0.76.2

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.76.2)

Updating crewai create commadn
</Update>

<Update label="Oct 23, 2024">
  ## v0.76.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.76.0)

* fix/fixed missing API prompt + CLI docs update
  * chore(readme): fixing step for 'running tests' in the contribution
  * support unsafe code execution. add in docker install and running checks
  * Fix memory imports for embedding functions by
</Update>

<Update label="Oct 23, 2024">
  ## v0.75.1

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.75.1)

new `--provider` option on crewai crewat
</Update>

<Update label="Oct 23, 2024">
  ## v0.75.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.75.0)

* Fixing test post training
  * Simplify flows
  * Adapt `crewai tool install <tool>`
  * Ensure original embedding config works
  * Fix bugs
  * Update docs - Including adding Cerebras LLM example configuration to LLM docs
  * Drop unnecessary tests
</Update>

<Update label="Oct 18, 2024">
  ## v0.74.2

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.74.2)

* feat: add poetry.lock to uv migration
  * fix tool calling issue
</Update>

<Update label="Oct 18, 2024">
  ## v0.74.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.74.0)

* UV migration
  * Adapt Tools CLI to UV
  * Add warning from Poetry -> UV
  * CLI to allow for model selection & submitting API keys
  * New Memory Base
  * Fix Linting and Warnings
  * Update Docs
  * Bug fixesh
</Update>

<Update label="Oct 11, 2024">
  ## v0.70.1

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.70.1)

* New Flow feature
  * Flow visualizer
  * Create `crewai create flow` command
  * Create `crewai tool create <tool>` command
  * Add Git validations for publishing tools
  * fix: JSON encoding date objects
  * New Docs
  * Update README
  * Bug fixes
</Update>

<Update label="Sep 27, 2024">
  ## v0.65.2

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.65.2)

* Adding experimental Flows feature
  * Fixing order of tasks bug
  * Updating templates
</Update>

<Update label="Sep 27, 2024">
  ## v0.64.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.64.0)

* Ordering tasks properly
  * Fixing summarization logic
  * Fixing stop words logic
  * Increases default max iterations to 20
  * Fix crew's key after input interpolation
  * Fixing Training Feature
  * Adding initial tools API
  * TYPOS
  * Updating Docs

Fixes: #1359 #1355 #1353 #1356 and others
</Update>

<Update label="Sep 25, 2024">
  ## v0.63.6

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.63.6)

* Updating projects templates
</Update>

<Update label="Sep 25, 2024">
  ## v0.63.5

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.63.5)

* Bringing support to o1 family back, and any model that don't support stop words
  * Updating dependencies
  * Updating logs
  * Updating docs
</Update>

<Update label="Sep 24, 2024">
  ## v0.63.2

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.63.2)

* Adding OPENAI\_BASE\_URL as fallback
  * Adding proper LLM import
  * Updating docs
</Update>

<Update label="Sep 24, 2024">
  ## v0.63.1

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.63.1)

* Small bug fix for support future CrewAI deploy
</Update>

<Update label="Sep 24, 2024">
  ## v0.63.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.63.0)

* New LLM class to interact with LLMs (leveraging LiteLLM)
  * Adding support to custom memory interfaces
  * Bringing GPT-4o-mini as the default model
  * Updates Docs
  * Updating dependencies
  * Bug fixes
    * Remove redundant task creation in `kickoff_for_each_async`
</Update>

<Update label="Sep 18, 2024">
  ## v0.61.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.61.0)

* Updating dependencies
  * Printing max rpm message in different color
  * Updating all cassettes for tests
  * Always ending on a user message - to better support certain models like bedrock ones
  * Overall small bug fixes
</Update>

<Update label="Sep 16, 2024">
  ## v0.60.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.60.0)

* Removing LangChain and Rebuilding Executor
  * Get all of out tests back to green
  * Adds the ability to not use system prompt use\_system\_prompt on the Agent
  * Adds the ability to not use stop words (to support o1 models) use\_stop\_words on the Agent
  * Sliding context window gets renamed to respect\_context\_window, and enable by default
  * Delegation is now disabled by default
  * Inner prompts were slightly changed as well
  * Overall reliability and quality of results
  * New support for:
    * Number of max requests per minute
    * A maximum number of iterations before giving a final answer
    * Proper take advantage of system prompts
    * Token calculation flow
    * New logging of the crew and agent execution
</Update>

<Update label="Sep 13, 2024">
  ## v0.55.2

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.55.2)

* Adding ability for auto complete
  * Add name and expected\_output to TaskOutput
  * New `crewai install` CLI
  * New `crewai deploy` CLI
  * Cleaning up of Pipeline feature
  * Updated docs
  * Dev experience improvements like bandit CI pipeline
  * Fix bugs:
    * Ability to use `planning_llm`
    * Fix YAML based projects
    * Fix Azure support
    * Add support to Python 3.10
    * Moving away from Pydantic v1
</Update>

<Update label="Aug 11, 2024">
  ## v0.51.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.51.0)

* crewAI Testing / Evaluation - [https://docs.crewai.com/core-concepts/Testing/](https://docs.crewai.com/core-concepts/Testing/)
  * Adding new sliding context window
  * Allowing all attributes on YAML - [https://docs.crewai.com/getting-started/Start-a-New-CrewAI-Project-Template-Method/#customizing-your-project](https://docs.crewai.com/getting-started/Start-a-New-CrewAI-Project-Template-Method/#customizing-your-project)
  * Adding initial Pipeline Structure - [https://docs.crewai.com/core-concepts/Pipeline/](https://docs.crewai.com/core-concepts/Pipeline/)
  * Ability to set LLM for planning step - [https://docs.crewai.com/core-concepts/Planning/](https://docs.crewai.com/core-concepts/Planning/)
  * New crew run command - [https://docs.crewai.com/getting-started/Start-a-New-CrewAI-Project-Template-Method/#running-your-project](https://docs.crewai.com/getting-started/Start-a-New-CrewAI-Project-Template-Method/#running-your-project)
  * Saving file now dumps dict into JSON - [https://docs.crewai.com/core-concepts/Tasks/#creating-directories-when-saving-files](https://docs.crewai.com/core-concepts/Tasks/#creating-directories-when-saving-files)
  * Using verbose settings for tool outputs
  * Added new Github Templates
  * New Vision tool - [https://docs.crewai.com/tools/VisionTool/](https://docs.crewai.com/tools/VisionTool/)
  * New DALL-E Tool - [https://docs.crewai.com/tools/DALL-ETool/](https://docs.crewai.com/tools/DALL-ETool/)
  * New MySQL tool - [https://docs.crewai.com/tools/MySQLTool/](https://docs.crewai.com/tools/MySQLTool/)
  * New NL2SQL Tool - [https://docs.crewai.com/tools/NL2SQLTool.md](https://docs.crewai.com/tools/NL2SQLTool.md)
  * Bug Fixes:
    * Bug with planning feature output
    * Async tasks for hierarchical process
    * Better pydantic output for non OAI models
    * JSON truncation issues
    * Fix logging types
    * Only import AgentOps if the Env Key is set
    * Sanitize agent roles to ensure valid directory names (Windows)
    * Tools name shouldn't contain space for OpenAI
    * A bunch of minor issues
</Update>

<Update label="Jul 20, 2024">
  ## v0.41.1

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.41.1)

* Fix bug with planning feature
</Update>

<Update label="Jul 19, 2024">
  ## v0.41.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.41.0)

* **\[Breaking Change]** Type Safe output
    * All crews and tasks now return a proper object TaskOuput and CrewOutput
  * **\[Feature]** New planning feature for crews (plan before act)
    * by adding planning=True to the Crew instance
  * **\[Feature]** Introduced Replay Feature
    * New CLI that allow you to list the tasks from last run and replay from a specific one
  * **\[Feature]** Ability to reset memory
    * You can clean your crew memory before running it again
  * **\[Feature]** Add retry feature for LLM calls
    * You can retry llm calls and not stop the crew execution
  * **\[Feature]** Added ability to customize converter
  * **\[Tool]** Enhanced tools with type hinting and new attributes
  * **\[Tool]** Added MultiON Tool
  * **\[Tool]** Fixed filecrawl tools
  * **\[Tool]** Fixed bug in Scraping tool
  * **\[Tools]** Bumped crewAI-tools dependency to version
  * **\[Bugs]** General bug fixes and improvements
  * **\[Bugs]** Telemetry fixes
  * **\[Bugs]** Spell check corrections
  * **\[Docs]** Updated documentation
</Update>

<Update label="Jul 06, 2024">
  ## v0.36.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.36.0)

* Bug fix
  * Updating Docs
  * Updating native prompts
  * Fixing TYPOs on the prompts
  * Adding AgentOps native support
  * Adding Firecrawl Tools
  * Adding new ability to return a tool results as an agent result
  * Improving coding Interpreter tool
  * Adding new option to create your own corveter class (docs pending)
</Update>

<Update label="Jul 04, 2024">
  ## v0.35.8

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.35.8)

* fixing embechain dependency issue
</Update>

<Update label="Jul 02, 2024">
  ## v0.35.7

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.35.7)

* New @composiohq integration is out
  * Documentation update
  * Custom GPT Updated
  * Adjusting manager verbosity level
  * Bug fixes
</Update>

<Update label="Jul 01, 2024">
  ## v0.35.5

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.35.5)

* Fix embedchain dependency
</Update>

<Update label="Jul 01, 2024">
  ## v0.35.4

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.35.4)

* Updating crewai create CLI to use the new version
</Update>

<Update label="Jul 01, 2024">
  ## v0.35.3

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.35.3)

* Code Execution Bug fixed
  * Updating overall docs
  * Bumping version of crewai-tools
  * Bumping versions of many dependencies
  * Overall bugfixes
</Update>

<Update label="Jun 29, 2024">
  ## v0.35.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.35.0)

* Your agents can now execute code
  * Bring Any 3rd-party agent, LlamaIndex, LangChain and Autogen  agents can all be part of your crew now!
  * Train you crew before you execute it and get consistent results! New CLI `crewai train -n X`
  * Bug fixes and docs updates (still missing some new docs updates coming soon)
</Update>

<Update label="Jun 22, 2024">
  ## v0.32.2

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.32.2)

* Updating `crewai create` CLI to use the new version
  * Fixing delegation agent matching
</Update>

<Update label="Jun 21, 2024">
  ## v0.32.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.32.0)

* New `kickoff_for_each`, `kickoff_async` and `kickoff_for_each_async` methods for better control over the kickoff process
  * Adding support for all LlamaIndex hub integrations
  * Adding `usage_metrics` to full output or a crew
  * Adding support to multiple crews on the new YAML format
  * Updating dependencies
  * Fixed Bugs and TYPOs
  * Documentation updated
  * Added search in docs
  * Making gpt-4o the default model
  * Adding new docs for LangTrace, Browserbase and Exa Search
  * Adding timestamp to logging
</Update>

<Update label="May 23, 2024">
  ## v0.30.11

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.30.11)

* Updating project generation template
</Update>

<Update label="May 14, 2024">
  ## v0.30.8

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.30.8)

* Updating dependencies
  * Small bug fixes on crewAI project structure
  * Removing custom YAML parser for now
</Update>

<Update label="May 14, 2024">
  ## v0.30.5

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.30.5)

* Making agent delegation more versatile for smaller models
</Update>

<Update label="May 13, 2024">
  ## v0.30.4

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.30.4)

**Docs Update will follow** sorry about that and thank you for bearing with me, we are launching new docs soon!

➿  Fixing task callback
  🧙  Ability to set a specific agent as manager instead of having crew create your one
  📄  Ability to set system, prompt and response templates, so it works more reliable with opensource models (works better with smaller models)
  👨‍💻  Improving json and pydantic output (works better with smaller models)
  🔎 Improving tool name recognition (works better with smaller models)
  🧰  Improvements for tool usage (works better with smaller models)
  📃  Initial support to bring your own prompts
  2️⃣  Fixing duplicating token calculator metrics
  🪚  Adding couple new tools, Browserbase and Exa Search
  📁  Ability to create directory when saving as file
  🔁  Updating dependencies - double check tools
  📄  Overall small documentation improvements
  🐛  Smaller bug fixes (typos and such)
  👬  Fixing co-worker / coworker issues
  👀  Smaller Readme Updates
</Update>

<Update label="Apr 11, 2024">
  ## v0.28.8

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.28.8)

* updating version used on crewai CLI
</Update>

<Update label="Apr 11, 2024">
  ## v0.28.7

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/0.28.7)

* Bug fixes
  * Updating crewAI tool version with bug fixes
</Update>

<Update label="Apr 08, 2024">
  ## v0.28.5

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.28.5)

* Major Long term memory interpolation issue
  * Updating tools package dependency with fixes
  * Removing unnecessary certificate
</Update>

<Update label="Apr 07, 2024">
  ## v0.28.2

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.28.2)

* Major long term memory fix
</Update>

<Update label="Apr 06, 2024">
  ## v0.28.1

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.28.1)

* Updating crewai-tools to 0.1.15
</Update>

<Update label="Apr 05, 2024">
  ## v0.28.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.28.0)

* Not overriding LLM callbacks
  * Adding `max_execution_time` support
  * Adding specific memory docs
  * Moving tool usage logging color to purple from yellow
  * Updating Docs
</Update>

<Update label="Apr 04, 2024">
  ## v0.27.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.27.0)

* 🧠 **Memory (shared crew memory)** - To enable it just add `memory=True` to your crew, it will work transparently and make outcomes better and more reliable, it's disable by default for now
  * 🤚🏼 **Native Human Input Support:** [docs](https://docs.crewai.com/how-to/Human-Input-on-Execution/)
  * 🌐 **Universal RAG Tools Support:** Any models, beyond just OpenAI. [Example](https://docs.crewai.com/tools/DirectorySearchTool/#custom-model-and-embeddings)
  * 🔍 **Enhanced Cache Control:** Meet the ingenious cache\_function attribute: [docs](https://docs.crewai.com/core-concepts/Tools/#custom-caching-mechanism)
  * 🔁 **Updated crewai-tools Dependency:** Always in sync with the latest and greatest.
  * ⛓️ **Cross Agent Delegation:** Smoother cooperation between agents.
  * 💠 **Inner Prompt Improvements:** A finer conversational flow.
  * 📝 **Improving tool usage with better parsing**
  * 🔒 **Security improvements and updating dependencies**
  * 📄 **Documentation improved**
  * 🐛 **Bug fixes**
</Update>

<Update label="Mar 12, 2024">
  ## v0.22.5

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.22.5)

* Other minor import issues on the new templates
</Update>

<Update label="Mar 12, 2024">
  ## v0.22.4

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.22.4)

Fixing template issues
</Update>

<Update label="Mar 11, 2024">
  ## v0.22.2

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.22.2)

* Fixing bug on the new cli template
  * Guaranteeing tasks order on new cli template
</Update>

<Update label="Mar 11, 2024">
  ## v0.22.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.22.0)

* Adding initial CLI `crewai create` command
  * Adding ability to agents and tasks to be defined using dictionaries
  * Adding more clear agent logging
  * Fixing bug Exceed maximum recursion depth bug
  * Fixing docs
  * Updating README
</Update>

<Update label="Mar 04, 2024">
  ## v0.19.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.19.0)

* Efficiency in tool usage +1023.21%
  * Mean tools used +276%
  * Tool errors slashed by 67%, more reliable than ever.
  * Delegation capabilities enhanced
  * Ability to fallback to function calling by setting `function_calling_llm` to Agent or Crew
  * Ability to get crew execution metrics after `kickoff` with `crew.usage_metrics`
  * Adding ability for inputs being passed in kickoff now `crew.kickoff(inputs: {'key': 'value})`
  * Updating Docs
</Update>

<Update label="Feb 28, 2024">
  ## v0.16.3

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.16.3)

* Fixing overall bugs
  * Making sure code is backwards compatible
</Update>

<Update label="Feb 28, 2024">
  ## v0.16.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.16.0)

* Removing lingering `crewai_tools` dependency
  * Adding initial support for inputs interpolation (missing docs)
  * Adding ability to track tools usage, tools error, formatting errors, tokens usage
  * Updating README
</Update>

<Update label="Feb 26, 2024">
  ## v0.14.4

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.14.4)

* Updating timeouts
  * Updating docs
  * Removing crewai\_tools as a mandatory
  * Making agents memory-less by default for token count reduction (breaking change for people counting on this previously)
</Update>

<Update label="Feb 24, 2024">
  ## v0.14.3

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.14.3)

* Fixing broken docs link
  * Adding support for agents without tools
  * Avoid empty task outputs
</Update>

<Update label="Feb 22, 2024">
  ## v0.14.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.14.0)

All improvements from the v0.14.0rc.

* Support to export json and pydantic from opensource models
</Update>

<Update label="Feb 20, 2024">
  ## v0.14.0rc

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.14.0rc0)

* Adding support to crewai-tools
  * Adding support to format tasks output as Pydantic Objects Or JSON
  * Adding support to save tasks ouput to a file
  * Improved reliability for inter agent delegation
  * Revamp tools usage logic to proper use function calling
  * Updating internal prompts
  * Supporting tools with no arguments
  * Bug fixes
</Update>

<Update label="Feb 16, 2024">
  ## v0.11.2

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.11.2)

* Adding further error logging so users understand what is happening if a tool fails
</Update>

<Update label="Feb 16, 2024">
  ## v0.11.1

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.11.1)

* It fixes a  bug on the tool usage logic that was early caching the result even if there was an error on the usage, preventing it from using the tool again.
  * It will also print any error message in red allowing the user to understand what was the problem with the tool.
</Update>

<Update label="Feb 13, 2024">
  ## v0.11.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.11.0)

* Ability to set `function_calling_llm` on both the entire crew and individual agents
  * Some early attempts on cost reduction
  * Improving function calling for tools
  * Updates docs
</Update>

<Update label="Feb 10, 2024">
  ## v0.10.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.10.0)

* Ability to get `full_ouput` from crew kickoff with all tasks outputs
  * Ability to set `step_callback` function for both Agents and Crews so you can get all intermediate steps
  * Remembering Agent of the expected format after certain number of tool usages.
  * New tool usage internals now using json, unlocking tools with multiple arguments
  * Refactoring overall delegation logic, now way more reliable
  * Fixed `max_inter` bug now properly forcing llm to answer as it gets to that
  * Rebuilt caching structure, making sure multiple agents can use the same cache
  * Refactoring Task repeated usage prevention logic
  * Removing now unnecessary `CrewAgentOutputParser`
  * Opt-in to share complete crew related data with the crewAI team
  * Overall Docs update
</Update>

<Update label="Feb 08, 2024">
  ## v0.5.5

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.5.5)

* Overall doc + readme improvements
  * Fixing RPM controller being set unnecessarily
  * Adding early stage anonymous telemetry for lib improvement
</Update>

<Update label="Feb 07, 2024">
  ## v0.5.3

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.5.3)

* quick Fix for hierarchical manager
</Update>

<Update label="Feb 06, 2024">
  ## v0.5.2

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.5.2)

* Adding `manager_llm` for hierarchical process
  * Improving `max_inter` and `max_rpm` logic
  * Updating README and Docs
</Update>

<Update label="Feb 04, 2024">
  ## v0.5.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.5.0)

This new version bring a lot of new features and improvements to the library.

* Adding Task Callbacks.
  * Adding support for Hierarchical process.
  * Adding ability to references specific tasks in another task.
  * Adding ability to parallel task execution.

* Revamping Max Iterations and Max Requests per Minute.
  * Developer experience improvements, docstrings and such.
  * Small improvements and TYPOs.
  * Fix static typing errors.
  * Updated README and Docs.
</Update>

<Update label="Jan 14, 2024">
  ## v0.1.32

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.1.32)

* Moving to LangChain 0.1.0
  * Improving Prompts
  * Adding ability to limit maximum number of iterations for an agent
  * Adding ability to Request Per Minute throttling for both Agents and Crews
  * Adding initial support for translations
  * Adding Greek translation
  * Improve code readability
  * Starting new documentation with mkdocs
</Update>

<Update label="Jan 07, 2024">
  ## v0.1.23

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.1.23)

* Many Reliability improvements
  * Prompt changes
  * Initial changes for supporting multiple languages
  * Fixing bug on task repeated execution
  * Better execution error handling
  * Updating READMe
</Update>

<Update label="Dec 30, 2023">
  ## v0.1.14

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.1.14)

* Adding tool caching a loop execution prevention. (@joaomdmoura)
  * Adding more guidelines for Agent delegation. (@joaomdmoura)
  * Updating to use new openai lib version. (@joaomdmoura)
  * Adding verbose levels to the logger. (@joaomdmoura)
  * Removing WIP code. (@joaomdmoura)
  * A lot of developer quality of life improvements (Special thanks to @greysonlalonde).
  * Updating to pydantic v2 (Special thanks to @greysonlalonde as well).
</Update>

<Update label="Nov 24, 2023">
  ## v0.1.2

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.1.2)

* Adding ability to use other LLMs, not OpenAI
</Update>

<Update label="Nov 19, 2023">
  ## v0.1.1

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.1.1)

# CrewAI v0.1.1 Release Notes

* **Crew Verbose Mode**:  Now allowing you to inspect a the tasks are being executed.

* **README and Docs Updates**: A series of minor updates on the docs
</Update>

<Update label="Nov 14, 2023">
  ## v0.1.0

[View release on GitHub](https://github.com/crewAIInc/crewAI/releases/tag/v0.1.0)

# CrewAI v0.1.0 Release Notes

We are thrilled to announce the initial release of CrewAI, version 0.1.0! CrewAI is a framework designed to facilitate the orchestration of autonomous AI agents capable of role-playing and collaboration to accomplish complex tasks more efficiently.

* **Initial Launch**: CrewAI is now officially in the wild! This foundational release lays the groundwork for AI agents to work in tandem, each with its own specialized role and objectives.

* **Role-Based Agent Design**: Define and customize agents with specific roles, goals, and the tools they need to succeed.

* **Inter-Agent Delegation**: Agents are now equipped to autonomously delegate tasks, enabling dynamic distribution of workload among the team.

* **Task Management**: Create and assign tasks dynamically with the flexibility to specify the tools needed for each task.

* **Sequential Processes**: Set up your agents to tackle tasks one after the other, ensuring organized and predictable workflows.

* **Documentation**: Start exploring CrewAI with our initial documentation that guides you through the setup and use of the framework.

* Detailed API documentation for the `Agent`, `Task`, `Crew`, and `Process` classes.
  * Examples and tutorials to help you build your first CrewAI application.
  * Basic setup for collaborative and delegation mechanisms among agents.

* As this is the first release, there may be undiscovered bugs and areas for optimization. We encourage the community to report any issues found during use.

* **Advanced Process Management**: In future releases, we will introduce more complex processes for task management including consensual and hierarchical workflows.
</Update>

---

## Check chunking behavior

**URL:** llms-txt#check-chunking-behavior

print(f"Original content length: {len(test_source.content)}")
print(f"Chunk size: {test_source.chunk_size}")
print(f"Chunk overlap: {test_source.chunk_overlap}")

---

## Check server documentation for required parameters

**URL:** llms-txt#check-server-documentation-for-required-parameters

---

## Check server status or try backup servers

**URL:** llms-txt#check-server-status-or-try-backup-servers

**Examples:**

Example 1 (unknown):
```unknown
**Authentication failures:**
```

---

## Check storage structure

**URL:** llms-txt#check-storage-structure

storage_path = db_storage_path()
knowledge_path = os.path.join(storage_path, "knowledge")

if os.path.exists(knowledge_path):
    print("Knowledge collections found:")
    for collection in os.listdir(knowledge_path):
        collection_path = os.path.join(knowledge_path, collection)
        if os.path.isdir(collection_path):
            print(f"  - {collection}/")
            # Show collection contents
            for item in os.listdir(collection_path):
                print(f"    └── {item}")
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
#### Test Knowledge Retrieval
```

---

## Check your MCP server URL and authentication

**URL:** llms-txt#check-your-mcp-server-url-and-authentication

---

## ChromaDB (default)

**URL:** llms-txt#chromadb-(default)

from crewai.rag.chromadb.config import ChromaDBConfig
set_rag_config(ChromaDBConfig())
chromadb_client = get_rag_client()

---

## Clear all hooks at once

**URL:** llms-txt#clear-all-hooks-at-once

result = clear_all_global_hooks()
print(f"Cleared {result['total']} hooks")

---

## Clear all LLM hooks

**URL:** llms-txt#clear-all-llm-hooks

**Contents:**
  - Listing Registered Hooks

before_count, after_count = clear_all_llm_call_hooks()
print(f"Cleared {before_count} before and {after_count} after hooks")
python theme={null}
from crewai.hooks import (
    get_before_llm_call_hooks,
    get_after_llm_call_hooks
)

**Examples:**

Example 1 (unknown):
```unknown
### Listing Registered Hooks
```

---

## Clear specific hook type

**URL:** llms-txt#clear-specific-hook-type

count = clear_before_tool_call_hooks()
print(f"Cleared {count} before hooks")

---

## Clear specific types

**URL:** llms-txt#clear-specific-types

**Contents:**
  - Unregistering Individual Hooks

llm_before_count = clear_before_llm_call_hooks()
tool_after_count = clear_after_tool_call_hooks()
python theme={null}
from crewai.hooks import (
    unregister_before_llm_call_hook,
    unregister_after_tool_call_hook
)

def my_hook(context):
    ...

**Examples:**

Example 1 (unknown):
```unknown
### Unregistering Individual Hooks
```

---

## CLI

**URL:** llms-txt#cli

**Contents:**
- Overview
- Installation
- Basic Usage
- Available Commands
  - 1. Create
  - 2. Version
  - 3. Train
  - 4. Replay
  - 5. Log-tasks-outputs
  - 6. Reset-memories

Source: https://docs.crewai.com/en/concepts/cli

Learn how to use the CrewAI CLI to interact with CrewAI.

<Warning>Since release 0.140.0, CrewAI AOP started a process of migrating their login provider. As such, the authentication flow via CLI was updated. Users that use Google to login, or that created their account after July 3rd, 2025 will be unable to log in with older versions of the `crewai` library.</Warning>

The CrewAI CLI provides a set of commands to interact with CrewAI, allowing you to create, train, run, and manage crews & flows.

To use the CrewAI CLI, make sure you have CrewAI installed:

The basic structure of a CrewAI CLI command is:

## Available Commands

Create a new crew or flow.

* `TYPE`: Choose between "crew" or "flow"
* `NAME`: Name of the crew or flow

Show the installed version of CrewAI.

* `--tools`: (Optional) Show the installed version of CrewAI tools

Train the crew for a specified number of iterations.

* `-n, --n_iterations INTEGER`: Number of iterations to train the crew (default: 5)
* `-f, --filename TEXT`: Path to a custom file for training (default: "trained\_agents\_data.pkl")

Replay the crew execution from a specific task.

* `-t, --task_id TEXT`: Replay the crew from this task ID, including all subsequent tasks

### 5. Log-tasks-outputs

Retrieve your latest crew\.kickoff() task outputs.

### 6. Reset-memories

Reset the crew memories (long, short, entity, latest\_crew\_kickoff\_outputs).

* `-l, --long`: Reset LONG TERM memory
* `-s, --short`: Reset SHORT TERM memory
* `-e, --entities`: Reset ENTITIES memory
* `-k, --kickoff-outputs`: Reset LATEST KICKOFF TASK OUTPUTS
* `-kn, --knowledge`: Reset KNOWLEDGE storage
* `-akn, --agent-knowledge`: Reset AGENT KNOWLEDGE storage
* `-a, --all`: Reset ALL memories

Test the crew and evaluate the results.

* `-n, --n_iterations INTEGER`: Number of iterations to test the crew (default: 3)
* `-m, --model TEXT`: LLM Model to run the tests on the Crew (default: "gpt-4o-mini")

Run the crew or flow.

<Note>
  Starting from version 0.103.0, the `crewai run` command can be used to run both standard crews and flows. For flows, it automatically detects the type from pyproject.toml and runs the appropriate command. This is now the recommended way to run both crews and flows.
</Note>

<Note>
  Make sure to run these commands from the directory where your CrewAI project is set up.
  Some commands may require additional configuration or setup within your project structure.
</Note>

Starting in version `0.98.0`, when you run the `crewai chat` command, you start an interactive session with your crew. The AI assistant will guide you by asking for necessary inputs to execute the crew. Once all inputs are provided, the crew will execute its tasks.

After receiving the results, you can continue interacting with the assistant for further instructions or questions.

<Note>
  Ensure you execute these commands from your CrewAI project's root directory.
</Note>

<Note>
  IMPORTANT: Set the `chat_llm` property in your `crew.py` file to enable this command.

Deploy the crew or flow to [CrewAI AOP](https://app.crewai.com).

* **Authentication**: You need to be authenticated to deploy to CrewAI AOP.
  You can login or create an account with:

* **Create a deployment**: Once you are authenticated, you can create a deployment for your crew or flow from the root of your localproject.
  
  * Reads your local project configuration.
  * Prompts you to confirm the environment variables (like `OPENAI_API_KEY`, `SERPER_API_KEY`) found locally. These will be securely stored with the deployment on the Enterprise platform. Ensure your sensitive keys are correctly configured locally (e.g., in a `.env` file) before running this.

### 11. Organization Management

Manage your CrewAI AOP organizations.

* `list`: List all organizations you belong to

* `current`: Display your currently active organization

* `switch`: Switch to a specific organization

<Note>
  You must be authenticated to CrewAI AOP to use these organization management commands.
</Note>

* **Create a deployment** (continued):
  * Links the deployment to the corresponding remote GitHub repository (it usually detects this automatically).

* **Deploy the Crew**: Once you are authenticated, you can deploy your crew or flow to CrewAI AOP.
  
  * Initiates the deployment process on the CrewAI AOP platform.
  * Upon successful initiation, it will output the Deployment created successfully! message along with the Deployment Name and a unique Deployment ID (UUID).

* **Deployment Status**: You can check the status of your deployment with:
  
  This fetches the latest deployment status of your most recent deployment attempt (e.g., `Building Images for Crew`, `Deploy Enqueued`, `Online`).

* **Deployment Logs**: You can check the logs of your deployment with:
  
  This streams the deployment logs to your terminal.

* **List deployments**: You can list all your deployments with:
  
  This lists all your deployments.

* **Delete a deployment**: You can delete a deployment with:
  
  This deletes the deployment from the CrewAI AOP platform.

* **Help Command**: You can get help with the CLI with:
  
  This shows the help message for the CrewAI Deploy CLI.

Watch this video tutorial for a step-by-step demonstration of deploying your crew to [CrewAI AOP](http://app.crewai.com) using the CLI.

<iframe title="CrewAI Deployment Guide" />

Authenticate with CrewAI AOP using a secure device code flow (no email entry required).

* A verification URL and short code are displayed in your terminal
* Your browser opens to the verification URL
* Enter/confirm the code to complete authentication

* The OAuth2 provider and domain are configured via `crewai config` (defaults use `login.crewai.com`)
* After successful login, the CLI also attempts to authenticate to the Tool Repository automatically
* If you reset your configuration, run `crewai login` again to re-authenticate

When running `crewai create crew` command, the CLI will show you a list of available LLM providers to choose from, followed by model selection for your chosen provider.

Once you've selected an LLM provider and model, you will be prompted for API keys.

#### Available LLM Providers

Here's a list of the most popular LLM providers suggested by the CLI:

* OpenAI
* Groq
* Anthropic
* Google Gemini
* SambaNova

When you select a provider, the CLI will then show you available models for that provider and prompt you to enter your API key.

If you select "other", you will be able to select from a list of LiteLLM supported providers.

When you select a provider, the CLI will prompt you to enter the Key name and the API key.

See the following link for each provider's key name:

* [LiteLLM Providers](https://docs.litellm.ai/docs/providers)

### 13. Configuration Management

Manage CLI configuration settings for CrewAI.

* `list`: Display all CLI configuration parameters

* `set`: Set a CLI configuration parameter

* `reset`: Reset all CLI configuration parameters to default values

#### Available Configuration Parameters

* `enterprise_base_url`: Base URL of the CrewAI AOP instance
* `oauth2_provider`: OAuth2 provider used for authentication (e.g., workos, okta, auth0)
* `oauth2_audience`: OAuth2 audience value, typically used to identify the target API or resource
* `oauth2_client_id`: OAuth2 client ID issued by the provider, used during authentication requests
* `oauth2_domain`: OAuth2 provider's domain (e.g., your-org.auth0.com) used for issuing tokens

Display current configuration:

| Setting               | Value                                            | Description                                  |
| :-------------------- | :----------------------------------------------- | :------------------------------------------- |
| enterprise\_base\_url | [https://app.crewai.com](https://app.crewai.com) | Base URL of the CrewAI AOP instance          |
| org\_name             | Not set                                          | Name of the currently active organization    |
| org\_uuid             | Not set                                          | UUID of the currently active organization    |
| oauth2\_provider      | workos                                           | OAuth2 provider (e.g., workos, okta, auth0)  |
| oauth2\_audience      | client\_01YYY                                    | Audience identifying the target API/resource |
| oauth2\_client\_id    | client\_01XXX                                    | OAuth2 client ID issued by the provider      |
| oauth2\_domain        | login.crewai.com                                 | Provider domain (e.g., your-org.auth0.com)   |

Set the enterprise base URL:

Reset all configuration to defaults:

<Tip>
  After resetting configuration, re-run `crewai login` to authenticate again.
</Tip>

### 14. Trace Management

Manage trace collection preferences for your Crew and Flow executions.

* `enable`: Enable trace collection for crew/flow executions

* `disable`: Disable trace collection for crew/flow executions

* `status`: Show current trace collection status

#### How Tracing Works

Trace collection is controlled by checking three settings in priority order:

1. **Explicit flag in code** (highest priority - can enable OR disable):
   
   * `tracing=True` will **always enable** tracing (overrides everything)
   * `tracing=False` will **always disable** tracing (overrides everything)
   * `tracing=None` or omitted will check lower priority settings

2. **Environment variable** (second priority):
   
   * Checked only if `tracing` is not explicitly set to `True` or `False` in code
   * Set to `true` or `1` to enable tracing

3. **User preference** (lowest priority):
   
   * Checked only if `tracing` is not set in code and `CREWAI_TRACING_ENABLED` is not set to `true`
   * Running `crewai traces enable` is sufficient to enable tracing by itself

<Note>
  **To enable tracing**, use any one of these methods:

* Set `tracing=True` in your Crew/Flow code, OR
  * Add `CREWAI_TRACING_ENABLED=true` to your `.env` file, OR
  * Run `crewai traces enable`

**To disable tracing**, use any ONE of these methods:

* Set `tracing=False` in your Crew/Flow code (overrides everything), OR
  * Remove or set to `false` the `CREWAI_TRACING_ENABLED` env var, OR
  * Run `crewai traces disable`

Higher priority settings override lower ones.
</Note>

<Tip>
  For more information about tracing, see the [Tracing documentation](/observability/tracing).
</Tip>

<Tip>
  CrewAI CLI handles authentication to the Tool Repository automatically when adding packages to your project. Just append `crewai` before any `uv` command to use it. E.g. `crewai uv add requests`. For more information, see [Tool Repository](https://docs.crewai.com/enterprise/features/tool-repository) docs.
</Tip>

<Note>
  Configuration settings are stored in `~/.config/crewai/settings.json`. Some settings like organization name and UUID are read-only and managed through authentication and organization commands. Tool repository related settings are hidden and cannot be set directly by users.
</Note>

**Examples:**

Example 1 (unknown):
```unknown
## Basic Usage

The basic structure of a CrewAI CLI command is:
```

Example 2 (unknown):
```unknown
## Available Commands

### 1. Create

Create a new crew or flow.
```

Example 3 (unknown):
```unknown
* `TYPE`: Choose between "crew" or "flow"
* `NAME`: Name of the crew or flow

Example:
```

Example 4 (unknown):
```unknown
### 2. Version

Show the installed version of CrewAI.
```

---

## CLI commands

**URL:** llms-txt#cli-commands

---

## Compare performance

**URL:** llms-txt#compare-performance

**Contents:**
  - Entity Memory batching behavior
- 2. External Memory
  - Basic External Memory with Mem0

openai_time = test_embedding_performance({
    "provider": "openai",
    "config": {"model": "text-embedding-3-small"}
})

ollama_time = test_embedding_performance({
    "provider": "ollama",
    "config": {"model": "mxbai-embed-large"}
})

print(f"OpenAI: {openai_time:.2f}s")
print(f"Ollama: {ollama_time:.2f}s")
python theme={null}
import os
from crewai import Agent, Crew, Process, Task
from crewai.memory.external.external_memory import ExternalMemory

**Examples:**

Example 1 (unknown):
```unknown
### Entity Memory batching behavior

Entity Memory supports batching when saving multiple entities at once. When you pass a list of `EntityMemoryItem`, the system:

* Emits a single MemorySaveStartedEvent with `entity_count`
* Saves each entity internally, collecting any partial errors
* Emits MemorySaveCompletedEvent with aggregate metadata (saved count, errors)
* Raises a partial-save exception if some entities failed (includes counts)

This improves performance and observability when writing many entities in one operation.

## 2. External Memory

External Memory provides a standalone memory system that operates independently from the crew's built-in memory. This is ideal for specialized memory providers or cross-application memory sharing.

### Basic External Memory with Mem0
```

---

## Complex flow benefits from structured state

**URL:** llms-txt#complex-flow-benefits-from-structured-state

**Contents:**
  - 3. Document State Transitions
  - 4. Handle State Errors Gracefully
  - 5. Use State for Progress Tracking
  - 6. Use Immutable Operations When Possible

class UserRegistrationState(BaseModel):
    username: str
    email: str
    verification_status: bool = False
    registration_date: datetime = Field(default_factory=datetime.now)
    last_login: Optional[datetime] = None

class RegistrationFlow(Flow[UserRegistrationState]):
    # Methods with strongly-typed state access
python theme={null}
@start()
def initialize_order(self):
    """
    Initialize order state with empty values.

State before: {}
    State after: {order_id: str, items: [], status: 'new'}
    """
    self.state.order_id = str(uuid.uuid4())
    self.state.items = []
    self.state.status = "new"
    return "Order initialized"
python theme={null}
@listen(previous_step)
def process_data(self, _):
    try:
        # Try to access a value that might not exist
        user_preference = self.state.preferences.get("theme", "default")
    except (AttributeError, KeyError):
        # Handle the error gracefully
        self.state.errors = self.state.get("errors", [])
        self.state.errors.append("Failed to access preferences")
        user_preference = "default"

return f"Used preference: {user_preference}"
python theme={null}
class ProgressTrackingFlow(Flow):
    @start()
    def initialize(self):
        self.state["total_steps"] = 3
        self.state["current_step"] = 0
        self.state["progress"] = 0.0
        self.update_progress()
        return "Initialized"

def update_progress(self):
        """Helper method to calculate and update progress"""
        if self.state.get("total_steps", 0) > 0:
            self.state["progress"] = (self.state.get("current_step", 0) /
                                    self.state["total_steps"]) * 100
            print(f"Progress: {self.state['progress']:.1f}%")

@listen(initialize)
    def step_one(self, _):
        # Do work...
        self.state["current_step"] = 1
        self.update_progress()
        return "Step 1 complete"

# Additional steps...
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### 3. Document State Transitions

For complex flows, document how state changes throughout the execution:
```

Example 2 (unknown):
```unknown
### 4. Handle State Errors Gracefully

Implement error handling for state access:
```

Example 3 (unknown):
```unknown
### 5. Use State for Progress Tracking

Leverage state to track progress in long-running flows:
```

Example 4 (unknown):
```unknown
### 6. Use Immutable Operations When Possible

Especially with structured state, prefer immutable operations for clarity:
```

---

## Configure custom storage location

**URL:** llms-txt#configure-custom-storage-location

custom_storage_path = "./storage"
os.makedirs(custom_storage_path, exist_ok=True)

crew = Crew(
    memory=True,
    long_term_memory=LongTermMemory(
        storage=LTMSQLiteStorage(
            db_path=f"{custom_storage_path}/memory.db"
        )
    )
)
python theme={null}
import os
from pathlib import Path

**Examples:**

Example 1 (unknown):
```unknown
#### Option 3: Project-Specific Storage
```

---

## Configure LLM with TrueFoundry

**URL:** llms-txt#configure-llm-with-truefoundry

llm = LLM(
    model="openai-main/gpt-4o",
    base_url="your_truefoundry_gateway_base_url", 
    api_key="your_truefoundry_api_key"
)

---

## Configure LLM with user tracking

**URL:** llms-txt#configure-llm-with-user-tracking

portkey_llm = LLM(
    model="gpt-4o",
    base_url=PORTKEY_GATEWAY_URL,
    api_key="dummy",
    extra_headers=createHeaders(
        api_key="YOUR_PORTKEY_API_KEY",
        virtual_key="YOUR_OPENAI_VIRTUAL_KEY",
        metadata={
            "_user": "user_123",  # Special _user field for user analytics
            "user_tier": "premium",
            "user_company": "Acme Corp",
            "session_id": "abc-123"
        }
    )
)

---

## Configure logging

**URL:** llms-txt#configure-logging

logger = logging.getLogger('memory_errors')

class MemoryErrorTracker(BaseEventListener):
    def __init__(self, notify_email: Optional[str] = None):
        super().__init__()
        self.notify_email = notify_email
        self.error_count = 0

def setup_listeners(self, crewai_event_bus):
        @crewai_event_bus.on(MemorySaveFailedEvent)
        def on_memory_save_failed(source, event: MemorySaveFailedEvent):
            self.error_count += 1
            agent_info = f"Agent '{event.agent_role}'" if event.agent_role else "Unknown agent"
            error_message = f"Memory save failed: {event.error}. {agent_info}"
            logger.error(error_message)

if self.notify_email and self.error_count % 5 == 0:
                self._send_notification(error_message)

@crewai_event_bus.on(MemoryQueryFailedEvent)
        def on_memory_query_failed(source, event: MemoryQueryFailedEvent):
            self.error_count += 1
            error_message = f"Memory query failed: {event.error}. Query: '{event.query}'"
            logger.error(error_message)

if self.notify_email and self.error_count % 5 == 0:
                self._send_notification(error_message)

def _send_notification(self, message):
        # Implement your notification system (email, Slack, etc.)
        print(f"[NOTIFICATION] Would send to {self.notify_email}: {message}")

---

## Connect to any LLM

**URL:** llms-txt#connect-to-any-llm

**Contents:**
- Connect CrewAI to LLMs
- Supported Providers
- Changing the LLM
- Configuration Options
- Connecting to OpenAI-Compatible LLMs
- Using Local Models with Ollama
- Changing the Base API URL
- Conclusion

Source: https://docs.crewai.com/en/learn/llm-connections

Comprehensive guide on integrating CrewAI with various Large Language Models (LLMs) using LiteLLM, including supported providers and configuration options.

## Connect CrewAI to LLMs

CrewAI uses LiteLLM to connect to a wide variety of Language Models (LLMs). This integration provides extensive versatility, allowing you to use models from numerous providers with a simple, unified interface.

<Note>
  By default, CrewAI uses the `gpt-4o-mini` model. This is determined by the `OPENAI_MODEL_NAME` environment variable, which defaults to "gpt-4o-mini" if not set.
  You can easily configure your agents to use a different model or provider as described in this guide.
</Note>

## Supported Providers

LiteLLM supports a wide range of providers, including but not limited to:

* OpenAI
* Anthropic
* Google (Vertex AI, Gemini)
* Azure OpenAI
* AWS (Bedrock, SageMaker)
* Cohere
* VoyageAI
* Hugging Face
* Ollama
* Mistral AI
* Replicate
* Together AI
* AI21
* Cloudflare Workers AI
* DeepInfra
* Groq
* SambaNova
* Nebius AI Studio
* [NVIDIA NIMs](https://docs.api.nvidia.com/nim/reference/models-1)
* And many more!

For a complete and up-to-date list of supported providers, please refer to the [LiteLLM Providers documentation](https://docs.litellm.ai/docs/providers).

To use a different LLM with your CrewAI agents, you have several options:

<Tabs>
  <Tab title="Using a String Identifier">
    Pass the model name as a string when initializing the agent:

<CodeGroup>
      
    </CodeGroup>
  </Tab>

<Tab title="Using the LLM Class">
    For more detailed configuration, use the LLM class:

<CodeGroup>
      
    </CodeGroup>
  </Tab>
</Tabs>

## Configuration Options

When configuring an LLM for your agent, you have access to a wide range of parameters:

| Parameter              |        Type        | Description                                                      |
| :--------------------- | :----------------: | :--------------------------------------------------------------- |
| **model**              |        `str`       | The name of the model to use (e.g., "gpt-4", "claude-2")         |
| **temperature**        |       `float`      | Controls randomness in output (0.0 to 1.0)                       |
| **max\_tokens**        |        `int`       | Maximum number of tokens to generate                             |
| **top\_p**             |       `float`      | Controls diversity of output (0.0 to 1.0)                        |
| **frequency\_penalty** |       `float`      | Penalizes new tokens based on their frequency in the text so far |
| **presence\_penalty**  |       `float`      | Penalizes new tokens based on their presence in the text so far  |
| **stop**               | `str`, `List[str]` | Sequence(s) to stop generation                                   |
| **base\_url**          |        `str`       | The base URL for the API endpoint                                |
| **api\_key**           |        `str`       | Your API key for authentication                                  |

For a complete list of parameters and their descriptions, refer to the LLM class documentation.

## Connecting to OpenAI-Compatible LLMs

You can connect to OpenAI-compatible LLMs using either environment variables or by setting specific attributes on the LLM class:

<Tabs>
  <Tab title="Using Environment Variables">
    <CodeGroup>

</CodeGroup>
  </Tab>

<Tab title="Using LLM Class Attributes">
    <CodeGroup>

</CodeGroup>
  </Tab>
</Tabs>

## Using Local Models with Ollama

For local models like those provided by Ollama:

<Steps>
  <Step title="Download and install Ollama">
    [Click here to download and install Ollama](https://ollama.com/download)
  </Step>

<Step title="Pull the desired model">
    For example, run `ollama pull llama3.2` to download the model.
  </Step>

<Step title="Configure your agent">
    <CodeGroup>
      
    </CodeGroup>
  </Step>
</Steps>

## Changing the Base API URL

You can change the base API URL for any LLM provider by setting the `base_url` parameter:

This is particularly useful when working with OpenAI-compatible APIs or when you need to specify a different endpoint for your chosen provider.

By leveraging LiteLLM, CrewAI offers seamless integration with a vast array of LLMs. This flexibility allows you to choose the most suitable model for your specific needs, whether you prioritize performance, cost-efficiency, or local deployment. Remember to consult the [LiteLLM documentation](https://docs.litellm.ai/docs/) for the most up-to-date information on supported models and configuration options.

**Examples:**

Example 1 (unknown):
```unknown
</CodeGroup>
  </Tab>

  <Tab title="Using the LLM Class">
    For more detailed configuration, use the LLM class:

    <CodeGroup>
```

Example 2 (unknown):
```unknown
</CodeGroup>
  </Tab>
</Tabs>

## Configuration Options

When configuring an LLM for your agent, you have access to a wide range of parameters:

| Parameter              |        Type        | Description                                                      |
| :--------------------- | :----------------: | :--------------------------------------------------------------- |
| **model**              |        `str`       | The name of the model to use (e.g., "gpt-4", "claude-2")         |
| **temperature**        |       `float`      | Controls randomness in output (0.0 to 1.0)                       |
| **max\_tokens**        |        `int`       | Maximum number of tokens to generate                             |
| **top\_p**             |       `float`      | Controls diversity of output (0.0 to 1.0)                        |
| **frequency\_penalty** |       `float`      | Penalizes new tokens based on their frequency in the text so far |
| **presence\_penalty**  |       `float`      | Penalizes new tokens based on their presence in the text so far  |
| **stop**               | `str`, `List[str]` | Sequence(s) to stop generation                                   |
| **base\_url**          |        `str`       | The base URL for the API endpoint                                |
| **api\_key**           |        `str`       | Your API key for authentication                                  |

For a complete list of parameters and their descriptions, refer to the LLM class documentation.

## Connecting to OpenAI-Compatible LLMs

You can connect to OpenAI-compatible LLMs using either environment variables or by setting specific attributes on the LLM class:

<Tabs>
  <Tab title="Using Environment Variables">
    <CodeGroup>
```

Example 3 (unknown):
```unknown

```

Example 4 (unknown):
```unknown
</CodeGroup>
  </Tab>

  <Tab title="Using LLM Class Attributes">
    <CodeGroup>
```

---

## Connect to Weaviate

**URL:** llms-txt#connect-to-weaviate

client = weaviate.connect_to_weaviate_cloud(
    cluster_url="https://your-weaviate-cluster-url.com",
    auth_credentials=Auth.api_key("your-weaviate-api-key"),
    headers={"X-OpenAI-Api-Key": "your-openai-api-key"}
)

---

## Consider creating new state:

**URL:** llms-txt#consider-creating-new-state:

**Contents:**
- Debugging Flow State
  - Logging State Changes
  - State Visualization
- Conclusion
- Next Steps

from pydantic import BaseModel
from typing import List

class ItemState(BaseModel):
    items: List[str] = []

class ImmutableFlow(Flow[ItemState]):
    @start()
    def add_item(self):
        # Create new list with the added item
        self.state.items = [*self.state.items, "new item"]
        return "Item added"
python theme={null}
import logging
logging.basicConfig(level=logging.INFO)

class LoggingFlow(Flow):
    def log_state(self, step_name):
        logging.info(f"State after {step_name}: {self.state}")

@start()
    def initialize(self):
        self.state["counter"] = 0
        self.log_state("initialize")
        return "Initialized"

@listen(initialize)
    def increment(self, _):
        self.state["counter"] += 1
        self.log_state("increment")
        return f"Incremented to {self.state['counter']}"
python theme={null}
def visualize_state(self):
    """Create a simple visualization of the current state"""
    import json
    from rich.console import Console
    from rich.panel import Panel

if hasattr(self.state, "model_dump"):
        # Pydantic v2
        state_dict = self.state.model_dump()
    elif hasattr(self.state, "dict"):
        # Pydantic v1
        state_dict = self.state.dict()
    else:
        # Unstructured state
        state_dict = dict(self.state)

# Remove id for cleaner output
    if "id" in state_dict:
        state_dict.pop("id")

state_json = json.dumps(state_dict, indent=2, default=str)
    console.print(Panel(state_json, title="Current Flow State"))
```

Mastering state management in CrewAI Flows gives you the power to build sophisticated, robust AI applications that maintain context, make complex decisions, and deliver consistent results.

Whether you choose unstructured or structured state, implementing proper state management practices will help you create flows that are maintainable, extensible, and effective at solving real-world problems.

As you develop more complex flows, remember that good state management is about finding the right balance between flexibility and structure, making your code both powerful and easy to understand.

<Check>
  You've now mastered the concepts and practices of state management in CrewAI Flows! With this knowledge, you can create robust AI workflows that effectively maintain context, share data between steps, and build sophisticated application logic.
</Check>

* Experiment with both structured and unstructured state in your flows
* Try implementing state persistence for long-running workflows
* Explore [building your first crew](/en/guides/crews/first-crew) to see how crews and flows can work together
* Check out the [Flow reference documentation](/en/concepts/flows) for more advanced features

**Examples:**

Example 1 (unknown):
```unknown
## Debugging Flow State

### Logging State Changes

When developing, add logging to track state changes:
```

Example 2 (unknown):
```unknown
### State Visualization

You can add methods to visualize your state for debugging:
```

---

## Context amplifies model effectiveness

**URL:** llms-txt#context-amplifies-model-effectiveness

domain_expert = Agent(
    role="B2B SaaS Marketing Strategist",
    goal="Develop comprehensive go-to-market strategies for enterprise software",
    backstory="""
    You have 10+ years of experience scaling B2B SaaS companies from Series A to IPO.
    You understand the nuances of enterprise sales cycles, the importance of product-market
    fit in different verticals, and how to balance growth metrics with unit economics.
    You've worked with companies like Salesforce, HubSpot, and emerging unicorns, giving
    you perspective on both established and disruptive go-to-market strategies.
    """,
    llm=LLM(model="claude-3-5-sonnet", temperature=0.3)  # Balanced creativity with domain knowledge
)

---

## Correct: @human_feedback is innermost (closest to the function)

**URL:** llms-txt#correct:-@human_feedback-is-innermost-(closest-to-the-function)

**Contents:**
- Best Practices
  - 1. Write Clear Request Messages

@start()
@human_feedback(message="Review this:")
def my_start_method(self):
    return "content"

@listen(other_method)
@human_feedback(message="Review this too:")
def my_listener(self, data):
    return f"processed: {data}"
python Code theme={null}

**Examples:**

Example 1 (unknown):
```unknown
<Tip>
  Place `@human_feedback` as the innermost decorator (last/closest to the function) so it wraps the method directly and can capture the return value before passing to the flow system.
</Tip>

## Best Practices

### 1. Write Clear Request Messages

The `request` parameter is what the human sees. Make it actionable:
```

---

## "country": "us",  # Select a proxy location

**URL:** llms-txt#"country":-"us",--#-select-a-proxy-location

---

## Create an index

**URL:** llms-txt#create-an-index

index = VectorStoreIndex.from_documents(documents)

---

## Create an instance of your listener

**URL:** llms-txt#create-an-instance-of-your-listener

**Contents:**
  - Integrating with Analytics Platforms
  - Best Practices for Memory Event Listeners
- Conclusion

error_tracker = MemoryErrorTracker(notify_email="admin@example.com")
python theme={null}
from crewai.events import (
    BaseEventListener,
    MemoryQueryCompletedEvent,
    MemorySaveCompletedEvent
)

class MemoryAnalyticsForwarder(BaseEventListener):
    def __init__(self, analytics_client):
        super().__init__()
        self.client = analytics_client

def setup_listeners(self, crewai_event_bus):
        @crewai_event_bus.on(MemoryQueryCompletedEvent)
        def on_memory_query_completed(source, event: MemoryQueryCompletedEvent):
            # Forward query metrics to analytics platform
            self.client.track_metric({
                "event_type": "memory_query",
                "query": event.query,
                "duration_ms": event.query_time_ms,
                "result_count": len(event.results) if hasattr(event.results, "__len__") else 0,
                "timestamp": event.timestamp
            })

@crewai_event_bus.on(MemorySaveCompletedEvent)
        def on_memory_save_completed(source, event: MemorySaveCompletedEvent):
            # Forward save metrics to analytics platform
            self.client.track_metric({
                "event_type": "memory_save",
                "agent_role": event.agent_role,
                "duration_ms": event.save_time_ms,
                "timestamp": event.timestamp
            })
```

### Best Practices for Memory Event Listeners

1. **Keep handlers lightweight**: Avoid complex processing in event handlers to prevent performance impacts
2. **Use appropriate logging levels**: Use INFO for normal operations, DEBUG for details, ERROR for issues
3. **Batch metrics when possible**: Accumulate metrics before sending to external systems
4. **Handle exceptions gracefully**: Ensure your event handlers don't crash due to unexpected data
5. **Consider memory consumption**: Be mindful of storing large amounts of event data

Integrating CrewAI's memory system into your projects is straightforward. By leveraging the provided memory components and configurations,
you can quickly empower your agents with the ability to remember, reason, and learn from their interactions, unlocking new levels of intelligence and capability.

**Examples:**

Example 1 (unknown):
```unknown
### Integrating with Analytics Platforms

Memory events can be forwarded to analytics and monitoring platforms to track performance metrics, detect anomalies, and visualize memory usage patterns:
```

---

## Create an LLM with a temperature of 0 to ensure deterministic outputs

**URL:** llms-txt#create-an-llm-with-a-temperature-of-0-to-ensure-deterministic-outputs

llm = LLM(model="gpt-4o-mini", temperature=0)

---

## Create a deterministic fingerprint using a seed string

**URL:** llms-txt#create-a-deterministic-fingerprint-using-a-seed-string

deterministic_fingerprint = Fingerprint.generate(seed="my-agent-id")

---

## Create a `.env` file in your project root:

**URL:** llms-txt#create-a-`.env`-file-in-your-project-root:

---

## Create a filter for specific conditions

**URL:** llms-txt#create-a-filter-for-specific-conditions

preset_filter = qmodels.Filter(
    must=[
        qmodels.FieldCondition(
            key="category",
            match=qmodels.MatchValue(value="research")
        ),
        qmodels.FieldCondition(
            key="year",
            match=qmodels.MatchValue(value=2024)
        )
    ]
)

---

## Create a flow class

**URL:** llms-txt#create-a-flow-class

class MarketResearchFlow(Flow[MarketResearchState]):
    @start()
    def initialize_research(self) -> Dict[str, Any]:
        print(f"Starting market research for {self.state.product}")
        return {"product": self.state.product}

@listen(initialize_research)
    async def analyze_market(self) -> Dict[str, Any]:
        # Create an Agent for market research
        analyst = Agent(
            role="Market Research Analyst",
            goal=f"Analyze the market for {self.state.product}",
            backstory="You are an experienced market analyst with expertise in "
            "identifying market trends and opportunities.",
            tools=[SerperDevTool()],
            verbose=True,
        )

# Define the research query
        query = f"""
        Research the market for {self.state.product}. Include:
        1. Key market trends
        2. Market size
        3. Major competitors

Format your response according to the specified structure.
        """

# Execute the analysis with structured output format
        result = await analyst.kickoff_async(query, response_format=MarketAnalysis)
        if result.pydantic:
            print("result", result.pydantic)
        else:
            print("result", result)

# Return the analysis to update the state
        return {"analysis": result.pydantic}

@listen(analyze_market)
    def present_results(self, analysis) -> None:
        print("\nMarket Analysis Results")
        print("=====================")

if isinstance(analysis, dict):
            # If we got a dict with 'analysis' key, extract the actual analysis object
            market_analysis = analysis.get("analysis")
        else:
            market_analysis = analysis

if market_analysis and isinstance(market_analysis, MarketAnalysis):
            print("\nKey Market Trends:")
            for trend in market_analysis.key_trends:
                print(f"- {trend}")

print(f"\nMarket Size: {market_analysis.market_size}")

print("\nMajor Competitors:")
            for competitor in market_analysis.competitors:
                print(f"- {competitor}")
        else:
            print("No structured analysis data available.")
            print("Raw analysis:", analysis)

---

## Create a flow with typed state

**URL:** llms-txt#create-a-flow-with-typed-state

class StructuredStateFlow(Flow[AppState]):
    @start()
    def initialize_data(self):
        print("Initializing flow data")
        # Set state values (type-checked)
        self.state.user_name = "Taylor"
        self.state.preferences.theme = "dark"

# The ID field is automatically available
        print(f"Flow ID: {self.state.id}")

@listen(initialize_data)
    def process_data(self, previous_result):
        print(f"Processing data for {self.state.user_name}")

# Modify state (with type checking)
        self.state.items.append("item1")
        self.state.items.append("item2")
        self.state.processed = True
        self.state.completion_percentage = 50.0

@listen(process_data)
    def generate_summary(self, previous_result):
        # Access state (with autocompletion)
        summary = f"User {self.state.user_name} has {len(self.state.items)} items "
        summary += f"with {self.state.preferences.theme} theme. "
        summary += "Data is processed." if self.state.processed else "Data is not processed."
        summary += f" Completion: {self.state.completion_percentage}%"

---

## Create a knowledge source

**URL:** llms-txt#create-a-knowledge-source

content = "Users name is John. He is 30 years old and lives in San Francisco."
string_source = StringKnowledgeSource(content=content)

---

## Create a knowledge source from web content

**URL:** llms-txt#create-a-knowledge-source-from-web-content

content_source = CrewDoclingSource(
    file_paths=[
        "https://lilianweng.github.io/posts/2024-11-28-reward-hacking",
        "https://lilianweng.github.io/posts/2024-07-07-hallucination",
    ],
)

---

## Create a query engine

**URL:** llms-txt#create-a-query-engine

query_engine = index.as_query_engine()

---

## Create a test knowledge source

**URL:** llms-txt#create-a-test-knowledge-source

test_source = StringKnowledgeSource(
    content="Test knowledge content for debugging",
    chunk_size=100,  # Small chunks for testing
    chunk_overlap=20
)

---

## Create custom storage with specific embedder

**URL:** llms-txt#create-custom-storage-with-specific-embedder

custom_storage = KnowledgeStorage(
    embedder={
        "provider": "ollama",
        "config": {"model": "mxbai-embed-large"}
    },
    collection_name="my_custom_knowledge"
)

---

## Create external memory instance with local Mem0 Configuration

**URL:** llms-txt#create-external-memory-instance-with-local-mem0-configuration

**Contents:**
  - Advanced External Memory with Mem0 Client

external_memory = ExternalMemory(
    embedder_config={
        "provider": "mem0",
        "config": {
            "user_id": "john",
            "local_mem0_config": {
                "vector_store": {
                    "provider": "qdrant",
                    "config": {"host": "localhost", "port": 6333}
                },
                "llm": {
                    "provider": "openai",
                    "config": {"api_key": "your-api-key", "model": "gpt-4"}
                },
                "embedder": {
                    "provider": "openai",
                    "config": {"api_key": "your-api-key", "model": "text-embedding-3-small"}
                }
            },
            "infer": True # Optional defaults to True
        },
    }
)

crew = Crew(
    agents=[...],
    tasks=[...],
    external_memory=external_memory, # Separate from basic memory
    process=Process.sequential,
    verbose=True
)
python theme={null}
import os
from crewai import Agent, Crew, Process, Task
from crewai.memory.external.external_memory import ExternalMemory

new_categories = [
    {"lifestyle_management_concerns": "Tracks daily routines, habits, hobbies and interests including cooking, time management and work-life balance"},
    {"seeking_structure": "Documents goals around creating routines, schedules, and organized systems in various life areas"},
    {"personal_information": "Basic information about the user including name, preferences, and personality traits"}
]

os.environ["MEM0_API_KEY"] = "your-api-key"

**Examples:**

Example 1 (unknown):
```unknown
### Advanced External Memory with Mem0 Client

When using Mem0 Client, you can customize the memory configuration further, by using parameters like 'includes', 'excludes', 'custom\_categories', 'infer' and 'run\_id' (this is only for short-term memory).
You can find more details in the [Mem0 documentation](https://docs.mem0.ai/).
```

---

## Create external memory instance with Mem0 Client

**URL:** llms-txt#create-external-memory-instance-with-mem0-client

**Contents:**
  - Custom Storage Implementation

external_memory = ExternalMemory(
    embedder_config={
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
)

crew = Crew(
    agents=[...],
    tasks=[...],
    external_memory=external_memory, # Separate from basic memory
    process=Process.sequential,
    verbose=True
)
python theme={null}
from crewai.memory.external.external_memory import ExternalMemory
from crewai.memory.storage.interface import Storage

class CustomStorage(Storage):
    def __init__(self):
        self.memories = []

def save(self, value, metadata=None, agent=None):
        self.memories.append({
            "value": value,
            "metadata": metadata,
            "agent": agent
        })

def search(self, query, limit=10, score_threshold=0.5):
        # Implement your search logic here
        return [m for m in self.memories if query.lower() in str(m["value"]).lower()]

def reset(self):
        self.memories = []

**Examples:**

Example 1 (unknown):
```unknown
### Custom Storage Implementation
```

---

## Create LLM with fallback configuration

**URL:** llms-txt#create-llm-with-fallback-configuration

portkey_llm = LLM(
    model="gpt-4o",
    max_tokens=1000,
    base_url=PORTKEY_GATEWAY_URL,
    api_key="dummy",
    extra_headers=createHeaders(
        api_key="YOUR_PORTKEY_API_KEY",
        config={
            "strategy": {
                "mode": "fallback"
            },
            "targets": [
                {
                    "provider": "openai",
                    "api_key": "YOUR_OPENAI_API_KEY",
                    "override_params": {"model": "gpt-4o"}
                },
                {
                    "provider": "anthropic",
                    "api_key": "YOUR_ANTHROPIC_API_KEY",
                    "override_params": {"model": "claude-3-opus-20240229"}
                }
            ]
        }
    )
)

---

## Create LLM with guardrails

**URL:** llms-txt#create-llm-with-guardrails

portkey_llm = LLM(
    model="gpt-4o",
    base_url=PORTKEY_GATEWAY_URL,
    api_key="dummy",
    extra_headers=createHeaders(
        api_key="YOUR_PORTKEY_API_KEY",
        virtual_key="YOUR_OPENAI_VIRTUAL_KEY",
        config={
            "input_guardrails": ["guardrails-id-xxx", "guardrails-id-yyy"],
            "output_guardrails": ["guardrails-id-zzz"]
        }
    )
)

---

## Create output directory if it doesn't exist

**URL:** llms-txt#create-output-directory-if-it-doesn't-exist

**Contents:**
- Step 7: Set Up Your Environment Variables

os.makedirs('output', exist_ok=True)

def run():
    """
    Run the research crew.
    """
    inputs = {
        'topic': 'Artificial Intelligence in Healthcare'
    }

# Create and run the crew
    result = ResearchCrew().crew().kickoff(inputs=inputs)

# Print the result
    print("\n\n=== FINAL REPORT ===\n\n")
    print(result.raw)

print("\n\nReport has been saved to output/report.md")

if __name__ == "__main__":
    run()
sh theme={null}
SERPER_API_KEY=your_serper_api_key

**Examples:**

Example 1 (unknown):
```unknown
This script prepares the environment, specifies our research topic, and kicks off the crew's work. The power of CrewAI is evident in how simple this code is - all the complexity of managing multiple AI agents is handled by the framework.

## Step 7: Set Up Your Environment Variables

Create a `.env` file in your project root with your API keys:
```

---

## Create Snowflake configuration

**URL:** llms-txt#create-snowflake-configuration

config = SnowflakeConfig(
    account="your_account",
    user="your_username",
    password="your_password",
    warehouse="COMPUTE_WH",
    database="your_database",
    snowflake_schema="your_schema"
)

---

## Create with proper permissions

**URL:** llms-txt#create-with-proper-permissions

if not os.path.exists(storage_path):
    os.makedirs(storage_path, mode=0o755, exist_ok=True)
    print(f"Created storage directory: {storage_path}")
python theme={null}
import chromadb
from crewai.utilities.paths import db_storage_path

**Examples:**

Example 1 (unknown):
```unknown
#### Inspect ChromaDB Collections
```

---

## Create your custom LLM

**URL:** llms-txt#create-your-custom-llm

custom_llm = CustomLLM(
    model="my-custom-model",
    api_key="your-api-key",
    endpoint="https://api.example.com/v1/chat/completions",
    temperature=0.7
)

---

## Creation timestamp (auto-generated)

**URL:** llms-txt#creation-timestamp-(auto-generated)

created_at = fingerprint.created_at  # A datetime object

---

## Creative model for content generation

**URL:** llms-txt#creative-model-for-content-generation

content_llm = LLM(model="claude-3-5-sonnet-20241022", temperature=0.7)

---

## Customizing Prompts

**URL:** llms-txt#customizing-prompts

**Contents:**
- Why Customize Prompts?
- Understanding CrewAI's Prompt System
- Understanding Default System Instructions
  - What CrewAI Automatically Injects
  - Viewing the Complete System Prompt

Source: https://docs.crewai.com/en/guides/advanced/customizing-prompts

Dive deeper into low-level prompt customization for CrewAI, enabling super custom and complex use cases for different models and languages.

## Why Customize Prompts?

Although CrewAI's default prompts work well for many scenarios, low-level customization opens the door to significantly more flexible and powerful agent behavior. Here's why you might want to take advantage of this deeper control:

1. **Optimize for specific LLMs** – Different models (such as GPT-4, Claude, or Llama) thrive with prompt formats tailored to their unique architectures.
2. **Change the language** – Build agents that operate exclusively in languages beyond English, handling nuances with precision.
3. **Specialize for complex domains** – Adapt prompts for highly specialized industries like healthcare, finance, or legal.
4. **Adjust tone and style** – Make agents more formal, casual, creative, or analytical.
5. **Support super custom use cases** – Utilize advanced prompt structures and formatting to meet intricate, project-specific requirements.

This guide explores how to tap into CrewAI's prompts at a lower level, giving you fine-grained control over how agents think and interact.

## Understanding CrewAI's Prompt System

Under the hood, CrewAI employs a modular prompt system that you can customize extensively:

* **Agent templates** – Govern each agent's approach to their assigned role.
* **Prompt slices** – Control specialized behaviors such as tasks, tool usage, and output structure.
* **Error handling** – Direct how agents respond to failures, exceptions, or timeouts.
* **Tool-specific prompts** – Define detailed instructions for how tools are invoked or utilized.

Check out the [original prompt templates in CrewAI's repository](https://github.com/crewAIInc/crewAI/blob/main/src/crewai/translations/en.json) to see how these elements are organized. From there, you can override or adapt them as needed to unlock advanced behaviors.

## Understanding Default System Instructions

<Warning>
  **Production Transparency Issue**: CrewAI automatically injects default instructions into your prompts that you might not be aware of. This section explains what's happening under the hood and how to gain full control.
</Warning>

When you define an agent with `role`, `goal`, and `backstory`, CrewAI automatically adds additional system instructions that control formatting and behavior. Understanding these default injections is crucial for production systems where you need full prompt transparency.

### What CrewAI Automatically Injects

Based on your agent configuration, CrewAI adds different default instructions:

#### For Agents Without Tools

#### For Agents With Tools

#### For Structured Outputs (JSON/Pydantic)

### Viewing the Complete System Prompt

To see exactly what prompt is being sent to your LLM, you can inspect the generated prompt:

```python theme={null}
from crewai import Agent, Crew, Task
from crewai.utilities.prompts import Prompts

**Examples:**

Example 1 (unknown):
```unknown
#### For Agents With Tools
```

Example 2 (unknown):
```unknown
#### For Structured Outputs (JSON/Pydantic)
```

Example 3 (unknown):
```unknown
### Viewing the Complete System Prompt

To see exactly what prompt is being sent to your LLM, you can inspect the generated prompt:
```

---

## Custom LLM Implementation

**URL:** llms-txt#custom-llm-implementation

**Contents:**
- Overview
- Quick Start
- Using Your Custom LLM

Source: https://docs.crewai.com/en/learn/custom-llm

Learn how to create custom LLM implementations in CrewAI.

CrewAI supports custom LLM implementations through the `BaseLLM` abstract base class. This allows you to integrate any LLM provider that doesn't have built-in support in LiteLLM, or implement custom authentication mechanisms.

Here's a minimal custom LLM implementation:

## Using Your Custom LLM

```python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
## Using Your Custom LLM
```

---

## Datadog Integration

**URL:** llms-txt#datadog-integration

Source: https://docs.crewai.com/en/observability/datadog

Learn how to integrate Datadog with CrewAI to submit LLM Observability traces to Datadog.

---

## Default behavior - directories are created automatically

**URL:** llms-txt#default-behavior---directories-are-created-automatically

**Contents:**
  - Disabling Directory Creation

report_task = Task(
    description='Generate a comprehensive market analysis report',
    expected_output='A detailed market analysis with charts and insights',
    agent=analyst_agent,
    output_file='reports/2025/market_analysis.md',  # Creates 'reports/2025/' if it doesn't exist
    markdown=True
)
python Code theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### Disabling Directory Creation

If you want to prevent automatic directory creation and ensure that the directory already exists, set `create_directory=False`:
```

---

## Define a structured output format

**URL:** llms-txt#define-a-structured-output-format

class MarketAnalysis(BaseModel):
    key_trends: List[str]
    opportunities: List[str]
    recommendation: str

---

## Define custom input schema

**URL:** llms-txt#define-custom-input-schema

custom_inputs = {
    "year": Field(..., description="Year to retrieve the report for (integer)"),
    "region": Field(default="global", description="Geographic region for analysis"),
    "format": Field(default="summary", description="Report format (summary, detailed, raw)")
}

---

## Define flow state

**URL:** llms-txt#define-flow-state

class MarketResearchState(BaseModel):
    product: str = ""
    analysis: MarketAnalysis | None = None

---

## Define our flow state

**URL:** llms-txt#define-our-flow-state

**Contents:**
- Step 6: Set Up Your Environment Variables

class GuideCreatorState(BaseModel):
    topic: str = ""
    audience_level: str = ""
    guide_outline: GuideOutline = None
    sections_content: Dict[str, str] = {}

class GuideCreatorFlow(Flow[GuideCreatorState]):
    """Flow for creating a comprehensive guide on any topic"""

@start()
    def get_user_input(self):
        """Get input from the user about the guide topic and audience"""
        print("\n=== Create Your Comprehensive Guide ===\n")

# Get user input
        self.state.topic = input("What topic would you like to create a guide for? ")

# Get audience level with validation
        while True:
            audience = input("Who is your target audience? (beginner/intermediate/advanced) ").lower()
            if audience in ["beginner", "intermediate", "advanced"]:
                self.state.audience_level = audience
                break
            print("Please enter 'beginner', 'intermediate', or 'advanced'")

print(f"\nCreating a guide on {self.state.topic} for {self.state.audience_level} audience...\n")
        return self.state

@listen(get_user_input)
    def create_guide_outline(self, state):
        """Create a structured outline for the guide using a direct LLM call"""
        print("Creating guide outline...")

# Initialize the LLM
        llm = LLM(model="openai/gpt-4o-mini", response_format=GuideOutline)

# Create the messages for the outline
        messages = [
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": f"""
            Create a detailed outline for a comprehensive guide on "{state.topic}" for {state.audience_level} level learners.

The outline should include:
            1. A compelling title for the guide
            2. An introduction to the topic
            3. 4-6 main sections that cover the most important aspects of the topic
            4. A conclusion or summary

For each section, provide a clear title and a brief description of what it should cover.
            """}
        ]

# Make the LLM call with JSON response format
        response = llm.call(messages=messages)

# Parse the JSON response
        outline_dict = json.loads(response)
        self.state.guide_outline = GuideOutline(**outline_dict)

# Ensure output directory exists before saving
        os.makedirs("output", exist_ok=True)

# Save the outline to a file
        with open("output/guide_outline.json", "w") as f:
            json.dump(outline_dict, f, indent=2)

print(f"Guide outline created with {len(self.state.guide_outline.sections)} sections")
        return self.state.guide_outline

@listen(create_guide_outline)
    def write_and_compile_guide(self, outline):
        """Write all sections and compile the guide"""
        print("Writing guide sections and compiling...")
        completed_sections = []

# Process sections one by one to maintain context flow
        for section in outline.sections:
            print(f"Processing section: {section.title}")

# Build context from previous sections
            previous_sections_text = ""
            if completed_sections:
                previous_sections_text = "# Previously Written Sections\n\n"
                for title in completed_sections:
                    previous_sections_text += f"## {title}\n\n"
                    previous_sections_text += self.state.sections_content.get(title, "") + "\n\n"
            else:
                previous_sections_text = "No previous sections written yet."

# Run the content crew for this section
            result = ContentCrew().crew().kickoff(inputs={
                "section_title": section.title,
                "section_description": section.description,
                "audience_level": self.state.audience_level,
                "previous_sections": previous_sections_text,
                "draft_content": ""
            })

# Store the content
            self.state.sections_content[section.title] = result.raw
            completed_sections.append(section.title)
            print(f"Section completed: {section.title}")

# Compile the final guide
        guide_content = f"# {outline.title}\n\n"
        guide_content += f"## Introduction\n\n{outline.introduction}\n\n"

# Add each section in order
        for section in outline.sections:
            section_content = self.state.sections_content.get(section.title, "")
            guide_content += f"\n\n{section_content}\n\n"

# Add conclusion
        guide_content += f"## Conclusion\n\n{outline.conclusion}\n\n"

# Save the guide
        with open("output/complete_guide.md", "w") as f:
            f.write(guide_content)

print("\nComplete guide compiled and saved to output/complete_guide.md")
        return "Guide creation completed successfully"

def kickoff():
    """Run the guide creator flow"""
    GuideCreatorFlow().kickoff()
    print("\n=== Flow Complete ===")
    print("Your comprehensive guide is ready in the output directory.")
    print("Open output/complete_guide.md to view it.")

def plot():
    """Generate a visualization of the flow"""
    flow = GuideCreatorFlow()
    flow.plot("guide_creator_flow")
    print("Flow visualization saved to guide_creator_flow.html")

if __name__ == "__main__":
    kickoff()
sh .env theme={null}
OPENAI_API_KEY=your_openai_api_key

**Examples:**

Example 1 (unknown):
```unknown
Let's analyze what's happening in this flow:

1. We define Pydantic models for structured data, ensuring type safety and clear data representation
2. We create a state class to maintain data across different steps of the flow
3. We implement three main flow steps:
   * Getting user input with the `@start()` decorator
   * Creating a guide outline with a direct LLM call
   * Processing sections with our content crew
4. We use the `@listen()` decorator to establish event-driven relationships between steps

This is the power of flows - combining different types of processing (user interaction, direct LLM calls, crew-based tasks) into a coherent, event-driven system.

## Step 6: Set Up Your Environment Variables

Create a `.env` file in your project root with your API keys. See the [LLM setup
guide](/en/concepts/llms#setting-up-your-llm) for details on configuring a provider.
```

---

## Define our models for structured data

**URL:** llms-txt#define-our-models-for-structured-data

class Section(BaseModel):
    title: str = Field(description="Title of the section")
    description: str = Field(description="Brief description of what the section should cover")

class GuideOutline(BaseModel):
    title: str = Field(description="Title of the guide")
    introduction: str = Field(description="Introduction to the topic")
    target_audience: str = Field(description="Description of the target audience")
    sections: List[Section] = Field(description="List of sections in the guide")
    conclusion: str = Field(description="Conclusion or summary of the guide")

---

## Define structured state

**URL:** llms-txt#define-structured-state

class SupportTicketState(BaseModel):
    ticket_id: str = ""
    customer_name: str = ""
    issue_description: str = ""
    category: str = ""
    priority: str = "medium"
    resolution: str = ""
    satisfaction_score: int = 0

class CustomerSupportFlow(Flow[SupportTicketState]):
    @start()
    def receive_ticket(self):
        # In a real app, this might come from an API
        self.state.ticket_id = "TKT-12345"
        self.state.customer_name = "Alex Johnson"
        self.state.issue_description = "Unable to access premium features after payment"
        return "Ticket received"

@listen(receive_ticket)
    def categorize_ticket(self, _):
        # Use a direct LLM call for categorization
        from crewai import LLM
        llm = LLM(model="openai/gpt-4o-mini")

prompt = f"""
        Categorize the following customer support issue into one of these categories:
        - Billing
        - Account Access
        - Technical Issue
        - Feature Request
        - Other

Issue: {self.state.issue_description}

Return only the category name.
        """

self.state.category = llm.call(prompt).strip()
        return self.state.category

@router(categorize_ticket)
    def route_by_category(self, category):
        # Route to different handlers based on category
        return category.lower().replace(" ", "_")

@listen("billing")
    def handle_billing_issue(self):
        # Handle billing-specific logic
        self.state.priority = "high"
        # More billing-specific processing...
        return "Billing issue handled"

@listen("account_access")
    def handle_access_issue(self):
        # Handle access-specific logic
        self.state.priority = "high"
        # More access-specific processing...
        return "Access issue handled"

# Additional category handlers...

@listen("billing", "account_access", "technical_issue", "feature_request", "other")
    def resolve_ticket(self, resolution_info):
        # Final resolution step
        self.state.resolution = f"Issue resolved: {resolution_info}"
        return self.state.resolution

---

## Define templates for system, user (prompt), and assistant (response) messages

**URL:** llms-txt#define-templates-for-system,-user-(prompt),-and-assistant-(response)-messages

system_template = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>{{ .System }}<|eot_id|>"""
prompt_template = """<|start_header_id|>user<|end_header_id|>{{ .Prompt }}<|eot_id|>"""
response_template = """<|start_header_id|>assistant<|end_header_id|>{{ .Response }}<|eot_id|>"""

---

## Define the Pydantic model for the blog

**URL:** llms-txt#define-the-pydantic-model-for-the-blog

class Blog(BaseModel):
    title: str
    content: str

---

## Define your own system template without default instructions

**URL:** llms-txt#define-your-own-system-template-without-default-instructions

**Contents:**
  - Debugging with Observability Tools
  - Best Practices for Production
- Best Practices for Managing Prompt Files
- The Simplest Way to Customize Prompts
  - Example: Basic Prompt Customization

custom_system_template = """You are {role}. {backstory}
Your goal is: {goal}

Respond naturally and conversationally. Focus on providing helpful, accurate information."""

custom_prompt_template = """Task: {input}

Please complete this task thoughtfully."""

agent = Agent(
    role="Research Assistant",
    goal="Help users find accurate information",
    backstory="You are a helpful research assistant.",
    system_template=custom_system_template,
    prompt_template=custom_prompt_template,
    use_system_prompt=True  # Use separate system/user messages
)
json theme={null}
{
  "slices": {
    "no_tools": "\nProvide your best answer in a natural, conversational way.",
    "tools": "\nYou have access to these tools: {tools}\n\nUse them when helpful, but respond naturally.",
    "formatted_task_instructions": "Format your response as: {output_format}"
  }
}
python theme={null}
crew = Crew(
    agents=[agent],
    tasks=[task],
    prompt_file="custom_prompts.json",
    verbose=True
)
python theme={null}
agent = Agent(
    role="Analyst",
    goal="Analyze data",
    backstory="Expert analyst",
    use_system_prompt=False  # Disables system prompt separation
)
json theme={null}
{
  "slices": {
    "format": "When responding, follow this structure:\n\nTHOUGHTS: Your step-by-step thinking\nACTION: Any tool you're using\nRESULT: Your final answer or conclusion"
  }
}
python theme={null}
from crewai import Agent, Crew, Task, Process

**Examples:**

Example 1 (unknown):
```unknown
#### Option 2: Custom Prompt File

Create a `custom_prompts.json` file to override specific prompt slices:
```

Example 2 (unknown):
```unknown
Then use it in your crew:
```

Example 3 (unknown):
```unknown
#### Option 3: Disable System Prompts for o1 Models
```

Example 4 (unknown):
```unknown
### Debugging with Observability Tools

For production transparency, integrate with observability platforms to monitor all prompts and LLM interactions. This allows you to see exactly what prompts (including default instructions) are being sent to your LLMs.

See our [Observability documentation](/en/observability/overview) for detailed integration guides with various platforms including Langfuse, MLflow, Weights & Biases, and custom logging solutions.

### Best Practices for Production

1. **Always inspect generated prompts** before deploying to production
2. **Use custom templates** when you need full control over prompt content
3. **Integrate observability tools** for ongoing prompt monitoring (see [Observability docs](/en/observability/overview))
4. **Test with different LLMs** as default instructions may work differently across models
5. **Document your prompt customizations** for team transparency

<Tip>
  The default instructions exist to ensure consistent agent behavior, but they can interfere with domain-specific requirements. Use the customization options above to maintain full control over your agent's behavior in production systems.
</Tip>

## Best Practices for Managing Prompt Files

When engaging in low-level prompt customization, follow these guidelines to keep things organized and maintainable:

1. **Keep files separate** – Store your customized prompts in dedicated JSON files outside your main codebase.
2. **Version control** – Track changes within your repository, ensuring clear documentation of prompt adjustments over time.
3. **Organize by model or language** – Use naming schemes like `prompts_llama.json` or `prompts_es.json` to quickly identify specialized configurations.
4. **Document changes** – Provide comments or maintain a README detailing the purpose and scope of your customizations.
5. **Minimize alterations** – Only override the specific slices you genuinely need to adjust, keeping default functionality intact for everything else.

## The Simplest Way to Customize Prompts

One straightforward approach is to create a JSON file for the prompts you want to override and then point your Crew at that file:

1. Craft a JSON file with your updated prompt slices.
2. Reference that file via the `prompt_file` parameter in your Crew.

CrewAI then merges your customizations with the defaults, so you don't have to redefine every prompt. Here's how:

### Example: Basic Prompt Customization

Create a `custom_prompts.json` file with the prompts you want to modify. Ensure you list all top-level prompts it should contain, not just your changes:
```

---

## Define your state model

**URL:** llms-txt#define-your-state-model

class UserPreferences(BaseModel):
    theme: str = "light"
    language: str = "English"

class AppState(BaseModel):
    user_name: str = ""
    preferences: UserPreferences = UserPreferences()
    items: List[str] = []
    processed: bool = False
    completion_percentage: float = 0.0

---

## Dog(name='Kona', age=3, breed='black german shepherd')

**URL:** llms-txt#dog(name='kona',-age=3,-breed='black-german-shepherd')

**Contents:**
- Advanced Features and Optimization
- Common Issues and Solutions

python theme={null}
    from crewai import LLM

# CrewAI automatically handles:
    # 1. Token counting and tracking
    # 2. Content summarization when needed
    # 3. Task splitting for large contexts

llm = LLM(
        model="gpt-4",
        max_tokens=4000,  # Limit response length
    )
    python theme={null}
        # Configure model with appropriate settings
        llm = LLM(
            model="openai/gpt-4-turbo-preview",
            temperature=0.7,    # Adjust based on task
            max_tokens=4096,    # Set based on output needs
            timeout=300        # Longer timeout for complex tasks
        )
        python theme={null}
    from crewai import LLM
    import os

os.environ["OPENAI_API_KEY"] = "<api-key>"

o3_llm = LLM(
        model="o3",
        drop_params=True,
        additional_drop_params=["stop"]
    )
    python theme={null}
    import httpx
    from crewai import LLM
    from crewai.llms.hooks import BaseInterceptor

class CustomInterceptor(BaseInterceptor[httpx.Request, httpx.Response]):
    """Custom interceptor to modify requests and responses."""

def on_outbound(self, request: httpx.Request) -> httpx.Request:
        """Print request before sending to the LLM provider."""
        print(request)
        return request

def on_inbound(self, response: httpx.Response) -> httpx.Response:
        """Process response after receiving from the LLM provider."""
        print(f"Status: {response.status_code}")
        print(f"Response time: {response.elapsed}")
        return response

# Use the interceptor with an LLM
    llm = LLM(
    model="openai/gpt-4o",
    interceptor=CustomInterceptor()
    )
    bash theme={null}
    # OpenAI
    OPENAI_API_KEY=sk-...

# Anthropic
    ANTHROPIC_API_KEY=sk-ant-...
    python theme={null}
    # Correct
    llm = LLM(model="openai/gpt-4")

# Incorrect
    llm = LLM(model="gpt-4")
    python theme={null}
    # Large context model
    llm = LLM(model="openai/gpt-4o")  # 128K tokens
    ```
  </Tab>
</Tabs>

**Examples:**

Example 1 (unknown):
```unknown
## Advanced Features and Optimization

Learn how to get the most out of your LLM configuration:

<AccordionGroup>
  <Accordion title="Context Window Management">
    CrewAI includes smart context management features:
```

Example 2 (unknown):
```unknown
<Info>
      Best practices for context management:

      1. Choose models with appropriate context windows
      2. Pre-process long inputs when possible
      3. Use chunking for large documents
      4. Monitor token usage to optimize costs
    </Info>
  </Accordion>

  <Accordion title="Performance Optimization">
    <Steps>
      <Step title="Token Usage Optimization">
        Choose the right context window for your task:

        * Small tasks (up to 4K tokens): Standard models
        * Medium tasks (between 4K-32K): Enhanced models
        * Large tasks (over 32K): Large context models
```

Example 3 (unknown):
```unknown
<Tip>
          * Lower temperature (0.1 to 0.3) for factual responses
          * Higher temperature (0.7 to 0.9) for creative tasks
        </Tip>
      </Step>

      <Step title="Best Practices">
        1. Monitor token usage
        2. Implement rate limiting
        3. Use caching when possible
        4. Set appropriate max\_tokens limits
      </Step>
    </Steps>

    <Info>
      Remember to regularly monitor your token usage and adjust your configuration as needed to optimize costs and performance.
    </Info>
  </Accordion>

  <Accordion title="Drop Additional Parameters">
    CrewAI internally uses native sdks for LLM calls, which allows you to drop additional parameters that are not needed for your specific use case. This can help simplify your code and reduce the complexity of your LLM configuration.
    For example, if you don't need to send the <code>stop</code> parameter, you can simply omit it from your LLM call:
```

Example 4 (unknown):
```unknown
</Accordion>

  <Accordion title="Transport Interceptors">
    CrewAI provides message interceptors for several providers, allowing you to hook into request/response cycles at the transport layer.

    **Supported Providers:**

    * ✅ OpenAI
    * ✅ Anthropic

    **Basic Usage:**
```

---

## Each can use different embedding providers

**URL:** llms-txt#each-can-use-different-embedding-providers

**Contents:**
- Knowledge Configuration
- Supported Knowledge Parameters
- Knowledge Storage Transparency
  - Where CrewAI Stores Knowledge Files
  - Finding Your Knowledge Storage Location

python Code theme={null}
from crewai.knowledge.knowledge_config import KnowledgeConfig

knowledge_config = KnowledgeConfig(results_limit=10, score_threshold=0.5)

agent = Agent(
    ...
    knowledge_config=knowledge_config
)

~/Library/Application Support/CrewAI/{project_name}/
└── knowledge/                    # Knowledge ChromaDB files
    ├── chroma.sqlite3           # ChromaDB metadata
    ├── {collection_id}/         # Vector embeddings
    └── knowledge_{collection}/  # Named collections

~/.local/share/CrewAI/{project_name}/
└── knowledge/
    ├── chroma.sqlite3
    ├── {collection_id}/
    └── knowledge_{collection}/

C:\Users\{username}\AppData\Local\CrewAI\{project_name}\
└── knowledge\
    ├── chroma.sqlite3
    ├── {collection_id}\
    └── knowledge_{collection}\
python theme={null}
from crewai.utilities.paths import db_storage_path
import os

**Examples:**

Example 1 (unknown):
```unknown
<Tip>
  Unlike retrieval from a vector database using a tool, agents preloaded with knowledge will not need a retrieval persona or task.
  Simply add the relevant knowledge sources your agent or crew needs to function.

  Knowledge sources can be added at the agent or crew level.
  Crew level knowledge sources will be used by **all agents** in the crew.
  Agent level knowledge sources will be used by the **specific agent** that is preloaded with the knowledge.
</Tip>

## Knowledge Configuration

You can configure the knowledge configuration for the crew or agent.
```

Example 2 (unknown):
```unknown
<Tip>
  `results_limit`: is the number of relevant documents to return. Default is 3.
  `score_threshold`: is the minimum score for a document to be considered relevant. Default is 0.35.
</Tip>

## Supported Knowledge Parameters

<ParamField type="List[BaseKnowledgeSource]">
  List of knowledge sources that provide content to be stored and queried. Can include PDF, CSV, Excel, JSON, text files, or string content.
</ParamField>

<ParamField type="str">
  Name of the collection where the knowledge will be stored. Used to identify different sets of knowledge. Defaults to "knowledge" if not provided.
</ParamField>

<ParamField type="Optional[KnowledgeStorage]">
  Custom storage configuration for managing how the knowledge is stored and retrieved. If not provided, a default storage will be created.
</ParamField>

## Knowledge Storage Transparency

<Info>
  **Understanding Knowledge Storage**: CrewAI automatically stores knowledge sources in platform-specific directories using ChromaDB for vector storage. Understanding these locations and defaults helps with production deployments, debugging, and storage management.
</Info>

### Where CrewAI Stores Knowledge Files

By default, CrewAI uses the same storage system as memory, storing knowledge in platform-specific directories:

#### Default Storage Locations by Platform

**macOS:**
```

Example 3 (unknown):
```unknown
**Linux:**
```

Example 4 (unknown):
```unknown
**Windows:**
```

---

## Ensure files are in the correct location

**URL:** llms-txt#ensure-files-are-in-the-correct-location

from crewai.utilities.constants import KNOWLEDGE_DIRECTORY
import os

knowledge_dir = KNOWLEDGE_DIRECTORY  # Usually "knowledge"
file_path = os.path.join(knowledge_dir, "your_file.pdf")

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Expected knowledge directory: {os.path.abspath(knowledge_dir)}")
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
**"Embedding dimension mismatch" errors:**
```

---

## Ensure TAVILY_API_KEY is set in your environment

**URL:** llms-txt#ensure-tavily_api_key-is-set-in-your-environment

---

## Ensure the TAVILY_API_KEY environment variable is set

**URL:** llms-txt#ensure-the-tavily_api_key-environment-variable-is-set

---

## Event Listeners

**URL:** llms-txt#event-listeners

**Contents:**
- Overview
- How It Works
- Creating a Custom Event Listener
- Properly Registering Your Listener
  - Option 1: Import and Instantiate in Your Crew or Flow Implementation

Source: https://docs.crewai.com/en/concepts/event-listener

Tap into CrewAI events to build custom integrations and monitoring

CrewAI provides a powerful event system that allows you to listen for and react to various events that occur during the execution of your Crew. This feature enables you to build custom integrations, monitoring solutions, logging systems, or any other functionality that needs to be triggered based on CrewAI's internal events.

CrewAI uses an event bus architecture to emit events throughout the execution lifecycle. The event system is built on the following components:

1. **CrewAIEventsBus**: A singleton event bus that manages event registration and emission
2. **BaseEvent**: Base class for all events in the system
3. **BaseEventListener**: Abstract base class for creating custom event listeners

When specific actions occur in CrewAI (like a Crew starting execution, an Agent completing a task, or a tool being used), the system emits corresponding events. You can register handlers for these events to execute custom code when they occur.

<Note type="info" title="Enterprise Enhancement: Prompt Tracing">
  CrewAI AOP provides a built-in Prompt Tracing feature that leverages the event system to track, store, and visualize all prompts, completions, and associated metadata. This provides powerful debugging capabilities and transparency into your agent operations.

<img alt="Prompt Tracing Dashboard" />

With Prompt Tracing you can:

* View the complete history of all prompts sent to your LLM
  * Track token usage and costs
  * Debug agent reasoning failures
  * Share prompt sequences with your team
  * Compare different prompt strategies
  * Export traces for compliance and auditing
</Note>

## Creating a Custom Event Listener

To create a custom event listener, you need to:

1. Create a class that inherits from `BaseEventListener`
2. Implement the `setup_listeners` method
3. Register handlers for the events you're interested in
4. Create an instance of your listener in the appropriate file

Here's a simple example of a custom event listener class:

## Properly Registering Your Listener

Simply defining your listener class isn't enough. You need to create an instance of it and ensure it's imported in your application. This ensures that:

1. The event handlers are registered with the event bus
2. The listener instance remains in memory (not garbage collected)
3. The listener is active when events are emitted

### Option 1: Import and Instantiate in Your Crew or Flow Implementation

The most important thing is to create an instance of your listener in the file where your Crew or Flow is defined and executed:

#### For Crew-based Applications

Create and import your listener at the top of your Crew implementation file:

```python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## Properly Registering Your Listener

Simply defining your listener class isn't enough. You need to create an instance of it and ensure it's imported in your application. This ensures that:

1. The event handlers are registered with the event bus
2. The listener instance remains in memory (not garbage collected)
3. The listener is active when events are emitted

### Option 1: Import and Instantiate in Your Crew or Flow Implementation

The most important thing is to create an instance of your listener in the file where your Crew or Flow is defined and executed:

#### For Crew-based Applications

Create and import your listener at the top of your Crew implementation file:
```

---

## Explicit type annotations

**URL:** llms-txt#explicit-type-annotations

def my_before_hook(context: ToolCallHookContext) -> bool | None:
    return None

def my_after_hook(context: ToolCallHookContext) -> str | None:
    return None

---

## External automation

**URL:** llms-txt#external-automation

analysis_automation = InvokeCrewAIAutomationTool(
    crew_api_url="https://analysis-crew.acme.crewai.com",
    crew_bearer_token="YOUR_BEARER_TOKEN",
    crew_name="Analysis Automation",
    crew_description="Runs the production-grade analysis pipeline",
)

---

## Extract all product information

**URL:** llms-txt#extract-all-product-information

result = stagehand_tool.run(
    instruction="Extract all product names, prices, and descriptions", 
    url="https://example.com/products",
    command_type="extract"
)

---

## Extract specific information with a selector

**URL:** llms-txt#extract-specific-information-with-a-selector

**Contents:**
  - 3. Observe Command

result = stagehand_tool.run(
    instruction="Extract the main article title and content", 
    url="https://example.com/blog/article",
    command_type="extract",
    selector=".article-container"  # Optional CSS selector
)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### 3. Observe Command

The `observe` command type identifies and analyzes webpage elements.
```

---

## Extract text from PDF

**URL:** llms-txt#extract-text-from-pdf

def extract_text_from_pdf(pdf_path):
    text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text.strip())
    return text

---

## Extract the text from the site

**URL:** llms-txt#extract-the-text-from-the-site

**Contents:**
- Arguments

text = tool.run()
print(text)
```

| Argument         | Type     | Description                                                                                                                                        |
| :--------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------- |
| **website\_url** | `string` | **Mandatory** website URL to read the file. This is the primary input for the tool, specifying which website's content should be scraped and read. |

---

## Fill out a form

**URL:** llms-txt#fill-out-a-form

**Contents:**
  - 2. Extract Command

result = stagehand_tool.run(
    instruction="Fill the contact form with name 'John Doe', email 'john@example.com', and message 'Hello world'", 
    url="https://example.com/contact"
)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### 2. Extract Command

The `extract` command type retrieves structured data from webpages.
```

---

## Find interactive elements

**URL:** llms-txt#find-interactive-elements

result = stagehand_tool.run(
    instruction="Find all interactive elements in the navigation menu", 
    url="https://example.com",
    command_type="observe"
)

---

## Fingerprinting

**URL:** llms-txt#fingerprinting

**Contents:**
- Overview
- How Fingerprints Work
- Basic Usage
  - Accessing Fingerprints

Source: https://docs.crewai.com/en/guides/advanced/fingerprinting

Learn how to use CrewAI's fingerprinting system to uniquely identify and track components throughout their lifecycle.

Fingerprints in CrewAI provide a way to uniquely identify and track components throughout their lifecycle. Each `Agent`, `Crew`, and `Task` automatically receives a unique fingerprint when created, which cannot be manually overridden.

These fingerprints can be used for:

* Auditing and tracking component usage
* Ensuring component identity integrity
* Attaching metadata to components
* Creating a traceable chain of operations

## How Fingerprints Work

A fingerprint is an instance of the `Fingerprint` class from the `crewai.security` module. Each fingerprint contains:

* A UUID string: A unique identifier for the component that is automatically generated and cannot be manually set
* A creation timestamp: When the fingerprint was generated, automatically set and cannot be manually modified
* Metadata: A dictionary of additional information that can be customized

Fingerprints are automatically generated and assigned when a component is created. Each component exposes its fingerprint through a read-only property.

### Accessing Fingerprints

```python theme={null}
from crewai import Agent, Crew, Task

---

## First, install and run Ollama locally, then pull an embedding model:

**URL:** llms-txt#first,-install-and-run-ollama-locally,-then-pull-an-embedding-model:

---

## First run

**URL:** llms-txt#first-run

flow1 = PersistentCounterFlow()
result1 = flow1.kickoff()
print(f"First run result: {result1}")

---

## Fix permissions

**URL:** llms-txt#fix-permissions

chmod -R 755 ~/.local/share/CrewAI/
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
**"Database is locked" errors:**
```

---

## Fix storage permissions

**URL:** llms-txt#fix-storage-permissions

chmod -R 755 ~/.local/share/CrewAI/
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
**Knowledge not persisting between runs:**
```

---

## For dynamic directory specification at runtime

**URL:** llms-txt#for-dynamic-directory-specification-at-runtime

tool = DirectorySearchTool()

---

## For fixed directory searches

**URL:** llms-txt#for-fixed-directory-searches

**Contents:**
- Arguments
- Custom Model and Embeddings

tool = DirectorySearchTool(directory='/path/to/directory')
python Code theme={null}
from chromadb.config import Settings

tool = DirectorySearchTool(
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

* `directory`: A string argument that specifies the search directory. This is optional during initialization but required for searches if not set initially.

## Custom Model and Embeddings

The DirectorySearchTool uses OpenAI for embeddings and summarization by default. Customization options for these settings include changing the model provider and configuration, enhancing flexibility for advanced users.
```

---

## For Simple DSL Integration (Recommended)

**URL:** llms-txt#for-simple-dsl-integration-(recommended)

---

## General JSON content search

**URL:** llms-txt#general-json-content-search

---

## Generate and inspect the actual prompt

**URL:** llms-txt#generate-and-inspect-the-actual-prompt

generated_prompt = prompt_generator.task_execution()

---

## Generate OpenAI embeddings

**URL:** llms-txt#generate-openai-embeddings

def get_openai_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-large"
    )
    return response.data[0].embedding

---

## Get API keys for services

**URL:** llms-txt#get-api-keys-for-services

OPENAI_API_KEY = getpass("🔑 Enter your OpenAI API key: ")

---

## Get a free-form response

**URL:** llms-txt#get-a-free-form-response

result = analyst.kickoff("Analyze the AI market in 2025")
print(result.raw)  # Access the raw response

---

## GET /inputs

**URL:** llms-txt#get-/inputs

Source: https://docs.crewai.com/en/api-reference/inputs

enterprise-api.en.yaml get /inputs
Get required inputs for your crew

---

## Get keys for your project from the project settings page: https://cloud.langfuse.com

**URL:** llms-txt#get-keys-for-your-project-from-the-project-settings-page:-https://cloud.langfuse.com

os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..." 
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..."
os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com" # 🇪🇺 EU region

---

## GET /{kickoff_id}/status

**URL:** llms-txt#get-/{kickoff_id}/status

Source: https://docs.crewai.com/en/api-reference/status

enterprise-api.en.yaml get /{kickoff_id}/status
Get execution status

---

## Get or create collection

**URL:** llms-txt#get-or-create-collection

test_docs = client.collections.get("example_collections")
if not test_docs:
    test_docs = client.collections.create(
        name="example_collections",
        vectorizer_config=Configure.Vectorizer.text2vec_openai(model="nomic-embed-text"),
        generative_config=Configure.Generative.openai(model="gpt-4o"),
    )

---

## Get structured output

**URL:** llms-txt#get-structured-output

structured_result = analyst.kickoff(
    "Provide a structured analysis of the AI market in 2025",
    response_format=MarketAnalysis
)

---

## Get the base storage path

**URL:** llms-txt#get-the-base-storage-path

storage_path = db_storage_path()
print(f"CrewAI storage location: {storage_path}")

---

## Get the knowledge storage path

**URL:** llms-txt#get-the-knowledge-storage-path

knowledge_path = os.path.join(db_storage_path(), "knowledge")
print(f"Knowledge storage location: {knowledge_path}")

---

## Get the status of your deployment

**URL:** llms-txt#get-the-status-of-your-deployment

---

## Get your Braintrust credentials

**URL:** llms-txt#get-your-braintrust-credentials

BRAINTRUST_API_KEY = getpass("🔑 Enter your Braintrust API Key: ")

---

## Get your Phoenix Cloud credentials

**URL:** llms-txt#get-your-phoenix-cloud-credentials

PHOENIX_API_KEY = getpass("🔑 Enter your Phoenix Cloud API Key: ")

---

## High-capability reasoning model for strategic planning

**URL:** llms-txt#high-capability-reasoning-model-for-strategic-planning

manager_llm = LLM(model="gemini-2.5-flash-preview-05-20", temperature=0.1)

---

## Human Feedback in Flows

**URL:** llms-txt#human-feedback-in-flows

**Contents:**
- Overview
- Quick Start
- The @human\_feedback Decorator
  - Parameters
  - Basic Usage (No Routing)
  - Routing with emit
- HumanFeedbackResult
  - Accessing in Listeners
- Accessing Feedback History
  - last\_human\_feedback

Source: https://docs.crewai.com/en/learn/human-feedback-in-flows

Learn how to integrate human feedback directly into your CrewAI Flows using the @human_feedback decorator

The `@human_feedback` decorator enables human-in-the-loop (HITL) workflows directly within CrewAI Flows. It allows you to pause flow execution, present output to a human for review, collect their feedback, and optionally route to different listeners based on the feedback outcome.

This is particularly valuable for:

* **Quality assurance**: Review AI-generated content before it's used downstream
* **Decision gates**: Let humans make critical decisions in automated workflows
* **Approval workflows**: Implement approve/reject/revise patterns
* **Interactive refinement**: Collect feedback to improve outputs iteratively

Here's the simplest way to add human feedback to a flow:

When this flow runs, it will:

1. Execute `generate_content` and return the string
2. Display the output to the user with the request message
3. Wait for the user to type feedback (or press Enter to skip)
4. Pass a `HumanFeedbackResult` object to `process_feedback`

## The @human\_feedback Decorator

| Parameter         | Type                    | Required              | Description                                                                                                     |
| ----------------- | ----------------------- | --------------------- | --------------------------------------------------------------------------------------------------------------- |
| `message`         | `str`                   | Yes                   | The message shown to the human alongside the method output                                                      |
| `emit`            | `Sequence[str]`         | No                    | List of possible outcomes. Feedback is collapsed to one of these, which triggers `@listen` decorators           |
| `llm`             | `str \| BaseLLM`        | When `emit` specified | LLM used to interpret feedback and map to an outcome                                                            |
| `default_outcome` | `str`                   | No                    | Outcome to use if no feedback provided. Must be in `emit`                                                       |
| `metadata`        | `dict`                  | No                    | Additional data for enterprise integrations                                                                     |
| `provider`        | `HumanFeedbackProvider` | No                    | Custom provider for async/non-blocking feedback. See [Async Human Feedback](#async-human-feedback-non-blocking) |

### Basic Usage (No Routing)

When you don't specify `emit`, the decorator simply collects feedback and passes a `HumanFeedbackResult` to the next listener:

### Routing with emit

When you specify `emit`, the decorator becomes a router. The human's free-form feedback is interpreted by an LLM and collapsed into one of the specified outcomes:

<Tip>
  The LLM uses structured outputs (function calling) when available to guarantee the response is one of your specified outcomes. This makes routing reliable and predictable.
</Tip>

## HumanFeedbackResult

The `HumanFeedbackResult` dataclass contains all information about a human feedback interaction:

### Accessing in Listeners

When a listener is triggered by a `@human_feedback` method with `emit`, it receives the `HumanFeedbackResult`:

## Accessing Feedback History

The `Flow` class provides two attributes for accessing human feedback:

### last\_human\_feedback

Returns the most recent `HumanFeedbackResult`:

### human\_feedback\_history

A list of all `HumanFeedbackResult` objects collected during the flow:

<Warning>
  Each `HumanFeedbackResult` is appended to `human_feedback_history`, so multiple feedback steps won't overwrite each other. Use this list to access all feedback collected during the flow.
</Warning>

## Complete Example: Content Approval Workflow

Here's a full example implementing a content review and approval workflow:

## Combining with Other Decorators

The `@human_feedback` decorator works with other flow decorators. Place it as the innermost decorator (closest to the function):

```python Code theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## Quick Start

Here's the simplest way to add human feedback to a flow:
```

Example 2 (unknown):
```unknown
When this flow runs, it will:

1. Execute `generate_content` and return the string
2. Display the output to the user with the request message
3. Wait for the user to type feedback (or press Enter to skip)
4. Pass a `HumanFeedbackResult` object to `process_feedback`

## The @human\_feedback Decorator

### Parameters

| Parameter         | Type                    | Required              | Description                                                                                                     |
| ----------------- | ----------------------- | --------------------- | --------------------------------------------------------------------------------------------------------------- |
| `message`         | `str`                   | Yes                   | The message shown to the human alongside the method output                                                      |
| `emit`            | `Sequence[str]`         | No                    | List of possible outcomes. Feedback is collapsed to one of these, which triggers `@listen` decorators           |
| `llm`             | `str \| BaseLLM`        | When `emit` specified | LLM used to interpret feedback and map to an outcome                                                            |
| `default_outcome` | `str`                   | No                    | Outcome to use if no feedback provided. Must be in `emit`                                                       |
| `metadata`        | `dict`                  | No                    | Additional data for enterprise integrations                                                                     |
| `provider`        | `HumanFeedbackProvider` | No                    | Custom provider for async/non-blocking feedback. See [Async Human Feedback](#async-human-feedback-non-blocking) |

### Basic Usage (No Routing)

When you don't specify `emit`, the decorator simply collects feedback and passes a `HumanFeedbackResult` to the next listener:
```

Example 3 (unknown):
```unknown
### Routing with emit

When you specify `emit`, the decorator becomes a router. The human's free-form feedback is interpreted by an LLM and collapsed into one of the specified outcomes:
```

Example 4 (unknown):
```unknown
<Tip>
  The LLM uses structured outputs (function calling) when available to guarantee the response is one of your specified outcomes. This makes routing reliable and predictable.
</Tip>

## HumanFeedbackResult

The `HumanFeedbackResult` dataclass contains all information about a human feedback interaction:
```

---

## Identify form fields

**URL:** llms-txt#identify-form-fields

**Contents:**
- Configuration Options
- Best Practices
- Troubleshooting
- Additional Resources

result = stagehand_tool.run(
    instruction="Identify all the input fields in the registration form", 
    url="https://example.com/register",
    command_type="observe",
    selector="#registration-form"
)
python theme={null}
stagehand_tool = StagehandTool(
    api_key="your-browserbase-api-key",
    project_id="your-browserbase-project-id",
    model_api_key="your-llm-api-key",
    model_name=AvailableModel.CLAUDE_3_7_SONNET_LATEST,
    dom_settle_timeout_ms=5000,  # Wait longer for DOM to settle
    headless=True,  # Run browser in headless mode
    self_heal=True,  # Attempt to recover from errors
    wait_for_captcha_solves=True,  # Wait for CAPTCHA solving
    verbose=1,  # Control logging verbosity (0-3)
)
```

1. **Be Specific**: Provide detailed instructions for better results
2. **Choose Appropriate Command Type**: Select the right command type for your task
3. **Use Selectors**: Leverage CSS selectors to improve accuracy
4. **Break Down Complex Tasks**: Split complex workflows into multiple tool calls
5. **Implement Error Handling**: Add error handling for potential issues

Common issues and solutions:

* **Session Issues**: Verify API keys for both Browserbase and LLM provider
* **Element Not Found**: Increase `dom_settle_timeout_ms` for slower pages
* **Action Failures**: Use `observe` to identify correct elements first
* **Incomplete Data**: Refine instructions or provide specific selectors

## Additional Resources

For questions about the CrewAI integration:

* Join Stagehand's [Slack community](https://stagehand.dev/slack)
* Open an issue in the [Stagehand repository](https://github.com/browserbase/stagehand)
* Visit [Stagehand documentation](https://docs.stagehand.dev/)

**Examples:**

Example 1 (unknown):
```unknown
## Configuration Options

Customize the StagehandTool behavior with these parameters:
```

---

## If an error occurs during reasoning, it will be logged and execution will continue

**URL:** llms-txt#if-an-error-occurs-during-reasoning,-it-will-be-logged-and-execution-will-continue

**Contents:**
- Example Reasoning Output

result = agent.execute_task(task)

Task: Analyze the provided sales data and identify key trends.

Reasoning Plan:
I'll analyze the sales data to identify the top 3 trends.

1. Understanding of the task:
   I need to analyze sales data to identify key trends that would be valuable for business decision-making.

2. Key steps I'll take:
   - First, I'll examine the data structure to understand what fields are available
   - Then I'll perform exploratory data analysis to identify patterns
   - Next, I'll analyze sales by time periods to identify temporal trends
   - I'll also analyze sales by product categories and customer segments
   - Finally, I'll identify the top 3 most significant trends

3. Approach to challenges:
   - If the data has missing values, I'll decide whether to fill or filter them
   - If the data has outliers, I'll investigate whether they're valid data points or errors
   - If trends aren't immediately obvious, I'll apply statistical methods to uncover patterns

4. Use of available tools:
   - I'll use data analysis tools to explore and visualize the data
   - I'll use statistical tools to identify significant patterns
   - I'll use knowledge retrieval to access relevant information about sales analysis

5. Expected outcome:
   A concise report highlighting the top 3 sales trends with supporting evidence from the data.

READY: I am ready to execute the task.
```

This reasoning plan helps the agent organize its approach to the task, consider potential challenges, and ensure it delivers the expected output.

**Examples:**

Example 1 (unknown):
```unknown
## Example Reasoning Output

Here's an example of what a reasoning plan might look like for a data analysis task:
```

---

## If hook2 returns False:

**URL:** llms-txt#if-hook2-returns-false:

---

## If QdrantConfig has a preset filter for category="research"

**URL:** llms-txt#if-qdrantconfig-has-a-preset-filter-for-category="research"

---

## if the URL is known or discovered during its execution:

**URL:** llms-txt#if-the-url-is-known-or-discovered-during-its-execution:

tool = CodeDocsSearchTool()

---

## If your handler is async (FastAPI, aiohttp, Slack Bolt async, etc.)

**URL:** llms-txt#if-your-handler-is-async-(fastapi,-aiohttp,-slack-bolt-async,-etc.)

**Contents:**
  - Best Practices for Async Feedback
- Related Documentation

async def on_slack_feedback_async(flow_id: str, slack_message: str):
    flow = ContentPipeline.from_pending(flow_id)
    result = await flow.resume_async(slack_message)
    return result
```

<Warning>
  If you're using an async web framework (FastAPI, aiohttp, Slack Bolt async mode), use `await flow.resume_async()` instead of `flow.resume()`. Calling `resume()` from within a running event loop will raise a `RuntimeError`.
</Warning>

### Best Practices for Async Feedback

1. **Check the return type**: `kickoff()` returns `HumanFeedbackPending` when paused—no try/except needed
2. **Use the right resume method**: Use `resume()` in sync code, `await resume_async()` in async code
3. **Store callback info**: Use `callback_info` to store webhook URLs, ticket IDs, etc.
4. **Implement idempotency**: Your resume handler should be idempotent for safety
5. **Automatic persistence**: State is automatically saved when `HumanFeedbackPending` is raised and uses `SQLiteFlowPersistence` by default
6. **Custom persistence**: Pass a custom persistence instance to `from_pending()` if needed

## Related Documentation

* [Flows Overview](/en/concepts/flows) - Learn about CrewAI Flows
* [Flow State Management](/en/guides/flows/mastering-flow-state) - Managing state in flows
* [Flow Persistence](/en/concepts/flows#persistence) - Persisting flow state
* [Routing with @router](/en/concepts/flows#router) - More about conditional routing
* [Human Input on Execution](/en/learn/human-input-on-execution) - Task-level human input

---

## ignore_scrape_failures=True

**URL:** llms-txt#ignore_scrape_failures=true

---

## Initialize enhanced tracing

**URL:** llms-txt#initialize-enhanced-tracing

Traceloop.init(
    api_endpoint="https://your-truefoundry-endpoint/api/tracing",
    headers={
        "Authorization": f"Bearer {your_truefoundry_pat_token}",
        "TFY-Tracing-Project": "your_project_name",
    },
)
```

This provides additional trace correlation across your entire CrewAI workflow.

<img alt="TrueFoundry CrewAI Tracing" />

---

## Initialize OpenAI client

**URL:** llms-txt#initialize-openai-client

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

---

## Initialize Qdrant client and load data

**URL:** llms-txt#initialize-qdrant-client-and-load-data

qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)
collection_name = "example_collection"
pdf_path = "path/to/your/document.pdf"
load_pdf_to_qdrant(pdf_path, qdrant, collection_name)

---

## Initialize the Patronus client

**URL:** llms-txt#initialize-the-patronus-client

---

## Initialize with custom configuration

**URL:** llms-txt#initialize-with-custom-configuration

**Contents:**
- Features
- Response Format
- Use Cases

extractor_tool = TavilyExtractorTool(
    extract_depth='advanced',  # More comprehensive extraction
    include_images=True,       # Include image results
    timeout=90                 # Custom timeout
)
```

* **Single or Multiple URLs**: Extract content from one URL or process multiple URLs in a single request
* **Configurable Depth**: Choose between basic (fast) and advanced (comprehensive) extraction modes
* **Image Support**: Optionally include images in the extraction results
* **Structured Output**: Returns well-formatted JSON containing the extracted content
* **Error Handling**: Robust handling of network timeouts and extraction errors

The tool returns a JSON string representing the structured data extracted from the provided URL(s). The exact structure depends on the content of the pages and the `extract_depth` used.

Common response elements include:

* **Title**: The page title
* **Content**: Main text content of the page
* **Images**: Image URLs and metadata (when `include_images=True`)
* **Metadata**: Additional page information like author, description, etc.

* **Content Analysis**: Extract and analyze content from competitor websites
* **Research**: Gather structured data from multiple sources for analysis
* **Content Migration**: Extract content from existing websites for migration
* **Monitoring**: Regular extraction of content for change detection
* **Data Collection**: Systematic extraction of information from web sources

Refer to the [Tavily API documentation](https://docs.tavily.com/docs/tavily-api/python-sdk#extract) for detailed information about the response structure and available options.

---

## Instead of modifying lists in place:

**URL:** llms-txt#instead-of-modifying-lists-in-place:

self.state.items.append(new_item)  # Mutable operation

---

## In your main.py or flow.py file

**URL:** llms-txt#in-your-main.py-or-flow.py-file

from crewai.flow import Flow, listen, start
from my_listeners import MyCustomListener

---

## Iterate over streaming output

**URL:** llms-txt#iterate-over-streaming-output

flow = StreamingFlow()
streaming = flow.kickoff()
for chunk in streaming:
    print(chunk.content, end="", flush=True)

---

## it learns about during execution

**URL:** llms-txt#it-learns-about-during-execution

tool = DirectoryReadTool()

---

## LangDB credentials

**URL:** llms-txt#langdb-credentials

export LANGDB_API_KEY="<your_langdb_api_key>"
export LANGDB_PROJECT_ID="<your_langdb_project_id>"
export LANGDB_API_BASE_URL='https://api.us-east-1.langdb.ai'

---

## LangDB Integration

**URL:** llms-txt#langdb-integration

Source: https://docs.crewai.com/en/observability/langdb

Govern, secure, and optimize your CrewAI workflows with LangDB AI Gateway—access 350+ models, automatic routing, cost optimization, and full observability.

---

## Langfuse Integration

**URL:** llms-txt#langfuse-integration

Source: https://docs.crewai.com/en/observability/langfuse

Learn how to integrate Langfuse with CrewAI via OpenTelemetry using OpenLit

---

## Later...

**URL:** llms-txt#later...

**Contents:**
  - Clearing Hooks

success = unregister_before_tool_call_hook(my_hook)
print(f"Unregistered: {success}")
python theme={null}
from crewai.hooks import (
    clear_before_tool_call_hooks,
    clear_after_tool_call_hooks,
    clear_all_tool_call_hooks
)

**Examples:**

Example 1 (unknown):
```unknown
### Clearing Hooks
```

---

## Later, unregister

**URL:** llms-txt#later,-unregister

**Contents:**
- Best Practices
  - 1. Keep Hooks Focused

success = unregister_before_llm_call_hook(my_hook)
print(f"Unregistered: {success}")
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## Best Practices

### 1. Keep Hooks Focused

Each hook should have a single, clear responsibility:
```

---

## Link: https://link.springer.com/article/10.1007/s10439-023-03171-8

**URL:** llms-txt#link:-https://link.springer.com/article/10.1007/s10439-023-03171-8

---

## Link: https://link.springer.com/article/10.1007/s10439-023-03172-7

**URL:** llms-txt#link:-https://link.springer.com/article/10.1007/s10439-023-03172-7

---

## Link: https://olympics.com/fr/paris-2024

**URL:** llms-txt#link:-https://olympics.com/fr/paris-2024

---

## Link: https://tickets.paris2024.org/

**URL:** llms-txt#link:-https://tickets.paris2024.org/

---

## List all your deployments

**URL:** llms-txt#list-all-your-deployments

---

## List knowledge collections and files

**URL:** llms-txt#list-knowledge-collections-and-files

**Contents:**
  - Controlling Knowledge Storage Locations

if os.path.exists(knowledge_path):
    print("\nKnowledge storage contents:")
    for item in os.listdir(knowledge_path):
        item_path = os.path.join(knowledge_path, item)
        if os.path.isdir(item_path):
            print(f"📁 Collection: {item}/")
            # Show collection contents
            try:
                for subitem in os.listdir(item_path):
                    print(f"   └── {subitem}")
            except PermissionError:
                print(f"   └── (permission denied)")
        else:
            print(f"📄 {item}")
else:
    print("No knowledge storage found yet.")
python theme={null}
import os
from crewai import Crew

**Examples:**

Example 1 (unknown):
```unknown
### Controlling Knowledge Storage Locations

#### Option 1: Environment Variable (Recommended)
```

---

## LLM Call Hooks

**URL:** llms-txt#llm-call-hooks

**Contents:**
- Overview
- Hook Types
  - Before LLM Call Hooks
  - After LLM Call Hooks
- LLM Hook Context
  - Modifying Messages

Source: https://docs.crewai.com/en/learn/llm-hooks

Learn how to use LLM call hooks to intercept, modify, and control language model interactions in CrewAI

LLM Call Hooks provide fine-grained control over language model interactions during agent execution. These hooks allow you to intercept LLM calls, modify prompts, transform responses, implement approval gates, and add custom logging or monitoring.

LLM hooks are executed at two critical points:

* **Before LLM Call**: Modify messages, validate inputs, or block execution
* **After LLM Call**: Transform responses, sanitize outputs, or modify conversation history

### Before LLM Call Hooks

Executed before every LLM call, these hooks can:

* Inspect and modify messages sent to the LLM
* Block LLM execution based on conditions
* Implement rate limiting or approval gates
* Add context or system messages
* Log request details

### After LLM Call Hooks

Executed after every LLM call, these hooks can:

* Modify or sanitize LLM responses
* Add metadata or formatting
* Log response details
* Update conversation history
* Implement content filtering

The `LLMCallHookContext` object provides comprehensive access to execution state:

### Modifying Messages

**Important:** Always modify messages in-place:

```python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### After LLM Call Hooks

Executed after every LLM call, these hooks can:

* Modify or sanitize LLM responses
* Add metadata or formatting
* Log response details
* Update conversation history
* Implement content filtering

**Signature:**
```

Example 2 (unknown):
```unknown
## LLM Hook Context

The `LLMCallHookContext` object provides comprehensive access to execution state:
```

Example 3 (unknown):
```unknown
### Modifying Messages

**Important:** Always modify messages in-place:
```

---

## Load documents

**URL:** llms-txt#load-documents

docs_to_load = os.listdir("knowledge")
with test_docs.batch.dynamic() as batch:
    for d in docs_to_load:
        with open(os.path.join("knowledge", d), "r") as f:
            content = f.read()
        batch.add_object(
            {
                "content": content,
                "year": d.split("_")[0],
            }
        )

---

## Load environment variables

**URL:** llms-txt#load-environment-variables

---

## Load model and tokenizer

**URL:** llms-txt#load-model-and-tokenizer

tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

def custom_embeddings(text: str) -> list[float]:
    # Tokenize and get model outputs
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)

# Use mean pooling to get text embedding
    embeddings = outputs.last_hidden_state.mean(dim=1)

# Convert to list of floats and return
    return embeddings[0].tolist()

---

## Load text content from a local folder and add to MongoDB

**URL:** llms-txt#load-text-content-from-a-local-folder-and-add-to-mongodb

texts = []
for fname in os.listdir("knowledge"):
    path = os.path.join("knowledge", fname)
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            texts.append(f.read())

tool.add_texts(texts)

---

## make sure OXYLABS_USERNAME and OXYLABS_PASSWORD variables are set

**URL:** llms-txt#make-sure-oxylabs_username-and-oxylabs_password-variables-are-set

tool = OxylabsUniversalScraperTool(
    config={
        "render": "html",
        "user_agent_type": "mobile",
        "context": [
            {"key": "force_headers", "value": True},
            {"key": "force_cookies", "value": True},
            {
                "key": "headers",
                "value": {
                    "Custom-Header-Name": "custom header content",
                },
            },
            {
                "key": "cookies",
                "value": [
                    {"key": "NID", "value": "1234567890"},
                    {"key": "1P JAR", "value": "0987654321"},
                ],
            },
            {"key": "http_method", "value": "get"},
            {"key": "follow_redirects", "value": True},
            {"key": "successful_status_codes", "value": [808, 909]},
        ],
    }
)

result = tool.run(url="https://ip.oxylabs.io")

---

## Mastering Flow State Management

**URL:** llms-txt#mastering-flow-state-management

**Contents:**
- Understanding the Power of State in Flows
  - Why State Management Matters
- State Management Fundamentals
  - The Flow State Lifecycle
  - Two Approaches to State Management
- Unstructured State Management
  - How It Works
  - Basic Example

Source: https://docs.crewai.com/en/guides/flows/mastering-flow-state

A comprehensive guide to managing, persisting, and leveraging state in CrewAI Flows for building robust AI applications.

## Understanding the Power of State in Flows

State management is the backbone of any sophisticated AI workflow. In CrewAI Flows, the state system allows you to maintain context, share data between steps, and build complex application logic. Mastering state management is essential for creating reliable, maintainable, and powerful AI applications.

This guide will walk you through everything you need to know about managing state in CrewAI Flows, from basic concepts to advanced techniques, with practical code examples along the way.

### Why State Management Matters

Effective state management enables you to:

1. **Maintain context across execution steps** - Pass information seamlessly between different stages of your workflow
2. **Build complex conditional logic** - Make decisions based on accumulated data
3. **Create persistent applications** - Save and restore workflow progress
4. **Handle errors gracefully** - Implement recovery patterns for more robust applications
5. **Scale your applications** - Support complex workflows with proper data organization
6. **Enable conversational applications** - Store and access conversation history for context-aware AI interactions

Let's explore how to leverage these capabilities effectively.

## State Management Fundamentals

### The Flow State Lifecycle

In CrewAI Flows, the state follows a predictable lifecycle:

1. **Initialization** - When a flow is created, its state is initialized (either as an empty dictionary or a Pydantic model instance)
2. **Modification** - Flow methods access and modify the state as they execute
3. **Transmission** - State is passed automatically between flow methods
4. **Persistence** (optional) - State can be saved to storage and later retrieved
5. **Completion** - The final state reflects the cumulative changes from all executed methods

Understanding this lifecycle is crucial for designing effective flows.

### Two Approaches to State Management

CrewAI offers two ways to manage state in your flows:

1. **Unstructured State** - Using dictionary-like objects for flexibility
2. **Structured State** - Using Pydantic models for type safety and validation

Let's examine each approach in detail.

## Unstructured State Management

Unstructured state uses a dictionary-like approach, offering flexibility and simplicity for straightforward applications.

With unstructured state:

* You access state via `self.state` which behaves like a dictionary
* You can freely add, modify, or remove keys at any point
* All state is automatically available to all flow methods

Here's a simple example of unstructured state management:

```python theme={null}
from crewai.flow.flow import Flow, listen, start

class UnstructuredStateFlow(Flow):
    @start()
    def initialize_data(self):
        print("Initializing flow data")
        # Add key-value pairs to state
        self.state["user_name"] = "Alex"
        self.state["preferences"] = {
            "theme": "dark",
            "language": "English"
        }
        self.state["items"] = []

# The flow state automatically gets a unique ID
        print(f"Flow ID: {self.state['id']}")

@listen(initialize_data)
    def process_data(self, previous_result):
        print(f"Previous step returned: {previous_result}")

# Access and modify state
        user = self.state["user_name"]
        print(f"Processing data for {user}")

# Add items to a list in state
        self.state["items"].append("item1")
        self.state["items"].append("item2")

# Add a new key-value pair
        self.state["processed"] = True

@listen(process_data)
    def generate_summary(self, previous_result):
        # Access multiple state values
        user = self.state["user_name"]
        theme = self.state["preferences"]["theme"]
        items = self.state["items"]
        processed = self.state.get("processed", False)

summary = f"User {user} has {len(items)} items with {theme} theme. "
        summary += "Data is processed." if processed else "Data is not processed."

---

## Maxim API Configuration

**URL:** llms-txt#maxim-api-configuration

**Contents:**
  - 2. Import the required packages
  - 3. Initialise Maxim with your API key

MAXIM_API_KEY=your_api_key_here
MAXIM_LOG_REPO_ID=your_repo_id_here
python theme={null}
from crewai import Agent, Task, Crew, Process
from maxim import Maxim
from maxim.logger.crewai import instrument_crewai
python {8} theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### 2. Import the required packages
```

Example 2 (unknown):
```unknown
### 3. Initialise Maxim with your API key
```

---

## Maxim Integration

**URL:** llms-txt#maxim-integration

Source: https://docs.crewai.com/en/observability/maxim

Start Agent monitoring, evaluation, and observability

---

## Memory

**URL:** llms-txt#memory

**Contents:**
- Overview
- Memory System Components
- 1. Basic Memory System (Recommended)
  - Quick Start

Source: https://docs.crewai.com/en/concepts/memory

Leveraging memory systems in the CrewAI framework to enhance agent capabilities.

The CrewAI framework provides a sophisticated memory system designed to significantly enhance AI agent capabilities. CrewAI offers **two distinct memory approaches** that serve different use cases:

1. **Basic Memory System** - Built-in short-term, long-term, and entity memory
2. **External Memory** - Standalone external memory providers

## Memory System Components

| Component             | Description                                                                                                                                                                                                                       |
| :-------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Short-Term Memory** | Temporarily stores recent interactions and outcomes using `RAG`, enabling agents to recall and utilize information relevant to their current context during the current executions.                                               |
| **Long-Term Memory**  | Preserves valuable insights and learnings from past executions, allowing agents to build and refine their knowledge over time.                                                                                                    |
| **Entity Memory**     | Captures and organizes information about entities (people, places, concepts) encountered during tasks, facilitating deeper understanding and relationship mapping. Uses `RAG` for storing entity information.                     |
| **Contextual Memory** | Maintains the context of interactions by combining `ShortTermMemory`, `LongTermMemory`, `ExternalMemory` and `EntityMemory`, aiding in the coherence and relevance of agent responses over a sequence of tasks or a conversation. |

## 1. Basic Memory System (Recommended)

The simplest and most commonly used approach. Enable memory for your crew with a single parameter:

```python theme={null}
from crewai import Crew, Agent, Task, Process

---

## Metadata - for additional information (can be customized)

**URL:** llms-txt#metadata---for-additional-information-(can-be-customized)

metadata = fingerprint.metadata  # A dictionary, defaults to {}
```

---

## Mix function-based and LLM-based guardrails

**URL:** llms-txt#mix-function-based-and-llm-based-guardrails

**Contents:**
  - Guardrail Function Requirements
  - Error Handling Best Practices
  - Handling Guardrail Results
- Getting Structured Consistent Outputs from Tasks
  - Using `output_pydantic`

blog_task = Task(
    description="Write a blog post about AI",
    expected_output="A well-formatted blog post between 100-500 words",
    agent=blog_agent,
    guardrails=[
        validate_word_count,  # Function-based: precise word count check
        "The content must be engaging and suitable for a general audience",  # LLM-based: subjective quality check
        "The writing style should be clear, concise, and free of technical jargon"  # LLM-based: style validation
    ],
    guardrail_max_retries=3
)
python Code theme={null}
from crewai import TaskOutput, LLMGuardrail

def validate_with_context(result: TaskOutput) -> Tuple[bool, Any]:
    try:
        # Main validation logic
        validated_data = perform_validation(result)
        return (True, validated_data)
    except ValidationError as e:
        return (False, f"VALIDATION_ERROR: {str(e)}")
    except Exception as e:
        return (False, str(e))
python Code theme={null}
from typing import Any, Dict, List, Tuple, Union
from crewai import TaskOutput

def complex_validation(result: TaskOutput) -> Tuple[bool, Any]:
    """Chain multiple validation steps."""
    # Step 1: Basic validation
    if not result:
        return (False, "Empty result")

# Step 2: Content validation
    try:
        validated = validate_content(result)
        if not validated:
            return (False, "Invalid content")

# Step 3: Format validation
        formatted = format_output(validated)
        return (True, formatted)
    except Exception as e:
        return (False, str(e))
python Code theme={null}
from typing import Optional, Tuple, Union
from crewai import TaskOutput, Task

def validate_json_output(result: TaskOutput) -> Tuple[bool, Any]:
    """Validate and parse JSON output."""
    try:
        # Try to parse as JSON
        data = json.loads(result)
        return (True, data)
    except json.JSONDecodeError as e:
        return (False, "Invalid JSON format")

task = Task(
    description="Generate a JSON report",
    expected_output="A valid JSON object",
    agent=analyst,
    guardrail=validate_json_output,
    guardrail_max_retries=3  # Limit retry attempts
)
python Code theme={null}
import json

from crewai import Agent, Crew, Process, Task
from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    content: str

blog_agent = Agent(
    role="Blog Content Generator Agent",
    goal="Generate a blog title and content",
    backstory="""You are an expert content creator, skilled in crafting engaging and informative blog posts.""",
    verbose=False,
    allow_delegation=False,
    llm="gpt-4o",
)

task1 = Task(
    description="""Create a blog title and content on a given topic. Make sure the content is under 200 words.""",
    expected_output="A compelling blog title and well-written content.",
    agent=blog_agent,
    output_pydantic=Blog,
)

**Examples:**

Example 1 (unknown):
```unknown
This approach combines the precision of programmatic validation with the flexibility of LLM-based assessment for subjective criteria.

### Guardrail Function Requirements

1. **Function Signature**:
   * Must accept exactly one parameter (the task output)
   * Should return a tuple of `(bool, Any)`
   * Type hints are recommended but optional

2. **Return Values**:
   * On success: it returns a tuple of `(bool, Any)`. For example: `(True, validated_result)`
   * On Failure: it returns a tuple of `(bool, str)`. For example: `(False, "Error message explain the failure")`

### Error Handling Best Practices

1. **Structured Error Responses**:
```

Example 2 (unknown):
```unknown
2. **Error Categories**:
   * Use specific error codes
   * Include relevant context
   * Provide actionable feedback

3. **Validation Chain**:
```

Example 3 (unknown):
```unknown
### Handling Guardrail Results

When a guardrail returns `(False, error)`:

1. The error is sent back to the agent
2. The agent attempts to fix the issue
3. The process repeats until:
   * The guardrail returns `(True, result)`
   * Maximum retries are reached (`guardrail_max_retries`)

Example with retry handling:
```

Example 4 (unknown):
```unknown
## Getting Structured Consistent Outputs from Tasks

<Note>
  It's also important to note that the output of the final task of a crew becomes the final output of the actual crew itself.
</Note>

### Using `output_pydantic`

The `output_pydantic` property allows you to define a Pydantic model that the task output should conform to. This ensures that the output is not only structured but also validated according to the Pydantic model.

Here's an example demonstrating how to use output\_pydantic:
```

---

## MLflow Overview

**URL:** llms-txt#mlflow-overview

**Contents:**
  - Features
- Setup Instructions

[MLflow](https://mlflow.org/) is an open-source platform to assist machine learning practitioners and teams in handling the complexities of the machine learning process.

It provides a tracing feature that enhances LLM observability in your Generative AI applications by capturing detailed information about the execution of your application’s services.
Tracing provides a way to record the inputs, outputs, and metadata associated with each intermediate step of a request, enabling you to easily pinpoint the source of bugs and unexpected behaviors.

<img alt="Overview of MLflow crewAI tracing usage" />

* **Tracing Dashboard**: Monitor activities of your crewAI agents with detailed dashboards that include inputs, outputs and metadata of spans.
* **Automated Tracing**: A fully automated integration with crewAI, which can be enabled by running `mlflow.crewai.autolog()`.
* **Manual Trace Instrumentation with minor efforts**: Customize trace instrumentation through MLflow's high-level fluent APIs such as decorators, function wrappers and context managers.
* **OpenTelemetry Compatibility**: MLflow Tracing supports exporting traces to an OpenTelemetry Collector, which can then be used to export traces to various backends such as Jaeger, Zipkin, and AWS X-Ray.
* **Package and Deploy Agents**: Package and deploy your crewAI agents to an inference server with a variety of deployment targets.
* **Securely Host LLMs**: Host multiple LLM from various providers in one unified endpoint through MFflow gateway.
* **Evaluation**: Evaluate your crewAI agents with a wide range of metrics using a convenient API `mlflow.evaluate()`.

## Setup Instructions

<Steps>
  <Step title="Install MLflow package">
    
  </Step>

<Step title="Start MFflow tracking server">
    
  </Step>

<Step title="Initialize MLflow in Your Application">
    Add the following two lines to your application code:

Example Usage for tracing CrewAI Agents:

Refer to [MLflow Tracing Documentation](https://mlflow.org/docs/latest/llms/tracing/index.html) for more configurations and use cases.
  </Step>

<Step title="Visualize Activities of Agents">
    Now traces for your crewAI agents are captured by MLflow.
    Let's visit MLflow tracking server to view the traces and get insights into your Agents.

Open `127.0.0.1:5000` on your browser to visit MLflow tracking server.

<Frame>
      <img alt="MLflow tracing example with crewai" />
    </Frame>
  </Step>
</Steps>

**Examples:**

Example 1 (unknown):
```unknown
</Step>

  <Step title="Start MFflow tracking server">
```

Example 2 (unknown):
```unknown
</Step>

  <Step title="Initialize MLflow in Your Application">
    Add the following two lines to your application code:
```

Example 3 (unknown):
```unknown
Example Usage for tracing CrewAI Agents:
```

---

## Multiple AMP services

**URL:** llms-txt#multiple-amp-services

**Contents:**
- Complete Example

mcps=[
    "crewai-amp:weather-insights",
    "crewai-amp:market-analysis",
    "crewai-amp:social-media-monitoring"
]
python theme={null}
from crewai import Agent, Task, Crew, Process

**Examples:**

Example 1 (unknown):
```unknown
## Complete Example

Here's a complete example using multiple MCP servers:
```

---

## Multiple hooks execute in registration order

**URL:** llms-txt#multiple-hooks-execute-in-registration-order

**Contents:**
- Best Practices
- Error Handling
- Type Safety

@before_llm_call
def first_hook(context):
    print("1. First hook executed")
    return None

@before_llm_call
def second_hook(context):
    print("2. Second hook executed")
    return None

@before_llm_call
def blocking_hook(context):
    if context.iterations > 10:
        print("3. Blocking hook - execution stopped")
        return False  # Subsequent hooks won't execute
    print("3. Blocking hook - execution allowed")
    return None
python theme={null}
@before_llm_call
def safe_hook(context: LLMCallHookContext) -> bool | None:
    try:
        # Your hook logic
        if some_condition:
            return False
    except Exception as e:
        print(f"⚠️ Hook error: {e}")
        # Decide: allow or block on error
        return None  # Allow execution despite error
python theme={null}
from crewai.hooks import LLMCallHookContext, BeforeLLMCallHookType, AfterLLMCallHookType

**Examples:**

Example 1 (unknown):
```unknown
## Best Practices

1. **Keep Hooks Focused**: Each hook should have a single responsibility
2. **Avoid Heavy Computation**: Hooks execute on every LLM call
3. **Handle Errors Gracefully**: Use try-except to prevent hook failures from breaking execution
4. **Use Type Hints**: Leverage `LLMCallHookContext` for better IDE support
5. **Document Hook Behavior**: Especially for blocking conditions
6. **Test Hooks Independently**: Unit test hooks before using in production
7. **Clear Hooks in Tests**: Use `clear_all_llm_call_hooks()` between test runs
8. **Modify In-Place**: Always modify `context.messages` in-place, never replace

## Error Handling
```

Example 2 (unknown):
```unknown
## Type Safety
```

---

## my_custom_listener.py

**URL:** llms-txt#my_custom_listener.py

from crewai.events import BaseEventListener

---

## Native async execution

**URL:** llms-txt#native-async-execution

**Contents:**
  - Example: Multiple Native Async Crews
  - Example: Native Async for Multiple Inputs
- Thread-Based Async with `kickoff_async()`
  - Method Signature
  - Parameters
  - Returns
  - Example: Thread-Based Async Execution
  - Example: Multiple Thread-Based Async Crews
- Async Streaming
- Potential Use Cases

async def main():
    result = await analysis_crew.akickoff(inputs={"ages": [25, 30, 35, 40, 45]})
    print("Crew Result:", result)

asyncio.run(main())
python Code theme={null}
import asyncio
from crewai import Crew, Agent, Task

coding_agent = Agent(
    role="Python Data Analyst",
    goal="Analyze data and provide insights using Python",
    backstory="You are an experienced data analyst with strong Python skills.",
    allow_code_execution=True
)

task_1 = Task(
    description="Analyze the first dataset and calculate the average age. Ages: {ages}",
    agent=coding_agent,
    expected_output="The average age of the participants."
)

task_2 = Task(
    description="Analyze the second dataset and calculate the average age. Ages: {ages}",
    agent=coding_agent,
    expected_output="The average age of the participants."
)

crew_1 = Crew(agents=[coding_agent], tasks=[task_1])
crew_2 = Crew(agents=[coding_agent], tasks=[task_2])

async def main():
    results = await asyncio.gather(
        crew_1.akickoff(inputs={"ages": [25, 30, 35, 40, 45]}),
        crew_2.akickoff(inputs={"ages": [20, 22, 24, 28, 30]})
    )

for i, result in enumerate(results, 1):
        print(f"Crew {i} Result:", result)

asyncio.run(main())
python Code theme={null}
import asyncio
from crewai import Crew, Agent, Task

coding_agent = Agent(
    role="Python Data Analyst",
    goal="Analyze data and provide insights using Python",
    backstory="You are an experienced data analyst with strong Python skills.",
    allow_code_execution=True
)

data_analysis_task = Task(
    description="Analyze the dataset and calculate the average age. Ages: {ages}",
    agent=coding_agent,
    expected_output="The average age of the participants."
)

analysis_crew = Crew(
    agents=[coding_agent],
    tasks=[data_analysis_task]
)

async def main():
    datasets = [
        {"ages": [25, 30, 35, 40, 45]},
        {"ages": [20, 22, 24, 28, 30]},
        {"ages": [30, 35, 40, 45, 50]}
    ]

results = await analysis_crew.akickoff_for_each(datasets)

for i, result in enumerate(results, 1):
        print(f"Dataset {i} Result:", result)

asyncio.run(main())
python Code theme={null}
async def kickoff_async(self, inputs: dict) -> CrewOutput:
python Code theme={null}
import asyncio
from crewai import Crew, Agent, Task

coding_agent = Agent(
    role="Python Data Analyst",
    goal="Analyze data and provide insights using Python",
    backstory="You are an experienced data analyst with strong Python skills.",
    allow_code_execution=True
)

data_analysis_task = Task(
    description="Analyze the given dataset and calculate the average age of participants. Ages: {ages}",
    agent=coding_agent,
    expected_output="The average age of the participants."
)

analysis_crew = Crew(
    agents=[coding_agent],
    tasks=[data_analysis_task]
)

async def async_crew_execution():
    result = await analysis_crew.kickoff_async(inputs={"ages": [25, 30, 35, 40, 45]})
    print("Crew Result:", result)

asyncio.run(async_crew_execution())
python Code theme={null}
import asyncio
from crewai import Crew, Agent, Task

coding_agent = Agent(
    role="Python Data Analyst",
    goal="Analyze data and provide insights using Python",
    backstory="You are an experienced data analyst with strong Python skills.",
    allow_code_execution=True
)

task_1 = Task(
    description="Analyze the first dataset and calculate the average age of participants. Ages: {ages}",
    agent=coding_agent,
    expected_output="The average age of the participants."
)

task_2 = Task(
    description="Analyze the second dataset and calculate the average age of participants. Ages: {ages}",
    agent=coding_agent,
    expected_output="The average age of the participants."
)

crew_1 = Crew(agents=[coding_agent], tasks=[task_1])
crew_2 = Crew(agents=[coding_agent], tasks=[task_2])

async def async_multiple_crews():
    result_1 = crew_1.kickoff_async(inputs={"ages": [25, 30, 35, 40, 45]})
    result_2 = crew_2.kickoff_async(inputs={"ages": [20, 22, 24, 28, 30]})

results = await asyncio.gather(result_1, result_2)

for i, result in enumerate(results, 1):
        print(f"Crew {i} Result:", result)

asyncio.run(async_multiple_crews())
python Code theme={null}
import asyncio
from crewai import Crew, Agent, Task

agent = Agent(
    role="Researcher",
    goal="Research and summarize topics",
    backstory="You are an expert researcher."
)

task = Task(
    description="Research the topic: {topic}",
    agent=agent,
    expected_output="A comprehensive summary of the topic."
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    stream=True  # Enable streaming
)

async def main():
    streaming_output = await crew.akickoff(inputs={"topic": "AI trends in 2024"})

# Async iteration over streaming chunks
    async for chunk in streaming_output:
        print(f"Chunk: {chunk.content}")

# Access final result after streaming completes
    result = streaming_output.result
    print(f"Final result: {result.raw}")

asyncio.run(main())
```

## Potential Use Cases

* **Parallel Content Generation**: Kickoff multiple independent crews asynchronously, each responsible for generating content on different topics. For example, one crew might research and draft an article on AI trends, while another crew generates social media posts about a new product launch.

* **Concurrent Market Research Tasks**: Launch multiple crews asynchronously to conduct market research in parallel. One crew might analyze industry trends, while another examines competitor strategies, and yet another evaluates consumer sentiment.

* **Independent Travel Planning Modules**: Execute separate crews to independently plan different aspects of a trip. One crew might handle flight options, another handles accommodation, and a third plans activities.

## Choosing Between `akickoff()` and `kickoff_async()`

| Feature             | `akickoff()`                          | `kickoff_async()`        |
| ------------------- | ------------------------------------- | ------------------------ |
| Execution model     | Native async/await                    | Thread-based wrapper     |
| Task execution      | Async with `aexecute_sync()`          | Sync in thread pool      |
| Memory operations   | Async                                 | Sync in thread pool      |
| Knowledge retrieval | Async                                 | Sync in thread pool      |
| Best for            | High-concurrency, I/O-bound workloads | Simple async integration |
| Streaming support   | Yes                                   | Yes                      |

**Examples:**

Example 1 (unknown):
```unknown
### Example: Multiple Native Async Crews

Run multiple crews concurrently using `asyncio.gather()` with native async:
```

Example 2 (unknown):
```unknown
### Example: Native Async for Multiple Inputs

Use `akickoff_for_each()` to execute your crew against multiple inputs concurrently with native async:
```

Example 3 (unknown):
```unknown
## Thread-Based Async with `kickoff_async()`

The `kickoff_async()` method provides async execution by wrapping the synchronous `kickoff()` in a thread. This is useful for simpler async integration or backward compatibility.

### Method Signature
```

Example 4 (unknown):
```unknown
### Parameters

* `inputs` (dict): A dictionary containing the input data required for the tasks.

### Returns

* `CrewOutput`: An object representing the result of the crew execution.

### Example: Thread-Based Async Execution
```

---

## Neatlogs Integration

**URL:** llms-txt#neatlogs-integration

Source: https://docs.crewai.com/en/observability/neatlogs

Understand, debug, and share your CrewAI agent runs

---

## Now all knowledge will be stored in your project directory

**URL:** llms-txt#now-all-knowledge-will-be-stored-in-your-project-directory

**Contents:**
  - Default Embedding Provider Behavior

python theme={null}
from crewai import Agent, Crew, LLM
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

**Examples:**

Example 1 (unknown):
```unknown
### Default Embedding Provider Behavior

<Info>
  **Default Embedding Provider**: CrewAI defaults to OpenAI embeddings (`text-embedding-3-small`) for knowledge storage, even when using different LLM providers. You can easily customize this to match your setup.
</Info>

#### Understanding Default Behavior
```

---

## Now all storage will be in your project directory

**URL:** llms-txt#now-all-storage-will-be-in-your-project-directory

**Contents:**
  - Embedding Provider Defaults

**Examples:**

Example 1 (unknown):
```unknown
### Embedding Provider Defaults

<Info>
  **Default Embedding Provider**: CrewAI defaults to OpenAI embeddings for consistency and reliability. You can easily customize this to match your LLM provider or use local embeddings.
</Info>

#### Understanding Default Behavior
```

---

## ollama pull mxbai-embed-large

**URL:** llms-txt#ollama-pull-mxbai-embed-large

crew = Crew(
    memory=True,
    embedder={
        "provider": "ollama",
        "config": {
            "model": "mxbai-embed-large",  # or "nomic-embed-text"
            "url": "http://localhost:11434/api/embeddings"  # Default Ollama URL
        }
    }
)

---

## Opik Integration

**URL:** llms-txt#opik-integration

Source: https://docs.crewai.com/en/observability/opik

Learn how to use Comet Opik to debug, evaluate, and monitor your CrewAI applications with comprehensive tracing, automated evaluations, and production-ready dashboards.

---

## Opik Overview

**URL:** llms-txt#opik-overview

**Contents:**
- Setup
- Resources

With [Comet Opik](https://www.comet.com/docs/opik/), debug, evaluate, and monitor your LLM applications, RAG systems, and agentic workflows with comprehensive tracing, automated evaluations, and production-ready dashboards.

<Frame>
  <img alt="Opik agent monitoring example with CrewAI" />
</Frame>

Opik provides comprehensive support for every stage of your CrewAI application development:

* **Log Traces and Spans**: Automatically track LLM calls and application logic to debug and analyze development and production systems. Manually or programmatically annotate, view, and compare responses across projects.
* **Evaluate Your LLM Application's Performance**: Evaluate against a custom test set and run built-in evaluation metrics or define your own metrics in the SDK or UI.
* **Test Within Your CI/CD Pipeline**: Establish reliable performance baselines with Opik's LLM unit tests, built on PyTest. Run online evaluations for continuous monitoring in production.
* **Monitor & Analyze Production Data**: Understand your models' performance on unseen data in production and generate datasets for new dev iterations.

Comet provides a hosted version of the Opik platform, or you can run the platform locally.

To use the hosted version, simply [create a free Comet account](https://www.comet.com/signup?utm_medium=github\&utm_source=crewai_docs) and grab you API Key.

To run the Opik platform locally, see our [installation guide](https://www.comet.com/docs/opik/self-host/overview/) for more information.

For this guide we will use CrewAI’s quickstart example.

<Steps>
  <Step title="Install required packages">
    
  </Step>

<Step title="Configure Opik">
    
  </Step>

<Step title="Prepare environment">
    First, we set up our API keys for our LLM-provider as environment variables:

<Step title="Using CrewAI">
    The first step is to create our project. We will use an example from CrewAI’s documentation:

Now we can import Opik’s tracker and run our crew:

After running your CrewAI application, visit the Opik app to view:

* LLM traces, spans, and their metadata
    * Agent interactions and task execution flow
    * Performance metrics like latency and token usage
    * Evaluation metrics (built-in or custom)
  </Step>
</Steps>

* [🦉 Opik Documentation](https://www.comet.com/docs/opik/)
* [👉 Opik + CrewAI Colab](https://colab.research.google.com/github/comet-ml/opik/blob/main/apps/opik-documentation/documentation/docs/cookbook/crewai.ipynb)
* [🐦 X](https://x.com/cometml)
* [💬 Slack](https://slack.comet.com/)

**Examples:**

Example 1 (unknown):
```unknown
</Step>

  <Step title="Configure Opik">
```

Example 2 (unknown):
```unknown
</Step>

  <Step title="Prepare environment">
    First, we set up our API keys for our LLM-provider as environment variables:
```

Example 3 (unknown):
```unknown
</Step>

  <Step title="Using CrewAI">
    The first step is to create our project. We will use an example from CrewAI’s documentation:
```

Example 4 (unknown):
```unknown
Now we can import Opik’s tracker and run our crew:
```

---

## Optionally export them if you need to access them elsewhere

**URL:** llms-txt#optionally-export-them-if-you-need-to-access-them-elsewhere

__all__ = ['my_custom_listener', 'another_listener']
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
4. Import your listeners package in your Crew or Flow file:
```

---

## Option 1: Accessing Properties Using Dictionary-Style Indexing

**URL:** llms-txt#option-1:-accessing-properties-using-dictionary-style-indexing

print("Accessing Properties - Option 1")
title = result["title"]
content = result["content"]
print("Title:", title)
print("Content:", content)

---

## Option 2: Accessing Properties Directly from the Pydantic Model

**URL:** llms-txt#option-2:-accessing-properties-directly-from-the-pydantic-model

print("Accessing Properties - Option 2")
title = result.pydantic.title
content = result.pydantic.content
print("Title:", title)
print("Content:", content)

---

## Option 3: Accessing Properties Using the to_dict() Method

**URL:** llms-txt#option-3:-accessing-properties-using-the-to_dict()-method

print("Accessing Properties - Option 3")
output_dict = result.to_dict()
title = output_dict["title"]
content = output_dict["content"]
print("Title:", title)
print("Content:", content)

---

## Option 4: Printing the Entire Blog Object

**URL:** llms-txt#option-4:-printing-the-entire-blog-object

**Contents:**
  - Using `output_json`

print("Accessing Properties - Option 5")
print("Blog:", result)

python Code theme={null}
import json

from crewai import Agent, Crew, Process, Task
from pydantic import BaseModel

**Examples:**

Example 1 (unknown):
```unknown
In this example:

* A Pydantic model Blog is defined with title and content fields.
* The task task1 uses the output\_pydantic property to specify that its output should conform to the Blog model.
* After executing the crew, you can access the structured output in multiple ways as shown.

#### Explanation of Accessing the Output

1. Dictionary-Style Indexing: You can directly access the fields using result\["field\_name"]. This works because the CrewOutput class implements the **getitem** method.
2. Directly from Pydantic Model: Access the attributes directly from the result.pydantic object.
3. Using to\_dict() Method: Convert the output to a dictionary and access the fields.
4. Printing the Entire Object: Simply print the result object to see the structured output.

### Using `output_json`

The `output_json` property allows you to define the expected output in JSON format. This ensures that the task's output is a valid JSON structure that can be easily parsed and used in your application.

Here's an example demonstrating how to use `output_json`:
```

---

## OR

**URL:** llms-txt#or

---

## Or use knowledge sources instead of large prompts

**URL:** llms-txt#or-use-knowledge-sources-instead-of-large-prompts

python Code theme={null}

**Examples:**

Example 1 (unknown):
```unknown
**If automatic summarization loses important information:**
```

---

## os.environ["LANGFUSE_HOST"] = "https://us.cloud.langfuse.com" # 🇺🇸 US region

**URL:** llms-txt#os.environ["langfuse_host"]-=-"https://us.cloud.langfuse.com"-#-🇺🇸-us-region

---

## os.environ["TAVILY_API_KEY"] = "YOUR_API_KEY"

**URL:** llms-txt#os.environ["tavily_api_key"]-=-"your_api_key"

---

## os.environ["TAVILY_API_KEY"] = "YOUR_TAVILY_API_KEY"

**URL:** llms-txt#os.environ["tavily_api_key"]-=-"your_tavily_api_key"

---

## Output:

**URL:** llms-txt#output:

---

## Outside the context, the temporary handler is removed

**URL:** llms-txt#outside-the-context,-the-temporary-handler-is-removed

**Contents:**
- Use Cases
- Best Practices

Event listeners can be used for a variety of purposes:

1. **Logging and Monitoring**: Track the execution of your Crew and log important events
2. **Analytics**: Collect data about your Crew's performance and behavior
3. **Debugging**: Set up temporary listeners to debug specific issues
4. **Integration**: Connect CrewAI with external systems like monitoring platforms, databases, or notification services
5. **Custom Behavior**: Trigger custom actions based on specific events

1. **Keep Handlers Light**: Event handlers should be lightweight and avoid blocking operations
2. **Error Handling**: Include proper error handling in your event handlers to prevent exceptions from affecting the main execution
3. **Cleanup**: If your listener allocates resources, ensure they're properly cleaned up
4. **Selective Listening**: Only listen for events you actually need to handle
5. **Testing**: Test your event listeners in isolation to ensure they behave as expected

By leveraging CrewAI's event system, you can extend its functionality and integrate it seamlessly with your existing infrastructure.

---

## Perform an action (default behavior)

**URL:** llms-txt#perform-an-action-(default-behavior)

result = stagehand_tool.run(
    instruction="Click the login button", 
    url="https://example.com",
    command_type="act"  # Default, so can be omitted
)

---

## Perform a search with custom parameters

**URL:** llms-txt#perform-a-search-with-custom-parameters

**Contents:**
- Return Format
- Error Handling
- Conclusion

results = linkup_tool.run(
    query="Women Nobel Prize Physics",
    depth="deep",
    output_type="searchResults"
)
json theme={null}
{
  "success": true,
  "results": [
    {
      "name": "Result Title",
      "url": "https://example.com/result",
      "content": "Content of the result..."
    },
    // Additional results...
  ]
}
json theme={null}
{
  "success": false,
  "error": "Error message"
}
```

The tool gracefully handles API errors and provides structured feedback. If the API request fails, the tool will return a dictionary with `success: false` and an error message.

The `LinkupSearchTool` provides a seamless way to integrate Linkup's contextual information retrieval capabilities into your CrewAI agents. By leveraging this tool, agents can access relevant and up-to-date information to enhance their decision-making and task execution.

**Examples:**

Example 1 (unknown):
```unknown
## Return Format

The tool returns results in the following format:
```

Example 2 (unknown):
```unknown
If an error occurs, the response will be:
```

---

## POST /kickoff

**URL:** llms-txt#post-/kickoff

Source: https://docs.crewai.com/en/api-reference/kickoff

enterprise-api.en.yaml post /kickoff
Start a crew execution

---

## POST /resume

**URL:** llms-txt#post-/resume

Source: https://docs.crewai.com/en/api-reference/resume

enterprise-api.en.yaml post /resume
Resume crew execution with human feedback

---

## Print the complete system prompt that will be sent to the LLM

**URL:** llms-txt#print-the-complete-system-prompt-that-will-be-sent-to-the-llm

if "system" in generated_prompt:
    print("=== SYSTEM PROMPT ===")
    print(generated_prompt["system"])
    print("\n=== USER PROMPT ===")
    print(generated_prompt["user"])
else:
    print("=== COMPLETE PROMPT ===")
    print(generated_prompt["prompt"])

---

## Print the UUID strings

**URL:** llms-txt#print-the-uuid-strings

**Contents:**
  - Working with Fingerprint Metadata

print(f"Agent fingerprint: {agent_fingerprint.uuid_str}")
print(f"Crew fingerprint: {crew_fingerprint.uuid_str}")
print(f"Task fingerprint: {task_fingerprint.uuid_str}")
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### Working with Fingerprint Metadata

You can add metadata to fingerprints for additional context:
```

---

## "proxy_pool": "public_residential_pool",  # Select a proxy pool

**URL:** llms-txt#"proxy_pool":-"public_residential_pool",--#-select-a-proxy-pool

---

## Push updates after code changes

**URL:** llms-txt#push-updates-after-code-changes

---

## Qdrant

**URL:** llms-txt#qdrant

from crewai.rag.qdrant.config import QdrantConfig
set_rag_config(QdrantConfig())
qdrant_client = get_rag_client()

---

## query="SELECT product_name, SUM(revenue) as total_revenue FROM sales GROUP BY product_name ORDER BY total_revenue DESC LIMIT 5"

**URL:** llms-txt#query="select-product_name,-sum(revenue)-as-total_revenue-from-sales-group-by-product_name-order-by-total_revenue-desc-limit-5"

---

## Quick fix: Enable automatic handling

**URL:** llms-txt#quick-fix:-enable-automatic-handling

agent.respect_context_window = True

---

## Register a custom evaluator

**URL:** llms-txt#register-a-custom-evaluator

@client.register_local_evaluator("random_evaluator")
def random_evaluator(**kwargs):
    score = random.random()
    return EvaluationResult(
        score_raw=score,
        pass_=score >= 0.5,
        explanation="example explanation",
    )

---

## Register

**URL:** llms-txt#register

register_before_llm_call_hook(my_hook)

---

## Register order matters!

**URL:** llms-txt#register-order-matters!

register_before_tool_call_hook(hook1)  # Executes first
register_before_tool_call_hook(hook2)  # Executes second
register_before_tool_call_hook(hook3)  # Executes third

---

## Register programmatically

**URL:** llms-txt#register-programmatically

register_before_llm_call_hook(my_hook)

---

## "render_js": True,  # Enable JavaScript rendering with a cloud headless browser

**URL:** llms-txt#"render_js":-true,--#-enable-javascript-rendering-with-a-cloud-headless-browser

---

## Reset knowledge storage to clear old embeddings

**URL:** llms-txt#reset-knowledge-storage-to-clear-old-embeddings

crew.reset_memories(command_type='knowledge')

---

## Reset specific memory types

**URL:** llms-txt#reset-specific-memory-types

**Contents:**
  - Production Best Practices
  - Common Storage Issues

crew.reset_memories(command_type='short')     # Short-term memory
crew.reset_memories(command_type='long')      # Long-term memory
crew.reset_memories(command_type='entity')    # Entity memory
crew.reset_memories(command_type='knowledge') # Knowledge storage
bash theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### Production Best Practices

1. **Set `CREWAI_STORAGE_DIR`** to a known location in production for better control
2. **Choose explicit embedding providers** to match your LLM setup
3. **Monitor storage directory size** for large-scale deployments
4. **Include storage directories** in your backup strategy
5. **Set appropriate file permissions** (0o755 for directories, 0o644 for files)
6. **Use project-relative paths** for containerized deployments

### Common Storage Issues

**"ChromaDB permission denied" errors:**
```

---

## Restricting search to a specific JSON file

**URL:** llms-txt#restricting-search-to-a-specific-json-file

---

## Result:

**URL:** llms-txt#result:

---

## Resuming when Slack webhook fires (sync handler)

**URL:** llms-txt#resuming-when-slack-webhook-fires-(sync-handler)

def on_slack_feedback(flow_id: str, slack_message: str):
    flow = ContentPipeline.from_pending(flow_id)
    result = flow.resume(slack_message)
    return result

---

## Run the flow

**URL:** llms-txt#run-the-flow

**Contents:**
  - Benefits of Structured State
  - When to Use Structured State
- The Automatic State ID
  - How It Works
- Dynamic State Updates
  - Passing Data Between Steps
- Persisting Flow State
  - The @persist() Decorator

flow = StructuredStateFlow()
result = flow.kickoff()
print(f"Final result: {result}")
print(f"Final state: {flow.state}")
python theme={null}
from crewai.flow.flow import Flow, listen, start

class DataPassingFlow(Flow):
    @start()
    def generate_data(self):
        # This return value will be passed to listening methods
        return "Generated data"

@listen(generate_data)
    def process_data(self, data_from_previous_step):
        print(f"Received: {data_from_previous_step}")
        # You can modify the data and pass it along
        processed_data = f"{data_from_previous_step} - processed"
        # Also update state
        self.state["last_processed"] = processed_data
        return processed_data

@listen(process_data)
    def finalize_data(self, processed_data):
        print(f"Received processed data: {processed_data}")
        # Access both the passed data and state
        last_processed = self.state.get("last_processed", "")
        return f"Final: {processed_data} (from state: {last_processed})"
python theme={null}
from crewai.flow.flow import Flow, listen, start
from crewai.flow.persistence import persist
from pydantic import BaseModel

class CounterState(BaseModel):
    value: int = 0

@persist()  # Apply to the entire flow class
class PersistentCounterFlow(Flow[CounterState]):
    @start()
    def increment(self):
        self.state.value += 1
        print(f"Incremented to {self.state.value}")
        return self.state.value

@listen(increment)
    def double(self, value):
        self.state.value = value * 2
        print(f"Doubled to {self.state.value}")
        return self.state.value

**Examples:**

Example 1 (unknown):
```unknown
### Benefits of Structured State

Using structured state provides several advantages:

1. **Type Safety** - Catch type errors at development time
2. **Self-Documentation** - The state model clearly documents what data is available
3. **Validation** - Automatic validation of data types and constraints
4. **IDE Support** - Get autocomplete and inline documentation
5. **Default Values** - Easily define fallbacks for missing data

### When to Use Structured State

Structured state is recommended for:

* Complex flows with well-defined data schemas
* Team projects where multiple developers work on the same code
* Applications where data validation is important
* Flows that need to enforce specific data types and constraints

## The Automatic State ID

Both unstructured and structured states automatically receive a unique identifier (UUID) to help track and manage state instances.

### How It Works

* For unstructured state, the ID is accessible as `self.state["id"]`
* For structured state, the ID is accessible as `self.state.id`
* This ID is generated automatically when the flow is created
* The ID remains the same throughout the flow's lifecycle
* The ID can be used for tracking, logging, and retrieving persisted states

This UUID is particularly valuable when implementing persistence or tracking multiple flow executions.

## Dynamic State Updates

Regardless of whether you're using structured or unstructured state, you can update state dynamically throughout your flow's execution.

### Passing Data Between Steps

Flow methods can return values that are then passed as arguments to listening methods:
```

Example 2 (unknown):
```unknown
This pattern allows you to combine direct data passing with state updates for maximum flexibility.

## Persisting Flow State

One of CrewAI's most powerful features is the ability to persist flow state across executions. This enables workflows that can be paused, resumed, and even recovered after failures.

### The @persist() Decorator

The `@persist()` decorator automates state persistence, saving your flow's state at key points in execution.

#### Class-Level Persistence

When applied at the class level, `@persist()` saves state after every method execution:
```

---

## scrape_config={

**URL:** llms-txt#scrape_config={

---

## scrape_format="markdown"

**URL:** llms-txt#scrape_format="markdown"

---

## Search results: Title: Jeux Olympiques de Paris 2024 - Actualités, calendriers, résultats

**URL:** llms-txt#search-results:-title:-jeux-olympiques-de-paris-2024---actualités,-calendriers,-résultats

---

## Search results: Title: Role of chat gpt in public health

**URL:** llms-txt#search-results:-title:-role-of-chat-gpt-in-public-health

---

## Second run - state is automatically loaded

**URL:** llms-txt#second-run---state-is-automatically-loaded

**Contents:**
- Advanced State Patterns
  - Conditional starts and resumable execution
  - State-Based Conditional Logic
  - Handling Complex State Transformations
- State Management with Crews
  - Passing State to Crews
  - Handling Crew Outputs in State
- Best Practices for State Management
  - 1. Keep State Focused

flow2 = PersistentCounterFlow()
result2 = flow2.kickoff()
print(f"Second run result: {result2}")  # Will be higher due to persisted state
python theme={null}
from crewai.flow.flow import Flow, listen, start
from crewai.flow.persistence import persist

class SelectivePersistFlow(Flow):
    @start()
    def first_step(self):
        self.state["count"] = 1
        return "First step"

@persist()  # Only persist after this method
    @listen(first_step)
    def important_step(self, prev_result):
        self.state["count"] += 1
        self.state["important_data"] = "This will be persisted"
        return "Important step completed"

@listen(important_step)
    def final_step(self, prev_result):
        self.state["count"] += 1
        return f"Complete with count {self.state['count']}"
python theme={null}
from crewai.flow.flow import Flow, start, listen, and_, or_

class ResumableFlow(Flow):
    @start()  # unconditional start
    def init(self):
        ...

# Conditional start: run after "init" or external trigger name
    @start("init")
    def maybe_begin(self):
        ...

@listen(and_(init, maybe_begin))
    def proceed(self):
        ...
python theme={null}
from crewai.flow.flow import Flow, listen, router, start
from pydantic import BaseModel

class PaymentState(BaseModel):
    amount: float = 0.0
    is_approved: bool = False
    retry_count: int = 0

class PaymentFlow(Flow[PaymentState]):
    @start()
    def process_payment(self):
        # Simulate payment processing
        self.state.amount = 100.0
        self.state.is_approved = self.state.amount < 1000
        return "Payment processed"

@router(process_payment)
    def check_approval(self, previous_result):
        if self.state.is_approved:
            return "approved"
        elif self.state.retry_count < 3:
            return "retry"
        else:
            return "rejected"

@listen("approved")
    def handle_approval(self):
        return f"Payment of ${self.state.amount} approved!"

@listen("retry")
    def handle_retry(self):
        self.state.retry_count += 1
        print(f"Retrying payment (attempt {self.state.retry_count})...")
        # Could implement retry logic here
        return "Retry initiated"

@listen("rejected")
    def handle_rejection(self):
        return f"Payment of ${self.state.amount} rejected after {self.state.retry_count} retries."
python theme={null}
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel
from typing import List, Dict

class UserData(BaseModel):
    name: str
    active: bool = True
    login_count: int = 0

class ComplexState(BaseModel):
    users: Dict[str, UserData] = {}
    active_user_count: int = 0

class TransformationFlow(Flow[ComplexState]):
    @start()
    def initialize(self):
        # Add some users
        self.add_user("alice", "Alice")
        self.add_user("bob", "Bob")
        self.add_user("charlie", "Charlie")
        return "Initialized"

@listen(initialize)
    def process_users(self, _):
        # Increment login counts
        for user_id in self.state.users:
            self.increment_login(user_id)

# Deactivate one user
        self.deactivate_user("bob")

# Update active count
        self.update_active_count()

return f"Processed {len(self.state.users)} users"

# Helper methods for state transformations
    def add_user(self, user_id: str, name: str):
        self.state.users[user_id] = UserData(name=name)
        self.update_active_count()

def increment_login(self, user_id: str):
        if user_id in self.state.users:
            self.state.users[user_id].login_count += 1

def deactivate_user(self, user_id: str):
        if user_id in self.state.users:
            self.state.users[user_id].active = False
            self.update_active_count()

def update_active_count(self):
        self.state.active_user_count = sum(
            1 for user in self.state.users.values() if user.active
        )
python theme={null}
from crewai.flow.flow import Flow, listen, start
from crewai import Agent, Crew, Process, Task
from pydantic import BaseModel

class ResearchState(BaseModel):
    topic: str = ""
    depth: str = "medium"
    results: str = ""

class ResearchFlow(Flow[ResearchState]):
    @start()
    def get_parameters(self):
        # In a real app, this might come from user input
        self.state.topic = "Artificial Intelligence Ethics"
        self.state.depth = "deep"
        return "Parameters set"

@listen(get_parameters)
    def execute_research(self, _):
        # Create agents
        researcher = Agent(
            role="Research Specialist",
            goal=f"Research {self.state.topic} in {self.state.depth} detail",
            backstory="You are an expert researcher with a talent for finding accurate information."
        )

writer = Agent(
            role="Content Writer",
            goal="Transform research into clear, engaging content",
            backstory="You excel at communicating complex ideas clearly and concisely."
        )

# Create tasks
        research_task = Task(
            description=f"Research {self.state.topic} with {self.state.depth} analysis",
            expected_output="Comprehensive research notes in markdown format",
            agent=researcher
        )

writing_task = Task(
            description=f"Create a summary on {self.state.topic} based on the research",
            expected_output="Well-written article in markdown format",
            agent=writer,
            context=[research_task]
        )

# Create and run crew
        research_crew = Crew(
            agents=[researcher, writer],
            tasks=[research_task, writing_task],
            process=Process.sequential,
            verbose=True
        )

# Run crew and store result in state
        result = research_crew.kickoff()
        self.state.results = result.raw

return "Research completed"

@listen(execute_research)
    def summarize_results(self, _):
        # Access the stored results
        result_length = len(self.state.results)
        return f"Research on {self.state.topic} completed with {result_length} characters of results."
python theme={null}
@listen(execute_crew)
def process_crew_results(self, _):
    # Parse the raw results (assuming JSON output)
    import json
    try:
        results_dict = json.loads(self.state.raw_results)
        self.state.processed_results = {
            "title": results_dict.get("title", ""),
            "main_points": results_dict.get("main_points", []),
            "conclusion": results_dict.get("conclusion", "")
        }
        return "Results processed successfully"
    except json.JSONDecodeError:
        self.state.error = "Failed to parse crew results as JSON"
        return "Error processing results"
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
#### Method-Level Persistence

For more granular control, you can apply `@persist()` to specific methods:
```

Example 2 (unknown):
```unknown
## Advanced State Patterns

### Conditional starts and resumable execution

Flows support conditional `@start()` and resumable execution for HITL/cyclic scenarios:
```

Example 3 (unknown):
```unknown
* Conditional `@start()` accepts a method name, a router label, or a callable condition.
* During resume, listeners continue from prior checkpoints; cycle/router branches honor resumption flags.

### State-Based Conditional Logic

You can use state to implement complex conditional logic in your flows:
```

Example 4 (unknown):
```unknown
### Handling Complex State Transformations

For complex state transformations, you can create dedicated methods:
```

---

## SERPER_API_KEY=<your api key>

**URL:** llms-txt#serper_api_key=<your-api-key>

search = GoogleSerperAPIWrapper()

class SearchTool(BaseTool):
    name: str = "Search"
    description: str = "Useful for search-based queries. Use this to find current information about markets, companies, and trends."
    search: GoogleSerperAPIWrapper = Field(default_factory=GoogleSerperAPIWrapper)

def _run(self, query: str) -> str:
        """Execute the search query and return results"""
        try:
            return self.search.run(query)
        except Exception as e:
            return f"Error performing search: {str(e)}"

---

## Server may be slow or overloaded

**URL:** llms-txt#server-may-be-slow-or-overloaded

---

## Server with authentication

**URL:** llms-txt#server-with-authentication

"https://mcp.exa.ai/mcp?api_key=your_key&profile=your_profile"

---

## Server with custom path

**URL:** llms-txt#server-with-custom-path

**Contents:**
  - Specific Tool Selection

"https://services.company.com/api/v1/mcp"
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### Specific Tool Selection

Use the `#` syntax to select specific tools from a server:
```

---

## Set custom storage location

**URL:** llms-txt#set-custom-storage-location

os.environ["CREWAI_STORAGE_DIR"] = "./my_project_storage"

---

## Set environment variables

**URL:** llms-txt#set-environment-variables

**Contents:**
  - Step 3: Initialize OpenTelemetry with Braintrust
  - Step 4: Create a CrewAI Application

os.environ["BRAINTRUST_API_KEY"] = BRAINTRUST_API_KEY
os.environ["BRAINTRUST_PARENT"] = "project_name:crewai-demo"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
python theme={null}
import os
from typing import Any, Dict

from braintrust.otel import BraintrustSpanProcessor
from crewai import Agent, Crew, Task
from crewai.llm import LLM
from opentelemetry import trace
from opentelemetry.instrumentation.crewai import CrewAIInstrumentor
from opentelemetry.instrumentation.openai import OpenAIInstrumentor
from opentelemetry.sdk.trace import TracerProvider

def setup_tracing() -> None:
    """Setup OpenTelemetry tracing with Braintrust."""
    current_provider = trace.get_tracer_provider()
    if isinstance(current_provider, TracerProvider):
        provider = current_provider
    else:
        provider = TracerProvider()
        trace.set_tracer_provider(provider)

provider.add_span_processor(BraintrustSpanProcessor())
    CrewAIInstrumentor().instrument(tracer_provider=provider)
    OpenAIInstrumentor().instrument(tracer_provider=provider)

setup_tracing()
python theme={null}
from crewai import Agent, Crew, Process, Task
from crewai_tools import SerperDevTool

def create_crew() -> Crew:
    """Create a crew with multiple agents for comprehensive tracing."""
    llm = LLM(model="gpt-4o-mini")
    search_tool = SerperDevTool()

# Define agents with specific roles
    researcher = Agent(
        role="Senior Research Analyst",
        goal="Uncover cutting-edge developments in AI and data science",
        backstory="""You work at a leading tech think tank.
        Your expertise lies in identifying emerging trends.
        You have a knack for dissecting complex data and presenting actionable insights.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[search_tool],
    )

writer = Agent(
        role="Tech Content Strategist",
        goal="Craft compelling content on tech advancements",
        backstory="""You are a renowned Content Strategist, known for your insightful and engaging articles.
        You transform complex concepts into compelling narratives.""",
        verbose=True,
        allow_delegation=True,
        llm=llm,
    )

# Create tasks for your agents
    research_task = Task(
        description="""Conduct a comprehensive analysis of the latest advancements in {topic}.
        Identify key trends, breakthrough technologies, and potential industry impacts.""",
        expected_output="Full analysis report in bullet points",
        agent=researcher,
    )

writing_task = Task(
        description="""Using the insights provided, develop an engaging blog
        post that highlights the most significant {topic} advancements.
        Your post should be informative yet accessible, catering to a tech-savvy audience.
        Make it sound cool, avoid complex words so it doesn't sound like AI.""",
        expected_output="Full blog post of at least 4 paragraphs",
        agent=writer,
        context=[research_task],
    )

# Instantiate your crew with a sequential process
    crew = Crew(
        agents=[researcher, writer], 
        tasks=[research_task, writing_task], 
        verbose=True, 
        process=Process.sequential
    )

def run_crew():
    """Run the crew and return results."""
    crew = create_crew()
    result = crew.kickoff(inputs={"topic": "AI developments"})
    return result

**Examples:**

Example 1 (unknown):
```unknown
### Step 3: Initialize OpenTelemetry with Braintrust

Initialize the Braintrust OpenTelemetry instrumentation to start capturing traces and send them to Braintrust.
```

Example 2 (unknown):
```unknown
### Step 4: Create a CrewAI Application

We'll create a CrewAI application where two agents collaborate to research and write a blog post about AI advancements, with comprehensive tracing enabled.
```

---

## Set up API keys

**URL:** llms-txt#set-up-api-keys

os.environ["SERPER_API_KEY"] = "Your Key" # serper.dev API key
os.environ["OPENAI_API_KEY"] = "Your Key"

---

## Set up LLMs with different providers

**URL:** llms-txt#set-up-llms-with-different-providers

openai_llm = LLM(
    model="gpt-4o",
    base_url=PORTKEY_GATEWAY_URL,
    api_key="dummy",
    extra_headers=createHeaders(
        api_key="YOUR_PORTKEY_API_KEY",
        virtual_key="YOUR_OPENAI_VIRTUAL_KEY"
    )
)

anthropic_llm = LLM(
    model="claude-3-5-sonnet-latest",
    max_tokens=1000,
    base_url=PORTKEY_GATEWAY_URL,
    api_key="dummy",
    extra_headers=createHeaders(
        api_key="YOUR_PORTKEY_API_KEY",
        virtual_key="YOUR_ANTHROPIC_VIRTUAL_KEY"
    )
)

---

## Set up logging to capture any reasoning errors

**URL:** llms-txt#set-up-logging-to-capture-any-reasoning-errors

logging.basicConfig(level=logging.INFO)

---

## Set up your SERPER_API_KEY key in an .env file, eg:

**URL:** llms-txt#set-up-your-serper_api_key-key-in-an-.env-file,-eg:

---

## Simple flow can use unstructured state

**URL:** llms-txt#simple-flow-can-use-unstructured-state

class SimpleGreetingFlow(Flow):
    @start()
    def greet(self):
        self.state["name"] = "World"
        return f"Hello, {self.state['name']}!"

---

## Simulate an Outlook trigger with realistic payload

**URL:** llms-txt#simulate-an-outlook-trigger-with-realistic-payload

**Contents:**
- Troubleshooting

crewai triggers run microsoft_outlook/email_received
```

The `crewai triggers run` command will execute your crew with a complete Outlook payload, allowing you to test your parsing logic before deployment.

<Warning>
  Use `crewai triggers run microsoft_outlook/email_received` (not `crewai run`) to simulate trigger execution during development. After deployment, your crew will automatically receive the trigger payload.
</Warning>

* Verify the Outlook connector is still authorized; the subscription must be renewed periodically
* Test locally with `crewai triggers run microsoft_outlook/email_received` to see the exact payload structure
* If attachments are missing, confirm the webhook subscription includes the `includeResourceData` flag
* Review execution logs when events fail to match—cancellation payloads lack attendee lists by design and the crew should account for that
* Remember: use `crewai triggers run` (not `crewai run`) to simulate trigger execution

---

## Simulate a Gmail trigger with realistic payload

**URL:** llms-txt#simulate-a-gmail-trigger-with-realistic-payload

**Contents:**
- Monitoring Executions
- Troubleshooting

crewai triggers run gmail/new_email_received
```

The `crewai triggers run` command will execute your crew with a complete Gmail payload, allowing you to test your parsing logic before deployment.

<Warning>
  Use `crewai triggers run gmail/new_email_received` (not `crewai run`) to simulate trigger execution during development. After deployment, your crew will automatically receive the trigger payload.
</Warning>

## Monitoring Executions

Track history and performance of triggered runs:

<Frame>
  <img alt="List of executions triggered by automation" />
</Frame>

* Ensure Gmail is connected in Tools & Integrations
* Verify the Gmail Trigger is enabled on the Triggers tab
* Test locally with `crewai triggers run gmail/new_email_received` to see the exact payload structure
* Check the execution logs and confirm the payload is passed as `crewai_trigger_payload`
* Remember: use `crewai triggers run` (not `crewai run`) to simulate trigger execution

---

## Simulate a Google Calendar trigger with realistic payload

**URL:** llms-txt#simulate-a-google-calendar-trigger-with-realistic-payload

**Contents:**
- Monitoring Executions
- Troubleshooting

crewai triggers run google_calendar/event_changed
```

The `crewai triggers run` command will execute your crew with a complete Calendar payload, allowing you to test your parsing logic before deployment.

<Warning>
  Use `crewai triggers run google_calendar/event_changed` (not `crewai run`) to simulate trigger execution during development. After deployment, your crew will automatically receive the trigger payload.
</Warning>

## Monitoring Executions

The **Executions** list in the deployment dashboard tracks every triggered run and surfaces payload metadata, output summaries, and errors.

<Frame>
  <img alt="List of executions triggered by automation" />
</Frame>

* Ensure the correct Google account is connected and the trigger is enabled
* Test locally with `crewai triggers run google_calendar/event_changed` to see the exact payload structure
* Confirm your workflow handles all-day events (payloads use `start.date` and `end.date` instead of timestamps)
* Check execution logs if reminders or attendee arrays are missing—calendar permissions can limit fields in the payload
* Remember: use `crewai triggers run` (not `crewai run`) to simulate trigger execution

---

## Simulate a Google Drive trigger with realistic payload

**URL:** llms-txt#simulate-a-google-drive-trigger-with-realistic-payload

**Contents:**
- Monitoring Executions
- Troubleshooting

crewai triggers run google_drive/file_changed
```

The `crewai triggers run` command will execute your crew with a complete Drive payload, allowing you to test your parsing logic before deployment.

<Warning>
  Use `crewai triggers run google_drive/file_changed` (not `crewai run`) to simulate trigger execution during development. After deployment, your crew will automatically receive the trigger payload.
</Warning>

## Monitoring Executions

Track history and performance of triggered runs with the **Executions** list in the deployment dashboard.

<Frame>
  <img alt="List of executions triggered by automation" />
</Frame>

* Verify Google Drive is connected and the trigger toggle is enabled
* Test locally with `crewai triggers run google_drive/file_changed` to see the exact payload structure
* If a payload is missing permission data, ensure the connected account has access to the file or folder
* The trigger sends file IDs only; use the Drive API if you need to fetch binary content during the crew run
* Remember: use `crewai triggers run` (not `crewai run`) to simulate trigger execution

---

## Simulate a Microsoft Teams trigger with realistic payload

**URL:** llms-txt#simulate-a-microsoft-teams-trigger-with-realistic-payload

**Contents:**
- Troubleshooting

crewai triggers run microsoft_teams/teams_message_created
```

The `crewai triggers run` command will execute your crew with a complete Teams payload, allowing you to test your parsing logic before deployment.

<Warning>
  Use `crewai triggers run microsoft_teams/teams_message_created` (not `crewai run`) to simulate trigger execution during development. After deployment, your crew will automatically receive the trigger payload.
</Warning>

* Ensure the Teams connection is active; it must be refreshed if the tenant revokes permissions
* Test locally with `crewai triggers run microsoft_teams/teams_message_created` to see the exact payload structure
* Confirm the webhook subscription in Microsoft 365 is still valid if payloads stop arriving
* Review execution logs for payload shape mismatches—Graph notifications may omit fields when a chat is private or restricted
* Remember: use `crewai triggers run` (not `crewai run`) to simulate trigger execution

---

## Simulate a OneDrive trigger with realistic payload

**URL:** llms-txt#simulate-a-onedrive-trigger-with-realistic-payload

**Contents:**
- Troubleshooting

crewai triggers run microsoft_onedrive/file_changed
```

The `crewai triggers run` command will execute your crew with a complete OneDrive payload, allowing you to test your parsing logic before deployment.

<Warning>
  Use `crewai triggers run microsoft_onedrive/file_changed` (not `crewai run`) to simulate trigger execution during development. After deployment, your crew will automatically receive the trigger payload.
</Warning>

* Ensure the connected account has permission to read the file metadata included in the webhook
* Test locally with `crewai triggers run microsoft_onedrive/file_changed` to see the exact payload structure
* If the trigger fires but the payload is missing `permissions`, confirm the site-level sharing settings allow Graph to return this field
* For large tenants, filter notifications upstream so the crew only runs on relevant directories
* Remember: use `crewai triggers run` (not `crewai run`) to simulate trigger execution

---

## Single LLM-based guardrail

**URL:** llms-txt#single-llm-based-guardrail

**Contents:**
  - Multiple Guardrails

blog_task = Task(
    description="Write a blog post about AI",
    expected_output="A blog post under 200 words",
    agent=blog_agent,
    guardrail="The blog post must be under 200 words and contain no technical jargon"
)
python Code theme={null}
research_task = Task(
    description="Research the latest developments in quantum computing",
    expected_output="A comprehensive research report",
    agent=researcher_agent,
    guardrail="""
    The research report must:
    - Be at least 1000 words long
    - Include at least 5 credible sources
    - Cover both technical and practical applications
    - Be written in a professional, academic tone
    - Avoid speculation or unverified claims
    """
)
python Code theme={null}
from typing import Tuple, Any
from crewai import TaskOutput, Task

def validate_word_count(result: TaskOutput) -> Tuple[bool, Any]:
    """Validate word count is within limits."""
    word_count = len(result.raw.split())
    if word_count < 100:
        return (False, f"Content too short: {word_count} words. Need at least 100 words.")
    if word_count > 500:
        return (False, f"Content too long: {word_count} words. Maximum is 500 words.")
    return (True, result.raw)

def validate_no_profanity(result: TaskOutput) -> Tuple[bool, Any]:
    """Check for inappropriate language."""
    profanity_words = ["badword1", "badword2"]  # Example list
    content_lower = result.raw.lower()
    for word in profanity_words:
        if word in content_lower:
            return (False, f"Inappropriate language detected: {word}")
    return (True, result.raw)

def format_output(result: TaskOutput) -> Tuple[bool, Any]:
    """Format and clean the output."""
    formatted = result.raw.strip()
    # Capitalize first letter
    formatted = formatted[0].upper() + formatted[1:] if formatted else formatted
    return (True, formatted)

**Examples:**

Example 1 (unknown):
```unknown
LLM-based guardrails are particularly useful for:

* **Complex validation logic** that's difficult to express programmatically
* **Subjective criteria** like tone, style, or quality assessments
* **Natural language requirements** that are easier to describe than code

The LLM guardrail will:

1. Analyze the task output against your description
2. Return `(True, output)` if the output complies with the criteria
3. Return `(False, feedback)` with specific feedback if validation fails

**Example with detailed validation criteria**:
```

Example 2 (unknown):
```unknown
### Multiple Guardrails

You can apply multiple guardrails to a task using the `guardrails` parameter. Multiple guardrails are executed sequentially, with each guardrail receiving the output from the previous one. This allows you to chain validation and transformation steps.

The `guardrails` parameter accepts:

* A list of guardrail functions or string descriptions
* A single guardrail function or string (same as `guardrail`)

**Note**: If `guardrails` is provided, it takes precedence over `guardrail`. The `guardrail` parameter will be ignored when `guardrails` is set.
```

---

## Snippet: Achetez vos billets exclusivement sur le site officiel de la billetterie de Paris 2024 pour participer au plus grand événement sportif au monde.

**URL:** llms-txt#snippet:-achetez-vos-billets-exclusivement-sur-le-site-officiel-de-la-billetterie-de-paris-2024-pour-participer-au-plus-grand-événement-sportif-au-monde.

---

## Snippet: … as ChatGPT, have the potential to play a critical role in advancing our understanding of climate

**URL:** llms-txt#snippet:-…-as-chatgpt,-have-the-potential-to-play-a-critical-role-in-advancing-our-understanding-of-climate

---

## Snippet: … ChatGPT in public health. In this overview, we will examine the potential uses of ChatGPT in

**URL:** llms-txt#snippet:-…-chatgpt-in-public-health.-in-this-overview,-we-will-examine-the-potential-uses-of-chatgpt-in

---

## Snippet: Quels sont les sports présents aux Jeux Olympiques de Paris 2024 ? · Athlétisme · Aviron · Badminton · Basketball · Basketball 3x3 · Boxe · Breaking · Canoë ...

**URL:** llms-txt#snippet:-quels-sont-les-sports-présents-aux-jeux-olympiques-de-paris-2024-?-·-athlétisme-·-aviron-·-badminton-·-basketball-·-basketball-3x3-·-boxe-·-breaking-·-canoë-...

---

## SSE Transport

**URL:** llms-txt#sse-transport

**Contents:**
- Overview
- Key Concepts
- Connecting via SSE
  - 1. Fully Managed Connection (Recommended)

Source: https://docs.crewai.com/en/mcp/sse

Learn how to connect CrewAI to remote MCP servers using Server-Sent Events (SSE) for real-time communication.

Server-Sent Events (SSE) provide a standard way for a web server to send updates to a client over a single, long-lived HTTP connection. In the context of MCP, SSE is used for remote servers to stream data (like tool responses) to your CrewAI application in real-time.

* **Remote Servers**: SSE is suitable for MCP servers hosted remotely.
* **Unidirectional Stream**: Typically, SSE is a one-way communication channel from server to client.
* **`MCPServerAdapter` Configuration**: For SSE, you'll provide the server's URL and specify the transport type.

## Connecting via SSE

You can connect to an SSE-based MCP server using two main approaches for managing the connection lifecycle:

### 1. Fully Managed Connection (Recommended)

Using a Python context manager (`with` statement) is the recommended approach. It automatically handles establishing and closing the connection to the SSE MCP server.

```python theme={null}
from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter

server_params = {
    "url": "http://localhost:8000/sse", # Replace with your actual SSE server URL
    "transport": "sse" 
}

---

## Starting the flow (will pause and wait for Slack response)

**URL:** llms-txt#starting-the-flow-(will-pause-and-wait-for-slack-response)

def start_content_pipeline():
    flow = ContentPipeline()
    result = flow.kickoff()

if isinstance(result, HumanFeedbackPending):
        return {"status": "pending", "flow_id": result.context.flow_id}

---

## Static filtering (allow/block lists)

**URL:** llms-txt#static-filtering-(allow/block-lists)

static_filter = create_static_tool_filter(
    allowed_tool_names=["read_file", "write_file"],
    blocked_tool_names=["delete_file"],
)

---

## Stdio Transport

**URL:** llms-txt#stdio-transport

**Contents:**
- Overview
- Key Concepts
- Connecting via Stdio
  - 1. Fully Managed Connection (Recommended)

Source: https://docs.crewai.com/en/mcp/stdio

Learn how to connect CrewAI to local MCP servers using the Stdio (Standard Input/Output) transport mechanism.

The Stdio (Standard Input/Output) transport is designed for connecting `MCPServerAdapter` to local MCP servers that communicate over their standard input and output streams. This is typically used when the MCP server is a script or executable running on the same machine as your CrewAI application.

* **Local Execution**: Stdio transport manages a locally running process for the MCP server.
* **`StdioServerParameters`**: This class from the `mcp` library is used to configure the command, arguments, and environment variables for launching the Stdio server.

## Connecting via Stdio

You can connect to an Stdio-based MCP server using two main approaches for managing the connection lifecycle:

### 1. Fully Managed Connection (Recommended)

Using a Python context manager (`with` statement) is the recommended approach. It automatically handles starting the MCP server process and stopping it when the context is exited.

```python theme={null}
from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters
import os

---

## Store in project directory

**URL:** llms-txt#store-in-project-directory

project_root = Path(__file__).parent
storage_dir = project_root / "crewai_storage"

os.environ["CREWAI_STORAGE_DIR"] = str(storage_dir)

---

## Store knowledge in project directory

**URL:** llms-txt#store-knowledge-in-project-directory

project_root = Path(__file__).parent
knowledge_dir = project_root / "knowledge_storage"

os.environ["CREWAI_STORAGE_DIR"] = str(knowledge_dir)

---

## Store sensitive data in environment variables

**URL:** llms-txt#store-sensitive-data-in-environment-variables

**Contents:**
  - Storage Security

crew = Crew(
    memory=True,
    embedder={
        "provider": "openai",
        "config": {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "model": "text-embedding-3-small"
        }
    }
)
python theme={null}
import os
from crewai import Crew
from crewai.memory import LongTermMemory
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage

**Examples:**

Example 1 (unknown):
```unknown
### Storage Security
```

---

## Store text and embeddings in Qdrant

**URL:** llms-txt#store-text-and-embeddings-in-qdrant

def load_pdf_to_qdrant(pdf_path, qdrant, collection_name):
    # Extract text from PDF
    text_chunks = extract_text_from_pdf(pdf_path)

# Create Qdrant collection
    if qdrant.collection_exists(collection_name):
        qdrant.delete_collection(collection_name)
    qdrant.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=3072, distance=Distance.COSINE)
    )

# Store embeddings
    points = []
    for chunk in text_chunks:
        embedding = get_openai_embedding(chunk)
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={"text": chunk}
        ))
    qdrant.upsert(collection_name=collection_name, points=points)

---

## Streamable HTTP Transport

**URL:** llms-txt#streamable-http-transport

**Contents:**
- Overview
- Key Concepts
- Connecting via Streamable HTTP
  - 1. Fully Managed Connection (Recommended)
  - 2. Manual Connection Lifecycle
- Security Considerations

Source: https://docs.crewai.com/en/mcp/streamable-http

Learn how to connect CrewAI to remote MCP servers using the flexible Streamable HTTP transport.

Streamable HTTP transport provides a flexible way to connect to remote MCP servers. It's often built upon HTTP and can support various communication patterns, including request-response and streaming, sometimes utilizing Server-Sent Events (SSE) for server-to-client streams within a broader HTTP interaction.

* **Remote Servers**: Designed for MCP servers hosted remotely.
* **Flexibility**: Can support more complex interaction patterns than plain SSE, potentially including bi-directional communication if the server implements it.
* **`MCPServerAdapter` Configuration**: You'll need to provide the server's base URL for MCP communication and specify `"streamable-http"` as the transport type.

## Connecting via Streamable HTTP

You have two primary methods for managing the connection lifecycle with a Streamable HTTP MCP server:

### 1. Fully Managed Connection (Recommended)

The recommended approach is to use a Python context manager (`with` statement), which handles the connection's setup and teardown automatically.

**Note:** Replace `"http://localhost:8001/mcp"` with the actual URL of your Streamable HTTP MCP server.

### 2. Manual Connection Lifecycle

For scenarios requiring more explicit control, you can manage the `MCPServerAdapter` connection manually.

<Info>
  It is **critical** to call `mcp_server_adapter.stop()` when you are done to close the connection and free up resources. A `try...finally` block is the safest way to ensure this.
</Info>

## Security Considerations

When using Streamable HTTP transport, general web security best practices are paramount:

* **Use HTTPS**: Always prefer HTTPS (HTTP Secure) for your MCP server URLs to encrypt data in transit.
* **Authentication**: Implement robust authentication mechanisms if your MCP server exposes sensitive tools or data.
* **Input Validation**: Ensure your MCP server validates all incoming requests and parameters.

For a comprehensive guide on securing your MCP integrations, please refer to our [Security Considerations](./security.mdx) page and the official [MCP Transport Security documentation](https://modelcontextprotocol.io/docs/concepts/transports#security-considerations).

**Examples:**

Example 1 (unknown):
```unknown
**Note:** Replace `"http://localhost:8001/mcp"` with the actual URL of your Streamable HTTP MCP server.

### 2. Manual Connection Lifecycle

For scenarios requiring more explicit control, you can manage the `MCPServerAdapter` connection manually.

<Info>
  It is **critical** to call `mcp_server_adapter.stop()` when you are done to close the connection and free up resources. A `try...finally` block is the safest way to ensure this.
</Info>
```

---

## Strict guardrail requiring high faithfulness score

**URL:** llms-txt#strict-guardrail-requiring-high-faithfulness-score

**Contents:**
  - Including Tool Response Context

strict_guardrail = HallucinationGuardrail(
    context="Quantum computing uses qubits that exist in superposition states.",
    llm=LLM(model="gpt-4o-mini"),
    threshold=8.0  # Requires score >= 8 to pass validation
)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### Including Tool Response Context

When your task uses tools, you can include tool responses for more accurate validation:
```

---

## Switch to a different organization

**URL:** llms-txt#switch-to-a-different-organization

crewai org switch <org_id>

---

## Sync handler:

**URL:** llms-txt#sync-handler:

def handle_feedback_webhook(flow_id: str, feedback: str):
    flow = ReviewFlow.from_pending(flow_id)
    result = flow.resume(feedback)
    return result

---

## Team Management

**URL:** llms-txt#team-management

**Contents:**
- Inviting Team Members
- Adding Roles
- Important Notes

Source: https://docs.crewai.com/en/enterprise/guides/team-management

Learn how to invite and manage team members in your CrewAI AOP organization

As an administrator of a CrewAI AOP account, you can easily invite new team members to join your organization. This guide will walk you through the process step-by-step.

## Inviting Team Members

<Steps>
  <Step title="Access the Settings Page">
    * Log in to your CrewAI AOP account
    * Look for the gear icon (⚙️) in the top right corner of the dashboard
    * Click on the gear icon to access the **Settings** page:
      <Frame>
        <img alt="Settings Page" />
      </Frame>
  </Step>

<Step title="Navigate to the Members Section">
    * On the Settings page, you'll see a `Members` tab
    * Click on the `Members` tab to access the **Members** page:
      <Frame>
        <img alt="Members Tab" />
      </Frame>
  </Step>

<Step title="Invite New Members">
    * In the Members section, you'll see a list of current members (including yourself)
    * Locate the `Email` input field
    * Enter the email address of the person you want to invite
    * Click the `Invite` button to send the invitation
  </Step>

<Step title="Repeat as Needed">
    * You can repeat this process to invite multiple team members
    * Each invited member will receive an email invitation to join your organization
  </Step>
</Steps>

You can add roles to your team members to control their access to different parts of the platform.

<Steps>
  <Step title="Access the Settings Page">
    * Log in to your CrewAI AOP account
    * Look for the gear icon (⚙️) in the top right corner of the dashboard
    * Click on the gear icon to access the **Settings** page:
      <Frame>
        <img alt="Settings Page" />
      </Frame>
  </Step>

<Step title="Navigate to the Members Section">
    * On the Settings page, you'll see a `Roles` tab
    * Click on the `Roles` tab to access the **Roles** page.
      <Frame>
        <img alt="Roles Tab" />
      </Frame>
    * Click on the `Add Role` button to add a new role.
    * Enter the details and permissions of the role and click the `Create Role` button to create the role.
      <Frame>
        <img alt="Add Role Modal" />
      </Frame>
  </Step>

<Step title="Add Roles to Members">
    * In the Members section, you'll see a list of current members (including yourself)
      <Frame>
        <img alt="Member Accepted Invitation" />
      </Frame>
    * Once the member has accepted the invitation, you can add a role to them.
    * Navigate back to `Roles` tab
    * Go to the member you want to add a role to and under the `Role` column, click on the dropdown
    * Select the role you want to add to the member
    * Click the `Update` button to save the role
      <Frame>
        <img alt="Add Role to Member" />
      </Frame>
  </Step>
</Steps>

* **Admin Privileges**: Only users with administrative privileges can invite new members
* **Email Accuracy**: Ensure you have the correct email addresses for your team members
* **Invitation Acceptance**: Invited members will need to accept the invitation to join your organization
* **Email Notifications**: You may want to inform your team members to check their email (including spam folders) for the invitation

By following these steps, you can easily expand your team and collaborate more effectively within your CrewAI AOP organization.

---

## Telemetry

**URL:** llms-txt#telemetry

**Contents:**
- Telemetry
  - Examples:

Source: https://docs.crewai.com/en/telemetry

Understanding the telemetry data collected by CrewAI and how it contributes to the enhancement of the library.

<Note>
  By default, we collect no data that would be considered personal information under GDPR and other privacy regulations.
  We do collect Tool's names and Agent's roles, so be advised not to include any personal information in the tool's names or the Agent's roles.
  Because no personal information is collected, it's not necessary to worry about data residency.
  When `share_crew` is enabled, additional data is collected which may contain personal information if included by the user.
  Users should exercise caution when enabling this feature to ensure compliance with privacy regulations.
</Note>

CrewAI utilizes anonymous telemetry to gather usage statistics with the primary goal of enhancing the library.
Our focus is on improving and developing the features, integrations, and tools most utilized by our users.

It's pivotal to understand that by default, **NO personal data is collected** concerning prompts, task descriptions, agents' backstories or goals,
usage of tools, API calls, responses, any data processed by the agents, or secrets and environment variables.
When the `share_crew` feature is enabled, detailed data including task descriptions, agents' backstories or goals, and other specific attributes are collected
to provide deeper insights. This expanded data collection may include personal information if users have incorporated it into their crews or tasks.
Users should carefully consider the content of their crews and tasks before enabling `share_crew`.
Users can disable telemetry by setting the environment variable `CREWAI_DISABLE_TELEMETRY` to `true` or by setting `OTEL_SDK_DISABLED` to `true` (note that the latter disables all OpenTelemetry instrumentation globally).

```python theme={null}

---

## Testing

**URL:** llms-txt#testing

**Contents:**
- Overview
  - Using the Testing Feature

Source: https://docs.crewai.com/en/concepts/testing

Learn how to test your CrewAI Crew and evaluate their performance.

Testing is a crucial part of the development process, and it is essential to ensure that your crew is performing as expected. With crewAI, you can easily test your crew and evaluate its performance using the built-in testing capabilities.

### Using the Testing Feature

We added the CLI command `crewai test` to make it easy to test your crew. This command will run your crew for a specified number of iterations and provide detailed performance metrics. The parameters are `n_iterations` and `model`, which are optional and default to 2 and `gpt-4o-mini` respectively. For now, the only provider available is OpenAI.

If you want to run more iterations or use a different model, you can specify the parameters like this:

or using the short forms:

When you run the `crewai test` command, the crew will be executed for the specified number of iterations, and the performance metrics will be displayed at the end of the run.

A table of scores at the end will show the performance of the crew in terms of the following metrics:

<center>**Tasks Scores (1-10 Higher is better)**</center>

| Tasks/Crew/Agents  | Run 1 | Run 2 | Avg. Total |            Agents            | Additional Info                |
| :----------------- | :---: | :---: | :--------: | :--------------------------: | :----------------------------- |
| Task 1             |  9.0  |  9.5  |   **9.2**  |     Professional Insights    |                                |
|                    |       |       |            |          Researcher          |                                |
| Task 2             |  9.0  |  10.0 |   **9.5**  | Company Profile Investigator |                                |
| Task 3             |  9.0  |  9.0  |   **9.0**  |      Automation Insights     |                                |
|                    |       |       |            |          Specialist          |                                |
| Task 4             |  9.0  |  9.0  |   **9.0**  |     Final Report Compiler    | Automation Insights Specialist |
| Crew               |  9.00 |  9.38 |   **9.2**  |                              |                                |
| Execution Time (s) |  126  |  145  |   **135**  |                              |                                |

The example above shows the test results for two runs of the crew with two tasks, with the average total score for each task and the crew as a whole.

**Examples:**

Example 1 (unknown):
```unknown
If you want to run more iterations or use a different model, you can specify the parameters like this:
```

Example 2 (unknown):
```unknown
or using the short forms:
```

---

## Test different providers with the same data

**URL:** llms-txt#test-different-providers-with-the-same-data

**Contents:**
  - Troubleshooting Embedding Issues

providers_to_test = [
    {
        "name": "OpenAI",
        "config": {
            "provider": "openai",
            "config": {"model": "text-embedding-3-small"}
        }
    },
    {
        "name": "Ollama",
        "config": {
            "provider": "ollama",
            "config": {"model": "mxbai-embed-large"}
        }
    }
]

for provider in providers_to_test:
    print(f"\nTesting {provider['name']} embeddings...")

# Create crew with specific embedder
    crew = Crew(
        agents=[...],
        tasks=[...],
        memory=True,
        embedder=provider['config']
    )

# Run your test and measure performance
    result = crew.kickoff()
    print(f"{provider['name']} completed successfully")
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### Troubleshooting Embedding Issues

**Model not found errors:**
```

---

## These servers will timeout gracefully if unresponsive

**URL:** llms-txt#these-servers-will-timeout-gracefully-if-unresponsive

**Contents:**
- Performance Features
  - Automatic Caching

mcps=[
    "https://slow-server.com/mcp",        # Will timeout after 10s if unresponsive
    "https://overloaded-api.com/mcp"      # Will timeout if discovery takes > 15s
]
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## Performance Features

### Automatic Caching

Tool schemas are cached for 5 minutes to improve performance:
```

---

## The fingerprint remains unchanged

**URL:** llms-txt#the-fingerprint-remains-unchanged

**Contents:**
- Deterministic Fingerprints

assert agent.fingerprint.uuid_str == original_fingerprint
python theme={null}
from crewai.security import Fingerprint

**Examples:**

Example 1 (unknown):
```unknown
## Deterministic Fingerprints

While you cannot directly set the UUID and creation timestamp, you can create deterministic fingerprints using the `generate` method with a seed:
```

---

## The same seed always produces the same fingerprint

**URL:** llms-txt#the-same-seed-always-produces-the-same-fingerprint

same_fingerprint = Fingerprint.generate(seed="my-agent-id")
assert deterministic_fingerprint.uuid_str == same_fingerprint.uuid_str

---

## This approach is suitable when the JSON path is either known beforehand or can be dynamically identified.

**URL:** llms-txt#this-approach-is-suitable-when-the-json-path-is-either-known-beforehand-or-can-be-dynamically-identified.

tool = JSONSearchTool()

---

## This context enables Claude to perform like a domain expert

**URL:** llms-txt#this-context-enables-claude-to-perform-like-a-domain-expert

---

## This happens when switching embedding providers

**URL:** llms-txt#this-happens-when-switching-embedding-providers

---

## timeout=600

**URL:** llms-txt#timeout=600

---

## Title: Billetterie Officielle de Paris 2024 - Jeux Olympiques et Paralympiques

**URL:** llms-txt#title:-billetterie-officielle-de-paris-2024---jeux-olympiques-et-paralympiques

---

## Title: Potential use of chat gpt in global warming

**URL:** llms-txt#title:-potential-use-of-chat-gpt-in-global-warming

---

## Too broad

**URL:** llms-txt#too-broad

class BloatedState(BaseModel):
    user_data: Dict = {}
    system_settings: Dict = {}
    temporary_calculations: List = []
    debug_info: Dict = {}
    # ...many more fields

---

## To enable scrapping any website it finds during it's execution

**URL:** llms-txt#to-enable-scrapping-any-website-it-finds-during-it's-execution

tool = ScrapeWebsiteTool()

---

## to search across any discovered websites

**URL:** llms-txt#to-search-across-any-discovered-websites

tool = WebsiteSearchTool()

---

## To search any code documentation content

**URL:** llms-txt#to-search-any-code-documentation-content

---

## To specifically focus your search on a given documentation site

**URL:** llms-txt#to-specifically-focus-your-search-on-a-given-documentation-site

---

## TrueFoundry Integration

**URL:** llms-txt#truefoundry-integration

**Contents:**
- How TrueFoundry Integrates with CrewAI
  - Installation & Setup
  - Complete CrewAI Example

Source: https://docs.crewai.com/en/observability/truefoundry

TrueFoundry provides an enterprise-ready [AI Gateway](https://www.truefoundry.com/ai-gateway) which can integrate with agentic frameworks like CrewAI and provides governance and observability for your AI Applications. TrueFoundry AI Gateway serves as a unified interface for LLM access, providing:

* **Unified API Access**: Connect to 250+ LLMs (OpenAI, Claude, Gemini, Groq, Mistral) through one API
* **Low Latency**: Sub-3ms internal latency with intelligent routing and load balancing
* **Enterprise Security**: SOC 2, HIPAA, GDPR compliance with RBAC and audit logging
* **Quota and cost management**: Token-based quotas, rate limiting, and comprehensive usage tracking
* **Observability**: Full request/response logging, metrics, and traces with customizable retention

## How TrueFoundry Integrates with CrewAI

### Installation & Setup

<Steps>
  <Step title="Install CrewAI">
    
  </Step>

<Step title="Get TrueFoundry Access Token">
    1. Sign up for a [TrueFoundry account](https://www.truefoundry.com/register)
    2. Follow the steps here in [Quick start](https://docs.truefoundry.com/gateway/quick-start)
  </Step>

<Step title="Configure CrewAI with TrueFoundry">
    <img alt="TrueFoundry Code Configuration" />

### Complete CrewAI Example

```python theme={null}
from crewai import Agent, Task, Crew, LLM

**Examples:**

Example 1 (unknown):
```unknown
</Step>

  <Step title="Get TrueFoundry Access Token">
    1. Sign up for a [TrueFoundry account](https://www.truefoundry.com/register)
    2. Follow the steps here in [Quick start](https://docs.truefoundry.com/gateway/quick-start)
  </Step>

  <Step title="Configure CrewAI with TrueFoundry">
    <img alt="TrueFoundry Code Configuration" />
```

Example 2 (unknown):
```unknown
</Step>
</Steps>

### Complete CrewAI Example
```

---

## Type-safe registration

**URL:** llms-txt#type-safe-registration

**Contents:**
- Integration with Existing Tools
  - Wrapping Existing Validation
  - Logging to External Systems
- Troubleshooting
  - Hook Not Executing
  - Input Modifications Not Working
  - Result Modifications Not Working
  - Tool Blocked Unexpectedly
- Conclusion

register_before_tool_call_hook(my_before_hook)
register_after_tool_call_hook(my_after_hook)
python theme={null}
def existing_validator(tool_name: str, inputs: dict) -> bool:
    """Your existing validation function."""
    # Your validation logic
    return True

@before_tool_call
def integrate_validator(context: ToolCallHookContext) -> bool | None:
    if not existing_validator(context.tool_name, context.tool_input):
        print(f"❌ Validation failed for {context.tool_name}")
        return False
    return None
python theme={null}
import logging

logger = logging.getLogger(__name__)

@before_tool_call
def log_to_external_system(context: ToolCallHookContext) -> None:
    logger.info(f"Tool call: {context.tool_name}", extra={
        'tool_name': context.tool_name,
        'tool_input': context.tool_input,
        'agent': context.agent.role if context.agent else None
    })
    return None
```

### Hook Not Executing

* Verify hook is registered before crew execution
* Check if previous hook returned `False` (blocks execution and subsequent hooks)
* Ensure hook signature matches expected type

### Input Modifications Not Working

* Use in-place modifications: `context.tool_input['key'] = value`
* Don't replace the dict: `context.tool_input = {}`

### Result Modifications Not Working

* Return the modified string from after hooks
* Returning `None` keeps the original result
* Ensure the tool actually returned a result

### Tool Blocked Unexpectedly

* Check all before hooks for blocking conditions
* Verify hook execution order
* Add debug logging to identify which hook is blocking

Tool Call Hooks provide powerful capabilities for controlling and monitoring tool execution in CrewAI. Use them to implement safety guardrails, approval gates, input validation, result sanitization, logging, and analytics. Combined with proper error handling and type safety, hooks enable secure and production-ready agent systems with comprehensive observability.

**Examples:**

Example 1 (unknown):
```unknown
## Integration with Existing Tools

### Wrapping Existing Validation
```

Example 2 (unknown):
```unknown
### Logging to External Systems
```

---

## Unregister specific hook

**URL:** llms-txt#unregister-specific-hook

def my_hook(context):
    ...

register_before_tool_call_hook(my_hook)

---

## url="https://web-scraping.dev/products"

**URL:** llms-txt#url="https://web-scraping.dev/products"

---

## Useful for:

**URL:** llms-txt#useful-for:

---

## Use knowledge sources instead of large prompts

**URL:** llms-txt#use-knowledge-sources-instead-of-large-prompts

**Contents:**
  - Context Window Best Practices
  - Troubleshooting Context Issues

knowledge_agent = Agent(
    role="Knowledge Expert",
    goal="Answer questions using curated knowledge",
    backstory="Expert at leveraging structured knowledge sources",
    knowledge_sources=[your_knowledge_sources],  # Pre-processed knowledge
    respect_context_window=True,
    verbose=True
)
python Code theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### Context Window Best Practices

1. **Monitor Context Usage**: Enable `verbose=True` to see context management in action
2. **Design for Efficiency**: Structure tasks to minimize context accumulation
3. **Use Appropriate Models**: Choose LLMs with context windows suitable for your tasks
4. **Test Both Settings**: Try both `True` and `False` to see which works better for your use case
5. **Combine with RAG**: Use RAG tools for very large datasets instead of relying solely on context windows

### Troubleshooting Context Issues

**If you're getting context limit errors:**
```

---

## Use secure storage paths

**URL:** llms-txt#use-secure-storage-paths

**Contents:**
- Troubleshooting
  - Common Issues
  - Performance Tips
- Benefits of Using CrewAI's Memory System
- Memory Events
  - Available Memory Events
  - Practical Applications

storage_path = os.getenv("CREWAI_STORAGE_DIR", "./storage")
os.makedirs(storage_path, mode=0o700, exist_ok=True)  # Restricted permissions

crew = Crew(
    memory=True,
    long_term_memory=LongTermMemory(
        storage=LTMSQLiteStorage(
            db_path=f"{storage_path}/memory.db"
        )
    )
)
python theme={null}
from crewai.events import (
    BaseEventListener,
    MemoryQueryCompletedEvent,
    MemorySaveCompletedEvent
)
import time

class MemoryPerformanceMonitor(BaseEventListener):
    def __init__(self):
        super().__init__()
        self.query_times = []
        self.save_times = []

def setup_listeners(self, crewai_event_bus):
        @crewai_event_bus.on(MemoryQueryCompletedEvent)
        def on_memory_query_completed(source, event: MemoryQueryCompletedEvent):
            self.query_times.append(event.query_time_ms)
            print(f"Memory query completed in {event.query_time_ms:.2f}ms. Query: '{event.query}'")
            print(f"Average query time: {sum(self.query_times)/len(self.query_times):.2f}ms")

@crewai_event_bus.on(MemorySaveCompletedEvent)
        def on_memory_save_completed(source, event: MemorySaveCompletedEvent):
            self.save_times.append(event.save_time_ms)
            print(f"Memory save completed in {event.save_time_ms:.2f}ms")
            print(f"Average save time: {sum(self.save_times)/len(self.save_times):.2f}ms")

**Examples:**

Example 1 (unknown):
```unknown
## Troubleshooting

### Common Issues

**Memory not persisting between sessions?**

* Check `CREWAI_STORAGE_DIR` environment variable
* Ensure write permissions to storage directory
* Verify memory is enabled with `memory=True`

**Mem0 authentication errors?**

* Verify `MEM0_API_KEY` environment variable is set
* Check API key permissions on Mem0 dashboard
* Ensure `mem0ai` package is installed

**High memory usage with large datasets?**

* Consider using External Memory with custom storage
* Implement pagination in custom storage search methods
* Use smaller embedding models for reduced memory footprint

### Performance Tips

* Use `memory=True` for most use cases (simplest and fastest)
* Only use User Memory if you need user-specific persistence
* Consider External Memory for high-scale or specialized requirements
* Choose smaller embedding models for faster processing
* Set appropriate search limits to control memory retrieval size

## Benefits of Using CrewAI's Memory System

* 🦾 **Adaptive Learning:** Crews become more efficient over time, adapting to new information and refining their approach to tasks.
* 🫡 **Enhanced Personalization:** Memory enables agents to remember user preferences and historical interactions, leading to personalized experiences.
* 🧠 **Improved Problem Solving:** Access to a rich memory store aids agents in making more informed decisions, drawing on past learnings and contextual insights.

## Memory Events

CrewAI's event system provides powerful insights into memory operations. By leveraging memory events, you can monitor, debug, and optimize your memory system's performance and behavior.

### Available Memory Events

CrewAI emits the following memory-related events:

| Event                             | Description                                                 | Key Properties                                                  |
| :-------------------------------- | :---------------------------------------------------------- | :-------------------------------------------------------------- |
| **MemoryQueryStartedEvent**       | Emitted when a memory query begins                          | `query`, `limit`, `score_threshold`                             |
| **MemoryQueryCompletedEvent**     | Emitted when a memory query completes successfully          | `query`, `results`, `limit`, `score_threshold`, `query_time_ms` |
| **MemoryQueryFailedEvent**        | Emitted when a memory query fails                           | `query`, `limit`, `score_threshold`, `error`                    |
| **MemorySaveStartedEvent**        | Emitted when a memory save operation begins                 | `value`, `metadata`, `agent_role`                               |
| **MemorySaveCompletedEvent**      | Emitted when a memory save operation completes successfully | `value`, `metadata`, `agent_role`, `save_time_ms`               |
| **MemorySaveFailedEvent**         | Emitted when a memory save operation fails                  | `value`, `metadata`, `agent_role`, `error`                      |
| **MemoryRetrievalStartedEvent**   | Emitted when memory retrieval for a task prompt starts      | `task_id`                                                       |
| **MemoryRetrievalCompletedEvent** | Emitted when memory retrieval completes successfully        | `task_id`, `memory_content`, `retrieval_time_ms`                |

### Practical Applications

#### 1. Memory Performance Monitoring

Track memory operation timing to optimize your application:
```

---

## Use this initialization method when you want to limit the search scope to a specific JSON file.

**URL:** llms-txt#use-this-initialization-method-when-you-want-to-limit-the-search-scope-to-a-specific-json-file.

**Contents:**
- Arguments
- Configuration Options

tool = JSONSearchTool(json_path='./path/to/your/file.json')
python Code theme={null}
tool = JSONSearchTool(
    config={
        "llm": {
            "provider": "ollama",  # Other options include google, openai, anthropic, llama2, etc.
            "config": {
                "model": "llama2",
                # Additional optional configurations can be specified here.
                # temperature=0.5,
                # top_p=1,
                # stream=true,
            },
        },
        "embedding_model": {
            "provider": "google-generativeai", # or openai, ollama, ...
            "config": {
                "model_name": "gemini-embedding-001",
                "task_type": "RETRIEVAL_DOCUMENT",
                # Further customization options can be added here.
            },
        },
    }
)
```

**Examples:**

Example 1 (unknown):
```unknown
## Arguments

* `json_path` (str, optional): Specifies the path to the JSON file to be searched. This argument is not required if the tool is initialized for a general search. When provided, it confines the search to the specified JSON file.

## Configuration Options

The JSONSearchTool supports extensive customization through a configuration dictionary. This allows users to select different models for embeddings and summarization based on their requirements.
```

---

## Use without exposing keys in code

**URL:** llms-txt#use-without-exposing-keys-in-code

**Contents:**
  - Testing Different Embedding Providers

crew = Crew(
    memory=True,
    embedder={
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small"
            # API key automatically loaded from environment
        }
    }
)
python theme={null}
from crewai import Crew
from crewai.utilities.paths import db_storage_path

**Examples:**

Example 1 (unknown):
```unknown
### Testing Different Embedding Providers

Compare embedding providers for your specific use case:
```

---

## Use with knowledge sources

**URL:** llms-txt#use-with-knowledge-sources

knowledge_source = StringKnowledgeSource(
    content="Your knowledge content here"
)
knowledge_source.storage = custom_storage
python theme={null}
import os
from pathlib import Path

**Examples:**

Example 1 (unknown):
```unknown
#### Option 3: Project-Specific Knowledge Storage
```

---

## UUID string - the unique identifier (auto-generated)

**URL:** llms-txt#uuid-string---the-unique-identifier-(auto-generated)

uuid_str = fingerprint.uuid_str  # e.g., "123e4567-e89b-12d3-a456-426614174000"

---

## Verify API keys and credentials

**URL:** llms-txt#verify-api-keys-and-credentials

---

## Verify model availability

**URL:** llms-txt#verify-model-availability

from crewai.rag.embeddings.configurator import EmbeddingConfigurator

configurator = EmbeddingConfigurator()
try:
    embedder = configurator.configure_embedder({
        "provider": "ollama",
        "config": {"model": "mxbai-embed-large"}
    })
    print("Embedder configured successfully")
except Exception as e:
    print(f"Configuration error: {e}")
python theme={null}
import os

**Examples:**

Example 1 (unknown):
```unknown
**API key issues:**
```

---

## Verify storage location consistency

**URL:** llms-txt#verify-storage-location-consistency

**Contents:**
  - Knowledge Reset Commands

import os
from crewai.utilities.paths import db_storage_path

print("CREWAI_STORAGE_DIR:", os.getenv("CREWAI_STORAGE_DIR"))
print("Computed storage path:", db_storage_path())
print("Knowledge path:", os.path.join(db_storage_path(), "knowledge"))
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### Knowledge Reset Commands
```

---

## Verify storage location is consistent

**URL:** llms-txt#verify-storage-location-is-consistent

**Contents:**
- Custom Embedder Configuration
  - Why Choose Different Embedding Providers?
  - OpenAI Embeddings (Default)

import os
print("CREWAI_STORAGE_DIR:", os.getenv("CREWAI_STORAGE_DIR"))
print("Current working directory:", os.getcwd())
print("Computed storage path:", db_storage_path())
python theme={null}
from crewai import Crew

**Examples:**

Example 1 (unknown):
```unknown
## Custom Embedder Configuration

CrewAI supports multiple embedding providers to give you flexibility in choosing the best option for your use case. Here's a comprehensive guide to configuring different embedding providers for your memory system.

### Why Choose Different Embedding Providers?

* **Cost Optimization**: Local embeddings (Ollama) are free after initial setup
* **Privacy**: Keep your data local with Ollama or use your preferred cloud provider
* **Performance**: Some models work better for specific domains or languages
* **Consistency**: Match your embedding provider with your LLM provider
* **Compliance**: Meet specific regulatory or organizational requirements

### OpenAI Embeddings (Default)

OpenAI provides reliable, high-quality embeddings that work well for most use cases.
```

---

## Verify the server is running and accessible

**URL:** llms-txt#verify-the-server-is-running-and-accessible

mcps=["https://mcp.example.com/mcp?api_key=valid_key"]
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
**Connection timeouts:**
```

---

## View all available commands

**URL:** llms-txt#view-all-available-commands

---

## View all available triggers

**URL:** llms-txt#view-all-available-triggers

---

## View current organization

**URL:** llms-txt#view-current-organization

---

## View metrics

**URL:** llms-txt#view-metrics

**Contents:**
  - Response Sanitization
- Hook Management
  - Clearing All Hooks

def print_metrics():
    for tool, data in metrics.items():
        avg = data['total_time'] / data['count']
        print(f"{tool}: {data['count']} calls, {avg:.2f}s avg")
python theme={null}
import re

@after_llm_call
def sanitize_llm_response(context):
    """Remove sensitive data from LLM responses."""
    if not context.response:
        return None

result = context.response
    result = re.sub(r'(api[_-]?key)["\']?\s*[:=]\s*["\']?[\w-]+',
                   r'\1: [REDACTED]', result, flags=re.IGNORECASE)
    return result

@after_tool_call
def sanitize_tool_result(context):
    """Remove sensitive data from tool results."""
    if not context.tool_result:
        return None

result = context.tool_result
    result = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                   '[EMAIL-REDACTED]', result)
    return result
python theme={null}
from crewai.hooks import clear_all_global_hooks

**Examples:**

Example 1 (unknown):
```unknown
### Response Sanitization
```

Example 2 (unknown):
```unknown
## Hook Management

### Clearing All Hooks
```

---

## View the logs of your deployment

**URL:** llms-txt#view-the-logs-of-your-deployment

---

## Weave Integration

**URL:** llms-txt#weave-integration

Source: https://docs.crewai.com/en/observability/weave

Learn how to use Weights & Biases (W&B) Weave to track, experiment with, evaluate, and improve your CrewAI applications.

---

## Weave Overview

**URL:** llms-txt#weave-overview

**Contents:**
- Setup Instructions
- Features
- Resources

[Weights & Biases (W\&B) Weave](https://weave-docs.wandb.ai/) is a framework for tracking, experimenting with, evaluating, deploying, and improving LLM-based applications.

<img alt="Overview of W&B Weave CrewAI tracing usage" />

Weave provides comprehensive support for every stage of your CrewAI application development:

* **Tracing & Monitoring**: Automatically track LLM calls and application logic to debug and analyze production systems
* **Systematic Iteration**: Refine and iterate on prompts, datasets, and models
* **Evaluation**: Use custom or pre-built scorers to systematically assess and enhance agent performance
* **Guardrails**: Protect your agents with pre- and post-safeguards for content moderation and prompt safety

Weave automatically captures traces for your CrewAI applications, enabling you to monitor and analyze your agents' performance, interactions, and execution flow. This helps you build better evaluation datasets and optimize your agent workflows.

## Setup Instructions

<Steps>
  <Step title="Install required packages">
    
  </Step>

<Step title="Set up W&B Account">
    Sign up for a [Weights & Biases account](https://wandb.ai) if you haven't already. You'll need this to view your traces and metrics.
  </Step>

<Step title="Initialize Weave in Your Application">
    Add the following code to your application:

After initialization, Weave will provide a URL where you can view your traces and metrics.
  </Step>

<Step title="Create your Crews/Flows">
    
  </Step>

<Step title="View Traces in Weave">
    After running your CrewAI application, visit the Weave URL provided during initialization to view:

* LLM calls and their metadata
    * Agent interactions and task execution flow
    * Performance metrics like latency and token usage
    * Any errors or issues that occurred during execution

<Frame>
      <img alt="Weave tracing example with CrewAI" />
    </Frame>
  </Step>
</Steps>

* Weave automatically captures all CrewAI operations: agent interactions and task executions; LLM calls with metadata and token usage; tool usage and results.
* The integration supports all CrewAI execution methods: `kickoff()`, `kickoff_for_each()`, `kickoff_async()`, and `kickoff_for_each_async()`.
* Automatic tracing of all [crewAI-tools](https://github.com/crewAIInc/crewAI-tools).
* Flow feature support with decorator patching (`@start`, `@listen`, `@router`, `@or_`, `@and_`).
* Track custom guardrails passed to CrewAI `Task` with `@weave.op()`.

For detailed information on what's supported, visit the [Weave CrewAI documentation](https://weave-docs.wandb.ai/guides/integrations/crewai/#getting-started-with-flow).

* [📘 Weave Documentation](https://weave-docs.wandb.ai)
* [📊 Example Weave x CrewAI dashboard](https://wandb.ai/ayut/crewai_demo/weave/traces?cols=%7B%22wb_run_id%22%3Afalse%2C%22attributes.weave.client_version%22%3Afalse%2C%22attributes.weave.os_name%22%3Afalse%2C%22attributes.weave.os_release%22%3Afalse%2C%22attributes.weave.os_version%22%3Afalse%2C%22attributes.weave.source%22%3Afalse%2C%22attributes.weave.sys_version%22%3Afalse%7D\&peekPath=%2Fayut%2Fcrewai_demo%2Fcalls%2F0195c838-38cb-71a2-8a15-651ecddf9d89)
* [🐦 X](https://x.com/weave_wb)

**Examples:**

Example 1 (unknown):
```unknown
</Step>

  <Step title="Set up W&B Account">
    Sign up for a [Weights & Biases account](https://wandb.ai) if you haven't already. You'll need this to view your traces and metrics.
  </Step>

  <Step title="Initialize Weave in Your Application">
    Add the following code to your application:
```

Example 2 (unknown):
```unknown
After initialization, Weave will provide a URL where you can view your traces and metrics.
  </Step>

  <Step title="Create your Crews/Flows">
```

---

## When using Claude as your LLM...

**URL:** llms-txt#when-using-claude-as-your-llm...

from crewai import Agent, LLM

agent = Agent(
    role="Analyst",
    goal="Analyze data",
    backstory="Expert analyst",
    llm=LLM(provider="anthropic", model="claude-3-sonnet")  # Using Claude
)

---

## Without it, even it would produce generic marketing advice

**URL:** llms-txt#without-it,-even-it-would-produce-generic-marketing-advice

**Contents:**
  - c. Holistic Agent-LLM Optimization

**Examples:**

Example 1 (unknown):
```unknown
**Backstory Elements That Enhance LLM Performance:**

* **Domain Experience**: "10+ years in enterprise SaaS sales"
* **Specific Expertise**: "Specializes in technical due diligence for Series B+ rounds"
* **Working Style**: "Prefers data-driven decisions with clear documentation"
* **Quality Standards**: "Insists on citing sources and showing analytical work"

### c. Holistic Agent-LLM Optimization

The most effective agent configurations create synergy between role specificity, backstory depth, and LLM selection. Each element reinforces the others to maximize model performance.

**Optimization Framework:**
```

---

## Your OpenAI key

**URL:** llms-txt#your-openai-key

os.environ["OPENAI_API_KEY"] = "sk-proj-..."
python theme={null}
from langfuse import get_client
 
langfuse = get_client()

**Examples:**

Example 1 (unknown):
```unknown
With the environment variables set, we can now initialize the Langfuse client. get\_client() initializes the Langfuse client using the credentials provided in the environment variables.
```

---

## You can also set metadata

**URL:** llms-txt#you-can-also-set-metadata

**Contents:**
- Advanced Usage
  - Fingerprint Structure

custom_fingerprint = Fingerprint.generate(
    seed="my-agent-id",
    metadata={"version": "1.0"}
)
python theme={null}
from crewai.security import Fingerprint

fingerprint = agent.fingerprint

**Examples:**

Example 1 (unknown):
```unknown
## Advanced Usage

### Fingerprint Structure

Each fingerprint has the following structure:
```

---

## You can easily customize this to match your preferred provider

**URL:** llms-txt#you-can-easily-customize-this-to-match-your-preferred-provider

python theme={null}
from crewai import Crew

**Examples:**

Example 1 (unknown):
```unknown
#### Customizing Embedding Providers
```

---

## }

**URL:** llms-txt#}

**Contents:**
- Parameters
  - Initialization Parameters
  - Run Parameters
- Scrapfly Configuration Options
- Usage

scrape_task = Task(
    description="Extract the main content from the product page at https://web-scraping.dev/products using advanced scraping options including JavaScript rendering and proxy settings.",
    expected_output="A detailed summary of the products with all available information.",
    agent=web_scraper_agent,
)
python Code theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## Parameters

The `ScrapflyScrapeWebsiteTool` accepts the following parameters:

### Initialization Parameters

* **api\_key**: Required. Your Scrapfly API key.

### Run Parameters

* **url**: Required. The URL of the website to scrape.
* **scrape\_format**: Optional. The format in which to extract the web page content. Options are "raw" (HTML), "markdown", or "text". Default is "markdown".
* **scrape\_config**: Optional. A dictionary containing additional Scrapfly scraping configuration options.
* **ignore\_scrape\_failures**: Optional. Whether to ignore failures during scraping. If set to `True`, the tool will return `None` instead of raising an exception when scraping fails.

## Scrapfly Configuration Options

The `scrape_config` parameter allows you to customize the scraping behavior with the following options:

* **asp**: Enable anti-scraping protection bypass.
* **render\_js**: Enable JavaScript rendering with a cloud headless browser.
* **proxy\_pool**: Select a proxy pool (e.g., "public\_residential\_pool", "datacenter").
* **country**: Select a proxy location (e.g., "us", "uk").
* **auto\_scroll**: Automatically scroll the page to load lazy-loaded content.
* **js**: Execute custom JavaScript code by the headless browser.

For a complete list of configuration options, refer to the [Scrapfly API documentation](https://scrapfly.io/docs/scrape-api/getting-started).

## Usage

When using the `ScrapflyScrapeWebsiteTool` with an agent, the agent will need to provide the URL of the website to scrape and can optionally specify the format and additional configuration options:
```

---

## ❌ Avoid: Overlapping or vague roles

**URL:** llms-txt#❌-avoid:-overlapping-or-vague-roles

**Contents:**
  - 2. **Strategic Delegation Enabling**

agent1 = Agent(role="General Assistant", ...)
agent2 = Agent(role="Helper", ...)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### 2. **Strategic Delegation Enabling**
```

---

## ❌ Bad - technical or unclear

**URL:** llms-txt#❌-bad---technical-or-unclear

**Contents:**
  - 3. Always Provide a Default Outcome
  - 4. Use Feedback History for Audit Trails
  - 5. Handle Both Routed and Non-Routed Feedback
- Async Human Feedback (Non-Blocking)
  - The Provider Abstraction
  - Handling Paused Flows
  - Resuming a Paused Flow

emit=["state_1", "state_2", "state_3"]
python Code theme={null}
@human_feedback(
    message="Approve? (press Enter to request revision)",
    emit=["approved", "needs_revision"],
    llm="gpt-4o-mini",
    default_outcome="needs_revision",  # Safe default
)
python Code theme={null}
@listen(final_step)
def create_audit_log(self):
    log = []
    for fb in self.human_feedback_history:
        log.append({
            "step": fb.method_name,
            "outcome": fb.outcome,
            "feedback": fb.feedback,
            "timestamp": fb.timestamp.isoformat(),
        })
    return log
python Code theme={null}
from crewai.flow import Flow, start, human_feedback, HumanFeedbackProvider, HumanFeedbackPending, PendingFeedbackContext

class WebhookProvider(HumanFeedbackProvider):
    """Provider that pauses flow and waits for webhook callback."""

def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

def request_feedback(self, context: PendingFeedbackContext, flow: Flow) -> str:
        # Notify external system (e.g., send Slack message, create ticket)
        self.send_notification(context)

# Pause execution - framework handles persistence automatically
        raise HumanFeedbackPending(
            context=context,
            callback_info={"webhook_url": f"{self.webhook_url}/{context.flow_id}"}
        )

class ReviewFlow(Flow):
    @start()
    @human_feedback(
        message="Review this content:",
        emit=["approved", "rejected"],
        llm="gpt-4o-mini",
        provider=WebhookProvider("https://myapp.com/api"),
    )
    def generate_content(self):
        return "AI-generated content..."

@listen("approved")
    def publish(self, result):
        return "Published!"
python Code theme={null}
flow = ReviewFlow()
result = flow.kickoff()

if isinstance(result, HumanFeedbackPending):
    # Flow is paused, state is automatically persisted
    print(f"Waiting for feedback at: {result.callback_info['webhook_url']}")
    print(f"Flow ID: {result.context.flow_id}")
else:
    # Normal completion
    print(f"Flow completed: {result}")
python Code theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### 3. Always Provide a Default Outcome

Use `default_outcome` to handle cases where users press Enter without typing:
```

Example 2 (unknown):
```unknown
### 4. Use Feedback History for Audit Trails

Access `human_feedback_history` to create audit logs:
```

Example 3 (unknown):
```unknown
### 5. Handle Both Routed and Non-Routed Feedback

When designing flows, consider whether you need routing:

| Scenario                                            | Use        |
| --------------------------------------------------- | ---------- |
| Simple review, just need the feedback text          | No `emit`  |
| Need to branch to different paths based on response | Use `emit` |
| Approval gates with approve/reject/revise           | Use `emit` |
| Collecting comments for logging only                | No `emit`  |

## Async Human Feedback (Non-Blocking)

By default, `@human_feedback` blocks execution waiting for console input. For production applications, you may need **async/non-blocking** feedback that integrates with external systems like Slack, email, webhooks, or APIs.

### The Provider Abstraction

Use the `provider` parameter to specify a custom feedback collection strategy:
```

Example 4 (unknown):
```unknown
<Tip>
  The flow framework **automatically persists state** when `HumanFeedbackPending` is raised. Your provider only needs to notify the external system and raise the exception—no manual persistence calls required.
</Tip>

### Handling Paused Flows

When using an async provider, `kickoff()` returns a `HumanFeedbackPending` object instead of raising an exception:
```

---

## ❌ Bad - too many responsibilities

**URL:** llms-txt#❌-bad---too-many-responsibilities

**Contents:**
  - 2. Handle Errors Gracefully
  - 3. Modify Context In-Place

@before_tool_call
def do_everything(context):
    # Validation + logging + metrics + approval...
    ...
python theme={null}
@before_llm_call
def safe_hook(context):
    try:
        # Your logic
        if some_condition:
            return False
    except Exception as e:
        print(f"Hook error: {e}")
        return None  # Allow execution despite error
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### 2. Handle Errors Gracefully
```

Example 2 (unknown):
```unknown
### 3. Modify Context In-Place
```

---

## ❌ Bad - vague

**URL:** llms-txt#❌-bad---vague

**Contents:**
  - 2. Choose Meaningful Outcomes

@human_feedback(message="Review this:")
python Code theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### 2. Choose Meaningful Outcomes

When using `emit`, pick outcomes that map naturally to human responses:
```

---

## - Conditional hook registration

**URL:** llms-txt#--conditional-hook-registration

---

## ✅ Correct

**URL:** llms-txt#✅-correct

**Contents:**
- Testing Your Custom LLM

def __init__(self, model: str, api_key: str, temperature: Optional[float] = None):
    super().__init__(model=model, temperature=temperature)
python theme={null}
from crewai import Agent, Task, Crew

def test_custom_llm():
    llm = CustomLLM(
        model="test-model",
        api_key="test-key",
        endpoint="https://api.test.com"
    )
    
    # Test basic call
    result = llm.call("Hello, world!")
    assert isinstance(result, str)
    assert len(result) > 0
    
    # Test with CrewAI agent
    agent = Agent(
        role="Test Agent",
        goal="Test custom LLM",
        backstory="A test agent.",
        llm=llm
    )
    
    task = Task(
        description="Say hello",
        expected_output="A greeting",
        agent=agent
    )
    
    crew = Crew(agents=[agent], tasks=[task])
    result = crew.kickoff()
    assert "hello" in result.raw.lower()
```

This guide covers the essentials of implementing custom LLMs in CrewAI.

**Examples:**

Example 1 (unknown):
```unknown
**Function Calling Not Working**

* Ensure `supports_function_calling()` returns `True`
* Check that you handle `tool_calls` in the response
* Verify `available_functions` parameter is used correctly

**Authentication Failures**

* Verify API key format and permissions
* Check authentication header format
* Ensure endpoint URLs are correct

**Response Parsing Errors**

* Validate response structure before accessing nested fields
* Handle cases where content might be None
* Add proper error handling for malformed responses

## Testing Your Custom LLM
```

---

## ✅ Correct - modify in-place

**URL:** llms-txt#✅-correct---modify-in-place

def sanitize_input(context: ToolCallHookContext) -> None:
    context.tool_input['query'] = context.tool_input['query'].lower()

---

## ✅ Disable for focused specialists (optional)

**URL:** llms-txt#✅-disable-for-focused-specialists-(optional)

**Contents:**
  - 3. **Context Sharing**

specialist_agent = Agent(
    role="Data Analyst", 
    allow_delegation=False,  # Focuses on core expertise
    ...
)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### 3. **Context Sharing**
```

---

## - embedding_model (required): choose provider + provider-specific config

**URL:** llms-txt#--embedding_model-(required):-choose-provider-+-provider-specific-config

---

## ✅ Enable delegation for coordinators and generalists

**URL:** llms-txt#✅-enable-delegation-for-coordinators-and-generalists

lead_agent = Agent(
    role="Content Lead",
    allow_delegation=True,  # Can delegate to specialists
    ...
)

---

## ✅ Good - clear and actionable

**URL:** llms-txt#✅-good---clear-and-actionable

@human_feedback(message="Does this summary accurately capture the key points? Reply 'yes' or explain what's missing:")

---

## ✅ Good - focused responsibility

**URL:** llms-txt#✅-good---focused-responsibility

@before_tool_call
def validate_file_path(context):
    if context.tool_name == 'read_file':
        if '..' in context.tool_input.get('path', ''):
            return False
    return None

---

## ✅ Good - natural language outcomes

**URL:** llms-txt#✅-good---natural-language-outcomes

emit=["approved", "rejected", "needs_more_detail"]

---

## ✅ Good: Specific, complementary roles

**URL:** llms-txt#✅-good:-specific,-complementary-roles

researcher = Agent(role="Market Research Analyst", ...)
writer = Agent(role="Technical Content Writer", ...)

---

## - hook1 executed

**URL:** llms-txt#--hook1-executed

---

## - hook2 executed and returned False

**URL:** llms-txt#--hook2-executed-and-returned-false

---

## - hook3 NOT executed

**URL:** llms-txt#--hook3-not-executed

---

## ... import events ...

**URL:** llms-txt#...-import-events-...

class MyCustomListener(BaseEventListener):
    # ... implementation ...

---

## - Loading hooks from configuration

**URL:** llms-txt#--loading-hooks-from-configuration

---

## - Plugin systems

**URL:** llms-txt#--plugin-systems

**Contents:**
- Performance Considerations
- Debugging Hooks
  - Enable Debug Logging
  - Hook Execution Order

python theme={null}
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@before_llm_call
def debug_hook(context):
    logger.debug(f"LLM call: {context.agent.role}, iteration {context.iterations}")
    return None
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
**Note:** For most use cases, decorators are cleaner and more maintainable.

## Performance Considerations

1. **Keep Hooks Fast**: Hooks execute on every call - avoid heavy computation
2. **Cache When Possible**: Store expensive validations or lookups
3. **Be Selective**: Use crew-scoped hooks when global hooks aren't needed
4. **Monitor Hook Overhead**: Profile hook execution time in production
5. **Lazy Import**: Import heavy dependencies only when needed

## Debugging Hooks

### Enable Debug Logging
```

Example 2 (unknown):
```unknown
### Hook Execution Order

Hooks execute in registration order. If a before hook returns `False`, subsequent hooks don't execute:
```

---

## ✅ Solution: Clear hierarchy and responsibilities

**URL:** llms-txt#✅-solution:-clear-hierarchy-and-responsibilities

**Contents:**
- Advanced Collaboration Features
  - Custom Collaboration Rules

manager = Agent(role="Manager", allow_delegation=True)
specialist1 = Agent(role="Specialist A", allow_delegation=False)  # No re-delegation
specialist2 = Agent(role="Specialist B", allow_delegation=False)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## Advanced Collaboration Features

### Custom Collaboration Rules
```

---

## ✅ Solution: Ensure delegation is enabled

**URL:** llms-txt#✅-solution:-ensure-delegation-is-enabled

**Contents:**
  - Issue: Too Much Back-and-Forth

agent = Agent(
    role="...",
    allow_delegation=True,  # This is required!
    ...
)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### Issue: Too Much Back-and-Forth

**Symptoms:** Agents ask excessive questions, slow progress
```

---

## ✅ Solution: Provide better context and specific roles

**URL:** llms-txt#✅-solution:-provide-better-context-and-specific-roles

**Contents:**
  - Issue: Delegation Loops

Task(
    description="""Write a technical blog post about machine learning.
    
    Context: Target audience is software developers with basic ML knowledge.
    Length: 1200 words
    Include: code examples, practical applications, best practices
    
    If you need specific technical details, delegate research to the researcher.""",
    ...
)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### Issue: Delegation Loops

**Symptoms:** Agents delegate back and forth indefinitely
```

---

## ✅ Specific, actionable descriptions

**URL:** llms-txt#✅-specific,-actionable-descriptions

Task(
    description="""Research competitors in the AI chatbot space.
    Focus on: pricing models, key features, target markets.
    Provide data in a structured format.""",
    ...
)

---

## ✅ Specific role - clear LLM requirements

**URL:** llms-txt#✅-specific-role---clear-llm-requirements

**Contents:**
  - b. Backstory as Model Context Amplifier

specific_agent = Agent(
    role="SaaS Revenue Operations Analyst",  # Clear domain expertise needed
    goal="Analyze recurring revenue metrics and identify growth opportunities",
    backstory="Specialist in SaaS business models with deep understanding of ARR, churn, and expansion revenue",
    llm=LLM(model="gpt-4o")  # Reasoning model justified for complex analysis
)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
**Role-to-Model Mapping Strategy:**

* **"Research Analyst"** → Reasoning model (GPT-4o, Claude Sonnet) for complex analysis
* **"Content Editor"** → Creative model (Claude, GPT-4o) for writing quality
* **"Data Processor"** → Efficient model (GPT-4o-mini, Gemini Flash) for structured tasks
* **"API Coordinator"** → Function-calling optimized model (GPT-4o, Claude) for tool usage

### b. Backstory as Model Context Amplifier

<Info>
  Strategic backstories multiply your chosen LLM's effectiveness by providing domain-specific context that generic prompting cannot achieve.
</Info>

A well-crafted backstory transforms your LLM choice from generic capability to specialized expertise. This is especially crucial for cost optimization - a well-contextualized efficient model can outperform a premium model without proper context.

**Context-Driven Performance Example:**
```

---

## ❌ These will cause deployment failures

**URL:** llms-txt#❌-these-will-cause-deployment-failures

OPENAI_TOKEN=sk-...
DATABASE_PASSWORD=mypassword
API_SECRET=secret123

---

## ✅ Use these naming patterns instead

**URL:** llms-txt#✅-use-these-naming-patterns-instead

**Contents:**
  - Best Practices
  - Interact with Your Deployed Crew
  - Trigger an Execution
  - Monitoring and Analytics
  - Advanced Features

OPENAI_API_KEY=sk-...
DATABASE_CREDENTIALS=mypassword
API_CONFIG=secret123
```

1. **Use standard naming conventions**: `PROVIDER_API_KEY` instead of `PROVIDER_TOKEN`
2. **Test locally first**: Ensure your crew works with the renamed variables
3. **Update your code**: Change any references to the old variable names
4. **Document changes**: Keep track of renamed variables for your team

<Tip>
  If you encounter deployment failures with cryptic environment variable errors, check your variable names against these patterns first.
</Tip>

### Interact with Your Deployed Crew

Once deployment is complete, you can access your crew through:

1. **REST API**: The platform generates a unique HTTPS endpoint with these key routes:
   * `/inputs`: Lists the required input parameters
   * `/kickoff`: Initiates an execution with provided inputs
   * `/status/{kickoff_id}`: Checks the execution status

2. **Web Interface**: Visit [app.crewai.com](https://app.crewai.com) to access:
   * **Status tab**: View deployment information, API endpoint details, and authentication token
   * **Run tab**: Visual representation of your crew's structure
   * **Executions tab**: History of all executions
   * **Metrics tab**: Performance analytics
   * **Traces tab**: Detailed execution insights

### Trigger an Execution

From the Enterprise dashboard, you can:

1. Click on your crew's name to open its details
2. Select "Trigger Crew" from the management interface
3. Enter the required inputs in the modal that appears
4. Monitor progress as the execution moves through the pipeline

### Monitoring and Analytics

The Enterprise platform provides comprehensive observability features:

* **Execution Management**: Track active and completed runs
* **Traces**: Detailed breakdowns of each execution
* **Metrics**: Token usage, execution times, and costs
* **Timeline View**: Visual representation of task sequences

### Advanced Features

The Enterprise platform also offers:

* **Environment Variables Management**: Securely store and manage API keys
* **LLM Connections**: Configure integrations with various LLM providers
* **Custom Tools Repository**: Create, share, and install tools
* **Crew Studio**: Build crews through a chat interface without writing code

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with deployment issues or questions about the Enterprise platform.
</Card>

---

## - vectordb (required): choose vector DB and pass its config

**URL:** llms-txt#--vectordb-(required):-choose-vector-db-and-pass-its-config

tool = PDFSearchTool(
    config={
        "embedding_model": {
            # Supported providers: "openai", "azure", "google-generativeai", "google-vertex",
            # "voyageai", "cohere", "huggingface", "jina", "sentence-transformer",
            # "text2vec", "ollama", "openclip", "instructor", "onnx", "roboflow", "watsonx", "custom"
            "provider": "openai",  # or: "google-generativeai", "cohere", "ollama", ...
            "config": {
                # Model identifier for the chosen provider. "model" will be auto-mapped to "model_name" internally.
                "model": "text-embedding-3-small",
                # Optional: API key. If omitted, the tool will use provider-specific env vars
                # (e.g., OPENAI_API_KEY or EMBEDDINGS_OPENAI_API_KEY for OpenAI).
                # "api_key": "sk-...",

# Provider-specific examples:
                # --- Google Generative AI ---
                # (Set provider="google-generativeai" above)
                # "model_name": "gemini-embedding-001",
                # "task_type": "RETRIEVAL_DOCUMENT",
                # "title": "Embeddings",

# --- Cohere ---
                # (Set provider="cohere" above)
                # "model": "embed-english-v3.0",

# --- Ollama (local) ---
                # (Set provider="ollama" above)
                # "model": "nomic-embed-text",
            },
        },
        "vectordb": {
                    "provider": "chromadb",  # or "qdrant"
                    "config": {
                        # For ChromaDB: pass "settings" (chromadb.config.Settings) or rely on defaults.
                        # Example (uncomment and import):
                        # from chromadb.config import Settings
                        # "settings": Settings(
                        #     persist_directory="/content/chroma",
                        #     allow_reset=True,
                        #     is_persistent=True,
                        # ),

# For Qdrant: pass "vectors_config" (qdrant_client.models.VectorParams).
                        # Example (uncomment and import):
                        # from qdrant_client.models import VectorParams, Distance
                        # "vectors_config": VectorParams(size=384, distance=Distance.COSINE),

# Note: collection name is controlled by the tool (default: "rag_tool_collection"), not set here.
                    }
        },
    }
)
```

---

## ❌ Wrong - missing required parameters

**URL:** llms-txt#❌-wrong---missing-required-parameters

def __init__(self, api_key: str):
    super().__init__()

---

## ❌ Wrong - replaces dict reference

**URL:** llms-txt#❌-wrong---replaces-dict-reference

**Contents:**
- Registration Methods
  - 1. Global Hook Registration
  - 2. Decorator-Based Registration
  - 3. Crew-Scoped Hooks
- Common Use Cases
  - 1. Safety Guardrails
  - 2. Human Approval Gate
  - 3. Input Validation and Sanitization
  - 4. Result Sanitization
  - 5. Tool Usage Analytics

def wrong_approach(context: ToolCallHookContext) -> None:
    context.tool_input = {'query': 'new query'}
python theme={null}
from crewai.hooks import register_before_tool_call_hook, register_after_tool_call_hook

def log_tool_call(context):
    print(f"Tool: {context.tool_name}")
    print(f"Input: {context.tool_input}")
    return None  # Allow execution

register_before_tool_call_hook(log_tool_call)
python theme={null}
from crewai.hooks import before_tool_call, after_tool_call

@before_tool_call
def block_dangerous_tools(context):
    dangerous_tools = ['delete_database', 'drop_table', 'rm_rf']
    if context.tool_name in dangerous_tools:
        print(f"⛔ Blocked dangerous tool: {context.tool_name}")
        return False  # Block execution
    return None

@after_tool_call
def sanitize_results(context):
    if context.tool_result and "password" in context.tool_result.lower():
        return context.tool_result.replace("password", "[REDACTED]")
    return None
python theme={null}
@CrewBase
class MyProjCrew:
    @before_tool_call_crew
    def validate_tool_inputs(self, context):
        # Only applies to this crew
        if context.tool_name == "web_search":
            if not context.tool_input.get('query'):
                print("❌ Invalid search query")
                return False
        return None

@after_tool_call_crew
    def log_tool_results(self, context):
        # Crew-specific tool logging
        print(f"✅ {context.tool_name} completed")
        return None

@crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
python theme={null}
@before_tool_call
def safety_check(context: ToolCallHookContext) -> bool | None:
    # Block tools that could cause harm
    destructive_tools = [
        'delete_file',
        'drop_table',
        'remove_user',
        'system_shutdown'
    ]

if context.tool_name in destructive_tools:
        print(f"🛑 Blocked destructive tool: {context.tool_name}")
        return False

# Warn on sensitive operations
    sensitive_tools = ['send_email', 'post_to_social_media', 'charge_payment']
    if context.tool_name in sensitive_tools:
        print(f"⚠️  Executing sensitive tool: {context.tool_name}")

return None
python theme={null}
@before_tool_call
def require_approval_for_actions(context: ToolCallHookContext) -> bool | None:
    approval_required = [
        'send_email',
        'make_purchase',
        'delete_file',
        'post_message'
    ]

if context.tool_name in approval_required:
        response = context.request_human_input(
            prompt=f"Approve {context.tool_name}?",
            default_message=f"Input: {context.tool_input}\nType 'yes' to approve:"
        )

if response.lower() != 'yes':
            print(f"❌ Tool execution denied: {context.tool_name}")
            return False

return None
python theme={null}
@before_tool_call
def validate_and_sanitize_inputs(context: ToolCallHookContext) -> bool | None:
    # Validate search queries
    if context.tool_name == 'web_search':
        query = context.tool_input.get('query', '')
        if len(query) < 3:
            print("❌ Search query too short")
            return False

# Sanitize query
        context.tool_input['query'] = query.strip().lower()

# Validate file paths
    if context.tool_name == 'read_file':
        path = context.tool_input.get('path', '')
        if '..' in path or path.startswith('/'):
            print("❌ Invalid file path")
            return False

return None
python theme={null}
@after_tool_call
def sanitize_sensitive_data(context: ToolCallHookContext) -> str | None:
    if not context.tool_result:
        return None

import re
    result = context.tool_result

# Remove API keys
    result = re.sub(
        r'(api[_-]?key|token)["\']?\s*[:=]\s*["\']?[\w-]+',
        r'\1: [REDACTED]',
        result,
        flags=re.IGNORECASE
    )

# Remove email addresses
    result = re.sub(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        '[EMAIL-REDACTED]',
        result
    )

# Remove credit card numbers
    result = re.sub(
        r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
        '[CARD-REDACTED]',
        result
    )

return result
python theme={null}
import time
from collections import defaultdict

tool_stats = defaultdict(lambda: {'count': 0, 'total_time': 0, 'failures': 0})

@before_tool_call
def start_timer(context: ToolCallHookContext) -> None:
    context.tool_input['_start_time'] = time.time()
    return None

@after_tool_call
def track_tool_usage(context: ToolCallHookContext) -> None:
    start_time = context.tool_input.get('_start_time', time.time())
    duration = time.time() - start_time

tool_stats[context.tool_name]['count'] += 1
    tool_stats[context.tool_name]['total_time'] += duration

if not context.tool_result or 'error' in context.tool_result.lower():
        tool_stats[context.tool_name]['failures'] += 1

print(f"""
    📊 Tool Stats for {context.tool_name}:
    - Executions: {tool_stats[context.tool_name]['count']}
    - Avg Time: {tool_stats[context.tool_name]['total_time'] / tool_stats[context.tool_name]['count']:.2f}s
    - Failures: {tool_stats[context.tool_name]['failures']}
    """)

return None
python theme={null}
from collections import defaultdict
from datetime import datetime, timedelta

tool_call_history = defaultdict(list)

@before_tool_call
def rate_limit_tools(context: ToolCallHookContext) -> bool | None:
    tool_name = context.tool_name
    now = datetime.now()

# Clean old entries (older than 1 minute)
    tool_call_history[tool_name] = [
        call_time for call_time in tool_call_history[tool_name]
        if now - call_time < timedelta(minutes=1)
    ]

# Check rate limit (max 10 calls per minute)
    if len(tool_call_history[tool_name]) >= 10:
        print(f"🚫 Rate limit exceeded for {tool_name}")
        return False

# Record this call
    tool_call_history[tool_name].append(now)
    return None
python theme={null}
import hashlib
import json

def cache_key(tool_name: str, tool_input: dict) -> str:
    """Generate cache key from tool name and input."""
    input_str = json.dumps(tool_input, sort_keys=True)
    return hashlib.md5(f"{tool_name}:{input_str}".encode()).hexdigest()

@before_tool_call
def check_cache(context: ToolCallHookContext) -> bool | None:
    key = cache_key(context.tool_name, context.tool_input)
    if key in tool_cache:
        print(f"💾 Cache hit for {context.tool_name}")
        # Note: Can't return cached result from before hook
        # Would need to implement this differently
    return None

@after_tool_call
def cache_result(context: ToolCallHookContext) -> None:
    if context.tool_result:
        key = cache_key(context.tool_name, context.tool_input)
        tool_cache[key] = context.tool_result
        print(f"💾 Cached result for {context.tool_name}")
    return None
python theme={null}
@before_tool_call
def debug_tool_call(context: ToolCallHookContext) -> None:
    print(f"""
    🔍 Tool Call Debug:
    - Tool: {context.tool_name}
    - Agent: {context.agent.role if context.agent else 'Unknown'}
    - Task: {context.task.description[:50] if context.task else 'Unknown'}...
    - Input: {context.tool_input}
    """)
    return None

@after_tool_call
def debug_tool_result(context: ToolCallHookContext) -> None:
    if context.tool_result:
        result_preview = context.tool_result[:200]
        print(f"✅ Result Preview: {result_preview}...")
    else:
        print("⚠️  No result returned")
    return None
python theme={null}
from crewai.hooks import (
    unregister_before_tool_call_hook,
    unregister_after_tool_call_hook
)

**Examples:**

Example 1 (unknown):
```unknown
## Registration Methods

### 1. Global Hook Registration

Register hooks that apply to all tool calls across all crews:
```

Example 2 (unknown):
```unknown
### 2. Decorator-Based Registration

Use decorators for cleaner syntax:
```

Example 3 (unknown):
```unknown
### 3. Crew-Scoped Hooks

Register hooks for a specific crew instance:
```

Example 4 (unknown):
```unknown
## Common Use Cases

### 1. Safety Guardrails
```

---

## ❌ Wrong - replaces list reference

**URL:** llms-txt#❌-wrong---replaces-list-reference

**Contents:**
- Registration Methods
  - 1. Global Hook Registration
  - 2. Decorator-Based Registration
  - 3. Crew-Scoped Hooks
- Common Use Cases
  - 1. Iteration Limiting
  - 2. Human Approval Gate
  - 3. Adding System Context
  - 4. Response Sanitization
  - 5. Cost Tracking

def wrong_approach(context: LLMCallHookContext) -> None:
    context.messages = [{"role": "system", "content": "Be concise"}]
python theme={null}
from crewai.hooks import register_before_llm_call_hook, register_after_llm_call_hook

def log_llm_call(context):
    print(f"LLM call by {context.agent.role} at iteration {context.iterations}")
    return None  # Allow execution

register_before_llm_call_hook(log_llm_call)
python theme={null}
from crewai.hooks import before_llm_call, after_llm_call

@before_llm_call
def validate_iteration_count(context):
    if context.iterations > 10:
        print("⚠️ Exceeded maximum iterations")
        return False  # Block execution
    return None

@after_llm_call
def sanitize_response(context):
    if context.response and "API_KEY" in context.response:
        return context.response.replace("API_KEY", "[REDACTED]")
    return None
python theme={null}
@CrewBase
class MyProjCrew:
    @before_llm_call_crew
    def validate_inputs(self, context):
        # Only applies to this crew
        if context.iterations == 0:
            print(f"Starting task: {context.task.description}")
        return None

@after_llm_call_crew
    def log_responses(self, context):
        # Crew-specific response logging
        print(f"Response length: {len(context.response)}")
        return None

@crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
python theme={null}
@before_llm_call
def limit_iterations(context: LLMCallHookContext) -> bool | None:
    max_iterations = 15
    if context.iterations > max_iterations:
        print(f"⛔ Blocked: Exceeded {max_iterations} iterations")
        return False  # Block execution
    return None
python theme={null}
@before_llm_call
def require_approval(context: LLMCallHookContext) -> bool | None:
    if context.iterations > 5:
        response = context.request_human_input(
            prompt=f"Iteration {context.iterations}: Approve LLM call?",
            default_message="Press Enter to approve, or type 'no' to block:"
        )
        if response.lower() == "no":
            print("🚫 LLM call blocked by user")
            return False
    return None
python theme={null}
@before_llm_call
def add_guardrails(context: LLMCallHookContext) -> None:
    # Add safety guidelines to every LLM call
    context.messages.append({
        "role": "system",
        "content": "Ensure responses are factual and cite sources when possible."
    })
    return None
python theme={null}
@after_llm_call
def sanitize_sensitive_data(context: LLMCallHookContext) -> str | None:
    if not context.response:
        return None

# Remove sensitive patterns
    import re
    sanitized = context.response
    sanitized = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN-REDACTED]', sanitized)
    sanitized = re.sub(r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b', '[CARD-REDACTED]', sanitized)

return sanitized
python theme={null}
import tiktoken

@before_llm_call
def track_token_usage(context: LLMCallHookContext) -> None:
    encoding = tiktoken.get_encoding("cl100k_base")
    total_tokens = sum(
        len(encoding.encode(msg.get("content", "")))
        for msg in context.messages
    )
    print(f"📊 Input tokens: ~{total_tokens}")
    return None

@after_llm_call
def track_response_tokens(context: LLMCallHookContext) -> None:
    if context.response:
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = len(encoding.encode(context.response))
        print(f"📊 Response tokens: ~{tokens}")
    return None
python theme={null}
@before_llm_call
def debug_request(context: LLMCallHookContext) -> None:
    print(f"""
    🔍 LLM Call Debug:
    - Agent: {context.agent.role}
    - Task: {context.task.description[:50]}...
    - Iteration: {context.iterations}
    - Message Count: {len(context.messages)}
    - Last Message: {context.messages[-1] if context.messages else 'None'}
    """)
    return None

@after_llm_call
def debug_response(context: LLMCallHookContext) -> None:
    if context.response:
        print(f"✅ Response Preview: {context.response[:100]}...")
    return None
python theme={null}
from crewai.hooks import (
    unregister_before_llm_call_hook,
    unregister_after_llm_call_hook
)

**Examples:**

Example 1 (unknown):
```unknown
## Registration Methods

### 1. Global Hook Registration

Register hooks that apply to all LLM calls across all crews:
```

Example 2 (unknown):
```unknown
### 2. Decorator-Based Registration

Use decorators for cleaner syntax:
```

Example 3 (unknown):
```unknown
### 3. Crew-Scoped Hooks

Register hooks for a specific crew instance:
```

Example 4 (unknown):
```unknown
## Common Use Cases

### 1. Iteration Limiting
```

---

## ❌ Wrong - replaces reference

**URL:** llms-txt#❌-wrong---replaces-reference

**Contents:**
  - 4. Use Type Hints
  - 5. Clean Up in Tests
- When to Use Which Hook
  - Use LLM Hooks When:
  - Use Tool Hooks When:
  - Use Both When:
- Alternative Registration Methods
  - Programmatic Registration (Advanced)

@before_llm_call
def wrong_approach(context):
    context.messages = [{"role": "system", "content": "Be concise"}]
python theme={null}
from crewai.hooks import LLMCallHookContext, ToolCallHookContext

def my_llm_hook(context: LLMCallHookContext) -> bool | None:
    # IDE autocomplete and type checking
    return None

def my_tool_hook(context: ToolCallHookContext) -> str | None:
    return None
python theme={null}
import pytest
from crewai.hooks import clear_all_global_hooks

@pytest.fixture(autouse=True)
def clean_hooks():
    """Reset hooks before each test."""
    yield
    clear_all_global_hooks()
python theme={null}
from crewai.hooks import (
    register_before_llm_call_hook,
    register_after_tool_call_hook
)

def my_hook(context):
    return None

**Examples:**

Example 1 (unknown):
```unknown
### 4. Use Type Hints
```

Example 2 (unknown):
```unknown
### 5. Clean Up in Tests
```

Example 3 (unknown):
```unknown
## When to Use Which Hook

### Use LLM Hooks When:

* Implementing iteration limits
* Adding context or safety guidelines to prompts
* Tracking token usage and costs
* Sanitizing or transforming responses
* Implementing approval gates for LLM calls
* Debugging prompt/response interactions

### Use Tool Hooks When:

* Blocking dangerous or destructive operations
* Validating tool inputs before execution
* Implementing approval gates for sensitive actions
* Caching tool results
* Tracking tool usage and performance
* Sanitizing tool outputs
* Rate limiting tool calls

### Use Both When:

Building comprehensive observability, safety, or approval systems that need to monitor all agent operations.

## Alternative Registration Methods

### Programmatic Registration (Advanced)

For dynamic hook registration or when you need to register hooks programmatically:
```

---

## ---

**URL:** llms-txt#---

**Contents:**
- Conclusion

By integrating the `SerperDevTool` into Python projects, users gain the ability to conduct real-time, relevant searches across the internet directly from their applications.
The updated parameters allow for more customized and localized search results. By adhering to the setup and usage guidelines provided, incorporating this tool into projects is streamlined and straightforward.

---

## __init__.py

**URL:** llms-txt#__init__.py

from .my_custom_listener import my_custom_listener
from .another_listener import another_listener

---
