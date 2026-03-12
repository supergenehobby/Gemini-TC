# 🏁 Team Orchestration Protocol

The "Team Mode" follows a staged pipeline to ensure high-quality and verified results.

## 📝 1. Team-Plan (The Architect)
- **Goal**: Define the "What" and "How" before implementation.
- **Outcome**: A structured plan including directory structure, dependencies, and risk assessment.
- **Action**: Use `references/agent_profiles.md#Architect`.

## 📘 2. Team-PRD (The Product Owner)
- **Goal**: Define the exact requirements and success criteria.
- **Outcome**: A PRD-style document with user stories and acceptance criteria.
- **Action**: Confirm the plan and define what "Done" looks like.

## 🚀 3. Team-Exec (The Developer)
- **Focus**: Surgical implementation.
- **Outcome**: High-quality code following the plan.
- **Action**: Use `references/agent_profiles.md#Developer`.

## ✅ 4. Team-Verify (The Tester)
- **Goal**: Ensure the change is correct and hasn't introduced regressions.
- **Outcome**: Test results, coverage report, and verification confirmation.
- **Action**: Use `references/agent_profiles.md#Tester`.

## 🛠️ 5. Team-Fix (The Fixer)
- **Goal**: Address any failures found in Team-Verify.
- **Outcome**: Final verified implementation.
- **Action**: If tests fail, go back to Exec and then Verify until success.
