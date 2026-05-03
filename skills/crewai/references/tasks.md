# Crewai - Tasks

**Pages:** 100

---

## Accessing the task output

**URL:** llms-txt#accessing-the-task-output

**Contents:**
- Markdown Output Formatting
  - Using Markdown Formatting

task_output = task.output

print(f"Task Description: {task_output.description}")
print(f"Task Summary: {task_output.summary}")
print(f"Raw Output: {task_output.raw}")
if task_output.json_dict:
    print(f"JSON Output: {json.dumps(task_output.json_dict, indent=2)}")
if task_output.pydantic:
    print(f"Pydantic Output: {task_output.pydantic}")
python Code theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## Markdown Output Formatting

The `markdown` parameter enables automatic markdown formatting for task outputs. When set to `True`, the task will instruct the agent to format the final answer using proper Markdown syntax.

### Using Markdown Formatting
```

---

## Alternative: Break tasks into smaller pieces

**URL:** llms-txt#alternative:-break-tasks-into-smaller-pieces

---

## Basic usage - will use task's expected_output as context

**URL:** llms-txt#basic-usage---will-use-task's-expected_output-as-context

guardrail = HallucinationGuardrail(
    llm=LLM(model="gpt-4o-mini")
)

---

## Complex automation task

**URL:** llms-txt#complex-automation-task

**Contents:**
  - Financial Modeling and Analysis

automation_task = Task(
    description="""
    1. Scan all Excel workbooks for specific data patterns
    2. Create consolidated reports from multiple workbooks
    3. Generate charts and tables for trend analysis
    4. Set up named ranges for easy data reference
    5. Create dashboard worksheets with key metrics
    6. Clean up unused worksheets and tables
    """,
    agent=excel_automator,
    expected_output="Automated Excel workflow completed with consolidated reports and dashboards"
)

crew = Crew(
    agents=[excel_automator],
    tasks=[automation_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

financial_modeler = Agent(
    role="Financial Modeler",
    goal="Create financial models and analysis in Excel",
    backstory="An AI assistant specialized in financial modeling and analysis using Excel.",
    apps=['microsoft_excel']
)

**Examples:**

Example 1 (unknown):
```unknown
### Financial Modeling and Analysis
```

---

## Complex contact management task

**URL:** llms-txt#complex-contact-management-task

**Contents:**
- Troubleshooting
  - Common Issues
  - Getting Help

comprehensive_task = Task(
    description="""
    1. Retrieve contacts from all sources (personal, directory, other)
    2. Search for duplicate contacts and merge information
    3. Update outdated contact information
    4. Create missing contacts for important stakeholders
    5. Organize contacts into meaningful groups
    6. Generate a comprehensive contact report
    """,
    agent=contact_specialist,
    expected_output="Complete contact management performed with unified contact database and detailed report"
)

crew = Crew(
    agents=[contact_specialist],
    tasks=[comprehensive_task]
)

**Permission Errors**

* Ensure your Google account has appropriate permissions for contacts access
* Verify that the OAuth connection includes required scopes for Google Contacts API
* Check that directory access permissions are granted for organization contacts

**Resource Name Format Issues**

* Ensure resource names follow the correct format (e.g., 'people/c123456789' for contacts)
* Verify that contact group resource names use the format 'contactGroups/groupId'
* Check that resource names exist and are accessible

**Search and Query Issues**

* Ensure search queries are properly formatted and not empty
* Use appropriate readMask fields for the data you need
* Verify that search sources are correctly specified (contacts vs profiles)

**Contact Creation and Updates**

* Ensure required fields are provided when creating contacts
* Verify that email addresses and phone numbers are properly formatted
* Check that updatePersonFields parameter includes all fields being updated

**Directory Access Issues**

* Ensure you have appropriate permissions to access organization directory
* Verify that directory sources are correctly specified
* Check that your organization allows API access to directory information

**Pagination and Limits**

* Be mindful of page size limits (varies by endpoint)
* Use pageToken for pagination through large result sets
* Respect API rate limits and implement appropriate delays

**Contact Groups and Organization**

* Ensure contact group names are unique when creating new groups
* Verify that contacts exist before adding them to groups
* Check that you have permissions to modify contact groups

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with Google Contacts integration setup or troubleshooting.
</Card>

---

## Complex presentation automation task

**URL:** llms-txt#complex-presentation-automation-task

**Contents:**
  - Template and Content Creation

automation_task = Task(
    description="""
    1. Create multiple presentations for different departments
    2. Import relevant data from various spreadsheets
    3. Update existing presentations with new content
    4. Generate thumbnails for all presentations
    5. Link supporting documents from Drive
    6. Create a master index presentation with links to all others
    """,
    agent=presentation_automator,
    expected_output="Automated presentation workflow completed with multiple presentations and organized structure"
)

crew = Crew(
    agents=[presentation_automator],
    tasks=[automation_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

template_creator = Agent(
    role="Template Creator",
    goal="Create presentation templates and standardized content",
    backstory="An AI assistant that creates consistent presentation templates and content standards.",
    apps=['google_slides']
)

**Examples:**

Example 1 (unknown):
```unknown
### Template and Content Creation
```

---

## Complex scheduling automation task

**URL:** llms-txt#complex-scheduling-automation-task

**Contents:**
- Troubleshooting
  - Common Issues
  - Getting Help

automation_task = Task(
    description="""
    1. List all upcoming events for the next two weeks
    2. Identify any scheduling conflicts or back-to-back meetings
    3. Suggest optimal meeting times by checking availability
    4. Create buffer time between meetings where needed
    5. Update event descriptions with agenda items and meeting links
    """,
    agent=scheduling_automator,
    expected_output="Calendar optimized with resolved conflicts, buffer times, and updated meeting details"
)

crew = Crew(
    agents=[scheduling_automator],
    tasks=[automation_task]
)

**Authentication Errors**

* Ensure your Google account has the necessary permissions for calendar access
* Verify that the OAuth connection includes all required scopes for Google Calendar API
* Check if calendar sharing settings allow the required access level

**Event Creation Issues**

* Verify that time formats are correct (RFC3339 format)
* Ensure attendee email addresses are properly formatted
* Check that the target calendar exists and is accessible
* Verify time zones are correctly specified

**Availability and Time Conflicts**

* Use proper RFC3339 format for time ranges when checking availability
* Ensure time zones are consistent across all operations
* Verify that calendar IDs are correct when checking multiple calendars

**Event Updates and Deletions**

* Verify that event IDs are correct and events exist
* Ensure you have edit permissions for the events
* Check that calendar ownership allows modifications

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with Google Calendar integration setup or troubleshooting.
</Card>

---

## Complex task involving multiple Google Drive operations

**URL:** llms-txt#complex-task-involving-multiple-google-drive-operations

organization_task = Task(
    description="""
    1. List all files in the shared folder
    2. Create folders for different document types (Reports, Presentations, Spreadsheets)
    3. Move files to appropriate folders based on their type
    4. Set appropriate sharing permissions for each folder
    5. Create a summary document of the organization changes
    """,
    agent=file_organizer,
    expected_output="Files organized into categorized folders with proper permissions and summary report"
)

crew = Crew(
    agents=[file_organizer],
    tasks=[organization_task]
)

---

## Complex workflow automation task

**URL:** llms-txt#complex-workflow-automation-task

**Contents:**
  - Data Integration and Reporting

automation_task = Task(
    description="""
    1. Monitor project lists across multiple sites
    2. Create status reports based on list data
    3. Upload reports to designated document libraries
    4. Update project tracking lists with completion status
    5. Archive completed project documents
    6. Send notifications for overdue items
    """,
    agent=workflow_automator,
    expected_output="Automated workflow completed with status reports generated and project tracking updated"
)

crew = Crew(
    agents=[workflow_automator],
    tasks=[automation_task]
)

crew.kickoff()
python theme={null}
from crewai import Agent, Task, Crew

data_integrator = Agent(
    role="Data Integrator",
    goal="Integrate and analyze data across SharePoint sites and lists",
    backstory="An AI assistant that specializes in data integration and cross-site analysis.",
    apps=['microsoft_sharepoint']
)

**Examples:**

Example 1 (unknown):
```unknown
### Data Integration and Reporting
```

---

## Continue with additional focused tasks...

**URL:** llms-txt#continue-with-additional-focused-tasks...

**Contents:**
  - 3. Misaligned Description and Expected Output
  - 4. Not Understanding the Process Yourself
  - 5. Premature Use of Hierarchical Structures
  - 6. Vague or Generic Agent Definitions
- Advanced Agent Design Strategies
  - Designing for Collaboration

yaml theme={null}
analysis_task:
  description: "Analyze customer feedback to find areas of improvement."
  expected_output: "A marketing plan for the next quarter."
yaml theme={null}
analysis_task:
  description: "Analyze customer feedback to identify the top 3 areas for product improvement."
  expected_output: "A report listing the 3 priority improvement areas with supporting customer quotes and data points."
yaml theme={null}
agent:
  role: "Business Analyst"
  goal: "Analyze business data"
  backstory: "You are good at business analysis."
yaml theme={null}
agent:
  role: "SaaS Metrics Specialist focusing on growth-stage startups"
  goal: "Identify actionable insights from business data that can directly impact customer retention and revenue growth"
  backstory: "With 10+ years analyzing SaaS business models, you've developed a keen eye for the metrics that truly matter for sustainable growth. You've helped numerous companies identify the leverage points that turned around their business trajectory. You believe in connecting data to specific, actionable recommendations rather than general observations."
yaml theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### 3. Misaligned Description and Expected Output

**Problem:** The task description asks for one thing while the expected output specifies something different.

**Example of Poor Design:**
```

