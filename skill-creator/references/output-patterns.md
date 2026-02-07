# Output Patterns

This guide presents two primary strategies for generating consistent, quality outputs.

## Template Pattern

Provide structured templates that match your requirements' rigidity.

### Strict Templates

For rigid specifications (API responses, data formats), use exact templates:

```markdown
ALWAYS use this exact template structure:

## Executive Summary
[2-3 sentences summarizing key findings]

## Key Findings
1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

## Recommendations
- [Recommendation 1]
- [Recommendation 2]
```

### Flexible Templates

For situations allowing flexibility:

```markdown
Use this as a sensible default format, but use your best judgment:

## Overview
[Adapt based on what you discover]

## Analysis
[Adjust sections as needed for the specific analysis type]

## Conclusion
[Summarize appropriately]
```

## Examples Pattern

Use input/output pairs when demonstration proves more effective than description.

Examples help Claude understand the desired style and level of detail more clearly than descriptions alone.

### Commit Message Example

```markdown
Format: type(scope): brief description

Followed by detailed explanation if needed.

Examples:

Input: Added user authentication with JWT tokens
Output:
feat(auth): add JWT-based user authentication

Implement secure token generation and validation for user sessions.
Includes refresh token rotation and automatic expiration handling.

Input: Fixed null pointer in user service
Output:
fix(users): handle null user in profile lookup

Add null check before accessing user properties to prevent
NullPointerException when user is not found in database.
```

## Key Takeaway

Choose template strictness based on your use case, and supplement with examples when demonstrating desired output quality matters most.
