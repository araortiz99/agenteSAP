def document_links(document_id, entities, record_id, limit=32):
    if limit < 1:
        raise ValueError("link limit must be greater than zero")
    return tuple((document_id, item.value, item.entity_type, record_id) for item in entities[:limit])