Example 2 (unknown):
```unknown
**Improved Version:**
```

Example 3 (unknown):
```unknown
### 4. Not Understanding the Process Yourself

**Problem:** Asking agents to execute tasks that you yourself don't fully understand.

**Solution:**

1. Try to perform the task manually first
2. Document your process, decision points, and information sources
3. Use this documentation as the basis for your task description

### 5. Premature Use of Hierarchical Structures

**Problem:** Creating unnecessarily complex agent hierarchies where sequential processes would work better.

**Solution:** Start with sequential processes and only move to hierarchical models when the workflow complexity truly requires it.

### 6. Vague or Generic Agent Definitions

**Problem:** Generic agent definitions lead to generic outputs.

**Example of Poor Design:**
```

Example 4 (unknown):
```unknown
**Improved Version:**
```

---

## Create a sample task

**URL:** llms-txt#create-a-sample-task

task = Task(
    description="Analyze the sales data and identify trends",
    expected_output="A detailed analysis with key insights and trends",
    agent=agent
)

---

## Create a task

**URL:** llms-txt#create-a-task

task = Task(
    description="Research the given topic and provide a comprehensive summary",
    agent=researcher,
    expected_output="Detailed research summary with key findings"
)

---

## Create a task for image analysis

**URL:** llms-txt#create-a-task-for-image-analysis

task = Task(
    description="Analyze the product image at https://example.com/product.jpg and provide a detailed description",
    expected_output="A detailed description of the product image",
    agent=image_analyst
)

---

## Create a task that encourages collaboration

**URL:** llms-txt#create-a-task-that-encourages-collaboration

article_task = Task(
    description="""Write a comprehensive 1000-word article about 'The Future of AI in Healthcare'.
    
    The article should include:
    - Current AI applications in healthcare
    - Emerging trends and technologies  
    - Potential challenges and ethical considerations
    - Expert predictions for the next 5 years
    
    Collaborate with your teammates to ensure accuracy and quality.""",
    expected_output="A well-researched, engaging 1000-word article with proper structure and citations",
    agent=writer  # Writer leads, but can delegate research to researcher
)

---

## Create a task that includes error handling instructions

**URL:** llms-txt#create-a-task-that-includes-error-handling-instructions

**Contents:**
- Rate Limiting
- Implementation Details
- Conclusion

robust_extract_task = Task(
    description="""
    Extract the main heading from example.com.
    Be aware that you might encounter errors such as:
    - Invalid URL format
    - Missing API key
    - Rate limit exceeded
    - Network or API errors
    
    If you encounter any errors, provide a clear explanation of what went wrong
    and suggest possible solutions.
    """,
    expected_output="Either the extracted heading or a clear error explanation",
    agent=web_scraper_agent,
)
python Code theme={null}
class ScrapegraphScrapeTool(BaseTool):
    """
    A tool that uses Scrapegraph AI to intelligently scrape website content.
    """
    
    # Implementation details...
    
    def _run(self, **kwargs: Any) -> Any:
        website_url = kwargs.get("website_url", self.website_url)
        user_prompt = (
            kwargs.get("user_prompt", self.user_prompt)
            or "Extract the main content of the webpage"
        )

if not website_url:
            raise ValueError("website_url is required")

# Validate URL format
        self._validate_url(website_url)

try:
            # Make the SmartScraper request
            response = self._client.smartscraper(
                website_url=website_url,
                user_prompt=user_prompt,
            )

return response
        # Error handling...
```

The `ScrapegraphScrapeTool` provides a powerful way to extract content from websites using AI-powered understanding of web page structure. By enabling agents to target specific information using natural language prompts, it makes web scraping tasks more efficient and focused. This tool is particularly useful for data extraction, content monitoring, and research tasks where specific information needs to be extracted from web pages.

**Examples:**

Example 1 (unknown):
```unknown
## Rate Limiting

The Scrapegraph API has rate limits that vary based on your subscription plan. Consider the following best practices:

* Implement appropriate delays between requests when processing multiple URLs.
* Handle rate limit errors gracefully in your application.
* Check your API plan limits on the Scrapegraph dashboard.

## Implementation Details

The `ScrapegraphScrapeTool` uses the Scrapegraph Python client to interact with the SmartScraper API:
```

---

## Create a task that requires code execution

**URL:** llms-txt#create-a-task-that-requires-code-execution

data_analysis_task = Task(
    description="Analyze the given dataset and calculate the average age of participants. Ages: {ages}",
    agent=coding_agent,
    expected_output="The average age calculated from the dataset"
)

---

## Create a task with more specific instructions

**URL:** llms-txt#create-a-task-with-more-specific-instructions

**Contents:**
- Error Handling

advanced_scrape_task = Task(
    description="""
    Extract content from example.com with the following requirements:
    - Convert the content to plain text format
    - Enable JavaScript rendering
    - Use a US-based proxy
    - Handle any scraping failures gracefully
    """,
    expected_output="The extracted content from example.com",
    agent=web_scraper_agent,
)
python Code theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## Error Handling

By default, the `ScrapflyScrapeWebsiteTool` will raise an exception if scraping fails. Agents can be instructed to handle failures gracefully by specifying the `ignore_scrape_failures` parameter:
```

---

## Create a task with specific analysis requirements

**URL:** llms-txt#create-a-task-with-specific-analysis-requirements

inspection_task = Task(
    description="""
    Analyze the product image at https://example.com/product.jpg with focus on:
    1. Quality of materials
    2. Manufacturing defects
    3. Compliance with standards
    Provide a detailed report highlighting any issues found.
    """,
    expected_output="A detailed report highlighting any issues found",
    agent=expert_analyst
)

---

## Create sequential tasks

**URL:** llms-txt#create-sequential-tasks

review_task = Task(
    description="Review all open pull requests in the 'api-service' repository and identify any that need attention.",
    agent=code_reviewer,
    expected_output="List of pull requests that need review or have issues"
)

update_task = Task(
    description="Update Linear issues based on the pull request review findings. Mark completed PRs as done.",
    agent=task_manager,
    expected_output="Summary of updated Linear issues"
)

notify_task = Task(
    description="Post a summary of today's code review and task updates to the #engineering Slack channel.",
    agent=communicator,
    expected_output="Confirmation that the message was posted"
)

---

## Create tasks

**URL:** llms-txt#create-tasks

research_task = Task(
    description="Find all available AWS services in us-west-2 region.",
    agent=researcher
)

analysis_task = Task(
    description="Analyze which services support IPv6 and their implementation requirements.",
    agent=analyst
)

summary_task = Task(
    description="Create a summary of IPv6-compatible services and their key features.",
    agent=summarizer
)

---

## Create task

**URL:** llms-txt#create-task

research_task = Task(
    description="Research the latest developments in AI agent frameworks",
    expected_output="Comprehensive research report with citations",
    agent=research_agent
)

---

## Create your task with the guardrail

**URL:** llms-txt#create-your-task-with-the-guardrail

**Contents:**
- Advanced Configuration
  - Custom Threshold Validation

task = Task(
    description="Write a summary about AI capabilities",
    expected_output="A factual summary based on the provided context",
    agent=my_agent,
    guardrail=guardrail  # Add the guardrail to validate output
)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## Advanced Configuration

### Custom Threshold Validation

For stricter validation, you can set a custom faithfulness threshold (0-10 scale):
```

---

## Define a condition function for the conditional task

**URL:** llms-txt#define-a-condition-function-for-the-conditional-task

---

## Define a sample task

**URL:** llms-txt#define-a-sample-task

engineering_task = Task(
    description="Review AI implementation files for potential improvements",
    expected_output="A summary of key findings and recommendations",
    agent=principal_engineer
)

---

## Define tasks

**URL:** llms-txt#define-tasks

search_task = Task(
    description="""Search for relevant documents about the {query}.
    Your final answer should include:
    - The relevant information found
    - The similarity scores of the results
    - The metadata of the relevant documents""",
    agent=search_agent
)

answer_task = Task(
    description="""Given the context and metadata of relevant documents,
    generate a final answer based on the context.""",
    agent=answer_agent
)

---

## Define their tasks

**URL:** llms-txt#define-their-tasks

research_task = Task(
    description="Research the current market landscape for AI-powered healthcare solutions",
    expected_output="Comprehensive market data including key players, market size, and growth trends",
    agent=researcher
)

analysis_task = Task(
    description="Analyze the market data and identify the top 3 investment opportunities",
    expected_output="Analysis report with 3 recommended investment opportunities and rationale",
    agent=analyst,
    context=[research_task]
)

---

## Define the task

**URL:** llms-txt#define-the-task

research_task = Task(
    description="Research the latest AI advancements...",
    expected_output="",
    agent=researcher
)

---

## Define the task with output_json set to the Blog model

**URL:** llms-txt#define-the-task-with-output_json-set-to-the-blog-model

task1 = Task(
    description="""Create a blog title and content on a given topic. Make sure the content is under 200 words.""",
    expected_output="A JSON object with 'title' and 'content' fields.",
    agent=blog_agent,
    output_json=Blog,
)

---

## Define your tasks

**URL:** llms-txt#define-your-tasks

research_task = Task(
  description='Gather relevant data...', 
  agent=researcher, 
  expected_output='Raw Data'
)
analysis_task = Task(
  description='Analyze the data...', 
  agent=analyst, 
  expected_output='Data Insights'
)
writing_task = Task(
  description='Compose the report...', 
  agent=writer, 
  expected_output='Final Report'
)

---

## Define your task

**URL:** llms-txt#define-your-task

task = Task(
    description="Generate a list of 5 interesting ideas for an article, then write one captivating paragraph for each idea that showcases the potential of a full article on this topic. Return the list of ideas with their paragraphs and your notes.",
    expected_output="5 bullet points, each with a paragraph and accompanying notes.",
)

---

## Delegate work to coworker(task: str, context: str, coworker: str)

**URL:** llms-txt#delegate-work-to-coworker(task:-str,-context:-str,-coworker:-str)

**Contents:**
  - 2. **Ask Question Tool**

**Examples:**

Example 1 (unknown):
```unknown
### 2. **Ask Question Tool**

