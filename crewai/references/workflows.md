# Crewai - Workflows

**Pages:** 8

---

## Efficient model for data processing

**URL:** llms-txt#efficient-model-for-data-processing

**Contents:**
  - b. Component-Specific Selection
- Task Definition Framework
  - a. Focus on Clarity Over Complexity
  - b. Task Sequencing Strategy
- Optimizing Agent Configuration for LLM Performance
  - a. Role-Driven LLM Selection

processing_llm = LLM(model="gpt-4o-mini", temperature=0)

research_manager = Agent(
    role="Research Strategy Manager",
    goal="Develop comprehensive research strategies and coordinate team efforts",
    backstory="Expert research strategist with deep analytical capabilities",
    llm=manager_llm,  # High-capability model for complex reasoning
    verbose=True
)

content_writer = Agent(
    role="Research Content Writer",
    goal="Transform research findings into compelling, well-structured reports",
    backstory="Skilled writer who excels at making complex topics accessible",
    llm=content_llm,  # Creative model for engaging content
    verbose=True
)

data_processor = Agent(
    role="Data Analysis Specialist",
    goal="Extract and organize key data points from research sources",
    backstory="Detail-oriented analyst focused on accuracy and efficiency",
    llm=processing_llm,  # Fast, cost-effective model for routine tasks
    verbose=True
)

crew = Crew(
    agents=[research_manager, content_writer, data_processor],
    tasks=[...],  # Your specific tasks
    manager_llm=manager_llm,  # Manager uses the reasoning model
    verbose=True
)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
The key to successful multi-model implementation is understanding how different agents interact and ensuring that model capabilities align with agent responsibilities. This requires careful planning but can result in significant improvements in both output quality and operational efficiency.

### b. Component-Specific Selection

<Tabs>
  <Tab title="Manager LLM">
    The manager LLM plays a crucial role in hierarchical CrewAI processes, serving as the coordination point for multiple agents and tasks. This model needs to excel at delegation, task prioritization, and maintaining context across multiple concurrent operations.

    Effective manager LLMs require strong reasoning capabilities to make good delegation decisions, consistent performance to ensure predictable coordination, and excellent context management to track the state of multiple agents simultaneously. The model needs to understand the capabilities and limitations of different agents while optimizing task allocation for efficiency and quality.

    Cost considerations are particularly important for manager LLMs since they're involved in every operation. The model needs to provide sufficient capability for effective coordination while remaining cost-effective for frequent use. This often means finding models that offer good reasoning capabilities without the premium pricing of the most sophisticated options.
  </Tab>

  <Tab title="Function Calling LLM">
    Function calling LLMs handle tool usage across all agents, making them critical for crews that rely heavily on external tools and APIs. These models need to excel at understanding tool capabilities, extracting parameters accurately, and handling tool responses effectively.

    The most important characteristics for function calling LLMs are precision and reliability rather than creativity or sophisticated reasoning. The model needs to consistently extract the correct parameters from natural language requests and handle tool responses appropriately. Speed is also important since tool usage often involves multiple round trips that can impact overall performance.

    Many teams find that specialized function calling models or general purpose models with strong tool support work better than creative or reasoning-focused models for this role. The key is ensuring that the model can reliably bridge the gap between natural language instructions and structured tool calls.
  </Tab>

  <Tab title="Agent-Specific Overrides">
    Individual agents can override crew-level LLM settings when their specific needs differ significantly from the general crew requirements. This capability allows for fine-tuned optimization while maintaining operational simplicity for most agents.

    Consider agent-specific overrides when an agent's role requires capabilities that differ substantially from other crew members. For example, a creative writing agent might benefit from a model optimized for content generation, while a data analysis agent might perform better with a reasoning-focused model.

    The challenge with agent-specific overrides is balancing optimization with operational complexity. Each additional model adds complexity to deployment, monitoring, and cost management. Teams should focus overrides on agents where the performance improvement justifies the additional complexity.
  </Tab>
</Tabs>

## Task Definition Framework

### a. Focus on Clarity Over Complexity

Effective task definition is often more important than model selection in determining the quality of CrewAI outputs. Well-defined tasks provide clear direction and context that enable even modest models to perform well, while poorly defined tasks can cause even sophisticated models to produce unsatisfactory results.

