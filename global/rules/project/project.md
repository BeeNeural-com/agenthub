# Project

This page contains the custom instructions for project.

## Instructions

Click the copy button to copy the entire instruction content.

````markdown
---
description: 'Project-level custom instruction example for a web application'
applyTo: '*'
---

# Project Instructions

## Overview

This project is a full-stack web application composed of three primary components:  
1. **Backend Services** – Contain business logic, authentication, data validation, and integration with other internal or external systems.  
2. **Frontend Application** – Provides the user interface and interacts with the backend through APIs.  
3. **Database Layer** – Stores, retrieves, and manages persistent data for the application.  

The main objective of this project is to create a modular and maintainable system that can be easily extended or scaled in the future.

## Architecture Summary

```
[Frontend]  →  [Backend Services]  →  [Database]
     ↓                ↑
   User UI        REST/GraphQL
```

- **Frontend:** Sends and receives data through REST or GraphQL APIs.  
- **Backend:** Contain business logic, authentication, data validation, and integration with other internal or external systems.   
- **Database:** Acts as the persistent layer for all entities and transactions.

> Note: This structure represents a simplified conceptual model, only for example purpose.  
> In production environments, additional layers (e.g., caching, messaging, authentication gateways, or external integrations) may exist depending on the system design.

## Folder Structure

- A typical folder layout for this project is as follows:

    ```
    root/
    ├── backend/
    │   ├── src/
    │   ├── tests/
    │   ├── requirements.txt / pyproject.toml / package.json
    │   └── README.md
    ├── frontend/
    │   ├── src/
    │   ├── public/
    │   ├── package.json
    │   └── README.md
    ├── database/
    │   ├── migrations/
    │   ├── seeds/
    │   └── schema.sql
    ├── docker/
    │   ├── backend.Dockerfile
    │   ├── frontend.Dockerfile
    │   └── docker-compose.yml
    └── README.md
    ```

- Each component has its own `README.md` explaining setup, configuration, and usage details.

````