Enables agents to ask specific questions to gather information from colleagues.
```

---

## `DirectoryReadTool`

**URL:** llms-txt#`directoryreadtool`

**Contents:**
- Description
- Installation
- Example

<Note>
  We are still working on improving tools, so there might be unexpected behavior or changes in the future.
</Note>

The DirectoryReadTool is a powerful utility designed to provide a comprehensive listing of directory contents.
It can recursively navigate through the specified directory, offering users a detailed enumeration of all files, including those within subdirectories.
This tool is crucial for tasks that require a thorough inventory of directory structures or for validating the organization of files within directories.

To utilize the DirectoryReadTool in your project, install the `crewai_tools` package. If this package is not yet part of your environment, you can install it using pip with the command below:

This command installs the latest version of the `crewai_tools` package, granting access to the DirectoryReadTool among other utilities.

Employing the DirectoryReadTool is straightforward. The following code snippet demonstrates how to set it up and use the tool to list the contents of a specified directory:

```python Code theme={null}
from crewai_tools import DirectoryReadTool

**Examples:**

Example 1 (unknown):
```unknown
This command installs the latest version of the `crewai_tools` package, granting access to the DirectoryReadTool among other utilities.

## Example

Employing the DirectoryReadTool is straightforward. The following code snippet demonstrates how to set it up and use the tool to list the contents of a specified directory:
```

---

## `DOCXSearchTool`

**URL:** llms-txt#`docxsearchtool`

**Contents:**
- Description
- Installation
- Example

<Note>
  We are still working on improving tools, so there might be unexpected behavior or changes in the future.
</Note>

The `DOCXSearchTool` is a RAG tool designed for semantic searching within DOCX documents.
It enables users to effectively search and extract relevant information from DOCX files using query-based searches.
This tool is invaluable for data analysis, information management, and research tasks,
streamlining the process of finding specific information within large document collections.

Install the crewai\_tools package by running the following command in your terminal:

The following example demonstrates initializing the DOCXSearchTool to search within any DOCX file's content or with a specific DOCX file path.

```python Code theme={null}
from crewai_tools import DOCXSearchTool

**Examples:**

Example 1 (unknown):
```unknown
## Example

The following example demonstrates initializing the DOCXSearchTool to search within any DOCX file's content or with a specific DOCX file path.
```

---

## Example task

**URL:** llms-txt#example-task

task = Task(
    description='Find and summarize the latest AI news',
    expected_output='A bullet list summary of the top 5 most important AI news',
    agent=research_agent,
    tools=[search_tool]
)

---

## Example task to extract content from a website

**URL:** llms-txt#example-task-to-extract-content-from-a-website

scrape_task = Task(
    description="Extract the main content from the product page at https://web-scraping.dev/products and summarize the available products.",
    expected_output="A summary of the products available on the website.",
    agent=web_scraper_agent,
)

---

## Example task to extract headlines from a news website

**URL:** llms-txt#example-task-to-extract-headlines-from-a-news-website

scrape_task = Task(
    description="Extract the main headlines from the CNN homepage. Use the CSS selector '.headline' to target the headline elements.",
    expected_output="A list of the main headlines from CNN.",
    agent=web_scraper_agent,
)

---

## Example task to extract product information from an e-commerce site

**URL:** llms-txt#example-task-to-extract-product-information-from-an-e-commerce-site

scrape_task = Task(
    description="Extract product names, prices, and descriptions from the featured products section of example.com.",
    expected_output="A structured list of product information including names, prices, and descriptions.",
    agent=web_scraper_agent,
)

---

## Example task to generate and evaluate code

**URL:** llms-txt#example-task-to-generate-and-evaluate-code

generate_code_task = Task(
    description="Create a simple program to generate the first N numbers in the Fibonacci sequence. Select the most appropriate evaluator and criteria for evaluating your output.",
    expected_output="Program that generates the first N numbers in the Fibonacci sequence.",
    agent=coding_agent,
)

---

## Example task to generate and execute code

**URL:** llms-txt#example-task-to-generate-and-execute-code

coding_task = Task(
    description="Write a Python function to calculate the Fibonacci sequence up to the 10th number and print the result.",
    expected_output="The Fibonacci sequence up to the 10th number.",
    agent=programmer_agent,
)

---

## Example task to generate code

**URL:** llms-txt#example-task-to-generate-code

generate_code_task = Task(
    description="Create a simple program to generate the first N numbers in the Fibonacci sequence.",
    expected_output="Program that generates the first N numbers in the Fibonacci sequence.",
    agent=coding_agent,
)

---

## Example task to query sales data

**URL:** llms-txt#example-task-to-query-sales-data

query_task = Task(
    description="Query the sales data for the last quarter and summarize the top 5 products by revenue.",
    expected_output="A summary of the top 5 products by revenue for the last quarter.",
    agent=data_analyst_agent,
)

---

## Example task to read a configuration file

**URL:** llms-txt#example-task-to-read-a-configuration-file

read_task = Task(
    description="Read the configuration file from {my_bucket} and summarize its contents.",
    expected_output="A summary of the configuration file contents.",
    agent=file_reader_agent,
)

---

## Example task to scrape content from a website

**URL:** llms-txt#example-task-to-scrape-content-from-a-website

scrape_task = Task(
    description="Extract the main content from the homepage of example.com. Use the CSS selector 'main' to target the main content area.",
    expected_output="The main content from example.com's homepage.",
    agent=web_scraper_agent,
)

---

## Example task to search and summarize news

**URL:** llms-txt#example-task-to-search-and-summarize-news

browse_task = Task(
    description="Summarize the top 3 trending AI News headlines",
    expected_output="A summary of the top 3 trending AI News headlines",
    agent=browser_agent,
)

---

## Example task to search for information in a specific video

**URL:** llms-txt#example-task-to-search-for-information-in-a-specific-video

research_task = Task(
    description="Search for information about machine learning frameworks in the YouTube video at {youtube_video_url}",
    expected_output="A summary of the key machine learning frameworks mentioned in the video.",
    agent=video_researcher,
)

---

## Example task to search for information in a specific channel

**URL:** llms-txt#example-task-to-search-for-information-in-a-specific-channel

research_task = Task(
    description="Search for information about machine learning tutorials in the YouTube channel {youtube_channel_handle}",
    expected_output="A summary of the key machine learning tutorials available on the channel.",
    agent=channel_researcher,
)

---

## Example task to write a report

**URL:** llms-txt#example-task-to-write-a-report

write_task = Task(
    description="Generate a summary report of the quarterly sales data and save it to {my_bucket}.",
    expected_output="Confirmation that the report was successfully saved to S3.",
    agent=file_writer_agent,
)

---

## Example task with markdown formatting enabled

**URL:** llms-txt#example-task-with-markdown-formatting-enabled

**Contents:**
  - YAML Configuration with Markdown
  - Benefits of Markdown Output
- Task Dependencies and Context
- Task Guardrails
  - Function-Based Guardrails
  - LLM-Based Guardrails (String Descriptions)

formatted_task = Task(
    description="Create a comprehensive report on AI trends",
    expected_output="A well-structured report with headers, sections, and bullet points",
    agent=reporter_agent,
    markdown=True  # Enable automatic markdown formatting
)
yaml tasks.yaml theme={null}
analysis_task:
  description: >
    Analyze the market data and create a detailed report
  expected_output: >
    A comprehensive analysis with charts and key findings
  agent: analyst
  markdown: true  # Enable markdown formatting
  output_file: analysis.md
python Code theme={null}
research_task = Task(
    description="Research the latest developments in AI",
    expected_output="A list of recent AI developments",
    agent=researcher
)

analysis_task = Task(
    description="Analyze the research findings and identify key trends",
    expected_output="Analysis report of AI trends",
    agent=analyst,
    context=[research_task]  # This task will wait for research_task to complete
)
python Code theme={null}
from typing import Tuple, Union, Dict, Any
from crewai import TaskOutput

def validate_blog_content(result: TaskOutput) -> Tuple[bool, Any]:
    """Validate blog content meets requirements."""
    try:
        # Check word count
        word_count = len(result.raw.split())
        if word_count > 200:
            return (False, "Blog content exceeds 200 words")

# Additional validation logic here
        return (True, result.raw.strip())
    except Exception as e:
        return (False, "Unexpected error during validation")

blog_task = Task(
    description="Write a blog post about AI",
    expected_output="A blog post under 200 words",
    agent=blog_agent,
    guardrail=validate_blog_content  # Add the guardrail function
)
python Code theme={null}
from crewai import Task

**Examples:**

Example 1 (unknown):
```unknown
When `markdown=True`, the agent will receive additional instructions to format the output using:

