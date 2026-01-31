---
name: Agent Instructions
description: This file describes the agents available for use in the project.
applyTo: "**"
---

# Agents Available

You have the following agents available for use. Your goal is to be proactive, precise, and organized in managing these resources.

<available_agents>
<agent>
<agentName>Conductor</agentName>
<description>
Orchestrates multi-phase plans by delegating research, implementation, and code review to specialized subagents. Use for complex tasks requiring structured execution.
</description>
<location>.github/agents/conductor.agent.md</location>
</agent>
<agent>
<agentName>Planner</agentName>
<description>
Research context and return findings to parent agent. Use for gathering comprehensive information about a task before implementation.
</description>
<location>.github/agents/.planner.agent.md</location>
</agent>
<agent>
<agentName>Implementer</agentName>
<description>
Execute implementation tasks delegated by the CONDUCTOR agent. Follow strict TDD principles to write tests first, implement minimum code, and verify functionality.
</description>
<location>.github/agents/.implementer.agent.md</location>
</agent>
<agent>
<agentName>Code Reviewer</agentName>
<description>
Review code changes from a completed implementation phase. Verify that the implementation meets requirements and follows best practices.
</description>
<location>.github/agents/.code-reviewer.agent.md</location>
</agent>
</available_agents>
