# Implementation Prompt: Superset Integration (Level 3)

**Role:** DevOps / Data Engineer
**Goal:** deeply integrate Apache Superset with the new WMS (Stack B).
**Scope:** Shared Authentication (SSO) and Automated Tenant Provisioning.

---

## 1. Environment Setup
*   Assume the WMS is running on `http://localhost:3000` (Frontend) and `http://localhost:8000` (Backend).
*   Deploy Apache Superset using Docker Compose (`docker-compose-non-dev.yml`).
*   Ensure Superset can reach the WMS PostgreSQL database (shared network).

---

## 2. Shared Authentication (SSO)
**Goal:** A user logs into the WMS via OIDC (e.g., Keycloak) and clicks "Analytics". They are redirected to Superset and automatically logged in without a second password prompt.

### Step 2.1: Superset Configuration
*   Create/Edit `docker/pythonpath_dev/superset_config.py`.
*   Enable OAuth:
    ```python
    from flask_appbuilder.security.manager import AUTH_OAUTH
    AUTH_TYPE = AUTH_OAUTH
    OAUTH_PROVIDERS = [
        {
            'name': 'wms-sso',
            'token_key': 'access_token',
            'icon': 'fa-address-card',
            'remote_app': {
                'client_id': 'superset-client',
                'client_secret': '...',
                'api_base_url': 'https://<your-oidc-provider>/',
                'client_kwargs': {'scope': 'openid profile email'},
                'access_token_url': 'https://<your-oidc-provider>/token',
                'authorize_url': 'https://<your-oidc-provider>/auth',
            }
        }
    ]
    ```
*   **Critical:** Map OIDC roles to Superset roles. Use `AUTH_ROLES_MAPPING` to ensure a WMS "Manager" gets Superset "Alpha" access automatically.

---

## 3. Automated Provisioning (The "Level 3" Magic)
**Goal:** When the WMS creates a new "Client" or "Tenant", programmatically setup their analytics environment.

### Step 3.1: The Provisioning Script
*   Write a Python script (or FastAPI background task) using `superset-api-client`.
*   **Function:** `provision_client_analytics(client_id, db_connection_string)`

### Step 3.2: Workflow Implementation
1.  **Auth with Superset API:** The script must first log in to Superset as an Admin to get a JWT.
2.  **Create Database Connection:**
    *   POST to `/api/v1/database/`.
    *   Pass the PostgreSQL connection string. *Tip: If multi-tenancy is logical (one DB, many clients), use Jinja templating in the connection string or RLS.*
3.  **Create User:**
    *   POST to `/api/v1/security/users/` to create a specific dashboard viewer user for that client (if not using SSO for them).
4.  **Clone Dashboard:**
    *   Superset allows exporting/importing dashboards via ZIP.
    *   Maintain a "Master Template" dashboard (JSON/YAML).
    *   On provisioning, inject the specific `database_id` for the new client into this template and upload it via `/api/v1/dashboard/import/`.

---

## 4. Deliverables
1.  **`superset_config.py`**: A hardened configuration file with OAuth enabled.
2.  **`provisioning_service.py`**: A robust Python module containing the logic to drive the Superset API.
3.  **`integration_guide.md`**: A step-by-step guide on how to register the OIDC clients for both WMS and Superset to ensure the "handshake" works.
