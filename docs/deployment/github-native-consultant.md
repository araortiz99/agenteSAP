# GitHub-native AgenteSAP

This workflow provides a no-hosting execution path for AgenteSAP.

## Usage

Open **Actions → AgenteSAP Consultation → Run workflow**, enter the SAP
question and optionally a ticket ID.

The workflow runs with repository read permission only. It does not enable
QAS and does not expose an HTTP endpoint.

The next implementation step is to connect the workflow input to the same
consultant entry point used by the CLI and publish the structured response as
a workflow artifact.