# Langchain - Chains

**Pages:** 22

---

## API Reference: https://api.smith.langchain.com/redoc#tag/datasets/operation/create_comparative_experiment_api_v1_datasets_comparative_post

**URL:** llms-txt#api-reference:-https://api.smith.langchain.com/redoc#tag/datasets/operation/create_comparative_experiment_api_v1_datasets_comparative_post

resp = requests.post(
    "https://api.smith.langchain.com/api/v1/datasets/comparative",
    json={
        "experiment_ids": experiment_ids,
        "name": "Toxicity detection - API Example - Comparative - " + str(uuid4())[0:8],
        "description": "An optional description for the comparative experiment",
        "extra": {
            "metadata": {"foo": "bar"},  # Optional metadata
        },
        "reference_dataset_id": str(dataset_id),
    },
    headers={"x-api-key": os.environ["LANGSMITH_API_KEY"]}
)

comparative_experiment = resp.json()
comparative_experiment_id = comparative_experiment["id"]

---

## API Reference: https://api.smith.langchain.com/redoc#tag/examples/operation/read_examples_api_v1_examples_get

**URL:** llms-txt#api-reference:-https://api.smith.langchain.com/redoc#tag/examples/operation/read_examples_api_v1_examples_get

dataset_id = dataset.id
params = { "dataset": dataset_id }

resp = requests.get(
    "https://api.smith.langchain.com/api/v1/examples",
    params=params,
    headers={"x-api-key": os.environ["LANGSMITH_API_KEY"]}
)

examples = resp.json()
python  theme={null}
os.environ["OPENAI_API_KEY"] = "sk-..."

def run_completion_on_example(example, model_name, experiment_id):
    """Run completions on a list of examples."""
    # We are using the OpenAI API here, but you can use any model you like

def _post_run(run_id, name, run_type, inputs, parent_id=None):
        """Function to post a new run to the API.
        API Reference: https://api.smith.langchain.com/redoc#tag/run/operation/create_run_api_v1_runs_post
        """
        data = {
            "id": run_id.hex,
            "name": name,
            "run_type": run_type,
            "inputs": inputs,
            "start_time": datetime.utcnow().isoformat(),
            "reference_example_id": example["id"],
            "session_id": experiment_id,
        }
        if parent_id:
            data["parent_run_id"] = parent_id.hex
        resp = requests.post(
            "https://api.smith.langchain.com/api/v1/runs", # Update appropriately for self-hosted installations or the EU region
            json=data,
            headers=headers
        )
        resp.raise_for_status()

def _patch_run(run_id, outputs):
        """Function to patch a run with outputs.
        API Reference: https://api.smith.langchain.com/redoc#tag/run/operation/update_run_api_v1_runs__run_id__patch
        """
        resp = requests.patch(
            f"https://api.smith.langchain.com/api/v1/runs/{run_id}",
            json={
                "outputs": outputs,
                "end_time": datetime.utcnow().isoformat(),
            },
            headers=headers,
        )
        resp.raise_for_status()

# Send your API Key in the request headers
    headers = {"x-api-key": os.environ["LANGSMITH_API_KEY"]}

text = example["inputs"]["text"]

messages = [
        {
            "role": "system",
            "content": "Please review the user query below and determine if it contains any form of toxic behavior, such as insults, threats, or highly negative comments. Respond with 'Toxic' if it does, and 'Not toxic' if it doesn't.",
        },
        {"role": "user", "content": text},
    ]

# Create parent run
    parent_run_id = uuid7()
    _post_run(parent_run_id, "LLM Pipeline", "chain", {"text": text})

# Create child run
    child_run_id = uuid7()
    _post_run(child_run_id, "OpenAI Call", "llm", {"messages": messages}, parent_run_id)

# Generate completion
    chat_completion = oa_client.chat.completions.create(model=model_name, messages=messages)
    output_text = chat_completion.choices[0].message.content

# End run
    _patch_run(child_run_id, {
    "messages": messages,
        "output": output_text,
        "model": model_name
    })

_patch_run(parent_run_id, {"label": output_text})
python  theme={null}

**Examples:**

Example 1 (unknown):
```unknown
from langsmith import uuid7

Next, define a function that will run your model on a single example and log the results to LangSmith. When using the API directly, you're responsible for:

* Creating run objects via POST to `/runs` with `reference_example_id` and `session_id` set.
* Tracking parent-child relationships between runs (e.g., a parent "chain" run containing a child "llm" run).
* Updating runs with outputs via PATCH to `/runs/{run_id}`.
```

Example 2 (unknown):
```unknown
Now create the experiments and run completions on all examples. In the API, an "experiment" is represented as a session (or "tracer session") that references a dataset via `reference_dataset_id`. The key difference from regular tracing is that runs in an experiment must have a `reference_example_id` that links each run to a specific example in the dataset.
```

---

## API Reference: https://api.smith.langchain.com/redoc#tag/run/operation/query_runs_api_v1_runs_query_post

**URL:** llms-txt#api-reference:-https://api.smith.langchain.com/redoc#tag/run/operation/query_runs_api_v1_runs_query_post

runs = requests.post(
    f"https://api.smith.langchain.com/api/v1/runs/query",
    headers={"x-api-key": os.environ["LANGSMITH_API_KEY"]},
    json={
        "session": experiment_ids,
        "is_root": True, # Only fetch root runs (spans) which contain the end outputs
        "select": ["id", "reference_example_id", "outputs"],
    }
).json()
runs = runs["runs"]
for run in runs:
    example_id = run["reference_example_id"]
    example_id_to_runs_map[example_id].append(run)

for example_id, runs in example_id_to_runs_map.items():
    print(f"Example ID: {example_id}")
    # Preferentially rank the outputs, in this case we will always prefer the first output
    # In reality, you can use an LLM to rank the outputs
    feedback_group_id = uuid4()

# Post a feedback score for each run, with the first run being the preferred one
    # API Reference: https://api.smith.langchain.com/redoc#tag/feedback/operation/create_feedback_api_v1_feedback_post
    # We'll use the feedback group ID to associate the feedback scores with the same group
    for i, run in enumerate(runs):
        print(f"Run ID: {run['id']}")
        feedback = {
            "score": 1 if i == 0 else 0,
            "run_id": str(run["id"]),
            "key": "ranked_preference",
            "feedback_group_id": str(feedback_group_id),
            "comparative_experiment_id": comparative_experiment_id,
        }
        resp = requests.post(
            "https://api.smith.langchain.com/api/v1/feedback",
            json=feedback,
            headers={"x-api-key": os.environ["LANGSMITH_API_KEY"]}
        )
        resp.raise_for_status()
