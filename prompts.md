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

---

## Original Task Prompt (from assignment)

> i need to build a small reproducible python program in app.py to prototype this workflow.
> in eval_set.json contains the test cases for this workflow.
> 1. the script needs to be run from the command line.
> 2. it makes at least one LLM API call.
> 3. one of the prompts needs to be configurable.
> 4. redirect the output of the program to a text file with structured sections.
> 5. make this app reproducible by another programmer.
>
> save this prompt i'm giving you into the prompts.md file and mark it initial version.
