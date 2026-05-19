from sqlalchemy import Column, String, ForeignKey, UUID, Index
from sqlalchemy.orm import relationship
import uuid
from backend.app.db.base_class import Base

class Factory(Base):
    __tablename__ = "factories"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    region_id = Column(UUID(as_uuid=True), ForeignKey("regions.id"), nullable=True, index=True)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))

    areas = relationship("Area", back_populates="factory", cascade="all, delete-orphan")
    region = relationship("Region", back_populates="factories")

class Area(Base):
    __tablename__ = "areas"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    factory_id = Column(UUID(as_uuid=True), ForeignKey("factories.id"), nullable=False, index=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    region_id = Column(UUID(as_uuid=True), ForeignKey("regions.id"), nullable=True, index=True)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))

    factory = relationship("Factory", back_populates="areas")
    production_lines = relationship("ProductionLine", back_populates="area", cascade="all, delete-orphan")

class ProductionLine(Base):
    __tablename__ = "production_lines"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    area_id = Column(UUID(as_uuid=True), ForeignKey("areas.id"), nullable=False, index=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    region_id = Column(UUID(as_uuid=True), ForeignKey("regions.id"), nullable=True, index=True)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))

    area = relationship("Area", back_populates="production_lines")
    machines = relationship("Machine", back_populates="production_line", cascade="all, delete-orphan")

class Machine(Base):
    __tablename__ = "machines"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, index=True)
    description = Column(String)
    line_id = Column(UUID(as_uuid=True), ForeignKey("production_lines.id"), nullable=False, index=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    region_id = Column(UUID(as_uuid=True), ForeignKey("regions.id"), nullable=True, index=True)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))

    production_line = relationship("ProductionLine", back_populates="machines")

# Indexes for tenant isolation enforcement
Index("idx_factory_tenant", Factory.id, Factory.tenant_id)
Index("idx_area_tenant", Area.id, Area.tenant_id)
Index("idx_line_tenant", ProductionLine.id, ProductionLine.tenant_id)
Index("idx_machine_tenant", Machine.id, Machine.tenant_id)