```

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/run-evals-api-only.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

---

## API Reference: https://api.smith.langchain.com/redoc#tag/tracer-sessions/operation/create_tracer_session_api_v1_sessions_post

**URL:** llms-txt#api-reference:-https://api.smith.langchain.com/redoc#tag/tracer-sessions/operation/create_tracer_session_api_v1_sessions_post

**Contents:**
  - Add evaluation feedback

model_names = ("gpt-3.5-turbo", "gpt-4o-mini")
experiment_ids = []
for model_name in model_names:
    resp = requests.post(
        "https://api.smith.langchain.com/api/v1/sessions",
        json={
            "start_time": datetime.utcnow().isoformat(),
            "reference_dataset_id": str(dataset_id),
            "description": "An optional description for the experiment",
            "name": f"Toxicity detection - API Example - {model_name} - {str(uuid4())[0:8]}",  # A name for the experiment
            "extra": {
                "metadata": {"foo": "bar"},  # Optional metadata
            },
        },
        headers={"x-api-key": os.environ["LANGSMITH_API_KEY"]}
    )

experiment = resp.json()
    experiment_ids.append(experiment["id"])

# Run completions on all examples
    for example in examples:
        run_completion_on_example(example, model_name, experiment["id"])

# Issue a patch request to "end" the experiment by updating the end_time
    requests.patch(
        f"https://api.smith.langchain.com/api/v1/sessions/{experiment['id']}",
        json={"end_time": datetime.utcnow().isoformat()},
        headers={"x-api-key": os.environ["LANGSMITH_API_KEY"]}
    )
python  theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### Add evaluation feedback

After running your [experiments](/langsmith/evaluation-concepts#experiment), you'll typically want to evaluate the results by adding feedback scores. This allows you to track metrics like correctness, accuracy, or any custom evaluation criteria.

In this example, the evaluation checks if each model's output matches the expected label in the dataset. The code posts a "correctness" score (1.0 for correct, 0.0 for incorrect) to track how accurately each model classifies toxic vs. non-toxic text.

The following code adds feedback to the runs from the [single experiment example](#run-a-single-experiment):
```

---

## Build a semantic search engine with LangChain

**URL:** llms-txt#build-a-semantic-search-engine-with-langchain

**Contents:**
- Overview
  - Concepts
- Setup
  - Installation
  - LangSmith
- 1. Documents and Document Loaders
  - Loading documents
  - Splitting
- 2. Embeddings
- 3. Vector stores

Source: https://docs.langchain.com/oss/python/langchain/knowledge-base

This tutorial will familiarize you with LangChain's [document loader](/oss/python/langchain/retrieval#document-loaders), [embedding](/oss/python/langchain/retrieval#embedding-models), and [vector store](/oss/python/langchain/retrieval#vector-store) abstractions. These abstractions are designed to support retrieval of data--  from (vector) databases and other sources -- for integration with LLM workflows. They are important for applications that fetch data to be reasoned over as part of model inference, as in the case of retrieval-augmented generation, or [RAG](/oss/python/langchain/retrieval).

Here we will build a search engine over a PDF document. This will allow us to retrieve passages in the PDF that are similar to an input query. The guide also includes a minimal RAG implementation on top of the search engine.

This guide focuses on retrieval of text data. We will cover the following concepts:

* [Documents and document loaders](/oss/python/integrations/document_loaders);
* [Text splitters](/oss/python/integrations/splitters);
* [Embeddings](/oss/python/integrations/text_embedding);
* [Vector stores](/oss/python/integrations/vectorstores) and [retrievers](/oss/python/integrations/retrievers).

This tutorial requires the `langchain-community` and `pypdf` packages:

For more details, see our [Installation guide](/oss/python/langchain/install).

