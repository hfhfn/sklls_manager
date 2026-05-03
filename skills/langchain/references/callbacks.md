# Langchain - Callbacks

**Pages:** 13

---

## Callbacks

**URL:** llms-txt#callbacks

Source: https://docs.langchain.com/oss/javascript/integrations/callbacks/index

<Columns cols={3}>
  <Card title="Datadog Tracer" icon="link" href="/oss/javascript/integrations/callbacks/datadog_tracer" arrow="true" cta="View guide" />

<Card title="Upstash Rate Limit" icon="link" href="/oss/javascript/integrations/callbacks/upstash_ratelimit_callback" arrow="true" cta="View guide" />
</Columns>

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/javascript/integrations/callbacks/index.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

---

## Configure LangSmith tracing

**URL:** llms-txt#configure-langsmith-tracing

configure(project_name="multi-framework-app")

---

## export LANGSMITH_TRACING="true"

**URL:** llms-txt#export-langsmith_tracing="true"

---

## Implement distributed tracing

**URL:** llms-txt#implement-distributed-tracing

**Contents:**
- Distributed tracing in Python

Source: https://docs.langchain.com/langsmith/distributed-tracing

Sometimes, you need to trace a request across multiple services.

LangSmith supports distributed tracing out of the box, linking runs within a trace across services using context propagation headers (`langsmith-trace` and optional `baggage` for metadata/tags).

Example client-server setup:

* Trace starts on client
* Continues on server

## Distributed tracing in Python

```python  theme={null}

---

## Import span processor to enable LangSmith tracing

**URL:** llms-txt#import-span-processor-to-enable-langsmith-tracing

**Contents:**
  - Step 4: Run your agent
- Advanced usage
  - Custom metadata and tags
  - Recording and attaching audio to traces

from langsmith_processor import span_processor
python  theme={null}
async def main():
    # Generate unique conversation ID for LangSmith
    conversation_id = str(uuid.uuid4())
    print(f"Starting conversation: {conversation_id}")

# Configure audio input/output with voice activity detection
    transport = LocalAudioTransport(
        LocalAudioTransportParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
            vad_analyzer=SileroVADAnalyzer(),
        )
    )

# Initialize AI services
    stt = WhisperSTTService()
    llm = OpenAILLMService(model="gpt-4o-mini")
    tts = OpenAITTSService(voice="alloy")

# Set up conversation context with system prompt
    context = OpenAILLMContext(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful voice assistant. Keep responses concise and conversational."
            }
        ]
    )
    context_aggregator = llm.create_context_aggregator(context)

# Build the processing pipeline
    pipeline = Pipeline([
        transport.input(),           # Capture microphone input
        stt,                         # Convert speech to text
        context_aggregator.user(),   # Add user message to context
        llm,                         # Generate AI response
        tts,                         # Convert response to speech
        transport.output(),          # Play through speakers
        context_aggregator.assistant(),  # Add assistant response to context
    ])

# Create task with tracing enabled
    task = PipelineTask(
        pipeline,
        params=PipelineParams(enable_metrics=True),
        enable_tracing=True,
        enable_turn_tracking=True,
        conversation_id=conversation_id,
    )

# Run the agent
    runner = PipelineRunner()
    await runner.run(task)
python  theme={null}
if __name__ == "__main__":
    asyncio.run(main())
bash  theme={null}
python agent.py
python  theme={null}
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

async def run_voice_session():
    with tracer.start_as_current_span("voice_conversation") as span:
        # Add custom metadata
        span.set_attribute("langsmith.metadata.session_type", "voice_assistant")
        span.set_attribute("langsmith.metadata.user_id", "user_123")
        span.set_attribute("langsmith.span.tags", "pipecat,voice-ai,stt-llm-tts")

# Your Pipecat pipeline code here
        task = PipelineTask(pipeline, enable_tracing=True)
        await task.queue_frames([TextFrame("Hello")])
python  theme={null}
from pathlib import Path
from datetime import datetime
from audio_recorder import AudioRecorder

**Examples:**

Example 1 (unknown):
```unknown
#### Part 2: Define the main function
```

Example 2 (unknown):
```unknown
#### Part 3: Add the entry point
```

Example 3 (unknown):
```unknown
### Step 4: Run your agent

