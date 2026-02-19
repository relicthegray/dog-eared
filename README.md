# Dog-Eared 🐾📚

A cozy home for your TBR.

Dog-Eared is a mobile-first, multi-user (invite-only) reading tracker built with FastAPI + React.  
V1 focuses on: **Capture → Inbox**, metadata enrichment (Open Library + Google Books), shelves, and an **Owned** “trophy case”.

## Quickstart (Docker)

1. Install Docker Desktop (Windows/macOS) and Git.
2. Copy env file and edit as needed:

   ```bash
   cp .env.example .env
   ```

3. Run the stack:

   ```bash
   docker compose up --build
   ```

- API: http://localhost:8000/docs
- Web: http://localhost:5173

## Dev (without Docker)

### Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -U pip
pip install -e .
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Repo layout

- `backend/` FastAPI + SQLModel structure
- `frontend/` React + Vite + Tailwind mobile-first shell
- `docker-compose.yml` dev stack

## Roadmap (V1)
- [ ] Invite-only auth (admin creates invites)
- [ ] Capture screen (paste TikTok/notes + source)
- [ ] Inbox list (new / needs review / matched)
- [ ] Enrichment (Open Library + Google Books)
- [ ] Resolve screen (choose correct match)
- [ ] Shelves + reading state
- [ ] Owned copies (“trophy case”)

## License
Choose a license when you decide whether the repo will be public.