Many of the applications you build with LangChain will contain multiple steps with multiple invocations of LLM calls.
As these applications get more and more complex, it becomes crucial to be able to inspect what exactly is going on inside your chain or agent.
The best way to do this is with [LangSmith](https://smith.langchain.com).

After you sign up at the link above, make sure to set your environment variables to start logging traces:

Or, if in a notebook, you can set them with:

## 1. Documents and Document Loaders

LangChain implements a [Document](https://reference.langchain.com/python/langchain_core/documents/#langchain_core.documents.base.Document) abstraction, which is intended to represent a unit of text and associated metadata. It has three attributes:

* `page_content`: a string representing the content;
* `metadata`: a dict containing arbitrary metadata;
* `id`: (optional) a string identifier for the document.

The `metadata` attribute can capture information about the source of the document, its relationship to other documents, and other information. Note that an individual [`Document`](https://reference.langchain.com/python/langchain_core/documents/#langchain_core.documents.base.Document) object often represents a chunk of a larger document.

We can generate sample documents when desired:

However, the LangChain ecosystem implements [document loaders](/oss/python/langchain/retrieval#document-loaders) that [integrate with hundreds of common sources](/oss/python/integrations/document_loaders/). This makes it easy to incorporate data from these sources into your AI application.

### Loading documents

Let's load a PDF into a sequence of [`Document`](https://reference.langchain.com/python/langchain_core/documents/#langchain_core.documents.base.Document) objects. [Here is a sample PDF](https://github.com/langchain-ai/langchain/blob/v0.3/docs/docs/example_data/nke-10k-2023.pdf) -- a 10-k filing for Nike from 2023. We can consult the LangChain documentation for [available PDF document loaders](/oss/python/integrations/document_loaders/#pdfs).

`PyPDFLoader` loads one [`Document`](https://reference.langchain.com/python/langchain_core/documents/#langchain_core.documents.base.Document) object per PDF page. For each, we can easily access:

* The string content of the page;
* Metadata containing the file name and page number.

For both information retrieval and downstream question-answering purposes, a page may be too coarse a representation. Our goal in the end will be to retrieve [`Document`](https://reference.langchain.com/python/langchain_core/documents/#langchain_core.documents.base.Document) objects that answer an input query, and further splitting our PDF will help ensure that the meanings of relevant portions of the document are not "washed out" by surrounding text.

We can use [text splitters](/oss/python/langchain/retrieval#text_splitters) for this purpose. Here we will use a simple text splitter that partitions based on characters. We will split our documents into chunks of 1000 characters
with 200 characters of overlap between chunks. The overlap helps
mitigate the possibility of separating a statement from important
context related to it. We use the
`RecursiveCharacterTextSplitter`,
which will recursively split the document using common separators like
new lines until each chunk is the appropriate size. This is the
recommended text splitter for generic text use cases.

We set `add_start_index=True` so that the character index where each
split Document starts within the initial Document is preserved as
metadata attribute “start\_index”.

Vector search is a common way to store and search over unstructured data (such as unstructured text). The idea is to store numeric vectors that are associated with the text. Given a query, we can [embed](/oss/python/langchain/retrieval#embedding_models) it as a vector of the same dimension and use vector similarity metrics (such as cosine similarity) to identify related text.

LangChain supports embeddings from [dozens of providers](/oss/python/integrations/text_embedding/). These models specify how text should be converted into a numeric vector. Let's select a model:

<Tabs>
  <Tab title="OpenAI">

<Tab title="Google Gemini">

<Tab title="Google Vertex">

<Tab title="HuggingFace">

<Tab title="MistralAI">

<Tab title="Voyage AI">

<Tab title="IBM watsonx">

<Tab title="Isaacus">

Armed with a model for generating text embeddings, we can next store them in a special data structure that supports efficient similarity search.

LangChain [VectorStore](https://reference.langchain.com/python/langchain_core/vectorstores/?h=#langchain_core.vectorstores.base.VectorStore) objects contain methods for adding text and [`Document`](https://reference.langchain.com/python/langchain_core/documents/#langchain_core.documents.base.Document) objects to the store, and querying them using various similarity metrics. They are often initialized with [embedding](/oss/python/langchain/retrieval#embedding_models) models, which determine how text data is translated to numeric vectors.

LangChain includes a suite of [integrations](/oss/python/integrations/vectorstores) with different vector store technologies. Some vector stores are hosted by a provider (e.g., various cloud providers) and require specific credentials to use; some (such as [Postgres](/oss/python/integrations/vectorstores/pgvector)) run in separate infrastructure that can be run locally or via a third-party; others can run in-memory for lightweight workloads. Let's select a vector store:

<Tabs>
  <Tab title="In-memory">

<Tab title="Amazon OpenSearch">

<Tab title="AstraDB">

<Tab title="MongoDB">

<Tab title="PGVector">

<Tab title="PGVectorStore">

<Tab title="Pinecone">

Having instantiated our vector store, we can now index the documents.

Note that most vector store implementations will allow you to connect to an existing vector store--  e.g., by providing a client, index name, or other information. See the documentation for a specific [integration](/oss/python/integrations/vectorstores) for more detail.

Once we've instantiated a [`VectorStore`](https://reference.langchain.com/python/langchain_core/vectorstores/?h=#langchain_core.vectorstores.base.VectorStore) that contains documents, we can query it. [VectorStore](https://reference.langchain.com/python/langchain_core/vectorstores/?h=#langchain_core.vectorstores.base.VectorStore) includes methods for querying:

* Synchronously and asynchronously;
* By string query and by vector;
* With and without returning similarity scores;
* By similarity and [maximum marginal relevance](https://reference.langchain.com/python/langchain_core/vectorstores/?h=#langchain_core.vectorstores.base.VectorStore.max_marginal_relevance_search) (to balance similarity with query to diversity in retrieved results).

The methods will generally include a list of [Document](https://reference.langchain.com/python/langchain_core/documents/#langchain_core.documents.base.Document) objects in their outputs.

Embeddings typically represent text as a "dense" vector such that texts with similar meanings are geometrically close. This lets us retrieve relevant information just by passing in a question, without knowledge of any specific key-terms used in the document.

Return documents based on similarity to a string query:

```python  theme={null}

**Examples:**

Example 1 (unknown):
```unknown

```

Example 2 (unknown):
```unknown
</CodeGroup>

For more details, see our [Installation guide](/oss/python/langchain/install).

### LangSmith

Many of the applications you build with LangChain will contain multiple steps with multiple invocations of LLM calls.
As these applications get more and more complex, it becomes crucial to be able to inspect what exactly is going on inside your chain or agent.
The best way to do this is with [LangSmith](https://smith.langchain.com).

After you sign up at the link above, make sure to set your environment variables to start logging traces:
```

Example 3 (unknown):
```unknown
Or, if in a notebook, you can set them with:
```

Example 4 (unknown):
```unknown
## 1. Documents and Document Loaders

LangChain implements a [Document](https://reference.langchain.com/python/langchain_core/documents/#langchain_core.documents.base.Document) abstraction, which is intended to represent a unit of text and associated metadata. It has three attributes:

* `page_content`: a string representing the content;
* `metadata`: a dict containing arbitrary metadata;
* `id`: (optional) a string identifier for the document.

The `metadata` attribute can capture information about the source of the document, its relationship to other documents, and other information. Note that an individual [`Document`](https://reference.langchain.com/python/langchain_core/documents/#langchain_core.documents.base.Document) object often represents a chunk of a larger document.

We can generate sample documents when desired:
```

---

## How to evaluate a runnable

**URL:** llms-txt#how-to-evaluate-a-runnable

**Contents:**
- Setup
- Evaluate
- Related

Source: https://docs.langchain.com/langsmith/langchain-runnable

<Info>
  * `langchain`: [Python](https://python.langchain.com) and [JS/TS](https://js.langchain.com)
  * Runnable: [Python](https://python.langchain.com/docs/concepts/runnables/) and [JS/TS](https://js.langchain.com/docs/concepts/runnables/)
</Info>

`langchain` [Runnable](https://python.langchain.com/docs/concepts/runnables/) objects (such as chat models, retrievers, chains, etc.) can be passed directly into `evaluate()` / `aevaluate()`.

Let's define a simple chain to evaluate. First, install all the required packages:

To evaluate our chain we can pass it directly to the `evaluate()` / `aevaluate()` method. Note that the input variables of the chain must match the keys of the example inputs. In this case, the example inputs should have the form `{"text": "..."}`.

The runnable is traced appropriately for each output.

<img src="https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/runnable-eval.png?fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=b9dac41dafb9a1cbb3b90fc508f212f7" alt="Runnable Evaluation" data-og-width="2288" width="2288" data-og-height="1052" height="1052" data-path="langsmith/images/runnable-eval.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/runnable-eval.png?w=280&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=39f7bda57df5d29c72729390065342c2 280w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/runnable-eval.png?w=560&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=2bbfa58f877541adff85056d2d4910c7 560w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/runnable-eval.png?w=840&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=198967ebb494d0577fac294f879f348c 840w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/runnable-eval.png?w=1100&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=dd0758a55517d6899d445bd203bc7d03 1100w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/runnable-eval.png?w=1650&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=6fa8f6a044a0b978ef727390f18f5ce3 1650w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/runnable-eval.png?w=2500&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=40dad8febfdaf0756c90b6326e2c4415 2500w" />

* [How to evaluate a `langgraph` graph](/langsmith/evaluate-on-intermediate-steps)

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/langchain-runnable.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

**Examples:**

Example 1 (unknown):
```unknown

```

Example 2 (unknown):
```unknown
</CodeGroup>

Now define a chain:

<CodeGroup>
```

Example 3 (unknown):
```unknown

```

Example 4 (unknown):
```unknown
</CodeGroup>

## Evaluate

To evaluate our chain we can pass it directly to the `evaluate()` / `aevaluate()` method. Note that the input variables of the chain must match the keys of the example inputs. In this case, the example inputs should have the form `{"text": "..."}`.

<CodeGroup>
```

---

## Image block

**URL:** llms-txt#image-block

**Contents:**
  - Serialize standard content
- Simplified package
  - Namespace
  - `langchain-classic`
- Breaking changes
  - Dropped Python 3.9 support
  - Updated return type for chat models
  - Default message format for OpenAI Responses API

image_block = {
    "type": "image",
    "url": "https://example.com/image.png",
    "mime_type": "image/png",
}
bash Environment variable theme={null}
  export LC_OUTPUT_VERSION=v1
  python Initialization parameter theme={null}
  from langchain.chat_models import init_chat_model

model = init_chat_model(
      "gpt-5-nano",
      output_version="v1",
  )
  python v1 (new) theme={null}
  # Chains
  from langchain_classic.chains import LLMChain

# Retrievers
  from langchain_classic.retrievers import ...

# Indexing
  from langchain_classic.indexes import ...

# Hub
  from langchain_classic import hub
  python v0 (old) theme={null}
  # Chains
  from langchain_classic.chains import LLMChain

# Retrievers
  from langchain.retrievers import ...

# Indexing
  from langchain.indexes import ...

# Hub
  from langchain import hub
  bash  theme={null}
uv pip install langchain-classic
python v1 (new) theme={null}
  def bind_tools(
          ...
      ) -> Runnable[LanguageModelInput, AIMessage]:
  python v0 (old) theme={null}
  def bind_tools(
          ...
      ) -> Runnable[LanguageModelInput, BaseMessage]:
  python  theme={null}

**Examples:**

Example 1 (unknown):
```unknown
See the content blocks [reference](/oss/python/langchain/messages#content-block-reference) for more details.

### Serialize standard content

Standard content blocks are **not serialized** into the `content` attribute by default. If you need to access standard content blocks in the `content` attribute (e.g., when sending messages to a client), you can opt-in to serializing them into `content`.

<CodeGroup>
```

Example 2 (unknown):
```unknown

```

Example 3 (unknown):
```unknown
</CodeGroup>

<Note>
  Learn more: [Messages](/oss/python/langchain/messages#message-content), [Standard content blocks](/oss/python/langchain/messages#standard-content-blocks), and [Multimodal](/oss/python/langchain/messages#multimodal).
</Note>

***

## Simplified package

The `langchain` package namespace has been significantly reduced in v1 to focus on essential building blocks for agents. The streamlined package makes it easier to discover and use the core functionality.

### Namespace

| Module                                                                                | What's available                                                                                                                                                                                                                                                          | Notes                             |
| ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| [`langchain.agents`](https://reference.langchain.com/python/langchain/agents)         | [`create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent), [`AgentState`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.AgentState)                                                            | Core agent creation functionality |
| [`langchain.messages`](https://reference.langchain.com/python/langchain/messages)     | Message types, [content blocks](https://reference.langchain.com/python/langchain/messages/#langchain.messages.ContentBlock), [`trim_messages`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.trim_messages)                               | Re-exported from `langchain-core` |
| [`langchain.tools`](https://reference.langchain.com/python/langchain/tools)           | [`@tool`](https://reference.langchain.com/python/langchain/tools/#langchain.tools.tool), [`BaseTool`](https://reference.langchain.com/python/langchain/tools/#langchain.tools.BaseTool), injection helpers                                                                | Re-exported from `langchain-core` |
| [`langchain.chat_models`](https://reference.langchain.com/python/langchain/models)    | [`init_chat_model`](https://reference.langchain.com/python/langchain/models/#langchain.chat_models.init_chat_model), [`BaseChatModel`](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.language_models.chat_models.BaseChatModel)   | Unified model initialization      |
| [`langchain.embeddings`](https://reference.langchain.com/python/langchain/embeddings) | [`init_embeddings`](https://reference.langchain.com/python/langchain_core/embeddings/#langchain_core.embeddings.embeddings.Embeddings), [`Embeddings`](https://reference.langchain.com/python/langchain_core/embeddings/#langchain_core.embeddings.embeddings.Embeddings) | Embedding models                  |

### `langchain-classic`

If you were using any of the following from the `langchain` package, you'll need to install [`langchain-classic`](https://pypi.org/project/langchain-classic/) and update your imports:

* Legacy chains (`LLMChain`, `ConversationChain`, etc.)
* Retrievers (e.g. `MultiQueryRetriever` or anything from the previous `langchain.retrievers` module)
* The indexing API
* The hub module (for managing prompts programmatically)
* Embeddings modules (e.g. `CacheBackedEmbeddings` and community embeddings)
* [`langchain-community`](https://pypi.org/project/langchain-community) re-exports
* Other deprecated functionality

<CodeGroup>
```

Example 4 (unknown):
```unknown

```

---

## Implement a LangChain integration

**URL:** llms-txt#implement-a-langchain-integration

Source: https://docs.langchain.com/oss/python/contributing/implement-langchain

Integration packages are Python packages that users can install for use in their projects. They implement one or more components that adhere to the LangChain interface standards.

LangChain components are subclasses of base classes in [`langchain-core`](https://github.com/langchain-ai/langchain/tree/master/libs/core). Examples include [chat models](/oss/python/integrations/chat), [tools](/oss/python/integrations/tools), [retrievers](/oss/python/integrations/retrievers), and more.

Your integration package will typically implement a subclass of at least one of these components. Expand the tabs below to see details on each.

<Tabs>
  <Tab title="Chat Models">
    Chat models are subclasses of the [`BaseChatModel`](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.language_models.chat_models.BaseChatModel) class. They implement methods for generating chat completions, handling message formatting, and managing model parameters.

<Warning>
      The chat model integration guide is currently WIP. In the meantime, read the [chat model conceptual guide](/oss/python/langchain/models) for details on how LangChain chat models function.
    </Warning>
  </Tab>

<Tab title="Tools">
    Tools are used in 2 main ways:

1. To define an "input schema" or "args schema" to pass to a chat model's tool calling feature along with a text request, such that the chat model can generate a "tool call", or parameters to call the tool with.
    2. To take a "tool call" as generated above, and take some action and return a response that can be passed back to the chat model as a ToolMessage.

The Tools class must inherit from the [`BaseTool`](https://reference.langchain.com/python/langchain/tools/#langchain.tools.BaseTool) base class. This interface has 3 properties and 2 methods that should be implemented in a subclass.

<Warning>
      The tools integration guide is currently WIP. In the meantime, read the [tools conceptual guide](/oss/python/langchain/tools) for details on how LangChain tools function.
    </Warning>
  </Tab>

<Tab title="Retrievers">
    Retrievers are used to retrieve documents from APIs, databases, or other sources based on a query. The Retriever class must inherit from the BaseRetriever base class.

<Warning>
      The retriever integration guide is currently WIP. In the meantime, read the [retriever conceptual guide](/oss/python/integrations/retrievers) for details on how LangChain retrievers function.
    </Warning>
  </Tab>

<Tab title="Vector Stores">
    All vector stores must inherit from the [`VectorStore`](https://reference.langchain.com/python/langchain_core/vectorstores/?h=#langchain_core.vectorstores.base.VectorStore) base class. This interface consists of methods for writing, deleting and searching for documents in the vector store.

See the [vector store integration guide](/oss/python/integrations/vectorstores) for details on implementing a vector store integration.

<Warning>
      The vector store integration guide is currently WIP. In the meantime, read the [vector store conceptual guide](/oss/python/integrations/vectorstores) for details on how LangChain vector stores function.
    </Warning>
  </Tab>

<Tab title="Embeddings">
    Embedding models are subclasses of the [`Embeddings`](https://reference.langchain.com/python/langchain_core/embeddings/#langchain_core.embeddings.embeddings.Embeddings) class.

<Warning>
      The embedding model integration guide is currently WIP. In the meantime, read the [embedding model conceptual guide](/oss/python/integrations/text_embedding) for details on how LangChain embedding models function.
    </Warning>
  </Tab>
</Tabs>

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/contributing/implement-langchain.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

---

## Install LangChain

**URL:** llms-txt#install-langchain

Source: https://docs.langchain.com/oss/python/langchain/install

To install the LangChain package:

LangChain provides integrations to hundreds of LLMs and thousands of other integrations. These live in independent provider packages.

<Tip>
  See the [Integrations tab](/oss/python/integrations/providers/overview) for a full list of available integrations.
</Tip>

Now that you have LangChain installed, you can get started by following the [Quickstart guide](/oss/python/langchain/quickstart).

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/install.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

**Examples:**

Example 1 (unknown):
```unknown

```

Example 2 (unknown):
```unknown
</CodeGroup>

LangChain provides integrations to hundreds of LLMs and thousands of other integrations. These live in independent provider packages.

<CodeGroup>
```

Example 3 (unknown):
```unknown

```

---

## LangChain Academy

**URL:** llms-txt#langchain-academy

Source: https://docs.langchain.com/oss/python/langchain/academy

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/academy.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

---

## LangChain SDK

**URL:** llms-txt#langchain-sdk

Source: https://docs.langchain.com/oss/python/reference/langchain-python

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/reference/langchain-python.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

---

## meaning you can use it as you would any other runnable.

**URL:** llms-txt#meaning-you-can-use-it-as-you-would-any-other-runnable.

---

## Model initialization

**URL:** llms-txt#model-initialization

**Contents:**
  - `langchain-classic`
- Migration guide
- Reporting issues
- Additional resources
- See also

from langchain.chat_models import init_chat_model
from langchain.embeddings import init_embeddings
bash pip theme={null}
  pip install langchain-classic
  bash uv theme={null}
  uv add langchain-classic
  python  theme={null}
from langchain import ...  # [!code --]
from langchain_classic import ...  # [!code ++]

from langchain.chains import ...  # [!code --]
from langchain_classic.chains import ...  # [!code ++]

from langchain.retrievers import ...  # [!code --]
from langchain_classic.retrievers import ...  # [!code ++]

from langchain import hub  # [!code --]
from langchain_classic import hub  # [!code ++]
```

See our [migration guide](/oss/python/migrate/langchain-v1) for help updating your code to LangChain v1.

Please report any issues discovered with 1.0 on [GitHub](https://github.com/langchain-ai/langchain/issues) using the `'v1'` [label](https://github.com/langchain-ai/langchain/issues?q=state%3Aopen%20label%3Av1).

## Additional resources

<CardGroup cols={3}>
  <Card title="LangChain 1.0" icon="rocket" href="https://blog.langchain.com/langchain-langchain-1-0-alpha-releases/">
    Read the announcement
  </Card>

<Card title="Middleware guide" icon="puzzle-piece" href="https://blog.langchain.com/agent-middleware/">
    Deep dive into middleware
  </Card>

<Card title="Agents Documentation" icon="book" href="/oss/python/langchain/agents" arrow>
    Full agent documentation
  </Card>

<Card title="Message Content" icon="message" href="/oss/python/langchain/messages#message-content" arrow>
    New content blocks API
  </Card>

<Card title="Migration guide" icon="arrow-right-arrow-left" href="/oss/python/migrate/langchain-v1" arrow>
    How to migrate to LangChain v1
  </Card>

<Card title="GitHub" icon="github" href="https://github.com/langchain-ai/langchain">
    Report issues or contribute
  </Card>
</CardGroup>

* [Versioning](/oss/python/versioning) – Understanding version numbers
* [Release policy](/oss/python/release-policy) – Detailed release policies

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/releases/langchain-v1.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

**Examples:**

Example 1 (unknown):
```unknown
### `langchain-classic`

Legacy functionality has moved to [`langchain-classic`](https://pypi.org/project/langchain-classic) to keep the core packages lean and focused.

**What's in `langchain-classic`:**

* Legacy chains and chain implementations
* Retrievers (e.g. `MultiQueryRetriever` or anything from the previous `langchain.retrievers` module)
* The indexing API
* The hub module (for managing prompts programmatically)
* [`langchain-community`](https://pypi.org/project/langchain-community) exports
* Other deprecated functionality

If you use any of this functionality, install [`langchain-classic`](https://pypi.org/project/langchain-classic):

<CodeGroup>
```

Example 2 (unknown):
```unknown

```

Example 3 (unknown):
```unknown
</CodeGroup>

Then update your imports:
```

---

## Remember that langgraph graphs are also langchain runnables.

**URL:** llms-txt#remember-that-langgraph-graphs-are-also-langchain-runnables.

**Contents:**
- Evaluating intermediate steps
- Running and evaluating individual nodes
- Related
- Reference code

target = example_to_state | app

experiment_results = await aevaluate(
    target,
    data="weather agent",
    evaluators=[correct],
    max_concurrency=4,  # optional
    experiment_prefix="claude-3.5-baseline",  # optional
)
python  theme={null}
def right_tool(outputs: dict) -> bool:
    tool_calls = outputs["messages"][1].tool_calls
    return bool(tool_calls and tool_calls[0]["name"] == "search")

experiment_results = await aevaluate(
    target,
    data="weather agent",
    evaluators=[correct, right_tool],
    max_concurrency=4,  # optional
    experiment_prefix="claude-3.5-baseline",  # optional
)
python  theme={null}
from langsmith.schemas import Run, Example

def right_tool_from_run(run: Run, example: Example) -> dict:
    # Get documents and answer
    first_model_run = next(run for run in root_run.child_runs if run.name == "agent")
    tool_calls = first_model_run.outputs["messages"][-1].tool_calls
    right_tool = bool(tool_calls and tool_calls[0]["name"] == "search")
    return {"key": "right_tool", "value": right_tool}

experiment_results = await aevaluate(
    target,
    data="weather agent",
    evaluators=[correct, right_tool_from_run],
    max_concurrency=4,  # optional
    experiment_prefix="claude-3.5-baseline",  # optional
)
python  theme={null}
node_target = example_to_state | app.nodes["agent"]

node_experiment_results = await aevaluate(
    node_target,
    data="weather agent",
    evaluators=[right_tool_from_run],
    max_concurrency=4,  # optional
    experiment_prefix="claude-3.5-model-node",  # optional
)
python  theme={null}
  from typing import Annotated, Literal, TypedDict
  from langchain.chat_models import init_chat_model
  from langchain.tools import tool
  from langgraph.prebuilt import ToolNode
  from langgraph.graph import END, START, StateGraph
  from langgraph.graph.message import add_messages
  from langsmith import Client, aevaluate

# Define a graph
  class State(TypedDict):
      # Messages have the type "list". The 'add_messages' function
      # in the annotation defines how this state key should be updated
      # (in this case, it appends messages to the list, rather than overwriting them)
      messages: Annotated[list, add_messages]

# Define the tools for the agent to use
  @tool
  def search(query: str) -> str:
      """Call to surf the web."""
      # This is a placeholder, but don't tell the LLM that...
      if "sf" in query.lower() or "san francisco" in query.lower():
          return "It's 60 degrees and foggy."
      return "It's 90 degrees and sunny."

tools = [search]
  tool_node = ToolNode(tools)
  model = init_chat_model("claude-sonnet-4-5-20250929").bind_tools(tools)

# Define the function that determines whether to continue or not
  def should_continue(state: State) -> Literal["tools", END]:
      messages = state['messages']
      last_message = messages[-1]

# If the LLM makes a tool call, then we route to the "tools" node
      if last_message.tool_calls:
          return "tools"

# Otherwise, we stop (reply to the user)
      return END

# Define the function that calls the model
  def call_model(state: State):
      messages = state['messages']
      response = model.invoke(messages)
      # We return a list, because this will get added to the existing list
      return {"messages": [response]}

# Define a new graph
  workflow = StateGraph(State)

# Define the two nodes we will cycle between
  workflow.add_node("agent", call_model)
  workflow.add_node("tools", tool_node)

# Set the entrypoint as 'agent'
  # This means that this node is the first one called
  workflow.add_edge(START, "agent")

# We now add a conditional edge
  workflow.add_conditional_edges(
      # First, we define the start node. We use 'agent'.
      # This means these are the edges taken after the 'agent' node is called.
      "agent",
      # Next, we pass in the function that will determine which node is called next.
      should_continue,
  )

# We now add a normal edge from 'tools' to 'agent'.
  # This means that after 'tools' is called, 'agent' node is called next.
  workflow.add_edge("tools", 'agent')

# Finally, we compile it!
  # This compiles it into a LangChain Runnable,
  # meaning you can use it as you would any other runnable.
  # Note that we're (optionally) passing the memory when compiling the graph
  app = workflow.compile()

questions = [
      "what's the weather in sf",
      "whats the weather in san fran",
      "whats the weather in tangier"
  ]

answers = [
      "It's 60 degrees and foggy.",
      "It's 60 degrees and foggy.",
      "It's 90 degrees and sunny.",
  ]

# Create a dataset
  ls_client = Client()
  dataset = ls_client.create_dataset(
      "weather agent",
      inputs=[{"question": q} for q in questions],
      outputs=[{"answers": a} for a in answers],
  )

# Define evaluators
  async def correct(outputs: dict, reference_outputs: dict) -> bool:
      instructions = (
          "Given an actual answer and an expected answer, determine whether"
          " the actual answer contains all of the information in the"
          " expected answer. Respond with 'CORRECT' if the actual answer"
          " does contain all of the expected information and 'INCORRECT'"
          " otherwise. Do not include anything else in your response."
      )
      # Our graph outputs a State dictionary, which in this case means
      # we'll have a 'messages' key and the final message should
      # be our actual answer.
      actual_answer = outputs["messages"][-1].content
      expected_answer = reference_outputs["answer"]
      user_msg = (
          f"ACTUAL ANSWER: {actual_answer}"
          f"\n\nEXPECTED ANSWER: {expected_answer}"
      )
      response = await judge_llm.ainvoke(
          [
              {"role": "system", "content": instructions},
              {"role": "user", "content": user_msg}
          ]
      )
      return response.content.upper() == "CORRECT"

def right_tool(outputs: dict) -> bool:
      tool_calls = outputs["messages"][1].tool_calls
      return bool(tool_calls and tool_calls[0]["name"] == "search")

# Run evaluation
  experiment_results = await aevaluate(
      target,
      data="weather agent",
      evaluators=[correct, right_tool],
      max_concurrency=4,  # optional
      experiment_prefix="claude-3.5-baseline",  # optional
  )
  ```
</Accordion>

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/evaluate-graph.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

**Examples:**

Example 1 (unknown):
```unknown
## Evaluating intermediate steps

Often it is valuable to evaluate not only the final output of an agent but also the intermediate steps it has taken. What's nice about `langgraph` is that the output of a graph is a state object that often already carries information about the intermediate steps taken. Usually we can evaluate whatever we're interested in just by looking at the messages in our state. For example, we can look at the messages to assert that the model invoked the 'search' tool upon as a first step.

Requires `langsmith>=0.2.0`
```

Example 2 (unknown):
```unknown
If we need access to information about intermediate steps that isn't in state, we can look at the Run object. This contains the full traces for all node inputs and outputs:

<Check>
  See more about what arguments you can pass to custom evaluators in this [how-to guide](/langsmith/code-evaluator).
</Check>
```

Example 3 (unknown):
```unknown
## Running and evaluating individual nodes

Sometimes you want to evaluate a single node directly to save time and costs. `langgraph` makes it easy to do this. In this case we can even continue using the evaluators we've been using.
```

Example 4 (unknown):
```unknown
## Related

* [`langgraph` evaluation docs](https://langchain-ai.github.io/langgraph/tutorials/#evaluation)

## Reference code

<Accordion title="Click to see a consolidated code snippet">
```

---

## See trace: https://smith.langchain.com/public/882f9ecf-5057-426a-ae98-0edf84fdcaf9/r

**URL:** llms-txt#see-trace:-https://smith.langchain.com/public/882f9ecf-5057-426a-ae98-0edf84fdcaf9/r

**Contents:**
- Ensure all traces are submitted before exiting
  - Using the LangSmith SDK
  - Using LangChain

MyClass(13).combine(29)
python Python theme={null}
  from langsmith import Client

@traceable(client=client)
  async def my_traced_func():
    # Your code here...
    pass

try:
    await my_traced_func()
  finally:
    await client.flush()
  typescript TypeScript theme={null}
  import { Client } from "langsmith";

const langsmithClient = new Client({});

const myTracedFunc = traceable(async () => {
    // Your code here...
  },{ client: langsmithClient });

try {
    await myTracedFunc();
  } finally {
    await langsmithClient.flush();
  }
  ```
</CodeGroup>

If you are using LangChain, please refer to our [LangChain tracing guide](/langsmith/trace-with-langchain#ensure-all-traces-are-submitted-before-exiting).

If you prefer a video tutorial, check out the [Tracing Basics video](https://academy.langchain.com/pages/intro-to-langsmith-preview) from the Introduction to LangSmith Course.

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/annotate-code.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

**Examples:**

Example 1 (unknown):
```unknown
## Ensure all traces are submitted before exiting

LangSmith's tracing is done in a background thread to avoid obstructing your production application. This means that your process may end before all traces are successfully posted to LangSmith. Here are some options for ensuring all traces are submitted before exiting your application.

### Using the LangSmith SDK

If you are using the LangSmith SDK standalone, you can use the `flush` method before exit:

<CodeGroup>
```

Example 2 (unknown):
```unknown

```

---

## Set environment variables for LangChain

**URL:** llms-txt#set-environment-variables-for-langchain

os.environ["LANGSMITH_OTEL_ENABLED"] = "true"
os.environ["LANGSMITH_TRACING"] = "true"

---

## The above chain will be traced as a child run of the traceable function

**URL:** llms-txt#the-above-chain-will-be-traced-as-a-child-run-of-the-traceable-function

**Contents:**
- Interoperability between LangChain.JS and LangSmith SDK
  - Tracing LangChain objects inside `traceable` (JS only)
  - Tracing LangChain child runs via `traceable` / RunTree API (JS only)

@traceable(
    tags=["openai", "chat"],
    metadata={"foo": "bar"}
)
def invoke_runnnable(question, context):
    result = chain.invoke({"question": question, "context": context})
    return "The response is: " + result

invoke_runnnable("Can you summarize this morning's meetings?", "During this morning's meeting, we solved all world conflict.")
typescript  theme={null}
import { ChatOpenAI } from "@langchain/openai";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { StringOutputParser } from "@langchain/core/output_parsers";
import { getLangchainCallbacks } from "langsmith/langchain";

const prompt = ChatPromptTemplate.fromMessages([
  [
    "system",
    "You are a helpful assistant. Please respond to the user's request only based on the given context.",
  ],
  ["user", "Question: {question}\nContext: {context}"],
]);

const model = new ChatOpenAI({ modelName: "gpt-4o-mini" });
const outputParser = new StringOutputParser();
const chain = prompt.pipe(model).pipe(outputParser);

const main = traceable(
  async (input: { question: string; context: string }) => {
    const callbacks = await getLangchainCallbacks();
    const response = await chain.invoke(input, { callbacks });
    return response;
  },
  { name: "main" }
);
typescript  theme={null}
import { traceable } from "langsmith/traceable";
import { RunnableLambda } from "@langchain/core/runnables";
import { RunnableConfig } from "@langchain/core/runnables";

const tracedChild = traceable((input: string) => `Child Run: ${input}`, {
  name: "Child Run",
});

const parrot = new RunnableLambda({
  func: async (input: { text: string }, config?: RunnableConfig) => {
    return await tracedChild(input.text);
  },
});
typescript Traceable theme={null}
  import { traceable } from "langsmith/traceable";
  import { RunnableLambda } from "@langchain/core/runnables";
  import { RunnableConfig } from "@langchain/core/runnables";

const tracedChild = traceable((input: string) => `Child Run: ${input}`, {
    name: "Child Run",
  });

const parrot = new RunnableLambda({
    func: async (input: { text: string }, config?: RunnableConfig) => {
      // Pass the config to existing traceable function
      await tracedChild(config, input.text);
      return input.text;
    },
  });
  typescript Run Tree theme={null}
  import { RunTree } from "langsmith/run_trees";
  import { RunnableLambda } from "@langchain/core/runnables";
  import { RunnableConfig } from "@langchain/core/runnables";

const parrot = new RunnableLambda({
    func: async (input: { text: string }, config?: RunnableConfig) => {
      // create the RunTree from the RunnableConfig of the RunnableLambda
      const childRunTree = RunTree.fromRunnableConfig(config, {
        name: "Child Run",
      });

childRunTree.inputs = { input: input.text };
      await childRunTree.postRun();

childRunTree.outputs = { output: `Child Run: ${input.text}` };
      await childRunTree.patchRun();

return input.text;
    },
  });
  ```
</CodeGroup>

If you prefer a video tutorial, check out the [Alternative Ways to Trace video](https://academy.langchain.com/pages/intro-to-langsmith-preview) from the Introduction to LangSmith Course.

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/trace-with-langchain.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

**Examples:**

Example 1 (unknown):
```unknown
This will produce the following trace tree: <img src="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/trace-tree-python-interop.png?fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=52c64fd784522c4b2d75886ae76f8c18" alt="Trace tree python interop" data-og-width="1334" width="1334" data-og-height="734" height="734" data-path="langsmith/images/trace-tree-python-interop.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/trace-tree-python-interop.png?w=280&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=21a424e2326767bb66a6b5a207390bec 280w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/trace-tree-python-interop.png?w=560&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=72f1854193fd30317d1b69d8de433d73 560w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/trace-tree-python-interop.png?w=840&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=34fa74aff75c11172b350d38319bf276 840w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/trace-tree-python-interop.png?w=1100&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=4ebfb4252764af54033e62ad088f60b1 1100w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/trace-tree-python-interop.png?w=1650&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=2d783eecf72ba0680e78a0f122bd4411 1650w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/trace-tree-python-interop.png?w=2500&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=9d977793e5281e5d255d962224bd70df 2500w" />

## Interoperability between LangChain.JS and LangSmith SDK

### Tracing LangChain objects inside `traceable` (JS only)

Starting with `langchain@0.2.x`, LangChain objects are traced automatically when used inside `@traceable` functions, inheriting the client, tags, metadata and project name of the traceable function.

For older versions of LangChain below `0.2.x`, you will need to manually pass an instance `LangChainTracer` created from the tracing context found in `@traceable`.
```

Example 2 (unknown):
```unknown
### Tracing LangChain child runs via `traceable` / RunTree API (JS only)

<Note>
  We're working on improving the interoperability between `traceable` and LangChain. The following limitations are present when using combining LangChain with `traceable`:

  1. Mutating RunTree obtained from `getCurrentRunTree()` of the RunnableLambda context will result in a no-op.
  2. It's discouraged to traverse the RunTree obtained from RunnableLambda via `getCurrentRunTree()` as it may not contain all the RunTree nodes.
  3. Different child runs may have the same `execution_order` and `child_execution_order` value. Thus in extreme circumstances, some runs may end up in a different order, depending on the `start_time`.
</Note>

In some uses cases, you might want to run `traceable` functions as part of the RunnableSequence or trace child runs of LangChain run imperatively via the `RunTree` API. Starting with LangSmith 0.1.39 and @langchain/core 0.2.18, you can directly invoke `traceable`-wrapped functions within RunnableLambda.
```

Example 3 (unknown):
```unknown
<img src="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/trace-tree-manual-tracing.png?fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=7b117d3aa9b419fe2a314ec6d9cc7c16" alt="Trace Tree" data-og-width="2564" width="2564" data-og-height="1530" height="1530" data-path="langsmith/images/trace-tree-manual-tracing.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/trace-tree-manual-tracing.png?w=280&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=517f8a525908d5241c0d635726bf2da7 280w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/trace-tree-manual-tracing.png?w=560&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=2772298bff6569c12537d8b31cc90e78 560w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/trace-tree-manual-tracing.png?w=840&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=4b02aa33df7ef1d18a33bb36c3e2edfe 840w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/trace-tree-manual-tracing.png?w=1100&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=e9d4021c62cf3bad95e01c8aa2895d44 1100w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/trace-tree-manual-tracing.png?w=1650&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=02ef49a98151ad9fc63c742241542d94 1650w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/trace-tree-manual-tracing.png?w=2500&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=765dabfe056ce5f28b1b09ca7eb735d7 2500w" />

Alternatively, you can convert LangChain's [`RunnableConfig`](https://reference.langchain.com/python/langchain_core/runnables/#langchain_core.runnables.RunnableConfig) to a equivalent RunTree object by using `RunTree.fromRunnableConfig` or pass the [`RunnableConfig`](https://reference.langchain.com/python/langchain_core/runnables/#langchain_core.runnables.RunnableConfig) as the first argument of `traceable`-wrapped function.

<CodeGroup>
```

Example 4 (unknown):
```unknown

```

---

## This compiles it into a LangChain Runnable,

**URL:** llms-txt#this-compiles-it-into-a-langchain-runnable,

---

## Trace with LangChain (Python and JS/TS)

**URL:** llms-txt#trace-with-langchain-(python-and-js/ts)

**Contents:**
- Installation
- Quick start
  - 1. Configure your environment

Source: https://docs.langchain.com/langsmith/trace-with-langchain

LangSmith integrates seamlessly with LangChain (Python and JavaScript), the popular open-source framework for building LLM applications.

Install the core library and the OpenAI integration for Python and JS (we use the OpenAI integration for the code snippets below).

For a full list of packages available, see the [LangChain docs](/oss/python/integrations/providers/overview).

### 1. Configure your environment

```bash wrap theme={null}
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=<your-api-key>

**Examples:**

Example 1 (unknown):
```unknown

```

Example 2 (unknown):
```unknown

```

Example 3 (unknown):
```unknown

```

Example 4 (unknown):
```unknown
</CodeGroup>

## Quick start

### 1. Configure your environment
```

---

## We use LCEL declarative syntax here.

**URL:** llms-txt#we-use-lcel-declarative-syntax-here.

---

## ... database connection and query code

**URL:** llms-txt#...-database-connection-and-query-code

**Contents:**
  - Define the customer support agent

[(1, 'AC/DC'), (2, 'Accept'), (3, 'Aerosmith'), (4, 'Alanis Morissette'), (5, 'Alice In Chains'), (6, 'Antônio Carlos Jobim'), (7, 'Apocalyptica'), (8, 'Audioslave'), (9, 'BackBeat'), (10, 'Billy Cobham')]
python  theme={null}
import sqlite3

def _refund(invoice_id: int | None, invoice_line_ids: list[int] | None, mock: bool = False) -> float:
    ...

def _lookup( ...
`python  theme={null}
from typing import Literal
import json

from langchain.chat_models import init_chat_model
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, StateGraph
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.types import Command, interrupt
from tabulate import tabulate
from typing_extensions import Annotated, TypedDict

**Examples:**

Example 1 (unknown):
```unknown

```

Example 2 (unknown):
```unknown
And here's the database schema (image from [https://github.com/lerocha/chinook-database](https://github.com/lerocha/chinook-database)):

<img src="https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/chinook-diagram.png?fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=5da2a8dcca68f02dfcec11f9c472d341" alt="Chinook DB" data-og-width="1672" width="1672" data-og-height="1132" height="1132" data-path="langsmith/images/chinook-diagram.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/chinook-diagram.png?w=280&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=ea7b3a27e9780b556aa90f6914dcef30 280w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/chinook-diagram.png?w=560&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=d9cf3ddad46562213014ffb1a77b1e45 560w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/chinook-diagram.png?w=840&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=2c9e1e70e9be2cf07111b2211e1ef9b7 840w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/chinook-diagram.png?w=1100&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=970f7f48c80222219b493211331ee22f 1100w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/chinook-diagram.png?w=1650&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=3188acb57c4abc0156f8687fa9e229d8 1650w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/chinook-diagram.png?w=2500&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=86b9655b9fd1bc38fcf9e054b11833df 2500w" />

### Define the customer support agent

We'll create a [LangGraph](https://langchain-ai.github.io/langgraph/) agent with limited access to our database. For demo purposes, our agent will support two basic types of requests:

* Lookup: The customer can look up song titles, artist names, and albums based on other identifying information. For example: "What songs do you have by Jimi Hendrix?"
* Refund: The customer can request a refund on their past purchases. For example: "My name is Claude Shannon and I'd like a refund on a purchase I made last week, could you help me?"

For simplicity in this demo, we'll implement refunds by deleting the corresponding database records. We'll skip implementing user authentication and other production security measures.

The agent's logic will be structured as two separate subgraphs (one for lookups and one for refunds), with a parent graph that routes requests to the appropriate subgraph.

#### Refund agent

Let's build the refund processing agent. This agent needs to:

1. Find the customer's purchase records in the database
2. Delete the relevant Invoice and InvoiceLine records to process the refund

We'll create two SQL helper functions:

1. A function to execute the refund by deleting records
2. A function to look up a customer's purchase history

To make testing easier, we'll add a "mock" mode to these functions. When mock mode is enabled, the functions will simulate database operations without actually modifying any data.
```

Example 3 (unknown):
```unknown
Now let's define our graph. We'll use a simple architecture with three main paths:

1. Extract customer and purchase information from the conversation

2. Route the request to one of three paths:

   * Refund path: If we have sufficient purchase details (Invoice ID or Invoice Line IDs) to process a refund
   * Lookup path: If we have enough customer information (name and phone) to search their purchase history
   * Response path: If we need more information, respond to the user requesting the specific details needed

The graph's state will track:

* The conversation history (messages between user and agent)
* All customer and purchase information extracted from the conversation
* The next message to send to the user (followup text)
```

---

## - Email: foo@langchain.dev

**URL:** llms-txt#--email:-foo@langchain.dev

python  theme={null}
from langchain.tools import tool, ToolRuntime

@tool
def get_weather(city: str, runtime: ToolRuntime) -> str:
    """Get weather for a given city."""
    writer = runtime.stream_writer

# Stream custom updates as the tool executes
    writer(f"Looking up data for city: {city}")
    writer(f"Acquired data for city: {city}")

return f"It's always sunny in {city}!"
```

<Note>
  If you use `runtime.stream_writer` inside your tool, the tool must be invoked within a LangGraph execution context. See [Streaming](/oss/python/langchain/streaming) for more details.
</Note>

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/tools.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

**Examples:**

Example 1 (unknown):
```unknown
#### Stream Writer

Stream custom updates from tools as they execute using `runtime.stream_writer`. This is useful for providing real-time feedback to users about what a tool is doing.
```

---
