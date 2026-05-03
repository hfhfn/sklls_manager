# Crewai - Tools

**Pages:** 206

---

## 3. Continue with available tools

**URL:** llms-txt#3.-continue-with-available-tools

---

## Additional API keys (optional)

**URL:** llms-txt#additional-api-keys-(optional)

**Contents:**
  - Complete Implementation
  - Running the Example
- Viewing Traces in LangDB
  - What You'll See
- Troubleshooting
  - Common Issues
- Resources
- Next Steps

export SERPER_API_KEY="<your_serper_api_key>"  # For web search capabilities
python theme={null}
#!/usr/bin/env python3

import os
import sys
from pylangdb.crewai import init
init()  # Initialize LangDB before any CrewAI imports
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool

def create_llm(model):
    return LLM(
        model=model,
        api_key=os.environ.get("LANGDB_API_KEY"),
        base_url=os.environ.get("LANGDB_API_BASE_URL"),
        extra_headers={"x-project-id": os.environ.get("LANGDB_PROJECT_ID")}
    )

class ResearchPlanningCrew:
    def researcher(self) -> Agent:
        return Agent(
            role="Research Specialist",
            goal="Research topics thoroughly and compile comprehensive information",
            backstory="Expert researcher with skills in finding and analyzing information from various sources",
            tools=[SerperDevTool()],
            llm=create_llm("openai/gpt-4o"),
            verbose=True
        )
    
    def planner(self) -> Agent:
        return Agent(
            role="Strategic Planner",
            goal="Create actionable plans based on research findings",
            backstory="Strategic planner who breaks down complex challenges into executable plans",
            reasoning=True,
            max_reasoning_attempts=3,
            llm=create_llm("openai/anthropic/claude-3.7-sonnet"),
            verbose=True
        )
    
    def research_task(self) -> Task:
        return Task(
            description="Research the topic thoroughly and compile comprehensive information",
            agent=self.researcher(),
            expected_output="Comprehensive research report with key findings and insights"
        )
    
    def planning_task(self) -> Task:
        return Task(
            description="Create a strategic plan based on the research findings",
            agent=self.planner(),
            expected_output="Strategic execution plan with phases, goals, and actionable steps",
            context=[self.research_task()]
        )
    
    def crew(self) -> Crew:
        return Crew(
            agents=[self.researcher(), self.planner()],
            tasks=[self.research_task(), self.planning_task()],
            verbose=True,
            process=Process.sequential
        )

def main():
        topic = sys.argv[1] if len(sys.argv) > 1 else "Artificial Intelligence in Healthcare"
        
        crew_instance = ResearchPlanningCrew()
        
        # Update task descriptions with the specific topic
        crew_instance.research_task().description = f"Research {topic} thoroughly and compile comprehensive information"
    crew_instance.planning_task().description = f"Create a strategic plan for {topic} based on the research findings"
    
    result = crew_instance.crew().kickoff()
    print(result)

if __name__ == "__main__":
    main()
bash theme={null}
python main.py "Sustainable Energy Solutions"
```

## Viewing Traces in LangDB

After running your CrewAI application, you can view detailed traces in the LangDB dashboard:

<Frame>
  <img alt="LangDB trace dashboard showing CrewAI workflow" />
</Frame>

* **Agent Interactions**: Complete flow of agent conversations and task handoffs
* **Tool Usage**: Which tools were called, their inputs, and outputs
* **Model Calls**: Detailed LLM interactions with prompts image.pngand responses
* **Performance Metrics**: Latency, token usage, and cost tracking
* **Execution Timeline**: Step-by-step view of the entire workflow

* **No traces appearing**: Ensure `init()` is called before any CrewAI imports
* **Authentication errors**: Verify your LangDB API key and project ID

<CardGroup>
  <Card title="LangDB Documentation" icon="book" href="https://docs.langdb.ai">
    Official LangDB documentation and guides
  </Card>

<Card title="LangDB Guides" icon="graduation-cap" href="https://docs.langdb.ai/guides">
    Step-by-step tutorials for building AI agents
  </Card>

<Card title="GitHub Examples" icon="github" href="https://github.com/langdb/langdb-samples/tree/main/examples/crewai">
    Complete CrewAI integration examples
  </Card>

<Card title="LangDB Dashboard" icon="chart-line" href="https://app.langdb.ai">
    Access your traces and analytics
  </Card>

<Card title="Model Catalog" icon="list" href="https://app.langdb.ai/models">
    Browse 350+ available language models
  </Card>

<Card title="Enterprise Features" icon="building" href="https://docs.langdb.ai/enterprise">
    Self-hosted options and enterprise capabilities
  </Card>
</CardGroup>

This guide covered the basics of integrating LangDB AI Gateway with CrewAI. To further enhance your AI workflows, explore:

* **Virtual Models**: Create custom model configurations with routing strategies
* **Guardrails & Safety**: Implement content filtering and compliance controls
* **Production Deployment**: Configure fallbacks, retries, and load balancing

For more advanced features and use cases, visit the [LangDB Documentation](https://docs.langdb.ai) or explore the [Model Catalog](https://app.langdb.ai/models) to discover all available models.

**Examples:**

Example 1 (unknown):
```unknown
### Complete Implementation
```

Example 2 (unknown):
```unknown
### Running the Example
```

---

## Add a directory of files

**URL:** llms-txt#add-a-directory-of-files

**Contents:**
- Agent Integration Example

rag_tool.add(data_type="directory", path="path/to/your/directory")
python Code theme={null}
from crewai import Agent
from crewai.project import agent
from crewai_tools import RagTool

**Examples:**

Example 1 (unknown):
```unknown
## Agent Integration Example

Here's how to integrate the `RagTool` with a CrewAI agent:
```

---

## `AIMindTool`

**URL:** llms-txt#`aimindtool`

**Contents:**
- Description
- Installation
- Steps to Get Started
- Example

The `AIMindTool` is a wrapper around [AI-Minds](https://mindsdb.com/minds) provided by [MindsDB](https://mindsdb.com/). It allows you to query data sources in natural language by simply configuring their connection parameters. This tool is useful when you need answers to questions from your data stored in various data sources including PostgreSQL, MySQL, MariaDB, ClickHouse, Snowflake, and Google BigQuery.

Minds are AI systems that work similarly to large language models (LLMs) but go beyond by answering any question from any data. This is accomplished by:

* Selecting the most relevant data for an answer using parametric search
* Understanding the meaning and providing responses within the correct context through semantic search
* Delivering precise answers by analyzing data and using machine learning (ML) models

To incorporate this tool into your project, you need to install the Minds SDK:

## Steps to Get Started

To effectively use the `AIMindTool`, follow these steps:

1. **Package Installation**: Confirm that the `crewai[tools]` and `minds-sdk` packages are installed in your Python environment.
2. **API Key Acquisition**: Sign up for a Minds account [here](https://mdb.ai/register), and obtain an API key.
3. **Environment Configuration**: Store your obtained API key in an environment variable named `MINDS_API_KEY` to facilitate its use by the tool.

The following example demonstrates how to initialize the tool and execute a query:

```python Code theme={null}
from crewai_tools import AIMindTool

**Examples:**

Example 1 (unknown):
```unknown
## Steps to Get Started

To effectively use the `AIMindTool`, follow these steps:

1. **Package Installation**: Confirm that the `crewai[tools]` and `minds-sdk` packages are installed in your Python environment.
2. **API Key Acquisition**: Sign up for a Minds account [here](https://mdb.ai/register), and obtain an API key.
3. **Environment Configuration**: Store your obtained API key in an environment variable named `MINDS_API_KEY` to facilitate its use by the tool.

## Example

The following example demonstrates how to initialize the tool and execute a query:
```

---

## AI Mind Tool

**URL:** llms-txt#ai-mind-tool

Source: https://docs.crewai.com/en/tools/ai-ml/aimindtool

The `AIMindTool` is designed to query data sources in natural language.

---

## and return the 3 most relevant results with scores > 0.35

**URL:** llms-txt#and-return-the-3-most-relevant-results-with-scores->-0.35

**Contents:**
- Complete Working Example

python theme={null}
import os
import uuid
import pdfplumber
from openai import OpenAI
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import QdrantVectorSearchTool
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams

**Examples:**

Example 1 (unknown):
```unknown
## Complete Working Example

Here's a complete example showing how to:

1. Extract text from a PDF
2. Generate embeddings using OpenAI
3. Store in Qdrant
4. Create a CrewAI agentic RAG workflow for semantic search
```

---

## `ApifyActorsTool`

**URL:** llms-txt#`apifyactorstool`

**Contents:**
- Description
- Steps to get started
- Usage example

