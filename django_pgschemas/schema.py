from contextvars import ContextVar
from typing import Optional

from .signals import schema_activate

_active: ContextVar["Optional[Schema]"] = ContextVar("active_schema", default=None)


def __getattr__(name):
    from warnings import warn

    if name == "SchemaDescriptor":
        warn("'SchemaDescriptor' is deprecated, use 'Schema' instead", DeprecationWarning)
        return globals()["Schema"]

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def get_default_schema() -> "Schema":
    return Schema.create("public")


def get_current_schema() -> "Schema":
    current_schema = _active.get()
    return current_schema or get_default_schema()


def activate(schema: "Schema"):
    if not isinstance(schema, Schema):
        raise RuntimeError("'activate' must be called with a Schema descendant")

    _active.set(schema)
    schema_activate.send(sender=Schema, schema=schema)


def deactivate():
    _active.set(None)
    schema_activate.send(sender=Schema, schema=Schema.create("public"))


activate_public = deactivate


class Schema:
    schema_name = None
    domain_url = None
    folder = None

    is_dynamic = False

    @staticmethod
    def create(schema_name: str, domain_url: Optional[str] = None, folder: Optional[str] = None) -> "Schema":
        schema = Schema()
        schema.schema_name = schema_name
        schema.domain_url = domain_url
        schema.folder = folder
        return schema

    def __enter__(self):
        self._previous_schema = get_current_schema()
        activate(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        _previous_schema = getattr(self, "_previous_schema", None)
        activate(_previous_schema) if _previous_schema else deactivate()
