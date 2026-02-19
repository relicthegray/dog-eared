📦 Dog-Eared — GitHub Setup & Workflow Standard
Purpose

This document captures the full GitHub integration process for the Dog-Eared project and establishes the permanent development workflow standard.

This workflow ensures:

Safe experimentation

Clean commit history

Feature isolation

Cloud backup

CI compatibility

Local-first fast development

Structured engineering documentation

Dog-Eared is now a disciplined, version-controlled software project.

🧰 Initial Git Setup (Windows)
1. Install Git

Download from:

https://git-scm.com/download/win

During installation select:

Git from the command line and also from 3rd-party software

2. Verify Installation
git --version

3. Configure Git Identity
git config --global user.name "Chris Youngblood"
git config --global user.email "relicthegray@gmail.com"


Verify:

git config --global --list

📁 Initialize Local Repository

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

⬆️ First Push (When Remote Already Has Commits)

If GitHub repo contains a starter README or initial commit, pushing may fail with:

non-fast-forward error

In that case:

git pull origin main --allow-unrelated-histories


If merge conflict occurs (e.g., README):

git checkout --ours README.md
git add README.md
git commit -m "Resolve README merge conflict"


Then push:

git push -u origin main

🧼 Line Ending Standardization (Windows Best Practice)

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

📚 Documentation Structure Standard

All engineering documentation lives in:

PROJECT_SOURCES/


Example structure:

PROJECT_SOURCES/
    PROJECT_STATE.md
    github-setup.md
    feature-<feature-name>.md


Major decisions, feature sessions, and architectural changes must be documented here.

Documentation is version-controlled like code.

🚀 Official Development Workflow
❌ Never Develop Directly on main

Always use a branch.

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

Test immediately

Iterate freely

Local development speed is unchanged by Git.

💾 Commit Work
git add .
git commit -m "Clear, descriptive commit message"

☁️ Push Feature Branch
git push -u origin feature/<feature-name>

🔀 Merge Strategy
Preferred (Recommended Habit)

Open Pull Request on GitHub

Merge via GitHub UI

Alternative (Local Merge)
git checkout main
git pull
git merge feature/<feature-name>
git push

🧹 Branch Cleanup After Merge

After merging a feature branch:

Delete local branch:

git branch -d feature/<feature-name>


Delete remote branch:

git push origin --delete feature/<feature-name>

🔍 Verifying Branch State

To visualize history:

git log --oneline --decorate --graph --all


To verify files exist in main:

git ls-tree -r --name-only main


To check current status:

git status

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

Structured documentation memory

Dog-Eared is no longer “a folder of files.”

It is a versioned, structured software project.

🏁 Status

Git installed and configured

Repository initialized

Remote connected

Non-fast-forward handled correctly

Merge conflict resolved properly

Line endings standardized

Documentation centralized

Branch workflow established

Cleanup discipline established

GitHub workflow successfully integrated.

Dog-Eared development standard permanently established.

If you’d like next, I can generate a reusable:

feature-session-template.md

or engineering-journal-template.md

so every new feature session follows the same disciplined pattern.
