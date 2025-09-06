from dataclasses import dataclass
from neo4j import Driver

@dataclass
class DbContext:
    """Graphdb context with typed dependencies."""

    driver: Driver