from sqlalchemy import Column, String, DateTime, ForeignKey, UUID
from sqlalchemy.sql import func
import uuid
from backend.app.db.base_class import Base
class Factory(Base):
    __tablename__ = "factories"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
class Area(Base):
    __tablename__ = "areas"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    factory_id = Column(UUID(as_uuid=True), ForeignKey("factories.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
class ProductionLine(Base):
    __tablename__ = "production_lines"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    area_id = Column(UUID(as_uuid=True), ForeignKey("areas.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
class Machine(Base):
    __tablename__ = "machines"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, index=True)
    line_id = Column(UUID(as_uuid=True), ForeignKey("production_lines.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