<AccordionGroup>
  <Accordion title="Effective Task Descriptions" icon="list-check">
    The best task descriptions strike a balance between providing sufficient detail and maintaining clarity. They should define the specific objective clearly enough that there's no ambiguity about what success looks like, while explaining the approach or methodology in enough detail that the agent understands how to proceed.

    Effective task descriptions include relevant context and constraints that help the agent understand the broader purpose and any limitations they need to work within. They break complex work into focused steps that can be executed systematically, rather than presenting overwhelming, multi-faceted objectives that are difficult to approach systematically.

    Common mistakes include being too vague about objectives, failing to provide necessary context, setting unclear success criteria, or combining multiple unrelated tasks into a single description. The goal is to provide enough information for the agent to succeed while maintaining focus on a single, clear objective.
  </Accordion>

  <Accordion title="Expected Output Guidelines" icon="bullseye">
    Expected output guidelines serve as a contract between the task definition and the agent, clearly specifying what the deliverable should look like and how it will be evaluated. These guidelines should describe both the format and structure needed, as well as the key elements that must be included for the output to be considered complete.

    The best output guidelines provide concrete examples of quality indicators and define completion criteria clearly enough that both the agent and human reviewers can assess whether the task has been completed successfully. This reduces ambiguity and helps ensure consistent results across multiple task executions.

    Avoid generic output descriptions that could apply to any task, missing format specifications that leave agents guessing about structure, unclear quality standards that make evaluation difficult, or failing to provide examples or templates that help agents understand expectations.
  </Accordion>
</AccordionGroup>

### b. Task Sequencing Strategy

<Tabs>
  <Tab title="Sequential Dependencies">
    Sequential task dependencies are essential when tasks build upon previous outputs, information flows from one task to another, or quality depends on the completion of prerequisite work. This approach ensures that each task has access to the information and context it needs to succeed.

    Implementing sequential dependencies effectively requires using the context parameter to chain related tasks, building complexity gradually through task progression, and ensuring that each task produces outputs that serve as meaningful inputs for subsequent tasks. The goal is to maintain logical flow between dependent tasks while avoiding unnecessary bottlenecks.

    Sequential dependencies work best when there's a clear logical progression from one task to another and when the output of one task genuinely improves the quality or feasibility of subsequent tasks. However, they can create bottlenecks if not managed carefully, so it's important to identify which dependencies are truly necessary versus those that are merely convenient.
  </Tab>

  <Tab title="Parallel Execution">
    Parallel execution becomes valuable when tasks are independent of each other, time efficiency is important, or different expertise areas are involved that don't require coordination. This approach can significantly reduce overall execution time while allowing specialized agents to work on their areas of strength simultaneously.

    Successful parallel execution requires identifying tasks that can truly run independently, grouping related but separate work streams effectively, and planning for result integration when parallel tasks need to be combined into a final deliverable. The key is ensuring that parallel tasks don't create conflicts or redundancies that reduce overall quality.

    Consider parallel execution when you have multiple independent research streams, different types of analysis that don't depend on each other, or content creation tasks that can be developed simultaneously. However, be mindful of resource allocation and ensure that parallel execution doesn't overwhelm your available model capacity or budget.
  </Tab>
</Tabs>

## Optimizing Agent Configuration for LLM Performance

### a. Role-Driven LLM Selection

<Warning>
  Generic agent roles make it impossible to select the right LLM. Specific roles enable targeted model optimization.
</Warning>

The specificity of your agent roles directly determines which LLM capabilities matter most for optimal performance. This creates a strategic opportunity to match precise model strengths with agent responsibilities.

**Generic vs. Specific Role Impact on LLM Choice:**

