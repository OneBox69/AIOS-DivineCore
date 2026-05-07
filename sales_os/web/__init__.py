"""HTTP-facing layer for Sales OS — FastAPI routers + Jinja templates.

Routers exported here are mounted by `divinecore-v2/api/main.py`.
"""

from .upwork_routes import router as upwork_router

__all__ = ["upwork_router"]
