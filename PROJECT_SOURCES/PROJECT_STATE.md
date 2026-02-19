# 🐾 Dog-Eared – Project State (V1 Stable)

## 1️⃣ Project Identity

**Name:** Dog-Eared  
**Purpose:** Personal reading system with physical “trophy shelf”
emphasis  
**Primary User:** Relic  
**Design Goal:** Cozy, structured, expandable, invite-only

Dog-Eared supplements Goodreads. It focuses on:

-   Capturing recommendations
-   Tracking sources
-   Managing inbox
-   Converting items to owned shelf
-   Displaying a visual trophy case
-   Learning backend systems + APIs + Docker

------------------------------------------------------------------------

## 2️⃣ Architecture

### Backend

-   FastAPI
-   SQLModel
-   SQLite (current)
-   JWT auth (HS256)
-   bcrypt hashing (72-byte safe)
-   Docker container
-   Port: 8000

### Frontend

-   React (Vite)
-   Tailwind CSS
-   Protected routes via auth wrapper
-   Responsive (mobile + desktop)
-   Docker container
-   Port: 5173

### Networking

Frontend API base:

``` ts
const API_BASE = `http://${window.location.hostname}:8000`;
```

Windows network must be set to **Private**.

------------------------------------------------------------------------

## 3️⃣ Authentication System

### Endpoints

-   POST /auth/login
-   GET /auth/me

### Behavior

-   JWT Bearer token required
-   Token stored client-side
-   Verified via Swagger + curl

### Fixes Applied

-   bcrypt 72-byte password limit enforced
-   email-validator dependency added
-   Double “Bearer” prefix issue resolved
-   SQLModel UUID `.hex` issue fixed
-   bcrypt backend mismatch resolved

------------------------------------------------------------------------

## 4️⃣ Intake System

### Endpoints

-   POST /intake
-   GET /intake

### Model

-   id (UUID)
-   raw_text
-   status (“new”)
-   captured_at
-   source_id (optional)
-   source_post_url (optional)

Status: Working. Auth protected.

------------------------------------------------------------------------

## 5️⃣ Sources System

### Endpoints

-   POST /sources
-   GET /sources

### Model

-   id
-   type (family, tiktok, etc.)
-   name
-   url (optional)
-   notes (optional)
-   created_at

Used in Capture dropdown. Auth protected.

------------------------------------------------------------------------

## 6️⃣ Owned Shelf System

### Endpoints

-   GET /owned
-   POST /owned
-   POST /owned/from-intake/{intake_id}
-   DELETE /owned/{owned_id}

### Model

-   id
-   title
-   author
-   format
-   is_favorite
-   acquired_at
-   notes
-   created_at
-   user_id

Status: Fully working via Swagger + frontend.

------------------------------------------------------------------------

## 7️⃣ Owned Page – Current Visual System

### Sections

1.  Add Form
2.  Trophy Case (is_favorite = true)
3.  Shelf (non-favorite items)

### Features

-   Grid layout
-   Subtle left spine strip
-   🏆 icon for favorites
-   Format icon pill
-   Mobile responsive

### Format Mapping

| Format    | Icon | Spine Color  |
|-----------|------|--------------|
| Hardcover | 📕   | bg-slate-900 |
| Paperback | 📗   | bg-slate-600 |
| eBook     | 📘   | bg-slate-400 |
| Audiobook | 🎧   | bg-slate-300 |
| Other     | 📖   | bg-slate-200 |

------------------------------------------------------------------------

## 8️⃣ Docker Setup

### Services

-   dog-eared-api
-   dog-eared-web

### Commands

    docker compose up --build
    docker compose down
    docker compose ps
    docker compose logs --tail 50 web

Rebuild required after backend changes.

------------------------------------------------------------------------

## 9️⃣ Folder Structure (Simplified)

    dog-eared/
      backend/
        app/
          core/
          models/
          routers/
          main.py
        pyproject.toml
        .env
      frontend/
        src/
          app/
          pages/
          components/
        package.json
      docker-compose.yml

------------------------------------------------------------------------

## 🔟 Known Issues (Resolved)

-   bcrypt backend error
-   bcrypt 72-byte limit
-   Missing POST /owned route
-   Router registration mistakes
-   Duplicate SQLModel table definition
-   Wrong port being called from frontend
-   Double Bearer prefix in Swagger
-   UUID `.hex` issue

All resolved.

------------------------------------------------------------------------

## 1️⃣1️⃣ Current Capability

Dog-Eared V1 is:

-   Authenticated
-   User scoped
-   Multi-device compatible
-   Dockerized
-   API documented
-   Visually structured
-   Expandable

Ready for Phase 2.