* `#` for headers
* `**text**` for bold text
* `*text*` for italic text
* `-` or `*` for bullet points
* `` `code` `` for inline code
* ` `language \`\`\` for code blocks

### YAML Configuration with Markdown
```

Example 2 (unknown):
```unknown
### Benefits of Markdown Output

* **Consistent Formatting**: Ensures all outputs follow proper markdown conventions
* **Better Readability**: Structured content with headers, lists, and emphasis
* **Documentation Ready**: Output can be directly used in documentation systems
* **Cross-Platform Compatibility**: Markdown is universally supported

<Note>
  The markdown formatting instructions are automatically added to the task prompt when `markdown=True`, so you don't need to specify formatting requirements in your task description.
</Note>

## Task Dependencies and Context

Tasks can depend on the output of other tasks using the `context` attribute. For example:
```

Example 3 (unknown):
```unknown
## Task Guardrails

Task guardrails provide a way to validate and transform task outputs before they
are passed to the next task. This feature helps ensure data quality and provides
feedback to agents when their output doesn't meet specific criteria.

CrewAI supports two types of guardrails:

1. **Function-based guardrails**: Python functions with custom validation logic, giving you complete control over the validation process and ensuring reliable, deterministic results.

2. **LLM-based guardrails**: String descriptions that use the agent's LLM to validate outputs based on natural language criteria. These are ideal for complex or subjective validation requirements.

### Function-Based Guardrails

To add a function-based guardrail to a task, provide a validation function through the `guardrail` parameter:
```

Example 4 (unknown):
```unknown
### LLM-Based Guardrails (String Descriptions)

Instead of writing custom validation functions, you can use string descriptions that leverage LLM-based validation. When you provide a string to the `guardrail` or `guardrails` parameter, CrewAI automatically creates an `LLMGuardrail` that uses the agent's LLM to validate the output based on your description.

**Requirements**:

* The task must have an `agent` assigned (the guardrail uses the agent's LLM)
* Provide a clear, descriptive string explaining the validation criteria
```

---

## Execute tasks

**URL:** llms-txt#execute-tasks

**Contents:**
- Available CrewAI Tools
- Creating your own Tools
  - Subclassing `BaseTool`
- Asynchronous Tool Support
  - Creating Async Tools
  - Using Async Tools

crew.kickoff()
python Code theme={null}
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class MyToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = "What this tool does. It's vital for effective utilization."
    args_schema: Type[BaseModel] = MyToolInput

def _run(self, argument: str) -> str:
        # Your tool's logic here
        return "Tool's result"
python Code theme={null}
from crewai.tools import tool

@tool("fetch_data_async")
async def fetch_data_async(query: str) -> str:
    """Asynchronously fetch data based on the query."""
    # Simulate async operation
    await asyncio.sleep(1)
    return f"Data retrieved for {query}"
python Code theme={null}
from crewai.tools import BaseTool

class AsyncCustomTool(BaseTool):
    name: str = "async_custom_tool"
    description: str = "An asynchronous custom tool"

async def _run(self, query: str = "") -> str:
        """Asynchronously run the tool"""
        # Your async implementation here
        await asyncio.sleep(1)
        return f"Processed {query} asynchronously"
python Code theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## Available CrewAI Tools

* **Error Handling**: All tools are built with error handling capabilities, allowing agents to gracefully manage exceptions and continue their tasks.
* **Caching Mechanism**: All tools support caching, enabling agents to efficiently reuse previously obtained results, reducing the load on external resources and speeding up the execution time. You can also define finer control over the caching mechanism using the `cache_function` attribute on the tool.

Here is a list of the available tools and their descriptions:

| Tool                             | Description                                                                                    |
| :------------------------------- | :--------------------------------------------------------------------------------------------- |
| **ApifyActorsTool**              | A tool that integrates Apify Actors with your workflows for web scraping and automation tasks. |
| **BrowserbaseLoadTool**          | A tool for interacting with and extracting data from web browsers.                             |
| **CodeDocsSearchTool**           | A RAG tool optimized for searching through code documentation and related technical documents. |
| **CodeInterpreterTool**          | A tool for interpreting python code.                                                           |
| **ComposioTool**                 | Enables use of Composio tools.                                                                 |
| **CSVSearchTool**                | A RAG tool designed for searching within CSV files, tailored to handle structured data.        |
| **DALL-E Tool**                  | A tool for generating images using the DALL-E API.                                             |
| **DirectorySearchTool**          | A RAG tool for searching within directories, useful for navigating through file systems.       |
| **DOCXSearchTool**               | A RAG tool aimed at searching within DOCX documents, ideal for processing Word files.          |
| **DirectoryReadTool**            | Facilitates reading and processing of directory structures and their contents.                 |
| **EXASearchTool**                | A tool designed for performing exhaustive searches across various data sources.                |
| **FileReadTool**                 | Enables reading and extracting data from files, supporting various file formats.               |
| **FirecrawlSearchTool**          | A tool to search webpages using Firecrawl and return the results.                              |
| **FirecrawlCrawlWebsiteTool**    | A tool for crawling webpages using Firecrawl.                                                  |
| **FirecrawlScrapeWebsiteTool**   | A tool for scraping webpages URL using Firecrawl and returning its contents.                   |
| **GithubSearchTool**             | A RAG tool for searching within GitHub repositories, useful for code and documentation search. |
| **SerperDevTool**                | A specialized tool for development purposes, with specific functionalities under development.  |
| **TXTSearchTool**                | A RAG tool focused on searching within text (.txt) files, suitable for unstructured data.      |
| **JSONSearchTool**               | A RAG tool designed for searching within JSON files, catering to structured data handling.     |
| **LlamaIndexTool**               | Enables the use of LlamaIndex tools.                                                           |
| **MDXSearchTool**                | A RAG tool tailored for searching within Markdown (MDX) files, useful for documentation.       |
| **PDFSearchTool**                | A RAG tool aimed at searching within PDF documents, ideal for processing scanned documents.    |
| **PGSearchTool**                 | A RAG tool optimized for searching within PostgreSQL databases, suitable for database queries. |
| **Vision Tool**                  | A tool for generating images using the DALL-E API.                                             |
| **RagTool**                      | A general-purpose RAG tool capable of handling various data sources and types.                 |
| **ScrapeElementFromWebsiteTool** | Enables scraping specific elements from websites, useful for targeted data extraction.         |
| **ScrapeWebsiteTool**            | Facilitates scraping entire websites, ideal for comprehensive data collection.                 |
| **WebsiteSearchTool**            | A RAG tool for searching website content, optimized for web data extraction.                   |
| **XMLSearchTool**                | A RAG tool designed for searching within XML files, suitable for structured data formats.      |
| **YoutubeChannelSearchTool**     | A RAG tool for searching within YouTube channels, useful for video content analysis.           |
| **YoutubeVideoSearchTool**       | A RAG tool aimed at searching within YouTube videos, ideal for video data extraction.          |

## Creating your own Tools

<Tip>
  Developers can craft `custom tools` tailored for their agent's needs or
  utilize pre-built options.
</Tip>

There are two main ways for one to create a CrewAI tool:

### Subclassing `BaseTool`
```

Example 2 (unknown):
```unknown
## Asynchronous Tool Support

CrewAI supports asynchronous tools, allowing you to implement tools that perform non-blocking operations like network requests, file I/O, or other async operations without blocking the main execution thread.

### Creating Async Tools

You can create async tools in two ways:

#### 1. Using the `tool` Decorator with Async Functions
```

Example 3 (unknown):
```unknown
#### 2. Implementing Async Methods in Custom Tool Classes
```

Example 4 (unknown):
```unknown
### Using Async Tools

Async tools work seamlessly in both standard Crew workflows and Flow-based workflows:
```

---

## Execute the task

**URL:** llms-txt#execute-the-task

---

## For complex reasoning tasks

**URL:** llms-txt#for-complex-reasoning-tasks

analyst:
  role: "Data Insights Analyst"
  goal: "..."
  backstory: "..."
  llm: openai/gpt-4o

---

## For creative content

**URL:** llms-txt#for-creative-content

**Contents:**
- Testing and Iterating on Agent Design
- Conclusion
- Next Steps

writer:
  role: "Creative Content Writer"
  goal: "..."
  backstory: "..."
  llm: anthropic/claude-3-opus
```

## Testing and Iterating on Agent Design

Agent design is often an iterative process. Here's a practical approach:

1. **Start with a prototype**: Create an initial agent definition
2. **Test with sample tasks**: Evaluate performance on representative tasks
3. **Analyze outputs**: Identify strengths and weaknesses
4. **Refine the definition**: Adjust role, goal, and backstory based on observations
5. **Test in collaboration**: Evaluate how the agent performs in a crew setting

Crafting effective agents is both an art and a science. By carefully defining roles, goals, and backstories that align with your specific needs, and combining them with well-designed tasks, you can create specialized AI collaborators that produce exceptional results.

Remember that agent and task design is an iterative process. Start with these best practices, observe your agents in action, and refine your approach based on what you learn. And always keep in mind the 80/20 rule - focus most of your effort on creating clear, focused tasks to get the best results from your agents.

<Check>
  Congratulations! You now understand the principles and practices of effective agent design. Apply these techniques to create powerful, specialized agents that work together seamlessly to accomplish complex tasks.
</Check>

