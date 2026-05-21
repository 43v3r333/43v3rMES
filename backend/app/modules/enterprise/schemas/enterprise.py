from typing import Optional, List, Any, Dict
from pydantic import BaseModel
import uuid
from datetime import datetime

class OrganizationBase(BaseModel):
    name: str
    description: Optional[str] = None

class OrganizationCreate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    class Config: from_attributes = True

class RegionBase(BaseModel):
    name: str
    organization_id: uuid.UUID

class RegionCreate(RegionBase):
    pass

class Region(RegionBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    class Config: from_attributes = True

class SiteComparisonItem(BaseModel):
    site_id: uuid.UUID
    site_name: str
    region_name: str
    availability: float
    mttr: float
    mtbf: float
    open_incidents: int

class EnterpriseOverview(BaseModel):
    total_sites: int
    active_incidents_total: int
    critical_risk_sites: int
    top_performing_site: str
    bottom_performing_site: str
    enterprise_availability: float