When defining roles, think about the specific domain knowledge, working style, and decision-making frameworks that would be most valuable for the tasks the agent will handle. The more specific and contextual the role definition, the better the model can embody that role effectively.
```

---

## Example: Customer Support Flow with structured processing

**URL:** llms-txt#example:-customer-support-flow-with-structured-processing

from crewai.flow.flow import Flow, listen, router, start
from pydantic import BaseModel
from typing import List, Dict

---

## HITL Workflows

**URL:** llms-txt#hitl-workflows

**Contents:**
- Setting Up HITL Workflows
- Best Practices
- Common Use Cases

Source: https://docs.crewai.com/en/enterprise/guides/human-in-the-loop

Learn how to implement Human-In-The-Loop workflows in CrewAI for enhanced decision-making

Human-In-The-Loop (HITL) is a powerful approach that combines artificial intelligence with human expertise to enhance decision-making and improve task outcomes. This guide shows you how to implement HITL within CrewAI.

## Setting Up HITL Workflows

<Steps>
  <Step title="Configure Your Task">
    Set up your task with human input enabled:

<Frame>
      <img alt="Crew Human Input" />
    </Frame>
  </Step>

<Step title="Provide Webhook URL">
    When kicking off your crew, include a webhook URL for human input:

<Frame>
      <img alt="Crew Webhook URL" />
    </Frame>
  </Step>

<Step title="Receive Webhook Notification">
    Once the crew completes the task requiring human input, you'll receive a webhook notification containing:

* **Execution ID**
    * **Task ID**
    * **Task output**
  </Step>

<Step title="Review Task Output">
    The system will pause in the `Pending Human Input` state. Review the task output carefully.
  </Step>

<Step title="Submit Human Feedback">
    Call the resume endpoint of your crew with the following information:

<Frame>
      <img alt="Crew Resume Endpoint" />
    </Frame>

<Warning>
      **Critical: Webhook URLs Must Be Provided Again**:
      You **must** provide the same webhook URLs (`taskWebhookUrl`, `stepWebhookUrl`, `crewWebhookUrl`) in the resume call that you used in the kickoff call. Webhook configurations are **NOT** automatically carried over from kickoff - they must be explicitly included in the resume request to continue receiving notifications for task completion, agent steps, and crew completion.
    </Warning>

Example resume call with webhooks:

<Warning>
      **Feedback Impact on Task Execution**:
      It's crucial to exercise care when providing feedback, as the entire feedback content will be incorporated as additional context for further task executions.
    </Warning>

* All information in your feedback becomes part of the task's context.
    * Irrelevant details may negatively influence it.
    * Concise, relevant feedback helps maintain task focus and efficiency.
    * Always review your feedback carefully before submission to ensure it contains only pertinent information that will positively guide the task's execution.
  </Step>

<Step title="Handle Negative Feedback">
    If you provide negative feedback:

* The crew will retry the task with added context from your feedback.
    * You'll receive another webhook notification for further review.
    * Repeat steps 4-6 until satisfied.
  </Step>

<Step title="Execution Continuation">
    When you submit positive feedback, the execution will proceed to the next steps.
  </Step>
</Steps>

* **Be Specific**: Provide clear, actionable feedback that directly addresses the task at hand
* **Stay Relevant**: Only include information that will help improve the task execution
* **Be Timely**: Respond to HITL prompts promptly to avoid workflow delays
* **Review Carefully**: Double-check your feedback before submitting to ensure accuracy

HITL workflows are particularly valuable for:

* Quality assurance and validation
* Complex decision-making scenarios
* Sensitive or high-stakes operations
* Creative tasks requiring human judgment
* Compliance and regulatory reviews

---

## Human-in-the-Loop (HITL) Workflows

**URL:** llms-txt#human-in-the-loop-(hitl)-workflows

**Contents:**
- Choosing Your HITL Approach
- Setting Up Webhook-Based HITL Workflows
- Best Practices
- Common Use Cases

Source: https://docs.crewai.com/en/learn/human-in-the-loop

Learn how to implement Human-in-the-Loop workflows in CrewAI for enhanced decision-making

Human-in-the-Loop (HITL) is a powerful approach that combines artificial intelligence with human expertise to enhance decision-making and improve task outcomes. CrewAI provides multiple ways to implement HITL depending on your needs.

## Choosing Your HITL Approach

CrewAI offers two main approaches for implementing human-in-the-loop workflows:

| Approach                                     | Best For                                                                            | Integration                                                  |
| -------------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| **Flow-based** (`@human_feedback` decorator) | Local development, console-based review, synchronous workflows                      | [Human Feedback in Flows](/en/learn/human-feedback-in-flows) |
| **Webhook-based** (Enterprise)               | Production deployments, async workflows, external integrations (Slack, Teams, etc.) | This guide                                                   |

<Tip>
  If you're building flows and want to add human review steps with routing based on feedback, check out the [Human Feedback in Flows](/en/learn/human-feedback-in-flows) guide for the `@human_feedback` decorator.
</Tip>

## Setting Up Webhook-Based HITL Workflows

<Steps>
  <Step title="Configure Your Task">
    Set up your task with human input enabled:

<Frame>
      <img alt="Crew Human Input" />
    </Frame>
  </Step>

<Step title="Provide Webhook URL">
    When kicking off your crew, include a webhook URL for human input:

<Frame>
      <img alt="Crew Webhook URL" />
    </Frame>

Example with Bearer authentication:

Or with Basic authentication:

<Step title="Receive Webhook Notification">
    Once the crew completes the task requiring human input, you'll receive a webhook notification containing:

* Execution ID
    * Task ID
    * Task output
  </Step>

<Step title="Review Task Output">
    The system will pause in the `Pending Human Input` state. Review the task output carefully.
  </Step>

<Step title="Submit Human Feedback">
    Call the resume endpoint of your crew with the following information:

<Frame>
      <img alt="Crew Resume Endpoint" />
    </Frame>

<Warning>
      **Critical: Webhook URLs Must Be Provided Again**:
      You **must** provide the same webhook URLs (`taskWebhookUrl`, `stepWebhookUrl`, `crewWebhookUrl`) in the resume call that you used in the kickoff call. Webhook configurations are **NOT** automatically carried over from kickoff - they must be explicitly included in the resume request to continue receiving notifications for task completion, agent steps, and crew completion.
    </Warning>

Example resume call with webhooks:

<Warning>
      **Feedback Impact on Task Execution**:
      It's crucial to exercise care when providing feedback, as the entire feedback content will be incorporated as additional context for further task executions.
    </Warning>

* All information in your feedback becomes part of the task's context.
    * Irrelevant details may negatively influence it.
    * Concise, relevant feedback helps maintain task focus and efficiency.
    * Always review your feedback carefully before submission to ensure it contains only pertinent information that will positively guide the task's execution.
  </Step>

<Step title="Handle Negative Feedback">
    If you provide negative feedback:

* The crew will retry the task with added context from your feedback.
    * You'll receive another webhook notification for further review.
    * Repeat steps 4-6 until satisfied.
  </Step>

<Step title="Execution Continuation">
    When you submit positive feedback, the execution will proceed to the next steps.
  </Step>
</Steps>

* **Be Specific**: Provide clear, actionable feedback that directly addresses the task at hand
* **Stay Relevant**: Only include information that will help improve the task execution
* **Be Timely**: Respond to HITL prompts promptly to avoid workflow delays
* **Review Carefully**: Double-check your feedback before submitting to ensure accuracy

HITL workflows are particularly valuable for:

* Quality assurance and validation
* Complex decision-making scenarios
* Sensitive or high-stakes operations
* Creative tasks requiring human judgment
* Compliance and regulatory reviews

**Examples:**

Example 1 (unknown):
```unknown
Or with Basic authentication:
```

Example 2 (unknown):
```unknown
</Step>

  <Step title="Receive Webhook Notification">
    Once the crew completes the task requiring human input, you'll receive a webhook notification containing:

    * Execution ID
    * Task ID
    * Task output
  </Step>

  <Step title="Review Task Output">
    The system will pause in the `Pending Human Input` state. Review the task output carefully.
  </Step>

  <Step title="Submit Human Feedback">
    Call the resume endpoint of your crew with the following information:

    <Frame>
      <img alt="Crew Resume Endpoint" />
    </Frame>

    <Warning>
      **Critical: Webhook URLs Must Be Provided Again**:
      You **must** provide the same webhook URLs (`taskWebhookUrl`, `stepWebhookUrl`, `crewWebhookUrl`) in the resume call that you used in the kickoff call. Webhook configurations are **NOT** automatically carried over from kickoff - they must be explicitly included in the resume request to continue receiving notifications for task completion, agent steps, and crew completion.
    </Warning>

    Example resume call with webhooks:
