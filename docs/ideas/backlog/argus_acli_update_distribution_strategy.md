# Idea: Argus ACLI Update & Distribution Strategy

---

## Metadata

- Status: Backlog  
- Priority: Medium  
- Category: Architecture / Distribution / Productization  
- Origin: Email / Concept Capture  

---

## Summary

Define a structured **update and distribution strategy** for Argus ACLI to ensure:

- consistent user environments  
- controlled updates  
- rollback capability  
- scalable distribution as adoption grows  

This system will evolve from simple Git-based updates into a controlled, versioned distribution model aligned with NeuroCore principles.

---

## Core Concept

Start with a minimal, transparent update model and evolve toward:

> controlled, observable, and reproducible distribution

The system should:

- remain simple in early stages  
- avoid premature packaging complexity  
- preserve system integrity and traceability  

---

## Problem This Solves

Without a defined update strategy, distribution risks include:

- inconsistent user environments  
- breaking changes during updates  
- lack of rollback capability  
- poor user experience as adoption grows  

---

## Current State

- NeuroCore is under active development  
- Argus ACLI is not yet formally packaged  
- no update mechanism exists  
- Git repository is the single source of truth  

---

## Structure / Design

### Phase 1 – Git-Based Updates

- install via:
  ```
  git clone
  ```
- update via:
  ```
  git pull
  ```
- document clearly in README  
- no automation  

Goal:
- simplicity  
- transparency  

---

### Phase 2 – CLI Update Command

Introduce:

```
argus update
```

Behavior:

- executes `git pull`  
- performs dependency updates (if required)  

Goal:
- improved usability  
- minimal abstraction  

---

### Phase 3 – Versioned Releases

Introduce:

- version tagging:
  - v0.x → early builds  
  - v1.0 → stable  

Capabilities:

- version pinning  
- rollback support  
- GitHub Releases integration  

Goal:
- stability  
- reproducibility  

---

### Phase 4 – Packaged Distribution

Potential options:

- install script (`curl | bash`)  
- `.deb` package  
- container image  

Goal:
- simplified installation for broader audience  
- enable non-technical users  

---

## Design Constraints

- avoid breaking changes without versioning  
- runtime and Argus distribution must remain loosely coupled  
- updates must NOT bypass control plane integrity  
- documentation must align with each release  
- system state must remain reproducible across versions  

---

## Integration Points

- Argus CLI (update commands)  
- repository structure and release process  
- documentation (README, install guides)  
- control plane integrity model  
- future manifest-driven systems  

---

## Strategic Purpose

- enable reliable distribution of Argus ACLI  
- improve user experience and adoption  
- support transition from project → product  
- maintain system integrity across environments  
- align with long-term platform scalability  

---

## Success Indicators

- users can reliably update without breakage  
- consistent behavior across installations  
- ability to rollback to known working versions  
- reduced support friction for updates  
- clean version history and release structure  

---

## Risks

- over-engineering update system too early  
- introducing hidden behavior in updates  
- breaking compatibility between runtime and Argus layers  
- inconsistent update processes across versions  

---

## Mitigation

- start with simple Git-based approach  
- introduce features incrementally  
- keep update logic transparent  
- enforce versioning before introducing complexity  
- validate each phase before expanding  

---

## Dependencies / Execution Gate

This idea should be implemented when:

- Argus ACLI is ready for distribution  
- core functionality is stable enough for external users  
- documentation is consistent and complete  

---

## Long-Term Vision

- manifest-driven update system  
- selective tool updates  
- compatibility checks between runtime and Argus layers  
- controlled rollout strategies  
- reproducible environment snapshots  

---

## Future Enhancements

- `argus version`  
- `argus rollback`  
- update manifests  
- compatibility validation system  
- partial updates / modular distribution  

---

## Notes

Start simple.

Do NOT:

- introduce packaging complexity too early  
- hide update behavior from the user  

Design early to avoid future constraints, but implement gradually.

All update behavior must align with:

> controlled, observable, reproducible system execution