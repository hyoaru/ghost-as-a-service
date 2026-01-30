---
name: Skill Instructions
description: This file describes the skills available for use in the project.
applyTo: "**"
---

# Skills Available

You have the following skills available for use. Your goal is to be proactive, precise, and organized in managing these resources. Make sure to identify which tool is the most appropriate, pass along relevant details and execute the actions needed to complete the task.

<available_skills>
  <skill>
    <name>scaffold-service</name>
    <description>
    Orchestrates business logic and manages dependencies. Use when creating a new service or adding operations without modifying the service class.
    </description>
    <location>.github/skills/scaffold-service/SKILL.md</location>
  </skill>
  <skill>
    <name>scaffold-repository</name>
    <description>
    Abstracts data access logic with provider-specific implementations (AWS, Postgres, etc.). Use when creating repositories or adding new backend providers.
    </description>
    <location>.github/skills/scaffold-repository/SKILL.md</location>
  </skill>
  <skill>
    <name>scaffold-utility</name>
    <description>
    Builds reusable helpers, automatically selecting between stateful (Infrastructure Wrapper) or stateless (Atomic Helper) patterns. Use when wrapping external services or creating helper functions.
    </description>
    <location>.github/skills/scaffold-utility/SKILL.md</location>
  </skill>
</available_skills>