* Experiment with different agent configurations for your specific use case
* Learn about [building your first crew](/en/guides/crews/first-crew) to see how agents work together
* Explore [CrewAI Flows](/en/guides/flows/first-flow) for more advanced orchestration

---

## Hallucination Guardrail

**URL:** llms-txt#hallucination-guardrail

**Contents:**
- Overview
- What are Hallucinations?
- Basic Usage
  - Setting Up the Guardrail

Source: https://docs.crewai.com/en/enterprise/features/hallucination-guardrail

Prevent and detect AI hallucinations in your CrewAI tasks

The Hallucination Guardrail is an enterprise feature that validates AI-generated content to ensure it's grounded in facts and doesn't contain hallucinations. It analyzes task outputs against reference context and provides detailed feedback when potentially hallucinated content is detected.

## What are Hallucinations?

AI hallucinations occur when language models generate content that appears plausible but is factually incorrect or not supported by the provided context. The Hallucination Guardrail helps prevent these issues by:

* Comparing outputs against reference context
* Evaluating faithfulness to source material
* Providing detailed feedback on problematic content
* Supporting custom thresholds for validation strictness

### Setting Up the Guardrail

```python theme={null}
from crewai.tasks.hallucination_guardrail import HallucinationGuardrail
from crewai import LLM

---

## Hierarchical Process

**URL:** llms-txt#hierarchical-process

**Contents:**
- Introduction
- Hierarchical Process Overview
  - Key Features
- Implementing the Hierarchical Process

Source: https://docs.crewai.com/en/learn/hierarchical-process

A comprehensive guide to understanding and applying the hierarchical process within your CrewAI projects, updated to reflect the latest coding practices and functionalities.

The hierarchical process in CrewAI introduces a structured approach to task management, simulating traditional organizational hierarchies for efficient task delegation and execution.
This systematic workflow enhances project outcomes by ensuring tasks are handled with optimal efficiency and accuracy.

<Tip>
  The hierarchical process is designed to leverage advanced models like GPT-4, optimizing token usage while handling complex tasks with greater efficiency.
</Tip>

## Hierarchical Process Overview

By default, tasks in CrewAI are managed through a sequential process. However, adopting a hierarchical approach allows for a clear hierarchy in task management,
where a 'manager' agent coordinates the workflow, delegates tasks, and validates outcomes for streamlined and effective execution. This manager agent can now be either
automatically created by CrewAI or explicitly set by the user.

* **Task Delegation**: A manager agent allocates tasks among crew members based on their roles and capabilities.
* **Result Validation**: The manager evaluates outcomes to ensure they meet the required standards.
* **Efficient Workflow**: Emulates corporate structures, providing an organized approach to task management.
* **System Prompt Handling**: Optionally specify whether the system should use predefined prompts.
* **Stop Words Control**: Optionally specify whether stop words should be used, supporting various models including the o1 models.
* **Context Window Respect**: Prioritize important context by enabling respect of the context window, which is now the default behavior.
* **Delegation Control**: Delegation is now disabled by default to give users explicit control.
* **Max Requests Per Minute**: Configurable option to set the maximum number of requests per minute.
* **Max Iterations**: Limit the maximum number of iterations for obtaining a final answer.

## Implementing the Hierarchical Process

To utilize the hierarchical process, it's essential to explicitly set the process attribute to `Process.hierarchical`, as the default behavior is `Process.sequential`.
Define a crew with a designated manager and establish a clear chain of command.

<Tip>
  Assign tools at the agent level to facilitate task delegation and execution by the designated agents under the manager's guidance.
  Tools can also be specified at the task level for precise control over tool availability during task execution.
</Tip>

<Tip>
  Configuring the `manager_llm` parameter is crucial for the hierarchical process.
  The system requires a manager LLM to be set up for proper function, ensuring tailored decision-making.
</Tip>

```python Code theme={null}
from crewai import Crew, Process, Agent

---

## If false, the task will be skipped, if true, then execute the task.

**URL:** llms-txt#if-false,-the-task-will-be-skipped,-if-true,-then-execute-the-task.

def is_data_missing(output: TaskOutput) -> bool:
    return len(output.pydantic.events) < 10  # this will skip this task

---

## Manager-led task

**URL:** llms-txt#manager-led-task

project_task = Task(
    description="Create a comprehensive market analysis report with recommendations",
    expected_output="Executive summary, detailed analysis, and strategic recommendations",
    agent=manager  # Manager will delegate to specialists
)

---

## `MDXSearchTool`

**URL:** llms-txt#`mdxsearchtool`

**Contents:**
- Description
- Installation
- Usage Example

<Note>
  The MDXSearchTool is in continuous development. Features may be added or removed, and functionality could change unpredictably as we refine the tool.
</Note>

The MDX Search Tool is a component of the `crewai_tools` package aimed at facilitating advanced markdown language extraction. It enables users to effectively search and extract relevant information from MD files using query-based searches. This tool is invaluable for data analysis, information management, and research tasks, streamlining the process of finding specific information within large document collections.

Before using the MDX Search Tool, ensure the `crewai_tools` package is installed. If it is not, you can install it with the following command:

To use the MDX Search Tool, you must first set up the necessary environment variables. Then, integrate the tool into your crewAI project to begin your market research. Below is a basic example of how to do this:

```python Code theme={null}
from crewai_tools import MDXSearchTool

**Examples:**

Example 1 (unknown):
```unknown
## Usage Example

To use the MDX Search Tool, you must first set up the necessary environment variables. Then, integrate the tool into your crewAI project to begin your market research. Below is a basic example of how to do this:
```

---

## Original task prompt

**URL:** llms-txt#original-task-prompt

task_prompt = "Answer the following questions about the user's favorite movies: What movie did John watch last week? Format your answer in JSON."

---

## Perfect for precision tasks

**URL:** llms-txt#perfect-for-precision-tasks

**Contents:**
  - Alternative Approaches for Large Data

precision_agent = Agent(
    role="Code Security Auditor",
    goal="Identify security vulnerabilities in code",
    backstory="Security expert requiring complete code context",
    respect_context_window=False,  # Prefer failure over incomplete analysis
    max_retry_limit=1,  # Fail fast on context issues
    verbose=True
)
python Code theme={null}
from crewai_tools import RagTool

**Examples:**

Example 1 (unknown):
```unknown
### Alternative Approaches for Large Data

When dealing with very large datasets, consider these strategies:

#### 1. Use RAG Tools
```

---

## Planning

**URL:** llms-txt#planning

**Contents:**
- Overview
  - Using the Planning Feature

Source: https://docs.crewai.com/en/concepts/planning

Learn how to add planning to your CrewAI Crew and improve their performance.

The planning feature in CrewAI allows you to add planning capability to your crew. When enabled, before each Crew iteration,
all Crew information is sent to an AgentPlanner that will plan the tasks step by step, and this plan will be added to each task description.

### Using the Planning Feature

Getting started with the planning feature is very easy, the only step required is to add `planning=True` to your Crew:

<CodeGroup>
  
</CodeGroup>

From this point on, your crew will have planning enabled, and the tasks will be planned before each iteration.

<Warning>
  When planning is enabled, crewAI will use `gpt-4o-mini` as the default LLM for planning, which requires a valid OpenAI API key. Since your agents might be using different LLMs, this could cause confusion if you don't have an OpenAI API key configured or if you're experiencing unexpected behavior related to LLM API calls.
</Warning>

Now you can define the LLM that will be used to plan the tasks.

When running the base case example, you will see something like the output below, which represents the output of the `AgentPlanner`
responsible for creating the step-by-step logic to add to the Agents' tasks.

**Task Tools:** None specified

**Agent Tools:** None specified

**Step-by-Step Plan:**

1. **Review the Bullet Points:**
     - Carefully read through the list of 10 bullet points provided by the AI LLMs Senior Data Researcher.

2. **Outline the Report:**
     - Create an outline with each bullet point as a main section heading.
     - Plan sub-sections under each main heading to cover different aspects of the topic.

3. **Research Further Details:**
     - For each bullet point, conduct additional research if necessary to gather more detailed information.
     - Look for case studies, examples, and statistical data to support each section.

4. **Write Detailed Sections:**
     - Expand each bullet point into a comprehensive section.
     - Ensure each section includes an introduction, detailed explanation, examples, and a conclusion.
     - Use markdown formatting for headings, subheadings, lists, and emphasis.

5. **Review and Edit:**
     - Proofread the report for clarity, coherence, and correctness.
     - Make sure the report flows logically from one section to the next.
     - Format the report according to markdown standards.

6. **Finalize the Report:**
     - Ensure the report is complete with all sections expanded and detailed.
     - Double-check formatting and make any necessary adjustments.

**Expected Output:**
  A fully fledged report with the main topics, each with a full section of information. Formatted as markdown without '`
</CodeGroup>

**Examples:**

Example 1 (unknown):
```unknown
</CodeGroup>

From this point on, your crew will have planning enabled, and the tasks will be planned before each iteration.

<Warning>
  When planning is enabled, crewAI will use `gpt-4o-mini` as the default LLM for planning, which requires a valid OpenAI API key. Since your agents might be using different LLMs, this could cause confusion if you don't have an OpenAI API key configured or if you're experiencing unexpected behavior related to LLM API calls.
</Warning>

#### Planning LLM

Now you can define the LLM that will be used to plan the tasks.

When running the base case example, you will see something like the output below, which represents the output of the `AgentPlanner`
responsible for creating the step-by-step logic to add to the Agents' tasks.

<CodeGroup>
```

