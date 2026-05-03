# Langchain - Deployment

**Pages:** 18

---

## App development in LangSmith Deployment

**URL:** llms-txt#app-development-in-langsmith-deployment

Source: https://docs.langchain.com/langsmith/app-development

**LangSmith Deployment** builds on the open-source [LangGraph](/oss/python/langgraph/overview) framework for developing stateful, multi-agent applications.
LangGraph provides the core abstractions and execution model, while LangSmith adds managed infrastructure, observability, deployment options, assistants, and concurrency controls—supporting the full lifecycle from development to production.

<Callout icon="cubes" color="#4F46E5" iconType="regular">
  LangSmith Deployment is framework-agnostic: you can deploy agents built with LangGraph or [other frameworks](/langsmith/deploy-other-frameworks). To get started with LangGraph itself, refer to the [LangGraph quickstart](/oss/python/langgraph/quickstart).
</Callout>

<CardGroup>
  <Card title="Assistants" cta="Explore assistants" href="/langsmith/assistants" icon="user-gear">
    Manage agent configurations, connect to threads, and build interactive assistants.
  </Card>

<Card title="Runs" cta="Learn about runs" href="/langsmith/background-run" icon="play">
    Execute background jobs, stateless runs, cron jobs, and manage configurable headers.
  </Card>

<Card title="Core capabilities" cta="See core features" href="/langsmith/streaming" icon="gear">
    Streaming, human-in-the-loop, webhooks, and concurrency controls like double-texting.
  </Card>

<Card title="Tutorials" cta="View tutorials" href="/langsmith/deploy-other-frameworks" icon="graduation-cap">
    Step-by-step examples: AutoGen integration, streaming UI, and generative UI in React.
  </Card>
</CardGroup>

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/app-development.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

---

## Control plane API reference for LangSmith Deployment

**URL:** llms-txt#control-plane-api-reference-for-langsmith-deployment

**Contents:**
- Host
- Authentication
- Versioning
- Quick Start
- Example Code

Source: https://docs.langchain.com/langsmith/api-ref-control-plane

The control plane API is part of [LangSmith Deployment](/langsmith/deployments). With the control plane API, you can programmatically create, manage, and automate your [Agent Server](/langsmith/agent-server) deployments—for example, as part of a custom CI/CD workflow.

Browse the full API reference in the **Control Plane API** section in the sidebar, or refer to the endpoint groups:

* [Integrations (v1)](/api-reference/integrations-v1/list-github-integrations): GitHub integrations and repository listings
* [Deployments (v2)](/api-reference/deployments-v2): Create, manage, and update Agent Server deployments
* [Listeners (v2)](/api-reference/listeners-v2): Listener resources for self-hosted enterprise organizations
* [Auth Service (v2)](/api-reference/auth-service-v2): OAuth provider configuration and authentication flows

The control plane hosts for Cloud data regions:

| US                               | EU                                  |
| -------------------------------- | ----------------------------------- |
| `https://api.host.langchain.com` | `https://eu.api.host.langchain.com` |