Integrate [Apify Actors](https://apify.com/actors) into your CrewAI workflows.

The `ApifyActorsTool` connects [Apify Actors](https://apify.com/actors), cloud-based programs for web scraping and automation, to your CrewAI workflows.
Use any of the 4,000+ Actors on [Apify Store](https://apify.com/store) for use cases such as extracting data from social media, search engines, online maps, e-commerce sites, travel portals, or general websites.

For details, see the [Apify CrewAI integration](https://docs.apify.com/platform/integrations/crewai) in Apify documentation.

## Steps to get started

<Steps>
  <Step title="Install dependencies">
    Install `crewai[tools]` and `langchain-apify` using pip: `pip install 'crewai[tools]' langchain-apify`.
  </Step>

<Step title="Obtain an Apify API token">
    Sign up to [Apify Console](https://console.apify.com/) and get your [Apify API token](https://console.apify.com/settings/integrations)..
  </Step>

<Step title="Configure environment">
    Set your Apify API token as the `APIFY_API_TOKEN` environment variable to enable the tool's functionality.
  </Step>
</Steps>

Use the `ApifyActorsTool` manually to run the [RAG Web Browser Actor](https://apify.com/apify/rag-web-browser) to perform a web search:

```python theme={null}
from crewai_tools import ApifyActorsTool

---

## Apify Actors

**URL:** llms-txt#apify-actors

Source: https://docs.crewai.com/en/tools/automation/apifyactorstool

`ApifyActorsTool` lets you call Apify Actors to provide your CrewAI workflows with web scraping, crawling, data extraction, and web automation capabilities.

---

## `ArxivPaperTool`

**URL:** llms-txt#`arxivpapertool`

**Contents:**
- Description
- Installation
- Steps to Get Started
- Example
  - Direct usage (without Agent)
- Parameters
  - Initialization Parameters
  - Run Parameters
- Output format
- Usage Notes

The `ArxivPaperTool` queries the arXiv API for academic papers and returns compact, readable results. It can also optionally download PDFs to disk.

This tool has no special installation beyond `crewai-tools`.

No API key is required. This tool uses the public arXiv Atom API.

## Steps to Get Started

1. Initialize the tool.
2. Provide a `search_query` (e.g., "transformer neural network").
3. Optionally set `max_results` (1–100) and enable PDF downloads in the constructor.

### Direct usage (without Agent)

### Initialization Parameters

* `download_pdfs` (bool, default `False`): Whether to download PDFs.
* `save_dir` (str, default `./arxiv_pdfs`): Directory to save PDFs.
* `use_title_as_filename` (bool, default `False`): Use paper titles for filenames.

* `search_query` (str, required): The arXiv search query.
* `max_results` (int, default `5`, range 1–100): Number of results.

The tool returns a human‑readable list of papers with:

* Title
* Link (abs page)
* Snippet/summary (truncated)

When `download_pdfs=True`, PDFs are saved to disk and the summary mentions saved files.

* The tool returns formatted text with key metadata and links.
* When `download_pdfs=True`, PDFs will be stored in `save_dir`.

* If you receive a network timeout, re‑try or reduce `max_results`.
* Invalid XML errors indicate an arXiv response parse issue; try a simpler query.
* File system errors (e.g., permission denied) may occur when saving PDFs; ensure `save_dir` is writable.

* arXiv API docs: [https://info.arxiv.org/help/api/index.html](https://info.arxiv.org/help/api/index.html)

* Network issues, invalid XML, and OS errors are handled with informative messages.

**Examples:**

Example 1 (unknown):
```unknown
No API key is required. This tool uses the public arXiv Atom API.

## Steps to Get Started

1. Initialize the tool.
2. Provide a `search_query` (e.g., "transformer neural network").
3. Optionally set `max_results` (1–100) and enable PDF downloads in the constructor.

## Example
```

Example 2 (unknown):
```unknown
### Direct usage (without Agent)
```

---

## Arxiv Paper Tool

**URL:** llms-txt#arxiv-paper-tool

Source: https://docs.crewai.com/en/tools/search-research/arxivpapertool

The `ArxivPaperTool` searches arXiv for papers matching a query and optionally downloads PDFs.

---

## Assuming the tool's execution and result population occurs within the system

**URL:** llms-txt#assuming-the-tool's-execution-and-result-population-occurs-within-the-system

**Contents:**
- Workflow in Action

task_result = coding_agent.execute_task(task)
```

## Workflow in Action

<Steps>
  <Step title="Task Execution">
    The agent executes the task using the tool provided.
  </Step>

<Step title="Tool Output">
    The tool generates the output, which is captured as the task result.
  </Step>

<Step title="Agent Interaction">
    The agent may reflect and take learnings from the tool but the output is not modified.
  </Step>

<Step title="Result Return">
    The tool output is returned as the task result without any modifications.
  </Step>
</Steps>

---

## Bedrock Knowledge Base Retriever

**URL:** llms-txt#bedrock-knowledge-base-retriever

Source: https://docs.crewai.com/en/tools/cloud-storage/bedrockkbretriever

Retrieve information from Amazon Bedrock Knowledge Bases using natural language queries

---

## Better solution: Use RAG tools for large data

**URL:** llms-txt#better-solution:-use-rag-tools-for-large-data

from crewai_tools import RagTool
agent.tools = [RagTool()]

---

## `BraveSearchTool`

**URL:** llms-txt#`bravesearchtool`

**Contents:**
- Description
- Installation
- Steps to Get Started
- Example

This tool is designed to perform web searches using the Brave Search API. It allows you to search the internet with a specified query and retrieve relevant results. The tool supports customizable result counts and country-specific searches.

To incorporate this tool into your project, follow the installation instructions below:

## Steps to Get Started

To effectively use the `BraveSearchTool`, follow these steps:

1. **Package Installation**: Confirm that the `crewai[tools]` package is installed in your Python environment.
2. **API Key Acquisition**: Acquire a Brave Search API key at [https://api.search.brave.com/app/keys](https://api.search.brave.com/app/keys) (sign in to generate a key).
3. **Environment Configuration**: Store your obtained API key in an environment variable named `BRAVE_API_KEY` to facilitate its use by the tool.

The following example demonstrates how to initialize the tool and execute a search with a given query:

```python Code theme={null}
from crewai_tools import BraveSearchTool

**Examples:**

Example 1 (unknown):
```unknown
## Steps to Get Started

To effectively use the `BraveSearchTool`, follow these steps:

1. **Package Installation**: Confirm that the `crewai[tools]` package is installed in your Python environment.
2. **API Key Acquisition**: Acquire a Brave Search API key at [https://api.search.brave.com/app/keys](https://api.search.brave.com/app/keys) (sign in to generate a key).
3. **Environment Configuration**: Store your obtained API key in an environment variable named `BRAVE_API_KEY` to facilitate its use by the tool.

## Example

The following example demonstrates how to initialize the tool and execute a search with a given query:
```

---

## Brave Search

**URL:** llms-txt#brave-search

Source: https://docs.crewai.com/en/tools/search-research/bravesearchtool

The `BraveSearchTool` is designed to search the internet using the Brave Search API.

---

## Bright Data Tools

**URL:** llms-txt#bright-data-tools

**Contents:**
- Installation
- Environment Variables
- Included Tools
- Examples
  - SERP Search
  - Web Unlocker
  - Dataset API
- Troubleshooting
- Example

This set of tools integrates Bright Data services for web extraction.

## Environment Variables

* `BRIGHT_DATA_API_KEY` (required)
* `BRIGHT_DATA_ZONE` (for SERP/Web Unlocker)

Create credentials at [https://brightdata.com/](https://brightdata.com/) (sign up, then create an API token and zone).
See their docs: [https://developers.brightdata.com/](https://developers.brightdata.com/)

* `BrightDataSearchTool`: SERP search (Google/Bing/Yandex) with geo/language/device options.
* `BrightDataWebUnlockerTool`: Scrape pages with anti-bot bypass and rendering.
* `BrightDataDatasetTool`: Run Dataset API jobs and fetch results.

* 401/403: verify `BRIGHT_DATA_API_KEY` and `BRIGHT_DATA_ZONE`.
* Empty/blocked content: enable rendering or try a different zone.

**Examples:**

Example 1 (unknown):
```unknown
## Environment Variables

* `BRIGHT_DATA_API_KEY` (required)
* `BRIGHT_DATA_ZONE` (for SERP/Web Unlocker)

Create credentials at [https://brightdata.com/](https://brightdata.com/) (sign up, then create an API token and zone).
See their docs: [https://developers.brightdata.com/](https://developers.brightdata.com/)

## Included Tools

* `BrightDataSearchTool`: SERP search (Google/Bing/Yandex) with geo/language/device options.
* `BrightDataWebUnlockerTool`: Scrape pages with anti-bot bypass and rendering.
* `BrightDataDatasetTool`: Run Dataset API jobs and fetch results.

## Examples

### SERP Search
```

Example 2 (unknown):
```unknown
### Web Unlocker
```

Example 3 (unknown):
```unknown
### Dataset API
```

Example 4 (unknown):
```unknown
## Troubleshooting

* 401/403: verify `BRIGHT_DATA_API_KEY` and `BRIGHT_DATA_ZONE`.
* Empty/blocked content: enable rendering or try a different zone.

## Example
```

---

## `BrowserbaseLoadTool`

**URL:** llms-txt#`browserbaseloadtool`

**Contents:**
- Description
- Installation
- Example

[Browserbase](https://browserbase.com) is a developer platform to reliably run, manage, and monitor headless browsers.

Power your AI data retrievals with:

* [Serverless Infrastructure](https://docs.browserbase.com/under-the-hood) providing reliable browsers to extract data from complex UIs
* [Stealth Mode](https://docs.browserbase.com/features/stealth-mode) with included fingerprinting tactics and automatic captcha solving
* [Session Debugger](https://docs.browserbase.com/features/sessions) to inspect your Browser Session with networks timeline and logs
* [Live Debug](https://docs.browserbase.com/guides/session-debug-connection/browser-remote-control) to quickly debug your automation

* Get an API key and Project ID from [browserbase.com](https://browserbase.com) and set it in environment variables (`BROWSERBASE_API_KEY`, `BROWSERBASE_PROJECT_ID`).
* Install the [Browserbase SDK](http://github.com/browserbase/python-sdk) along with `crewai[tools]` package:

Utilize the BrowserbaseLoadTool as follows to allow your agent to load websites:

```python Code theme={null}
from crewai_tools import BrowserbaseLoadTool

**Examples:**

Example 1 (unknown):
```unknown
## Example

Utilize the BrowserbaseLoadTool as follows to allow your agent to load websites:
```

---

## Browserbase Web Loader

**URL:** llms-txt#browserbase-web-loader

Source: https://docs.crewai.com/en/tools/web-scraping/browserbaseloadtool

Browserbase is a developer platform to reliably run, manage, and monitor headless browsers.

---

## Clear all tool hooks

**URL:** llms-txt#clear-all-tool-hooks

**Contents:**
  - Listing Registered Hooks

before_count, after_count = clear_all_tool_call_hooks()
print(f"Cleared {before_count} before and {after_count} after hooks")
python theme={null}
from crewai.hooks import (
    get_before_tool_call_hooks,
    get_after_tool_call_hooks
)

**Examples:**

Example 1 (unknown):
```unknown
### Listing Registered Hooks
```

---

## `CodeDocsSearchTool`

**URL:** llms-txt#`codedocssearchtool`

**Contents:**
- Description
- Installation
- Example

<Note>
  **Experimental**: We are still working on improving tools, so there might be unexpected behavior or changes in the future.
</Note>

The CodeDocsSearchTool is a powerful RAG (Retrieval-Augmented Generation) tool designed for semantic searches within code documentation.
It enables users to efficiently find specific information or topics within code documentation. By providing a `docs_url` during initialization,
the tool narrows down the search to that particular documentation site. Alternatively, without a specific `docs_url`,
it searches across a wide array of code documentation known or discovered throughout its execution, making it versatile for various documentation search needs.

To start using the CodeDocsSearchTool, first, install the crewai\_tools package via pip:

Utilize the CodeDocsSearchTool as follows to conduct searches within code documentation:

```python Code theme={null}
from crewai_tools import CodeDocsSearchTool

**Examples:**

Example 1 (unknown):
```unknown
## Example

Utilize the CodeDocsSearchTool as follows to conduct searches within code documentation:
```

---

## Code Docs RAG Search

**URL:** llms-txt#code-docs-rag-search

Source: https://docs.crewai.com/en/tools/search-research/codedocssearchtool

The `CodeDocsSearchTool` is a powerful RAG (Retrieval-Augmented Generation) tool designed for semantic searches within code documentation.

---

## Code Interpreter

**URL:** llms-txt#code-interpreter

Source: https://docs.crewai.com/en/tools/ai-ml/codeinterpretertool

The `CodeInterpreterTool` is a powerful tool designed for executing Python 3 code within a secure, isolated environment.

---

## Configure the tool with custom parameters

**URL:** llms-txt#configure-the-tool-with-custom-parameters

**Contents:**
  - Tool Parameters

custom_extractor = TavilyExtractorTool(
    extract_depth='advanced',
    include_images=True,
    timeout=120
)

agent_with_custom_tool = Agent(
    role="Advanced Content Extractor",
    goal="Extract comprehensive content with images",
    tools=[custom_extractor]
)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### Tool Parameters

You can customize the tool's behavior by setting parameters during initialization:
```

---

## Create AI tools

**URL:** llms-txt#create-ai-tools

image_generator = DallETool()
vision_processor = VisionTool()
code_executor = CodeInterpreterTool()

---

## Create automation tools

**URL:** llms-txt#create-automation-tools

apify_automation = ApifyActorTool()
platform_integration = ComposioTool()
browser_automation = MultiOnTool()

---

## Create a LlamaIndexTool from the query engine

**URL:** llms-txt#create-a-llamaindextool-from-the-query-engine

**Contents:**
- Class Methods
  - from\_tool
  - from\_query\_engine
- Parameters
- Conclusion

query_tool = LlamaIndexTool.from_query_engine(
    query_engine,
    name="Company Data Query Tool",
    description="Use this tool to lookup information in company documents"
)
python Code theme={null}
@classmethod
def from_tool(cls, tool: Any, **kwargs: Any) -> "LlamaIndexTool":
    # Implementation details
python Code theme={null}
@classmethod
def from_query_engine(
    cls,
    query_engine: Any,
    name: Optional[str] = None,
    description: Optional[str] = None,
    return_direct: bool = False,
    **kwargs: Any,
) -> "LlamaIndexTool":
    # Implementation details
```

The `from_query_engine` method accepts the following parameters:

* **query\_engine**: Required. The LlamaIndex query engine to wrap.
* **name**: Optional. The name of the tool.
* **description**: Optional. The description of the tool.
* **return\_direct**: Optional. Whether to return the response directly. Default is `False`.

The `LlamaIndexTool` provides a powerful way to integrate LlamaIndex's capabilities into CrewAI agents. By wrapping LlamaIndex tools and query engines, it enables agents to leverage sophisticated data retrieval and processing functionalities, enhancing their ability to work with complex information sources.

**Examples:**

Example 1 (unknown):
```unknown
## Class Methods

The `LlamaIndexTool` provides two main class methods for creating instances:

### from\_tool

Creates a `LlamaIndexTool` from a LlamaIndex tool.
```

Example 2 (unknown):
```unknown
### from\_query\_engine

Creates a `LlamaIndexTool` from a LlamaIndex query engine.
```

---

## Create a LlamaIndex FunctionTool

**URL:** llms-txt#create-a-llamaindex-functiontool

og_tool = FunctionTool.from_defaults(
    search_data, 
    name="DataSearchTool",
    description="Search for information in the data"
)

---

## Create a RAG tool with custom configuration

**URL:** llms-txt#create-a-rag-tool-with-custom-configuration

**Contents:**
- Embedding Model Configuration
  - Supported Providers
  - Notes
- Conclusion

vectordb: VectorDbConfig = {
    "provider": "qdrant",
    "config": {
        "collection_name": "my-collection"
    }
}

embedding_model: ProviderSpec = {
    "provider": "openai",
    "config": {
        "model_name": "text-embedding-3-small"
    }
}

config: RagToolConfig = {
    "vectordb": vectordb,
    "embedding_model": embedding_model
}

rag_tool = RagTool(config=config, summarize=True)
python theme={null}
{
    "provider": "provider-name",  # Required
    "config": {                    # Optional
        # Provider-specific configuration
    }
}
python main.py theme={null}
    from crewai.rag.embeddings.providers.openai.types import OpenAIProviderSpec

embedding_model: OpenAIProviderSpec = {
        "provider": "openai",
        "config": {
            "api_key": "your-api-key",
            "model_name": "text-embedding-ada-002",
            "dimensions": 1536,
            "organization_id": "your-org-id",
            "api_base": "https://api.openai.com/v1",
            "api_version": "v1",
            "default_headers": {"Custom-Header": "value"}
        }
    }
    python main.py theme={null}
    from crewai.rag.embeddings.providers.cohere.types import CohereProviderSpec

embedding_model: CohereProviderSpec = {
        "provider": "cohere",
        "config": {
            "api_key": "your-api-key",
            "model_name": "embed-english-v3.0"
        }
    }
    python main.py theme={null}
    from crewai.rag.embeddings.providers.voyageai.types import VoyageAIProviderSpec

embedding_model: VoyageAIProviderSpec = {
        "provider": "voyageai",
        "config": {
            "api_key": "your-api-key",
            "model": "voyage-3",
            "input_type": "document",
            "truncation": True,
            "output_dtype": "float32",
            "output_dimension": 1024,
            "max_retries": 3,
            "timeout": 60.0
        }
    }
    python main.py theme={null}
    from crewai.rag.embeddings.providers.ollama.types import OllamaProviderSpec

embedding_model: OllamaProviderSpec = {
        "provider": "ollama",
        "config": {
            "model_name": "llama2",
            "url": "http://localhost:11434/api/embeddings"
        }
    }
    python main.py theme={null}
    from crewai.rag.embeddings.providers.aws.types import BedrockProviderSpec

embedding_model: BedrockProviderSpec = {
        "provider": "amazon-bedrock",
        "config": {
            "model_name": "amazon.titan-embed-text-v2:0",
            "session": boto3_session
        }
    }
    python main.py theme={null}
    from crewai.rag.embeddings.providers.microsoft.types import AzureProviderSpec

embedding_model: AzureProviderSpec = {
        "provider": "azure",
        "config": {
            "deployment_id": "your-deployment-id",
            "api_key": "your-api-key",
            "api_base": "https://your-resource.openai.azure.com",
            "api_version": "2024-02-01",
            "model_name": "text-embedding-ada-002",
            "api_type": "azure"
        }
    }
    python main.py theme={null}
    from crewai.rag.embeddings.providers.google.types import GenerativeAiProviderSpec

embedding_model: GenerativeAiProviderSpec = {
        "provider": "google-generativeai",
        "config": {
            "api_key": "your-api-key",
            "model_name": "gemini-embedding-001",
            "task_type": "RETRIEVAL_DOCUMENT"
        }
    }
    python main.py theme={null}
    from crewai.rag.embeddings.providers.google.types import VertexAIProviderSpec

embedding_model: VertexAIProviderSpec = {
        "provider": "google-vertex",
        "config": {
            "model_name": "text-embedding-004",
            "project_id": "your-project-id",
            "region": "us-central1",
            "api_key": "your-api-key"
        }
    }
    python main.py theme={null}
    from crewai.rag.embeddings.providers.jina.types import JinaProviderSpec

embedding_model: JinaProviderSpec = {
        "provider": "jina",
        "config": {
            "api_key": "your-api-key",
            "model_name": "jina-embeddings-v3"
        }
    }
    python main.py theme={null}
    from crewai.rag.embeddings.providers.huggingface.types import HuggingFaceProviderSpec

embedding_model: HuggingFaceProviderSpec = {
        "provider": "huggingface",
        "config": {
            "url": "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
        }
    }
    python main.py theme={null}
    from crewai.rag.embeddings.providers.instructor.types import InstructorProviderSpec

embedding_model: InstructorProviderSpec = {
        "provider": "instructor",
        "config": {
            "model_name": "hkunlp/instructor-xl",
            "device": "cuda",
            "instruction": "Represent the document"
        }
    }
    python main.py theme={null}
    from crewai.rag.embeddings.providers.sentence_transformer.types import SentenceTransformerProviderSpec

embedding_model: SentenceTransformerProviderSpec = {
        "provider": "sentence-transformer",
        "config": {
            "model_name": "all-mpnet-base-v2",
            "device": "cuda",
            "normalize_embeddings": True
        }
    }
    python main.py theme={null}
    from crewai.rag.embeddings.providers.onnx.types import ONNXProviderSpec

embedding_model: ONNXProviderSpec = {
        "provider": "onnx",
        "config": {
            "preferred_providers": ["CUDAExecutionProvider", "CPUExecutionProvider"]
        }
    }
    python main.py theme={null}
    from crewai.rag.embeddings.providers.openclip.types import OpenCLIPProviderSpec

embedding_model: OpenCLIPProviderSpec = {
        "provider": "openclip",
        "config": {
            "model_name": "ViT-B-32",
            "checkpoint": "laion2b_s34b_b79k",
            "device": "cuda"
        }
    }
    python main.py theme={null}
    from crewai.rag.embeddings.providers.text2vec.types import Text2VecProviderSpec

embedding_model: Text2VecProviderSpec = {
        "provider": "text2vec",
        "config": {
            "model_name": "shibing624/text2vec-base-multilingual"
        }
    }
    python main.py theme={null}
    from crewai.rag.embeddings.providers.roboflow.types import RoboflowProviderSpec

embedding_model: RoboflowProviderSpec = {
        "provider": "roboflow",
        "config": {
            "api_key": "your-api-key",
            "api_url": "https://infer.roboflow.com"
        }
    }
    python main.py theme={null}
    from crewai.rag.embeddings.providers.ibm.types import WatsonXProviderSpec

embedding_model: WatsonXProviderSpec = {
        "provider": "watsonx",
        "config": {
            "model_id": "ibm/slate-125m-english-rtrvr",
            "url": "https://us-south.ml.cloud.ibm.com",
            "api_key": "your-api-key",
            "project_id": "your-project-id",
            "batch_size": 100,
            "concurrency_limit": 10,
            "persistent_connection": True
        }
    }
    python main.py theme={null}
    from crewai.rag.core.base_embeddings_callable import EmbeddingFunction
    from crewai.rag.embeddings.providers.custom.types import CustomProviderSpec

class MyEmbeddingFunction(EmbeddingFunction):
        def __call__(self, input):
            # Your custom embedding logic
            return embeddings

embedding_model: CustomProviderSpec = {
        "provider": "custom",
        "config": {
            "embedding_callable": MyEmbeddingFunction
        }
    }
    ```

* `embedding_callable` (type\[EmbeddingFunction]): Custom embedding function class

**Note:** Custom embedding functions must implement the `EmbeddingFunction` protocol defined in `crewai.rag.core.base_embeddings_callable`. The `__call__` method should accept input data and return embeddings as a list of numpy arrays (or compatible format that will be normalized). The returned embeddings are automatically normalized and validated.
  </Accordion>
</AccordionGroup>

* All config fields are optional unless marked as **Required**
* API keys can typically be provided via environment variables instead of config
* Default values are shown where applicable

The `RagTool` provides a powerful way to create and query knowledge bases from various data sources. By leveraging Retrieval-Augmented Generation, it enables agents to access and retrieve relevant information efficiently, enhancing their ability to provide accurate and contextually appropriate responses.

**Examples:**

Example 1 (unknown):
```unknown
## Embedding Model Configuration

The `embedding_model` parameter accepts a `crewai.rag.embeddings.types.ProviderSpec` dictionary with the structure:
```

Example 2 (unknown):
```unknown
### Supported Providers

<AccordionGroup>
  <Accordion title="OpenAI">
```

Example 3 (unknown):
```unknown
**Config Options:**

    * `api_key` (str): OpenAI API key
    * `model_name` (str): Model to use. Default: `text-embedding-ada-002`. Options: `text-embedding-3-small`, `text-embedding-3-large`, `text-embedding-ada-002`
    * `dimensions` (int): Number of dimensions for the embedding
    * `organization_id` (str): OpenAI organization ID
    * `api_base` (str): Custom API base URL
    * `api_version` (str): API version
    * `default_headers` (dict): Custom headers for API requests

    **Environment Variables:**

    * `OPENAI_API_KEY` or `EMBEDDINGS_OPENAI_API_KEY`: `api_key`
    * `OPENAI_ORGANIZATION_ID` or `EMBEDDINGS_OPENAI_ORGANIZATION_ID`: `organization_id`
    * `OPENAI_MODEL_NAME` or `EMBEDDINGS_OPENAI_MODEL_NAME`: `model_name`
    * `OPENAI_API_BASE` or `EMBEDDINGS_OPENAI_API_BASE`: `api_base`
    * `OPENAI_API_VERSION` or `EMBEDDINGS_OPENAI_API_VERSION`: `api_version`
    * `OPENAI_DIMENSIONS` or `EMBEDDINGS_OPENAI_DIMENSIONS`: `dimensions`
  </Accordion>

  <Accordion title="Cohere">
```

Example 4 (unknown):
```unknown
**Config Options:**

    * `api_key` (str): Cohere API key
    * `model_name` (str): Model to use. Default: `large`. Options: `embed-english-v3.0`, `embed-multilingual-v3.0`, `large`, `small`

    **Environment Variables:**

    * `COHERE_API_KEY` or `EMBEDDINGS_COHERE_API_KEY`: `api_key`
    * `EMBEDDINGS_COHERE_MODEL_NAME`: `model_name`
  </Accordion>

  <Accordion title="VoyageAI">
```

---

## Create a RAG tool with default settings

**URL:** llms-txt#create-a-rag-tool-with-default-settings

---

## Create a StdioServerParameters object

**URL:** llms-txt#create-a-stdioserverparameters-object

stdio_params=StdioServerParameters(
    command="python3", 
    args=["servers/your_stdio_server.py"],
    env={"UV_PYTHON": "3.12", **os.environ},
)

mcp_server_adapter = MCPServerAdapter(server_params=stdio_params)
try:
    mcp_server_adapter.start()  # Manually start the connection and server process
    tools = mcp_server_adapter.tools
    print(f"Available tools (manual Stdio): {[tool.name for tool in tools]}")

# Example: Using the tools with your Agent, Task, Crew setup
    manual_agent = Agent(
        role="Local Task Executor",
        goal="Execute a specific local task using a manually managed Stdio tool.",
        backstory="An AI proficient in controlling local processes via MCP.",
        tools=tools,
        verbose=True
    )
    
    manual_task = Task(
        description="Execute the 'perform_analysis' command via the Stdio tool.",
        expected_output="Results of the analysis.",
        agent=manual_agent
    )
    
    manual_crew = Crew(
        agents=[manual_agent],
        tasks=[manual_task],
        verbose=True,
        process=Process.sequential
    )
        
       
    result = manual_crew.kickoff() # Actual inputs depend on your tool
    print("\nCrew Task Result (Stdio - Manual):\n", result)
            
except Exception as e:
    print(f"An error occurred during manual Stdio MCP integration: {e}")
finally:
    if mcp_server_adapter and mcp_server_adapter.is_connected: # Check if connected before stopping
        print("Stopping Stdio MCP server connection (manual)...")
        mcp_server_adapter.stop()  # **Crucial: Ensure stop is called**
    elif mcp_server_adapter: # If adapter exists but not connected (e.g. start failed)
        print("Stdio MCP server adapter was not connected. No stop needed or start failed.")

Remember to replace placeholder paths and commands with your actual Stdio server details. The `env` parameter in `StdioServerParameters` can
be used to set environment variables for the server process, which can be useful for configuring its behavior or providing necessary paths (like `PYTHONPATH`).

---

## Create a tool for Linear issue creation

**URL:** llms-txt#create-a-tool-for-linear-issue-creation

linear_create_tool = MergeAgentHandlerTool.from_tool_name(
    tool_name="linear__create_issue",
    tool_pack_id="134e0111-0f67-44f6-98f0-597000290bb3",
    registered_user_id="91b2b905-e866-40c8-8be2-efe53827a0aa"
)

---

## Create cloud tools

**URL:** llms-txt#create-cloud-tools

s3_reader = S3ReaderTool()
s3_writer = S3WriterTool()
bedrock_agent = BedrockInvokeAgentTool()

---

## Create Custom Tools

**URL:** llms-txt#create-custom-tools

**Contents:**
- Creating and Utilizing Tools in CrewAI
  - Subclassing `BaseTool`
  - Using the `tool` Decorator
  - Defining a Cache Function for the Tool
  - Creating Async Tools

Source: https://docs.crewai.com/en/learn/create-custom-tools

Comprehensive guide on crafting, using, and managing custom tools within the CrewAI framework, including new functionalities and error handling.

## Creating and Utilizing Tools in CrewAI

This guide provides detailed instructions on creating custom tools for the CrewAI framework and how to efficiently manage and utilize these tools,
incorporating the latest functionalities such as tool delegation, error handling, and dynamic tool calling. It also highlights the importance of collaboration tools,
enabling agents to perform a wide range of actions.

### Subclassing `BaseTool`

To create a personalized tool, inherit from `BaseTool` and define the necessary attributes, including the `args_schema` for input validation, and the `_run` method.

### Using the `tool` Decorator

Alternatively, you can use the tool decorator `@tool`. This approach allows you to define the tool's attributes and functionality directly within a function,
offering a concise and efficient way to create specialized tools tailored to your needs.

### Defining a Cache Function for the Tool

To optimize tool performance with caching, define custom caching strategies using the `cache_function` attribute.

### Creating Async Tools

CrewAI supports async tools for non-blocking I/O operations. This is useful when your tool needs to make HTTP requests, database queries, or other I/O-bound operations.

#### Using the `@tool` Decorator with Async Functions

The simplest way to create an async tool is using the `@tool` decorator with an async function:

#### Subclassing `BaseTool` with Async Support

For more control, subclass `BaseTool` and implement both `_run` (sync) and `_arun` (async) methods:

By adhering to these guidelines and incorporating new functionalities and collaboration tools into your tool creation and management processes,
you can leverage the full capabilities of the CrewAI framework, enhancing both the development experience and the efficiency of your AI agents.

**Examples:**

Example 1 (unknown):
```unknown
### Using the `tool` Decorator

Alternatively, you can use the tool decorator `@tool`. This approach allows you to define the tool's attributes and functionality directly within a function,
offering a concise and efficient way to create specialized tools tailored to your needs.
```

Example 2 (unknown):
```unknown
### Defining a Cache Function for the Tool

To optimize tool performance with caching, define custom caching strategies using the `cache_function` attribute.
```

Example 3 (unknown):
```unknown
### Creating Async Tools

CrewAI supports async tools for non-blocking I/O operations. This is useful when your tool needs to make HTTP requests, database queries, or other I/O-bound operations.

#### Using the `@tool` Decorator with Async Functions

The simplest way to create an async tool is using the `@tool` decorator with an async function:
```

Example 4 (unknown):
```unknown
#### Subclassing `BaseTool` with Async Support

For more control, subclass `BaseTool` and implement both `_run` (sync) and `_arun` (async) methods:
```

---

## Create database tools

**URL:** llms-txt#create-database-tools

mysql_db = MySQLTool()
vector_search = QdrantVectorSearchTool()
nl_to_sql = NL2SQLTool()

---

## Create RAG tool for large document processing

**URL:** llms-txt#create-rag-tool-for-large-document-processing

rag_agent = Agent(
    role="Research Assistant",
    goal="Query large knowledge bases efficiently",
    backstory="Expert at using RAG tools for information retrieval",
    tools=[rag_tool],  # Use RAG instead of large context windows
    respect_context_window=True,
    verbose=True
)
python Code theme={null}

**Examples:**

Example 1 (unknown):
```unknown
#### 2. Use Knowledge Sources
```

---

## Create research tools

**URL:** llms-txt#create-research-tools

web_search = SerperDevTool()
code_search = GitHubSearchTool()
video_research = YoutubeVideoSearchTool()
tavily_search = TavilySearchTool()
content_extractor = TavilyExtractorTool()

---

## Create scraping tools

**URL:** llms-txt#create-scraping-tools

simple_scraper = ScrapeWebsiteTool()
advanced_scraper = FirecrawlScrapeWebsiteTool()
browser_automation = SeleniumScrapingTool()

---

## Create the Atlas Vector Search index (e.g., 3072 dims for text-embedding-3-large)

**URL:** llms-txt#create-the-atlas-vector-search-index-(e.g.,-3072-dims-for-text-embedding-3-large)

**Contents:**
- Example

tool.create_vector_search_index(dimensions=3072)
python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import MongoDBVectorSearchTool

tool = MongoDBVectorSearchTool(
    connection_string="mongodb+srv://...",
    database_name="mydb",
    collection_name="docs",
)

agent = Agent(
    role="RAG Agent",
    goal="Answer using MongoDB vector search",
    backstory="Knowledge retrieval specialist",
    tools=[tool],
    verbose=True,
)

task = Task(
    description="Find relevant content for 'indexing guidance'",
    expected_output="A concise answer citing the most relevant matches",
    agent=agent,
)

crew = Crew(
    agents=[agent], 
    tasks=[task],
    verbose=True,
)

result = crew.kickoff()
```

**Examples:**

Example 1 (unknown):
```unknown
## Example
```

---

## Create the prompt generator

**URL:** llms-txt#create-the-prompt-generator

prompt_generator = Prompts(
    agent=agent,
    has_tools=len(agent.tools) > 0,
    use_system_prompt=agent.use_system_prompt
)

---

## Create tools

**URL:** llms-txt#create-tools

file_reader = FileReadTool()
pdf_searcher = PDFSearchTool()
json_processor = JSONSearchTool()

---

## Create tools with the same session ID to maintain context

**URL:** llms-txt#create-tools-with-the-same-session-id-to-maintain-context

**Contents:**
- Use Cases
  - Unified Integration Access
  - Secure Enterprise Workflows
  - Cross-Platform Automation
  - Dynamic Tool Discovery
  - User-Specific Tool Access
- Available Integrations
- Error Handling

session_id = "project-sprint-planning-2024"

create_tool = MergeAgentHandlerTool(
    name="linear_create_issue",
    description="Creates a new issue in Linear",
    tool_name="linear__create_issue",
    tool_pack_id="134e0111-0f67-44f6-98f0-597000290bb3",
    registered_user_id="91b2b905-e866-40c8-8be2-efe53827a0aa",
    session_id=session_id
)

update_tool = MergeAgentHandlerTool(
    name="linear_update_issue",
    description="Updates an existing issue in Linear",
    tool_name="linear__update_issue",
    tool_pack_id="134e0111-0f67-44f6-98f0-597000290bb3",
    registered_user_id="91b2b905-e866-40c8-8be2-efe53827a0aa",
    session_id=session_id
)

sprint_planner = Agent(
    role='Sprint Planner',
    goal='Plan and organize sprint tasks',
    backstory='I help teams plan effective sprints with well-defined tasks.',
    tools=[create_tool, update_tool],
    verbose=True
)

planning_task = Task(
    description="Create 5 sprint tasks for the authentication feature and set their priorities based on dependencies.",
    agent=sprint_planner
)

crew = Crew(
    agents=[sprint_planner],
    tasks=[planning_task],
    verbose=True
)

result = crew.kickoff()
```

### Unified Integration Access

* Access hundreds of third-party tools through a single unified API without managing multiple SDKs
* Enable agents to work with Linear, GitHub, Slack, Notion, Jira, Asana, and more from one integration point
* Reduce integration complexity by letting Agent Handler manage authentication and API versioning

### Secure Enterprise Workflows

* Leverage built-in authentication and permission management for all third-party integrations
* Maintain enterprise security standards with centralized access control and audit logging
* Enable agents to access company tools without exposing API keys or credentials in code

### Cross-Platform Automation

* Build workflows that span multiple platforms (e.g., create GitHub issues from Linear tasks, sync Notion pages to Slack)
* Enable seamless data flow between different tools in your tech stack
* Create intelligent automation that understands context across different platforms

### Dynamic Tool Discovery

* Load all available tools at runtime without hardcoding integration logic
* Enable agents to discover and use new tools as they're added to your Tool Pack
* Build flexible agents that can adapt to changing tool availability

### User-Specific Tool Access

* Different users can have different tool permissions and access levels
* Enable multi-tenant workflows where agents act on behalf of specific users
* Maintain proper attribution and permissions for all tool actions

## Available Integrations

Merge Agent Handler supports hundreds of integrations across multiple categories:

* **Project Management**: Linear, Jira, Asana, Monday.com, ClickUp
* **Code Management**: GitHub, GitLab, Bitbucket
* **Communication**: Slack, Microsoft Teams, Discord
* **Documentation**: Notion, Confluence, Google Docs
* **CRM**: Salesforce, HubSpot, Pipedrive
* **And many more...**

Visit the [Merge Agent Handler documentation](https://docs.ah.merge.dev/) for a complete list of available integrations.

The tool provides comprehensive error handling:

* **Authentication Errors**: Invalid or missing API keys
* **Permission Errors**: User lacks permission for the requested action
* **API Errors**: Issues communicating with Agent Handler or third-party services
* **Validation Errors**: Invalid parameters passed to tool methods

All errors are wrapped in `MergeAgentHandlerToolError` for consistent error handling.

---

## Create tool with custom inputs

**URL:** llms-txt#create-tool-with-custom-inputs

market_research_tool = InvokeCrewAIAutomationTool(
    crew_api_url="https://state-of-ai-report-crew-[...].crewai.com",
    crew_bearer_token="your_bearer_token_here",
    crew_name="State of AI Report",
    crew_description="Retrieves a comprehensive report on state of AI for a given year and region",
    crew_inputs=custom_inputs,
    max_polling_time=15 * 60  # 15 minutes timeout
)

---

## `CSVSearchTool`

**URL:** llms-txt#`csvsearchtool`

**Contents:**
- Description
- Installation
- Example

<Note>
  **Experimental**: We are still working on improving tools, so there might be unexpected behavior or changes in the future.
</Note>

This tool is used to perform a RAG (Retrieval-Augmented Generation) search within a CSV file's content. It allows users to semantically search for queries in the content of a specified CSV file.
This feature is particularly useful for extracting information from large CSV datasets where traditional search methods might be inefficient. All tools with "Search" in their name, including CSVSearchTool,
are RAG tools designed for searching different sources of data.

Install the crewai\_tools package

```python Code theme={null}
from crewai_tools import CSVSearchTool

**Examples:**

Example 1 (unknown):
```unknown
## Example
```

---

## CSV RAG Search

**URL:** llms-txt#csv-rag-search

Source: https://docs.crewai.com/en/tools/file-document/csvsearchtool

The `CSVSearchTool` is a powerful RAG (Retrieval-Augmented Generation) tool designed for semantic searches within a CSV file's content.

---

## `DallETool`

**URL:** llms-txt#`dalletool`

**Contents:**
- Description
- Installation
- Example

This tool is used to give the Agent the ability to generate images using the DALL-E model. It is a transformer-based model that generates images from textual descriptions.
This tool allows the Agent to generate images based on the text input provided by the user.

Install the crewai\_tools package

Remember that when using this tool, the text must be generated by the Agent itself. The text must be a description of the image you want to generate.

If needed you can also tweak the parameters of the DALL-E model by passing them as arguments to the `DallETool` class. For example:

The parameters are based on the `client.images.generate` method from the OpenAI API. For more information on the parameters,
please refer to the [OpenAI API documentation](https://platform.openai.com/docs/guides/images/introduction?lang=python).

**Examples:**

Example 1 (unknown):
```unknown
## Example

Remember that when using this tool, the text must be generated by the Agent itself. The text must be a description of the image you want to generate.
```

Example 2 (unknown):
```unknown
If needed you can also tweak the parameters of the DALL-E model by passing them as arguments to the `DallETool` class. For example:
```

---

## DALL-E Tool

**URL:** llms-txt#dall-e-tool

Source: https://docs.crewai.com/en/tools/ai-ml/dalletool

The `DallETool` is a powerful tool designed for generating images from textual descriptions.

---

## `DatabricksQueryTool`

**URL:** llms-txt#`databricksquerytool`

**Contents:**
- Description
- Installation
- Environment Variables
- Example
- Parameters
- Defaults on initialization
  - Error handling & tips

Run SQL against Databricks workspace tables with either CLI profile or direct host/token authentication.

## Environment Variables

* `DATABRICKS_CONFIG_PROFILE` or (`DATABRICKS_HOST` + `DATABRICKS_TOKEN`)

Create a personal access token and find host details in the Databricks workspace under User Settings → Developer.
Docs: [https://docs.databricks.com/en/dev-tools/auth/pat.html](https://docs.databricks.com/en/dev-tools/auth/pat.html)

* `query` (required): SQL query to execute
* `catalog` (optional): Override default catalog
* `db_schema` (optional): Override default schema
* `warehouse_id` (optional): Override default SQL warehouse
* `row_limit` (optional): Maximum rows to return (default: 1000)

## Defaults on initialization

* `default_catalog`
* `default_schema`
* `default_warehouse_id`

### Error handling & tips

* Authentication errors: verify `DATABRICKS_HOST` begins with `https://` and token is valid.
* Permissions: ensure your SQL warehouse and schema are accessible by your token.
* Limits: long‑running queries should be avoided in agent loops; add filters/limits.

**Examples:**

Example 1 (unknown):
```unknown
## Environment Variables

* `DATABRICKS_CONFIG_PROFILE` or (`DATABRICKS_HOST` + `DATABRICKS_TOKEN`)

Create a personal access token and find host details in the Databricks workspace under User Settings → Developer.
Docs: [https://docs.databricks.com/en/dev-tools/auth/pat.html](https://docs.databricks.com/en/dev-tools/auth/pat.html)

## Example
```

---

## Databricks SQL Query Tool

**URL:** llms-txt#databricks-sql-query-tool

Source: https://docs.crewai.com/en/tools/search-research/databricks-query-tool

The `DatabricksQueryTool` executes SQL queries against Databricks workspace tables.

---

## Define parameters for multiple MCP servers

**URL:** llms-txt#define-parameters-for-multiple-mcp-servers

**Contents:**
- Connection Management

server_params_list = [
    # Streamable HTTP Server
    {
        "url": "http://localhost:8001/mcp", 
        "transport": "streamable-http"
    },
    # SSE Server
    {
        "url": "http://localhost:8000/sse",
        "transport": "sse"
    },
    # StdIO Server
    StdioServerParameters(
        command="python3",
        args=["servers/your_stdio_server.py"],
        env={"UV_PYTHON": "3.12", **os.environ},
    )
]

try:
    with MCPServerAdapter(server_params_list) as aggregated_tools:
        print(f"Available aggregated tools: {[tool.name for tool in aggregated_tools]}")

multi_server_agent = Agent(
            role="Versatile Assistant",
            goal="Utilize tools from local Stdio, remote SSE, and remote HTTP MCP servers.",
            backstory="An AI agent capable of leveraging a diverse set of tools from multiple sources.",
            tools=aggregated_tools, # All tools are available here
            verbose=True,
        )

... # Your other agent, tasks, and crew code here

except Exception as e:
    print(f"Error connecting to or using multiple MCP servers (Managed): {e}")
    print("Ensure all MCP servers are running and accessible with correct configurations.")

## Connection Management

When using the context manager (`with` statement), `MCPServerAdapter` handles the lifecycle (start and stop) of all connections to the configured MCP servers. This simplifies resource management and ensures that all connections are properly closed when the context is exited.

---

## `DirectorySearchTool`

**URL:** llms-txt#`directorysearchtool`

**Contents:**
- Description
- Installation
- Initialization and Usage

<Note>
  **Experimental**: The DirectorySearchTool is under continuous development. Features and functionalities might evolve, and unexpected behavior may occur as we refine the tool.
</Note>

The DirectorySearchTool enables semantic search within the content of specified directories, leveraging the Retrieval-Augmented Generation (RAG) methodology for efficient navigation through files. Designed for flexibility, it allows users to dynamically specify search directories at runtime or set a fixed directory during initial setup.

To use the DirectorySearchTool, begin by installing the crewai\_tools package. Execute the following command in your terminal:

## Initialization and Usage

Import the DirectorySearchTool from the `crewai_tools` package to start. You can initialize the tool without specifying a directory, enabling the setting of the search directory at runtime. Alternatively, the tool can be initialized with a predefined directory.

```python Code theme={null}
from crewai_tools import DirectorySearchTool

**Examples:**

Example 1 (unknown):
```unknown
## Initialization and Usage

Import the DirectorySearchTool from the `crewai_tools` package to start. You can initialize the tool without specifying a directory, enabling the setting of the search directory at runtime. Alternatively, the tool can be initialized with a predefined directory.
```

---

## Directory RAG Search

**URL:** llms-txt#directory-rag-search

Source: https://docs.crewai.com/en/tools/file-document/directorysearchtool

The `DirectorySearchTool` is a powerful RAG (Retrieval-Augmented Generation) tool designed for semantic searches within a directory's content.

---

## Directory Read

**URL:** llms-txt#directory-read

Source: https://docs.crewai.com/en/tools/file-document/directoryreadtool

The `DirectoryReadTool` is a powerful utility designed to provide a comprehensive listing of directory contents.

---

## Disable auto-summarization and use RAG instead

**URL:** llms-txt#disable-auto-summarization-and-use-rag-instead

**Contents:**
- Direct Agent Interaction with `kickoff()`
  - How `kickoff()` Works

agent = Agent(
    role="Detailed Analyst",
    goal="Maintain complete information accuracy",
    backstory="Expert requiring full context",
    respect_context_window=False,  # No summarization
    tools=[RagTool()],  # Use RAG for large data
    verbose=True
)
python Code theme={null}
from crewai import Agent
from crewai_tools import SerperDevTool

**Examples:**

Example 1 (unknown):
```unknown
<Note>
  The context window management feature works automatically in the background. You don't need to call any special functions - just set `respect_context_window` to your preferred behavior and CrewAI handles the rest!
</Note>

## Direct Agent Interaction with `kickoff()`

Agents can be used directly without going through a task or crew workflow using the `kickoff()` method. This provides a simpler way to interact with an agent when you don't need the full crew orchestration capabilities.

### How `kickoff()` Works

The `kickoff()` method allows you to send messages directly to an agent and get a response, similar to how you would interact with an LLM but with all the agent's capabilities (tools, reasoning, etc.).
```

---

## DOCX RAG Search

**URL:** llms-txt#docx-rag-search

Source: https://docs.crewai.com/en/tools/file-document/docxsearchtool

The `DOCXSearchTool` is a RAG tool designed for semantic searching within DOCX documents.

---

## Dynamic filtering (context-aware)

**URL:** llms-txt#dynamic-filtering-(context-aware)

**Contents:**
- Configuration Parameters
  - MCPServerStdio Parameters
  - MCPServerHTTP Parameters
  - MCPServerSSE Parameters
  - Common Parameters
- Key Features
- Error Handling

def dynamic_filter(context: ToolFilterContext, tool: dict) -> bool:
    # Block dangerous tools for certain agent roles
    if context.agent.role == "Code Reviewer":
        if "delete" in tool.get("name", "").lower():
            return False
    return True

mcps=[
    MCPServerStdio(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem"],
        tool_filter=static_filter,  # or dynamic_filter
    ),
]
python theme={null}
from crewai import Agent
from crewai.mcp import MCPServerStdio, MCPServerHTTP

agent = Agent(
    role="Resilient Agent",
    goal="Continue working despite server issues",
    backstory="Agent that handles failures gracefully",
    mcps=[
        # String references
        "https://reliable-server.com/mcp",        # Will work
        "https://unreachable-server.com/mcp",     # Will be skipped gracefully
        "crewai-amp:working-service",             # Will work

# Structured configs
        MCPServerStdio(
            command="python",
            args=["reliable_server.py"],          # Will work
        ),
        MCPServerHTTP(
            url="https://slow-server.com/mcp",     # Will timeout gracefully
        ),
    ]
)

**Examples:**

Example 1 (unknown):
```unknown
## Configuration Parameters

Each transport type supports specific configuration options:

### MCPServerStdio Parameters

* **`command`** (required): Command to execute (e.g., `"python"`, `"node"`, `"npx"`, `"uvx"`)
* **`args`** (optional): List of command arguments (e.g., `["server.py"]` or `["-y", "@mcp/server"]`)
* **`env`** (optional): Dictionary of environment variables to pass to the process
* **`tool_filter`** (optional): Tool filter function for filtering available tools
* **`cache_tools_list`** (optional): Whether to cache the tool list for faster subsequent access (default: `False`)

### MCPServerHTTP Parameters

* **`url`** (required): Server URL (e.g., `"https://api.example.com/mcp"`)
* **`headers`** (optional): Dictionary of HTTP headers for authentication or other purposes
* **`streamable`** (optional): Whether to use streamable HTTP transport (default: `True`)
* **`tool_filter`** (optional): Tool filter function for filtering available tools
* **`cache_tools_list`** (optional): Whether to cache the tool list for faster subsequent access (default: `False`)

### MCPServerSSE Parameters

* **`url`** (required): Server URL (e.g., `"https://api.example.com/mcp/sse"`)
* **`headers`** (optional): Dictionary of HTTP headers for authentication or other purposes
* **`tool_filter`** (optional): Tool filter function for filtering available tools
* **`cache_tools_list`** (optional): Whether to cache the tool list for faster subsequent access (default: `False`)

### Common Parameters

All transport types support:

* **`tool_filter`**: Filter function to control which tools are available. Can be:
  * `None` (default): All tools are available
  * Static filter: Created with `create_static_tool_filter()` for allow/block lists
  * Dynamic filter: Created with `create_dynamic_tool_filter()` for context-aware filtering
* **`cache_tools_list`**: When `True`, caches the tool list after first discovery to improve performance on subsequent connections

## Key Features

* 🔄 **Automatic Tool Discovery**: Tools are automatically discovered and integrated
* 🏷️ **Name Collision Prevention**: Server names are prefixed to tool names
* ⚡ **Performance Optimized**: On-demand connections with schema caching
* 🛡️ **Error Resilience**: Graceful handling of unavailable servers
* ⏱️ **Timeout Protection**: Built-in timeouts prevent hanging connections
* 📊 **Transparent Integration**: Works seamlessly with existing CrewAI features
* 🔧 **Full Transport Support**: Stdio, HTTP/Streamable HTTP, and SSE transports
* 🎯 **Advanced Filtering**: Static and dynamic tool filtering capabilities
* 🔐 **Flexible Authentication**: Support for headers, environment variables, and query parameters

## Error Handling

The MCP DSL integration is designed to be resilient and handles failures gracefully:
```

---

## Each server's tools get unique prefixes based on the server name

**URL:** llms-txt#each-server's-tools-get-unique-prefixes-based-on-the-server-name

---

## Ensure query parameters are properly URL encoded

**URL:** llms-txt#ensure-query-parameters-are-properly-url-encoded

**Contents:**
- Advanced: MCPServerAdapter

## Advanced: MCPServerAdapter

For complex scenarios requiring manual connection management, use the `MCPServerAdapter` class from `crewai-tools`. Using a Python context manager (`with` statement) is the recommended approach as it automatically handles starting and stopping the connection to the MCP server.

---

## Example 1: Initialize from FunctionTool

**URL:** llms-txt#example-1:-initialize-from-functiontool

def search_data(query: str) -> str:
    """Search for information in the data."""
    # Your implementation here
    return f"Results for: {query}"

---

## Example usage (uncomment and adapt once server_params is set):

**URL:** llms-txt#example-usage-(uncomment-and-adapt-once-server_params-is-set):

**Contents:**
- Filtering Tools
  - Accessing a specific tool using dictionary-style indexing.
  - Pass a list of tool names to the `MCPServerAdapter` constructor.
- Using with CrewBase
  - Connection Timeout Configuration
  - Filtering Tools
- Explore MCP Integrations
- Staying Safe with MCP
  - Limitations

with MCPServerAdapter(server_params, connect_timeout=60) as mcp_tools:
    print(f"Available tools: {[tool.name for tool in mcp_tools]}")

my_agent = Agent(
        role="MCP Tool User",
        goal="Utilize tools from an MCP server.",
        backstory="I can connect to MCP servers and use their tools.",
        tools=mcp_tools, # Pass the loaded tools to your agent
        reasoning=True,
        verbose=True
    )
    # ... rest of your crew setup ...
python theme={null}
with MCPServerAdapter(server_params, connect_timeout=60) as mcp_tools:
    print(f"Available tools: {[tool.name for tool in mcp_tools]}")

my_agent = Agent(
        role="MCP Tool User",
        goal="Utilize tools from an MCP server.",
        backstory="I can connect to MCP servers and use their tools.",
        tools=[mcp_tools["tool_name"]], # Pass the loaded tools to your agent
        reasoning=True,
        verbose=True
    )
    # ... rest of your crew setup ...
python theme={null}
with MCPServerAdapter(server_params, "tool_name", connect_timeout=60) as mcp_tools:
    print(f"Available tools: {[tool.name for tool in mcp_tools]}")

my_agent = Agent(
        role="MCP Tool User",
        goal="Utilize tools from an MCP server.",
        backstory="I can connect to MCP servers and use their tools.",
        tools=mcp_tools, # Pass the loaded tools to your agent
        reasoning=True,
        verbose=True
    )
    # ... rest of your crew setup ...
python theme={null}
@CrewBase
class CrewWithMCP:
  # ... define your agents and tasks config file ...

mcp_server_params = [
    # Streamable HTTP Server
    {
        "url": "http://localhost:8001/mcp",
        "transport": "streamable-http"
    },
    # SSE Server
    {
        "url": "http://localhost:8000/sse",
        "transport": "sse"
    },
    # StdIO Server
    StdioServerParameters(
        command="python3",
        args=["servers/your_stdio_server.py"],
        env={"UV_PYTHON": "3.12", **os.environ},
    )
  ]

@agent
  def your_agent(self):
      return Agent(config=self.agents_config["your_agent"], tools=self.get_mcp_tools()) # get all available tools

# ... rest of your crew setup ...
python theme={null}
@CrewBase
class CrewWithMCP:
  mcp_server_params = [...]
  mcp_connect_timeout = 60  # 60 seconds timeout for all MCP connections

@agent
  def your_agent(self):
      return Agent(config=self.agents_config["your_agent"], tools=self.get_mcp_tools())
python theme={null}
@CrewBase
class CrewWithDefaultTimeout:
  mcp_server_params = [...]
  # No mcp_connect_timeout specified - uses default 30 seconds

@agent
  def your_agent(self):
      return Agent(config=self.agents_config["your_agent"], tools=self.get_mcp_tools())
python theme={null}
@agent
def another_agent(self):
    return Agent(
      config=self.agents_config["your_agent"],
      tools=self.get_mcp_tools("tool_1", "tool_2") # get specific tools
    )
python theme={null}
@CrewBase
class CrewWithCustomTimeout:
  mcp_server_params = [...]
  mcp_connect_timeout = 90  # 90 seconds timeout for all MCP connections

@agent
  def filtered_agent(self):
      return Agent(
        config=self.agents_config["your_agent"],
        tools=self.get_mcp_tools("tool_1", "tool_2") # specific tools with custom timeout
      )
```

## Explore MCP Integrations

<CardGroup>
  <Card title="Simple DSL Integration" icon="code" href="/en/mcp/dsl-integration">
    **Recommended**: Use the simple `mcps=[]` field syntax for effortless MCP integration.
  </Card>

<Card title="Stdio Transport" icon="server" href="/en/mcp/stdio">
    Connect to local MCP servers via standard input/output. Ideal for scripts and local executables.
  </Card>

<Card title="SSE Transport" icon="wifi" href="/en/mcp/sse">
    Integrate with remote MCP servers using Server-Sent Events for real-time data streaming.
  </Card>

<Card title="Streamable HTTP Transport" icon="globe" href="/en/mcp/streamable-http">
    Utilize flexible Streamable HTTP for robust communication with remote MCP servers.
  </Card>

<Card title="Connecting to Multiple Servers" icon="layer-group" href="/en/mcp/multiple-servers">
    Aggregate tools from several MCP servers simultaneously using a single adapter.
  </Card>

<Card title="Security Considerations" icon="lock" href="/en/mcp/security">
    Review important security best practices for MCP integration to keep your agents safe.
  </Card>
</CardGroup>

Checkout this repository for full demos and examples of MCP integration with CrewAI! 👇

<Card title="GitHub Repository" icon="github" href="https://github.com/tonykipkemboi/crewai-mcp-demo">
  CrewAI MCP Demo
</Card>

## Staying Safe with MCP

<Warning>
  Always ensure that you trust an MCP Server before using it.
</Warning>

#### Security Warning: DNS Rebinding Attacks

SSE transports can be vulnerable to DNS rebinding attacks if not properly secured.
To prevent this:

1. **Always validate Origin headers** on incoming SSE connections to ensure they come from expected sources
2. **Avoid binding servers to all network interfaces** (0.0.0.0) when running locally - bind only to localhost (127.0.0.1) instead
3. **Implement proper authentication** for all SSE connections

Without these protections, attackers could use DNS rebinding to interact with local MCP servers from remote websites.

For more details, see the [Anthropic's MCP Transport Security docs](https://modelcontextprotocol.io/docs/concepts/transports#security-considerations).

* **Supported Primitives**: Currently, `MCPServerAdapter` primarily supports adapting MCP `tools`.
  Other MCP primitives like `prompts` or `resources` are not directly integrated as CrewAI components through this adapter at this time.
* **Output Handling**: The adapter typically processes the primary text output from an MCP tool (e.g., `.content[0].text`). Complex or multi-modal outputs might require custom handling if not fitting this pattern.

**Examples:**

Example 1 (unknown):
```unknown
This general pattern shows how to integrate tools. For specific examples tailored to each transport, refer to the detailed guides below.

## Filtering Tools

There are two ways to filter tools:

1. Accessing a specific tool using dictionary-style indexing.
2. Pass a list of tool names to the `MCPServerAdapter` constructor.

### Accessing a specific tool using dictionary-style indexing.
```

Example 2 (unknown):
```unknown
### Pass a list of tool names to the `MCPServerAdapter` constructor.
```

Example 3 (unknown):
```unknown
## Using with CrewBase

To use MCPServer tools within a CrewBase class, use the `get_mcp_tools` method. Server configurations should be provided via the `mcp_server_params` attribute. You can pass either a single configuration or a list of multiple server configurations.
```

Example 4 (unknown):
```unknown
<Tip>
  When a crew class is decorated with `@CrewBase`, the adapter lifecycle is managed for you:

  * The first call to `get_mcp_tools()` lazily creates a shared `MCPServerAdapter` that is reused by every agent in the crew.
  * The adapter automatically shuts down after `.kickoff()` completes thanks to an implicit after-kickoff hook injected by `@CrewBase`, so no manual cleanup is required.
  * If `mcp_server_params` is not defined, `get_mcp_tools()` simply returns an empty list, allowing the same code paths to run with or without MCP configured.

  This makes it safe to call `get_mcp_tools()` from multiple agent methods or selectively enable MCP per environment.
</Tip>

### Connection Timeout Configuration

You can configure the connection timeout for MCP servers by setting the `mcp_connect_timeout` class attribute. If no timeout is specified, it defaults to 30 seconds.
```

---

## Example with custom connection timeout

**URL:** llms-txt#example-with-custom-connection-timeout

with MCPServerAdapter(server_params, connect_timeout=60) as tools:
    # Connection will timeout after 60 seconds if not established
    pass
python theme={null}
from crewai import Agent
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters # For Stdio Server

**Examples:**

Example 1 (unknown):
```unknown

```

---

## Example with custom scraping parameters

**URL:** llms-txt#example-with-custom-scraping-parameters

web_scraper_agent = Agent(
    role="Web Scraper",
    goal="Extract information from websites with custom parameters",
    backstory="An expert in web scraping who can extract content from any website.",
    tools=[scrape_tool],
    verbose=True,
)

---

## `EXASearchTool`

**URL:** llms-txt#`exasearchtool`

**Contents:**
- Description
- Installation
- Example

The EXASearchTool is designed to perform a semantic search for a specified query from a text's content across the internet.
It utilizes the [exa.ai](https://exa.ai/) API to fetch and display the most relevant search results based on the query provided by the user.

To incorporate this tool into your project, follow the installation instructions below:

The following example demonstrates how to initialize the tool and execute a search with a given query:

```python Code theme={null}
from crewai_tools import EXASearchTool

**Examples:**

Example 1 (unknown):
```unknown
## Example

The following example demonstrates how to initialize the tool and execute a search with a given query:
```

---

## EXA Search Web Loader

**URL:** llms-txt#exa-search-web-loader

Source: https://docs.crewai.com/en/tools/search-research/exasearchtool

The `EXASearchTool` is designed to perform a semantic search for a specified query from a text's content across the internet.

---

## Execute a search

**URL:** llms-txt#execute-a-search

**Contents:**
- Agent Integration Example

results = tool.run(search_query="Latest AI developments")
print(results)
python Code theme={null}
from crewai import Agent
from crewai.project import agent
from crewai_tools import BraveSearchTool

**Examples:**

Example 1 (unknown):
```unknown
## Agent Integration Example

Here's how to integrate the `BraveSearchTool` with a CrewAI agent:
```

---

## `FileWriterTool`

**URL:** llms-txt#`filewritertool`

**Contents:**
- Description
- Installation
- Example

The `FileWriterTool` is a component of the crewai\_tools package, designed to simplify the process of writing content to files with cross-platform compatibility (Windows, Linux, macOS).
It is particularly useful in scenarios such as generating reports, saving logs, creating configuration files, and more.
This tool handles path differences across operating systems, supports UTF-8 encoding, and automatically creates directories if they don't exist, making it easier to organize your output reliably across different platforms.

Install the crewai\_tools package to use the `FileWriterTool` in your projects:

To get started with the `FileWriterTool`:

```python Code theme={null}
from crewai_tools import FileWriterTool

**Examples:**

Example 1 (unknown):
```unknown
## Example

To get started with the `FileWriterTool`:
```

---

## File Read

**URL:** llms-txt#file-read

**Contents:**
- Overview
- Installation
- Usage Example

Source: https://docs.crewai.com/en/tools/file-document/filereadtool

The `FileReadTool` is designed to read files from the local file system.

<Note>
  We are still working on improving tools, so there might be unexpected behavior or changes in the future.
</Note>

The FileReadTool conceptually represents a suite of functionalities within the crewai\_tools package aimed at facilitating file reading and content retrieval.
This suite includes tools for processing batch text files, reading runtime configuration files, and importing data for analytics.
It supports a variety of text-based file formats such as `.txt`, `.csv`, `.json`, and more. Depending on the file type, the suite offers specialized functionality,
such as converting JSON content into a Python dictionary for ease of use.

To utilize the functionalities previously attributed to the FileReadTool, install the crewai\_tools package:

To get started with the FileReadTool:

```python Code theme={null}
from crewai_tools import FileReadTool

**Examples:**

Example 1 (unknown):
```unknown
## Usage Example

To get started with the FileReadTool:
```

---

## File Write

**URL:** llms-txt#file-write

Source: https://docs.crewai.com/en/tools/file-document/filewritetool

The `FileWriterTool` is designed to write content to files.

---

## `FirecrawlCrawlWebsiteTool`

**URL:** llms-txt#`firecrawlcrawlwebsitetool`

**Contents:**
- Description
- Installation
- Example
- Arguments

[Firecrawl](https://firecrawl.dev) is a platform for crawling and convert any website into clean markdown or structured data.

* Get an API key from [firecrawl.dev](https://firecrawl.dev) and set it in environment variables (`FIRECRAWL_API_KEY`).
* Install the [Firecrawl SDK](https://github.com/mendableai/firecrawl) along with `crewai[tools]` package:

Utilize the FirecrawlScrapeFromWebsiteTool as follows to allow your agent to load websites:

* `api_key`: Optional. Specifies Firecrawl API key. Defaults is the `FIRECRAWL_API_KEY` environment variable.
* `url`: The base URL to start crawling from.
* `page_options`: Optional.
  * `onlyMainContent`: Optional. Only return the main content of the page excluding headers, navs, footers, etc.
  * `includeHtml`: Optional. Include the raw HTML content of the page. Will output a html key in the response.
* `crawler_options`: Optional. Options for controlling the crawling behavior.
  * `includes`: Optional. URL patterns to include in the crawl.
  * `exclude`: Optional. URL patterns to exclude from the crawl.
  * `generateImgAltText`: Optional. Generate alt text for images using LLMs (requires a paid plan).
  * `returnOnlyUrls`: Optional. If true, returns only the URLs as a list in the crawl status. Note: the response will be a list of URLs inside the data, not a list of documents.
  * `maxDepth`: Optional. Maximum depth to crawl. Depth 1 is the base URL, depth 2 includes the base URL and its direct children, and so on.
  * `mode`: Optional. The crawling mode to use. Fast mode crawls 4x faster on websites without a sitemap but may not be as accurate and shouldn't be used on heavily JavaScript-rendered websites.
  * `limit`: Optional. Maximum number of pages to crawl.
  * `timeout`: Optional. Timeout in milliseconds for the crawling operation.

**Examples:**

Example 1 (unknown):
```unknown
## Example

Utilize the FirecrawlScrapeFromWebsiteTool as follows to allow your agent to load websites:
```

---

## `FirecrawlScrapeWebsiteTool`

**URL:** llms-txt#`firecrawlscrapewebsitetool`

**Contents:**
- Description
- Installation
- Example
- Arguments

[Firecrawl](https://firecrawl.dev) is a platform for crawling and convert any website into clean markdown or structured data.

* Get an API key from [firecrawl.dev](https://firecrawl.dev) and set it in environment variables (`FIRECRAWL_API_KEY`).
* Install the [Firecrawl SDK](https://github.com/mendableai/firecrawl) along with `crewai[tools]` package:

Utilize the FirecrawlScrapeWebsiteTool as follows to allow your agent to load websites:

* `api_key`: Optional. Specifies Firecrawl API key. Defaults is the `FIRECRAWL_API_KEY` environment variable.
* `url`: The URL to scrape.
* `page_options`: Optional.
  * `onlyMainContent`: Optional. Only return the main content of the page excluding headers, navs, footers, etc.
  * `includeHtml`: Optional. Include the raw HTML content of the page. Will output a html key in the response.
* `extractor_options`: Optional. Options for LLM-based extraction of structured information from the page content
  * `mode`: The extraction mode to use, currently supports 'llm-extraction'
  * `extractionPrompt`: Optional. A prompt describing what information to extract from the page
  * `extractionSchema`: Optional. The schema for the data to be extracted
* `timeout`: Optional. Timeout in milliseconds for the request

**Examples:**

Example 1 (unknown):
```unknown
## Example

Utilize the FirecrawlScrapeWebsiteTool as follows to allow your agent to load websites:
```

---

## Firecrawl Crawl Website

**URL:** llms-txt#firecrawl-crawl-website

Source: https://docs.crewai.com/en/tools/web-scraping/firecrawlcrawlwebsitetool

The `FirecrawlCrawlWebsiteTool` is designed to crawl and convert websites into clean markdown or structured data.

---

## Firecrawl Scrape Website

**URL:** llms-txt#firecrawl-scrape-website

Source: https://docs.crewai.com/en/tools/web-scraping/firecrawlscrapewebsitetool

The `FirecrawlScrapeWebsiteTool` is designed to scrape websites and convert them into clean markdown or structured data.

---

## Force Tool Output as Result

**URL:** llms-txt#force-tool-output-as-result

**Contents:**
- Introduction
- Forcing Tool Output as Result

Source: https://docs.crewai.com/en/learn/force-tool-output-as-result

Learn how to force tool output as the result in an Agent's task in CrewAI.

In CrewAI, you can force the output of a tool as the result of an agent's task.
This feature is useful when you want to ensure that the tool output is captured and returned as the task result, avoiding any agent modification during the task execution.

## Forcing Tool Output as Result

To force the tool output as the result of an agent's task, you need to set the `result_as_answer` parameter to `True` when adding a tool to the agent.
This parameter ensures that the tool output is captured and returned as the task result, without any modifications by the agent.

Here's an example of how to force the tool output as the result of an agent's task:

```python Code theme={null}
from crewai.agent import Agent
from my_tool import MyCustomTool

---

## For Advanced MCPServerAdapter usage

**URL:** llms-txt#for-advanced-mcpserveradapter-usage

**Contents:**
- Quick Start: Simple DSL Integration
  - Quick Start with String References

uv pip install 'crewai-tools[mcp]'
python theme={null}
from crewai import Agent, Task, Crew

**Examples:**

Example 1 (unknown):
```unknown
## Quick Start: Simple DSL Integration

The easiest way to integrate MCP servers is using the `mcps` field on your agents. You can use either string references or structured configurations.

### Quick Start with String References
```

---

## Full service with all tools

**URL:** llms-txt#full-service-with-all-tools

"crewai-amp:financial-data"

---

## Get only the forecast tool from weather server

**URL:** llms-txt#get-only-the-forecast-tool-from-weather-server

"https://weather.api.com/mcp#get_forecast"

---

## Get only the search tool from Exa

**URL:** llms-txt#get-only-the-search-tool-from-exa

**Contents:**
  - CrewAI AOP Marketplace

"https://mcp.exa.ai/mcp?api_key=your_key#web_search_exa"
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### CrewAI AOP Marketplace

Access tools from the CrewAI AOP marketplace:
```

---

## `GithubSearchTool`

**URL:** llms-txt#`githubsearchtool`

**Contents:**
- Description
- Installation
- Example

<Note>
  We are still working on improving tools, so there might be unexpected behavior or changes in the future.
</Note>

The GithubSearchTool is a Retrieval-Augmented Generation (RAG) tool specifically designed for conducting semantic searches within GitHub repositories. Utilizing advanced semantic search capabilities, it sifts through code, pull requests, issues, and repositories, making it an essential tool for developers, researchers, or anyone in need of precise information from GitHub.

To use the GithubSearchTool, first ensure the crewai\_tools package is installed in your Python environment:

This command installs the necessary package to run the GithubSearchTool along with any other tools included in the crewai\_tools package.

Get a GitHub Personal Access Token at [https://github.com/settings/tokens](https://github.com/settings/tokens) (Developer settings → Fine‑grained tokens or classic tokens).

Here’s how you can use the GithubSearchTool to perform semantic searches within a GitHub repository:

```python Code theme={null}
from crewai_tools import GithubSearchTool

**Examples:**

Example 1 (unknown):
```unknown
This command installs the necessary package to run the GithubSearchTool along with any other tools included in the crewai\_tools package.

Get a GitHub Personal Access Token at [https://github.com/settings/tokens](https://github.com/settings/tokens) (Developer settings → Fine‑grained tokens or classic tokens).

## Example

Here’s how you can use the GithubSearchTool to perform semantic searches within a GitHub repository:
```

---

## Github Search

**URL:** llms-txt#github-search

Source: https://docs.crewai.com/en/tools/search-research/githubsearchtool

The `GithubSearchTool` is designed to search websites and convert them into clean markdown or structured data.

---

## Good - only get the tools you need

**URL:** llms-txt#good---only-get-the-tools-you-need

mcps=["https://weather.api.com/mcp#get_forecast"]

---

## Google Serper Search

**URL:** llms-txt#google-serper-search

Source: https://docs.crewai.com/en/tools/search-research/serperdevtool

The `SerperDevTool` is designed to search the internet and return the most relevant results.

---

## Guardrail with tool response context

**URL:** llms-txt#guardrail-with-tool-response-context

**Contents:**
- How It Works
  - Validation Process
  - Validation Logic
- Guardrail Results

weather_guardrail = HallucinationGuardrail(
    context="Current weather information for the requested location",
    llm=LLM(model="gpt-4o-mini"),
    tool_response="Weather API returned: Temperature 22°C, Humidity 65%, Clear skies"
)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## How It Works

### Validation Process

1. **Context Analysis**: The guardrail compares task output against the provided reference context
2. **Faithfulness Scoring**: Uses an internal evaluator to assign a faithfulness score (0-10)
3. **Verdict Determination**: Determines if content is faithful or contains hallucinations
4. **Threshold Checking**: If a custom threshold is set, validates against that score
5. **Feedback Generation**: Provides detailed reasons when validation fails

### Validation Logic

* **Default Mode**: Uses verdict-based validation (FAITHFUL vs HALLUCINATED)
* **Threshold Mode**: Requires faithfulness score to meet or exceed the specified threshold
* **Error Handling**: Gracefully handles evaluation errors and provides informative feedback

## Guardrail Results

The guardrail returns structured results indicating validation status:
```

---

## `HyperbrowserLoadTool`

**URL:** llms-txt#`hyperbrowserloadtool`

**Contents:**
- Description
- Installation
- Steps to Get Started
- Example

The `HyperbrowserLoadTool` enables web scraping and crawling using [Hyperbrowser](https://hyperbrowser.ai), a platform for running and scaling headless browsers. This tool allows you to scrape a single page or crawl an entire site, returning the content in properly formatted markdown or HTML.

* Instant Scalability - Spin up hundreds of browser sessions in seconds without infrastructure headaches
* Simple Integration - Works seamlessly with popular tools like Puppeteer and Playwright
* Powerful APIs - Easy to use APIs for scraping/crawling any site
* Bypass Anti-Bot Measures - Built-in stealth mode, ad blocking, automatic CAPTCHA solving, and rotating proxies

To use this tool, you need to install the Hyperbrowser SDK:

## Steps to Get Started

To effectively use the `HyperbrowserLoadTool`, follow these steps:

1. **Sign Up**: Head to [Hyperbrowser](https://app.hyperbrowser.ai/) to sign up and generate an API key.
2. **API Key**: Set the `HYPERBROWSER_API_KEY` environment variable or pass it directly to the tool constructor.
3. **Install SDK**: Install the Hyperbrowser SDK using the command above.

The following example demonstrates how to initialize the tool and use it to scrape a website:

```python Code theme={null}
from crewai_tools import HyperbrowserLoadTool
from crewai import Agent

**Examples:**

Example 1 (unknown):
```unknown
## Steps to Get Started

To effectively use the `HyperbrowserLoadTool`, follow these steps:

1. **Sign Up**: Head to [Hyperbrowser](https://app.hyperbrowser.ai/) to sign up and generate an API key.
2. **API Key**: Set the `HYPERBROWSER_API_KEY` environment variable or pass it directly to the tool constructor.
3. **Install SDK**: Install the Hyperbrowser SDK using the command above.

## Example

The following example demonstrates how to initialize the tool and use it to scrape a website:
```

---

## Hyperbrowser Load Tool

**URL:** llms-txt#hyperbrowser-load-tool

Source: https://docs.crewai.com/en/tools/web-scraping/hyperbrowserloadtool

The `HyperbrowserLoadTool` enables web scraping and crawling using Hyperbrowser.

---

## Initialize a search tool

**URL:** llms-txt#initialize-a-search-tool

search_tool = SerperDevTool()

---

## Initialize different automation tools

**URL:** llms-txt#initialize-different-automation-tools

data_collection_tool = InvokeCrewAIAutomationTool(
    crew_api_url="https://data-collection-crew-[...].crewai.com",
    crew_bearer_token="your_bearer_token_here",
    crew_name="Data Collection Automation",
    crew_description="Collects and preprocesses raw data"
)

analysis_tool = InvokeCrewAIAutomationTool(
    crew_api_url="https://analysis-crew-[...].crewai.com",
    crew_bearer_token="your_bearer_token_here",
    crew_name="Analysis Automation",
    crew_description="Performs advanced data analysis and modeling"
)

reporting_tool = InvokeCrewAIAutomationTool(
    crew_api_url="https://reporting-crew-[...].crewai.com",
    crew_bearer_token="your_bearer_token_here",
    crew_name="Reporting Automation",
    crew_description="Generates comprehensive reports and visualizations"
)

---

## Initialize from LlamaHub Tools

**URL:** llms-txt#initialize-from-llamahub-tools

**Contents:**
  - From a LlamaIndex Query Engine

wolfram_spec = WolframAlphaToolSpec(app_id="your_app_id")
wolfram_tools = wolfram_spec.to_tool_list()
tools = [LlamaIndexTool.from_tool(t) for t in wolfram_tools]
python Code theme={null}
from crewai_tools import LlamaIndexTool
from llama_index.core import VectorStoreIndex
from llama_index.core.readers import SimpleDirectoryReader

**Examples:**

Example 1 (unknown):
```unknown
### From a LlamaIndex Query Engine
```

---

## Initialize Qdrant search tool

**URL:** llms-txt#initialize-qdrant-search-tool

from crewai_tools import QdrantConfig

qdrant_tool = QdrantVectorSearchTool(
    qdrant_config=QdrantConfig(
        qdrant_url=os.getenv("QDRANT_URL"),
        qdrant_api_key=os.getenv("QDRANT_API_KEY"),
        collection_name=collection_name,
        limit=3,
        score_threshold=0.35
    )
)

---

## Initialize the AIMindTool

**URL:** llms-txt#initialize-the-aimindtool

aimind_tool = AIMindTool(
    datasources=[
        {
            "description": "house sales data",
            "engine": "postgres",
            "connection_data": {
                "user": "demo_user",
                "password": "demo_password",
                "host": "samples.mindsdb.com",
                "port": 5432,
                "database": "demo",
                "schema": "demo_data"
            },
            "tables": ["house_sales"]
        }
    ]
)

---

## Initialize the tool allowing for any PDF content search if the path is provided during execution

**URL:** llms-txt#initialize-the-tool-allowing-for-any-pdf-content-search-if-the-path-is-provided-during-execution

tool = PDFSearchTool()

---

## Initialize the tool and add content

**URL:** llms-txt#initialize-the-tool-and-add-content

rag_tool = RagTool()
rag_tool.add(data_type="web_page", url="https://docs.crewai.com")
rag_tool.add(data_type="file", path="company_data.pdf")

---

## Initialize the tool

**URL:** llms-txt#initialize-the-tool

automation_tool = InvokeCrewAIAutomationTool(
    crew_api_url="https://data-analysis-crew-[...].crewai.com",
    crew_bearer_token="your_bearer_token_here",
    crew_name="Data Analysis Crew",
    crew_description="Analyzes data and generates insights"
)

---

## Initialize the tool for general YouTube channel searches

**URL:** llms-txt#initialize-the-tool-for-general-youtube-channel-searches

youtube_channel_tool = YoutubeChannelSearchTool()

---

## Initialize the tool for general YouTube video searches

**URL:** llms-txt#initialize-the-tool-for-general-youtube-video-searches

youtube_search_tool = YoutubeVideoSearchTool()

---

## Initialize the tool for internet searching capabilities

**URL:** llms-txt#initialize-the-tool-for-internet-searching-capabilities

**Contents:**
- Parameters
- Example with Parameters

tool = SerperDevTool()
python Code theme={null}
from crewai_tools import SerperDevTool

tool = SerperDevTool(
    search_url="https://google.serper.dev/scholar",
    n_results=2,
)

print(tool.run(search_query="ChatGPT"))

**Examples:**

Example 1 (unknown):
```unknown
## Parameters

The `SerperDevTool` comes with several parameters that will be passed to the API :

* **search\_url**: The URL endpoint for the search API. (Default is `https://google.serper.dev/search`)

* **country**: Optional. Specify the country for the search results.

* **location**: Optional. Specify the location for the search results.

* **locale**: Optional. Specify the locale for the search results.

* **n\_results**: Number of search results to return. Default is `10`.

The values for `country`, `location`, `locale` and `search_url` can be found on the [Serper Playground](https://serper.dev/playground).

## Example with Parameters

Here is an example demonstrating how to use the tool with additional parameters:
```

---

## Initialize the tool for semantic searches within a specific GitHub repository

**URL:** llms-txt#initialize-the-tool-for-semantic-searches-within-a-specific-github-repository

tool = GithubSearchTool(
	github_repo='https://github.com/example/repo',
	gh_token='your_github_personal_access_token',
	content_types=['code', 'issue'] # Options: code, repo, pr, issue
)

---

## Initialize the tool to search any MDX content it learns about during execution

**URL:** llms-txt#initialize-the-tool-to-search-any-mdx-content-it-learns-about-during-execution

tool = MDXSearchTool()

---

## Initialize the tool to search within any DOCX file's content

**URL:** llms-txt#initialize-the-tool-to-search-within-any-docx-file's-content

tool = DOCXSearchTool()

---

## Initialize the tool to search within any text file's content

**URL:** llms-txt#initialize-the-tool-to-search-within-any-text-file's-content

---

## Initialize the tool without a specific CSV file.

**URL:** llms-txt#initialize-the-tool-without-a-specific-csv-file.

---

## Initialize the tool with an Apify Actor

**URL:** llms-txt#initialize-the-tool-with-an-apify-actor

tool = ApifyActorsTool(actor_name="apify/rag-web-browser")

---

## Initialize the tool with a specific CSV file.

**URL:** llms-txt#initialize-the-tool-with-a-specific-csv-file.

---

## Initialize the tool with a specific directory,

**URL:** llms-txt#initialize-the-tool-with-a-specific-directory,

---

## Initialize the tool with a specific DOCX file,

**URL:** llms-txt#initialize-the-tool-with-a-specific-docx-file,

---

## Initialize the tool with a specific MDX file path for an exclusive search within that document

**URL:** llms-txt#initialize-the-tool-with-a-specific-mdx-file-path-for-an-exclusive-search-within-that-document

**Contents:**
- Parameters
- Customization of Model and Embeddings

tool = MDXSearchTool(mdx='path/to/your/document.mdx')
python Code theme={null}
from chromadb.config import Settings

tool = MDXSearchTool(
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
## Parameters

* mdx: **Optional**. Specifies the MDX file path for the search. It can be provided during initialization.

## Customization of Model and Embeddings

The tool defaults to using OpenAI for embeddings and summarization. For customization, utilize a configuration dictionary as shown below:
```

---

## Initialize the tool with a specific PDF path for exclusive search within that document

**URL:** llms-txt#initialize-the-tool-with-a-specific-pdf-path-for-exclusive-search-within-that-document

**Contents:**
- Arguments
- Custom model and embeddings

tool = PDFSearchTool(pdf='path/to/your/document.pdf')
python Code theme={null}
from crewai_tools import PDFSearchTool

**Examples:**

Example 1 (unknown):
```unknown
## Arguments

* `pdf`: **Optional** The PDF path for the search. Can be provided at initialization or within the `run` method's arguments. If provided at initialization, the tool confines its search to the specified document.

## Custom model and embeddings

By default, the tool uses OpenAI for both embeddings and summarization. To customize the model, you can use a config dictionary as follows. Note: a vector database is required because generated embeddings must be stored and queried from a vectordb.
```

---

## Initialize the tool with a specific text file,

**URL:** llms-txt#initialize-the-tool-with-a-specific-text-file,

---

## Initialize the tool with a specific XML file path

**URL:** llms-txt#initialize-the-tool-with-a-specific-xml-file-path

**Contents:**
- Arguments
- Custom model and embeddings

#for exclusive search within that document
tool = XMLSearchTool(xml='path/to/your/xmlfile.xml')
python Code   theme={null}
from chromadb.config import Settings

tool = XMLSearchTool(
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

* `xml`: This is the path to the XML file you wish to search.
  It is an optional parameter during the tool's initialization but must be provided either at initialization or as part of the `run` method's arguments to execute a search.

## Custom model and embeddings

By default, the tool uses OpenAI for both embeddings and summarization. To customize the model, you can use a config dictionary as follows:
```

---

## Initialize the tool with a specific YouTube channel handle

**URL:** llms-txt#initialize-the-tool-with-a-specific-youtube-channel-handle

youtube_channel_tool = YoutubeChannelSearchTool(
    youtube_channel_handle='@exampleChannel'
)

---

## Initialize the tool with a specific YouTube video URL

**URL:** llms-txt#initialize-the-tool-with-a-specific-youtube-video-url

youtube_search_tool = YoutubeVideoSearchTool(
    youtube_video_url='https://youtube.com/watch?v=example'
)

---

## Initialize the tool with custom parameters

**URL:** llms-txt#initialize-the-tool-with-custom-parameters

tool = BraveSearchTool(
    country="US",
    n_results=5,
    save_file=True
)

---

## Initialize the tool with predefined criteria

**URL:** llms-txt#initialize-the-tool-with-predefined-criteria

patronus_eval_tool = PatronusPredefinedCriteriaEvalTool(
    evaluators=[{"evaluator": "judge", "criteria": "contains-code"}]
)

---

## Initialize the tool with predefined parameters

**URL:** llms-txt#initialize-the-tool-with-predefined-parameters

selenium_tool = SeleniumScrapingTool(
    website_url='https://example.com',
    css_element='.main-content',
    wait_time=5
)

---

## Initialize the tool with QdrantConfig

**URL:** llms-txt#initialize-the-tool-with-qdrantconfig

qdrant_tool = QdrantVectorSearchTool(
    qdrant_config=QdrantConfig(
        qdrant_url="your_qdrant_url",
        qdrant_api_key="your_qdrant_api_key",
        collection_name="your_collection"
    )
)

---

## Initialize the tool with the Browserbase API key and Project ID

**URL:** llms-txt#initialize-the-tool-with-the-browserbase-api-key-and-project-id

**Contents:**
- Arguments

tool = BrowserbaseLoadTool()
```

The following parameters can be used to customize the `BrowserbaseLoadTool`'s behavior:

| Argument          | Type     | Description                                                                           |
| :---------------- | :------- | :------------------------------------------------------------------------------------ |
| **api\_key**      | `string` | *Optional*. Browserbase API key. Default is `BROWSERBASE_API_KEY` env variable.       |
| **project\_id**   | `string` | *Optional*. Browserbase Project ID. Default is `BROWSERBASE_PROJECT_ID` env variable. |
| **text\_content** | `bool`   | *Optional*. Retrieve only text content. Default is `False`.                           |
| **session\_id**   | `string` | *Optional*. Provide an existing Session ID.                                           |
| **proxy**         | `bool`   | *Optional*. Enable/Disable Proxies. Default is `False`.                               |

---

## Initialize the tool with the custom evaluator

**URL:** llms-txt#initialize-the-tool-with-the-custom-evaluator

patronus_eval_tool = PatronusLocalEvaluatorTool(
    patronus_client=client,
    evaluator="random_evaluator",
    evaluated_model_gold_answer="example label",
)

---

## Initialize the tool with the database URI and the target table name

**URL:** llms-txt#initialize-the-tool-with-the-database-uri-and-the-target-table-name

**Contents:**
- Arguments
- Custom Model and Embeddings

tool = PGSearchTool(
    db_uri='postgresql://user:password@localhost:5432/mydatabase', 
    table_name='employees'
)
python Code theme={null}
tool = PGSearchTool(
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

The PGSearchTool is designed to require the following arguments for its operation:

| Argument        | Type     | Description                                                                                                                                                                                                    |
| :-------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **db\_uri**     | `string` | **Mandatory**. A string representing the URI of the PostgreSQL database to be queried. This argument will be mandatory and must include the necessary authentication details and the location of the database. |
| **table\_name** | `string` | **Mandatory**. A string specifying the name of the table within the database on which the semantic search will be performed. This argument will also be mandatory.                                             |

## Custom Model and Embeddings

The tool intends to use OpenAI for both embeddings and summarization by default. Users will have the option to customize the model using a config dictionary as follows:
```

---

## Initialize the tool with the website URL,

**URL:** llms-txt#initialize-the-tool-with-the-website-url,

---

## Initialize the tool with your API keys

**URL:** llms-txt#initialize-the-tool-with-your-api-keys

**Contents:**
- Command Types
  - 1. Act Command

stagehand_tool = StagehandTool(
    api_key="your-browserbase-api-key",
    project_id="your-browserbase-project-id",
    model_api_key="your-llm-api-key",
    model_name=AvailableModel.CLAUDE_3_7_SONNET_LATEST,
)

try:
    # Create an agent with the tool
    researcher = Agent(
        role="Web Researcher",
        goal="Find and summarize information from websites",
        backstory="I'm an expert at finding information online.",
        verbose=True,
        tools=[stagehand_tool],
    )

# Create a task that uses the tool
    research_task = Task(
        description="Go to https://www.example.com and tell me what you see on the homepage.",
        agent=researcher,
    )

# Run the crew
    crew = Crew(
        agents=[researcher],
        tasks=[research_task],
        verbose=True,
    )

result = crew.kickoff()
    print(result)
finally:
    # Explicitly clean up resources
    stagehand_tool.close()
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## Command Types

The StagehandTool supports three different command types for specific web automation tasks:

### 1. Act Command

The `act` command type (default) enables webpage interactions like clicking buttons, filling forms, and navigation.
```

---

## Initialize the tool with your API keys using a context manager

**URL:** llms-txt#initialize-the-tool-with-your-api-keys-using-a-context-manager

with StagehandTool(
    api_key="your-browserbase-api-key",
    project_id="your-browserbase-project-id",
    model_api_key="your-llm-api-key",  # OpenAI or Anthropic API key
    model_name=AvailableModel.CLAUDE_3_7_SONNET_LATEST,  # Optional: specify which model to use
) as stagehand_tool:
    # Create an agent with the tool
    researcher = Agent(
        role="Web Researcher",
        goal="Find and summarize information from websites",
        backstory="I'm an expert at finding information online.",
        verbose=True,
        tools=[stagehand_tool],
    )

# Create a task that uses the tool
    research_task = Task(
        description="Go to https://www.example.com and tell me what you see on the homepage.",
        agent=researcher,
    )

# Run the crew
    crew = Crew(
        agents=[researcher],
        tasks=[research_task],
        verbose=True,
    )

result = crew.kickoff()
    print(result)
python theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import StagehandTool
from stagehand.schemas import AvailableModel

**Examples:**

Example 1 (unknown):
```unknown
#### 2. Manual Resource Management
```

---

## Initialize the tool with your API key

**URL:** llms-txt#initialize-the-tool-with-your-api-key

tool = HyperbrowserLoadTool(api_key="your_api_key")  # Or use environment variable

---

## Initialize tools with session management

**URL:** llms-txt#initialize-tools-with-session-management

initial_tool = BedrockInvokeAgentTool(
    agent_id="your-agent-id",
    agent_alias_id="your-agent-alias-id",
    session_id="custom-session-id"
)

followup_tool = BedrockInvokeAgentTool(
    agent_id="your-agent-id",
    agent_alias_id="your-agent-alias-id",
    session_id="custom-session-id"
)

final_tool = BedrockInvokeAgentTool(
    agent_id="your-agent-id",
    agent_alias_id="your-agent-alias-id",
    session_id="custom-session-id",
    end_session=True
)

---

## Initialize tool with preset filter

**URL:** llms-txt#initialize-tool-with-preset-filter

**Contents:**
  - Combining Filters

qdrant_tool = QdrantVectorSearchTool(
    qdrant_config=QdrantConfig(
        qdrant_url="your_url",
        qdrant_api_key="your_key",
        collection_name="your_collection",
        filter=preset_filter  # Preset filter applied to all searches
    )
)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### Combining Filters

The tool automatically combines preset filters from `QdrantConfig` with dynamic filters from `filter_by` and `filter_value`:
```

---

## Instantiate tools

**URL:** llms-txt#instantiate-tools

docs_tool = DirectoryReadTool(directory='./blog-posts')
file_tool = FileReadTool()
search_tool = SerperDevTool()
web_rag_tool = WebsiteSearchTool()

---

## `JSONSearchTool`

**URL:** llms-txt#`jsonsearchtool`

**Contents:**
- Description
- Installation
- Usage Examples

<Note>
  The JSONSearchTool is currently in an experimental phase. This means the tool
  is under active development, and users might encounter unexpected behavior or
  changes. We highly encourage feedback on any issues or suggestions for
  improvements.
</Note>

The JSONSearchTool is designed to facilitate efficient and precise searches within JSON file contents. It utilizes a RAG (Retrieve and Generate) search mechanism, allowing users to specify a JSON path for targeted searches within a particular JSON file. This capability significantly improves the accuracy and relevance of search results.

To install the JSONSearchTool, use the following pip command:

Here are updated examples on how to utilize the JSONSearchTool effectively for searching within JSON files. These examples take into account the current implementation and usage patterns identified in the codebase.

```python Code theme={null}
from crewai_tools import JSONSearchTool

**Examples:**

Example 1 (unknown):
```unknown
## Usage Examples

Here are updated examples on how to utilize the JSONSearchTool effectively for searching within JSON files. These examples take into account the current implementation and usage patterns identified in the codebase.
```

---

## JSON RAG Search

**URL:** llms-txt#json-rag-search

Source: https://docs.crewai.com/en/tools/file-document/jsonsearchtool

The `JSONSearchTool` is designed to search JSON files and return the most relevant results.

---

## LangChain Tool

**URL:** llms-txt#langchain-tool

**Contents:**
- `LangChainTool`

Source: https://docs.crewai.com/en/tools/ai-ml/langchaintool

The `LangChainTool` is a wrapper for LangChain tools and query engines.

<Info>
  CrewAI seamlessly integrates with LangChain's comprehensive [list of tools](https://python.langchain.com/docs/integrations/tools/), all of which can be used with CrewAI.
</Info>

```python Code theme={null}
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from pydantic import Field
from langchain_community.utilities import GoogleSerperAPIWrapper

---

## Less efficient - gets all tools from server

**URL:** llms-txt#less-efficient---gets-all-tools-from-server

**Contents:**
  - 2. Handle Authentication Securely

mcps=["https://weather.api.com/mcp"]
python theme={null}
import os

**Examples:**

Example 1 (unknown):
```unknown
### 2. Handle Authentication Securely
```

---

## Linkup Search Tool

**URL:** llms-txt#linkup-search-tool

Source: https://docs.crewai.com/en/tools/search-research/linkupsearchtool

The `LinkupSearchTool` enables querying the Linkup API for contextual information.

---

## LlamaIndex Tool

**URL:** llms-txt#llamaindex-tool

Source: https://docs.crewai.com/en/tools/ai-ml/llamaindextool

The `LlamaIndexTool` is a wrapper for LlamaIndex tools and query engines.

---

## Loading Tools

**URL:** llms-txt#loading-tools

search_tool = SerperDevTool()

---

## Load all tools from the Tool Pack

**URL:** llms-txt#load-all-tools-from-the-tool-pack

tools = MergeAgentHandlerTool.from_tool_pack(
    tool_pack_id="134e0111-0f67-44f6-98f0-597000290bb3",
    registered_user_id="91b2b905-e866-40c8-8be2-efe53827a0aa"
)

---

## Load specific tools from the Tool Pack

**URL:** llms-txt#load-specific-tools-from-the-tool-pack

**Contents:**
- Tool Arguments
  - `from_tool_name()` Method
  - `from_tool_pack()` Method
- Environment Variables
- Advanced Usage
  - Multi-Agent Workflow with Different Tool Access

selected_tools = MergeAgentHandlerTool.from_tool_pack(
    tool_pack_id="134e0111-0f67-44f6-98f0-597000290bb3",
    registered_user_id="91b2b905-e866-40c8-8be2-efe53827a0aa",
    tool_names=["linear__create_issue", "linear__get_issues", "slack__post_message"]
)

developer_assistant = Agent(
    role='Developer Assistant',
    goal='Help developers track and communicate about their work',
    backstory='I help developers stay organized and keep the team informed.',
    tools=selected_tools,
    verbose=True
)

daily_update_task = Task(
    description="Get all issues assigned to the current user in Linear and post a summary to the #dev-updates Slack channel.",
    agent=developer_assistant
)

crew = Crew(
    agents=[developer_assistant],
    tasks=[daily_update_task],
    verbose=True
)

result = crew.kickoff()
bash theme={null}
AGENT_HANDLER_API_KEY=your_api_key_here  # Required for authentication
python {2, 4-20} theme={null}
from crewai import Agent, Task, Crew, Process
from crewai_tools import MergeAgentHandlerTool

**Examples:**

Example 1 (unknown):
```unknown
## Tool Arguments

### `from_tool_name()` Method

| Argument                 | Type  | Required | Default                                                | Description                                                        |
| :----------------------- | :---- | :------- | :----------------------------------------------------- | :----------------------------------------------------------------- |
| **tool\_name**           | `str` | Yes      | None                                                   | Name of the specific tool to use (e.g., "linear\_\_create\_issue") |
| **tool\_pack\_id**       | `str` | Yes      | None                                                   | UUID of your Agent Handler Tool Pack                               |
| **registered\_user\_id** | `str` | Yes      | None                                                   | UUID or origin\_id of the registered user                          |
| **base\_url**            | `str` | No       | "[https://ah-api.merge.dev](https://ah-api.merge.dev)" | Base URL for Agent Handler API                                     |
| **session\_id**          | `str` | No       | Auto-generated                                         | MCP session ID for maintaining context                             |

### `from_tool_pack()` Method

| Argument                 | Type        | Required | Default                                                | Description                                                     |
| :----------------------- | :---------- | :------- | :----------------------------------------------------- | :-------------------------------------------------------------- |
| **tool\_pack\_id**       | `str`       | Yes      | None                                                   | UUID of your Agent Handler Tool Pack                            |
| **registered\_user\_id** | `str`       | Yes      | None                                                   | UUID or origin\_id of the registered user                       |
| **tool\_names**          | `list[str]` | No       | None                                                   | Specific tool names to load. If None, loads all available tools |
| **base\_url**            | `str`       | No       | "[https://ah-api.merge.dev](https://ah-api.merge.dev)" | Base URL for Agent Handler API                                  |

## Environment Variables
```

Example 2 (unknown):
```unknown
## Advanced Usage

### Multi-Agent Workflow with Different Tool Access
```

---

## MCP connection is made only when a tool is actually executed

**URL:** llms-txt#mcp-connection-is-made-only-when-a-tool-is-actually-executed

---

## MCP tools are now automatically available!

**URL:** llms-txt#mcp-tools-are-now-automatically-available!

---

## MDX RAG Search

**URL:** llms-txt#mdx-rag-search

Source: https://docs.crewai.com/en/tools/file-document/mdxsearchtool

The `MDXSearchTool` is designed to search MDX files and return the most relevant results.

---

## `MongoDBVectorSearchTool`

**URL:** llms-txt#`mongodbvectorsearchtool`

**Contents:**
- Description
- Installation
- Parameters
  - Initialization
  - Run Parameters
- Quick start
- Index creation helpers
- Common issues
- More examples
  - Basic initialization

Perform vector similarity queries on MongoDB Atlas collections. Supports index creation helpers and bulk insert of embedded texts.

MongoDB Atlas supports native vector search. Learn more:
[https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview/](https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview/)

Install with the MongoDB extra:

* `connection_string` (str, required)
* `database_name` (str, required)
* `collection_name` (str, required)
* `vector_index_name` (str, default `vector_index`)
* `text_key` (str, default `text`)
* `embedding_key` (str, default `embedding`)
* `dimensions` (int, default `1536`)

* `query` (str, required): Natural language query to embed and search.

## Index creation helpers

Use `create_vector_search_index(...)` to provision an Atlas Vector Search index with the correct dimensions and similarity.

* Authentication failures: ensure your Atlas IP Access List allows your runner and the connection string includes credentials.
* Index not found: create the vector index first; name must match `vector_index_name`.
* Dimensions mismatch: align embedding model dimensions with `dimensions`.

### Basic initialization

### Custom query configuration

### Preloading the database and creating the index

```python Code theme={null}
import os
from crewai_tools import MongoDBVectorSearchTool

tool = MongoDBVectorSearchTool(
    database_name="example_database",
    collection_name="example_collection",
    connection_string="<your_mongodb_connection_string>",
)

**Examples:**

Example 1 (unknown):
```unknown
or
```

Example 2 (unknown):
```unknown
## Parameters

### Initialization

* `connection_string` (str, required)
* `database_name` (str, required)
* `collection_name` (str, required)
* `vector_index_name` (str, default `vector_index`)
* `text_key` (str, default `text`)
* `embedding_key` (str, default `embedding`)
* `dimensions` (int, default `1536`)

### Run Parameters

* `query` (str, required): Natural language query to embed and search.

## Quick start
```

Example 3 (unknown):
```unknown
## Index creation helpers

Use `create_vector_search_index(...)` to provision an Atlas Vector Search index with the correct dimensions and similarity.

## Common issues

* Authentication failures: ensure your Atlas IP Access List allows your runner and the connection string includes credentials.
* Index not found: create the vector index first; name must match `vector_index_name`.
* Dimensions mismatch: align embedding model dimensions with `dimensions`.

## More examples

### Basic initialization
```

Example 4 (unknown):
```unknown
### Custom query configuration
```

---

## MongoDB Vector Search Tool

**URL:** llms-txt#mongodb-vector-search-tool

Source: https://docs.crewai.com/en/tools/database-data/mongodbvectorsearchtool

The `MongoDBVectorSearchTool` performs vector search on MongoDB Atlas with optional indexing helpers.

---

## MySQL RAG Search

**URL:** llms-txt#mysql-rag-search

**Contents:**
- Overview
- Installation
- Example

Source: https://docs.crewai.com/en/tools/database-data/mysqltool

The `MySQLSearchTool` is designed to search MySQL databases and return the most relevant results.

This tool is designed to facilitate semantic searches within MySQL database tables. Leveraging the RAG (Retrieve and Generate) technology,
the MySQLSearchTool provides users with an efficient means of querying database table content, specifically tailored for MySQL databases.
It simplifies the process of finding relevant data through semantic search queries, making it an invaluable resource for users needing
to perform advanced queries on extensive datasets within a MySQL database.

To install the `crewai_tools` package and utilize the MySQLSearchTool, execute the following command in your terminal:

Below is an example showcasing how to use the MySQLSearchTool to conduct a semantic search on a table within a MySQL database:

```python Code theme={null}
from crewai_tools import MySQLSearchTool

**Examples:**

Example 1 (unknown):
```unknown
## Example

Below is an example showcasing how to use the MySQLSearchTool to conduct a semantic search on a table within a MySQL database:
```

---

## NL2SQL Tool

**URL:** llms-txt#nl2sql-tool

**Contents:**
- Overview
- Requirements
- Installation
- Usage

Source: https://docs.crewai.com/en/tools/database-data/nl2sqltool

The `NL2SQLTool` is designed to convert natural language to SQL queries.

This tool is used to convert natural language to SQL queries. When passed to the agent it will generate queries and then use them to interact with the database.

This enables multiple workflows like having an Agent to access the database fetch information based on the goal and then use the information to generate a response, report or any other output.
Along with that provides the ability for the Agent to update the database based on its goal.

**Attention**: Make sure that the Agent has access to a Read-Replica or that is okay for the Agent to run insert/update queries on the database.

* SqlAlchemy
* Any DB compatible library (e.g. psycopg2, mysql-connector-python)

Install the crewai\_tools package

In order to use the NL2SQLTool, you need to pass the database URI to the tool. The URI should be in the format `dialect+driver://username:password@host:port/database`.

```python Code theme={null}
from crewai_tools import NL2SQLTool

**Examples:**

Example 1 (unknown):
```unknown
## Usage

In order to use the NL2SQLTool, you need to pass the database URI to the tool. The URI should be in the format `dialect+driver://username:password@host:port/database`.
```

---

## No need for manual connection management or tool configuration

**URL:** llms-txt#no-need-for-manual-connection-management-or-tool-configuration

**Contents:**
- Supported Reference Formats
  - External MCP Remote Servers

**Examples:**

Example 1 (unknown):
```unknown
## Supported Reference Formats

### External MCP Remote Servers
```

---

## `OCRTool`

**URL:** llms-txt#`ocrtool`

**Contents:**
- Description
- Installation
- Parameters
  - Run Parameters
- Examples
  - Direct usage
  - With an agent
- Notes
- Example

Extract text from images (local path or URL). Uses a vision‑capable LLM via CrewAI’s LLM interface.

No extra install beyond `crewai-tools`. Ensure your selected LLM supports vision.

* `image_path_url` (str, required): Local image path or HTTP(S) URL.

* Ensure the selected LLM supports image inputs.
* For large images, consider downscaling to reduce token usage.
* You can pass a specific LLM instance to the tool (e.g., `LLM(model="gpt-4o")`) if needed, matching the README guidance.

**Examples:**

Example 1 (unknown):
```unknown
### With an agent
```

Example 2 (unknown):
```unknown
## Notes

* Ensure the selected LLM supports image inputs.
* For large images, consider downscaling to reduce token usage.
* You can pass a specific LLM instance to the tool (e.g., `LLM(model="gpt-4o")`) if needed, matching the README guidance.

## Example
```

---

## OCR Tool

**URL:** llms-txt#ocr-tool

Source: https://docs.crewai.com/en/tools/file-document/ocrtool

The `OCRTool` extracts text from local images or image URLs using an LLM with vision.

---

## OneDrive Trigger

**URL:** llms-txt#onedrive-trigger

**Contents:**
- Overview
- Enabling the OneDrive Trigger
- Example: Audit file permissions
- Testing Locally

Source: https://docs.crewai.com/en/enterprise/guides/onedrive-trigger

Automate responses to OneDrive file activity

Start automations when files change inside OneDrive. You can generate audit summaries, notify security teams about external sharing, or update downstream line-of-business systems with new document metadata.

<Tip>
  Connect OneDrive in **Tools & Integrations** and toggle the trigger on for your deployment.
</Tip>

## Enabling the OneDrive Trigger

1. Open your deployment in CrewAI AOP
2. Go to the **Triggers** tab
3. Locate **OneDrive** and switch the toggle to enable

<Frame>
  <img alt="Enable or disable triggers with toggle" />
</Frame>

## Example: Audit file permissions

The crew inspects file metadata, user activity, and permission changes to produce a compliance-friendly summary.

Test your OneDrive trigger integration locally using the CrewAI CLI:

**Examples:**

Example 1 (unknown):
```unknown
The crew inspects file metadata, user activity, and permission changes to produce a compliance-friendly summary.

## Testing Locally

Test your OneDrive trigger integration locally using the CrewAI CLI:
```

---

## Option 2: Printing the Entire Blog Object

**URL:** llms-txt#option-2:-printing-the-entire-blog-object

**Contents:**
- Integrating Tools with Tasks
- Creating a Task with Tools

print("Accessing Properties - Option 2")
print("Blog:", result)
python Code theme={null}
import os
os.environ["OPENAI_API_KEY"] = "Your Key"
os.environ["SERPER_API_KEY"] = "Your Key" # serper.dev API key

from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool

research_agent = Agent(
  role='Researcher',
  goal='Find and summarize the latest AI news',
  backstory="""You're a researcher at a large company.
  You're responsible for analyzing data and providing insights
  to the business.""",
  verbose=True
)

**Examples:**

Example 1 (unknown):
```unknown
In this example:

* A Pydantic model Blog is defined with title and content fields, which is used to specify the structure of the JSON output.
* The task task1 uses the output\_json property to indicate that it expects a JSON output conforming to the Blog model.
* After executing the crew, you can access the structured JSON output in two ways as shown.

#### Explanation of Accessing the Output

1. Accessing Properties Using Dictionary-Style Indexing: You can access the fields directly using result\["field\_name"]. This is possible because the CrewOutput class implements the **getitem** method, allowing you to treat the output like a dictionary. In this option, we're retrieving the title and content from the result.
2. Printing the Entire Blog Object: By printing result, you get the string representation of the CrewOutput object. Since the **str** method is implemented to return the JSON output, this will display the entire output as a formatted string representing the Blog object.

***

By using output\_pydantic or output\_json, you ensure that your tasks produce outputs in a consistent and structured format, making it easier to process and utilize the data within your application or across multiple tasks.

## Integrating Tools with Tasks

Leverage tools from the [CrewAI Toolkit](https://github.com/joaomdmoura/crewai-tools) and [LangChain Tools](https://python.langchain.com/docs/integrations/tools) for enhanced task performance and agent interaction.

## Creating a Task with Tools
```

---

## Original MCP server has tools: "search", "analyze"

**URL:** llms-txt#original-mcp-server-has-tools:-"search",-"analyze"

---

## Outlook Trigger

**URL:** llms-txt#outlook-trigger

**Contents:**
- Overview
- Enabling the Outlook Trigger
- Example: Summarize a new email
- Testing Locally

Source: https://docs.crewai.com/en/enterprise/guides/outlook-trigger

Launch automations from Outlook emails and calendar updates

Automate responses when Outlook delivers a new message or when an event is removed from the calendar. Teams commonly route escalations, file tickets, or alert attendees of cancellations.

<Tip>
  Connect Outlook in **Tools & Integrations** and ensure the trigger is enabled for your deployment.
</Tip>

## Enabling the Outlook Trigger

1. Open your deployment in CrewAI AOP
2. Go to the **Triggers** tab
3. Locate **Outlook** and switch the toggle to enable

<Frame>
  <img alt="Enable or disable triggers with toggle" />
</Frame>

## Example: Summarize a new email

The crew extracts sender details, subject, body preview, and attachments before generating a structured response.

Test your Outlook trigger integration locally using the CrewAI CLI:

**Examples:**

Example 1 (unknown):
```unknown
The crew extracts sender details, subject, body preview, and attachments before generating a structured response.

## Testing Locally

Test your Outlook trigger integration locally using the CrewAI CLI:
```

---

## Output: {'llm_hooks': (2, 1), 'tool_hooks': (1, 2), 'total': (3, 3)}

**URL:** llms-txt#output:-{'llm_hooks':-(2,-1),-'tool_hooks':-(1,-2),-'total':-(3,-3)}

**Contents:**
  - Clearing Specific Hook Types

python theme={null}
from crewai.hooks import (
    clear_before_llm_call_hooks,
    clear_after_llm_call_hooks,
    clear_before_tool_call_hooks,
    clear_after_tool_call_hooks
)

**Examples:**

Example 1 (unknown):
```unknown
### Clearing Specific Hook Types
```

---

## `OxylabsAmazonProductScraperTool`

**URL:** llms-txt#`oxylabsamazonproductscrapertool`

**Contents:**
  - Example

```python theme={null}
from crewai_tools import OxylabsAmazonProductScraperTool

---

## `OxylabsAmazonSearchScraperTool`

**URL:** llms-txt#`oxylabsamazonsearchscrapertool`

**Contents:**
  - Example

```python theme={null}
from crewai_tools import OxylabsAmazonSearchScraperTool

---

## `OxylabsGoogleSearchScraperTool`

**URL:** llms-txt#`oxylabsgooglesearchscrapertool`

**Contents:**
  - Example

```python theme={null}
from crewai_tools import OxylabsGoogleSearchScraperTool

---

## `OxylabsUniversalScraperTool`

**URL:** llms-txt#`oxylabsuniversalscrapertool`

**Contents:**
  - Example

```python theme={null}
from crewai_tools import OxylabsUniversalScraperTool

---

## Oxylabs Scrapers

**URL:** llms-txt#oxylabs-scrapers

**Contents:**
- Installation

Source: https://docs.crewai.com/en/tools/web-scraping/oxylabsscraperstool

Oxylabs Scrapers allow to easily access the information from the respective sources. Please see the list of available sources below:
  - `Amazon Product`
  - `Amazon Search`
  - `Google Seach`
  - `Universal`

Get the credentials by creating an Oxylabs Account [here](https://oxylabs.io).

Check [Oxylabs Documentation](https://developers.oxylabs.io/scraping-solutions/web-scraper-api/targets) to get more information about API parameters.

---

## `PDFSearchTool`

**URL:** llms-txt#`pdfsearchtool`

**Contents:**
- Description
- Installation
- Example

<Note>
  We are still working on improving tools, so there might be unexpected behavior or changes in the future.
</Note>

The PDFSearchTool is a RAG tool designed for semantic searches within PDF content. It allows for inputting a search query and a PDF document, leveraging advanced search techniques to find relevant content efficiently.
This capability makes it especially useful for extracting specific information from large PDF files quickly.

To get started with the PDFSearchTool, first, ensure the crewai\_tools package is installed with the following command:

Here's how to use the PDFSearchTool to search within a PDF document:

```python Code theme={null}
from crewai_tools import PDFSearchTool

**Examples:**

Example 1 (unknown):
```unknown
## Example

Here's how to use the PDFSearchTool to search within a PDF document:
```

---

## `PDFTextWritingTool`

**URL:** llms-txt#`pdftextwritingtool`

**Contents:**
- Description
- Parameters
  - Run Parameters
- Example
  - Direct usage
- Tips

Write text at precise coordinates on a PDF page, optionally embedding a custom TrueType font.

* `pdf_path` (str, required): Path to the input PDF.
* `text` (str, required): Text to add.
* `position` (tuple\[int, int], required): `(x, y)` coordinates.
* `font_size` (int, default `12`)
* `font_color` (str, default `"0 0 0 rg"`)
* `font_name` (str, default `"F1"`)
* `font_file` (str, optional): Path to `.ttf` file.
* `page_number` (int, default `0`)

* Coordinate origin is the bottom‑left corner.
* If using a custom font (`font_file`), ensure it is a valid `.ttf`.

**Examples:**

Example 1 (unknown):
```unknown
### Direct usage
```

---

## PDF RAG Search

**URL:** llms-txt#pdf-rag-search

Source: https://docs.crewai.com/en/tools/file-document/pdfsearchtool

The `PDFSearchTool` is designed to search PDF files and return the most relevant results.

---

## PDF Text Writing Tool

**URL:** llms-txt#pdf-text-writing-tool

Source: https://docs.crewai.com/en/tools/file-document/pdf-text-writing-tool

The `PDFTextWritingTool` writes text to specific positions in a PDF, supporting custom fonts.

---

## PG RAG Search

**URL:** llms-txt#pg-rag-search

**Contents:**
- Overview
- Description
- Installation
- Example Usage

Source: https://docs.crewai.com/en/tools/database-data/pgsearchtool

The `PGSearchTool` is designed to search PostgreSQL databases and return the most relevant results.

<Note>
  The PGSearchTool is currently under development. This document outlines the intended functionality and interface.
  As development progresses, please be aware that some features may not be available or could change.
</Note>

The PGSearchTool is envisioned as a powerful tool for facilitating semantic searches within PostgreSQL database tables. By leveraging advanced Retrieve and Generate (RAG) technology,
it aims to provide an efficient means for querying database table content, specifically tailored for PostgreSQL databases.
The tool's goal is to simplify the process of finding relevant data through semantic search queries, offering a valuable resource for users needing to conduct advanced queries on
extensive datasets within a PostgreSQL environment.

The `crewai_tools` package, which will include the PGSearchTool upon its release, can be installed using the following command:

<Note>
  The PGSearchTool is not yet available in the current version of the `crewai_tools` package. This installation command will be updated once the tool is released.
</Note>

Below is a proposed example showcasing how to use the PGSearchTool for conducting a semantic search on a table within a PostgreSQL database:

```python Code theme={null}
from crewai_tools import PGSearchTool

**Examples:**

Example 1 (unknown):
```unknown
<Note>
  The PGSearchTool is not yet available in the current version of the `crewai_tools` package. This installation command will be updated once the tool is released.
</Note>

## Example Usage

Below is a proposed example showcasing how to use the PGSearchTool for conducting a semantic search on a table within a PostgreSQL database:
```

---

## Process the results

**URL:** llms-txt#process-the-results

**Contents:**
  - Expected output
- Configuration
- Resources

for result in results:
    print(f"URL: {result['metadata']['url']}")
    print(f"Content: {result.get('markdown', 'N/A')[:100]}...")
text theme={null}
URL: https://www.example.com/crewai-intro
Content: CrewAI is a framework for building AI-powered workflows...
URL: https://docs.crewai.com/
Content: Official documentation for CrewAI...
python theme={null}
from crewai import Agent
from crewai_tools import ApifyActorsTool

rag_browser = ApifyActorsTool(actor_name="apify/rag-web-browser")

agent = Agent(
    role="Research Analyst",
    goal="Find and summarize information about specific topics",
    backstory="You are an experienced researcher with attention to detail",
    tools=[rag_browser],
)
```

You can run other Actors from [Apify Store](https://apify.com/store) simply by changing the `actor_name` and, when using it manually, adjusting the `run_input` based on the Actor input schema.

For an example of usage with agents, see the [CrewAI Actor template](https://apify.com/templates/python-crewai).

The `ApifyActorsTool` requires these inputs to work:

* **`actor_name`**
  The ID of the Apify Actor to run, e.g., `"apify/rag-web-browser"`. Browse all Actors on [Apify Store](https://apify.com/store).
* **`run_input`**
  A dictionary of input parameters for the Actor when running the tool manually.
  * For example, for the `apify/rag-web-browser` Actor: `{"query": "search term", "maxResults": 5}`
  * See the Actor's [input schema](https://apify.com/apify/rag-web-browser/input-schema) for the list of input parameters.

* **[Apify](https://apify.com/)**: Explore the Apify platform.
* **[How to build an AI agent on Apify](https://blog.apify.com/how-to-build-an-ai-agent/)** - A complete step-by-step guide to creating, publishing, and monetizing AI agents on the Apify platform.
* **[RAG Web Browser Actor](https://apify.com/apify/rag-web-browser)**: A popular Actor for web search for LLMs.
* **[CrewAI Integration Guide](https://docs.apify.com/platform/integrations/crewai)**: Follow the official guide for integrating Apify and CrewAI.

**Examples:**

Example 1 (unknown):
```unknown
### Expected output

Here is the output from running the code above:
```

Example 2 (unknown):
```unknown
The `ApifyActorsTool` automatically fetches the Actor definition and input schema from Apify using the provided `actor_name` and then constructs the tool description and argument schema. This means you need to specify only a valid `actor_name`, and the tool handles the rest when used with agents—no need to specify the `run_input`. Here's how it works:
```

---

## `RagTool`

**URL:** llms-txt#`ragtool`

**Contents:**
- Description
- Example

The `RagTool` is designed to answer questions by leveraging the power of Retrieval-Augmented Generation (RAG) through CrewAI's native RAG system.
It provides a dynamic knowledge base that can be queried to retrieve relevant information from various data sources.
This tool is particularly useful for applications that require access to a vast array of information and need to provide contextually relevant answers.

The following example demonstrates how to initialize the tool and use it with different data sources:

```python Code theme={null}
from crewai_tools import RagTool

---

## RAG Tool

**URL:** llms-txt#rag-tool

Source: https://docs.crewai.com/en/tools/ai-ml/ragtool

The `RagTool` is a dynamic knowledge base tool for answering questions using Retrieval-Augmented Generation.

---

## Results will be filtered where category == "technology"

**URL:** llms-txt#results-will-be-filtered-where-category-==-"technology"

**Contents:**
  - Preset Filters with QdrantConfig

python theme={null}
from qdrant_client.http import models as qmodels
from crewai_tools import QdrantVectorSearchTool, QdrantConfig

**Examples:**

Example 1 (unknown):
```unknown
### Preset Filters with QdrantConfig

For complex filtering, use Qdrant Filter instances in your configuration:
```

---

## Run a natural language query

**URL:** llms-txt#run-a-natural-language-query

**Contents:**
- Parameters
- Agent Integration Example

result = aimind_tool.run("How many 3 bedroom houses were sold in 2008?")
print(result)
python Code theme={null}
from crewai import Agent
from crewai.project import agent
from crewai_tools import AIMindTool

**Examples:**

Example 1 (unknown):
```unknown
## Parameters

The `AIMindTool` accepts the following parameters:

* **api\_key**: Optional. Your Minds API key. If not provided, it will be read from the `MINDS_API_KEY` environment variable.
* **datasources**: A list of dictionaries, each containing the following keys:
  * **description**: A description of the data contained in the datasource.
  * **engine**: The engine (or type) of the datasource.
  * **connection\_data**: A dictionary containing the connection parameters for the datasource.
  * **tables**: A list of tables that the data source will use. This is optional and can be omitted if all tables in the data source are to be used.

A list of supported data sources and their connection parameters can be found [here](https://docs.mdb.ai/docs/data_sources).

## Agent Integration Example

Here's how to integrate the `AIMindTool` with a CrewAI agent:
```

---

## Run the tool with input parameters

**URL:** llms-txt#run-the-tool-with-input-parameters

results = tool.run(run_input={"query": "What is CrewAI?", "maxResults": 5})

---

## Scrapegraph Scrape Tool

**URL:** llms-txt#scrapegraph-scrape-tool

Source: https://docs.crewai.com/en/tools/web-scraping/scrapegraphscrapetool

The `ScrapegraphScrapeTool` leverages Scrapegraph AI's SmartScraper API to intelligently extract content from websites.

---

## Scrape Website

**URL:** llms-txt#scrape-website

Source: https://docs.crewai.com/en/tools/web-scraping/scrapewebsitetool

The `ScrapeWebsiteTool` is designed to extract and read the content of a specified website.

---

## Scrapfly Scrape Website Tool

**URL:** llms-txt#scrapfly-scrape-website-tool

Source: https://docs.crewai.com/en/tools/web-scraping/scrapflyscrapetool

The `ScrapflyScrapeWebsiteTool` leverages Scrapfly's web scraping API to extract content from websites in various formats.

---

## Selenium Scraper

**URL:** llms-txt#selenium-scraper

Source: https://docs.crewai.com/en/tools/web-scraping/seleniumscrapingtool

The `SeleniumScrapingTool` is designed to extract and read the content of a specified website using Selenium.

---

## `SerpApiGoogleSearchTool`

**URL:** llms-txt#`serpapigooglesearchtool`

**Contents:**
- Description
- Installation
- Environment Variables
- Example
- Notes
- Parameters
  - Run Parameters
- Notes

Use the `SerpApiGoogleSearchTool` to run Google searches with SerpApi and retrieve structured results. Requires a SerpApi API key.

## Environment Variables

* `SERPAPI_API_KEY` (required): API key for SerpApi. Create one at [https://serpapi.com/](https://serpapi.com/) (free tier available).

* Set `SERPAPI_API_KEY` in the environment. Create a key at [https://serpapi.com/](https://serpapi.com/)
* See also Google Shopping via SerpApi: `/en/tools/search-research/serpapi-googleshoppingtool`

* `search_query` (str, required): The Google query.
* `location` (str, optional): Geographic location parameter.

* This tool wraps SerpApi and returns structured search results.

**Examples:**

Example 1 (unknown):
```unknown
## Environment Variables

* `SERPAPI_API_KEY` (required): API key for SerpApi. Create one at [https://serpapi.com/](https://serpapi.com/) (free tier available).

## Example
```

---

## `SerpApiGoogleShoppingTool`

**URL:** llms-txt#`serpapigoogleshoppingtool`

**Contents:**
- Description
- Installation
- Environment Variables
- Example
- Notes
- Parameters
  - Run Parameters

Leverage `SerpApiGoogleShoppingTool` to query Google Shopping via SerpApi and retrieve product-oriented results.

## Environment Variables

* `SERPAPI_API_KEY` (required): API key for SerpApi. Create one at [https://serpapi.com/](https://serpapi.com/) (free tier available).

* Set `SERPAPI_API_KEY` in the environment. Create a key at [https://serpapi.com/](https://serpapi.com/)
* See also Google Web Search via SerpApi: `/en/tools/search-research/serpapi-googlesearchtool`

* `search_query` (str, required): Product search query.
* `location` (str, optional): Geographic location parameter.

**Examples:**

Example 1 (unknown):
```unknown
## Environment Variables

* `SERPAPI_API_KEY` (required): API key for SerpApi. Create one at [https://serpapi.com/](https://serpapi.com/) (free tier available).

## Example
```

---

## SerpApi Google Search Tool

**URL:** llms-txt#serpapi-google-search-tool

Source: https://docs.crewai.com/en/tools/search-research/serpapi-googlesearchtool

The `SerpApiGoogleSearchTool` performs Google searches using the SerpApi service.

---

## SerpApi Google Shopping Tool

**URL:** llms-txt#serpapi-google-shopping-tool

Source: https://docs.crewai.com/en/tools/search-research/serpapi-googleshoppingtool

The `SerpApiGoogleShoppingTool` searches Google Shopping results using SerpApi.

---

## `SerperDevTool`

**URL:** llms-txt#`serperdevtool`

**Contents:**
- Description
- Installation
- Example

This tool is designed to perform a semantic search for a specified query from a text's content across the internet. It utilizes the [serper.dev](https://serper.dev) API
to fetch and display the most relevant search results based on the query provided by the user.

To effectively use the `SerperDevTool`, follow these steps:

1. **Package Installation**: Confirm that the `crewai[tools]` package is installed in your Python environment.
2. **API Key Acquisition**: Acquire a `serper.dev` API key at [https://serper.dev/](https://serper.dev/) (free tier available).
3. **Environment Configuration**: Store your obtained API key in an environment variable named `SERPER_API_KEY` to facilitate its use by the tool.

To incorporate this tool into your project, follow the installation instructions below:

The following example demonstrates how to initialize the tool and execute a search with a given query:

```python Code theme={null}
from crewai_tools import SerperDevTool

**Examples:**

Example 1 (unknown):
```unknown
## Example

The following example demonstrates how to initialize the tool and execute a search with a given query:
```

---

## Setup custom model for vectorizer and generative model

**URL:** llms-txt#setup-custom-model-for-vectorizer-and-generative-model

**Contents:**
- Preloading Documents

tool = WeaviateVectorSearchTool(
    collection_name='example_collections',
    limit=3,
    alpha=0.75,
    vectorizer=Configure.Vectorizer.text2vec_openai(model="nomic-embed-text"),
    generative_model=Configure.Generative.openai(model="gpt-4o-mini"),
    weaviate_cluster_url="https://your-weaviate-cluster-url.com",
    weaviate_api_key="your-weaviate-api-key",
)
python Code theme={null}
import os
from crewai_tools import WeaviateVectorSearchTool
import weaviate
from weaviate.classes.init import Auth

**Examples:**

Example 1 (unknown):
```unknown
## Preloading Documents

You can preload your Weaviate database with documents before using the tool:
```

---

## Set API keys for tool initialization

**URL:** llms-txt#set-api-keys-for-tool-initialization

os.environ["OPENAI_API_KEY"] = "Your Key"
os.environ["SERPER_API_KEY"] = "Your Key"

---

## `SingleStoreSearchTool`

**URL:** llms-txt#`singlestoresearchtool`

**Contents:**
- Description
- Installation
- Environment Variables
- Example

Execute read‑only queries (`SELECT`/`SHOW`) against SingleStore with connection pooling and input validation.

## Environment Variables

Variables like `SINGLESTOREDB_HOST`, `SINGLESTOREDB_USER`, `SINGLESTOREDB_PASSWORD`, etc., can be used, or `SINGLESTOREDB_URL` as a single DSN.

Generate the API key from the SingleStore dashboard, [docs here](https://docs.singlestore.com/cloud/reference/management-api/#generate-an-api-key).

**Examples:**

Example 1 (unknown):
```unknown
## Environment Variables

Variables like `SINGLESTOREDB_HOST`, `SINGLESTOREDB_USER`, `SINGLESTOREDB_PASSWORD`, etc., can be used, or `SINGLESTOREDB_URL` as a single DSN.

Generate the API key from the SingleStore dashboard, [docs here](https://docs.singlestore.com/cloud/reference/management-api/#generate-an-api-key).

## Example
```

---

## SingleStore Search Tool

**URL:** llms-txt#singlestore-search-tool

Source: https://docs.crewai.com/en/tools/database-data/singlestoresearchtool

The `SingleStoreSearchTool` safely executes SELECT/SHOW queries on SingleStore with pooling.

---

## Specific tool from AMP service

**URL:** llms-txt#specific-tool-from-amp-service

"crewai-amp:research-tools#pubmed_search"

---

## `SpiderTool`

**URL:** llms-txt#`spidertool`

**Contents:**
- Description
- Installation
- Example
- Arguments

[Spider](https://spider.cloud/?ref=crewai) is the [fastest](https://github.com/spider-rs/spider/blob/main/benches/BENCHMARKS.md#benchmark-results)
open source scraper and crawler that returns LLM-ready data.
It converts any website into pure HTML, markdown, metadata or text while enabling you to crawl with custom actions using AI.

To use the `SpiderTool` you need to download the [Spider SDK](https://pypi.org/project/spider-client/)
and the `crewai[tools]` SDK too:

This example shows you how you can use the `SpiderTool` to enable your agent to scrape and crawl websites.
The data returned from the Spider API is already LLM-ready, so no need to do any cleaning there.

| Argument                | Type     | Description                                                                                                                       |
| :---------------------- | :------- | :-------------------------------------------------------------------------------------------------------------------------------- |
| **api\_key**            | `string` | Specifies Spider API key. If not specified, it looks for `SPIDER_API_KEY` in environment variables.                               |
| **params**              | `object` | Optional parameters for the request. Defaults to `{"return_format": "markdown"}` to optimize content for LLMs.                    |
| **request**             | `string` | Type of request to perform (`http`, `chrome`, `smart`). `smart` defaults to HTTP, switching to JavaScript rendering if needed.    |
| **limit**               | `int`    | Max pages to crawl per website. Set to `0` or omit for unlimited.                                                                 |
| **depth**               | `int`    | Max crawl depth. Set to `0` for no limit.                                                                                         |
| **cache**               | `bool`   | Enables HTTP caching to speed up repeated runs. Default is `true`.                                                                |
| **budget**              | `object` | Sets path-based limits for crawled pages, e.g., `{"*":1}` for root page only.                                                     |
| **locale**              | `string` | Locale for the request, e.g., `en-US`.                                                                                            |
| **cookies**             | `string` | HTTP cookies for the request.                                                                                                     |
| **stealth**             | `bool`   | Enables stealth mode for Chrome requests to avoid detection. Default is `true`.                                                   |
| **headers**             | `object` | HTTP headers as a map of key-value pairs for all requests.                                                                        |
| **metadata**            | `bool`   | Stores metadata about pages and content, aiding AI interoperability. Defaults to `false`.                                         |
| **viewport**            | `object` | Sets Chrome viewport dimensions. Default is `800x600`.                                                                            |
| **encoding**            | `string` | Specifies encoding type, e.g., `UTF-8`, `SHIFT_JIS`.                                                                              |
| **subdomains**          | `bool`   | Includes subdomains in the crawl. Default is `false`.                                                                             |
| **user\_agent**         | `string` | Custom HTTP user agent. Defaults to a random agent.                                                                               |
| **store\_data**         | `bool`   | Enables data storage for the request. Overrides `storageless` when set. Default is `false`.                                       |
| **gpt\_config**         | `object` | Allows AI to generate crawl actions, with optional chaining steps via an array for `"prompt"`.                                    |
| **fingerprint**         | `bool`   | Enables advanced fingerprinting for Chrome.                                                                                       |
| **storageless**         | `bool`   | Prevents all data storage, including AI embeddings. Default is `false`.                                                           |
| **readability**         | `bool`   | Pre-processes content for reading via [Mozilla’s readability](https://github.com/mozilla/readability). Improves content for LLMs. |
| **return\_format**      | `string` | Format to return data: `markdown`, `raw`, `text`, `html2text`. Use `raw` for default page format.                                 |
| **proxy\_enabled**      | `bool`   | Enables high-performance proxies to avoid network-level blocking.                                                                 |
| **query\_selector**     | `string` | CSS query selector for content extraction from markup.                                                                            |
| **full\_resources**     | `bool`   | Downloads all resources linked to the website.                                                                                    |
| **request\_timeout**    | `int`    | Timeout in seconds for requests (5-60). Default is `30`.                                                                          |
| **run\_in\_background** | `bool`   | Runs the request in the background, useful for data storage and triggering dashboard crawls. No effect if `storageless` is set.   |

**Examples:**

Example 1 (unknown):
```unknown
## Example

This example shows you how you can use the `SpiderTool` to enable your agent to scrape and crawl websites.
The data returned from the Spider API is already LLM-ready, so no need to do any cleaning there.
```

---

## Spider Scraper

**URL:** llms-txt#spider-scraper

Source: https://docs.crewai.com/en/tools/web-scraping/spidertool

The `SpiderTool` is designed to extract and read the content of a specified website using Spider.

---

## Stagehand Tool

**URL:** llms-txt#stagehand-tool

Source: https://docs.crewai.com/en/tools/web-scraping/stagehandtool

Web automation tool that integrates Stagehand with CrewAI for browser interaction and automation

---

## Store API keys in environment variables

**URL:** llms-txt#store-api-keys-in-environment-variables

**Contents:**
  - 3. Plan for Server Failures

exa_key = os.getenv("EXA_API_KEY")
exa_profile = os.getenv("EXA_PROFILE")

agent = Agent(
    role="Secure Agent",
    goal="Use MCP tools securely",
    backstory="Security-conscious agent",
    mcps=[f"https://mcp.exa.ai/mcp?api_key={exa_key}&profile={exa_profile}"]
)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### 3. Plan for Server Failures
```

---

## The tool schema accepts filter_by and filter_value

**URL:** llms-txt#the-tool-schema-accepts-filter_by-and-filter_value

---

## The tool will automatically use OpenAI embeddings

**URL:** llms-txt#the-tool-will-automatically-use-openai-embeddings

---

## This minimizes connection overhead and improves startup performance

**URL:** llms-txt#this-minimizes-connection-overhead-and-improves-startup-performance

**Contents:**
- Integration with Existing Features
- Best Practices
  - 1. Use Specific Tools When Possible

python theme={null}
from crewai.tools import BaseTool

class CustomTool(BaseTool):
    name: str = "custom_analysis"
    description: str = "Custom analysis tool"

def _run(self, **kwargs):
        return "Custom analysis result"

agent = Agent(
    role="Full-Featured Agent",
    goal="Use all available tool types",
    backstory="Agent with comprehensive tool access",

# All tool types work together
    tools=[CustomTool()],                          # Custom tools
    apps=["gmail", "slack"],                       # Platform integrations
    mcps=[                                         # MCP servers
        "https://mcp.exa.ai/mcp?api_key=key",
        "crewai-amp:research-tools"
    ],

verbose=True,
    max_iter=15
)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## Integration with Existing Features

MCP tools work seamlessly with other CrewAI features:
```

Example 2 (unknown):
```unknown
## Best Practices

### 1. Use Specific Tools When Possible
```

---

## This prevents naming conflicts between different MCP servers

**URL:** llms-txt#this-prevents-naming-conflicts-between-different-mcp-servers

**Contents:**
- Error Handling and Resilience
  - Graceful Server Failures

python theme={null}
agent = Agent(
    role="Resilient Researcher",
    goal="Research despite server issues",
    backstory="Experienced researcher who adapts to available tools",
    mcps=[
        "https://primary-server.com/mcp",         # Primary data source
        "https://backup-server.com/mcp",          # Backup if primary fails
        "https://unreachable-server.com/mcp",     # Will be skipped with warning
        "crewai-amp:reliable-service"             # Reliable AMP service
    ]
)

**Examples:**

Example 1 (unknown):
```unknown
## Error Handling and Resilience

The MCP DSL is designed to be robust and user-friendly:

### Graceful Server Failures
```

---

## Tool Call Hooks

**URL:** llms-txt#tool-call-hooks

**Contents:**
- Overview
- Hook Types
  - Before Tool Call Hooks
  - After Tool Call Hooks
- Tool Hook Context
  - Modifying Tool Inputs

Source: https://docs.crewai.com/en/learn/tool-hooks

Learn how to use tool call hooks to intercept, modify, and control tool execution in CrewAI

Tool Call Hooks provide fine-grained control over tool execution during agent operations. These hooks allow you to intercept tool calls, modify inputs, transform outputs, implement safety checks, and add comprehensive logging or monitoring.

Tool hooks are executed at two critical points:

* **Before Tool Call**: Modify inputs, validate parameters, or block execution
* **After Tool Call**: Transform results, sanitize outputs, or log execution details

### Before Tool Call Hooks

Executed before every tool execution, these hooks can:

* Inspect and modify tool inputs
* Block tool execution based on conditions
* Implement approval gates for dangerous operations
* Validate parameters
* Log tool invocations

### After Tool Call Hooks

Executed after every tool execution, these hooks can:

* Modify or sanitize tool results
* Add metadata or formatting
* Log execution results
* Implement result validation
* Transform output formats

The `ToolCallHookContext` object provides comprehensive access to tool execution state:

### Modifying Tool Inputs

**Important:** Always modify tool inputs in-place:

```python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### After Tool Call Hooks

Executed after every tool execution, these hooks can:

* Modify or sanitize tool results
* Add metadata or formatting
* Log execution results
* Implement result validation
* Transform output formats

**Signature:**
```

Example 2 (unknown):
```unknown
## Tool Hook Context

The `ToolCallHookContext` object provides comprehensive access to tool execution state:
```

Example 3 (unknown):
```unknown
### Modifying Tool Inputs

**Important:** Always modify tool inputs in-place:
```

---

## Triggers Overview

**URL:** llms-txt#triggers-overview

**Contents:**
  - Integration Playbooks
- Trigger Capabilities
- Managing Triggers
  - Viewing Available Triggers
  - Enabling and Disabling Triggers
  - Monitoring Trigger Executions
- Building Trigger-Driven Automations
  - Trigger Setup Checklist
  - Testing Triggers Locally with CLI
  - Triggers with Crew

Source: https://docs.crewai.com/en/enterprise/guides/automation-triggers

Understand how CrewAI AOP triggers work, how to manage them, and where to find integration-specific playbooks

CrewAI AOP triggers connect your automations to real-time events across the tools your teams already use. Instead of polling systems or relying on manual kickoffs, triggers listen for changes—new emails, calendar updates, CRM status changes—and immediately launch the crew or flow you specify.

<Frame>
  <img alt="Automation Triggers Overview" />
</Frame>

### Integration Playbooks

Deep-dive guides walk through setup and sample workflows for each integration:

<CardGroup>
  <Card title="Gmail Trigger" icon="envelope">
    <a href="/en/enterprise/guides/gmail-trigger">Enable crews when emails arrive or threads update.</a>
  </Card>

<Card title="Google Calendar Trigger" icon="calendar-days">
    <a href="/en/enterprise/guides/google-calendar-trigger">React to calendar events as they are created, updated, or cancelled.</a>
  </Card>

<Card title="Google Drive Trigger" icon="folder-open">
    <a href="/en/enterprise/guides/google-drive-trigger">Handle Drive file uploads, edits, and deletions.</a>
  </Card>

<Card title="Outlook Trigger" icon="envelope-open">
    <a href="/en/enterprise/guides/outlook-trigger">Automate responses to new Outlook messages and calendar updates.</a>
  </Card>

<Card title="OneDrive Trigger" icon="cloud">
    <a href="/en/enterprise/guides/onedrive-trigger">Audit file activity and sharing changes in OneDrive.</a>
  </Card>

<Card title="Microsoft Teams Trigger" icon="comments">
    <a href="/en/enterprise/guides/microsoft-teams-trigger">Kick off workflows when new Teams chats start.</a>
  </Card>

<Card title="HubSpot Trigger" icon="hubspot">
    <a href="/en/enterprise/guides/hubspot-trigger">Launch automations from HubSpot workflows and lifecycle events.</a>
  </Card>

<Card title="Salesforce Trigger" icon="salesforce">
    <a href="/en/enterprise/guides/salesforce-trigger">Connect Salesforce processes to CrewAI for CRM automation.</a>
  </Card>

<Card title="Slack Trigger" icon="slack">
    <a href="/en/enterprise/guides/slack-trigger">Start crews directly from Slack slash commands.</a>
  </Card>

<Card title="Zapier Trigger" icon="bolt">
    <a href="/en/enterprise/guides/zapier-trigger">Bridge CrewAI with thousands of Zapier-supported apps.</a>
  </Card>
</CardGroup>

## Trigger Capabilities

With triggers, you can:

* **Respond to real-time events** - Automatically execute workflows when specific conditions are met
* **Integrate with external systems** - Connect with platforms like Gmail, Outlook, OneDrive, JIRA, Slack, Stripe and more
* **Scale your automation** - Handle high-volume events without manual intervention
* **Maintain context** - Access trigger data within your crews and flows

### Viewing Available Triggers

To access and manage your automation triggers:

1. Navigate to your deployment in the CrewAI dashboard
2. Click on the **Triggers** tab to view all available trigger integrations

<Frame>
  <img alt="List of available automation triggers" />
</Frame>

This view shows all the trigger integrations available for your deployment, along with their current connection status.

### Enabling and Disabling Triggers

Each trigger can be easily enabled or disabled using the toggle switch:

<Frame>
  <img alt="Enable or disable triggers with toggle" />
</Frame>

* **Enabled (blue toggle)**: The trigger is active and will automatically execute your deployment when the specified events occur
* **Disabled (gray toggle)**: The trigger is inactive and will not respond to events

Simply click the toggle to change the trigger state. Changes take effect immediately.

### Monitoring Trigger Executions

Track the performance and history of your triggered executions:

<Frame>
  <img alt="List of executions triggered by automation" />
</Frame>

## Building Trigger-Driven Automations

Before building your automation, it's helpful to understand the structure of trigger payloads that your crews and flows will receive.

### Trigger Setup Checklist

Before wiring a trigger into production, make sure you:

* Connect the integration under **Tools & Integrations** and complete any OAuth or API key steps
* Enable the trigger toggle on the deployment that should respond to events
* Provide any required environment variables (API tokens, tenant IDs, shared secrets)
* Create or update tasks that can parse the incoming payload within the first crew task or flow step
* Decide whether to pass trigger context automatically using `allow_crewai_trigger_context`
* Set up monitoring—webhook logs, CrewAI execution history, and optional external alerting

### Testing Triggers Locally with CLI

The CrewAI CLI provides powerful commands to help you develop and test trigger-driven automations without deploying to production.

#### List Available Triggers

View all available triggers for your connected integrations:

This command displays all triggers available based on your connected integrations, showing:

* Integration name and connection status
* Available trigger types
* Trigger names and descriptions

#### Simulate Trigger Execution

Test your crew with realistic trigger payloads before deployment:

* Executes your crew locally
* Passes a complete, realistic trigger payload
* Simulates exactly how your crew will be called in production

<Warning>
  **Important Development Notes:**

* Use `crewai triggers run <trigger>` to simulate trigger execution during development
  * Using `crewai run` will NOT simulate trigger calls and won't pass the trigger payload
  * After deployment, your crew will be executed with the actual trigger payload
  * If your crew expects parameters that aren't in the trigger payload, execution may fail
</Warning>

### Triggers with Crew

Your existing crew definitions work seamlessly with triggers, you just need to have a task to parse the received payload:

The crew will automatically receive and can access the trigger payload through the standard CrewAI context mechanisms.

<Note>
  Crew and Flow inputs can include `crewai_trigger_payload`. CrewAI automatically injects this payload:

* Tasks: appended to the first task's description by default ("Trigger Payload: ")
  * Control via `allow_crewai_trigger_context`: set `True` to always inject, `False` to never inject
  * Flows: any `@start()` method that accepts a `crewai_trigger_payload` parameter will receive it
</Note>

### Integration with Flows

For flows, you have more control over how trigger data is handled:

#### Accessing Trigger Payload

All `@start()` methods in your flows will accept an additional parameter called `crewai_trigger_payload`:

#### Triggering Crews from Flows

When kicking off a crew within a flow that was triggered, pass the trigger payload as it:

**Trigger not firing:**

* Verify the trigger is enabled in your deployment's Triggers tab
* Check integration connection status under Tools & Integrations
* Ensure all required environment variables are properly configured

**Execution failures:**

* Check the execution logs for error details
* Use `crewai triggers run <trigger_name>` to test locally and see the exact payload structure
* Verify your crew can handle the `crewai_trigger_payload` parameter
* Ensure your crew doesn't expect parameters that aren't included in the trigger payload

**Development issues:**

* Always test with `crewai triggers run <trigger>` before deploying to see the complete payload
* Remember that `crewai run` does NOT simulate trigger calls—use `crewai triggers run` instead
* Use `crewai triggers list` to verify which triggers are available for your connected integrations
* After deployment, your crew will receive the actual trigger payload, so test thoroughly locally first

Automation triggers transform your CrewAI deployments into responsive, event-driven systems that can seamlessly integrate with your existing business processes and tools.

**Examples:**

Example 1 (unknown):
```unknown
This command displays all triggers available based on your connected integrations, showing:

* Integration name and connection status
* Available trigger types
* Trigger names and descriptions

#### Simulate Trigger Execution

Test your crew with realistic trigger payloads before deployment:
```

Example 2 (unknown):
```unknown
For example:
```

Example 3 (unknown):
```unknown
This command:

* Executes your crew locally
* Passes a complete, realistic trigger payload
* Simulates exactly how your crew will be called in production

<Warning>
  **Important Development Notes:**

  * Use `crewai triggers run <trigger>` to simulate trigger execution during development
  * Using `crewai run` will NOT simulate trigger calls and won't pass the trigger payload
  * After deployment, your crew will be executed with the actual trigger payload
  * If your crew expects parameters that aren't in the trigger payload, execution may fail
</Warning>

### Triggers with Crew

Your existing crew definitions work seamlessly with triggers, you just need to have a task to parse the received payload:
```

Example 4 (unknown):
```unknown
The crew will automatically receive and can access the trigger payload through the standard CrewAI context mechanisms.

<Note>
  Crew and Flow inputs can include `crewai_trigger_payload`. CrewAI automatically injects this payload:

  * Tasks: appended to the first task's description by default ("Trigger Payload: ")
  * Control via `allow_crewai_trigger_context`: set `True` to always inject, `False` to never inject
  * Flows: any `@start()` method that accepts a `crewai_trigger_payload` parameter will receive it
</Note>

### Integration with Flows

For flows, you have more control over how trigger data is handled:

#### Accessing Trigger Payload

All `@start()` methods in your flows will accept an additional parameter called `crewai_trigger_payload`:
```

---

## TXT RAG Search

**URL:** llms-txt#txt-rag-search

**Contents:**
- Overview
- Installation
- Example

Source: https://docs.crewai.com/en/tools/file-document/txtsearchtool

The `TXTSearchTool` is designed to perform a RAG (Retrieval-Augmented Generation) search within the content of a text file.

<Note>
  We are still working on improving tools, so there might be unexpected behavior or changes in the future.
</Note>

This tool is used to perform a RAG (Retrieval-Augmented Generation) search within the content of a text file.
It allows for semantic searching of a query within a specified text file's content,
making it an invaluable resource for quickly extracting information or finding specific sections of text based on the query provided.

To use the `TXTSearchTool`, you first need to install the `crewai_tools` package.
This can be done using pip, a package manager for Python.
Open your terminal or command prompt and enter the following command:

This command will download and install the TXTSearchTool along with any necessary dependencies.

The following example demonstrates how to use the TXTSearchTool to search within a text file.
This example shows both the initialization of the tool with a specific text file and the subsequent search within that file's content.

```python Code theme={null}
from crewai_tools import TXTSearchTool

**Examples:**

Example 1 (unknown):
```unknown
This command will download and install the TXTSearchTool along with any necessary dependencies.

## Example

The following example demonstrates how to use the TXTSearchTool to search within a text file.
This example shows both the initialization of the tool with a specific text file and the subsequent search within that file's content.
```

---

## Use custom embeddings with the tool

**URL:** llms-txt#use-custom-embeddings-with-the-tool

**Contents:**
- Error Handling
- Environment Variables

from crewai_tools import QdrantConfig

tool = QdrantVectorSearchTool(
    qdrant_config=QdrantConfig(
        qdrant_url="your_url",
        qdrant_api_key="your_key",
        collection_name="your_collection"
    ),
    custom_embedding_fn=custom_embeddings  # Pass your custom function
)
bash theme={null}
export QDRANT_URL="your_qdrant_url"  # If not provided in constructor
export QDRANT_API_KEY="your_api_key"  # If not provided in constructor
export OPENAI_API_KEY="your_openai_key"  # If using default embeddings
```

**Examples:**

Example 1 (unknown):
```unknown
## Error Handling

The tool handles these specific errors:

* Raises ImportError if `qdrant-client` is not installed (with option to auto-install)
* Raises ValueError if `QDRANT_URL` is not set
* Prompts to install `qdrant-client` if missing using `uv add qdrant-client`

## Environment Variables

Required environment variables:
```

---

## Using MCPServerAdapter with a context manager

**URL:** llms-txt#using-mcpserveradapter-with-a-context-manager

**Contents:**
  - 2. Manual Connection Lifecycle
- Security Considerations for SSE

try:
    with MCPServerAdapter(server_params) as tools:
        print(f"Available tools from SSE MCP server: {[tool.name for tool in tools]}")

# Example: Using a tool from the SSE MCP server
        sse_agent = Agent(
            role="Remote Service User",
            goal="Utilize a tool provided by a remote SSE MCP server.",
            backstory="An AI agent that connects to external services via SSE.",
            tools=tools,
            reasoning=True,
            verbose=True,
        )

sse_task = Task(
            description="Fetch real-time stock updates for 'AAPL' using an SSE tool.",
            expected_output="The latest stock price for AAPL.",
            agent=sse_agent,
            markdown=True
        )

sse_crew = Crew(
            agents=[sse_agent],
            tasks=[sse_task],
            verbose=True,
            process=Process.sequential
        )
        
        if tools: # Only kickoff if tools were loaded
            result = sse_crew.kickoff() # Add inputs={'stock_symbol': 'AAPL'} if tool requires it
            print("\nCrew Task Result (SSE - Managed):\n", result)
        else:
            print("Skipping crew kickoff as tools were not loaded (check server connection).")

except Exception as e:
    print(f"Error connecting to or using SSE MCP server (Managed): {e}")
    print("Ensure the SSE MCP server is running and accessible at the specified URL.")

python theme={null}
from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter

server_params = {
    "url": "http://localhost:8000/sse", # Replace with your actual SSE server URL
    "transport": "sse"
}

mcp_server_adapter = None 
try:
    mcp_server_adapter = MCPServerAdapter(server_params)
    mcp_server_adapter.start()
    tools = mcp_server_adapter.tools
    print(f"Available tools (manual SSE): {[tool.name for tool in tools]}")

manual_sse_agent = Agent(
        role="Remote Data Analyst",
        goal="Analyze data fetched from a remote SSE MCP server using manual connection management.",
        backstory="An AI skilled in handling SSE connections explicitly.",
        tools=tools,
        verbose=True
    )
    
    analysis_task = Task(
        description="Fetch and analyze the latest user activity trends from the SSE server.",
        expected_output="A summary report of user activity trends.",
        agent=manual_sse_agent
    )
    
    analysis_crew = Crew(
        agents=[manual_sse_agent],
        tasks=[analysis_task],
        verbose=True,
        process=Process.sequential
    )
    
    result = analysis_crew.kickoff()
    print("\nCrew Task Result (SSE - Manual):\n", result)

except Exception as e:
    print(f"An error occurred during manual SSE MCP integration: {e}")
    print("Ensure the SSE MCP server is running and accessible.")
finally:
    if mcp_server_adapter and mcp_server_adapter.is_connected:
        print("Stopping SSE MCP server connection (manual)...")
        mcp_server_adapter.stop()  # **Crucial: Ensure stop is called**
    elif mcp_server_adapter:
        print("SSE MCP server adapter was not connected. No stop needed or start failed.")

## Security Considerations for SSE

<Warning>
  **DNS Rebinding Attacks**: SSE transports can be vulnerable to DNS rebinding attacks if the MCP server is not properly secured. This could allow malicious websites to interact with local or intranet-based MCP servers.
</Warning>

To mitigate this risk:

* MCP server implementations should **validate `Origin` headers** on incoming SSE connections.
* When running local SSE MCP servers for development, **bind only to `localhost` (`127.0.0.1`)** rather than all network interfaces (`0.0.0.0`).
* Implement **proper authentication** for all SSE connections if they expose sensitive tools or data.

For a comprehensive overview of security best practices, please refer to our [Security Considerations](./security.mdx) page and the official [MCP Transport Security documentation](https://modelcontextprotocol.io/docs/concepts/transports#security-considerations).

**Examples:**

Example 1 (unknown):
```unknown
<Note>
  Replace `"http://localhost:8000/sse"` with the actual URL of your SSE MCP server.
</Note>

### 2. Manual Connection Lifecycle

If you need finer-grained control, you can manage the `MCPServerAdapter` connection lifecycle manually.

<Info>
  You **MUST** call `mcp_server_adapter.stop()` to ensure the connection is closed and resources are released. Using a `try...finally` block is highly recommended.
</Info>
```

---

## Using Tool: Search the internet

**URL:** llms-txt#using-tool:-search-the-internet

---

## Verify connection

**URL:** llms-txt#verify-connection

**Contents:**
  - Step 3: Initialize OpenLit
  - Step 4: Create a Simple CrewAI Application
  - Step 5: See Traces in Langfuse
- References

if langfuse.auth_check():
    print("Langfuse client is authenticated and ready!")
else:
    print("Authentication failed. Please check your credentials and host.")
python theme={null}
import openlit

openlit.init()
python theme={null}
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

task = Task(description=("What is {multiplication}?"),
            expected_output=("Compose a haiku that includes the answer."),
            agent=writer)

crew = Crew(
  agents=[writer],
  tasks=[task],
  share_crew=False
)
```

### Step 5: See Traces in Langfuse

After running the agent, you can view the traces generated by your CrewAI application in [Langfuse](https://cloud.langfuse.com). You should see detailed steps of the LLM interactions, which can help you debug and optimize your AI agent.

![CrewAI example trace in Langfuse](https://langfuse.com/images/cookbook/integration_crewai/crewai-example-trace.png)

*[Public example trace in Langfuse](https://cloud.langfuse.com/project/cloramnkj0002jz088vzn1ja4/traces/e2cf380ffc8d47d28da98f136140642b?timestamp=2025-02-05T15%3A12%3A02.717Z\&observation=3b32338ee6a5d9af)*

* [Langfuse OpenTelemetry Docs](https://langfuse.com/docs/opentelemetry/get-started)

**Examples:**

Example 1 (unknown):
```unknown
### Step 3: Initialize OpenLit

Initialize the OpenLit OpenTelemetry instrumentation SDK to start capturing OpenTelemetry traces.
```

Example 2 (unknown):
```unknown
### Step 4: Create a Simple CrewAI Application

We'll create a simple CrewAI application where multiple agents collaborate to answer a user's question.
```

---

## `VisionTool`

**URL:** llms-txt#`visiontool`

**Contents:**
- Description
- Installation
- Usage
- Arguments

This tool is used to extract text from images. When passed to the agent it will extract the text from the image and then use it to generate a response, report or any other output.
The URL or the PATH of the image should be passed to the Agent.

Install the crewai\_tools package

In order to use the VisionTool, the OpenAI API key should be set in the environment variable `OPENAI_API_KEY`.

The VisionTool requires the following arguments:

| Argument             | Type     | Description                                                                      |
| :------------------- | :------- | :------------------------------------------------------------------------------- |
| **image\_path\_url** | `string` | **Mandatory**. The path to the image file from which text needs to be extracted. |

**Examples:**

Example 1 (unknown):
```unknown
## Usage

In order to use the VisionTool, the OpenAI API key should be set in the environment variable `OPENAI_API_KEY`.
```

---

## Vision Tool

**URL:** llms-txt#vision-tool

Source: https://docs.crewai.com/en/tools/ai-ml/visiontool

The `VisionTool` is designed to extract text from images.

---

## Weaviate Vector Search

**URL:** llms-txt#weaviate-vector-search

**Contents:**
- Overview
- Installation
- Steps to Get Started
- Example

Source: https://docs.crewai.com/en/tools/database-data/weaviatevectorsearchtool

The `WeaviateVectorSearchTool` is designed to search a Weaviate vector database for semantically similar documents using hybrid search.

The `WeaviateVectorSearchTool` is specifically crafted for conducting semantic searches within documents stored in a Weaviate vector database. This tool allows you to find semantically similar documents to a given query, leveraging the power of vector and keyword search for more accurate and contextually relevant search results.

[Weaviate](https://weaviate.io/) is a vector database that stores and queries vector embeddings, enabling semantic search capabilities.

To incorporate this tool into your project, you need to install the Weaviate client:

## Steps to Get Started

To effectively use the `WeaviateVectorSearchTool`, follow these steps:

1. **Package Installation**: Confirm that the `crewai[tools]` and `weaviate-client` packages are installed in your Python environment.
2. **Weaviate Setup**: Set up a Weaviate cluster. You can follow the [Weaviate documentation](https://weaviate.io/developers/wcs/manage-clusters/connect) for instructions.
3. **API Keys**: Obtain your Weaviate cluster URL and API key.
4. **OpenAI API Key**: Ensure you have an OpenAI API key set in your environment variables as `OPENAI_API_KEY`.

The following example demonstrates how to initialize the tool and execute a search:

```python Code theme={null}
from crewai_tools import WeaviateVectorSearchTool

**Examples:**

Example 1 (unknown):
```unknown
## Steps to Get Started

To effectively use the `WeaviateVectorSearchTool`, follow these steps:

1. **Package Installation**: Confirm that the `crewai[tools]` and `weaviate-client` packages are installed in your Python environment.
2. **Weaviate Setup**: Set up a Weaviate cluster. You can follow the [Weaviate documentation](https://weaviate.io/developers/wcs/manage-clusters/connect) for instructions.
3. **API Keys**: Obtain your Weaviate cluster URL and API key.
4. **OpenAI API Key**: Ensure you have an OpenAI API key set in your environment variables as `OPENAI_API_KEY`.

## Example

The following example demonstrates how to initialize the tool and execute a search:
```

---

## `WebsiteSearchTool`

**URL:** llms-txt#`websitesearchtool`

**Contents:**
- Description
- Installation
- Example Usage

<Note>
  The WebsiteSearchTool is currently in an experimental phase. We are actively working on incorporating this tool into our suite of offerings and will update the documentation accordingly.
</Note>

The WebsiteSearchTool is designed as a concept for conducting semantic searches within the content of websites.
It aims to leverage advanced machine learning models like Retrieval-Augmented Generation (RAG) to navigate and extract information from specified URLs efficiently.
This tool intends to offer flexibility, allowing users to perform searches across any website or focus on specific websites of interest.
Please note, the current implementation details of the WebsiteSearchTool are under development, and its functionalities as described may not yet be accessible.

To prepare your environment for when the WebsiteSearchTool becomes available, you can install the foundational package with:

This command installs the necessary dependencies to ensure that once the tool is fully integrated, users can start using it immediately.

Below are examples of how the WebsiteSearchTool could be utilized in different scenarios. Please note, these examples are illustrative and represent planned functionality:

```python Code theme={null}
from crewai_tools import WebsiteSearchTool

**Examples:**

Example 1 (unknown):
```unknown
This command installs the necessary dependencies to ensure that once the tool is fully integrated, users can start using it immediately.

## Example Usage

Below are examples of how the WebsiteSearchTool could be utilized in different scenarios. Please note, these examples are illustrative and represent planned functionality:
```

---

## Website RAG Search

**URL:** llms-txt#website-rag-search

Source: https://docs.crewai.com/en/tools/search-research/websitesearchtool

The `WebsiteSearchTool` is designed to perform a RAG (Retrieval-Augmented Generation) search within the content of a website.

---

## Wrap it with LlamaIndexTool

**URL:** llms-txt#wrap-it-with-llamaindextool

tool = LlamaIndexTool.from_tool(og_tool)

---

## `XMLSearchTool`

**URL:** llms-txt#`xmlsearchtool`

**Contents:**
- Description
- Installation
- Example

<Note>
  We are still working on improving tools, so there might be unexpected behavior or changes in the future.
</Note>

The XMLSearchTool is a cutting-edge RAG tool engineered for conducting semantic searches within XML files.
Ideal for users needing to parse and extract information from XML content efficiently, this tool supports inputting a search query and an optional XML file path.
By specifying an XML path, users can target their search more precisely to the content of that file, thereby obtaining more relevant search outcomes.

To start using the XMLSearchTool, you must first install the crewai\_tools package. This can be easily done with the following command:

Here are two examples demonstrating how to use the XMLSearchTool.
The first example shows searching within a specific XML file, while the second example illustrates initiating a search without predefining an XML path, providing flexibility in search scope.

```python Code theme={null}
from crewai_tools import XMLSearchTool

**Examples:**

Example 1 (unknown):
```unknown
## Example

Here are two examples demonstrating how to use the XMLSearchTool.
The first example shows searching within a specific XML file, while the second example illustrates initiating a search without predefining an XML path, providing flexibility in search scope.
```

---

## XML RAG Search

**URL:** llms-txt#xml-rag-search

Source: https://docs.crewai.com/en/tools/file-document/xmlsearchtool

The `XMLSearchTool` is designed to perform a RAG (Retrieval-Augmented Generation) search within the content of a XML file.

---

## `YoutubeChannelSearchTool`

**URL:** llms-txt#`youtubechannelsearchtool`

**Contents:**
- Description
- Installation
- Example

<Note>
  We are still working on improving tools, so there might be unexpected behavior or changes in the future.
</Note>

This tool is designed to perform semantic searches within a specific Youtube channel's content.
Leveraging the RAG (Retrieval-Augmented Generation) methodology, it provides relevant search results,
making it invaluable for extracting information or finding specific content without the need to manually sift through videos.
It streamlines the search process within Youtube channels, catering to researchers, content creators, and viewers seeking specific information or topics.

To utilize the YoutubeChannelSearchTool, the `crewai_tools` package must be installed. Execute the following command in your shell to install:

The following example demonstrates how to use the `YoutubeChannelSearchTool` with a CrewAI agent:

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import YoutubeChannelSearchTool

**Examples:**

Example 1 (unknown):
```unknown
## Example

The following example demonstrates how to use the `YoutubeChannelSearchTool` with a CrewAI agent:
```

---

## `YoutubeVideoSearchTool`

**URL:** llms-txt#`youtubevideosearchtool`

**Contents:**
- Description
- Installation
- Example

<Note>
  We are still working on improving tools, so there might be unexpected behavior or changes in the future.
</Note>

This tool is part of the `crewai_tools` package and is designed to perform semantic searches within Youtube video content, utilizing Retrieval-Augmented Generation (RAG) techniques.
It is one of several "Search" tools in the package that leverage RAG for different sources.
The YoutubeVideoSearchTool allows for flexibility in searches; users can search across any Youtube video content without specifying a video URL,
or they can target their search to a specific Youtube video by providing its URL.

To utilize the `YoutubeVideoSearchTool`, you must first install the `crewai_tools` package.
This package contains the `YoutubeVideoSearchTool` among other utilities designed to enhance your data analysis and processing tasks.
Install the package by executing the following command in your terminal:

The following example demonstrates how to use the `YoutubeVideoSearchTool` with a CrewAI agent:

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import YoutubeVideoSearchTool

**Examples:**

Example 1 (unknown):
```unknown
## Example

The following example demonstrates how to use the `YoutubeVideoSearchTool` with a CrewAI agent:
```

---

## YouTube Channel RAG Search

**URL:** llms-txt#youtube-channel-rag-search

Source: https://docs.crewai.com/en/tools/search-research/youtubechannelsearchtool

The `YoutubeChannelSearchTool` is designed to perform a RAG (Retrieval-Augmented Generation) search within the content of a Youtube channel.

---

## YouTube Video RAG Search

**URL:** llms-txt#youtube-video-rag-search

Source: https://docs.crewai.com/en/tools/search-research/youtubevideosearchtool

The `YoutubeVideoSearchTool` is designed to perform a RAG (Retrieval-Augmented Generation) search within the content of a Youtube video.

---

## Zapier Actions Tool

**URL:** llms-txt#zapier-actions-tool

Source: https://docs.crewai.com/en/tools/automation/zapieractionstool

The `ZapierActionsAdapter` exposes Zapier actions as CrewAI tools for automation.

---

## - Tool call blocked

**URL:** llms-txt#--tool-call-blocked

**Contents:**
- Related Documentation
- Conclusion

## Related Documentation

* [LLM Call Hooks →](/learn/llm-hooks) - Detailed LLM hook documentation
* [Tool Call Hooks →](/learn/tool-hooks) - Detailed tool hook documentation
* [Before and After Kickoff Hooks →](/learn/before-and-after-kickoff-hooks) - Crew lifecycle hooks
* [Human-in-the-Loop →](/learn/human-in-the-loop) - Human input patterns

Execution hooks provide powerful control over agent runtime behavior. Use them to implement safety guardrails, approval workflows, comprehensive monitoring, and custom business logic. Combined with proper error handling, type safety, and performance considerations, hooks enable production-ready, secure, and observable agent systems.

---
