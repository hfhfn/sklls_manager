# Crewai - Examples

**Pages:** 12

---

## Example: Initialize with specific parameters

**URL:** llms-txt#example:-initialize-with-specific-parameters

custom_tavily_tool = TavilySearchTool(
    search_depth='advanced',
    max_results=10,
    include_answer=True
)

---

## Example of guardrail result structure

**URL:** llms-txt#example-of-guardrail-result-structure

**Contents:**
  - Result Properties
- Integration with Task System
  - Automatic Validation

{
    "valid": False,
    "feedback": "Content appears to be hallucinated (score: 4.2/10, verdict: HALLUCINATED). The output contains information not supported by the provided context."
}
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### Result Properties

* **valid**: Boolean indicating whether the output passed validation
* **feedback**: Detailed explanation when validation fails, including:
  * Faithfulness score
  * Verdict classification
  * Specific reasons for failure

## Integration with Task System

### Automatic Validation

When a guardrail is added to a task, it automatically validates the output before the task is marked as complete:
```

---

## Example of limiting the search to the content of a specific website,

**URL:** llms-txt#example-of-limiting-the-search-to-the-content-of-a-specific-website,

---

## Example of using kickoff_for_each

**URL:** llms-txt#example-of-using-kickoff_for_each

inputs_array = [{'topic': 'AI in healthcare'}, {'topic': 'AI in finance'}]
results = my_crew.kickoff_for_each(inputs=inputs_array)
for result in results:
    print(result)

---

## Example of using native async with akickoff

**URL:** llms-txt#example-of-using-native-async-with-akickoff

inputs = {'topic': 'AI in healthcare'}
async_result = await my_crew.akickoff(inputs=inputs)
print(async_result)

---

## Example of using native async with akickoff_for_each

**URL:** llms-txt#example-of-using-native-async-with-akickoff_for_each

inputs_array = [{'topic': 'AI in healthcare'}, {'topic': 'AI in finance'}]
async_results = await my_crew.akickoff_for_each(inputs=inputs_array)
for async_result in async_results:
    print(async_result)

---

## Example of using thread-based kickoff_async

**URL:** llms-txt#example-of-using-thread-based-kickoff_async

inputs = {'topic': 'AI in healthcare'}
async_result = await my_crew.kickoff_async(inputs=inputs)
print(async_result)

---

## Example of using thread-based kickoff_for_each_async

**URL:** llms-txt#example-of-using-thread-based-kickoff_for_each_async

**Contents:**
  - Streaming Crew Execution

inputs_array = [{'topic': 'AI in healthcare'}, {'topic': 'AI in finance'}]
async_results = await my_crew.kickoff_for_each_async(inputs=inputs_array)
for async_result in async_results:
    print(async_result)
python Code theme={null}

**Examples:**

Example 1 (unknown):
```unknown
These methods provide flexibility in how you manage and execute tasks within your crew, allowing for both synchronous and asynchronous workflows tailored to your needs. For detailed async examples, see the [Kickoff Crew Asynchronously](/en/learn/kickoff-async) guide.

### Streaming Crew Execution

For real-time visibility into crew execution, you can enable streaming to receive output as it's generated:
```

---

## Example: search with category filter

**URL:** llms-txt#example:-search-with-category-filter

---

## Example server_params (choose one based on your server type):

**URL:** llms-txt#example-server_params-(choose-one-based-on-your-server-type):

---

## Example with multiple URLs and advanced extraction

**URL:** llms-txt#example-with-multiple-urls-and-advanced-extraction

multi_extract_task = Task(
    description='Extract content from https://example.com and https://anotherexample.org using advanced extraction.',
    expected_output='A JSON string containing the extracted content from both URLs.',
    agent=extractor_agent
)

---

## Usage example

**URL:** llms-txt#usage-example

async def run_flow():
    flow = MarketResearchFlow()
    flow.plot("MarketResearchFlowPlot")
    result = await flow.kickoff_async(inputs={"product": "AI-powered chatbots"})
    return result

---
