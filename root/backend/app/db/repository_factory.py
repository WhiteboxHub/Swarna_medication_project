import os
from app.db.repository import InMemoryRepository
from app.db.documentdb import DocumentDBRepository


_repo = None


# def get_repository():
#     global _repo
#     if _repo:
#         return _repo

#     if os.getenv("USE_LOCAL_STORE") == "1":
#         _repo = InMemoryRepository()
#         return _repo

#     mongo_uri = os.getenv("DOCUMENTDB_URI")
#     if not mongo_uri:
#         raise RuntimeError("DOCUMENTDB_URI not set")

#     _repo = DocumentDBRepository(
#         uri=mongo_uri,
#         db_name=os.getenv("DOCUMENTDB_NAME", "medication_db"),
#     )
#     return _repo

def get_repository():
    global _repo
    if _repo:
        return _repo

    use_local = os.getenv("USE_LOCAL_STORE", "1") == "1"

    if use_local:
        _repo = InMemoryRepository()
        return _repo

    mongo_uri = os.getenv("DOCUMENTDB_URI")
    if not mongo_uri:
        raise RuntimeError(
            "DOCUMENTDB_URI not set. "
            "Set USE_LOCAL_STORE=1 for local development."
        )

    _repo = DocumentDBRepository(
        uri=mongo_uri,
        db_name=os.getenv("DOCUMENTDB_NAME", "medication_db"),
    )
    return _repo
