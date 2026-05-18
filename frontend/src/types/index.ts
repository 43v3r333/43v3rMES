export type DowntimeStatus = 'OPEN' | 'IN_PROGRESS' | 'RESOLVED' | 'CLOSED';
export type DowntimeSeverity = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

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

export interface DowntimeEvent {
  id: string;
  event_number: string;
  title: string;
  description?: string;
  factory_id: string;
  area_id: string;
  production_line_id: string;
  status: DowntimeStatus;
  severity: DowntimeSeverity;
  category_id?: string;
  started_at: string;
  ended_at?: string;
  duration_minutes?: number;
  root_cause?: string;
  resolution_notes?: string;
  reported_by?: string;
  assigned_to?: string;
  tenant_id: string;
  created_at: string;
}

export interface DowntimeEventCreate {
  title: string;
  description?: string;
  factory_id: string;
  area_id: string;
  production_line_id: string;
  started_at: string;
  machine_ids: string[];
}

export interface DowntimeEventUpdate {
  title?: string;
  description?: string;
  root_cause?: string;
  resolution_notes?: string;
  status?: DowntimeStatus;
  severity?: DowntimeSeverity;
  ended_at?: string;
}

export interface Shift {
  id: string;
  name: string;
  start_time: string;
  end_time: string;
  factory_id: string;
  is_active: boolean;
}

export interface ShiftCreate {
  name: string;
  start_time: string;
  end_time: string;
  factory_id: string;
}

export interface ShiftHandover {
  id: string;
  outgoing_shift_id: string;
  incoming_shift_id: string;
  supervisor_id: string;
  date: string;
  operational_concerns?: string;
  maintenance_notes?: string;
  production_risks?: string;
  escalation_tracking?: string;
  tenant_id: string;
}

export interface ShiftHandoverCreate {
  outgoing_shift_id: string;
  incoming_shift_id: string;
  supervisor_id: string;
  date: string;
  operational_concerns?: string;
  maintenance_notes?: string;
  production_risks?: string;
  escalation_tracking?: string;
  carryover_event_ids: string[];
}

export interface KPIResponse {
  mttr: number;
  mtbf: number;
  availability: number;
  downtime_percentage: number;
  open_issue_count: number;
  escalation_count: number;
}

export interface ParetoItem {
  label: string;
  value: number;
  percentage: number;
  cumulative_percentage: number;
}

export interface AgingIssue {
  event_number: string;
  title: string;
  age_hours: number;
  status: string;
  severity: string;
}

export interface Notification {
  id: string;
  title: string;
  message: string;
  type: string;
  severity: string;
  is_read: boolean;
  is_acknowledged: boolean;
  link_to_entity_type?: string;
  link_to_entity_id?: string;
  created_at: string;
}

export interface EscalationRule {
  id: string;
  name: string;
  entity_type: string;
  condition_type: string;
  threshold_value: number;
  escalate_to_role?: string;
  new_severity?: string;
  is_active: boolean;
}

export interface MachineStatus {
  machine_id: string;
  name: string;
  code: string;
  status: 'RUNNING' | 'IDLE' | 'DOWN';
  active_event_id?: string;
}

export interface ActiveIncident {
  id: string;
  event_number: string;
  title: string;
  severity: string;
  started_at: string;
  duration_minutes: number;
  machines: string[];
}

export interface OperationsOverview {
  active_incident_count: number;
  critical_alert_count: number;
  mttr_last_24h: number;
  availability_score: number;
  current_shift_name: string;
  supervisor_on_duty: string;
}

export type WorkOrderStatus = 'OPEN' | 'ASSIGNED' | 'IN_PROGRESS' | 'WAITING_PARTS' | 'COMPLETED' | 'VERIFIED' | 'CLOSED';
export type WorkOrderPriority = 'EMERGENCY' | 'HIGH' | 'MEDIUM' | 'LOW';
export type WorkOrderType = 'CORRECTIVE' | 'PREVENTIVE' | 'EMERGENCY' | 'INSPECTION';

export interface WorkOrder {
  id: string;
  work_order_number: string;
  title: string;
  description?: string;
  machine_id: string;
  status: WorkOrderStatus;
  priority: WorkOrderPriority;
  type: WorkOrderType;
  assigned_to?: string;
  due_date?: string;
  completed_at?: string;
  labor_hours: number;
  tenant_id: string;
  created_at: string;
}

export interface WorkOrderCreate {
  title: string;
  description?: string;
  machine_id: string;
  priority: WorkOrderPriority;
  type: WorkOrderType;
  due_date?: string;
}

export interface WorkOrderUpdate {
  title?: string;
  status?: WorkOrderStatus;
  priority?: WorkOrderPriority;
  assigned_to?: string;
  maintenance_notes?: string;
  resolution_summary?: string;
  labor_hours?: number;
}

export interface PMSchedule {
  id: string;
  name: string;
  description?: string;
  machine_id: string;
  interval_days?: number;
  runtime_threshold_hours?: number;
  next_due_at?: string;
  is_active: boolean;
}

export type ReportStatus = 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED';
export type ExportFormat = 'CSV' | 'XLSX' | 'PDF';

export interface ReportTemplate {
  id: string;
  name: string;
  report_type: string;
  filters_json?: Record<string, any>;
  tenant_id: string;
  created_at: string;
}

export interface ReportRequest {
  id: string;
  report_type: string;
  format: ExportFormat;
  status: ReportStatus;
  parameters?: Record<string, any>;
  started_at?: string;
  completed_at?: string;
  file_path?: string;
}

export interface ReportRequestCreate {
  report_type: string;
  format: ExportFormat;
  parameters?: Record<string, any>;
}
