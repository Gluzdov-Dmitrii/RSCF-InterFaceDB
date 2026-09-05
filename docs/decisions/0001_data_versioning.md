# ADR 0001 Git for code and DVC for data

Date: 2026-09-05

Status: accepted for the scaffold; remote configuration pending

## Context

The project begins with large PDFs, DOCX/PPTX partner material and will later generate databases, model files and molecular trajectories. The linked GitHub repository is empty and the local source directory had no Git history at the start of the audit.

## Decision

- Use Git for code, tests, schemas, prompts, plans, search strategies, bibliographic metadata and manuscript sources.
- Keep current binary materials out of Git from the first commit.
- Use DVC for large data and model lineage after a durable institutional or cluster remote is approved.
- Use RO-Crate for published release packaging, not as a replacement for Git or DVC.
- Reconsider DataLad only if selective distribution of many independent datasets becomes a dominant requirement.

## Consequences

The first commit remains lightweight and safe for a public repository. Data reproduction will require access to the appropriate DVC remote. Restricted source files need a separate access policy. DVC setup is blocked until storage ownership, retention and credentials are settled.
