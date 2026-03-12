# Final Requirement Document (FRD) - Solitaire Garden City

## 1. Project Overview
- **Title**: Solitaire Garden City (Working Title)
- **Target**: North American Females (40-65)
- **Genre**: Solitaire (Tripeaks) + City Decoration

## 2. Core Logic Clarifications
- **Meta-Core Relationship**: Parallel structure. Decoration does not hard-gate solitaire progress.
- **Animation Strategy**: High priority on "Visual Juice" and fluidity.
- **Undo Behavior**: Simple state reversal for streak meter. No penalties.
- **Gimmick Execution**: Sequential playback for chain reactions.

## 3. Data & Network Integrity
- **Deduction Policy**: Immediate currency deduction upon request trigger.
- **Sync Policy**: Server-response required before executing decoration actions.
- **State Recovery**: If interrupted, the state must reflect the deducted currency and updated building status upon restart.

## 4. QA Focus Areas
- High-quality animation performance on target devices.
- Immediate data commitment during interrupted sessions.
- Correct sequence of gimmick triggers.
