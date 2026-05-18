export interface Permission {
  id: string;
  name: string;
  description?: string;
}

export interface Role {
  id: string;
  name: string;
  description?: string;
  permissions: Permission[];
}

export interface User {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  is_superuser: boolean;
  tenant_id: string | null;
  roles: Role[];
}

export interface Tenant {
  id: string;
  name: string;
  slug: string;
  is_active: boolean;
}

export interface Factory {
  id: string;
  name: string;
  description?: string;
  tenant_id: string;
  created_at: string;
  updated_at: string;
}

export interface FactoryCreate {
  name: string;
  description?: string;
}

export interface Machine {
  id: string;
  name: string;
  code: string;
  description?: string;
  line_id: string;
  tenant_id: string;
  created_at: string;
}

export interface MachineCreate {
  name: string;
  code: string;
  description?: string;
  line_id: string;
}
