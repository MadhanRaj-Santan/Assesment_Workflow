# Customer Request Approval System (ApprovalFlow)

A full-stack, responsive, and distributed enterprise application designed to manage customer request submissions and human-in-the-loop approvals using **React**, **FastAPI**, **PostgreSQL**, and **Temporal** for durable workflow orchestration.

---

## 🚀 Overview

The **Customer Request Approval System** solves the challenge of managing asynchronous business processes where actions pause indefinitely waiting for human intervention (such as an owner approving or rejecting a customer submission). By integrating **Temporal workflows and signals**, the system guarantees execution durability, meaning workflows survive server reboots, network failures, or crashes without losing state.

---

## 🛠️ Tech Stack

### **Frontend**
* **React (v19+)** with **Vite** for fast bundling and hot module replacement.
* **React Router** for seamless multi-page routing (`NavLink` with active states).
* **Axios** for robust HTTP client-server communication.
* **Modern CSS3** incorporating responsive grid/flexbox layouts, floating card styles, accessibility focus rings, and soft enterprise status badges.

### **Backend**
* **FastAPI (Python)** for building high-performance asynchronous REST endpoints.
* **SQLAlchemy** (ORM) for object-relational mapping and database interactions.
* **Pydantic** for strict data validation and schema serialization.
* **Uvicorn** as the ASGI server.

### **Workflow Orchestration & Database**
* **Temporal SDK (Python)** for defining durable workflows, signals, activities, and background workers.
* **Temporal Server & Web UI (`v1.29.1`)** running locally via Docker Compose.
* **PostgreSQL (v15)** for persistent data storage (requests, statuses, metadata).
* **Docker & Docker Compose** for containerized service orchestration.

---

## 📂 Project Structure

```text
Customer-Approval-System/
├── docker-compose.yml          # Container orchestration for Postgres, Temporal, and UI
├── .gitignore                  # Git exclusion rules (venv, node_modules, uploads, etc.)
├── server/
│   ├── app/
│   │   ├── api/
│   │   │   ├── customer.py     # Customer endpoints (file upload & request creation)
│   │   │   └── owner.py        # Owner endpoints (fetching list & sending approval signals)
│   │   ├── temporal/
│   │   │   ├── workflows.py    # Temporal Workflow definition & signal handler
│   │   │   ├── activities.py   # Database mutation activities
│   │   │   └── worker.py       # Background worker loop processing task queues
│   │   ├── models/
│   │   │   └── request.py      # SQLAlchemy PostgreSQL models
│   │   ├── schemas/
│   │   │   └── request.py      # Pydantic response & validation schemas
│   │   ├── database.py         # SQLAlchemy engine and session management
│   │   └── main.py             # FastAPI app initialization and router mounting
│   ├── uploads/                # Local secure storage for uploaded customer files
│   └── venv/                   # Python virtual environment
└── frontend/
    ├── src/
    │   ├── components/         # Reusable components (FileUpload, StatusBadge)
    │   ├── pages/              # CustomerDashboard & OwnerDashboard
    │   ├── services/           # Axios API service wrapper
    │   ├── App.jsx             # Root layout and router configuration
    │   └── index.css           # Global enterprise SaaS styling system
    └── package.json            # Frontend dependencies


🔄 Workflow Architecture & Lifecycle
Submission Phase:

A customer fills out their details, provides a description, and attaches a file on the Customer Dashboard.

FastAPI saves the attachment securely to the server/uploads/ directory and creates a database row in PostgreSQL with a initial status of PENDING.

Workflow Initialization:

FastAPI generates a unique temporal_workflow_id and connects to the Temporal server to start the ApprovalWorkflow.

Durable Pause (Human-in-the-Loop):

The workflow enters a suspended state (workflow.wait_condition), idling indefinitely without consuming CPU cycles while waiting for an external signal.

Decision Phase:

The business owner reviews incoming requests on the Owner Dashboard.

Clicking Approve or Reject dispatches an asynchronous Signal (APPROVED or REJECTED) from FastAPI directly to the running Temporal workflow handle.

Activity Execution & Resolution:

Temporal unblocks the workflow and executes the update_request_status activity.

The activity mutates the database record.

The customer dashboard polls the backend every 5 seconds, instantly displaying the updated status pill (APPROVED or REJECTED).

⚙️ Local Setup and Installation
Prerequisites
Python (v3.10+) installed.

Node.js & npm installed.

Docker Desktop running.