Example 2 (unknown):
```unknown

```

---

## Returns a TaskOutput object with the description and results of the task

**URL:** llms-txt#returns-a-taskoutput-object-with-the-description-and-results-of-the-task

**Contents:**
- Tool Override Mechanism
- Error Handling and Validation Mechanisms
- Creating Directories when Saving Files
  - Default Behavior

print(f"""
    Task completed!
    Task: {task1.output.description}
    Output: {task1.output.raw}
""")
python Code theme={null}

**Examples:**

Example 1 (unknown):
```unknown
## Tool Override Mechanism

Specifying tools in a task allows for dynamic adaptation of agent capabilities, emphasizing CrewAI's flexibility.

## Error Handling and Validation Mechanisms

While creating and executing tasks, certain validation mechanisms are in place to ensure the robustness and reliability of task attributes. These include but are not limited to:

* Ensuring only one output type is set per task to maintain clear output expectations.
* Preventing the manual assignment of the `id` attribute to uphold the integrity of the unique identifier system.

These validations help in maintaining the consistency and reliability of task executions within the crewAI framework.

## Creating Directories when Saving Files

The `create_directory` parameter controls whether CrewAI should automatically create directories when saving task outputs to files. This feature is particularly useful for organizing outputs and ensuring that file paths are correctly structured, especially when working with complex project hierarchies.

### Default Behavior

By default, `create_directory=True`, which means CrewAI will automatically create any missing directories in the output file path:
```

---

## `ScrapegraphScrapeTool`

**URL:** llms-txt#`scrapegraphscrapetool`

**Contents:**
- Description
- Installation
- Steps to Get Started
- Example

The `ScrapegraphScrapeTool` is designed to leverage Scrapegraph AI's SmartScraper API to intelligently extract content from websites. This tool provides advanced web scraping capabilities with AI-powered content extraction, making it ideal for targeted data collection and content analysis tasks. Unlike traditional web scrapers, it can understand the context and structure of web pages to extract the most relevant information based on natural language prompts.

To use this tool, you need to install the Scrapegraph Python client:

You'll also need to set up your Scrapegraph API key as an environment variable:

You can obtain an API key from [Scrapegraph AI](https://scrapegraphai.com).

## Steps to Get Started

To effectively use the `ScrapegraphScrapeTool`, follow these steps:

1. **Install Dependencies**: Install the required package using the command above.
2. **Set Up API Key**: Set your Scrapegraph API key as an environment variable or provide it during initialization.
3. **Initialize the Tool**: Create an instance of the tool with the necessary parameters.
4. **Define Extraction Prompts**: Create natural language prompts to guide the extraction of specific content.

The following example demonstrates how to use the `ScrapegraphScrapeTool` to extract content from a website:

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import ScrapegraphScrapeTool

**Examples:**

Example 1 (unknown):
```unknown
You'll also need to set up your Scrapegraph API key as an environment variable:
```

Example 2 (unknown):
```unknown
You can obtain an API key from [Scrapegraph AI](https://scrapegraphai.com).

## Steps to Get Started

To effectively use the `ScrapegraphScrapeTool`, follow these steps:

1. **Install Dependencies**: Install the required package using the command above.
2. **Set Up API Key**: Set your Scrapegraph API key as an environment variable or provide it during initialization.
3. **Initialize the Tool**: Create an instance of the tool with the necessary parameters.
4. **Define Extraction Prompts**: Create natural language prompts to guide the extraction of specific content.

## Example

The following example demonstrates how to use the `ScrapegraphScrapeTool` to extract content from a website:
```

---

## `ScrapeWebsiteTool`

**URL:** llms-txt#`scrapewebsitetool`

**Contents:**
- Description
- Installation
- Example

<Note>
  We are still working on improving tools, so there might be unexpected behavior or changes in the future.
</Note>

A tool designed to extract and read the content of a specified website. It is capable of handling various types of web pages by making HTTP requests and parsing the received HTML content.
This tool can be particularly useful for web scraping tasks, data collection, or extracting specific information from websites.

Install the crewai\_tools package

```python theme={null}
from crewai_tools import ScrapeWebsiteTool

**Examples:**

Example 1 (unknown):
```unknown
## Example
```

---

## `ScrapflyScrapeWebsiteTool`

**URL:** llms-txt#`scrapflyscrapewebsitetool`

**Contents:**
- Description
- Installation
- Steps to Get Started
- Example

The `ScrapflyScrapeWebsiteTool` is designed to leverage [Scrapfly](https://scrapfly.io/)'s web scraping API to extract content from websites. This tool provides advanced web scraping capabilities with headless browser support, proxies, and anti-bot bypass features. It allows for extracting web page data in various formats, including raw HTML, markdown, and plain text, making it ideal for a wide range of web scraping tasks.

To use this tool, you need to install the Scrapfly SDK:

You'll also need to obtain a Scrapfly API key by registering at [scrapfly.io/register](https://www.scrapfly.io/register/).

## Steps to Get Started

To effectively use the `ScrapflyScrapeWebsiteTool`, follow these steps:

1. **Install Dependencies**: Install the Scrapfly SDK using the command above.
2. **Obtain API Key**: Register at Scrapfly to get your API key.
3. **Initialize the Tool**: Create an instance of the tool with your API key.
4. **Configure Scraping Parameters**: Customize the scraping parameters based on your needs.

The following example demonstrates how to use the `ScrapflyScrapeWebsiteTool` to extract content from a website:

```python Code theme={null}
from crewai import Agent, Task, Crew
from crewai_tools import ScrapflyScrapeWebsiteTool

**Examples:**

Example 1 (unknown):
```unknown
You'll also need to obtain a Scrapfly API key by registering at [scrapfly.io/register](https://www.scrapfly.io/register/).

## Steps to Get Started

To effectively use the `ScrapflyScrapeWebsiteTool`, follow these steps:

1. **Install Dependencies**: Install the Scrapfly SDK using the command above.
2. **Obtain API Key**: Register at Scrapfly to get your API key.
3. **Initialize the Tool**: Create an instance of the tool with your API key.
4. **Configure Scraping Parameters**: Customize the scraping parameters based on your needs.

## Example

The following example demonstrates how to use the `ScrapflyScrapeWebsiteTool` to extract content from a website:
```

---

## `SeleniumScrapingTool`

**URL:** llms-txt#`seleniumscrapingtool`

**Contents:**
- Description
- Installation
- Example

<Note>
  This tool is currently in development. As we refine its capabilities, users may encounter unexpected behavior.
  Your feedback is invaluable to us for making improvements.
</Note>

The `SeleniumScrapingTool` is crafted for high-efficiency web scraping tasks.
It allows for precise extraction of content from web pages by using CSS selectors to target specific elements.
Its design caters to a wide range of scraping needs, offering flexibility to work with any provided website URL.

To use this tool, you need to install the CrewAI tools package and Selenium:

You'll also need to have Chrome installed on your system, as the tool uses Chrome WebDriver for browser automation.

The following example demonstrates how to use the `SeleniumScrapingTool` with a CrewAI agent:

```python Code theme={null}
from crewai import Agent, Task, Crew, Process
from crewai_tools import SeleniumScrapingTool

**Examples:**

Example 1 (unknown):
```unknown
You'll also need to have Chrome installed on your system, as the tool uses Chrome WebDriver for browser automation.

## Example

The following example demonstrates how to use the `SeleniumScrapingTool` with a CrewAI agent:
```

---

## Sequential Processes

**URL:** llms-txt#sequential-processes

**Contents:**
- Introduction
- Sequential Process Overview
  - Key Features
- Implementing the Sequential Process

Source: https://docs.crewai.com/en/learn/sequential-process

A comprehensive guide to utilizing the sequential processes for task execution in CrewAI projects.

CrewAI offers a flexible framework for executing tasks in a structured manner, supporting both sequential and hierarchical processes.
This guide outlines how to effectively implement these processes to ensure efficient task execution and project completion.

## Sequential Process Overview

The sequential process ensures tasks are executed one after the other, following a linear progression.
This approach is ideal for projects requiring tasks to be completed in a specific order.

* **Linear Task Flow**: Ensures orderly progression by handling tasks in a predetermined sequence.
* **Simplicity**: Best suited for projects with clear, step-by-step tasks.
* **Easy Monitoring**: Facilitates easy tracking of task completion and project progress.

## Implementing the Sequential Process

To use the sequential process, assemble your crew and define tasks in the order they need to be executed.

```python Code theme={null}
from crewai import Crew, Process, Agent, Task, TaskOutput, CrewOutput

---

## Strict mode - directory must already exist

**URL:** llms-txt#strict-mode---directory-must-already-exist

**Contents:**
  - YAML Configuration
  - Use Cases
  - Error Handling
- Conclusion

strict_output_task = Task(
    description='Save critical data that requires existing infrastructure',
    expected_output='Data saved to pre-configured location',
    agent=data_agent,
    output_file='secure/vault/critical_data.json',
    create_directory=False  # Will raise RuntimeError if 'secure/vault/' doesn't exist
)
yaml tasks.yaml theme={null}
analysis_task:
  description: >
    Generate quarterly financial analysis
  expected_output: >
    A comprehensive financial report with quarterly insights
  agent: financial_analyst
  output_file: reports/quarterly/q4_2024_analysis.pdf
  create_directory: true  # Automatically create 'reports/quarterly/' directory

audit_task:
  description: >
    Perform compliance audit and save to existing audit directory
  expected_output: >
    A compliance audit report
  agent: auditor
  output_file: audit/compliance_report.md
  create_directory: false  # Directory must already exist
python Code theme={null}
try:
    result = crew.kickoff()
except RuntimeError as e:
    # Handle missing directory error
    print(f"Directory creation failed: {e}")
    # Create directory manually or use fallback location
```

Check out the video below to see how to use structured outputs in CrewAI:

<iframe title="Structured outputs in CrewAI" />

Tasks are the driving force behind the actions of agents in CrewAI.
By properly defining tasks and their outcomes, you set the stage for your AI agents to work effectively, either independently or as a collaborative unit.
Equipping tasks with appropriate tools, understanding the execution process, and following robust validation practices are crucial for maximizing CrewAI's potential,
ensuring agents are effectively prepared for their assignments and that tasks are executed as intended.

**Examples:**

Example 1 (unknown):
```unknown
### YAML Configuration

You can also configure this behavior in your YAML task definitions:
```

Example 2 (unknown):
```unknown
### Use Cases

**Automatic Directory Creation (`create_directory=True`):**

* Development and prototyping environments
* Dynamic report generation with date-based folders
* Automated workflows where directory structure may vary
* Multi-tenant applications with user-specific folders

**Manual Directory Management (`create_directory=False`):**

* Production environments with strict file system controls
* Security-sensitive applications where directories must be pre-configured
* Systems with specific permission requirements
* Compliance environments where directory creation is audited

### Error Handling

When `create_directory=False` and the directory doesn't exist, CrewAI will raise a `RuntimeError`:
```

---

## Task 1

**URL:** llms-txt#task-1

research_task:
  description: "Research the top 5 market trends in the AI industry for 2024."
  expected_output: "A markdown list of the 5 trends with supporting evidence."

---

## Task 1: Research

**URL:** llms-txt#task-1:-research

market_research_task:
  description: "Research current market trends in the SaaS project management space."
  expected_output: "A markdown summary of key market trends."

---

## Task 2

**URL:** llms-txt#task-2

analysis_task:
  description: "Analyze the identified trends to determine potential business impacts."
  expected_output: "A structured analysis with impact ratings (High/Medium/Low)."

---

## Task 2: Competitive Analysis

**URL:** llms-txt#task-2:-competitive-analysis

competitor_analysis_task:
  description: "Analyze strategies of the top 3 competitors based on the market research."
  expected_output: "A comparison table of competitor strategies."
  context: [market_research_task]

---

## Task 3

**URL:** llms-txt#task-3

**Contents:**
- Common Mistakes to Avoid
  - 1. Unclear Task Instructions
  - 2. "God Tasks" That Try to Do Too Much

visualization_task:
  description: "Create a visual representation of the analyzed trends."
  expected_output: "A description of a chart showing trends and their impact ratings."
yaml theme={null}
analysis_task:
  description: >
    Analyze the customer feedback data from the CSV file.
    Focus on identifying recurring themes related to product usability.
    Consider sentiment and frequency when determining importance.
  expected_output: >
    A markdown report with the following sections:
    1. Executive summary (3-5 bullet points)
    2. Top 3 usability issues with supporting data
    3. Recommendations for improvement
yaml theme={null}
competitor_analysis_task:
  description: >
    Analyze our three main competitors' pricing strategies.
    This analysis will inform our upcoming pricing model revision.
    Focus on identifying patterns in how they price premium features
    and how they structure their tiered offerings.
yaml theme={null}
data_extraction_task:
  description: "Extract key metrics from the quarterly report."
  expected_output: "JSON object with the following keys: revenue, growth_rate, customer_acquisition_cost, and retention_rate."
yaml theme={null}
research_task:
  description: "Research AI trends."
  expected_output: "A report on AI trends."
yaml theme={null}
research_task:
  description: >
    Research the top emerging AI trends for 2024 with a focus on:
    1. Enterprise adoption patterns
    2. Technical breakthroughs in the past 6 months
    3. Regulatory developments affecting implementation

For each trend, identify key companies, technologies, and potential business impacts.
  expected_output: >
    A comprehensive markdown report with:
    - Executive summary (5 bullet points)
    - 5-7 major trends with supporting evidence
    - For each trend: definition, examples, and business implications
    - References to authoritative sources
yaml theme={null}
comprehensive_task:
  description: "Research market trends, analyze competitor strategies, create a marketing plan, and design a launch timeline."
yaml theme={null}

**Examples:**

Example 1 (unknown):
```unknown
#### 2. Be Explicit About Inputs and Outputs

Always clearly specify what inputs the task will use and what the output should look like:

**Example:**
```

Example 2 (unknown):
```unknown
#### 3. Include Purpose and Context

Explain why the task matters and how it fits into the larger workflow:

**Example:**
```

Example 3 (unknown):
```unknown
#### 4. Use Structured Output Tools

For machine-readable outputs, specify the format clearly:

**Example:**
```

Example 4 (unknown):
```unknown
## Common Mistakes to Avoid

Based on lessons learned from real-world implementations, here are the most common pitfalls in agent and task design:

### 1. Unclear Task Instructions

**Problem:** Tasks lack sufficient detail, making it difficult for agents to execute effectively.

**Example of Poor Design:**
```

---

## Task for financial modeling

**URL:** llms-txt#task-for-financial-modeling

**Contents:**
- Troubleshooting
  - Common Issues
  - Getting Help

modeling_task = Task(
    description="""
    1. Create financial model workbooks with multiple scenarios
    2. Set up input tables for assumptions and variables
    3. Create calculation worksheets with formulas and logic
    4. Generate charts for financial projections and trends
    5. Add summary tables for key financial metrics
    6. Create sensitivity analysis tables
    """,
    agent=financial_modeler,
    expected_output="Financial model created with scenarios, calculations, and analysis charts"
)

crew = Crew(
    agents=[financial_modeler],
    tasks=[modeling_task]
)

**Permission Errors**

* Ensure your Microsoft account has appropriate permissions for Excel and OneDrive/SharePoint
* Verify that the OAuth connection includes required scopes (Files.Read.All, Files.ReadWrite.All)
* Check that you have access to the specific workbooks you're trying to modify

**File ID and Path Issues**

* Verify that file IDs are correct and files exist in your OneDrive or SharePoint
* Ensure file paths are properly formatted when creating new workbooks
* Check that workbook files have the correct .xlsx extension

**Worksheet and Range Issues**

* Verify that worksheet names exist in the specified workbook
* Ensure range addresses are properly formatted (e.g., 'A1:C10')
* Check that ranges don't exceed worksheet boundaries

**Data Format Issues**

* Ensure data values are properly formatted for Excel (strings, numbers, integers)
* Verify that 2D arrays for ranges have consistent row and column counts
* Check that table data includes proper headers when has\_headers is true

**Chart Creation Issues**

* Verify that chart types are supported (ColumnClustered, Line, Pie, etc.)
* Ensure source data ranges contain appropriate data for the chart type
* Check that the source data range exists and contains data

**Table Management Issues**

* Ensure table names are unique within worksheets
* Verify that table ranges don't overlap with existing tables
* Check that new row data matches the table's column structure

**Cell and Range Operations**

* Verify that row and column indices are 0-based for cell operations
* Ensure ranges contain data when using get\_used\_range
* Check that named ranges exist before referencing them

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with Microsoft Excel integration setup or troubleshooting.
</Card>

---

## Task output validation flow

**URL:** llms-txt#task-output-validation-flow

**Contents:**
  - Event Tracking
- Best Practices
  - Context Guidelines
  - Threshold Selection
- Performance Considerations
  - Impact on Execution Time
  - Cost Optimization
- Troubleshooting

task_output = agent.execute_task(task)
validation_result = guardrail(task_output)

if validation_result.valid:
    # Task completes successfully
    return task_output
else:
    # Task fails with validation feedback
    raise ValidationError(validation_result.feedback)
python theme={null}
    context = """
    Company XYZ was founded in 2020 and specializes in renewable energy solutions.
    They have 150 employees and generated $50M revenue in 2023.
    Their main products include solar panels and wind turbines.
    """
    python theme={null}
    # Good: Focused context
    context = "The current weather in New York is 18°C with light rain."

# Avoid: Unrelated information
    context = "The weather is 18°C. The city has 8 million people. Traffic is heavy."
    ```
  </Step>

<Step title="Update Context Regularly">
    Ensure your reference context reflects current, accurate information.
  </Step>
</Steps>

### Threshold Selection

<Steps>
  <Step title="Start with Default Validation">
    Begin without custom thresholds to understand baseline performance.
  </Step>

<Step title="Adjust Based on Requirements">
    * **High-stakes content**: Use threshold 8-10 for maximum accuracy
    * **General content**: Use threshold 6-7 for balanced validation
    * **Creative content**: Use threshold 4-5 or default verdict-based validation
  </Step>

<Step title="Monitor and Iterate">
    Track validation results and adjust thresholds based on false positives/negatives.
  </Step>
</Steps>

## Performance Considerations

### Impact on Execution Time

* **Validation Overhead**: Each guardrail adds \~1-3 seconds per task
* **LLM Efficiency**: Choose efficient models for evaluation (e.g., gpt-4o-mini)

### Cost Optimization

* **Model Selection**: Use smaller, efficient models for guardrail evaluation
* **Context Size**: Keep reference context concise but comprehensive
* **Caching**: Consider caching validation results for repeated content

<Accordion title="Validation Always Fails">
  **Possible Causes:**

* Context is too restrictive or unrelated to task output
  * Threshold is set too high for the content type
  * Reference context contains outdated information

* Review and update context to match task requirements
  * Lower threshold or use default verdict-based validation
  * Ensure context is current and accurate
</Accordion>

<Accordion title="False Positives (Valid Content Marked Invalid)">
  **Possible Causes:**

* Threshold too high for creative or interpretive tasks
  * Context doesn't cover all valid aspects of the output
  * Evaluation model being overly conservative

* Lower threshold or use default validation
  * Expand context to include broader acceptable content
  * Test with different evaluation models
</Accordion>

<Accordion title="Evaluation Errors">
  **Possible Causes:**

* Network connectivity issues
  * LLM model unavailable or rate limited
  * Malformed task output or context

* Check network connectivity and LLM service status
  * Implement retry logic for transient failures
  * Validate task output format before guardrail evaluation
</Accordion>

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with hallucination guardrail configuration or troubleshooting.
</Card>

**Examples:**

Example 1 (unknown):
```unknown
### Event Tracking

The guardrail integrates with CrewAI's event system to provide observability:

* **Validation Started**: When guardrail evaluation begins
* **Validation Completed**: When evaluation finishes with results
* **Validation Failed**: When technical errors occur during evaluation

## Best Practices

### Context Guidelines

<Steps>
  <Step title="Provide Comprehensive Context">
    Include all relevant factual information that the AI should base its output on:
```

Example 2 (unknown):
```unknown
</Step>

  <Step title="Keep Context Relevant">
    Only include information directly related to the task to avoid confusion:
```

---

## Task to add new data to a spreadsheet

**URL:** llms-txt#task-to-add-new-data-to-a-spreadsheet

data_entry_task = Task(
    description="Add a new customer record to the customer database spreadsheet with name, email, and signup date",
    agent=sheets_agent,
    expected_output="New customer record added successfully to the spreadsheet"
)

---

## Task to create and populate a workbook

**URL:** llms-txt#task-to-create-and-populate-a-workbook

data_management_task = Task(
    description="Create a new sales report workbook with data analysis and charts",
    agent=excel_agent,
    expected_output="Excel workbook created with sales data, analysis, and visualizations"
)

---

## Task to create a bug report

**URL:** llms-txt#task-to-create-a-bug-report

create_bug_task = Task(
    description="Create a high-priority bug report for the authentication system and assign it to the backend team",
    agent=linear_agent,
    expected_output="Bug report created successfully with issue ID"
)

---

## Task to create a folder structure

**URL:** llms-txt#task-to-create-a-folder-structure

create_structure_task = Task(
    description="Create a folder called 'Project Files' in the root directory and upload a document from URL",
    agent=box_agent,
    expected_output="Folder created and file uploaded successfully"
)

---

## Task to create a new company

**URL:** llms-txt#task-to-create-a-new-company

create_company_task = Task(
    description="Create a new company in HubSpot with name 'Innovate Corp' and domain 'innovatecorp.com'.",
    agent=hubspot_agent,
    expected_output="Company created successfully with confirmation"
)

---

## Task to create a new customer

**URL:** llms-txt#task-to-create-a-new-customer

create_customer_task = Task(
    description="Create a new premium customer John Doe with email john.doe@example.com",
    agent=stripe_agent,
    expected_output="Customer created successfully with customer ID"
)

---

## Task to create a new document

**URL:** llms-txt#task-to-create-a-new-document

create_doc_task = Task(
    description="Create a new Google Document titled 'Project Status Report'",
    agent=docs_agent,
    expected_output="New Google Document 'Project Status Report' created successfully"
)

---

## Task to create a new issue

**URL:** llms-txt#task-to-create-a-new-issue

create_issue_task = Task(
    description="Create a bug report issue for the login functionality in the main repository",
    agent=github_agent,
    expected_output="Issue created successfully with issue number"
)

---

## Task to create a new lead

**URL:** llms-txt#task-to-create-a-new-lead

create_lead_task = Task(
    description="Create a new lead for John Doe from Example Corp with email john.doe@example.com",
    agent=salesforce_agent,
    expected_output="Lead created successfully with lead ID"
)

---

## Task to create a new project

**URL:** llms-txt#task-to-create-a-new-project

create_project_task = Task(
    description="Create a new project called 'Q1 Marketing Campaign' in the Marketing workspace",
    agent=asana_agent,
    expected_output="Confirmation that the project was created successfully with project ID"
)

---

## Task to create a new support ticket

**URL:** llms-txt#task-to-create-a-new-support-ticket

create_ticket_task = Task(
    description="Create a high-priority support ticket for John Smith who is unable to access his account after password reset",
    agent=zendesk_agent,
    expected_output="Support ticket created successfully with ticket ID"
)

---

## Task to create a new task

**URL:** llms-txt#task-to-create-a-new-task

create_task = Task(
    description="Create a task called 'Review Q1 Reports' in the Marketing list with high priority",
    agent=clickup_agent,
    expected_output="Task created successfully with task ID"
)

---

## Task to create a new text document

**URL:** llms-txt#task-to-create-a-new-text-document

create_doc_task = Task(
    description="Create a new text document named 'meeting_notes.txt' with content 'Meeting Notes from January 2024: Key discussion points and action items.'",
    agent=word_agent,
    expected_output="New text document 'meeting_notes.txt' created successfully."
)

---

## Task to create a presentation

**URL:** llms-txt#task-to-create-a-presentation

create_presentation_task = Task(
    description="Create a new presentation for the quarterly business review with key slides",
    agent=slides_agent,
    expected_output="Quarterly business review presentation created with structured content"
)

---

## Task to list files and create a folder

**URL:** llms-txt#task-to-list-files-and-create-a-folder

organize_files_task = Task(
    description="List all files in my OneDrive root directory and create a new folder called 'Project Documents'.",
    agent=onedrive_agent,
    expected_output="List of files displayed and new folder 'Project Documents' created."
)

---

## Task to list teams and channels

**URL:** llms-txt#task-to-list-teams-and-channels

explore_teams_task = Task(
    description="List all teams I'm a member of and then get the channels for the first team.",
    agent=teams_agent,
    expected_output="List of teams and channels displayed."
)

---

## Task to list workspace users

**URL:** llms-txt#task-to-list-workspace-users

user_management_task = Task(
    description="List all users in the workspace and provide a summary of team members",
    agent=notion_agent,
    expected_output="Complete list of workspace users with their details"
)

---

## Task to organize files

**URL:** llms-txt#task-to-organize-files

organize_files_task = Task(
    description="List all files in the root directory and organize them into appropriate folders",
    agent=drive_agent,
    expected_output="Summary of files organized with folder structure"
)

---

## Task to organize SharePoint content

**URL:** llms-txt#task-to-organize-sharepoint-content

content_organization_task = Task(
    description="List all accessible SharePoint sites and organize content by department",
    agent=sharepoint_agent,
    expected_output="SharePoint sites listed and content organized by department"
)

---

## Task to retrieve and organize contacts

**URL:** llms-txt#task-to-retrieve-and-organize-contacts

contact_management_task = Task(
    description="Retrieve all contacts and organize them by company affiliation",
    agent=contacts_agent,
    expected_output="Contacts retrieved and organized by company with summary report"
)

---

## Task to send an email

**URL:** llms-txt#task-to-send-an-email

send_email_task = Task(
    description="Send an email to 'colleague@example.com' with subject 'Project Update' and body 'Hi, here is the latest project update. Best regards.'",
    agent=outlook_agent,
    expected_output="Email sent successfully to colleague@example.com"
)

---

## Task to send a follow-up email

**URL:** llms-txt#task-to-send-a-follow-up-email

send_email_task = Task(
    description="Send a follow-up email to john@example.com about the project update meeting",
    agent=gmail_agent,
    expected_output="Email sent successfully with confirmation"
)

---

## Task to send project updates

**URL:** llms-txt#task-to-send-project-updates

update_task = Task(
    description="Send a project status update to the #general channel with current progress",
    agent=slack_agent,
    expected_output="Project update message sent successfully to team channel"
)

---

## With explicit reference context

**URL:** llms-txt#with-explicit-reference-context

**Contents:**
  - Adding to Tasks

context_guardrail = HallucinationGuardrail(
    context="AI helps with various tasks including analysis and generation.",
    llm=LLM(model="gpt-4o-mini")
)
python theme={null}
from crewai import Task

**Examples:**

Example 1 (unknown):
```unknown
### Adding to Tasks
```

---

## You can also see how the task description gets formatted

**URL:** llms-txt#you-can-also-see-how-the-task-description-gets-formatted

**Contents:**
  - Overriding Default Instructions

print("\n=== TASK CONTEXT ===")
print(f"Task Description: {task.description}")
print(f"Expected Output: {task.expected_output}")
python theme={null}
from crewai import Agent

**Examples:**

Example 1 (unknown):
```unknown
### Overriding Default Instructions

You have several options to gain full control over the prompts:

#### Option 1: Custom Templates (Recommended)
```

---

## ✅ Use context parameter for task dependencies

**URL:** llms-txt#✅-use-context-parameter-for-task-dependencies

**Contents:**
  - 4. **Clear Task Descriptions**

writing_task = Task(
    description="Write article based on research",
    agent=writer,
    context=[research_task],  # Shares research results
    ...
)
python theme={null}

**Examples:**

Example 1 (unknown):
```unknown
### 4. **Clear Task Descriptions**
```

---