Run your voice agent:
```

Example 4 (unknown):
```unknown
Speak to the agent through your microphone. All traces will automatically appear in LangSmith. Here is an example of a trace in LangSmith: [LangSmith trace with Pipecat](https://smith.langchain.com/public/07721f41-cd27-413e-bc79-90bd23b6807d/r).

View the complete [agent.py code](https://github.com/langchain-ai/voice-agents-tracing/blob/main/pipecat/agent.py).

## Advanced usage

### Custom metadata and tags

You can add custom metadata to your traces using span attributes:
```

---

## Oauth Callback

**URL:** llms-txt#oauth-callback

Source: https://docs.langchain.com/api-reference/auth-service-v2/oauth-callback

https://api.host.langchain.com/openapi.json post /v2/auth/callback/{provider_id}

---

## Optional: OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true

**URL:** llms-txt#optional:-otel_python_logging_auto_instrumentation_enabled=true

**Contents:**
- `DD_API_KEY`
- `LANGCHAIN_TRACING_SAMPLING_RATE`
- `LANGGRAPH_AUTH_TYPE`
- `LANGGRAPH_POSTGRES_POOL_MAX_SIZE`
- `LANGSMITH_API_KEY`
- `LANGSMITH_ENDPOINT`
- `LANGSMITH_TRACING`
- `LOG_COLOR`
- `LOG_LEVEL`
- `LOG_JSON`

shell  theme={null}
OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=https://otlp.nr-data.net/v1/traces
OTEL_EXPORTER_OTLP_ENDPOINT=https://otlp.nr-data.net
OTEL_EXPORTER_OTLP_HEADERS=api-key=<YOUR_INGEST_LICENSE_KEY>
```

<Note>
  OTel tracing was added in Agent Server version `0.5.32` and is currently in Alpha.
</Note>

Specify `DD_API_KEY` (your [Datadog API Key](https://docs.datadoghq.com/account_management/api-app-keys/)) to automatically enable Datadog tracing for the deployment. Specify other [`DD_*` environment variables](https://ddtrace.readthedocs.io/en/stable/configuration.html) to configure the tracing instrumentation.

If `DD_API_KEY` is specified, the application process is wrapped in the [`ddtrace-run` command](https://ddtrace.readthedocs.io/en/stable/installation_quickstart.html). Other `DD_*` environment variables (e.g. `DD_SITE`, `DD_ENV`, `DD_SERVICE`, `DD_TRACE_ENABLED`) are typically needed to properly configure the tracing instrumentation. See [`DD_*` environment variables](https://ddtrace.readthedocs.io/en/stable/configuration.html) for more details. You can enable `DD_TRACE_DEBUG=true` and set `DD_LOG_LEVEL=debug` to troubleshoot.

<Note>
  Enabling `DD_API_KEY` (and thus `ddtrace-run`) can override or interfere with other auto-instrumentation solutions (such as OpenTelemetry) that you may have instrumented into your application code.
</Note>

## `LANGCHAIN_TRACING_SAMPLING_RATE`

Sampling rate for traces sent to LangSmith. Valid values: Any float between `0` and `1`.

For more details, refer to [Set a sampling rate for traces](/langsmith/sample-traces).

## `LANGGRAPH_AUTH_TYPE`

Type of authentication for the Agent Server deployment. Valid values: `langsmith`, `noop`.

For deployments to LangSmith, this environment variable is set automatically. For local development or deployments where authentication is handled externally (e.g. self-hosted), set this environment variable to `noop`.

## `LANGGRAPH_POSTGRES_POOL_MAX_SIZE`

Beginning with langgraph-api version `0.2.12`, the maximum size of the Postgres connection pool (per replica) can be controlled using the `LANGGRAPH_POSTGRES_POOL_MAX_SIZE` environment variable. By setting this variable, you can determine the upper bound on the number of simultaneous connections the server will establish with the Postgres database.

For example, if a deployment is scaled up to 10 replicas and `LANGGRAPH_POSTGRES_POOL_MAX_SIZE` is configured to `150`, then up to `1500` connections to Postgres can be established. This is particularly useful for deployments where database resources are limited (or more available) or where you need to tune connection behavior for performance or scaling reasons.

Defaults to `150` connections.

## `LANGSMITH_API_KEY`

For deployments with [self-hosted LangSmith](/langsmith/self-hosted) only.

To send traces to a self-hosted LangSmith instance, set `LANGSMITH_API_KEY` to an API key created from the self-hosted instance.

## `LANGSMITH_ENDPOINT`

For deployments with [self-hosted LangSmith](/langsmith/self-hosted) only.

To send traces to a self-hosted LangSmith instance, set `LANGSMITH_ENDPOINT` to the hostname of the self-hosted instance.

## `LANGSMITH_TRACING`

Set `LANGSMITH_TRACING` to `false` to disable tracing to LangSmith.

This is mainly relevant in the context of using the dev server via the `langgraph dev` command. Set `LOG_COLOR` to `true` to enable ANSI-colored console output when using the default console renderer. Disabling color output by setting this variable to `false` produces monochrome logs. Defaults to `true`.

Configure [log level](https://docs.python.org/3/library/logging.html#logging-levels). Defaults to `INFO`.

Set `LOG_JSON` to `true` to render all log messages as JSON objects using the configured `JSONRenderer`. This produces structured logs that can be easily parsed or ingested by log management systems. Defaults to `false`.

<Info>
  **Only Allowed in Self-Hosted Deployments**
  The `MOUNT_PREFIX` environment variable is only allowed in Self-Hosted Deployment models, LangSmith SaaS will not allow this environment variable.
</Info>

Set `MOUNT_PREFIX` to serve the Agent Server under a specific path prefix. This is useful for deployments where the server is behind a reverse proxy or load balancer that requires a specific path prefix.

For example, if the server is to be served under `https://example.com/langgraph`, set `MOUNT_PREFIX` to `/langgraph`.

## `N_JOBS_PER_WORKER`

Number of jobs per worker for the Agent Server task queue. Defaults to `10`.

## `POSTGRES_URI_CUSTOM`

<Info>
  **Only for Hybrid and Self-Hosted**
  Custom Postgres instances are only available for [Hybrid](/langsmith/hybrid) and [Self-Hosted](/langsmith/self-hosted) deployments.
</Info>

Specify `POSTGRES_URI_CUSTOM` to use a custom Postgres instance. The value of `POSTGRES_URI_CUSTOM` must be a valid [Postgres connection URI](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING-URIS).

* Version 15.8 or higher.
* An initial database must be present and the connection URI must reference the database.

Control Plane Functionality:

* If `POSTGRES_URI_CUSTOM` is specified, the control plane will not provision a database for the server.
* If `POSTGRES_URI_CUSTOM` is removed, the control plane will not provision a database for the server and will not delete the externally managed Postgres instance.
* If `POSTGRES_URI_CUSTOM` is removed, deployment of the revision will not succeed. Once `POSTGRES_URI_CUSTOM` is specified, it must always be set for the lifecycle of the deployment.
* If the deployment is deleted, the control plane will not delete the externally managed Postgres instance.
* The value of `POSTGRES_URI_CUSTOM` can be updated. For example, a password in the URI can be updated.

Database Connectivity:

* The custom Postgres instance must be accessible by the Agent Server. The user is responsible for ensuring connectivity.

<Warning>
  This feature is in Alpha.
</Warning>

<Info>
  **Only Allowed in Self-Hosted Deployments**
  Redis Cluster mode is only available in Self-Hosted Deployment models, LangSmith SaaS will provision a redis instance for you by default.
</Info>

Set `REDIS_CLUSTER` to `True` to enable Redis Cluster mode. When enabled, the system will connect to Redis using cluster mode. This is useful when connecting to a Redis Cluster deployment.

## `REDIS_KEY_PREFIX`

<Info>
  **Available in API Server version 0.1.9+**
  This environment variable is supported in API Server version 0.1.9 and above.
</Info>

Specify a prefix for Redis keys. This allows multiple Agent Server instances to share the same Redis instance by using different key prefixes.

## `REDIS_URI_CUSTOM`

<Info>
  **Only for Hybrid and Self-Hosted**
  Custom Redis instances are only available for [Hybrid](/langsmith/hybrid) and [Self-Hosted](/langsmith/self-hosted) deployments.
</Info>

Specify `REDIS_URI_CUSTOM` to use a custom Redis instance. The value of `REDIS_URI_CUSTOM` must be a valid [Redis connection URI](https://redis-py.readthedocs.io/en/stable/connections.html#redis.Redis.from_url).

## `REDIS_MAX_CONNECTIONS`

The maximum size of the Redis connection pool (per replica) can be controlled using the `REDIS_MAX_CONNECTIONS` environment variable. By setting this variable, you can determine the upper bound on the number of simultaneous connections the server will establish with the Redis instance.

For example, if a deployment is scaled up to 10 replicas and `REDIS_MAX_CONNECTIONS` is configured to `150`, then up to `1500` connections to Redis can be established.

## `RESUMABLE_STREAM_TTL_SECONDS`

Time-to-live in seconds for resumable stream data in Redis.

When a run is created and the output is streamed, the stream can be configured to be resumable (e.g. `stream_resumable=True`). If a stream is resumable, output from the stream is temporarily stored in Redis. The TTL for this data can be configured by setting `RESUMABLE_STREAM_TTL_SECONDS`.

See the [Python](https://reference.langchain.com/python/langsmith/deployment/sdk/#langgraph_sdk.client.RunsClient.stream) and [JS/TS](https://langchain-ai.github.io/langgraphjs/reference/classes/sdk_client.RunsClient.html#stream) SDKs for more details on how to implement resumable streams.

Defaults to `120` seconds.

<Note>
  Setting a very high value for `RESUMABLE_STREAM_TTL_SECONDS` can result in substantial Redis memory usage when there are many concurrent runs with large or frequent streaming output. Set this value to the minimum value to enable recovery during network interruptions and prefer checkpointing for long term durability and execution snapshotting.
</Note>

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/env-var.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

**Examples:**

Example 1 (unknown):
```unknown
For example, to submit OpenTelemetry traces to [New Relic's US region](https://docs.newrelic.com/docs/opentelemetry/best-practices/opentelemetry-otlp/), set the following:
```

---

## Prevent logging of sensitive data in traces

**URL:** llms-txt#prevent-logging-of-sensitive-data-in-traces

**Contents:**
- Rule-based masking of inputs and outputs
- Processing Inputs & Outputs for a Single Function
- Quick starts
  - Regex

Source: https://docs.langchain.com/langsmith/mask-inputs-outputs

In some situations, you may need to prevent the inputs and outputs of your traces from being logged for privacy or security reasons. LangSmith provides a way to filter the inputs and outputs of your traces before they are sent to the LangSmith backend.

If you want to completely hide the inputs and outputs of your traces, you can set the following environment variables when running your application:

This works for both the LangSmith SDK (Python and TypeScript) and LangChain.

You can also customize and override this behavior for a given `Client` instance. This can be done by setting the `hide_inputs` and `hide_outputs` parameters on the `Client` object (`hideInputs` and `hideOutputs` in TypeScript).

For the example below, we will simply return an empty object for both `hide_inputs` and `hide_outputs`, but you can customize this to your needs.

## Rule-based masking of inputs and outputs

<Info>
  This feature is available in the following LangSmith SDK versions:

* Python: 0.1.81 and above
  * TypeScript: 0.1.33 and above
</Info>

To mask specific data in inputs and outputs, you can use the `create_anonymizer` / `createAnonymizer` function and pass the newly created anonymizer when instantiating the client. The anonymizer can be either constructed from a list of regex patterns and the replacement values or from a function that accepts and returns a string value.

The anonymizer will be skipped for inputs if `LANGSMITH_HIDE_INPUTS = true`. Same applies for outputs if `LANGSMITH_HIDE_OUTPUTS = true`.

However, if inputs or outputs are to be sent to client, the `anonymizer` method will take precedence over functions found in `hide_inputs` and `hide_outputs`. By default, the `create_anonymizer` will only look at maximum of 10 nesting levels deep, which can be configured via the `max_depth` parameter.

Please note, that using the anonymizer might incur a performance hit with complex regular expressions or large payloads, as the anonymizer serializes the payload to JSON before processing.

<Note>
  Improving the performance of `anonymizer` API is on our roadmap! If you are encountering performance issues, please contact support via [support.langchain.com](https://support.langchain.com).
</Note>

<img src="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/hide-inputs-outputs.png?fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=ac9ba9a6729029a7fa38da03e1466a1a" alt="Hide inputs outputs" data-og-width="1708" width="1708" data-og-height="717" height="717" data-path="langsmith/images/hide-inputs-outputs.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/hide-inputs-outputs.png?w=280&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=7ded12c0345f47d55e9802083c5032d0 280w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/hide-inputs-outputs.png?w=560&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=8cbe74d09660d8c65e8a75dd78cdb24e 560w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/hide-inputs-outputs.png?w=840&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=8cb8c0b5c926e46522b9539b0262ee7a 840w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/hide-inputs-outputs.png?w=1100&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=9b8ef244796fad943ec76b0aa5733f80 1100w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/hide-inputs-outputs.png?w=1650&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=87f35d63f42f05c49a220d5b8a87787a 1650w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/hide-inputs-outputs.png?w=2500&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=5173e30032c065646c13e9b9c6a95fb5 2500w" />

Older versions of LangSmith SDKs can use the `hide_inputs` and `hide_outputs` parameters to achieve the same effect. You can also use these parameters to process the inputs and outputs more efficiently as well.

## Processing Inputs & Outputs for a Single Function

<Info>
  The `process_outputs` parameter is available in LangSmith SDK version 0.1.98 and above for Python.
</Info>

In addition to client-level input and output processing, LangSmith provides function-level processing through the `process_inputs` and `process_outputs` parameters of the `@traceable` decorator.

These parameters accept functions that allow you to transform the inputs and outputs of a specific function before they are logged to LangSmith. This is useful for reducing payload size, removing sensitive information, or customizing how an object should be serialized and represented in LangSmith for a particular function.

Here's an example of how to use `process_inputs` and `process_outputs`:

In this example, `process_inputs` creates a new dictionary with processed input data, and `process_outputs` transforms the output into a specific format before logging to LangSmith.

<Warning>
  It's recommended to avoid mutating the source objects in the processor functions. Instead, create and return new objects with the processed data.
</Warning>

For asynchronous functions, the usage is similar:

These function-level processors take precedence over client-level processors (`hide_inputs` and `hide_outputs`) when both are defined.

You can combine rule-based masking with various anonymizers to scrub sensitive information from inputs and outputs. In this how-to-guide, we'll cover working with regex, Microsoft Presidio, and Amazon Comprehend.

<Info>
  The implementation below is not exhaustive and may miss some formats or edge cases. Test any implementation thoroughly before using it in production.
</Info>

You can use regex to mask inputs and outputs before they are sent to LangSmith. The implementation below masks email addresses, phone numbers, full names, credit card numbers, and SSNs.

```python  theme={null}
import re
import openai
from langsmith import Client
from langsmith.wrappers import wrap_openai

**Examples:**

Example 1 (unknown):
```unknown
This works for both the LangSmith SDK (Python and TypeScript) and LangChain.

You can also customize and override this behavior for a given `Client` instance. This can be done by setting the `hide_inputs` and `hide_outputs` parameters on the `Client` object (`hideInputs` and `hideOutputs` in TypeScript).

For the example below, we will simply return an empty object for both `hide_inputs` and `hide_outputs`, but you can customize this to your needs.

<CodeGroup>
```

Example 2 (unknown):
```unknown

```

Example 3 (unknown):
```unknown
</CodeGroup>

## Rule-based masking of inputs and outputs

<Info>
  This feature is available in the following LangSmith SDK versions:

  * Python: 0.1.81 and above
  * TypeScript: 0.1.33 and above
</Info>

To mask specific data in inputs and outputs, you can use the `create_anonymizer` / `createAnonymizer` function and pass the newly created anonymizer when instantiating the client. The anonymizer can be either constructed from a list of regex patterns and the replacement values or from a function that accepts and returns a string value.

The anonymizer will be skipped for inputs if `LANGSMITH_HIDE_INPUTS = true`. Same applies for outputs if `LANGSMITH_HIDE_OUTPUTS = true`.

However, if inputs or outputs are to be sent to client, the `anonymizer` method will take precedence over functions found in `hide_inputs` and `hide_outputs`. By default, the `create_anonymizer` will only look at maximum of 10 nesting levels deep, which can be configured via the `max_depth` parameter.

<CodeGroup>
```

Example 4 (unknown):
```unknown

```

---

## Separate loop to avoid logging at the same time as logs from evaluate()

**URL:** llms-txt#separate-loop-to-avoid-logging-at-the-same-time-as-logs-from-evaluate()

**Contents:**
- Understand the result structure
- Examples
  - Implement a quality gate

for result in aggregated_results:
    print("Input:", result["run"].inputs)
    print("Output:", result["run"].outputs)
    print("Evaluation Results:", result["evaluation_results"]["results"])
    print("--------------------------------")

Input: {'input': 'MY INPUT'}
Output: {'output': 'MY OUTPUT'}
Evaluation Results: [EvaluationResult(key='randomness', score=1, value=None, comment=None, correction=None, evaluator_info={}, feedback_config=None, source_run_id=UUID('7ebb4900-91c0-40b0-bb10-f2f6a451fd3c'), target_run_id=None, extra=None)]
--------------------------------
python  theme={null}
from langsmith import Client
import sys

def my_application(inputs):
    # Your application logic
    return {"response": "..."}

def accuracy_evaluator(run, example):
    # Your evaluation logic
    is_correct = run.outputs["response"] == example.outputs["expected"]
    return {"key": "accuracy", "score": 1 if is_correct else 0}

**Examples:**

Example 1 (unknown):
```unknown
This produces output like:
```

Example 2 (unknown):
```unknown
## Understand the result structure

Each result in the iterator contains:

* `result["run"]`: The execution of your target function.
  * `result["run"].inputs`: The inputs from your [dataset](/langsmith/evaluation-concepts#datasets) example.
  * `result["run"].outputs`: The outputs produced by your target function.
  * `result["run"].id`: The unique ID for this run.

* `result["evaluation_results"]["results"]`: A list of `EvaluationResult` objects, one per evaluator.
  * `key`: The metric name (from your evaluator's return value).
  * `score`: The numeric score (typically 0-1 or boolean).
  * `comment`: Optional explanatory text.
  * `source_run_id`: The ID of the evaluator run.

* `result["example"]`: The dataset example that was evaluated.
  * `result["example"].inputs`: The input values.
  * `result["example"].outputs`: The reference outputs (if any).

## Examples

### Implement a quality gate

This example uses evaluation results to pass or fail a CI/CD build automatically based on quality thresholds. The script iterates through results, calculates an average accuracy score, and exits with a non-zero status code if the accuracy falls below 85%. This ensures that you can deploy code changes that meet quality standards.
```

---

## Set up LangSmith tracing

**URL:** llms-txt#set-up-langsmith-tracing

def setup_langsmith():
    """Setup OpenTelemetry tracing to export spans to LangSmith."""
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    headers = os.getenv("OTEL_EXPORTER_OTLP_HEADERS")

if not endpoint or not headers:
        print("⚠️  Warning: OTEL environment variables not set. Tracing disabled.")
        return

# Create tracer provider with custom span processor
    trace_provider = TracerProvider()
    trace_provider.add_span_processor(LangSmithSpanProcessor())

# Set as LiveKit's tracer provider
    set_tracer_provider(trace_provider)
    print("✅ LangSmith tracing enabled")

---

## This will NOT be traced (if LANGSMITH_TRACING is not set)

**URL:** llms-txt#this-will-not-be-traced-(if-langsmith_tracing-is-not-set)

**Contents:**
- Log to a project
- Add metadata to traces
- Use anonymizers to prevent logging of sensitive data in traces

agent.invoke({"messages": [{"role": "user", "content": "Send another email"}]})
bash  theme={null}
  export LANGSMITH_PROJECT=my-agent-project
  python  theme={null}
  import langsmith as ls

with ls.tracing_context(project_name="email-agent-test", enabled=True):
      response = agent.invoke({
          "messages": [{"role": "user", "content": "Send a welcome email"}]
      })
  python  theme={null}
response = agent.invoke(
    {"messages": [{"role": "user", "content": "Send a welcome email"}]},
    config={
        "tags": ["production", "email-assistant", "v1.0"],
        "metadata": {
            "user_id": "user_123",
            "session_id": "session_456",
            "environment": "production"
        }
    }
)
python  theme={null}
with ls.tracing_context(
    project_name="email-agent-test",
    enabled=True,
    tags=["production", "email-assistant", "v1.0"],
    metadata={"user_id": "user_123", "session_id": "session_456", "environment": "production"}):
    response = agent.invoke(
        {"messages": [{"role": "user", "content": "Send a welcome email"}]}
    )
python Python theme={null}
from langchain_core.tracers.langchain import LangChainTracer
from langgraph.graph import StateGraph, MessagesState
from langsmith import Client
from langsmith.anonymizer import create_anonymizer

anonymizer = create_anonymizer([
    # Matches SSNs
    { "pattern": r"\b\d{3}-?\d{2}-?\d{4}\b", "replace": "<ssn>" }
])

tracer_client = Client(anonymizer=anonymizer)
tracer = LangChainTracer(client=tracer_client)

**Examples:**

Example 1 (unknown):
```unknown
## Log to a project

<Accordion title="Statically">
  You can set a custom project name for your entire application by setting the `LANGSMITH_PROJECT` environment variable:
```

Example 2 (unknown):
```unknown
</Accordion>

<Accordion title="Dynamically">
  You can set the project name programmatically for specific operations:
```

Example 3 (unknown):
```unknown
</Accordion>

## Add metadata to traces

You can annotate your traces with custom metadata and tags:
```

Example 4 (unknown):
```unknown
`tracing_context` also accepts tags and metadata for fine-grained control:
```

---

## Trace JS functions in serverless environments

**URL:** llms-txt#trace-js-functions-in-serverless-environments

**Contents:**
- Rate limits at high concurrency[](#rate-limits-at-high-concurrency "Direct link to Rate limits at high concurrency")

Source: https://docs.langchain.com/langsmith/serverless-environments

<Note>
  This section is relevant for those using the LangSmith JS SDK version 0.2.0 and higher. If you are tracing using LangChain.js or LangGraph.js in serverless environments, see [this guide](https://js.langchain.com/docs/how_to/callbacks_serverless).
</Note>

When tracing JavaScript functions, LangSmith will trace runs in the background by default to avoid adding latency. In serverless environments where the execution context may be terminated abruptly, it's important to ensure that all tracing data is properly flushed before the function completes.

To make sure this occurs, you can either:

* Set an environment variable named `LANGSMITH_TRACING_BACKGROUND` to `"false"`. This will cause your traced functions to wait for tracing to complete before returning.
  * Note that this is named differently from the [environment variable](https://js.langchain.com/docs/how_to/callbacks_serverless) in LangChain.js because LangSmith can be used without LangChain.
* Pass a custom client into your traced runs and `await` the `client.awaitPendingTraceBatches();` method.

Here's an example of using `awaitPendingTraceBatches` alongside the [`traceable`](/langsmith/annotate-code) method:

## Rate limits at high concurrency[](#rate-limits-at-high-concurrency "Direct link to Rate limits at high concurrency")

By default, the LangSmith client will batch operations as your traced run executions, sending a new batch every few milliseconds.

This works well in most situations, but if your traced function is long-running and you have very high concurrency, you may also hit rate limits related to overall request count.

If you are seeing rate limit errors related to this, you can try setting `manualFlushMode: true` in your client like this:

And then manually calling `client.flush()` like this before your serverless function closes:

Note that this will prevent runs from appearing in the LangSmith UI until you call `.flush()`.

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/serverless-environments.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

**Examples:**

Example 1 (unknown):
```unknown
## Rate limits at high concurrency[](#rate-limits-at-high-concurrency "Direct link to Rate limits at high concurrency")

By default, the LangSmith client will batch operations as your traced run executions, sending a new batch every few milliseconds.

This works well in most situations, but if your traced function is long-running and you have very high concurrency, you may also hit rate limits related to overall request count.

If you are seeing rate limit errors related to this, you can try setting `manualFlushMode: true` in your client like this:
```

Example 2 (unknown):
```unknown
And then manually calling `client.flush()` like this before your serverless function closes:
```

---

## Turn off LangSmith default tracing, as we want to only trace with OpenTelemetry

**URL:** llms-txt#turn-off-langsmith-default-tracing,-as-we-want-to-only-trace-with-opentelemetry

**Contents:**
- 4. Prepare for deployment

LANGSMITH_TRACING=false

OTEL_EXPORTER_OTLP_ENDPOINT = "https://api.smith.langchain.com/otel/"

OTEL_EXPORTER_OTLP_HEADERS = "x-api-key=your-langsmith-api-key,Langsmith-Project=your-tracing-project-name"
python  theme={null}
from strands.telemetry import StrandsTelemetry

strands_telemetry = StrandsTelemetry()
strands_telemetry.setup_otlp_exporter()
strands_telemetry.setup_meter()

my-strands-agent/
├── agent.py          # Your main agent code
├── requirements.txt  # Python dependencies
└── langgraph.json   # LangGraph configuration
```

To deploy your agent, follow the [Deploy to cloud](/langsmith/deploy-to-cloud) guide.

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/deploy-other-frameworks.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

**Examples:**

Example 1 (unknown):
```unknown
<Note>
  If you're [self-hosting LangSmith](/langsmith/self-hosted), replace the  `OTEL_EXPORTER_OTLP_ENDPOINT` endpoint with your LangSmith API endpoint and append `/api/v1/otel`. For example: `OTEL_EXPORTER_OTLP_ENDPOINT = "https://ai-company.com/api/v1/otel"`
</Note>

<Note>
  Strand's OTel tracing contains synchronous code. In this case, you may need to set `BG_JOB_ISOLATED_LOOPS=true` to execute background runs in an isolated event loop separate from the serving API event loop.
</Note>

In your main agent, set up the following:
```

Example 2 (unknown):
```unknown
## 4. Prepare for deployment

From here, to deploy to LangSmith, create a file structure like the following:
```

---
