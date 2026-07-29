def summary(data: dict) -> dict:
    return {"documents": len({c["document_name"] for c in data["chunks"]}), "chunks": len(data["chunks"]),
            "entities": len(data["entities"]), "relationships": len(data["relationships"])}
