from aioli import Package

from .service import DatabaseService
from .config import ConfigSchema


export = Package(
    name="aioli_rdbms",
    version="0.1.0",
    description="ORM and CRUD Service for Aioli with support for MySQL and PostgreSQL",
    controllers=[],
    services=[DatabaseService],
    config=ConfigSchema,
)
