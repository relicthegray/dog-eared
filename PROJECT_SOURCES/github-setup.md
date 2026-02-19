📦 Dog-Eared — GitHub Setup & Workflow Standard
Purpose

This document captures the initial GitHub integration process for the Dog-Eared project and establishes the long-term development workflow standard.

This workflow ensures:

Safe experimentation

Clean commit history

Feature isolation

Cloud backup

CI compatibility

Local-first fast development

🧰 Initial Git Setup (Windows)
1. Install Git

Download from:

https://git-scm.com/download/win

During installation:

Select:

Git from the command line and also from 3rd-party software

2. Verify Installation
git --version

3. Configure Git Identity
git config --global user.name "Chris Youngblood"
git config --global user.email "relicthegray@gmail.com"


Verify:

git config --global --list

📁 Initialize Local Repo

Inside project folder:

cd C:\Users\young\Projects\dog-eared
git init
git branch -M main

🚫 .gitignore (Critical)

Create .gitignore at repo root:

# --- OS / Editor ---
.DS_Store
Thumbs.db
.idea/
.vscode/

# --- Python ---
__pycache__/
*.py[cod]
*.pyo
.Python
*.egg-info/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.venv/
venv/

# --- Node / Vite ---
node_modules/
dist/
.vite/
frontend/node_modules/
frontend/dist/

# --- Env / secrets ---
.env
*.env.local
backend/.env
backend/.env.*

# --- DB / runtime data ---
*.db
*.sqlite
*.sqlite3
backend/app/static/
backend/app/uploads/
backend/app/.local/
docker-data/

# --- Docker ---
**/.docker/

🧱 First Commit
git add .
git status
git commit -m "Initial commit: Dog-Eared baseline"

🔗 Connect to GitHub
git remote add origin https://github.com/relicthegray/dog-eared.git
git remote -v

⬆️ Push to GitHub

If remote contains starter README:

git pull origin main --allow-unrelated-histories


Resolve conflict (if README):

git checkout --ours README.md
git add README.md
git commit -m "Resolve README merge conflict"


Then:

git push -u origin main

🧼 Line Ending Standardization

Set Windows behavior:

git config --global core.autocrlf true


Create .gitattributes at repo root:

* text=auto eol=lf


Commit:

git add .gitattributes
git commit -m "Add .gitattributes to enforce LF line endings"
git push


Optional normalization:

git add --renormalize .
git commit -m "Normalize line endings"
git push

🚀 Official Development Workflow (Required Going Forward)
❌ Never develop directly on main

Always create a feature branch.

🧪 Starting a Feature
git checkout -b feature/<feature-name>


Examples:

feature/owned-shelf-polish

feature/alembic-migrations

feature/search-filter

feature/queue-refactor

💻 Develop Locally

Edit files

Run Docker / Vite

Test fast

Iterate freely

💾 Commit Work
git add .
git commit -m "Clear, descriptive commit message"

☁️ Push Feature Branch
git push -u origin feature/<feature-name>

🔀 Merge Strategy

Preferred:

Open Pull Request on GitHub

Merge via GitHub UI

Alternative (local merge):

git checkout main
git pull
git merge feature/<feature-name>
git push

🔒 Protect main Branch (Recommended)

On GitHub:

Settings → Branches → Add rule for main

Enable:

Require pull request before merging

Require status checks to pass

Require branches to be up to date

🧠 Why This Is Now Standard

This workflow provides:

Safe experimentation

Easy rollback

Clean history

CI compatibility

Scalable team readiness

Deployment readiness

Long-term maintainability

Dog-Eared is no longer “a folder of files.”

It is a versioned, structured software project.

📚 Recommended Structure for Future Chat Sessions

Yes — saving major ChatGPT sessions is absolutely the right move.

I recommend:

docs/
    github-setup.md
    feature-owned-shelf-polish.md
    feature-migrations.md
    ui-refactor-session.md


Each file should contain:

Goal

Files changed

Commands used

Architectural decisions

Lessons learned

This builds a living engineering journal.

🏁 Status

GitHub workflow successfully integrated.

Dog-Eared development standard established.

If you’d like, I can also generate:

A reusable Feature Session Template.md

Or a structured Engineering Journal Template

Or a clean /docs folder structure plan

Your project just leveled up.