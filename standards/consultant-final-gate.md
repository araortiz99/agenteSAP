# Consultant Final Gate

The final gate certifies the read-only SAP consultant core.

## Required behavior

A consultation must be able to:

1. distinguish SAP Standard from business knowledge;
2. preserve authority and provenance;
3. distinguish documented facts from inference;
4. expose evidence gaps;
5. expose unresolved conflicts;
6. avoid treating candidate or superseded knowledge as current truth;
7. remain read-only;
8. produce a structured, traceable consultant response.

## Out of scope

QAS runtime and SAP database access are not required for this gate.

## Acceptance contract

The gate fails if:

- an authoritative business fact loses its authority metadata;
- superseded knowledge supports a current conclusion;
- a documented conflict is hidden;
- a missing required source is silently ignored;
- a conclusion has no supporting evidence;
- the response claims runtime state without runtime evidence;
- a write capability is exposed by the consultant path.

## Evidence hierarchy

The gate does not impose a universal truth hierarchy between SAP Standard and company knowledge. Applicability and scope determine which source is authoritative for a particular question.

Within governed business knowledge:

authoritative > reference > candidate > superseded

This ordering controls current applicability, not historical relevance.