**Note**: Self-hosted deployments of LangSmith will have a custom host for the control plane. The control plane APIs can be accessed at the path `/api-host`. For example, `http(s)://<host>/api-host/v2/deployments`. See [here](../langsmith/self-host-usage#configuring-the-application-you-want-to-use-with-langsmith) for more details.

To authenticate with the control plane API, set the `X-Api-Key` header to a valid LangSmith API key and set the `X-Tenant-Id` header to a valid workspace ID to target.

Example `curl` command:

Each endpoint path is prefixed with a version (e.g. `v1`, `v2`).

1. Call `POST /v2/deployments` to create a new Deployment. The response body contains the Deployment ID (`id`) and the ID of the latest (and first) revision (`latest_revision_id`).
2. Call `GET /v2/deployments/{deployment_id}` to retrieve the Deployment. Set `deployment_id` in the URL to the value of Deployment ID (`id`).
3. Poll for revision `status` until `status` is `DEPLOYED` by calling `GET /v2/deployments/{deployment_id}/revisions/{latest_revision_id}`.
4. Call `PATCH /v2/deployments/{deployment_id}` to update the deployment.

Below is example Python code that demonstrates how to orchestrate the control plane APIs to create a deployment, update the deployment, and delete the deployment.

```python  theme={null}
import os
import time

import requests
from dotenv import load_dotenv

**Examples:**

Example 1 (unknown):
```unknown
## Versioning

Each endpoint path is prefixed with a version (e.g. `v1`, `v2`).

## Quick Start

1. Call `POST /v2/deployments` to create a new Deployment. The response body contains the Deployment ID (`id`) and the ID of the latest (and first) revision (`latest_revision_id`).
2. Call `GET /v2/deployments/{deployment_id}` to retrieve the Deployment. Set `deployment_id` in the URL to the value of Deployment ID (`id`).
3. Poll for revision `status` until `status` is `DEPLOYED` by calling `GET /v2/deployments/{deployment_id}/revisions/{latest_revision_id}`.
4. Call `PATCH /v2/deployments/{deployment_id}` to update the deployment.

## Example Code

Below is example Python code that demonstrates how to orchestrate the control plane APIs to create a deployment, update the deployment, and delete the deployment.
```

---

## Create Deployment

**URL:** llms-txt#create-deployment

Source: https://docs.langchain.com/api-reference/deployments-v2/create-deployment

https://api.host.langchain.com/openapi.json post /v2/deployments
Create a new deployment.

---

## Delete Deployment

**URL:** llms-txt#delete-deployment

Source: https://docs.langchain.com/api-reference/deployments-v2/delete-deployment

https://api.host.langchain.com/openapi.json delete /v2/deployments/{deployment_id}
Delete a deployment by ID.

---

## Deploy an observability stack for your LangSmith deployment

**URL:** llms-txt#deploy-an-observability-stack-for-your-langsmith-deployment

Source: https://docs.langchain.com/langsmith/observability-stack

<Warning>
  **This section is only applicable for Kubernetes deployments.**
</Warning>

LangSmith applications expose telemetry data that can be sent to the backend of your choice. If you don’t already have an observability stack, or prefer to keep LangSmith telemetry separate from your main application, you can use the LangSmith Observability Helm chart to deploy a basic observability stack.

---

## Evaluation concepts

**URL:** llms-txt#evaluation-concepts

**Contents:**
- What to evaluate
- Offline and online evaluations
  - Offline evaluations
  - Online evaluations
- Evaluation lifecycle
  - 1. Development with offline evaluation
  - 2. Initial deployment with online evaluation
  - 3. Continuous improvement
- Core evaluation targets
  - Targets for offline evaluation

Source: https://docs.langchain.com/langsmith/evaluation-concepts

LLM outputs are non-deterministic, which makes response quality hard to assess. Evaluations (evals) are a way to breakdown what "good" looks like and measure it. LangSmith Evaluation provides a framework for measuring quality throughout the application lifecycle, from pre-deployment testing to production monitoring.

Before building evaluations, identify what matters for your application. Break down your system into its critical components—LLM calls, retrieval steps, tool invocations, output formatting—and determine quality criteria for each.

**Start with manually curated examples.** Create 5-10 examples of what "good" looks like for each critical component. These examples serve as your ground truth and inform which evaluation approaches to use. For instance:

* **RAG system**: Examples of good retrievals (relevant documents) and good answers (accurate, complete).
* **Agent**: Examples of correct tool selection and proper argument formatting or trajectory that the agent took.
* **Chatbot**: Examples of helpful, on-brand responses that address user intent.

Once you've defined "good" through examples, you can measure how often your system produces similar quality outputs.

## Offline and online evaluations

LangSmith supports two types of evaluations that serve different purposes in your development workflow:

### Offline evaluations

<Icon icon="flask" iconType="solid" /> Use offline evaluations for **pre-deployment testing**:

* **Benchmarking**: Compare multiple versions to find the best performer.
* **Regression testing**: Ensure new versions don't degrade quality.
* **Unit testing**: Verify correctness of individual components.
* **Backtesting**: Test new versions against historical data.

Offline evaluations target [*examples*](#examples) from [*datasets*](#datasets)—curated test cases with reference outputs that define what "good" looks like.

### Online evaluations

<Icon icon="radar" iconType="solid" /> Use online evaluations for **production monitoring**:

* **Real-time monitoring**: Track quality continuously on live traffic.
* **Anomaly detection**: Flag unusual patterns or edge cases.
* **Production feedback**: Identify issues to add to offline datasets.

Online evaluations target [*runs*](#runs) and [*threads*](#threads) from [tracing](/langsmith/observability-quickstart)—real production traces without reference outputs.

This difference in targets determines what you can evaluate: offline evaluations can check correctness against expected answers, while online evaluations focus on quality patterns, safety, and real-world behavior.

## Evaluation lifecycle

As you develop and [deploy your application](/langsmith/deployments), your evaluation strategy evolves from pre-deployment testing to production monitoring. During development and testing, offline evaluations validate functionality against curated datasets. After deployment, online evaluations monitor production behavior on live traffic. As applications mature, both evaluation types work together in an iterative feedback loop to improve quality continuously.

### 1. Development with offline evaluation

Before production deployment, use offline evaluations to validate functionality, benchmark different approaches, and build confidence.

Follow the [quickstart](/langsmith/evaluation-quickstart) to run your first offline evaluation.

### 2. Initial deployment with online evaluation

After deployment, use online evaluations to monitor production quality, detect unexpected issues, and collect real-world data.

Learn how to [configure online evaluations](/langsmith/online-evaluations) for production monitoring.

### 3. Continuous improvement

Use both evaluation types together in an iterative feedback loop. Online evaluations surface issues that become offline test cases, offline evaluations validate fixes, and online evaluations confirm production improvements.

## Core evaluation targets

Evaluations run on different targets depending on whether they are offline or online.

### Targets for offline evaluation

Offline evaluations run on datasets and examples. The presence of reference outputs enables comparison between expected and actual results.

A dataset is a *collection of examples* used for evaluating an application. An example is a test input, reference output pair.

<img src="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/dataset-concept.png?fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=be2adaa8535dbb253bc0f199895da2e1" alt="Dataset" data-og-width="1279" width="1279" data-og-height="495" height="495" data-path="langsmith/images/dataset-concept.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/dataset-concept.png?w=280&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=b86cc15fe64ec6fdac0a14472b84c1e0 280w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/dataset-concept.png?w=560&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=b388730259225fbf466b9a8682303330 560w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/dataset-concept.png?w=840&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=bf8930b4598fbc88212e6e3dde2d0950 840w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/dataset-concept.png?w=1100&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=10220cebf437b481fd655d8e1ddca492 1100w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/dataset-concept.png?w=1650&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=16e3d46679352d87e6358acc155d0bd9 1650w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/dataset-concept.png?w=2500&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=8b987fee69c354d78e7182a685ac38ed 2500w" />

Each example consists of:

* **Inputs**: a dictionary of input variables to pass to your application.
* **Reference outputs** (optional): a dictionary of reference outputs. These do not get passed to your application, they are only used in evaluators.
* **Metadata** (optional): a dictionary of additional information that can be used to create filtered views of a dataset.

<img src="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/example-concept.png?fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=0c25674bd30e502e3034b754b8649d66" alt="Example" data-og-width="1281" width="1281" data-og-height="406" height="406" data-path="langsmith/images/example-concept.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/example-concept.png?w=280&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=3f49d9e298b397039ae97266ad8eda6e 280w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/example-concept.png?w=560&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=eb14858aac0f28b26cb1e6ee9ca920f4 560w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/example-concept.png?w=840&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=ae707f4b153d7c6e77215012018483c7 840w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/example-concept.png?w=1100&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=9791ddf51677e2e4f046f32e46304e3d 1100w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/example-concept.png?w=1650&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=02b7df4950f45c8d4460b0b0cfad88c0 1650w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/example-concept.png?w=2500&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=db7340730c6025b03bcb96339fdc980e 2500w" />

Learn more about [managing datasets](/langsmith/manage-datasets).

An *experiment* represents the results of evaluating a specific application version on a dataset. Each experiment captures outputs, evaluator scores, and execution traces for every example in the dataset.

<img src="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/experiment-view.png?fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=89c78822157136d0e28e9a110dbdbfd5" alt="Experiment view" data-og-width="1633" width="1633" data-og-height="942" height="942" data-path="langsmith/images/experiment-view.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/experiment-view.png?w=280&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=f911d77a92d1fb020d6ddea937bd224e 280w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/experiment-view.png?w=560&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=11c80e9c9aad7df87ea97a540170809a 560w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/experiment-view.png?w=840&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=5b3722ed4fa19b7fcd7d73454dfd342a 840w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/experiment-view.png?w=1100&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=97d5e419a79137652aeac9139473414a 1100w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/experiment-view.png?w=1650&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=4a79633866510d7f8ea1d92fa6f58138 1650w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/experiment-view.png?w=2500&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=53012b35d0f323587d5956b3a800818b 2500w" />

Multiple experiments typically run on a given dataset to test different application configurations (e.g., different prompts or LLMs). LangSmith displays all experiments associated with a dataset and supports [comparing multiple experiments](/langsmith/compare-experiment-results) side-by-side.

<img src="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/comparison-view.png?fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=c4ed751dc3e74f5ad16634dff061bd77" alt="Comparison view" data-og-width="3018" width="3018" data-og-height="1532" height="1532" data-path="langsmith/images/comparison-view.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/comparison-view.png?w=280&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=4b6c96f4480262f4db39b7a06a971ca8 280w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/comparison-view.png?w=560&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=568b65404d8bbe7444d742fbf131bb4d 560w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/comparison-view.png?w=840&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=36c750c22fcc302d617f1e6e8a5014a0 840w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/comparison-view.png?w=1100&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=fe9225cdcf381e2b6ef17c0bf99b3004 1100w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/comparison-view.png?w=1650&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=ac42818b24a858252bb320a23e06b1c2 1650w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/comparison-view.png?w=2500&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=bd4214772a68d401b48b704b56a35e4a 2500w" />

Learn [how to analyze experiment results](/langsmith/analyze-an-experiment).

### Targets for online evaluation

Online evaluations run on runs and threads from production traffic. Without reference outputs, evaluators focus on detecting issues, anomalies, and quality degradation in real-time.

A *run* is a single execution trace from your [deployed application](/langsmith/deployments). Each run contains:

* **Inputs**: The actual user inputs your application received.
* **Outputs**: What your application actually returned.
* **Intermediate steps**: All the child runs (tool calls, LLM calls, and so on).
* **Metadata**: Tags, user feedback, latency metrics, etc.

Unlike examples in datasets, runs do not include reference outputs. Online evaluators must assess quality without knowing what the "correct" answer should be, relying instead on quality heuristics, safety checks, and reference-free evaluation techniques.

Learn more about [runs and traces in the Observability concepts](/langsmith/observability-concepts#runs).

*Threads* are collections of related runs representing multi-turn conversations. Online evaluators can run at the thread level to evaluate entire conversations rather than individual turns. This enables assessment of conversation-level properties like coherence across turns, topic maintenance, and user satisfaction throughout an interaction.

*Evaluators* are functions that score application performance. They provide the measurement layer for both offline and online evaluation, adapting their inputs based on what data is available.

Run evaluators using the LangSmith SDK ([Python](https://docs.smith.langchain.com/reference/python/reference) and [TypeScript](https://docs.smith.langchain.com/reference/js)), via the [Prompt Playground](/langsmith/observability-concepts#prompt-playground), or by configuring [rules](/langsmith/rules) to run them automatically on tracing projects or datasets.

Evaluator inputs differ based on evaluation type:

**Offline evaluators** receive:

* [Example](#examples): The example from your [dataset](#datasets), containing inputs, reference outputs, and metadata.
* [Run](/langsmith/observability-concepts#runs): The actual outputs and intermediate steps from running the application on the example inputs.

**Online evaluators** receive:

* [Run](/langsmith/observability-concepts#runs): The production trace containing inputs, outputs, and intermediate steps (no reference outputs available).

### Evaluator outputs

Evaluators return **feedback**, which is the scores from evaluation. Feedback is a dictionary or list of dictionaries. Each dictionary contains:

* `key`: The metric name.
* `score` | `value`: The metric value (`score` for numerical metrics, `value` for categorical metrics).
* `comment` (optional): Additional reasoning or explanation for the score.

### Evaluation techniques

LangSmith supports several evaluation approaches:

* [Human](#human)
* [Code](#code)
* [LLM-as-judge](#llm-as-judge)
* [Pairwise](#pairwise)

*Human evaluation* involves manual review of application outputs and execution traces. This approach is [often an effective starting point for evaluation](https://hamel.dev/blog/posts/evals/#looking-at-your-traces). LangSmith provides tools to review application outputs and traces (all intermediate steps).

[Annotation queues](/langsmith/annotation-queues) streamline the process of collecting human feedback on application outputs.

*Code evaluators* are deterministic, rule-based functions. They work well for checks such as verifying the structure of a chatbot's response is not empty, that generated code compiles, or that a classification matches exactly.

*LLM-as-judge evaluators* use LLMs to score application outputs. The grading rules and criteria are typically encoded in the LLM prompt. These evaluators can be:

* **Reference-free**: Check if output contains offensive content or adheres to specific criteria.
* **Reference-based**: Compare output to a reference (e.g., check factual accuracy relative to the reference).

LLM-as-judge evaluators require careful review of scores and prompt tuning. Few-shot evaluators, which include examples of inputs, outputs, and expected grades in the grader prompt, often improve performance.

Learn about [how to define an LLM-as-a-judge evaluator](/langsmith/llm-as-judge).

*Pairwise evaluators* compare outputs from two application versions using heuristics (e.g., which response is longer), LLMs (with pairwise prompts), or human reviewers.

Pairwise evaluation works well when directly scoring an output is difficult but comparing two outputs is straightforward. For example, in summarization tasks, choosing the more informative of two summaries is often easier than assigning an absolute score to a single summary.

Learn [how run pairwise evaluations](/langsmith/evaluate-pairwise).

### Reference-free vs reference-based evaluators

Understanding whether an evaluator requires reference outputs is essential for determining when it can be used.

**Reference-free evaluators** assess quality without comparing to expected outputs. These work for both offline and online evaluation:

* **Safety checks**: Toxicity detection, PII detection, content policy violations
* **Format validation**: JSON structure, required fields, schema compliance
* **Quality heuristics**: Response length, latency, specific keywords
* **Reference-free LLM-as-judge**: Clarity, coherence, helpfulness, tone

**Reference-based evaluators** require reference outputs and only work for offline evaluation:

* **Correctness**: Semantic similarity to reference answer
* **Factual accuracy**: Fact-checking against ground truth
* **Exact match**: Classification tasks with known labels
* **Reference-based LLM-as-judge**: Comparing output quality to a reference

When designing an evaluation strategy, reference-free evaluators provide consistency across both offline testing and online monitoring, while reference-based evaluators enable more precise correctness checks during development.

LangSmith supports various evaluation approaches for different stages of development and deployment. Understanding when to use each type helps build a comprehensive evaluation strategy.

Offline and online evaluations serve different purposes:

* **Offline evaluation types** test pre-deployment on curated datasets with reference outputs
* **Online evaluation types** monitor production behavior on live traffic without reference outputs

Learn more about [evaluation types and when to use each](/langsmith/evaluation-types).

### Building datasets

There are various strategies for building datasets:

**Manually curated examples**

This is the recommended starting point. Create 10–20 high-quality examples covering common scenarios and edge cases. These examples define what "good" looks like for your application.

**Historical traces**

Once in production, convert real traces into examples. For high-traffic applications:

* **User feedback**: Add runs that received negative feedback to test against.
* **Heuristics**: Identify interesting runs (e.g., long latency, errors).
* **LLM feedback**: Use LLMs to detect noteworthy conversations.

Generate additional examples from existing ones. Works best when starting with several high-quality, hand-crafted examples as templates.

### Dataset organization

Partition datasets into subsets for targeted evaluation. Use splits for performance optimization (smaller splits for rapid iteration) and interpretability (evaluate different input types separately).

Learn how to [create and manage dataset splits](/langsmith/manage-datasets-in-application#create-and-manage-dataset-splits).

LangSmith automatically creates dataset [versions](/langsmith/manage-datasets#version-a-dataset) when examples change. [Tag versions](/langsmith/manage-datasets#tag-a-version) to mark important milestones. Target specific versions in CI pipelines to ensure dataset updates don't break workflows.

### Human feedback collection

Human feedback often provides the most valuable assessment, particularly for subjective quality dimensions.

**Annotation queues**

[Annotation queues](/langsmith/annotation-queues) enable structured collection of human feedback. Flag specific runs for review, collect annotations in a streamlined interface, and transfer annotated runs to datasets for future evaluations.

Annotation queues complement [inline annotation](/langsmith/annotate-traces-inline) by offering additional capabilities: grouping runs, specifying criteria, and configuring reviewer permissions.

### Evaluations vs testing

Testing and evaluation are similar but distinct concepts.

**Evaluation measures performance according to metrics.** Metrics can be fuzzy or subjective, and prove more useful in relative terms. They typically compare systems against each other.

**Testing asserts correctness.** A system can only be deployed if it passes all tests.

Evaluation metrics can be converted into tests. For example, regression tests can assert that new versions must outperform baseline versions on relevant metrics. Run tests and evaluations together for efficiency when systems are expensive to run.

Evaluations can be written using standard testing tools like [pytest](/langsmith/pytest) or [Vitest/Jest](/langsmith/vitest-jest).

## Quick reference: Offline vs online evaluation

The following table summarizes the key differences between offline and online evaluations:

|                       | **Offline Evaluation**                                      | **Online Evaluation**                                                |
| --------------------- | ----------------------------------------------------------- | -------------------------------------------------------------------- |
| **Runs on**           | Dataset (Examples)                                          | Tracing Project (Runs/Threads)                                       |
| **Data access**       | Inputs, Outputs, Reference Outputs                          | Inputs, Outputs only                                                 |
| **When to use**       | Pre-deployment, during development                          | Production, post-deployment                                          |
| **Primary use cases** | Benchmarking, unit testing, regression testing, backtesting | Real-time monitoring, production feedback, anomaly detection         |
| **Evaluation timing** | Batch processing on curated test sets                       | Real-time or near real-time on live traffic                          |
| **Setup location**    | Evaluation tab (SDK, UI, Prompt Playground)                 | [Observability tab](/langsmith/online-evaluations) (automated rules) |
| **Data requirements** | Requires dataset curation                                   | No dataset needed, evaluates live traces                             |

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/evaluation-concepts.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

---

## For production use, consider using a configuration file or environment variables

**URL:** llms-txt#for-production-use,-consider-using-a-configuration-file-or-environment-variables

api_url = "https://api.smith.langchain.com"
api_key = os.environ.get("LANGSMITH_API_KEY")

if not api_key:
    raise ValueError("LANGSMITH_API_KEY environment variable is not set")

---

## Get Deployment

**URL:** llms-txt#get-deployment

Source: https://docs.langchain.com/api-reference/deployments-v2/get-deployment

https://api.host.langchain.com/openapi.json get /v2/deployments/{deployment_id}
Get a deployment by ID.

---

## How to interact with a deployment using RemoteGraph

**URL:** llms-txt#how-to-interact-with-a-deployment-using-remotegraph

**Contents:**
- Prerequisites
- Initialize the graph
  - Use a URL
  - Use a client
- Invoke the graph
  - Asynchronously
  - Synchronously
- Persist state at the thread level
- Use as a subgraph

Source: https://docs.langchain.com/langsmith/use-remote-graph

[`RemoteGraph`](https://reference.langchain.com/python/langsmith/deployment/remote_graph/) is a client-side interface that allows you to interact with your [deployment](/langsmith/deployments) as if it were a local graph. It provides API parity with [`CompiledGraph`](/oss/python/langgraph/graph-api#compiling-your-graph), which means that you can use the same methods (`invoke()`, `stream()`, `get_state()`, etc.) in your development and production environments. This page describes how to initialize a `RemoteGraph` and interact with it.

`RemoteGraph` is useful for the following:

* Separation of development and deployment: Build and test a graph locally with `CompiledGraph`, deploy it to LangSmith, and then [use `RemoteGraph`](#initialize-the-graph) to call it in production while working with the same API interface.
* Thread-level persistence: [Persist and fetch the state](#persist-state-at-the-thread-level) of a conversation across calls with a thread ID.
* Subgraph embedding: Compose modular graphs for a multi-agent workflow by embedding a `RemoteGraph` as a [subgraph](#use-as-a-subgraph) within another graph.
* Reusable workflows: Use deployed graphs as nodes or [tools](https://reference.langchain.com/python/langsmith/deployment/remote_graph/#langgraph.pregel.remote.RemoteGraph.as_tool), so that you can reuse and expose complex logic.

<Warning>
  **Important: Avoid calling the same deployment**

`RemoteGraph` is designed to call graphs on other deployments. Do not use `RemoteGraph` to call itself or another graph on the same deployment, as this can lead to deadlocks and resource exhaustion. Instead, use local graph composition or [subgraphs](/oss/python/langgraph/use-subgraphs) for graphs within the same deployment.
</Warning>

Before getting started with `RemoteGraph`, make sure you have:

* Access to [LangSmith](/langsmith/home), where your graphs are developed and managed.
* A running [Agent Server](/langsmith/agent-server), which hosts your deployed graphs for remote interaction.

## Initialize the graph

When initializing a `RemoteGraph`, you must always specify:

* `name`: The name of the graph you want to interact with **or** an assistant ID. If you specify a graph name, the default assistant will be used. If you specify an assistant ID, that specific assistant will be used. The graph name is the same name you use in the `langgraph.json` configuration file for your deployment.
* `api_key`: A valid [LangSmith API key](/langsmith/create-account-api-key). You can set as an environment variable (`LANGSMITH_API_KEY`) or pass directly in the `api_key` argument. You can also provide the API key in the `client` / `sync_client` arguments, if `LangGraphClient` / `SyncLangGraphClient` was initialized with the `api_key` argument.

Additionally, you have to provide one of the following:

* [`url`](#use-a-url): The URL of the deployment you want to interact with. If you pass the `url` argument, both sync and async clients will be created using the provided URL, headers (if provided), and default configuration values (e.g., timeout).
* [`client`](#use-a-client): A `LangGraphClient` instance for interacting with the deployment asynchronously (e.g., using `.astream()`, `.ainvoke()`, `.aget_state()`, `.aupdate_state()`).
* `sync_client`: A `SyncLangGraphClient` instance for interacting with the deployment synchronously (e.g., using `.stream()`, `.invoke()`, `.get_state()`, `.update_state()`).

<Note>
  If you pass both `client` or `sync_client` as well as the `url` argument, they will take precedence over the `url` argument. If none of the `client` / `sync_client` / `url` arguments are provided, `RemoteGraph` will raise a `ValueError` at runtime.
</Note>

`RemoteGraph` implements the same Runnable interface as `CompiledGraph`, so you can use it in the same way as a compiled graph. It supports the full set of standard methods, including `.invoke()`, `.stream()`, `.get_state()`, and `.update_state()`, as well as their asynchronous variants.

<Note>
  To use the graph asynchronously, you must provide either the `url` or `client` when initializing the `RemoteGraph`.
</Note>

<Note>
  To use the graph synchronously, you must provide either the `url` or `sync_client` when initializing the `RemoteGraph`.
</Note>

<CodeGroup>
  
</CodeGroup>

## Persist state at the thread level

By default, graph runs (for example, calls made with `.invoke()` or `.stream()`) are stateless, which means that intermediate checkpoints and the final state are not persisted after a run.

If you want to preserve the outputs of a run—for example, to support human-in-the-loop workflows—you can create a thread and pass its ID through the `config` argument. This works the same way as with a regular compiled graph:

<Note>
  If you need to use a `checkpointer` with a graph that has a `RemoteGraph` subgraph node, make sure to use UUIDs as thread IDs.
</Note>

A graph can also call out to multiple `RemoteGraph` instances as [*subgraph*](/oss/python/langgraph/use-subgraphs) nodes. This allows for modular, scalable workflows where different responsibilities are split across separate graphs.

`RemoteGraph` exposes the same interface as a regular `CompiledGraph`, so you can use it directly as a subgraph inside another graph. For example:

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/use-remote-graph.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
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

### Use a client

<CodeGroup>
```

Example 3 (unknown):
```unknown

```

Example 4 (unknown):
```unknown
</CodeGroup>

## Invoke the graph

`RemoteGraph` implements the same Runnable interface as `CompiledGraph`, so you can use it in the same way as a compiled graph. It supports the full set of standard methods, including `.invoke()`, `.stream()`, `.get_state()`, and `.update_state()`, as well as their asynchronous variants.

### Asynchronously

<Note>
  To use the graph asynchronously, you must provide either the `url` or `client` when initializing the `RemoteGraph`.
</Note>

<CodeGroup>
```

---

## Implement a CI/CD pipeline using LangSmith Deployment and Evaluation

**URL:** llms-txt#implement-a-ci/cd-pipeline-using-langsmith-deployment-and-evaluation

**Contents:**
- Overview
- Pipeline architecture
  - Trigger sources
  - Testing layers
- GitHub Actions workflow
  - Prerequisites
- Deployment options
  - Prerequisites for manual deployment
  - Local development and testing

Source: https://docs.langchain.com/langsmith/cicd-pipeline-example

This guide demonstrates how to implement a comprehensive CI/CD pipeline for AI agent applications deployed in LangSmith Deployment. In this example, you'll use the [LangGraph](/oss/python/langgraph/overview) open source framework for orchestrating and building the agent, [LangSmith](/langsmith/home) for observability and evaluations. This pipeline is based on the [cicd-pipeline-example repository](https://github.com/langchain-ai/cicd-pipeline-example).

The CI/CD pipeline provides:

* <Icon icon="check-circle" /> **Automated testing**: Unit, integration, and end-to-end tests.
* <Icon icon="chart-line" /> **Offline evaluations**: Performance assessment using [AgentEvals](https://github.com/langchain-ai/agentevals), [OpenEvals](https://github.com/langchain-ai/openevals) and [LangSmith](https://docs.langchain.com/langsmith/home).
* <Icon icon="rocket" /> **Preview and production deployments**: Automated staging and quality-gated production releases using the Control Plane API.
* <Icon icon="eye" /> **Monitoring**: Continuous evaluation and alerting.

## Pipeline architecture

The CI/CD pipeline consists of several key components that work together to ensure code quality and reliable deployments:

There are multiple ways you can trigger this pipeline, either during development or if your application is already live. The pipeline can be triggered by:

* <Icon icon="code-branch" /> **Code changes**: Pushes to main/development branches where you can modify the LangGraph architecture, try different models, update agent logic, or make any code improvements.
* <Icon icon="edit" /> **PromptHub updates**: Changes to prompt templates stored in LangSmith PromptHub—whenever there's a new prompt commit, the system triggers a webhook to run the pipeline.
* <Icon icon="exclamation-triangle" /> **Online evaluation alerts**: Performance degradation notifications from live deployments
* <Icon icon="webhook" /> **LangSmith traces webhooks**: Automated triggers based on trace analysis and performance metrics.
* <Icon icon="play" /> **Manual trigger**: Manual initiation of the pipeline for testing or emergency deployments.

Compared to traditional software, testing AI agent applications also requires assessing response quality, so it is important to test each part of the workflow. The pipeline implements multiple testing layers:

1. <Icon icon="puzzle-piece" /> **Unit tests**: Individual node and utility function testing.
2. <Icon icon="link" /> **Integration tests**: Component interaction testing.
3. <Icon icon="route" /> **End-to-end tests**: Full graph execution testing.
4. <Icon icon="brain" /> **Offline evaluations**: Performance assessment with real-world scenarios including end-to-end evaluations, single-step evaluations, agent trajectory analysis, and multi-turn simulations.
5. <Icon icon="server" /> **LangGraph dev server tests**: Use the [langgraph-cli](/langsmith/cli) tool for spinning up (inside the GitHub Action) a local server to run the LangGraph agent. This polls the `/ok` server API endpoint until it is available and for 30 seconds, after that it throws an error.

## GitHub Actions workflow

The CI/CD pipeline uses GitHub Actions with the [Control Plane API](/langsmith/api-ref-control-plane) and [LangSmith API](https://api.smith.langchain.com/redoc) to automate deployment. A helper script manages API interactions and deployments: [https://github.com/langchain-ai/cicd-pipeline-example/blob/main/.github/scripts/langgraph\_api.py](https://github.com/langchain-ai/cicd-pipeline-example/blob/main/.github/scripts/langgraph_api.py).

The workflow includes:

* **New agent deployment**: When a new PR is opened and tests pass, a new preview deployment is created in LangSmith Deployment using the [Control Plane API](/langsmith/api-ref-control-plane). This allows you to test the agent in a staging environment before promoting to production.

* **Agent deployment revision**: A revision happens when an existing deployment with the same ID is found, or when the PR is merged into main. In the case of merging to main, the preview deployment is deleted and a production deployment is created. This ensures that any updates to the agent are properly deployed and integrated into the production infrastructure.

<img src="https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-new-lgp-revision.png?fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=3ef7d51a322b8b5e2f9c2c70579fcc97" alt="Agent Deployment Revision Workflow" data-og-width="1022" width="1022" data-og-height="196" height="196" data-path="langsmith/images/cicd-new-lgp-revision.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-new-lgp-revision.png?w=280&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=a3d06c339e84a1af99450d23e8bd617f 280w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-new-lgp-revision.png?w=560&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=30589c8727af3ecb1d97881fd6692554 560w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-new-lgp-revision.png?w=840&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=c05ab515ea0901fb2d076dee256ad108 840w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-new-lgp-revision.png?w=1100&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=b939ad6842110227f70cc0526468d21d 1100w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-new-lgp-revision.png?w=1650&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=0559d5b2a85414e954a72377b2eed9ec 1650w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-new-lgp-revision.png?w=2500&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=b8b96047a8b37f31b78d793cd7d18f45 2500w" />

* **Testing and evaluation workflow**: In addition to the more traditional testing phases (unit tests, integration tests, end-to-end tests, etc.), the pipeline includes [offline evaluations](/langsmith/evaluation-concepts#offline-evaluation) and [Agent dev server testing](/langsmith/local-server) because you want to test the quality of your agent. These evaluations provide comprehensive assessment of the agent's performance using real-world scenarios and data.

<img src="https://mintcdn.com/langchain-5e9cc07a/MrTet_AXQVddxOlO/langsmith/images/cicd-test-with-results.png?fit=max&auto=format&n=MrTet_AXQVddxOlO&q=85&s=477c3f5ec3d9bb9dfc354b9a57860636" alt="Test with Results Workflow" data-og-width="2050" width="2050" data-og-height="996" height="996" data-path="langsmith/images/cicd-test-with-results.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/MrTet_AXQVddxOlO/langsmith/images/cicd-test-with-results.png?w=280&fit=max&auto=format&n=MrTet_AXQVddxOlO&q=85&s=7c5885b5f85c1c408fda449c5a0c706a 280w, https://mintcdn.com/langchain-5e9cc07a/MrTet_AXQVddxOlO/langsmith/images/cicd-test-with-results.png?w=560&fit=max&auto=format&n=MrTet_AXQVddxOlO&q=85&s=3b9a25332a9f6b56edfc9fbbfec248c1 560w, https://mintcdn.com/langchain-5e9cc07a/MrTet_AXQVddxOlO/langsmith/images/cicd-test-with-results.png?w=840&fit=max&auto=format&n=MrTet_AXQVddxOlO&q=85&s=380cb346fffbaf13365b37c6fa955c05 840w, https://mintcdn.com/langchain-5e9cc07a/MrTet_AXQVddxOlO/langsmith/images/cicd-test-with-results.png?w=1100&fit=max&auto=format&n=MrTet_AXQVddxOlO&q=85&s=8994d1e816e725865f90a2ac6601f7a4 1100w, https://mintcdn.com/langchain-5e9cc07a/MrTet_AXQVddxOlO/langsmith/images/cicd-test-with-results.png?w=1650&fit=max&auto=format&n=MrTet_AXQVddxOlO&q=85&s=42b752f1e5f0043dd6998ae372e83874 1650w, https://mintcdn.com/langchain-5e9cc07a/MrTet_AXQVddxOlO/langsmith/images/cicd-test-with-results.png?w=2500&fit=max&auto=format&n=MrTet_AXQVddxOlO&q=85&s=043be8ed1ef59cea171f30146790a877 2500w" />

<AccordionGroup>
    <Accordion title="Final Response Evaluation" icon="check-circle">
      Evaluates the final output of your agent against expected results. This is the most common type of evaluation that checks if the agent's final response meets quality standards and answers the user's question correctly.
    </Accordion>

<Accordion title="Single Step Evaluation" icon="step-forward">
      Tests individual steps or nodes within your LangGraph workflow. This allows you to validate specific components of your agent's logic in isolation, ensuring each step functions correctly before testing the full pipeline.
    </Accordion>

<Accordion title="Agent Trajectory Evaluation" icon="route">
      Analyzes the complete path your agent takes through the graph, including all intermediate steps and decision points. This helps identify bottlenecks, unnecessary steps, or suboptimal routing in your agent's workflow. It also evaluates whether your agent invoked the right tools in the right order or at the right time.
    </Accordion>

<Accordion title="Multi-Turn Evaluation" icon="comments">
      Tests conversational flows where the agent maintains context across multiple interactions. This is crucial for agents that handle follow-up questions, clarifications, or extended dialogues with users.
    </Accordion>
  </AccordionGroup>

See the [LangGraph testing documentation](/oss/python/langgraph/test) for specific testing approaches and the [evaluation approaches guide](/langsmith/evaluation-approaches) for a comprehensive overview of offline evaluations.

Before setting up the CI/CD pipeline, ensure you have:

* <Icon icon="robot" /> An AI agent application (in this case built using [LangGraph](/oss/python/langgraph/overview))
* <Icon icon="user" /> A [LangSmith account](https://smith.langchain.com/)
* <Icon icon="key" /> A [LangSmith API key](/langsmith/create-account-api-key) needed to deploy agents and retrieve experiment results
* <Icon icon="cog" /> Project-specific environment variables configured in your repository secrets (e.g., LLM model API keys, vector store credentials, database connections)

<Note>
  While this example uses GitHub, the CI/CD pipeline works with other Git hosting platforms including GitLab, Bitbucket, and others.
</Note>

## Deployment options

LangSmith supports multiple deployment methods, depending on how your [LangSmith instance is hosted](/langsmith/platform-setup):

* <Icon icon="cloud" /> **Cloud LangSmith**: Direct GitHub integration.
* <Icon icon="server" /> **Self-Hosted/Hybrid**: Container registry-based deployments.

The deployment flow starts by modifying your agent implementation. At minimum, you must have a [`langgraph.json`](/langsmith/application-structure) and dependency file in your project (`requirements.txt` or `pyproject.toml`). Use the `langgraph dev` CLI tool to check for errors—fix any errors; otherwise, the deployment will succeed when deployed to LangSmith Deployment.

### Prerequisites for manual deployment

Before deploying your agent, ensure you have:

1. <Icon icon="project-diagram" /> **LangGraph graph**: Your agent implementation (e.g., `./agents/simple_text2sql.py:agent`).
2. <Icon icon="box" /> **Dependencies**: Either `requirements.txt` or `pyproject.toml` with all required packages.
3. <Icon icon="cog" /> **Configuration**: `langgraph.json` file specifying:
   * Path to your agent graph
   * Dependencies location
   * Environment variables
   * Python version

Example `langgraph.json`:

### Local development and testing

<img src="https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-studio-cli.png?fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=425460d3401221ab441e21fc706c9cf1" alt="Studio CLI Interface" data-og-width="2972" width="2972" data-og-height="1354" height="1354" data-path="langsmith/images/cicd-studio-cli.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-studio-cli.png?w=280&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=35e64359dba47f4db4962148073cfadb 280w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-studio-cli.png?w=560&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=c12eb479d5c46921633c56bdead978bc 560w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-studio-cli.png?w=840&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=b36efc12f81027b7364cea82a4600fc3 840w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-studio-cli.png?w=1100&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=131c3fa2e989fbb8ebc4748a5790dc36 1100w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-studio-cli.png?w=1650&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=afa56b4e5ca02495ef5e7cb69d8e1329 1650w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-studio-cli.png?w=2500&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=774ec3dcf76a4b0e61989cd12e41e0c3 2500w" />

First, test your agent locally using [Studio](/langsmith/studio):

```bash  theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### Trigger sources

There are multiple ways you can trigger this pipeline, either during development or if your application is already live. The pipeline can be triggered by:

* <Icon icon="code-branch" /> **Code changes**: Pushes to main/development branches where you can modify the LangGraph architecture, try different models, update agent logic, or make any code improvements.
* <Icon icon="edit" /> **PromptHub updates**: Changes to prompt templates stored in LangSmith PromptHub—whenever there's a new prompt commit, the system triggers a webhook to run the pipeline.
* <Icon icon="exclamation-triangle" /> **Online evaluation alerts**: Performance degradation notifications from live deployments
* <Icon icon="webhook" /> **LangSmith traces webhooks**: Automated triggers based on trace analysis and performance metrics.
* <Icon icon="play" /> **Manual trigger**: Manual initiation of the pipeline for testing or emergency deployments.

### Testing layers

Compared to traditional software, testing AI agent applications also requires assessing response quality, so it is important to test each part of the workflow. The pipeline implements multiple testing layers:

1. <Icon icon="puzzle-piece" /> **Unit tests**: Individual node and utility function testing.
2. <Icon icon="link" /> **Integration tests**: Component interaction testing.
3. <Icon icon="route" /> **End-to-end tests**: Full graph execution testing.
4. <Icon icon="brain" /> **Offline evaluations**: Performance assessment with real-world scenarios including end-to-end evaluations, single-step evaluations, agent trajectory analysis, and multi-turn simulations.
5. <Icon icon="server" /> **LangGraph dev server tests**: Use the [langgraph-cli](/langsmith/cli) tool for spinning up (inside the GitHub Action) a local server to run the LangGraph agent. This polls the `/ok` server API endpoint until it is available and for 30 seconds, after that it throws an error.

## GitHub Actions workflow

The CI/CD pipeline uses GitHub Actions with the [Control Plane API](/langsmith/api-ref-control-plane) and [LangSmith API](https://api.smith.langchain.com/redoc) to automate deployment. A helper script manages API interactions and deployments: [https://github.com/langchain-ai/cicd-pipeline-example/blob/main/.github/scripts/langgraph\_api.py](https://github.com/langchain-ai/cicd-pipeline-example/blob/main/.github/scripts/langgraph_api.py).

The workflow includes:

* **New agent deployment**: When a new PR is opened and tests pass, a new preview deployment is created in LangSmith Deployment using the [Control Plane API](/langsmith/api-ref-control-plane). This allows you to test the agent in a staging environment before promoting to production.

* **Agent deployment revision**: A revision happens when an existing deployment with the same ID is found, or when the PR is merged into main. In the case of merging to main, the preview deployment is deleted and a production deployment is created. This ensures that any updates to the agent are properly deployed and integrated into the production infrastructure.

  <img src="https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-new-lgp-revision.png?fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=3ef7d51a322b8b5e2f9c2c70579fcc97" alt="Agent Deployment Revision Workflow" data-og-width="1022" width="1022" data-og-height="196" height="196" data-path="langsmith/images/cicd-new-lgp-revision.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-new-lgp-revision.png?w=280&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=a3d06c339e84a1af99450d23e8bd617f 280w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-new-lgp-revision.png?w=560&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=30589c8727af3ecb1d97881fd6692554 560w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-new-lgp-revision.png?w=840&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=c05ab515ea0901fb2d076dee256ad108 840w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-new-lgp-revision.png?w=1100&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=b939ad6842110227f70cc0526468d21d 1100w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-new-lgp-revision.png?w=1650&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=0559d5b2a85414e954a72377b2eed9ec 1650w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-new-lgp-revision.png?w=2500&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=b8b96047a8b37f31b78d793cd7d18f45 2500w" />

* **Testing and evaluation workflow**: In addition to the more traditional testing phases (unit tests, integration tests, end-to-end tests, etc.), the pipeline includes [offline evaluations](/langsmith/evaluation-concepts#offline-evaluation) and [Agent dev server testing](/langsmith/local-server) because you want to test the quality of your agent. These evaluations provide comprehensive assessment of the agent's performance using real-world scenarios and data.

  <img src="https://mintcdn.com/langchain-5e9cc07a/MrTet_AXQVddxOlO/langsmith/images/cicd-test-with-results.png?fit=max&auto=format&n=MrTet_AXQVddxOlO&q=85&s=477c3f5ec3d9bb9dfc354b9a57860636" alt="Test with Results Workflow" data-og-width="2050" width="2050" data-og-height="996" height="996" data-path="langsmith/images/cicd-test-with-results.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/MrTet_AXQVddxOlO/langsmith/images/cicd-test-with-results.png?w=280&fit=max&auto=format&n=MrTet_AXQVddxOlO&q=85&s=7c5885b5f85c1c408fda449c5a0c706a 280w, https://mintcdn.com/langchain-5e9cc07a/MrTet_AXQVddxOlO/langsmith/images/cicd-test-with-results.png?w=560&fit=max&auto=format&n=MrTet_AXQVddxOlO&q=85&s=3b9a25332a9f6b56edfc9fbbfec248c1 560w, https://mintcdn.com/langchain-5e9cc07a/MrTet_AXQVddxOlO/langsmith/images/cicd-test-with-results.png?w=840&fit=max&auto=format&n=MrTet_AXQVddxOlO&q=85&s=380cb346fffbaf13365b37c6fa955c05 840w, https://mintcdn.com/langchain-5e9cc07a/MrTet_AXQVddxOlO/langsmith/images/cicd-test-with-results.png?w=1100&fit=max&auto=format&n=MrTet_AXQVddxOlO&q=85&s=8994d1e816e725865f90a2ac6601f7a4 1100w, https://mintcdn.com/langchain-5e9cc07a/MrTet_AXQVddxOlO/langsmith/images/cicd-test-with-results.png?w=1650&fit=max&auto=format&n=MrTet_AXQVddxOlO&q=85&s=42b752f1e5f0043dd6998ae372e83874 1650w, https://mintcdn.com/langchain-5e9cc07a/MrTet_AXQVddxOlO/langsmith/images/cicd-test-with-results.png?w=2500&fit=max&auto=format&n=MrTet_AXQVddxOlO&q=85&s=043be8ed1ef59cea171f30146790a877 2500w" />

  <AccordionGroup>
    <Accordion title="Final Response Evaluation" icon="check-circle">
      Evaluates the final output of your agent against expected results. This is the most common type of evaluation that checks if the agent's final response meets quality standards and answers the user's question correctly.
    </Accordion>

    <Accordion title="Single Step Evaluation" icon="step-forward">
      Tests individual steps or nodes within your LangGraph workflow. This allows you to validate specific components of your agent's logic in isolation, ensuring each step functions correctly before testing the full pipeline.
    </Accordion>

    <Accordion title="Agent Trajectory Evaluation" icon="route">
      Analyzes the complete path your agent takes through the graph, including all intermediate steps and decision points. This helps identify bottlenecks, unnecessary steps, or suboptimal routing in your agent's workflow. It also evaluates whether your agent invoked the right tools in the right order or at the right time.
    </Accordion>

    <Accordion title="Multi-Turn Evaluation" icon="comments">
      Tests conversational flows where the agent maintains context across multiple interactions. This is crucial for agents that handle follow-up questions, clarifications, or extended dialogues with users.
    </Accordion>
  </AccordionGroup>

  See the [LangGraph testing documentation](/oss/python/langgraph/test) for specific testing approaches and the [evaluation approaches guide](/langsmith/evaluation-approaches) for a comprehensive overview of offline evaluations.

### Prerequisites

Before setting up the CI/CD pipeline, ensure you have:

* <Icon icon="robot" /> An AI agent application (in this case built using [LangGraph](/oss/python/langgraph/overview))
* <Icon icon="user" /> A [LangSmith account](https://smith.langchain.com/)
* <Icon icon="key" /> A [LangSmith API key](/langsmith/create-account-api-key) needed to deploy agents and retrieve experiment results
* <Icon icon="cog" /> Project-specific environment variables configured in your repository secrets (e.g., LLM model API keys, vector store credentials, database connections)

<Note>
  While this example uses GitHub, the CI/CD pipeline works with other Git hosting platforms including GitLab, Bitbucket, and others.
</Note>

## Deployment options

LangSmith supports multiple deployment methods, depending on how your [LangSmith instance is hosted](/langsmith/platform-setup):

* <Icon icon="cloud" /> **Cloud LangSmith**: Direct GitHub integration.
* <Icon icon="server" /> **Self-Hosted/Hybrid**: Container registry-based deployments.

The deployment flow starts by modifying your agent implementation. At minimum, you must have a [`langgraph.json`](/langsmith/application-structure) and dependency file in your project (`requirements.txt` or `pyproject.toml`). Use the `langgraph dev` CLI tool to check for errors—fix any errors; otherwise, the deployment will succeed when deployed to LangSmith Deployment.
```

Example 2 (unknown):
```unknown
### Prerequisites for manual deployment

Before deploying your agent, ensure you have:

1. <Icon icon="project-diagram" /> **LangGraph graph**: Your agent implementation (e.g., `./agents/simple_text2sql.py:agent`).
2. <Icon icon="box" /> **Dependencies**: Either `requirements.txt` or `pyproject.toml` with all required packages.
3. <Icon icon="cog" /> **Configuration**: `langgraph.json` file specifying:
   * Path to your agent graph
   * Dependencies location
   * Environment variables
   * Python version

Example `langgraph.json`:
```

Example 3 (unknown):
```unknown
### Local development and testing

<img src="https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-studio-cli.png?fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=425460d3401221ab441e21fc706c9cf1" alt="Studio CLI Interface" data-og-width="2972" width="2972" data-og-height="1354" height="1354" data-path="langsmith/images/cicd-studio-cli.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-studio-cli.png?w=280&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=35e64359dba47f4db4962148073cfadb 280w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-studio-cli.png?w=560&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=c12eb479d5c46921633c56bdead978bc 560w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-studio-cli.png?w=840&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=b36efc12f81027b7364cea82a4600fc3 840w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-studio-cli.png?w=1100&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=131c3fa2e989fbb8ebc4748a5790dc36 1100w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-studio-cli.png?w=1650&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=afa56b4e5ca02495ef5e7cb69d8e1329 1650w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-studio-cli.png?w=2500&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=774ec3dcf76a4b0e61989cd12e41e0c3 2500w" />

First, test your agent locally using [Studio](/langsmith/studio):
```

---

## LangSmith Deployment

**URL:** llms-txt#langsmith-deployment

**Contents:**
- Prerequisites
- Deploy your agent
  - 1. Create a repository on GitHub
  - 2. Deploy to LangSmith
  - 3. Test your application in Studio
  - 4. Get the API URL for your deployment
  - 5. Test the API

Source: https://docs.langchain.com/oss/python/langgraph/deploy

This guide shows you how to deploy your agent to **[LangSmith Cloud](/langsmith/deploy-to-cloud)**, a fully managed hosting platform designed for agent workloads. With Cloud deployment, you can deploy directly from your GitHub repository—LangSmith handles the infrastructure, scaling, and operational concerns.

Traditional hosting platforms are built for stateless, short-lived web applications. LangSmith Cloud is **purpose-built for stateful, long-running agents** that require persistent state and background execution.

<Tip>
  LangSmith offers multiple deployment options beyond Cloud, including deploying with a [control plane (hybrid/self-hosted)](/langsmith/deploy-with-control-plane) or as [standalone servers](/langsmith/deploy-standalone-server). For more information, refer to the [Deployment overview](/langsmith/deployments).
</Tip>

Before you begin, ensure you have the following:

* A [GitHub account](https://github.com/)
* A [LangSmith account](https://smith.langchain.com/) (free to sign up)

### 1. Create a repository on GitHub

Your application's code must reside in a GitHub repository to be deployed on LangSmith. Both public and private repositories are supported. For this quickstart, first make sure your app is LangGraph-compatible by following the [local server setup guide](/oss/python/langgraph/studio#setup-local-agent-server). Then, push your code to the repository.

### 2. Deploy to LangSmith

<Steps>
  <Step title="Navigate to LangSmith Deployment">
    Log in to [LangSmith](https://smith.langchain.com/). In the left sidebar, select **Deployments**.
  </Step>

<Step title="Create new deployment">
    Click the **+ New Deployment** button. A pane will open where you can fill in the required fields.
  </Step>

<Step title="Link repository">
    If you are a first time user or adding a private repository that has not been previously connected, click the **Add new account** button and follow the instructions to connect your GitHub account.
  </Step>

<Step title="Deploy repository">
    Select your application's repository. Click **Submit** to deploy. This may take about 15 minutes to complete. You can check the status in the **Deployment details** view.
  </Step>
</Steps>

### 3. Test your application in Studio

Once your application is deployed:

1. Select the deployment you just created to view more details.
2. Click the **Studio** button in the top right corner. Studio will open to display your graph.

### 4. Get the API URL for your deployment

1. In the **Deployment details** view in LangGraph, click the **API URL** to copy it to your clipboard.
2. Click the `URL` to copy it to the clipboard.

You can now test the API:

<Tabs>
  <Tab title="Python">
    1. Install LangGraph Python:

2. Send a message to the agent:

<Tab title="Rest API">
    
  </Tab>
</Tabs>

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langgraph/deploy.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

**Examples:**

Example 1 (unknown):
```unknown
2. Send a message to the agent:
```

Example 2 (unknown):
```unknown
</Tab>

  <Tab title="Rest API">
```

---

## LangSmith docs

**URL:** llms-txt#langsmith-docs

**Contents:**
- Get started
  - More ways to build
- Workflow

Source: https://docs.langchain.com/langsmith/home

**LangSmith provides tools for developing, debugging, and deploying LLM applications.**
It helps you trace requests, evaluate outputs, test prompts, and manage deployments in one place.
LangSmith is framework agnostic, so you can use it with or without LangChain's open-source libraries
[`langchain`](/oss/python/langchain/overview) and [`langgraph`](/oss/python/langgraph/overview).
Prototype locally, then move to production with integrated monitoring and evaluation to build more reliable AI systems.

<Callout icon="bullhorn" color="#DFC5FE" iconType="regular">
  LangGraph Platform is now [LangSmith Deployment](/langsmith/deployments). For more information, check out the [Changelog](https://changelog.langchain.com/announcements/product-naming-changes-langsmith-deployment-and-langsmith-studio).
</Callout>

<Steps>
  <Step title="Create an account" icon="user-plus">
    Sign up at [smith.langchain.com](https://smith.langchain.com) (no credit card required).
    You can log in with **Google**, **GitHub**, or **email**.
  </Step>

<Step title="Create an API key" icon="key">
    Go to your [Settings page](https://smith.langchain.com/settings) → **API Keys** → **Create API Key**.
    Copy the key and save it securely.
  </Step>
</Steps>

Once your account and API key are ready, choose a quickstart to begin building with LangSmith:

<Columns cols={3}>
  <Card title="Observability" icon="magnifying-glass" href="/langsmith/observability-quickstart" arrow="true" cta="Start tracing">
    Gain visibility into every step your application takes to debug faster and improve reliability.
  </Card>

<Card title="Evaluation" icon="chart-line" href="/langsmith/evaluation-quickstart" arrow="true" cta="Evaluate your app">
    Measure and track quality over time to ensure your AI applications are consistent and trustworthy.
  </Card>

<Card title="Deployment" icon="cloud-arrow-up" iconType="solid" href="/langsmith/deployments" arrow="true" cta="Deploy your agents">
    Deploy your agents as Agent Servers, ready to scale in production.
  </Card>
</Columns>

### More ways to build

<Columns cols={2}>
  <Card title="Platform setup" icon="server" iconType="solid" href="/langsmith/platform-setup" arrow="true" cta="Choose how to set up LangSmith">
    Use LangSmith in managed cloud, in a self-hosted environment, or hybrid to match your infrastructure and compliance needs.
  </Card>

<Card title="Agent Builder (Beta)" icon="sparkles" href="/langsmith/agent-builder" arrow="true" cta="Build an agent">
    Design and deploy AI agents visually with a no-code interface—perfect for rapid prototyping and getting started without writing code.
  </Card>

<Card title="Studio" icon="window" href="/langsmith/quick-start-studio" arrow="true" cta="Develop with Studio">
    Use a visual interface to design, test, and refine applications end-to-end.
  </Card>

<Card title="Prompt testing" icon="flask" href="/langsmith/prompt-engineering-quickstart" arrow="true" cta="Test your prompts">
    Iterate on prompts with built-in versioning and collaboration to ship improvements faster.
  </Card>
</Columns>

<Callout icon="lock" color="#DFC5FE" iconType="regular">
  LangSmith meets the highest standards of data security and privacy with HIPAA, SOC 2 Type 2, and GDPR compliance. For more information, see the [Trust Center](https://trust.langchain.com/).
</Callout>

LangSmith combines observability, evaluation, deployment, and platform setup in one integrated workflow—from local development to production.

<img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/gnE-C9CZc2IgnmJo/langsmith/images/overview-light.svg?fit=max&auto=format&n=gnE-C9CZc2IgnmJo&q=85&s=84312d9c72c44e44ac513eaa78abefc6" alt="Diagram showing how LangSmith integrates observability, evaluation, deployment, and platform setup in a single workflow from development to production." data-og-width="1138" width="1138" data-og-height="549" height="549" data-path="langsmith/images/overview-light.svg" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/gnE-C9CZc2IgnmJo/langsmith/images/overview-light.svg?w=280&fit=max&auto=format&n=gnE-C9CZc2IgnmJo&q=85&s=32fa495af106d1eb30c9d512b59c3926 280w, https://mintcdn.com/langchain-5e9cc07a/gnE-C9CZc2IgnmJo/langsmith/images/overview-light.svg?w=560&fit=max&auto=format&n=gnE-C9CZc2IgnmJo&q=85&s=f30ac54ecdc55dd22b5762800f33a5bb 560w, https://mintcdn.com/langchain-5e9cc07a/gnE-C9CZc2IgnmJo/langsmith/images/overview-light.svg?w=840&fit=max&auto=format&n=gnE-C9CZc2IgnmJo&q=85&s=aee1643d7b4ab4cf74ffb54b555e3788 840w, https://mintcdn.com/langchain-5e9cc07a/gnE-C9CZc2IgnmJo/langsmith/images/overview-light.svg?w=1100&fit=max&auto=format&n=gnE-C9CZc2IgnmJo&q=85&s=65946469f91ff9cfbd26d154d31c6caf 1100w, https://mintcdn.com/langchain-5e9cc07a/gnE-C9CZc2IgnmJo/langsmith/images/overview-light.svg?w=1650&fit=max&auto=format&n=gnE-C9CZc2IgnmJo&q=85&s=a310e56592be23e233075ebffa1b124d 1650w, https://mintcdn.com/langchain-5e9cc07a/gnE-C9CZc2IgnmJo/langsmith/images/overview-light.svg?w=2500&fit=max&auto=format&n=gnE-C9CZc2IgnmJo&q=85&s=f9e2edcac083797d0498806cb512d5de 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/Dai6LUVulRwLjxET/langsmith/images/overview-dark.svg?fit=max&auto=format&n=Dai6LUVulRwLjxET&q=85&s=f930d2f475ab68e1cdfe7105b5f1abe6" alt="Diagram showing how LangSmith integrates observability, evaluation, deployment, and platform setup in a single workflow from development to production." data-og-width="1157" width="1157" data-og-height="549" height="549" data-path="langsmith/images/overview-dark.svg" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/Dai6LUVulRwLjxET/langsmith/images/overview-dark.svg?w=280&fit=max&auto=format&n=Dai6LUVulRwLjxET&q=85&s=cab90851ba7c49d855f89c86f6bfdd0b 280w, https://mintcdn.com/langchain-5e9cc07a/Dai6LUVulRwLjxET/langsmith/images/overview-dark.svg?w=560&fit=max&auto=format&n=Dai6LUVulRwLjxET&q=85&s=d04a2b423106d1f64fa0a3a05948a19a 560w, https://mintcdn.com/langchain-5e9cc07a/Dai6LUVulRwLjxET/langsmith/images/overview-dark.svg?w=840&fit=max&auto=format&n=Dai6LUVulRwLjxET&q=85&s=84c821c5464a20cf4a3d397e5baf7357 840w, https://mintcdn.com/langchain-5e9cc07a/Dai6LUVulRwLjxET/langsmith/images/overview-dark.svg?w=1100&fit=max&auto=format&n=Dai6LUVulRwLjxET&q=85&s=202f8ed1e7c38c5a6184b9e1b2ea377f 1100w, https://mintcdn.com/langchain-5e9cc07a/Dai6LUVulRwLjxET/langsmith/images/overview-dark.svg?w=1650&fit=max&auto=format&n=Dai6LUVulRwLjxET&q=85&s=f8d03af520cd2f0363f9b41f86428396 1650w, https://mintcdn.com/langchain-5e9cc07a/Dai6LUVulRwLjxET/langsmith/images/overview-dark.svg?w=2500&fit=max&auto=format&n=Dai6LUVulRwLjxET&q=85&s=576885f21fd2e6bc4ecb4e4176515a3d 2500w" />

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/home.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

---

## List Deployments

**URL:** llms-txt#list-deployments

Source: https://docs.langchain.com/api-reference/deployments-v2/list-deployments

https://api.host.langchain.com/openapi.json get /v2/deployments
List all deployments.

---

## Patch Deployment

**URL:** llms-txt#patch-deployment

Source: https://docs.langchain.com/api-reference/deployments-v2/patch-deployment

https://api.host.langchain.com/openapi.json patch /v2/deployments/{deployment_id}
Patch a deployment by ID.

---

## Section 2: Full Observability Stack

**URL:** llms-txt#section-2:-full-observability-stack

**Contents:**
- Prerequisites
  - 1. Compute Resources
  - 2. Cert-Manager
  - 3. OpenTelemetry Operator
- Installation
- Post-Installation
  - Enable Logs and Traces in LangSmith
- Grafana Usage

<Warning>
  **This is not a production observability stack. Use this to gain quick insight into logs, metrics and traces for your deployment. This is only made to handle a few dozen GB of data per day.**
</Warning>

This section will show you how to deploy the end-to-end observability stack for LangSmith, using the [Helm Chart](https://github.com/langchain-ai/helm/tree/main/charts/langsmith-observability).

This chart is built around the open-source LGTM Stack from Grafana. It consists of:

* [Loki](https://grafana.com/docs/loki/latest/) for logs.
* [Mimir](https://grafana.com/docs/mimir/latest/) for metrics + alerting.
* [Tempo](https://grafana.com/docs/tempo/latest/) for traces.
* [Grafana](https://grafana.com/docs/grafana/latest/) for monitoring UI.

As well as [OpenTelemetry Collectors](https://opentelemetry.io/docs/collector/) for gathering the telemetry data.

### 1. Compute Resources

The resource requests and limits for each part of the stack can be modified in the helm chart. Here are the current allocations (request/limit):

* Loki: `2vCPU/3vCPU + 2Gi/4Gi`
* Mimir: `1vCPU/2vCPU + 2Gi/4Gi`
* Tempo: `1vCPU/2vCPU + 4Gi/6Gi`

Make sure you have those resources allocated before bringing up the helm chart, or modify the resource values in your helm configuration file.

The helm chart uses the OpenTelemetry Operator to provision collectors. The operator require that you have [cert-manager](https://cert-manager.io/docs/installation/) installed in your Kubernetes cluster.

If you do not have it installed, you can run the following commands:

### 3. OpenTelemetry Operator

Use the following to install the OpenTelemetry Operator:

The following instructions will bring up OTel collectors, the LGTM stack, Grafana and Prometheus exporters.

1. Create a local file called `langsmith_obs_config.yaml`
2. Copy over the values from this [file](https://github.com/langchain-ai/helm/blob/main/charts/langsmith-observability/examples/e2e-stack.yaml) into `langsmith_obs_config.yaml`, making sure to modify the values to match your LangSmith deployment.
3. Find the latest version of the chart by running `helm search repo langchain/langsmith-observability --versions`.
4. Grab the latest version number, and run `helm install langsmith-observability langchain/langsmith-observability --values langsmith_obs_config.yaml --version <version> -n <namespace> --wait --debug`

<Note>
  **You can selectively collect logs, metrics or traces by modifying the boolean values under `otelCollector` in your config file. You can also selectively bring up each respective piece of the backend (Loki, Mimir, Tempo).**
</Note>

You should see the following if the install went through:

And if you run `kubectl get pods -n langsmith-observability`, you should see:

### Enable Logs and Traces in LangSmith

Once you have installed the observability helm chart, you need to set the following values in your *LangSmith* helm configuration file to enable collection of logs and traces.

<Info>
  1. To get `${LANGSMITH_OTEL_CRD_NAME}`, you can run `kubectl get opentelemetrycollectors -n ${LANGSMITH_OBS_NAMESPACE}` and select the name of the one with MODE = `sidecar`
  2. To get `${GATEWAY_COLLECTOR_SERVICE_NAME}` name, run `kubectl get services -n ${LANGSMITH_OBS_NAMESPACE}` and select the one with Ports 4317/4318 AND a ClusterIP set. It should be something like `langsmith-observability-collector-gateway-collector`
</Info>

Now run `helm upgrade langsmith langchain/langsmith --values langsmith_config.yaml -n <langsmith-namespace> --wait --debug`

Once upgraded, if you run `kubectl get pods -n <langsmith-namespace>` you should see the following (note the 2/2 for sidecar collectors):

Once everything is installed, do the following: to get your Grafana password:

Then port-forward into the `langsmith-observability-grafana` container at port 3000, and open your browser as `localhost:3000`. Use the username `admin` and the password from the secret above to log into Grafana.

Once in Grafana, you can use the UI to monitor logs, metrics and traces. Grafana also comes pre-packaged with sets of dashboards for monitoring the main components of your deployment.

<img src="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/langsmith-grafana-dashboards.png?fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=ee47243826737bab23944e01536dec71" alt="LangSmith Grafana Dashboards" data-og-width="1715" width="1715" data-og-height="1073" height="1073" data-path="langsmith/images/langsmith-grafana-dashboards.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/langsmith-grafana-dashboards.png?w=280&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=11e0d71897053d012e929ca49533d6dd 280w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/langsmith-grafana-dashboards.png?w=560&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=0e674be629c1c1e795e1b6e686ca28e2 560w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/langsmith-grafana-dashboards.png?w=840&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=fb3bcdc4fa39e82fe9f3370834c7f7fa 840w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/langsmith-grafana-dashboards.png?w=1100&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=80c401f8794ac0671207e1a260aac25b 1100w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/langsmith-grafana-dashboards.png?w=1650&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=3f5baa041ab9e5c39b7d8a62e2bfe1e5 1650w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/langsmith-grafana-dashboards.png?w=2500&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=7620f91021593db1d87c92fc43d8fe2b 2500w" />

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/observability-stack.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

**Examples:**

Example 1 (unknown):
```unknown
### 3. OpenTelemetry Operator

Use the following to install the OpenTelemetry Operator:
```

Example 2 (unknown):
```unknown
## Installation

The following instructions will bring up OTel collectors, the LGTM stack, Grafana and Prometheus exporters.

1. Create a local file called `langsmith_obs_config.yaml`
2. Copy over the values from this [file](https://github.com/langchain-ai/helm/blob/main/charts/langsmith-observability/examples/e2e-stack.yaml) into `langsmith_obs_config.yaml`, making sure to modify the values to match your LangSmith deployment.
3. Find the latest version of the chart by running `helm search repo langchain/langsmith-observability --versions`.
4. Grab the latest version number, and run `helm install langsmith-observability langchain/langsmith-observability --values langsmith_obs_config.yaml --version <version> -n <namespace> --wait --debug`

<Note>
  **You can selectively collect logs, metrics or traces by modifying the boolean values under `otelCollector` in your config file. You can also selectively bring up each respective piece of the backend (Loki, Mimir, Tempo).**
</Note>

You should see the following if the install went through:
```

Example 3 (unknown):
```unknown
And if you run `kubectl get pods -n langsmith-observability`, you should see:
```

Example 4 (unknown):
```unknown
## Post-Installation

### Enable Logs and Traces in LangSmith

Once you have installed the observability helm chart, you need to set the following values in your *LangSmith* helm configuration file to enable collection of logs and traces.
```

---

## This isn't for production use, but is useful for local

**URL:** llms-txt#this-isn't-for-production-use,-but-is-useful-for-local

store = LocalFileStore("./cache/") # [!code highlight]

cached_embedder = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings,
    store,
    namespace=underlying_embeddings.model
)

---

## This is our toy user database. Do not do this in production

**URL:** llms-txt#this-is-our-toy-user-database.-do-not-do-this-in-production

VALID_TOKENS = {
    "user1-token": {"id": "user1", "name": "Alice"},
    "user2-token": {"id": "user2", "name": "Bob"},
}

---

## thread_id is the persistent pointer (stores a stable ID in production)

**URL:** llms-txt#thread_id-is-the-persistent-pointer-(stores-a-stable-id-in-production)

config = {"configurable": {"thread_id": "thread-1"}}
result = graph.invoke({"input": "data"}, config=config)

---
