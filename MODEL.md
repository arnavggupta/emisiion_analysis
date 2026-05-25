# Data Model Architecture

The data model for BreatheSG is designed around multi-tenancy, strict source-of-truth tracking, and immutable audit logs. It is implemented in Django's ORM and uses PostgreSQL-compatible features (using standard relational structures that work cross-db, but intended for Postgres in production).

## Core Entities

### 1. `Tenant`
Represents a client company.
* `id` (UUID): Primary key.
* `name` (String): Client's name.
* `created_at` (Datetime): Timestamp of onboarding.

### 2. `EmissionRecord`
The central truth for a single line item of emissions or activity data. Every record belongs to a `Tenant` to guarantee data isolation.
* **Scope Categorization:** `scope` field explicitly tags the record as `Scope 1`, `Scope 2`, or `Scope 3`.
* **Source Tracking:** 
  * `source_system` tracks where the data originated (e.g., SAP, Concur, Utility Portal).
  * `ingestion_timestamp` records exactly when it entered our system.
  * `raw_data` (JSONField) stores the unmodified, exact payload received. This guarantees we never lose original context.
* **Normalization Engine Storage:**
  * `normalized_unit` (e.g., "kg CO2e")
  * `normalized_value` (Float): The computed emissions value.
* **Approval Workflow:**
  * `status`: Tracks the lifecycle (`PENDING`, `APPROVED`, `REJECTED`, `LOCKED`).
  * `last_edited_by` & `last_edited_at`: High-level human tracking (detailed tracking is in the Audit Log).

### 3. `AuditLog`
An immutable log tracking all state changes to an `EmissionRecord`.
* **Source-of-Truth Validation:** Anytime a record changes status (e.g. Approved -> Locked) or value, a new row is appended here.
* `action`: e.g., `STATUS_CHANGED`, `UPDATED`.
* `previous_state` & `new_state` (JSON): Captures a snapshot of the change.
* `changed_by`: Identity of the analyst making the change.