```

---

## Perfect for document processing

**URL:** llms-txt#perfect-for-document-processing

document_processor = Agent(
    role="Document Analyst",
    goal="Extract insights from large research papers",
    backstory="Expert at analyzing extensive documentation",
    respect_context_window=True,  # Handle large documents gracefully
    max_iter=50,  # Allow more iterations for complex analysis
    verbose=True
)
python Code theme={null}

**Examples:**

Example 1 (unknown):
```unknown
#### Use `respect_context_window=False` when:

* **Precision is critical** and information loss is unacceptable
* **Legal or medical tasks** requiring complete context
* **Code review** where missing details could introduce bugs
* **Financial analysis** where accuracy is paramount
```

---

## Process and inspect chunks

**URL:** llms-txt#process-and-inspect-chunks

**Contents:**
  - Common Knowledge Storage Issues

test_source.add()
print(f"Number of chunks created: {len(test_source.chunks)}")
for i, chunk in enumerate(test_source.chunks[:3]):  # Show first 3 chunks
    print(f"Chunk {i+1}: {chunk[:50]}...")
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### Common Knowledge Storage Issues

**"File not found" errors:**
```

---

## Webhook Automation

**URL:** llms-txt#webhook-automation

**Contents:**
- Setting Up Webhooks
- Webhook Output Examples

