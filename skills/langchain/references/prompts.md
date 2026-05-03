# Langchain - Prompts

**Pages:** 24

---

## Add the function to the kernel

**URL:** llms-txt#add-the-function-to-the-kernel

code_analyzer = kernel.add_function(
    function_name="analyzeCode",
    plugin_name="codeAnalysisPlugin",
    prompt_template_config=prompt_template_config,
)

---

## Configure prompt settings

**URL:** llms-txt#configure-prompt-settings

**Contents:**
- Model configurations
  - Create saved configurations
  - Edit configurations
  - Delete configurations
  - Extra parameters
- Tool settings
- Prompt formatting

Source: https://docs.langchain.com/langsmith/managing-model-configurations

The LangSmith [playground](/langsmith/prompt-engineering-concepts#prompt-playground) enables you to control various settings for your prompts. The **Prompt Settings** window contains:

* [Model configuration](#model-configurations)
* [Tool settings](#tool-settings)
* [Prompt formatting](#prompt-formatting)

To access **Prompt Settings**:

1. Navigate to the **Playground** in the left sidebar.
2. Under the **Prompts** heading select the gear <Icon icon="gear" iconType="solid" /> icon next to the model name, which will launch the **Prompt Settings** window.

<div style={{ textAlign: 'center' }}>
     <img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=6c0f7d7012b1e5295fe545149f955e6b" alt="Model Configuration window in the LangSmith UI, settings for Provider, Model, Temperature, Max Output Tokens, Top P, Presence Penalty, Frequency Penalty, Reasoning Effort, etc." data-og-width="886" width="886" data-og-height="689" height="689" data-path="langsmith/images/model-config-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?w=280&fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=4e3b9ad92f6f14f4e0523bef50199318 280w, https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?w=560&fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=e538eb740495a8afa8bfc552b13ae294 560w, https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?w=840&fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=ebe73264e977153c869fd04d1552d09b 840w, https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?w=1100&fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=2eeb01882056046bc73cc019d674af7e 1100w, https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?w=1650&fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=8f28fe2fe8054cf0623fb9d17f91966f 1650w, https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?w=2500&fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=cf9ad39be3623e73322d123699e73f19 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=2e9da272c3fc8f7ac958c6e6d1da85e3" alt="Model Configuration window in the LangSmith UI, settings for Provider, Model, Temperature, Max Output Tokens, Top P, Presence Penalty, Frequency Penalty, Reasoning Effort, etc." data-og-width="881" width="881" data-og-height="732" height="732" data-path="langsmith/images/model-config-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?w=280&fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=652fb75a4682cfc813743a1260764e59 280w, https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?w=560&fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=02c980a8387f3d69a5870660b1668080 560w, https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?w=840&fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=ee633c06056fa7ad46ea58a179afa169 840w, https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?w=1100&fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=f62a35ed726b5f89c156a40c9ea76f2c 1100w, https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?w=1650&fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=18114575db8e6c7ce928763ddcb88c12 1650w, https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?w=2500&fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=ab24dc4975def52db55c4896ead5b77c 2500w" />
   </div>

## Model configurations

Model configurations define the parameters your prompt runs against. In the LangSmith Playground, you can save and manage these configurations, which allows you to reuse your preferred settings across prompts and sessions. For details on specific settings, refer to your model provider’s documentation (for example, [Anthropic](https://platform.claude.com/docs/en/api/messages), [OpenAI](https://platform.openai.com/docs/api-reference/responses/create)).

### Create saved configurations

1. In the **Model Configurations** tab, adjust the model configuration as needed—you can select a [saved configuration to edit](#edit-configurations).
2. Click the **Save As** button in the top bar.
3. Enter a name and optional description for your configuration and confirm.
4. Now that you've saved the configuration, anyone in your organization's [workspace](/langsmith/administration-overview#workspaces) can access it. All saved configurations are available in the **Model Configuration** dropdown.
5. Once you have created a saved configuration, you can set it as your default, so any new prompt you create will automatically use this configuration. To set a configuration as your default, click the **Set as default** <Icon icon="thumbtack" iconType="solid" /> icon next to the model name in the dropdown.

### Edit configurations

1. To rename a saved configuration, or update the description, select the configuration name or description and make the necessary changes.
2. Update the current configuration's parameters as needed and click the **Save** button at the top.

### Delete configurations

1. Select the configuration you want to remove.
2. Click the trash <Icon icon="trash" iconType="solid" /> icon to delete it.

The **Extra Parameters** field allows you to pass additional model parameters that aren't directly supported in the LangSmith interface. This is particularly useful in two scenarios:

1. When model providers release new parameters that haven't yet been integrated into the LangSmith interface. You can specify these parameters in JSON format to use them right away. For example:

2. When troubleshooting parameter-related errors in the playground, such as:

If you receive an error about unnecessary parameters (which is more common when using [LangChain JS](/oss/python/langchain/overview) for run tracing), you can use this field to remove the extra parameters.

[*Tools*](/langsmith/prompt-engineering-concepts#tools) enable your LLM to perform tasks like searching the web, looking up information, and so on. In the **Tools Settings** tab, you can manage the ways your LLM uses and accesses the tools you have defined in your prompt, including:

* **Parallel Tool Calls**: Calling multiple tools in parallel when appropriate. This allows the model to gather information from different sources simultaneously. (Dependent on model support for parallel execution.)
* **Tool Choice**: Select the tools that the model can access. For more details, refer to [Use tools in a prompt](/langsmith/use-tools).

The **Prompt Format** tab allows you to specify:

* The **Prompt type**. For details on chat and completion prompts, refer to [Prompt engineering](/langsmith/prompt-engineering-concepts#chat-vs-completion) concepts.
* The **Template format**. For details on prompt templating and using variables, refer to [F-string vs. mustache](/langsmith/prompt-engineering-concepts##f-string-vs-mustache).

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/managing-model-configurations.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

**Examples:**

Example 1 (unknown):
```unknown
2. When troubleshooting parameter-related errors in the playground, such as:
```

---

## Create a code analysis prompt template

**URL:** llms-txt#create-a-code-analysis-prompt-template

code_analysis_prompt = """
Analyze the following code and provide insights:

Please provide:
1. A brief summary of what the code does
2. Any potential improvements
3. Code quality assessment
"""

prompt_template_config = PromptTemplateConfig(
    template=code_analysis_prompt,
    name="code_analyzer",
    template_format="semantic-kernel",
    input_variables=[
        InputVariable(name="code", description="The code to analyze", is_required=True),
    ],
)

---

## Create a documentation generator

**URL:** llms-txt#create-a-documentation-generator

**Contents:**
- Advanced usage
  - Custom metadata and tags

doc_prompt = """
Generate comprehensive documentation for the following function:

Include:
- Purpose and functionality
- Parameters and return values
- Usage examples
- Any important notes
"""

doc_template_config = PromptTemplateConfig(
    template=doc_prompt,
    name="doc_generator",
    template_format="semantic-kernel",
    input_variables=[
        InputVariable(name="function_code", description="The function code to document", is_required=True),
    ],
)

doc_generator = kernel.add_function(
    function_name="generateDocs",
    plugin_name="documentationPlugin",
    prompt_template_config=doc_template_config,
)

async def main():
    # Example code to analyze
    sample_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
    """

# Analyze the code
    analysis_result = await kernel.invoke(code_analyzer, code=sample_code)
    print("Code Analysis:")
    print(analysis_result)
    print("\n" + "="*50 + "\n")

# Generate documentation
    doc_result = await kernel.invoke(doc_generator, function_code=sample_code)
    print("Generated Documentation:")
    print(doc_result)

return {"analysis": str(analysis_result), "documentation": str(doc_result)}

if __name__ == "__main__":
    asyncio.run(main())
python  theme={null}
from opentelemetry import trace

**Examples:**

Example 1 (unknown):
```unknown
## Advanced usage

### Custom metadata and tags

You can add custom metadata to your traces by setting span attributes:
```

---

## Create a function that will take in a list of examples and format them into a string

**URL:** llms-txt#create-a-function-that-will-take-in-a-list-of-examples-and-format-them-into-a-string

**Contents:**
  - NEW CODE ###
- Semantic search over examples

def create_example_string(examples):
    final_strings = []
    for e in examples:
        final_strings.append(f"Input: {e.inputs['topic']}\n> {e.outputs['output']}")
    return "\n\n".join(final_strings)
### NEW CODE ###

client = openai.Client()

available_topics = [
    "bug",
    "improvement",
    "new_feature",
    "documentation",
    "integration",
]

prompt_template = """Classify the type of the issue as one of {topics}.

Here are some examples:
{examples}

Begin!
Issue: {text}
>"""

@traceable(
    run_type="chain",
    name="Classifier",
)
def topic_classifier(
    topic: str):
    # We can now pull down the examples from the dataset
    # We do this inside the function so it always get the most up-to-date examples,
    # But this can be done outside and cached for speed if desired
    examples = list(ls_client.list_examples(dataset_name="classifier-github-issues"))  # <- New Code
    example_string = create_example_string(examples)
    return client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt_template.format(
                    topics=','.join(available_topics),
                    text=topic,
                    examples=example_string,
                )
            }
        ],
    ).choices[0].message.content
python  theme={null}
ls_client = Client()
run_id = uuid7()
topic_classifier(
    "address bug in documentation",
    langsmith_extra={"run_id": run_id})
python  theme={null}
import numpy as np

def find_similar(examples, topic, k=5):
    inputs = [e.inputs['topic'] for e in examples] + [topic]
    vectors = client.embeddings.create(input=inputs, model="text-embedding-3-small")
    vectors = [e.embedding for e in vectors.data]
    vectors = np.array(vectors)
    args = np.argsort(-vectors.dot(vectors[-1])[:-1])[:5]
    examples = [examples[i] for i in args]
    return examples
python  theme={null}
ls_client = Client()

def create_example_string(examples):
    final_strings = []
    for e in examples:
        final_strings.append(f"Input: {e.inputs['topic']}\n> {e.outputs['output']}")
    return "\n\n".join(final_strings)

client = openai.Client()

available_topics = [
    "bug",
    "improvement",
    "new_feature",
    "documentation",
    "integration",
]

prompt_template = """Classify the type of the issue as one of {topics}.

Here are some examples:
{examples}

Begin!
Issue: {text}
>"""

@traceable(
    run_type="chain",
    name="Classifier",
)
def topic_classifier(
    topic: str):
    examples = list(ls_client.list_examples(dataset_name="classifier-github-issues"))
    examples = find_similar(examples, topic)
    example_string = create_example_string(examples)
    return client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt_template.format(
                    topics=','.join(available_topics),
                    text=topic,
                    examples=example_string,
                )
            }
        ],
    ).choices[0].message.content
```

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/optimize-classifier.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

**Examples:**

Example 1 (unknown):
```unknown
If now run the application with a similar input as before, we can see that it correctly learns that anything related to docs (even if a bug) should be classified as `documentation`
```

Example 2 (unknown):
```unknown
## Semantic search over examples

One additional thing we can do is only use the most semantically similar examples. This is useful when you start to build up a lot of examples.

In order to do this, we can first define an example to find the `k` most similar examples:
```

Example 3 (unknown):
```unknown
We can then use that in the application
```

---

## Create a prompt

**URL:** llms-txt#create-a-prompt

**Contents:**
- Compose your prompt
  - Template format
  - Add a template variable
  - Structured output
  - Tools
- Run the prompt
- Save your prompt
- View your prompts
- Add metadata

Source: https://docs.langchain.com/langsmith/create-a-prompt

Navigate to the  in the left-hand sidebar or from the application homepage.

<img src="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/empty-playground.png?fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=2bede4ae9332bdf43ae20580d5bb957d" alt="Empty playground" data-og-width="1747" width="1747" data-og-height="1285" height="1285" data-path="langsmith/images/empty-playground.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/empty-playground.png?w=280&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=20602d3b2e7b4219a8dc3612fee194b7 280w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/empty-playground.png?w=560&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=141b0ab234c54970f4e86f24ed13a954 560w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/empty-playground.png?w=840&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=1fa1d0cb9075f4fbdcae487ea4348116 840w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/empty-playground.png?w=1100&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=bb3583d9357a597754396ee94e52c0da 1100w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/empty-playground.png?w=1650&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=c21b3e9881e95a0b954d578fa1d8aa47 1650w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/empty-playground.png?w=2500&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=3dcdde6a3fd4f3365059e181f53f68a0 2500w" />

## Compose your prompt

On the left is an editable view of the prompt.

The prompt is made up of messages, each of which has a "role" - including `system`, `human`, and `ai`.

The default template format is `f-string`, but you can change the prompt template format to `mustache` by clicking on the settings icon next to the model -> prompt format -> template format. Learn more about template formats [here](/langsmith/prompt-engineering-concepts#f-string-vs-mustache).
<img src="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/template-format.png?fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=417fa567135babb46d2bf080b7eb44f0" alt="Template format" data-og-width="938" width="938" data-og-height="352" height="352" data-path="langsmith/images/template-format.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/template-format.png?w=280&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=5bbcf83ad9e251ea9fdeb6c0f7dd49eb 280w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/template-format.png?w=560&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=02776bb45c6ffe0df98775886e75eaeb 560w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/template-format.png?w=840&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=c63b67b6afe893f7944ee2fb8b76bbaf 840w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/template-format.png?w=1100&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=9df27878d7eaf60e953b9438fcf3f8c4 1100w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/template-format.png?w=1650&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=a8b2e1b3fd0977e5b6beb984119bc6fd 1650w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/template-format.png?w=2500&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=d30b1d76394200f9473f0b8fb08d2a5e 2500w" />

### Add a template variable

The power of prompts comes from the ability to use variables in your prompt. You can use variables to add dynamic content to your prompt. Add a template variable in one of two ways:

1. Add `{{variable_name}}` to your prompt (with one curly brace on each side for `f-string` and two for `mustache`). <img src="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-with-variable.png?fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=b250a57ef0e0a40a56822af750d52810" alt="Prompt with variable" data-og-width="726" width="726" data-og-height="169" height="169" data-path="langsmith/images/prompt-with-variable.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-with-variable.png?w=280&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=ea82252d99c7ee63c15d1c1036db8c55 280w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-with-variable.png?w=560&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=fc56d047cf631b1e66ecfd09ab4c03a5 560w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-with-variable.png?w=840&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=7cc8cb861e9361445dcee545cbac84b7 840w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-with-variable.png?w=1100&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=a7ed018754ebb8dad675a75c4aa638cb 1100w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-with-variable.png?w=1650&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=5d360aac28b60689789e8d3274103611 1650w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-with-variable.png?w=2500&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=b9b98555c36f929004d234cc7fadaea5 2500w" />

2. Highlight text you want to templatize and click the tooltip button that shows up. Enter a name for your variable, and convert. <img src="https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/langsmith/images/convert-to-variable.gif" alt="Convert to variable" />

When we add a variable, we see a place to enter sample inputs for our prompt variables. Fill these in with values to test the prompt. <img src="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-inputs.png?fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=35674518c53e340d02719cbb7b5fd782" alt="Prompt inputs" data-og-width="775" width="775" data-og-height="134" height="134" data-path="langsmith/images/prompt-inputs.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-inputs.png?w=280&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=59775af2fccde924b7ad7657db2b4656 280w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-inputs.png?w=560&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=df9b24f1eb306578590ee772720ced08 560w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-inputs.png?w=840&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=df549771817326a72a9387d0133ea590 840w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-inputs.png?w=1100&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=4bc399d02630e4873ae34afbbb60057e 1100w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-inputs.png?w=1650&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=78917ac5c4c938d926a5fe420d4d2780 1650w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-inputs.png?w=2500&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=89368aa76e0764d3f3fcb90623b2f28b 2500w" />

### Structured output

Adding an output schema to your prompt will get output in a structured format. Learn more about structured output [here](/langsmith/prompt-engineering-concepts#structured-output). <img src="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/structured-output.png?fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=51cdef35a620c225896dbf2f3ab07528" alt="Structured output" data-og-width="814" width="814" data-og-height="574" height="574" data-path="langsmith/images/structured-output.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/structured-output.png?w=280&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=7af3797e6106f2c7858cc67dac7cfe60 280w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/structured-output.png?w=560&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=7a3b8bb3d32eda103213856e4e05e74c 560w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/structured-output.png?w=840&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=e973d61622e18ab678631c734c4b16a8 840w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/structured-output.png?w=1100&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=c63196b1604baef88db3f56375458005 1100w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/structured-output.png?w=1650&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=e672a8f8af25d414d61592a1b22205c0 1650w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/structured-output.png?w=2500&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=9d57196b5940203b66a31196ea464243 2500w" />

You can also add a tool by clicking the `+ Tool` button at the bottom of the prompt editor. See [here](/langsmith/use-tools) for more information on how to use tools.

<Callout type="info" icon="bird">
  Use **[Polly](/langsmith/polly)** in the Playground to generate tools, create output schemas, and optimize your prompts with AI assistance.
</Callout>

Click "Start" to run the prompt.

<img src="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-a-prompt-run.png?fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=9dec20b94326e5c8b11775b56eca55b4" alt="Create a prompt run" data-og-width="1525" width="1525" data-og-height="766" height="766" data-path="langsmith/images/create-a-prompt-run.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-a-prompt-run.png?w=280&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=10cdcbb52db991d37478cdd199f51baf 280w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-a-prompt-run.png?w=560&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=14986d2ef1ad2aafd69d5005413604c8 560w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-a-prompt-run.png?w=840&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=20cc523bb2ffa9756d95908b0b434d91 840w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-a-prompt-run.png?w=1100&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=5bdcb8118c13d9e9710ccc663058f47c 1100w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-a-prompt-run.png?w=1650&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=1f6760ed7f81ce2d9c7907c8539d6122 1650w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-a-prompt-run.png?w=2500&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=4c47787a81ad1ffed842e630ec80a362 2500w" />

To save your prompt, click the "Save" button, name your prompt, and decide if you want it to be "private" or "public". Private prompts are only visible to your workspace, while public prompts are discoverable to anyone.

The model and configuration you select in the Playground settings will be saved with the prompt. When you reopen the prompt, the model and configuration will automatically load from the saved version. <img src="https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/save-prompt.png?fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=180e2c79fb9d1ee8d7869fc279e2d94a" alt="Save prompt" data-og-width="465" width="465" data-og-height="306" height="306" data-path="langsmith/images/save-prompt.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/save-prompt.png?w=280&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=2a2ea17f2ffb787ce2bbbfc88302636e 280w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/save-prompt.png?w=560&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=7120851531e79e13d8717ba14eb64483 560w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/save-prompt.png?w=840&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=6b7d47e08120d2329fa923be8c19a612 840w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/save-prompt.png?w=1100&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=b6a4ed33c82c54f093ad4f07db1b7a1c 1100w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/save-prompt.png?w=1650&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=5746af64213ab0bc08d7315a895a0d28 1650w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/save-prompt.png?w=2500&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=470e4700c6ed64348f25ae23a8d462c5 2500w" />

<Check>
  The first time you create a public prompt, you'll be asked to set a LangChain Hub handle. All your public prompts will be linked to this handle. In a shared workspace, this handle will be set for the whole workspace.
</Check>

<img src="https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/public-handle.png?fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=56dbd809c50fb2abc816c73c599f0baf" alt="Public handle" data-og-width="575" width="575" data-og-height="357" height="357" data-path="langsmith/images/public-handle.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/public-handle.png?w=280&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=2e87d4538d4413b9ce13aed26f43e075 280w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/public-handle.png?w=560&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=df539980aec2f06214ee13668d271e38 560w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/public-handle.png?w=840&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=0b19f257c2d9eb78b88c0df6e7920d8d 840w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/public-handle.png?w=1100&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=06c1efd1463437913cbdd6e19274f354 1100w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/public-handle.png?w=1650&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=648394098abe45d6d916ee1fe3f9066b 1650w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/public-handle.png?w=2500&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=844bf001cfa48ba449c873d228cc5fa3 2500w" />

You've just created your first prompt! View a table of your prompts in the prompts tab.

<img src="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-table.png?fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=9f8f5567bb93a0add181a51531474796" alt="Prompt table" data-og-width="1508" width="1508" data-og-height="309" height="309" data-path="langsmith/images/prompt-table.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-table.png?w=280&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=6421b33ff02f9af3f994e665fbcddf96 280w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-table.png?w=560&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=bf3d973fd239d93c0c4b0dd45e2e7129 560w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-table.png?w=840&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=d2d60a1b18eb7baaeaa5a04fa67d4ac7 840w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-table.png?w=1100&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=9d11895d724a60910231494927f86e24 1100w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-table.png?w=1650&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=52afb51d257f64c5e59ad77e3a3cb67a 1650w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-table.png?w=2500&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=15e2b24c349a9f21729b572fdb23734f 2500w" />

To add metadata to your prompt, click the prompt and then click the "Edit" pencil icon next to the name. This brings you to where you can add additional information about the prompt, including a description, a README, and use cases. For public prompts this information will be visible to anyone who views your prompt in the LangChain Hub.

<img src="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/pencil.png?fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=e54ca6c0c8283b027f5848f79d1cf064" alt="Pencil" data-og-width="1167" width="1167" data-og-height="1067" height="1067" data-path="langsmith/images/pencil.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/pencil.png?w=280&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=0336448912188bb85366b0c49556d207 280w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/pencil.png?w=560&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=6456cdae3e5743b770ca530748efd21b 560w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/pencil.png?w=840&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=7f16e9adaa3e2d3063623317344fb7d7 840w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/pencil.png?w=1100&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=12e5f2c3a2cc2f91d66d467cff910809 1100w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/pencil.png?w=1650&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=ce6cb1b3011638d9bec990c1e8131837 1650w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/pencil.png?w=2500&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=b61eb5331a47c9e6998261799729fdbf 2500w" /> <img src="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/edit-prompt.png?fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=febb5f53b2f917cf3e5a2ff2566eaef4" alt="Edit prompt" data-og-width="1508" width="1508" data-og-height="1084" height="1084" data-path="langsmith/images/edit-prompt.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/edit-prompt.png?w=280&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=440242ac2e20e092c50810ca84d37286 280w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/edit-prompt.png?w=560&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=46ad1078bdd4342cc49ecd1a70837149 560w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/edit-prompt.png?w=840&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=f4998ff77574085ec2eb2fdc8c755fdc 840w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/edit-prompt.png?w=1100&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=2065392afa627416297cc8dc5a10780d 1100w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/edit-prompt.png?w=1650&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=bda747e312cbabdd107a7b54b4e1c03e 1650w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/edit-prompt.png?w=2500&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=846eaa58fed8f3a14aa76dbb610a0e41 2500w" />

---

## Dynamic few shot example selection

**URL:** llms-txt#dynamic-few-shot-example-selection

**Contents:**
- Pre-conditions
- Index your dataset for few shot search
- Test search quality in the few shot playground
- Adding few shot search to your application
  - Code snippets

Source: https://docs.langchain.com/langsmith/index-datasets-for-dynamic-few-shot-example-selection

<Note>
  This feature is in open beta. It is only available to paid team plans. Please contact support via [support.langchain.com](https://support.langchain.com) if you have questions about enablement.
</Note>

Configure your datasets so that you can search for few shot examples based on an incoming request.

1. Your dataset must use the KV store data type (we do not currently support chat model or LLM type datasets)
2. You must have an input schema defined for your dataset. See our docs on setting up schema validation [in our UI](/langsmith/manage-datasets-in-application#dataset-schema-validation) for details.
3. You must be on a paid team plan (e.g. Plus plan)
4. You must be on LangSmith cloud

## Index your dataset for few shot search

Navigate to the datasets UI, and click the new `Few-Shot search` tab. Hit the `Start sync` button, which will create a new index on your dataset to make it searchable.

<img src="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-tab-unsynced.png?fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=7bc50f1a3d4ea7b9e7458f3ed9770179" alt="Few shot tab unsynced" data-og-width="3208" width="3208" data-og-height="1902" height="1902" data-path="langsmith/images/few-shot-tab-unsynced.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-tab-unsynced.png?w=280&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=c2ee3688a24b8d142d4a5dd89c8797c1 280w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-tab-unsynced.png?w=560&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=44a4d8b59948893b4bd20d4c1b62198c 560w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-tab-unsynced.png?w=840&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=16a303eab8e2aede574c12353f782789 840w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-tab-unsynced.png?w=1100&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=fbcf4566ec48c219bb7828bdc2cfe6b9 1100w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-tab-unsynced.png?w=1650&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=15da2b6b3e4a29ac3a2b4e139e2cf345 1650w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-tab-unsynced.png?w=2500&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=6bd99520313da2fedbbbaf388c956ba7 2500w" />

By default, we sync to the latest version of your dataset. That means when new examples are added to your dataset, they will automatically be added to your index. This process runs every few minutes, so there should be a very short delay for indexing new examples. You can see whether your index is up to date under `Few-shot index` on the lefthand side of the screen in the next section.

## Test search quality in the few shot playground

Now that you have turned on indexing for your dataset, you will see the new few shot playground.

<img src="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-synced-empty-state.png?fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=b2b714b5a281ab8f39761566afd452f7" alt="Few shot synced empty state" data-og-width="3208" width="3208" data-og-height="1902" height="1902" data-path="langsmith/images/few-shot-synced-empty-state.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-synced-empty-state.png?w=280&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=b8e4e648ce36f12a141f98815fd2e63d 280w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-synced-empty-state.png?w=560&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=49044eef3af8c08b60bcfeabadde6d16 560w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-synced-empty-state.png?w=840&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=b0fb897716bfac9521d0490c11eb006e 840w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-synced-empty-state.png?w=1100&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=f21c2ad1fc5177af66c5f0c5ac59f660 1100w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-synced-empty-state.png?w=1650&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=dd9e2f9aa42366063ca14ad2b365e6fc 1650w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-synced-empty-state.png?w=2500&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=72158d44bcf916f2548bc5c7a6dabbce 2500w" />

You can type in a sample input, and check which results would be returned by our search API.

<img src="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-search-results.png?fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=f64d39010f85b68d4d9ae3febc2b59d7" alt="Few shot search results" data-og-width="3208" width="3208" data-og-height="1902" height="1902" data-path="langsmith/images/few-shot-search-results.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-search-results.png?w=280&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=cbbd01172c4514eb3d775a4c0f3ca2e4 280w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-search-results.png?w=560&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=4a15ea167365f8d9105ab5aab50ed241 560w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-search-results.png?w=840&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=94ac208df6e860b9c194a646e3183779 840w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-search-results.png?w=1100&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=ec68d9679e4cc86eebe352a9364e8894 1100w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-search-results.png?w=1650&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=5650c218963b5e8bd8d56e0bf886cd3e 1650w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-search-results.png?w=2500&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=89e90c66c065bee2a728cd5dad69432a 2500w" />

Each result will have a score and a link to the example in the dataset. The scoring system works such that 0 is a completely random result, and higher scores are better. Results will be sorted in descending order according to score.

<Note>
  Search uses a BM25-like algorithm for keyword based similarity scores. The actual score is subject to change as we improve the search algorithm, so we recommend not relying on the scores themselves, as their meaning may evolve over time. They are simply used for convenience in vibe-testing outputs in the playground.
</Note>

## Adding few shot search to your application

Click the `Get Code Snippet` button in the previous diagram, you'll be taken to a screen that has code snippets from our LangSmith SDK in different languages.

<img src="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-code-snippet.png?fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=015d9416ef4f2708a6f2dfedceb1ea07" alt="Few shot code snippet" data-og-width="3208" width="3208" data-og-height="1902" height="1902" data-path="langsmith/images/few-shot-code-snippet.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-code-snippet.png?w=280&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=a5b15cf813569f4f218d972f2dbe89a5 280w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-code-snippet.png?w=560&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=231a3aad9937aab1fa92e65839bb5869 560w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-code-snippet.png?w=840&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=8aa86a24694342bca8ab387c83338afe 840w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-code-snippet.png?w=1100&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=d92247c22e6fb2fd85e80713616b7fba 1100w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-code-snippet.png?w=1650&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=28f6e81c67c52687cd24431b83145675 1650w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-code-snippet.png?w=2500&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=aeafca83ae2489c43aa38d24165e5d62 2500w" />

For code samples on using few shot search in LangChain python applications, please see our [how-to guide in the LangChain docs](https://python.langchain.com/v0.2/docs/how_to/example_selectors_langsmith/).

<Note>
  Please ensure you are using the python SDK with version >= 1.101 or the typescript SDK with version >= 1.43
</Note>

For copy and paste convenience, you can find the similar code snippets to the ones shown in the screenshot above here:

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/index-datasets-for-dynamic-few-shot-example-selection.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
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

```

---

## Dynamic prompts

**URL:** llms-txt#dynamic-prompts

@dynamic_prompt
def dynamic_system_prompt(request: ModelRequest) -> str:
    user_name = request.runtime.context.user_name  # [!code highlight]
    system_prompt = f"You are a helpful assistant. Address the user as {user_name}."
    return system_prompt

---

## How to improve your evaluator with few-shot examples

**URL:** llms-txt#how-to-improve-your-evaluator-with-few-shot-examples

**Contents:**
- How few-shot examples work
- Configure your evaluator
  - 1. Configure variable mapping
  - 2. Specify the number of few-shot examples to use
- Make corrections
- View your corrections dataset

Source: https://docs.langchain.com/langsmith/create-few-shot-evaluators

Using LLM-as-a-judge evaluators can be very helpful when you can't evaluate your system programmatically. However, their effectiveness depends on their quality and how well they align with human reviewer feedback. LangSmith provides the ability to improve the alignment of LLM-as-a-judge evaluator to human preferences using few-shot examples.

Human corrections are automatically inserted into your evaluator prompt using few-shot examples. Few-shot examples is a technique inspired by [few-shot prompting](https://www.promptingguide.ai/techniques/fewshot) that guides the models output with a few high-quality examples.

This guide covers how to set up few-shot examples as part of your LLM-as-a-judge evaluator and apply corrections to feedback scores.

## How few-shot examples work

* Few-shot examples are added to your evaluator prompt using the `{{Few-shot examples}}` variable
* Creating an evaluator with few-shot examples, will automatically create a dataset for you, which will be auto-populated with few-shot examples once you start making corrections
* At runtime, these examples will inserted into the evaluator to serve as a guide for its outputs - this will help the evaluator to better align with human preferences

## Configure your evaluator

<Note>
  Few-shot examples are not currently supported in LLM-as-a-judge evaluators that use the prompt hub and are only compatible with prompts that use mustache formatting.
</Note>

Before enabling few-shot examples, set up your LLM-as-a-judge evaluator. If you haven't done this yet, follow the steps in the [LLM-as-a-judge evaluator guide](/langsmith/llm-as-judge).

### 1. Configure variable mapping

Each few-shot example is formatted according to the variable mapping specified in the configuration. The variable mapping for few-shot examples, should contain the same variables as your main prompt, plus a `few_shot_explanation` and a `score` variable which should have the same name as your feedback key.

For example, if your main prompt has variables `question` and `response`, and your evaluator outputs a `correctness` score, then your few-shot prompt should have the vartiables `question`, `response`, `few_shot_explanation`, and `correctness`.

### 2. Specify the number of few-shot examples to use

You may also specify the number of few-shot examples to use. The default is 5. If your examples are very long, you may want to set this number lower to save tokens - whereas if your examples tend to be short, you can set a higher number in order to give your evaluator more examples to learn from. If you have more examples in your dataset than this number, we will randomly choose them for you.

<Info>
  [Audit evaluator scores](/langsmith/audit-evaluator-scores)
</Info>

As you start logging traces or running experiments, you will likely disagree with some of the scores that your evaluator has given. When you [make corrections to these scores](/langsmith/audit-evaluator-scores), you will begin seeing examples populated inside your corrections dataset. As you make corrections, make sure to attach explanations - these will get populated into your evaluator prompt in place of the `few_shot_explanation` variable.

The inputs to the few-shot examples will be the relevant fields from the inputs, outputs, and reference (if this an offline evaluator) of your chain/dataset. The outputs will be the corrected evaluator score and the explanations that you created when you left the corrections. Feel free to edit these to your liking. Here is an example of a few-shot example in a corrections dataset:

<img src="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-example.png?fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=8c7bfcc6cc4ab86c18240c3cbf2ea44c" alt="Few-shot example" data-og-width="1572" width="1572" data-og-height="790" height="790" data-path="langsmith/images/few-shot-example.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-example.png?w=280&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=91f4e17fd853ba23c1b04934144dfa77 280w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-example.png?w=560&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=e0a5e2a026e4166c341900dd49316f35 560w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-example.png?w=840&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=88aec2ef5c37c16c67e0eefecd3fbc0a 840w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-example.png?w=1100&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=bfbbd35cf503ce2f3dbf743fab8fb75b 1100w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-example.png?w=1650&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=bf0765bfeabc8d34ef49626dca0135ae 1650w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-example.png?w=2500&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=f9d2cf9437ee0e160a511903bd88238a 2500w" />

Note that the corrections may take a minute or two to be populated into your few-shot dataset. Once they are there, future runs of your evaluator will include them in the prompt!

## View your corrections dataset

In order to view your corrections dataset:

* **Online evaluators**: Select your run rule and click **Edit Rule**
* **Offline evaluators**: Select your evaluator and click **Edit Evaluator**

<img src="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/edit-evaluator.png?fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=03453ef08f1c272d5d9aaf71d1fb7301" alt="Edit Evaluator" data-og-width="800" width="800" data-og-height="284" height="284" data-path="langsmith/images/edit-evaluator.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/edit-evaluator.png?w=280&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=d495c791e6c8ae9d241085795d4b67b5 280w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/edit-evaluator.png?w=560&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=b1ddde8054744862494e4d3f02a460b0 560w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/edit-evaluator.png?w=840&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=9838e073d1d7e61c6b79d8f35ba1a1b3 840w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/edit-evaluator.png?w=1100&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=67322be4166f4479a466427a9b270ca1 1100w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/edit-evaluator.png?w=1650&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=4cd490404d1616498fed810b3ce75a21 1650w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/edit-evaluator.png?w=2500&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=4c8a87ad332661a0b8b472dd34f1f4ab 2500w" />

Head to your dataset of corrections linked in the the **Improve evaluator accuracy using few-shot examples** section. You can view and update your few-shot examples in the dataset.

<img src="https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/view-few-shot-ds.png?fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=3215f3f24a08186fd76c6dbad18a3cf5" alt="View few-shot dataset" data-og-width="1470" width="1470" data-og-height="478" height="478" data-path="langsmith/images/view-few-shot-ds.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/view-few-shot-ds.png?w=280&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=ad702a532a8f083c71056baff4370f30 280w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/view-few-shot-ds.png?w=560&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=d45ebd4263adc9c10598fad633167ca3 560w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/view-few-shot-ds.png?w=840&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=fe060c8d000a41566949ff35d6c62135 840w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/view-few-shot-ds.png?w=1100&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=f735943da46a1e57328b86246f5da25f 1100w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/view-few-shot-ds.png?w=1650&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=9861b9651d5d63a07662e7aa1bc68491 1650w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/view-few-shot-ds.png?w=2500&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=6084c3697ffd582e30301540906a5698 2500w" />

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/create-few-shot-evaluators.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

---

## How to sync prompts with GitHub

**URL:** llms-txt#how-to-sync-prompts-with-github

**Contents:**
- Prerequisites
- Understanding LangSmith "Prompt Commits" and webhooks
- Implementing a FastAPI server for webhook reception
- Configuring the webhook in LangSmith
- The workflow in action
- Beyond a simple commit

Source: https://docs.langchain.com/langsmith/prompt-commit

LangSmith provides a collaborative interface to create, test, and iterate on prompts.

While you can [dynamically fetch prompts](/langsmith/manage-prompts-programmatically#pull-a-prompt) from LangSmith into your application at runtime, you may prefer to sync prompts with your own database or version control system. To support this workflow, LangSmith allows you to receive notifications of prompt updates via webhooks.

**Why sync prompts with GitHub?**

* **Version Control:** Keep your prompts versioned alongside your application code in a familiar system.
* **CI/CD Integration:** Trigger automated staging or production deployments when critical prompts change.

<img src="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-excalidraw.png?fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=a7fd1ae2a70f91c14298803a48785f89" alt="Prompt Webhook Diagram" data-og-width="1336" width="1336" data-og-height="343" height="343" data-path="langsmith/images/prompt-excalidraw.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-excalidraw.png?w=280&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=02f868ec42337b43a533f23effa76417 280w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-excalidraw.png?w=560&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=68806f6d9d1e5b8dbaf49d98294190da 560w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-excalidraw.png?w=840&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=133aeb6d3a880b989c2246632b8c0d5d 840w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-excalidraw.png?w=1100&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=fc7091cce5fec3407e005f798db85544 1100w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-excalidraw.png?w=1650&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=d789978f57574ec4f0c75beac19fc10c 1650w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-excalidraw.png?w=2500&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=d6362e5787b7fd1a5db69b3d704912bb 2500w" />

Before we begin, ensure you have the following set up:

1. **GitHub Account:** A standard GitHub account.

2. **GitHub Repository:** Create a new (or choose an existing) repository where your LangSmith prompt manifests will be stored. This could be the same repository as your application code or a dedicated one for prompts.

3. **GitHub Personal Access Token (PAT):**

* LangSmith webhooks don't directly interact with GitHub—they call an intermediary server that *you* create.
   * This server requires a GitHub PAT to authenticate and make commits to your repository.
   * Must include the `repo` scope (`public_repo` is sufficient for public repositories).
   * Go to **GitHub > Settings > Developer settings > Personal access tokens > Tokens (classic)**.
   * Click **Generate new token (classic)**.
   * Name it (e.g., "LangSmith Prompt Sync"), set an expiration, and select the required scopes.
   * Click **Generate token** and **copy it immediately** — it won't be shown again.
   * Store the token securely and provide it as an environment variable to your server.

## Understanding LangSmith "Prompt Commits" and webhooks

In LangSmith, when you save changes to a prompt, you're essentially creating a new version or a "Prompt Commit." These commits are what can trigger webhooks.

The webhook will send a JSON payload containing the new **prompt manifest**.

<Accordion title="Sample Webhook Payload">
  
</Accordion>

<Note>
  It's important to understand that LangSmith webhooks for prompt commits are generally triggered at the **workspace level**. This means if *any* prompt within your LangSmith workspace is modified and a "prompt commit" is saved, the webhook will fire and send the updated manifest of the prompt. The payloads are identifiable by prompt id. Your receiving server should be designed with this in mind.
</Note>

## Implementing a FastAPI server for webhook reception

To effectively process webhook notifications from LangSmith when prompts are updated, an intermediary server application is necessary. This server will act as the receiver for HTTP POST requests sent by LangSmith. For demonstration purposes in this guide, we will outline the creation of a simple FastAPI application to fulfill this role.

This publicly accessible server will be responsible for:

1. **Receiving Webhook Requests:** Listening for incoming HTTP POST requests.
2. **Parsing Payloads:** Extracting and interpreting the JSON-formatted prompt manifest from the request body.
3. **Committing to GitHub:** Programmatically creating a new commit in your specified GitHub repository, containing the updated prompt manifest. This ensures your prompts remain version-controlled and synchronized with changes made in LangSmith.

For deployment, platforms like [Render.com](https://render.com/) (offering a suitable free tier), Vercel, Fly.io, or other cloud providers (AWS, GCP, Azure) can be utilized to host the FastAPI application and obtain a public URL.

The server's core functionality will include an endpoint for webhook reception, logic for parsing the manifest, and integration with the GitHub API (using a Personal Access Token for authentication) to manage commits.

<Accordion title="Minimal FastAPI Server Code ()">
  `main.py`

This server will listen for incoming webhooks from LangSmith and commit the received prompt manifest to your GitHub repository.

**Key aspects of this server:**

* **Configuration (`.env`):** It expects a `.env` file with your `GITHUB_TOKEN`, `GITHUB_REPO_OWNER`, and `GITHUB_REPO_NAME`. You can also customize `GITHUB_FILE_PATH` (default: `LangSmith_prompt_manifest.json`) and `GITHUB_BRANCH` (default: `main`).
  * **GitHub Interaction:** The `commit_manifest_to_github` function handles the logic of fetching the current file's SHA (to update it) and then committing the new manifest content.
  * **Webhook Endpoint (`/webhook/commit`):** This is the URL path your LangSmith webhook will target.
  * **Error Handling:** Basic error handling for GitHub API interactions is included.

**Deploy this server to your chosen platform (e.g., Render) and note down its public URL (e.g., `https://prompt-commit-webhook.onrender.com`).**
</Accordion>

## Configuring the webhook in LangSmith

Once your FastAPI server is deployed and you have its public URL, you can configure the webhook in LangSmith:

1. Navigate to your LangSmith workspace.

2. Go to the **Prompts** section. Here you'll see a list of your prompts.

<img src="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-commit-main.png?fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=7e61c83cdd67749970d8f0e401066d60" alt="LangSmith Prompts section" data-og-width="2996" width="2996" data-og-height="852" height="852" data-path="langsmith/images/prompt-commit-main.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-commit-main.png?w=280&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=f492027577eacd4131954de447fa77f2 280w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-commit-main.png?w=560&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=b5f7ea835f9cddd0724a209869c2512e 560w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-commit-main.png?w=840&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=9aceebb242173d56a79e4974eb0fc7cd 840w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-commit-main.png?w=1100&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=2ec5c08e0a4682b84a202ebb52bf981d 1100w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-commit-main.png?w=1650&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=7dce8f5f164d40ab0f47dbf7e308382e 1650w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-commit-main.png?w=2500&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=03f8d9d0d9368ec370a71f7605f019a2 2500w" />

3. On the top right of the Prompts page, click the **+ Webhook** button.

4. You'll be presented with a form to configure your webhook:

<img src="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-commit-webhook.png?fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=775cc6392de007e894c42400117d113e" alt="LangSmith Webhook configuration modal" data-og-width="3008" width="3008" data-og-height="1454" height="1454" data-path="langsmith/images/prompt-commit-webhook.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-commit-webhook.png?w=280&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=a1d037dbc657bc0758b444d94d458c91 280w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-commit-webhook.png?w=560&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=708b8a9d27bd584fdd3a4a8df17be36d 560w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-commit-webhook.png?w=840&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=080f345e1d97aeac9b0d15a0d762fd42 840w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-commit-webhook.png?w=1100&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=387781e1444e51ff64cc2b0f7f02cd26 1100w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-commit-webhook.png?w=1650&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=c855c18d16698e49737ea6f581162970 1650w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-commit-webhook.png?w=2500&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=38e417a519b578f880d59a6c23efb102 2500w" />

* **Webhook URL:** Enter the full public URL of your deployed FastAPI server's endpoint. For our example server, this would be `https://prompt-commit-webhook.onrender.com/webhook/commit`.
   * **Headers (Optional):**
     * You can add custom headers that LangSmith will send with each webhook request.

5. **Test the Webhook:** LangSmith provides a "Send Test Notification" button. Use this to send a sample payload to your server. Check your server logs (e.g., on Render) to ensure it receives the request and processes it successfully (or to debug any issues).

6. **Save** the webhook configuration.

## The workflow in action

<img src="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-sequence-diagram.png?fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=823988be6300f39a6e9de784b34a2a77" alt="Workflow Diagram showing: User saves prompt in LangSmith, LangSmith sends webhook to FastAPI Server, which interacts with GitHub to update files" data-og-width="2922" width="2922" data-og-height="1014" height="1014" data-path="langsmith/images/prompt-sequence-diagram.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-sequence-diagram.png?w=280&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=13a26887fccdca822c175912ed7fbd3b 280w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-sequence-diagram.png?w=560&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=07e46cc25aa6d0ebe76b14ce9057936b 560w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-sequence-diagram.png?w=840&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=887758bfcf886c3062177706b7f22fb1 840w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-sequence-diagram.png?w=1100&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=a5aa30f606eac545f30a715eccfd80a1 1100w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-sequence-diagram.png?w=1650&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=32cae9f09ec30759550214f3c3e490ff 1650w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-sequence-diagram.png?w=2500&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=bced33a052aa88056de397389f9f7d64 2500w" />

Now, with everything set up, here's what happens:

1. **Prompt Modification:** A user (developer or non-technical team member) modifies a prompt in the LangSmith UI and saves it, creating a new "prompt commit."

2. **Webhook Trigger:** LangSmith detects this new prompt commit and triggers the configured webhook.

3. **HTTP Request:** LangSmith sends an HTTP POST request to the public URL of your FastAPI server (e.g., `https://prompt-commit-webhook.onrender.com/webhook/commit`). The body of this request contains the JSON prompt manifest for the entire workspace.

4. **Server Receives Payload:** Your FastAPI server's endpoint receives the request.

5. **GitHub Commit:** The server parses the JSON manifest from the request body. It then uses the configured GitHub Personal Access Token, repository owner, repository name, file path, and branch to:

* Check if the manifest file already exists in the repository on the specified branch to get its SHA (this is necessary for updating an existing file).
   * Create a new commit with the latest prompt manifest, either creating the file or updating it if it already exists. The commit message will indicate that it's an update from LangSmith.

6. **Confirmation:** You should see the new commit appear in your GitHub repository.

<img src="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-commit-github.png?fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=213d6364ce20e4acf4e3eb7fe8c1b13d" alt="Manifest commited to GitHub" data-og-width="2982" width="2982" data-og-height="1270" height="1270" data-path="langsmith/images/prompt-commit-github.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-commit-github.png?w=280&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=f03e1a469e28196f66bc1f92993e6045 280w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-commit-github.png?w=560&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=645f3cf20850a03a89a2e56a53d95719 560w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-commit-github.png?w=840&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=418f7716a8521e3d57a4381d4ebd4d08 840w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-commit-github.png?w=1100&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=34af751c0c20b176c715f0c6f86654f1 1100w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-commit-github.png?w=1650&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=13309faa18bde23df5e6df56521823fb 1650w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-commit-github.png?w=2500&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=f17d618b6d8e237aa8be023cccea4fd3 2500w" />

You've now successfully synced your LangSmith prompts with GitHub!

## Beyond a simple commit

Our example FastAPI server performs a direct commit of the entire prompt manifest. However, this is just the starting point. You can extend the server's functionality to perform more sophisticated actions:

* **Granular Commits:** Parse the manifest and commit changes to individual prompt files if you prefer a more granular structure in your repository.
* **Trigger CI/CD:** Instead of (or in addition to) committing, have the server trigger a CI/CD pipeline (e.g., Jenkins, GitHub Actions, GitLab CI) to deploy a staging environment, run tests, or build new application versions.
* **Update Databases/Caches:** If your application loads prompts from a database or cache, update these stores directly.
* **Notifications:** Send notifications to Slack, email, or other communication channels about prompt changes.
* **Selective Processing:** Based on metadata within the LangSmith payload (if available, e.g., which specific prompt changed or by whom), you could apply different logic.

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/prompt-commit.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

**Examples:**

Example 1 (unknown):
```unknown
</Accordion>

<Note>
  It's important to understand that LangSmith webhooks for prompt commits are generally triggered at the **workspace level**. This means if *any* prompt within your LangSmith workspace is modified and a "prompt commit" is saved, the webhook will fire and send the updated manifest of the prompt. The payloads are identifiable by prompt id. Your receiving server should be designed with this in mind.
</Note>

## Implementing a FastAPI server for webhook reception

To effectively process webhook notifications from LangSmith when prompts are updated, an intermediary server application is necessary. This server will act as the receiver for HTTP POST requests sent by LangSmith. For demonstration purposes in this guide, we will outline the creation of a simple FastAPI application to fulfill this role.

This publicly accessible server will be responsible for:

1. **Receiving Webhook Requests:** Listening for incoming HTTP POST requests.
2. **Parsing Payloads:** Extracting and interpreting the JSON-formatted prompt manifest from the request body.
3. **Committing to GitHub:** Programmatically creating a new commit in your specified GitHub repository, containing the updated prompt manifest. This ensures your prompts remain version-controlled and synchronized with changes made in LangSmith.

For deployment, platforms like [Render.com](https://render.com/) (offering a suitable free tier), Vercel, Fly.io, or other cloud providers (AWS, GCP, Azure) can be utilized to host the FastAPI application and obtain a public URL.

The server's core functionality will include an endpoint for webhook reception, logic for parsing the manifest, and integration with the GitHub API (using a Personal Access Token for authentication) to manage commits.

<Accordion title="Minimal FastAPI Server Code ()">
  `main.py`

  This server will listen for incoming webhooks from LangSmith and commit the received prompt manifest to your GitHub repository.
```

---

## Include multimodal content in a prompt

**URL:** llms-txt#include-multimodal-content-in-a-prompt

**Contents:**
- Inline content
- Template variables
- Populate the template variable
- Run an evaluation

Source: https://docs.langchain.com/langsmith/multimodal-content

Some applications are based around multimodal content, like a chatbot that can answer questions about a PDF or image. In these cases, you'll want to include multimodal content in your prompt and test the model's ability to answer questions about the content.

The LangSmith Playground supports two methods for incorporating multimodal content in your prompts:

1. Inline content: Embed static files (images, PDFs, audio) directly in your prompt. This is ideal when you want to consistently include the same multimodal content across all uses of the prompt. For example, you might include a reference image that helps ground the model's responses.

2. Template variables: Create dynamic placeholders for attachments that can be populated with different content each time. This approach offers more flexibility, allowing you to:

* Test how the model handles different inputs
   * Create reusable prompts that work with varying content

<Note>
  Not all models support multimodal content. Before using multimodal features in the playground, make sure your selected model supports the file types you want to use.
</Note>

Click the file icon in the message where you want to add multimodal content. Under the `Upload content` tab, you can upload a file and include it inline in the prompt.

<img src="https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/upload-inline-multimodal-content.png?fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=b93d2a6731d26d3ff58a3d0d6d909159" alt="Upload inline multimodal content" data-og-width="410" width="410" data-og-height="339" height="339" data-path="langsmith/images/upload-inline-multimodal-content.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/upload-inline-multimodal-content.png?w=280&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=ae329136b8de8d5f4b12ecab49651063 280w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/upload-inline-multimodal-content.png?w=560&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=f1644a04d5a33e803a15bc9794ecb528 560w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/upload-inline-multimodal-content.png?w=840&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=275ffe46010c6b24012ed049a17a59fb 840w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/upload-inline-multimodal-content.png?w=1100&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=9591d26a3b27c0462f7674f84c2a525c 1100w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/upload-inline-multimodal-content.png?w=1650&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=f4439dc91e005750232b40efbb19954d 1650w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/upload-inline-multimodal-content.png?w=2500&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=1c429f8f78846a14e0c9a379b9a24355 2500w" />

## Template variables

Click the file icon in the message where you want to add multimodal content. Under the `Template variables` tab, you can create a template variable for a specific attachment type. Currently, only images, PDFs, and audio files (.wav, .mp3) are supported.

<img src="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/template-variable-multimodal-content.png?fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=e69596dd9fe7d16252c7054bf9efcdf0" alt="Template variable multimodal content" data-og-width="391" width="391" data-og-height="303" height="303" data-path="langsmith/images/template-variable-multimodal-content.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/template-variable-multimodal-content.png?w=280&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=1efb9ed1c9a4a64be7174b90ffbfe664 280w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/template-variable-multimodal-content.png?w=560&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=1375989ffa599f506d308441e46907f9 560w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/template-variable-multimodal-content.png?w=840&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=f50c62b520314c18e433f77952ff79a2 840w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/template-variable-multimodal-content.png?w=1100&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=e38e8283352a13b54e96a381a2449396 1100w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/template-variable-multimodal-content.png?w=1650&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=331ff1a4664debd8d7b08a6ad645d9c6 1650w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/template-variable-multimodal-content.png?w=2500&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=ffa740fa2a3f4f52173cd073843d697f 2500w" />

## Populate the template variable

Once you've added a template variable, you can provide content for it using the panel on the right side of the screen. Simply click the `+` button to upload or select content that will be used to populate the template variable.

<img src="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/manual-prompt-multimodal.png?fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=5983e91ca9f596918c9068f8d7450d8d" alt="Manual prompt multimodal" data-og-width="1466" width="1466" data-og-height="482" height="482" data-path="langsmith/images/manual-prompt-multimodal.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/manual-prompt-multimodal.png?w=280&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=ccb36221eb97f54196de13df4f9749e7 280w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/manual-prompt-multimodal.png?w=560&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=6b4554ac3156e805655eba6afd2ce771 560w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/manual-prompt-multimodal.png?w=840&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=a3e85646401f9aa31e1d79257344c158 840w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/manual-prompt-multimodal.png?w=1100&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=9727ce9dec69152f6e49e3d8ff575300 1100w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/manual-prompt-multimodal.png?w=1650&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=f73957416f51c78a0e29c449f64ff1e2 1650w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/manual-prompt-multimodal.png?w=2500&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=ab8421f512b312b56ac515b970d337f4 2500w" />

After testing out your prompt manually, you can [run an evaluation](/langsmith/evaluate-with-attachments?mode=ui) to see how the prompt performs over a golden dataset of examples.

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/multimodal-content.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

---

## Load a prompt by name

**URL:** llms-txt#load-a-prompt-by-name

messages = await client.get_prompt("server_name", "summarize")  # [!code highlight]

---

## Load a prompt with arguments

**URL:** llms-txt#load-a-prompt-with-arguments

messages = await client.get_prompt(  # [!code highlight]
    "server_name",  # [!code highlight]
    "code_review",  # [!code highlight]
    arguments={"language": "python", "focus": "security"}  # [!code highlight]
)  # [!code highlight]

---

## Manage prompts

**URL:** llms-txt#manage-prompts

**Contents:**
- Commit tags
  - Create a tag
  - Move a tag
  - Delete a tag
  - Use tags in code

Source: https://docs.langchain.com/langsmith/manage-prompts

LangSmith provides several tools to help you manage your [*prompts*](/langsmith/prompt-engineering-concepts) effectively. This page describes the following features:

* [Commit tags](#commit-tags) for version control and environment management.
* [Webhook triggers](#trigger-a-webhook-on-prompt-commit) for automating workflows when prompts are updated.
* [Public prompt hub](#public-prompt-hub) for discovering and using community-created prompts.

[*Commit tags*](/langsmith/prompt-engineering-concepts#tags) are labels that reference a specific [*commit*](/langsmith/prompt-engineering-concepts#commits) in your prompt's version history. They help you mark significant versions and control which versions run in different environments. By referencing tags rather than commit IDs in your code, you can update which version is being used without modifying the code itself.

Each tag references exactly one commit, though you can reassign a tag to point to a different commit.

<Note>
  **Not to be confused with resource tags**: Commit tags are specific to prompt versioning and reference individual commits in a prompt's history. [Resource tags](/langsmith/set-up-resource-tags) are key-value pairs used to organize workspace resources like projects, datasets, and prompts. While both can use similar naming conventions (like `prod` or `staging`), commit tags control **which version** of a prompt runs, while resource tags help you **organize and filter** resources across your workspace.
</Note>

To create a tag, navigate to the **Commits** tab for a prompt. Click on the tag icon next to the commit you want to tag. Click **New Tag** and enter a name for the tag.

<img src="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/commits-tab.png?fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=b0cb7961f70d5c0bab9af960041bc54f" alt="Commits tab" data-og-width="2868" width="2868" data-og-height="992" height="992" data-path="langsmith/images/commits-tab.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/commits-tab.png?w=280&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=5786acfc0582c73c73efb5535a954ab4 280w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/commits-tab.png?w=560&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=410aa69f0ef5cc13ff7651df331495b7 560w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/commits-tab.png?w=840&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=b9845d256b71636a9bb6ee60c774a29e 840w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/commits-tab.png?w=1100&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=e16686b15bf2a95709a5d963ffc339d0 1100w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/commits-tab.png?w=1650&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=cb9560e6aa774505cb9ff1857f95ae61 1650w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/commits-tab.png?w=2500&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=bef88e11fa0de6173fc4dfd9c9339f39 2500w" /> <img src="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-new-prompt-tag.png?fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=cc27df9c5392a9b71319969c14924c61" alt="Create new prompt tag" data-og-width="1410" width="1410" data-og-height="872" height="872" data-path="langsmith/images/create-new-prompt-tag.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-new-prompt-tag.png?w=280&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=ed473769995e6148b60aec9cdd652ab6 280w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-new-prompt-tag.png?w=560&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=1f817be111dfc54af9717f9cdb664752 560w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-new-prompt-tag.png?w=840&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=fb0b979bf3362bd8faf796e4d617ac1c 840w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-new-prompt-tag.png?w=1100&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=22c63285bd22dd0c82d53b8d46c6638b 1100w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-new-prompt-tag.png?w=1650&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=1b4d05163bd948c4bce8ea08b5ceb70f 1650w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-new-prompt-tag.png?w=2500&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=c34b5ce29b2f1914399b6a084885e09a 2500w" />

To point a tag to a different commit, click on the tag icon next to the destination commit, and select the tag you want to move. This will automatically update the tag to point to the new commit.

<img src="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/move-prompt-tag.png?fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=3cb3c6218961cbdd8f6f1fb6d06b50e3" alt="Move prompt tag" data-og-width="874" width="874" data-og-height="694" height="694" data-path="langsmith/images/move-prompt-tag.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/move-prompt-tag.png?w=280&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=c2094e7486cfd3a7f4d7979e7883d1bc 280w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/move-prompt-tag.png?w=560&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=163481cc4580e4fe7934a5e02497fb9f 560w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/move-prompt-tag.png?w=840&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=9d53ef06dc6d69cc4024821fe8cfc32d 840w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/move-prompt-tag.png?w=1100&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=00ce6c08638961bfbbe5713c0066929b 1100w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/move-prompt-tag.png?w=1650&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=fa898ee3d7089b443e741d4f10b7845a 1650w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/move-prompt-tag.png?w=2500&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=cd97d2004b3b0a2ac0d3c7e4d3e7fff7 2500w" />

To delete a tag, click on the delete icon next to the tag you want to delete. This will delete the tag altogether and it will no longer be associated with any commit.

Tags provide a stable way to reference specific versions of your prompts in code. Instead of using commit hashes directly, you can reference tags that can be updated without changing your code.

Here is an example of pulling a prompt by tag in Python:

```python  theme={null}
prompt = client.pull_prompt("joke-generator:prod")

---

## Manage prompts programmatically

**URL:** llms-txt#manage-prompts-programmatically

**Contents:**
- Install packages
- Configure environment variables
- Push a prompt
- Pull a prompt
- Use a prompt without LangChain
  - OpenAI
  - Anthropic
- List, delete, and like prompts

Source: https://docs.langchain.com/langsmith/manage-prompts-programmatically

You can use the LangSmith Python and TypeScript SDK to manage prompts programmatically.

<Note>
  Previously this functionality lived in the `langchainhub` package which is now deprecated. All functionality going forward will live in the `langsmith` package.
</Note>

In Python, you can directly use the LangSmith SDK (*recommended, full functionality*) or you can use through the LangChain package (limited to pushing and pulling prompts).

In TypeScript, you must use the LangChain npm package for pulling prompts (it also allows pushing). For all other functionality, use the LangSmith package.

## Configure environment variables

If you already have `LANGSMITH_API_KEY` set to your current workspace's api key from LangSmith, you can skip this step.

Otherwise, get an API key for your workspace by navigating to `Settings > API Keys > Create API Key` in LangSmith.

Set your environment variable.

<Note>
  What we refer to as "prompts" used to be called "repos", so any references to "repo" in the code are referring to a prompt.
</Note>

To create a new prompt or update an existing prompt, you can use the `push prompt` method.

You can also push a prompt as a RunnableSequence of a prompt and a model. This is useful for storing the model configuration you want to use with this prompt. The provider must be supported by the LangSmith playground. (see settings here: [Supported Providers](https://langsmith.com/playground))

To pull a prompt, you can use the `pull prompt` method, which returns a the prompt as a langchain `PromptTemplate`.

To pull a **private prompt** you do not need to specify the owner handle (though you can, if you have one set).

To pull a **public prompt** from the LangChain Hub, you need to specify the handle of the prompt's author.

Similar to pushing a prompt, you can also pull a prompt as a RunnableSequence of a prompt and a model. Just specify include\_model when pulling the prompt. If the stored prompt includes a model, it will be returned as a RunnableSequence. Make sure you have the proper environment variables set for the model you are using.

When pulling a prompt, you can also specify a specific commit hash or [commit tag](/langsmith/manage-prompts#commit-tags) to pull a specific version of the prompt.

To pull a public prompt from the LangChain Hub, you need to specify the handle of the prompt's author.

<Note>
  For pulling prompts, if you are using Node.js or an environment that supports dynamic imports, we recommend using the `langchain/hub/node` entrypoint, as it handles deserialization of models associated with your prompt configuration automatically.

If you are in a non-Node environment, "includeModel" is not supported for non-OpenAI models and you should use the base `langchain/hub` entrypoint.
</Note>

## Use a prompt without LangChain

If you want to store your prompts in LangSmith but use them directly with a model provider's API, you can use our conversion methods. These convert your prompt into the payload required for the OpenAI or Anthropic API.

These conversion methods rely on logic from within LangChain integration packages, and you will need to install the appropriate package as a dependency in addition to your official SDK of choice. Here are some examples:

## List, delete, and like prompts

You can also list, delete, and like/unlike prompts using the `list prompts`, `delete prompt`, `like prompt` and `unlike prompt` methods. See the [LangSmith SDK client](https://github.com/langchain-ai/langsmith-sdk) for extensive documentation on these methods.

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/manage-prompts-programmatically.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
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

```

Example 3 (unknown):
```unknown
</CodeGroup>

## Configure environment variables

If you already have `LANGSMITH_API_KEY` set to your current workspace's api key from LangSmith, you can skip this step.

Otherwise, get an API key for your workspace by navigating to `Settings > API Keys > Create API Key` in LangSmith.

Set your environment variable.
```

Example 4 (unknown):
```unknown
<Note>
  What we refer to as "prompts" used to be called "repos", so any references to "repo" in the code are referring to a prompt.
</Note>

## Push a prompt

To create a new prompt or update an existing prompt, you can use the `push prompt` method.

<CodeGroup>
```

---

## Node that updates instructions

**URL:** llms-txt#node-that-updates-instructions

**Contents:**
  - Writing memories
  - Memory storage

def update_instructions(state: State, store: BaseStore):
    namespace = ("instructions",)
    instructions = store.search(namespace)[0]
    # Memory logic
    prompt = prompt_template.format(instructions=instructions.value["instructions"], conversation=state["messages"])
    output = llm.invoke(prompt)
    new_instructions = output['new_instructions']
    store.put(("agent_instructions",), "agent_a", {"instructions": new_instructions})
    ...
python  theme={null}
from langgraph.store.memory import InMemoryStore

def embed(texts: list[str]) -> list[list[float]]:
    # Replace with an actual embedding function or LangChain embeddings object
    return [[1.0, 2.0] * len(texts)]

**Examples:**

Example 1 (unknown):
```unknown
<img src="https://mintcdn.com/langchain-5e9cc07a/ybiAaBfoBvFquMDz/oss/images/update-instructions.png?fit=max&auto=format&n=ybiAaBfoBvFquMDz&q=85&s=13644c954ed79a45b8a1a762b3e39da1" alt="Update instructions" data-og-width="493" width="493" data-og-height="515" height="515" data-path="oss/images/update-instructions.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/ybiAaBfoBvFquMDz/oss/images/update-instructions.png?w=280&fit=max&auto=format&n=ybiAaBfoBvFquMDz&q=85&s=90632c71febee5777be6ae2c338f0880 280w, https://mintcdn.com/langchain-5e9cc07a/ybiAaBfoBvFquMDz/oss/images/update-instructions.png?w=560&fit=max&auto=format&n=ybiAaBfoBvFquMDz&q=85&s=aefcc771a030a2d6a89f815b87e60fd4 560w, https://mintcdn.com/langchain-5e9cc07a/ybiAaBfoBvFquMDz/oss/images/update-instructions.png?w=840&fit=max&auto=format&n=ybiAaBfoBvFquMDz&q=85&s=9115490b76daffe987e3867bc9176386 840w, https://mintcdn.com/langchain-5e9cc07a/ybiAaBfoBvFquMDz/oss/images/update-instructions.png?w=1100&fit=max&auto=format&n=ybiAaBfoBvFquMDz&q=85&s=0df26f2e6f669f2fbea59a9a49482fb4 1100w, https://mintcdn.com/langchain-5e9cc07a/ybiAaBfoBvFquMDz/oss/images/update-instructions.png?w=1650&fit=max&auto=format&n=ybiAaBfoBvFquMDz&q=85&s=132e7b1f377e0b57c03ab31c6d788df4 1650w, https://mintcdn.com/langchain-5e9cc07a/ybiAaBfoBvFquMDz/oss/images/update-instructions.png?w=2500&fit=max&auto=format&n=ybiAaBfoBvFquMDz&q=85&s=651cd1bb14e445a972a671a196b6a893 2500w" />

### Writing memories

There are two primary methods for agents to write memories: ["in the hot path"](#in-the-hot-path) and ["in the background"](#in-the-background).

<img src="https://mintcdn.com/langchain-5e9cc07a/dL5Sn6Cmy9pwtY0V/oss/images/hot_path_vs_background.png?fit=max&auto=format&n=dL5Sn6Cmy9pwtY0V&q=85&s=edd006d6189dc29a2edcba57c41fd744" alt="Hot path vs background" data-og-width="842" width="842" data-og-height="418" height="418" data-path="oss/images/hot_path_vs_background.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/dL5Sn6Cmy9pwtY0V/oss/images/hot_path_vs_background.png?w=280&fit=max&auto=format&n=dL5Sn6Cmy9pwtY0V&q=85&s=3efd9962012347a64b596d1d36925b33 280w, https://mintcdn.com/langchain-5e9cc07a/dL5Sn6Cmy9pwtY0V/oss/images/hot_path_vs_background.png?w=560&fit=max&auto=format&n=dL5Sn6Cmy9pwtY0V&q=85&s=add54b5469d7b4a8f22d7da250c19ddf 560w, https://mintcdn.com/langchain-5e9cc07a/dL5Sn6Cmy9pwtY0V/oss/images/hot_path_vs_background.png?w=840&fit=max&auto=format&n=dL5Sn6Cmy9pwtY0V&q=85&s=1e763d0f2ee8aa4f5b302ad44bc19d2f 840w, https://mintcdn.com/langchain-5e9cc07a/dL5Sn6Cmy9pwtY0V/oss/images/hot_path_vs_background.png?w=1100&fit=max&auto=format&n=dL5Sn6Cmy9pwtY0V&q=85&s=ce84a68af250e53a4693332d39179136 1100w, https://mintcdn.com/langchain-5e9cc07a/dL5Sn6Cmy9pwtY0V/oss/images/hot_path_vs_background.png?w=1650&fit=max&auto=format&n=dL5Sn6Cmy9pwtY0V&q=85&s=5f807accb9c63dae57c27c9a1d17f29a 1650w, https://mintcdn.com/langchain-5e9cc07a/dL5Sn6Cmy9pwtY0V/oss/images/hot_path_vs_background.png?w=2500&fit=max&auto=format&n=dL5Sn6Cmy9pwtY0V&q=85&s=ecef974859d58f691dbb22a4a1cc1572 2500w" />

#### In the hot path

Creating memories during runtime offers both advantages and challenges. On the positive side, this approach allows for real-time updates, making new memories immediately available for use in subsequent interactions. It also enables transparency, as users can be notified when memories are created and stored.

However, this method also presents challenges. It may increase complexity if the agent requires a new tool to decide what to commit to memory. In addition, the process of reasoning about what to save to memory can impact agent latency. Finally, the agent must multitask between memory creation and its other responsibilities, potentially affecting the quantity and quality of memories created.

As an example, ChatGPT uses a [save\_memories](https://openai.com/index/memory-and-new-controls-for-chatgpt/) tool to upsert memories as content strings, deciding whether and how to use this tool with each user message. See our [memory-agent](https://github.com/langchain-ai/memory-agent) template as an reference implementation.

#### In the background

Creating memories as a separate background task offers several advantages. It eliminates latency in the primary application, separates application logic from memory management, and allows for more focused task completion by the agent. This approach also provides flexibility in timing memory creation to avoid redundant work.

However, this method has its own challenges. Determining the frequency of memory writing becomes crucial, as infrequent updates may leave other threads without new context. Deciding when to trigger memory formation is also important. Common strategies include scheduling after a set time period (with rescheduling if new events occur), using a cron schedule, or allowing manual triggers by users or the application logic.

See our [memory-service](https://github.com/langchain-ai/memory-template) template as an reference implementation.

### Memory storage

LangGraph stores long-term memories as JSON documents in a [store](/oss/python/langgraph/persistence#memory-store). Each memory is organized under a custom `namespace` (similar to a folder) and a distinct `key` (like a file name). Namespaces often include user or org IDs or other labels that makes it easier to organize information. This structure enables hierarchical organization of memories. Cross-namespace searching is then supported through content filters.
```

---

## Node that *uses* the instructions

**URL:** llms-txt#node-that-*uses*-the-instructions

def call_model(state: State, store: BaseStore):
    namespace = ("agent_instructions", )
    instructions = store.get(namespace, key="agent_a")[0]
    # Application logic
    prompt = prompt_template.format(instructions=instructions.value["instructions"])
    ...

---

## Prompt engineering concepts

**URL:** llms-txt#prompt-engineering-concepts

**Contents:**
- Why prompt engineering?
- Prompts vs. prompt templates
- Prompts in LangSmith
  - Chat vs Completion
  - F-string vs. mustache
  - Tools
  - Structured output
  - Model
- Prompt versioning
  - Commits

Source: https://docs.langchain.com/langsmith/prompt-engineering-concepts

While traditional software applications are built by writing code, AI applications often derive their logic from prompts.

This guide will walk through the key concepts of prompt engineering in LangSmith.

## Why prompt engineering?

A prompt sets the stage for the model, like an audience member at an improv show directing the actor's next performance - it guides the model's behavior without changing its underlying capabilities. Just as telling an actor to "be a pirate" determines how they act, a prompt provides instructions, examples, and context that shape how the model responds.

Prompt engineering is important because it allows you to change the way the model behaves. While there are other ways to change the model's behavior (like fine-tuning), prompt engineering is usually the simplest to get started with and often provides the highest ROI.

We often see that prompt engineering is multi-disciplinary. Sometimes the best prompt engineer is not the software engineer who is building the application, but rather the product manager or another domain expert. It is important to have the proper tooling and infrastructure to support this cross-disciplinary building.

## Prompts vs. prompt templates

Although we often use these terms interchangably, it is important to understand the difference between "prompts" and "prompt templates".

Prompts refer to the messages that are passed into the language model.

Prompt Templates refer to a way of formatting information to get that prompt to hold the information that you want. Prompt templates can include variables for few shot examples, outside context, or any other external data that is needed in your prompt.

<img src="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-vs-prompt-template.png?fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=714ad4962c85cfb8847ebbf01559c217" alt="Prompt vs prompt template" data-og-width="1084" width="1084" data-og-height="450" height="450" data-path="langsmith/images/prompt-vs-prompt-template.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-vs-prompt-template.png?w=280&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=81497578f297dd5a7311de6f1c06ef85 280w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-vs-prompt-template.png?w=560&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=d13dfcf34430d876cdc1a2b77a5fd3c4 560w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-vs-prompt-template.png?w=840&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=feec2461df390de635a2534b50eab8e6 840w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-vs-prompt-template.png?w=1100&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=e1851de62aa377fc3d70ec62dd91c5b2 1100w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-vs-prompt-template.png?w=1650&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=6bccce7c02cb065f9ef8964fbe3112b6 1650w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-vs-prompt-template.png?w=2500&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=c3494cef2e70686d55493ded764cc8c0 2500w" />

## Prompts in LangSmith

You can store and version prompts templates in LangSmith. There are few key aspects of a prompt template to understand.

### Chat vs Completion

There are two different types of prompts: `chat` style prompts and `completion` style prompts.

Chat style prompts are a **list of messages**. This is the prompting style supported by most model APIs these days, and so this should generally be preferred.

Completion style prompts are just a string. This is an older style of prompting, and so mostly exists for legacy reasons.

### F-string vs. mustache

You can format your prompt with input variables using either [f-string](https://realpython.com/python-f-strings/) or [mustache](https://mustache.github.io/mustache.5.html) format. Here is an example prompt with f-string format:

And here is one with mustache:

To add a conditional mustache prompt:

* The playground UI will pick up `is_logged_in` variable, but any nested variables you'll need to specify yourself. Paste the following into inputs to ensure the above conditional prompt works:

<Check>
  The LangSmith Playground uses `f-string` as the default template format, but you can switch to `mustache` format in the prompt settings/template format section. `mustache` gives you more flexibility around conditional variables, loops, and nested keys. For conditional variables, you'll need to manually add json variables in the 'inputs' section. Read [the documentation](https://mustache.github.io/mustache.5.html)
</Check>

Tools are interfaces the LLM can use to interact with the outside world. Tools consist of a name, description, and JSON schema of arguments used to call the tool.

### Structured output

Structured output is a feature of most state of the art LLMs, wherein instead of producing raw text as output they stick to a specified schema. This may or may not use [Tools](#tools) under the hood.

<Check>
  Structured output is similar to tools, but different in a few key ways. With tools, the LLM choose which tool to call (or may choose not to call any); with structured output, the LLM **always** responds in this format. With tools, the LLM may select **multiple** tools; with structured output, only one response is generate.
</Check>

Optionally, you can store a model configuration alongside a prompt template. This includes the name of the model and any other parameters (temperature, etc).

Verisioning is a key part of iterating and collaborating on your different prompts.

Every saved update to a prompt creates a new commit with a unique commit hash. This allows you to:

* View the full history of changes to a prompt.
* Review earlier versions.
* Revert to a previous state if needed.
* Reference specific versions in your code using the commit hash (e.g., `client.pull_prompt("prompt_name:commit_hash")`).

In the UI, you can compare a commit with its previous version by toggling **Show diff** in the top-right corner of the **Commits** tab.

<img src="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/commit-diff.png?fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=a045b239f92dc1c616c7e42ae282c2b9" alt="The commit hashes list for a prompt with the diff of one commit." data-og-width="2884" width="2884" data-og-height="1426" height="1426" data-path="langsmith/images/commit-diff.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/commit-diff.png?w=280&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=5f1f1e66762226af9ec78e7dcd88a40e 280w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/commit-diff.png?w=560&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=9170a56b51a619a3aea586942c6d1825 560w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/commit-diff.png?w=840&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=198ae20ca965b50d42178bb241bddf46 840w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/commit-diff.png?w=1100&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=5e56c9323edf28650c4c667def63d7d1 1100w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/commit-diff.png?w=1650&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=25b8995161ed4523c09526eee44aef8a 1650w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/commit-diff.png?w=2500&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=ac495d702a4df63f35ac47e5584a1c4b 2500w" />

Commit tags are human-readable labels that point to specific commits in your prompt's history. Unlike commit hashes, tags can be moved to point to different commits, allowing you to update which version your code references without changing the code itself.

Use cases for commit tags can include:

* **Environment-specific tags**: Mark commits for `production` or `staging` environments, which allows you to switch between different versions without changing your code.
* **Version control**: Mark stable versions of your prompts, for example, `v1`, `v2`, which lets you reference specific versions in your code and track changes over time.
* **Collaboration**: Mark versions ready for review, which enables you to share specific versions with collaborators and get feedback.

<Note>
  **Not to be confused with resource tags**: Commit tags reference specific prompt versions. [Resource tags](/langsmith/set-up-resource-tags) are key-value pairs used to organize workspace resources.
</Note>

For detailed information on creating and managing commit tags, see [Manage prompts](/langsmith/manage-prompts#commit-tags).

The prompt playground makes the process of iterating and testing your prompts seamless. You can enter the playground from the sidebar or directly from a saved prompt.

In the playground you can:

* Change the model being used
* Change prompt template being used
* Change the output schema
* Change the tools available
* Enter the input variables to run through the prompt template
* Run the prompt through the model
* Observe the outputs

<Callout type="info" icon="bird">
  Use **[Polly](/langsmith/polly)** in the Playground to optimize prompts, generate tools, and create output schemas with AI assistance.
</Callout>

## Testing multiple prompts

You can add more prompts to your playground to easily compare outputs and decide which version is better:

<img src="https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/add-prompt-to-playground.gif?s=1c6f0c32b45a3f480b16d704c09570fc" alt="Add prompt to playground" data-og-width="1000" width="1000" data-og-height="539" height="539" data-path="langsmith/images/add-prompt-to-playground.gif" data-optimize="true" data-opv="3" />

## Testing over a dataset

To test over a dataset, you simply select the dataset from the top right and press Start. You can modify whether the results are streamed back as well as how many repitions there are in the test.

<img src="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/test-over-dataset-in-playground.gif?s=aaf0f90a0c61934a928f81d5e11e2c35" alt="Test over dataset in playground" data-og-width="1000" width="1000" data-og-height="539" height="539" data-path="langsmith/images/test-over-dataset-in-playground.gif" data-optimize="true" data-opv="3" />

You can click on the "View Experiment" button to dive deeper into the results of the test.

<iframe className="w-full aspect-video rounded-xl" src="https://www.youtube.com/embed/h4f6bIWGkog?si=IVJFfhldC7M3HL4G" title="YouTube video player" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen />

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/prompt-engineering-concepts.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

**Examples:**

Example 1 (unknown):
```unknown
And here is one with mustache:
```

Example 2 (unknown):
```unknown
To add a conditional mustache prompt:
```

Example 3 (unknown):
```unknown
* The playground UI will pick up `is_logged_in` variable, but any nested variables you'll need to specify yourself. Paste the following into inputs to ensure the above conditional prompt works:
```

---

## Prompt engineering

**URL:** llms-txt#prompt-engineering

Source: https://docs.langchain.com/langsmith/prompt-engineering

The following sections help you create, manage, and optimize your prompts:

<Columns cols={3}>
  <Card title="Review core concepts" icon="circle-info" href="/langsmith/prompt-engineering-concepts" arrow="true">
    Read definitions and key terminology for prompt engineering in LangSmith.
  </Card>

<Card title="Create and update prompts" icon="pen-to-square" href="/langsmith/create-a-prompt" arrow="true">
    Build prompts via the UI or SDK, configure settings, use tools, add multimodal inputs, and connect model providers.
  </Card>

<Card title="Manage prompts" icon="tags" href="/langsmith/manage-prompts" arrow="true">
    Organize with tags, commit changes, trigger webhooks, and share through the public prompt hub.
  </Card>

<Card title="Explore the prompt hub" icon="folder-tree" href="/langsmith/manage-prompts#public-prompt-hub" arrow="true">
    Browse and manage prompt tags and discover community prompts from the LangChain Hub.
  </Card>

<Card title="Open the prompt playground" icon="vial" href="/langsmith/prompt-engineering-concepts#prompt-playground" arrow="true">
    Test and experiment with prompts using custom endpoints and model configurations.
  </Card>

<Card title="Follow tutorials" icon="book-open" href="/langsmith/optimize-classifier" arrow="true">
    Learn step-by-step techniques, like optimizing classifiers and advanced prompt engineering.
  </Card>
</Columns>

<Callout type="info" icon="bird">
  Use **[Polly](/langsmith/polly)** in the Prompt Playground to optimize prompts, generate tools, and create output schemas with AI-powered assistance.
</Callout>

<Note>
  To set up a LangSmith instance, visit the [Platform setup section](/langsmith/platform-setup) to choose between cloud, hybrid, or self-hosted. All options include observability, evaluation, prompt engineering, and deployment.
</Note>

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/prompt-engineering.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

---

## Run an evaluation from the prompt playground

**URL:** llms-txt#run-an-evaluation-from-the-prompt-playground

**Contents:**
- Create an experiment in the prompt playground[​](#create-an-experiment-in-the-prompt-playground "Direct link to Create an experiment in the prompt playground")
- Add evaluation scores to the experiment[​](#add-evaluation-scores-to-the-experiment "Direct link to Add evaluation scores to the experiment")

Source: https://docs.langchain.com/langsmith/run-evaluation-from-prompt-playground

LangSmith allows you to run evaluations directly in the UI. The [**Prompt Playground**](/langsmith/prompt-engineering#prompt-playground) allows you to test your prompt or model configuration over a series of inputs to see how well it scores across different contexts or scenarios, without having to write any code.

Before you run an evaluation, you need to have an [existing dataset](/langsmith/evaluation-concepts#datasets). Learn how to [create a dataset from the UI](/langsmith/manage-datasets-in-application#set-up-your-dataset).

If you prefer to run experiments in code, visit [run an evaluation using the SDK](/langsmith/evaluate-llm-application).

<img src="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/playground-experiment.gif?s=05ec3d2b1aa6590c443a033924fc6141" alt="Playground experiment" data-og-width="1358" width="1358" data-og-height="720" height="720" data-path="langsmith/images/playground-experiment.gif" data-optimize="true" data-opv="3" />

<Callout type="info" icon="bird">
  **[Polly](/langsmith/polly)** is available in the Playground to help you optimize prompts before running evaluations.
</Callout>

## Create an experiment in the prompt playground[​](#create-an-experiment-in-the-prompt-playground "Direct link to Create an experiment in the prompt playground")

1. **Navigate to the playground** by clicking **Playground** in the sidebar.
2. **Add a prompt** by selecting an existing saved a prompt or creating a new one.
3. **Select a dataset** from the **Test over dataset** dropdown

* Note that the keys in the dataset input must match the input variables of the prompt. For example, in the above video the selected dataset has inputs with the key "blog", which correctly match the input variable of the prompt.
* There is a maximum of 15 input variables allowed in the prompt playground.

4. **Start the experiment** by clicking on the **Start** or CMD+Enter. This will run the prompt over all the examples in the dataset and create an entry for the experiment in the dataset details page. We recommend committing the prompt to the prompt hub before starting the experiment so that it can be easily referenced later when reviewing your experiment.
5. **View the full results** by clicking **View full experiment**. This will take you to the experiment details page where you can see the results of the experiment.

## Add evaluation scores to the experiment[​](#add-evaluation-scores-to-the-experiment "Direct link to Add evaluation scores to the experiment")

Evaluate your experiment over specific critera by adding evaluators. Add LLM-as-a-judge or custom code evaluators in the playground using the **+Evaluator** button.

To learn more about adding evaluators in via UI, visit [how to define an LLM-as-a-judge evaluator](/langsmith/llm-as-judge).

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/run-evaluation-from-prompt-playground.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

---

## Service A: Create a span and propagate context to Service B

**URL:** llms-txt#service-a:-create-a-span-and-propagate-context-to-service-b

def service_a():
    with tracer.start_as_current_span("service_a_operation") as span:
        # Create a chain
        prompt = ChatPromptTemplate.from_template("Summarize: {text}")
        model = ChatOpenAI()
        chain = prompt | model

# Run the chain
        result = chain.invoke({"text": "OpenTelemetry is an observability framework"})

# Propagate context to Service B
        headers = {}
        inject(headers)  # Inject trace context into headers

# Call Service B with the trace context
        response = requests.post(
            "http://service-b.example.com/process",
            headers=headers,
            json={"summary": result.content}
        )
        return response.json()

---

## Service B: Extract the context and continue the trace

**URL:** llms-txt#service-b:-extract-the-context-and-continue-the-trace

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def service_b_endpoint():
    # Extract the trace context from the request headers
    context = extract(request.headers)
    with tracer.start_as_current_span("service_b_operation", context=context) as span:
        data = request.json
        summary = data.get("summary", "")

# Process the summary with another LLM chain
        prompt = ChatPromptTemplate.from_template("Analyze the sentiment of: {text}")
        model = ChatOpenAI()
        chain = prompt | model
        result = chain.invoke({"text": summary})

return jsonify({"analysis": result.content})

if __name__ == "__main__":
    app.run(port=5000)
```

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/trace-with-opentelemetry.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

---

## Write your prompt with AI

**URL:** llms-txt#write-your-prompt-with-ai

**Contents:**
- Chat sidebar
- Quick actions
- Custom quick actions
- Diffing
- Saving and using prompts

Source: https://docs.langchain.com/langsmith/write-prompt-with-ai

The prompt canvas makes it easy to edit a prompt with the help of an LLM. This allows you to iterate faster on long prompts and also makes it easier to make overarching stylisting or tonal changes to your prompt. You can enter the promp canvas by clicking the glowing wand over any message in your prompt:

<img src="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-canvas-open.gif?s=480b38abe2797436e0b7969e2d961e23" alt="Prompt canvas open" data-og-width="1000" width="1000" data-og-height="539" height="539" data-path="langsmith/images/prompt-canvas-open.gif" data-optimize="true" data-opv="3" />

You can use the chat sidebar to ask questions about your prompt, or to give instructions in natural language to the LLM for how to rewrite your prompt.

<img src="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-canvas-rewrite.gif?s=91ba55b2e7b1e3a18a799265250dedb0" alt="Prompt canvas rewrite" data-og-width="1000" width="1000" data-og-height="539" height="539" data-path="langsmith/images/prompt-canvas-rewrite.gif" data-optimize="true" data-opv="3" />

<Note>
  You can also edit the prompt directly - you don't **need** to use the LLM. This is useful if you know what edits you want to make and just want to make them directly
</Note>

There are quick actions to change the reading level or length of the prompt with a single mouse click:

<img src="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-canvas-quick-actions.gif?s=6d2bb4ee78ec98fe551ce7f1a0e94ad9" alt="Prompt canvas quick actions" data-og-width="1000" width="1000" data-og-height="539" height="539" data-path="langsmith/images/prompt-canvas-quick-actions.gif" data-optimize="true" data-opv="3" />

## Custom quick actions

You can also save your own custom quick actions, for ease of use across all the prompts you are working on in LangSmith:

<img src="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-canvas-custom-quick-action.gif?s=3fd706f2fdd87abe339f83a2639ce708" alt="Prompt canvas custom quick action" data-og-width="1000" width="1000" data-og-height="539" height="539" data-path="langsmith/images/prompt-canvas-custom-quick-action.gif" data-optimize="true" data-opv="3" />

You can also see the specific differences between each version of your prompt by selecting the diff slider in the top right of the canvas:

<img src="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-canvas-diff.gif?s=be6259e6ac773c4a01c5b1ac4fe79e92" alt="Prompt canvas diff" data-og-width="1000" width="1000" data-og-height="539" height="539" data-path="langsmith/images/prompt-canvas-diff.gif" data-optimize="true" data-opv="3" />

## Saving and using prompts

Lastly, you can save the prompt you have created in the canvas by clicking the "Use this Version" button in the bottom right:

<img src="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prompt-canvas-save.gif?s=f54b0d1b6374e6b69750a6489c787172" alt="Prompt canvas save" data-og-width="1000" width="1000" data-og-height="539" height="539" data-path="langsmith/images/prompt-canvas-save.gif" data-optimize="true" data-opv="3" />

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/write-prompt-with-ai.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>

---

## -- This code should be in a separate file or service --

**URL:** llms-txt#---this-code-should-be-in-a-separate-file-or-service---

**Contents:**
- Interoperability between LangChain (Python) and LangSmith SDK

@chain
def parent_chain(inputs):
    rt = get_current_run_tree()
    headers = rt.to_headers()
    # ... make a request to another service with the headers
    # The headers should be passed to the other service, eventually to the child_wrapper function

parent_chain.invoke({"test": 1})
python  theme={null}
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langsmith import traceable

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Please respond to the user's request only based on the given context."),
    ("user", "Question: {question}\nContext: {context}")
])

model = ChatOpenAI(model="gpt-4o-mini")
output_parser = StrOutputParser()
chain = prompt | model | output_parser

**Examples:**

Example 1 (unknown):
```unknown
## Interoperability between LangChain (Python) and LangSmith SDK

If you are using LangChain for part of your application and the LangSmith SDK (see [this guide](/langsmith/annotate-code)) for other parts, you can still trace the entire application seamlessly.

LangChain objects will be traced when invoked within a `traceable` function and be bound as a child run of the `traceable` function.
```

---
