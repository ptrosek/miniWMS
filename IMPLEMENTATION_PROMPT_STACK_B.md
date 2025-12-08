# Implementation Prompt: WMS Modernization (Stack B)

**Role:** Senior Full Stack Engineer
**Target Stack:** FastAPI (Backend), React + Ant Design + AG Grid (Frontend), PostgreSQL (Database)
**Goal:** Refactor the legacy monolithic Flask WMS into a modern, decoupled Single Page Application (SPA).

---

## 1. Project Overview
You are tasked with rebuilding a Warehouse Management System (WMS) from the ground up. The current system is a Flask app with server-side rendering, using MySQL. The new system must be "Data-First," meaning the API schema (OpenAPI) and Database Models drive the development.

**Key Constraints:**
*   **Database:** Migrate from MySQL to **PostgreSQL**. Use `JSONB` columns for flexible product attributes.
*   **Backend:** **FastAPI** with `SQLAlchemy` (Async) and `Pydantic` v2.
*   **Frontend:** **React** (Vite), **Ant Design** (UI Components), and **AG Grid** (Data Tables).
*   **Auth:** **OAuth2/OIDC** (Prepared for Single Sign-On).

---

## 2. Backend Implementation (FastAPI)
### Step 2.1: Database & Models
*   Define SQLAlchemy models mirroring the core logic (Receipts, Issues, Moves, Inventory).
*   Use Pydantic models for request/response validation.
*   **Crucial:** Ensure the API automatically generates the `openapi.json` spec.

### Step 2.2: AG Grid Integration (Server-Side Row Model)
*   Create a specialized endpoint pattern (e.g., `POST /api/v1/inventory/search`) that accepts AG Grid's "Server-Side Row Model" request payload:
    ```json
    {
      "startRow": 0,
      "endRow": 100,
      "filterModel": { ... },
      "sortModel": [ ... ]
    }
    ```
*   Implement a service helper in Python to translate this JSON into a generic SQLAlchemy query (filtering, sorting, pagination).
*   *Why?* The WMS will handle large datasets. We cannot load all records to the client.

### Step 2.3: Logic Migration
*   Port the business logic from the legacy `app.py` (specifically `views_custom.py` if present) into clean Service classes.
*   *Key Logic to Port:*
    *   **Receipts:** Validating incoming goods against Purchase Orders.
    *   **Issues:** FIFO (First-In-First-Out) logic for stock removal.
    *   **Moves:** Updating bin locations.

---

## 3. Frontend Implementation (React)
### Step 3.1: Scaffolding
*   Initialize a React project using Vite (`npm create vite@latest`).
*   Install dependencies: `antd`, `ag-grid-react`, `ag-grid-community`, `axios`.

### Step 3.2: Layout & Navigation
*   Use Ant Design's `Layout` (Sider, Header, Content) to create a professional admin shell.
*   Create a clean, responsive navigation menu mirroring the defined modules (Dashboard, Inventory, Operations, Settings).

### Step 3.3: The "Data-First" Grid
*   Build a reusable `ServerSideGrid` component wrapping AG Grid.
*   **Functionality:**
    *   It should accept an API URL (e.g., `/api/v1/products`).
    *   It should automatically handle the "datasource" logic to fetch data from FastAPI on scroll/sort/filter.
    *   *Bonus:* Map AG Grid column definitions directly from the Pydantic schema if possible, or define them in a typed config.

---

## 4. Authentication (Preparation for Superset)
*   Do **not** use simple JWT auth. Implement **OAuth2** (Authorization Code flow).
*   Use a provider like Auth0 (dev tier) or Keycloak (Docker) as the identity provider.
*   The frontend should use `react-oidc-context` (or similar) to handle the login flow.
*   *Reason:* This same OIDC provider will be used to log users into Apache Superset.

---

## 5. Deliverables
1.  **`docker-compose.yml`**: Spinning up FastAPI, Postgres, and the React dev server.
2.  **`backend/`**: Complete FastAPI source code with Migrations (Alembic).
3.  **`frontend/`**: Complete React source code.
4.  **`README.md`**: Instructions on how to run the stack and trigger the "Infinite Scroll" demo.