Source: https://docs.crewai.com/en/enterprise/guides/webhook-automation

Automate CrewAI AOP workflows using webhooks with platforms like ActivePieces, Zapier, and Make.com

CrewAI AOP allows you to automate your workflow using webhooks. This article will guide you through the process of setting up and using webhooks to kickoff your crew execution, with a focus on integration with ActivePieces, a workflow automation platform similar to Zapier and Make.com.

## Setting Up Webhooks

<Steps>
  <Step title="Accessing the Kickoff Interface">
    * Navigate to the CrewAI AOP dashboard
    * Look for the `/kickoff` section, which is used to start the crew execution
      <Frame>
        <img alt="Kickoff Interface" />
      </Frame>
  </Step>

<Step title="Configuring the JSON Content">
    In the JSON Content section, you'll need to provide the following information:

* **inputs**: A JSON object containing:
      * `company`: The name of the company (e.g., "tesla")
      * `product_name`: The name of the product (e.g., "crewai")
      * `form_response`: The type of response (e.g., "financial")
      * `icp_description`: A brief description of the Ideal Customer Profile
      * `product_description`: A short description of the product
      * `taskWebhookUrl`, `stepWebhookUrl`, `crewWebhookUrl`: URLs for various webhook endpoints (ActivePieces, Zapier, Make.com or another compatible platform)
  </Step>

<Step title="Integrating with ActivePieces">
    In this example we will be using ActivePieces. You can use other platforms such as Zapier and Make.com

To integrate with ActivePieces:

1. Set up a new flow in ActivePieces

2. Add a trigger (e.g., `Every Day` schedule)
       <Frame>
         <img alt="ActivePieces Trigger" />
       </Frame>

3. Add an HTTP action step
       * Set the action to `Send HTTP request`

* Use `POST` as the method

* Set the URL to your CrewAI AOP kickoff endpoint

* Add necessary headers (e.g., `Bearer Token`)
         <Frame>
           <img alt="ActivePieces Headers" />
         </Frame>

* In the body, include the JSON content as configured in step 2
         <Frame>
           <img alt="ActivePieces Body" />
         </Frame>

* The crew will then kickoff at the pre-defined time.
  </Step>

<Step title="Setting Up the Webhook">
    1. Create a new flow in ActivePieces and name it
       <Frame>
         <img alt="ActivePieces Flow" />
       </Frame>

2. Add a webhook step as the trigger:
       * Select `Catch Webhook` as the trigger type

* This will generate a unique URL that will receive HTTP requests and trigger your flow
         <Frame>
           <img alt="ActivePieces Webhook" />
         </Frame>

* Configure the email to use crew webhook body text
         <Frame>
           <img alt="ActivePieces Email" />
         </Frame>
  </Step>
</Steps>

## Webhook Output Examples

**Note:** Any `meta` object provided in your kickoff request will be included in all webhook payloads, allowing you to track requests and maintain context across the entire crew execution lifecycle.

<Tabs>
  <Tab title="Step Webhook">
    `stepWebhookUrl` - Callback that will be executed upon each agent inner thought

<Tab title="Task Webhook">
    `taskWebhookUrl` - Callback that will be executed upon the end of each task

<Tab title="Crew Webhook">
    `crewWebhookUrl` - Callback that will be executed upon the end of the crew execution

**Examples:**

Example 1 (unknown):
```unknown
</Tab>

  <Tab title="Task Webhook">
    `taskWebhookUrl` - Callback that will be executed upon the end of each task
```

Example 2 (unknown):
```unknown
</Tab>

  <Tab title="Crew Webhook">
    `crewWebhookUrl` - Callback that will be executed upon the end of the crew execution
```

---

## ❌ Vague descriptions that don't guide collaboration

**URL:** llms-txt#❌-vague-descriptions-that-don't-guide-collaboration

**Contents:**
- Troubleshooting Collaboration
  - Issue: Agents Not Collaborating

Task(description="Do some research about chatbots", ...)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## Troubleshooting Collaboration

### Issue: Agents Not Collaborating

**Symptoms:** Agents work in isolation, no delegation occurs
```

---
