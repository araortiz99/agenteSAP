# GitHub-native Consultation Interface

GitHub Issues are the immediate interface for AgenteSAP when no remote hosting is available.

## Flow

1. Create an Issue with the SAP incident/question.
2. The workflow executes AgenteSAP in read-only mode.
3. The structured consultant response is published as an Issue comment.
4. The JSON response is retained as a workflow artifact.

An existing Issue can be explicitly routed by adding the `agentesap` label.

## Security

- QAS/runtime remains disabled.
- No SAP write capability is introduced.
- Repository access is read-only.
- `issues: write` is limited to publishing the generated comment.
- Do not put credentials, tokens or passwords in Issues.
