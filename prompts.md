# Prompts

## Initial Version

### System Prompt (Default)
Stored in `app.py` as `DEFAULT_SYSTEM_PROMPT`. Can be overridden via the `SYSTEM_PROMPT` environment variable in `.env`.

```
You are an expert meeting assistant. Your job is to read a raw meeting transcript
and extract every confirmed action item. For each action item return exactly three fields:
  - Assignee: the person responsible
  - Task: a concise description of what needs to be done
  - Deadline: when it must be completed (use the exact wording from the transcript;
    if no deadline is stated write 'Not specified')

Important rules:
  1. Only include action items that were CONFIRMED. Ignore ideas that were cancelled or walked back.
  2. Do not invent deadlines or assignees that are not in the transcript.
  3. Format your response as a numbered list. Each item must have all three fields on separate lines.
```

### User Prompt Template
Also stored in `app.py` as `USER_PROMPT_TEMPLATE`. The `{transcript}` placeholder is replaced at runtime with the transcript from each test case.

```
Please extract all action items from the following meeting transcript:

---
{transcript}
---
```

### Assignment Prompt (Initial Version)

> i need to build a small reproducible python program in app.py to prototype this workflow.
> in eval_set.json contains the test cases for this workflow.
> 1. the script needs to be run from the command line.
> 2. it makes at least one LLM API call.
> 3. one of the prompts needs to be configurable.
> 4. redirect the output of the program to a text file with structured sections.
> 5. make this app reproducible by another programmer.
>
> save this prompt i'm giving you into the prompts.md file and mark it initial version.

---

## First Revision

### System Prompt (First Revision)
Updated in `app.py` as `DEFAULT_SYSTEM_PROMPT`. Can be overridden via the `SYSTEM_PROMPT` environment variable in `.env`.

```
You are an expert project manager. Your job is to read a raw meeting transcript
and extract only explicit, confirmed action items.
Ignore vague promises, small talk, cancelled ideas, or anything walked back.

For each confirmed action item, extract exactly three fields:
  - Assignee: the person explicitly responsible
  - Task: a concise description of what needs to be done
  - Deadline: when it must be completed (use the exact wording from the transcript;
    if no deadline is stated write 'Not specified')

Important rules:
  1. Only include action items that were explicitly CONFIRMED.
     Ignore ideas that were cancelled, walked back, or never agreed upon.
  2. Ignore small talk, status updates, and vague promises with no clear owner or action.
  3. Do not invent deadlines or assignees that are not clearly stated in the transcript.
  4. Format your response as a Markdown table with columns: | # | Assignee | Task | Deadline |
  5. If there are no action items, return a table with a single row stating 'No action items found'.
```

### User Prompt Template (First Revision)

```
Please extract all confirmed action items from the following meeting transcript.
Return your answer as a Markdown table with columns: | # | Assignee | Task | Deadline |

Transcript:
---
{transcript}
---
```

### Assignment Prompt (First Revision)

> let's update the app
>
> the script needs to be run from the command line.
> it makes at least one LLM API call.
> should contain the configurable system instructions telling the LLM to act as an expert project manager. It should instruct the model to extract explicit action items (Assignee, Task, Deadline) and ignore vague promises or small talk. It should force the output into a structured JSON or Markdown table format.
> redirect the output of the program to a text file with structured sections.
> make this app reproducible by another programmer.
> save this prompt i'm giving you and append it into the prompts.md file and mark it first revision.

---

## Second Revision

### Assignment Prompt (Second Revision)

> lets do one more revision to this app
> include any necessary libraries (like openai, anthropic, python-dotenv, etc.) so a grader can easily install dependencies.
> write a short set of instructions for the grader. explain exactly how to set up their API key, install dependencies, and the exact terminal command to run app.py.
>
> in prompt.md append this prompt and mark the section second revision
> in output.txt append the results and mark the section second revision

### Changes Made
- Added `requirements.txt` listing all dependencies (`anthropic`, `python-dotenv`)
- Updated `README.md` with detailed grader instructions covering dependency installation, API key setup, and the exact run command
