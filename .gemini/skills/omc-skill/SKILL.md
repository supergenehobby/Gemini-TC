---
name: omc-skill
description: Autonomous multi-agent orchestration for Gemini CLI. Use when the user requests "team mode", "autopilot", "ralph", "ultrawork", or requires specialized agents (Architect, Tester, etc.) for complex engineering tasks.
---

# 🤖 Oh-My-Gemini (OMC) Orchestration

This skill transforms Gemini CLI into a coordinated team of specialized agents, enabling parallel execution, autonomous loops, and high-integrity development.

## 🚀 Core Commands & Triggers

Use these triggers to activate specific orchestration modes:
- **`team:`** Starts the structured 5-stage pipeline (`plan` → `prd` → `exec` → `verify` → `fix`).
- **`autopilot:`** Full autonomous mode. Executes research, implementation, and verification until the user-defined goal is met.
- **`ralph:`** Persistence mode. Re-runs implementation and verification loops until all tests pass. "Never give up."
- **`ultrawork:`** Parallel processing mode. Use for bulk tasks (e.g., "Fix all lint errors in src/"). Splits work into multiple `generalist` calls.
- **`interview:`** Start the Socratic questioning phase using [deep_interview.md](references/deep_interview.md).
- **`setup:` / `omc-setup:`** Initialize the project environment and verify toolchains (Node, Git, etc.).
- **`role:[AgentName]:`** Force the sub-agent to assume a specific profile from `references/agent_profiles.md`.

## 🏁 Structured Workflows

### 1. Team Mode Protocol
When `team:` is triggered, strictly follow the stages defined in [team_protocol.md](references/team_protocol.md).
1. **Deep Interview (Clarify)**: (Optional/Recommended) Run `interview:` if requirements are vague.
2. **Architect (Plan)**: Map architecture and dependencies.
...
### 4. Deep Interview (Socratic)
When `interview:` is triggered, strictly follow the protocol in [deep_interview.md](references/deep_interview.md). Ask only one or two questions at a time to keep the user engaged.

### 5. Setup / OMC-Setup
1. **Verify Environment**: Check OS, Node.js version, and core dependencies.
2. **Scan Tools**: Check for ESLint, Prettier, Jest, Vitest, etc.
3. **Configure**: Suggest optimized scripts for `package.json` to support `ultrawork` and `team` modes.

2. **Product Owner (PRD)**: Define requirements and success criteria.
3. **Developer (Exec)**: Surgical implementation.
4. **Tester (Verify)**: Automated and manual verification.
5. **Fixer (Fix)**: Address any failures found.

### 2. Ralph (Persistence) Loop
1. **Reproduce**: Confirm the failure/bug with a test case.
2. **Fix**: Implement the fix.
3. **Verify**: Run tests.
4. **Iterate**: If tests fail, analyze the logs and repeat from Step 2. Max 5 iterations before asking for user hint.

### 3. Autopilot (Autonomous)
1. **Research**: Systematically map the codebase.
2. **Strategy**: Propose a comprehensive execution plan.
3. **Execution**: Implement all sub-tasks using the **Plan-Act-Validate** cycle.
4. **Final Validation**: Run full build and test suites.

## 👥 Specialized Agents
Refer to [agent_profiles.md](references/agent_profiles.md) for detailed role definitions.
- **Architect**: System design & strategy.
- **Tester**: Verification & edge cases.
- **Researcher**: Codebase mapping & documentation.
- **Developer**: Implementation & idiomatic code.

## 🛠️ Usage Guidelines
- Always prioritize **verification** (tests) before declaring a task finished.
- For large tasks, use `ultrawork` to delegate sub-tasks to `generalist` instances in parallel.
- Maintain a **HUD (Heads-Up Display)** mindset: Report task progress (e.g., "[Team-Plan] Complete. Moving to [Team-PRD]") to keep the user informed.
