from src.tools.get_related_knowledge import get_related_knowledge


class FakeGitHubClient:
    def __init__(self, files):
        self.files = files

    def get_tree(self, ref="main"):
        return [{"path": path, "type": "blob"} for path in self.files]

    def get_file(self, path, ref="main"):
        return self.files[path]


REL_31426 = """---
relationship_id: "REL-TEST-001"
source_id: "31426"
source_type: "TICKET"
relation_type: "relacionado_con"
target_id: "ZMM_IMX_0004"
target_type: "SAP_OBJECT"
knowledge_type: "custom"
knowledge_scope: "ticket"
version: "1.0"
status: "test"
date: "2026-09-01"
author: "test-fixture"
---

# Relationship

Synthetic relationship for testing.
"""

REL_PROCESS = """---
relationship_id: "REL-TEST-002"
source_id: "ZMM_IMX_0004"
source_type: "SAP_OBJECT"
relation_type: "participa_en"
target_id: "SNC_LOGISTICO"
target_type: "PROCESS"
knowledge_type: "mixed"
knowledge_scope: "process"
version: "1.0"
status: "test"
date: "2026-09-01"
author: "test-fixture"
---

# Relationship

Synthetic relationship for testing.
"""

UNRELATED = """---
relationship_id: "REL-TEST-003"
source_id: "33007"
source_type: "TICKET"
relation_type: "relacionado_con"
target_id: "ZTMM_PU_018"
target_type: "SAP_OBJECT"
knowledge_type: "custom"
knowledge_scope: "ticket"
version: "1.0"
status: "test"
date: "2026-09-01"
author: "test-fixture"
---

# Relationship

Synthetic unrelated relationship.
"""


def test_get_related_knowledge_returns_direct_relationships():
    client = FakeGitHubClient(
        {
            "knowledge/relationships/rel-001.md": REL_31426,
            "knowledge/relationships/rel-002.md": REL_PROCESS,
            "knowledge/relationships/rel-003.md": UNRELATED,
        }
    )

    result = get_related_knowledge(client, "TICKET", "31426")

    assert len(result.relationships) == 1
    relation = result.relationships[0]
    assert relation.source_id == "31426"
    assert relation.target_id == "ZMM_IMX_0004"


def test_get_related_knowledge_traverses_target_side():
    client = FakeGitHubClient(
        {
            "knowledge/relationships/rel-001.md": REL_31426,
            "knowledge/relationships/rel-002.md": REL_PROCESS,
        }
    )

    result = get_related_knowledge(client, "SAP_OBJECT", "ZMM_IMX_0004")

    assert len(result.relationships) == 2
    assert {r.path for r in result.relationships} == {
        "knowledge/relationships/rel-001.md",
        "knowledge/relationships/rel-002.md",
    }


def test_get_related_knowledge_does_not_infer_from_other_documents():
    client = FakeGitHubClient(
        {
            "knowledge/sap-objects/object.md": "# ZMM_IMX_0004 mentions 31426",
            "tickets/31426/ticket.md": "# Ticket 31426 mentions ZMM_IMX_0004",
        }
    )

    result = get_related_knowledge(client, "TICKET", "31426")

    assert result.relationships == ()


def test_get_related_knowledge_returns_empty_for_unknown_entity():
    client = FakeGitHubClient(
        {
            "knowledge/relationships/rel-001.md": REL_31426,
        }
    )

    result = get_related_knowledge(client, "TICKET", "99999")

    assert result.relationships == ()
