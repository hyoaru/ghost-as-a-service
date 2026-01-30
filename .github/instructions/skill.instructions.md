---
name: Skill Instructions
description: This file describes the skills available for use in the project.
applyTo: "**"
---

# Skills Available

You have the following skills available for use. Your goal is to be proactive, precise, and organized in managing these resources. Make sure to identify which tool is the most appropriate, pass along relevant details and execute the actions needed to complete the task

## 1. Scaffold Service Skill

Location: [Scaffold Service Skill](../skills/scaffold-service/SKILL.md)
Orchestrates business logic and manages dependencies. Use when creating a new service or adding operations without modifying the service class.

## 2. Scaffold Repository Skill

Location: [Scaffold Repository Skill](../skills/scaffold-repository/SKILL.md)
Abstracts data access logic with provider-specific implementations (AWS, Postgres, etc.). Use when creating repositories or adding new backend providers.

## 3. Scaffold Utility Skill

Location: [Scaffold Utility Skill](../skills/scaffold-utility/SKILL.md)
Builds reusable helpers, automatically selecting between stateful (Infrastructure Wrapper) or stateless (Atomic Helper) patterns. Use when wrapping external services or creating helper functions.
