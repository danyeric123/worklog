# Work Log Tool

This repository provides a simple CLI for recording and reviewing your daily work log. The core idea is inspired by Gergely Orosz's [blog post](https://blog.pragmaticengineer.com/work-log-template-for-software-engineers/) on maintaining a “work log” to track code changes, reviews, discussions, and other efforts.

## Why Keep a Work Log?

- **Visibility of Work**: Avoid “invisible work” by documenting tasks, meetings, reviews, and more.
- **Prioritization**: Know what’s on your plate and decide what to focus on.
- **Performance Reviews**: Quickly reference achievements, leading to smoother self-assessments and promotions.
- **Better Planning**: Helps with saying “no” when overloaded, or adjusting priorities.

## Best Practices for Work Logging

### 1. Track Regularly

- Log work daily or weekly, not retrospectively
- Fresh details are more accurate and complete
- Set a recurring calendar reminder

### 2. Be Specific and Measurable

✅ Good Example:

```markdown
- Optimized database queries
  - Reduced average response time from 2s to 200ms
  - Impacted 3 critical API endpoints
  - Ticket: PROJ-123
```

❌ Poor Example:

```markdown
- Made some database improvements
```

### 3. Include "Invisible Work"

- Mentoring and pair programming sessions
- Code reviews and technical discussions
- Helping others debug issues
- Documentation improvements
- Knowledge sharing

### 4. Structure Your Entries

- Start with the main task/project
- Add specific sub-items for:
  - What you did
  - Impact/results
  - Related tickets/PRs
  - Collaborators involved

### 5. Connect Work to Impact

✅ Good Example:

```markdown
- Implemented API rate limiting
  - Prevented abuse of free tier
  - Reduced infrastructure costs by 15%
  - Protected service availability during traffic spikes
```

❌ Poor Example:

```markdown
- Added rate limiting to API
```

### 6. Regular Review

- Review logs monthly
- Use for:
  - Performance reviews
  - Planning discussions
  - Team retrospectives
  - Career growth tracking

## How It Works

- **Monthly Log Files**: Each month has its own Markdown file.
- **Daily Entries**: Each day is prefixed with a date header and relevant category headers (e.g., Projects, Code Reviews).
- **Configurable**: A YAML config file lets you customize categories and behavior (e.g., auto-commit to git).
- **CLI Commands**:
  - `python log_script.py log` – prompts you for daily work entries.
  - `python log_script.py view --month YYYY-MM` – view logs for a given month.
  - `python log_script.py init` – create or overwrite the default configuration.

## Getting Started

1. **Install dependencies**:

   ```bash
   uv sync
   ```

2. **Initialize Configuration**:

   ```bash
   uv run python log_script.py init
   ```

3. **Start Logging**:

   ```bash
   uv run python ./log_script.py log
   ```

## Configuration

The `worklog_config.yaml` file contains:

- `categories` – adjustable list of log sections.
- `git_auto_commit` – whether to auto-commit changes to Git.
