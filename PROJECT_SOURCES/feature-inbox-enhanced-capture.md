📌 Dog-Eared — Feature Session
feature/inbox-enhanced-capture
🎯 Goal

Improve the Inbox intake layer to make capturing books from TikTok fast, structured, and low-friction — without breaking the existing Owned flow.

Primary Objective:

Paste a TikTok URL and save it quickly

Store structured source metadata

Keep manual entry lightweight

Avoid premature scraping/automation unless clearly justified

🏗 Scope
✅ In Scope (V1 Finalized)

Add a Quick Capture UI directly on the Inbox page

Use existing source_post_url field to store TikTok URLs

Use existing raw_text field for optional notes/title hints

Keep status = "new" default behavior

No database migrations

No schema changes

No new API routes

❌ Out of Scope (V1)

Automated TikTok scraping or caption extraction

Schema expansion (no new columns)

Auto-creation of Source records

Tagging system

Analytics

Refactors to Owned flow

📌 Current System State (Confirmed from Code)
Backend Models
Source

id (UUID)

user_id

type (tiktok/family/friend/etc.)

name

url (optional)

notes (optional)

created_at

IntakeItem

id (UUID)

user_id

raw_text (string)

source_id (optional UUID)

source_post_url (optional string)

captured_at (datetime)

status (default "new")

matched_book_id (optional)

match_confidence (optional)

parse_json (JSON)

created_at

API
POST /intake

Accepts:

raw_text (required)

source_id (optional)

source_post_url (optional)

Creates:

status = "new"

captured_at = now

GET /intake?status=new

Returns:

id

raw_text

status

captured_at

source_id

source_post_url

🧠 Step 4 — Final Design Decision

After reviewing actual backend and frontend code:

✅ We will implement Option A (Minimal Change)

We will:

Reuse source_post_url for TikTok links

Reuse raw_text for optional notes/title hints

Leave source_id null in V1

Avoid schema renaming or refactoring

This delivers the feature with zero backend modifications.

🎨 Frontend Implementation Plan

Add a Quick Capture card at the top of Inbox with:

TikTok URL input

Optional notes textarea

Save button

Calls existing POST /intake

Behavior Rules
User Input	Stored raw_text	Stored source_post_url
URL only	"TikTok capture"	URL
Notes only	Notes	null
URL + Notes	Notes	URL

After successful save:

Clear form

Reload inbox list

🔒 Constraints Honored

No unnecessary backend complexity

No premature automation

No breaking changes

Self-contained feature branch

Docker + Vite workflow unchanged

Owned conversion untouched

🧪 Testing Plan

Paste TikTok URL → Save

Confirm item appears in Inbox

Confirm Open link works

Confirm status remains "new"

Confirm converting to Owned still works

Confirm no API errors

🔮 Future Enhancements (V2+)

Not part of this branch:

Accept source_type and auto-create Source

Add source_notes column

Add tagging (JSON or relational)

Add metadata enrichment

Add analytics hooks

🔄 Commands Used
git checkout main
git pull
git checkout -b feature/inbox-enhanced-capture
# (implementation commits)
git add .
git commit -m "..."
git push -u origin feature/inbox-enhanced-capture

📈 Impact on PROJECT_STATE.md

None for V1 (no schema changes).

🏁 Feature Progress

 Branch created

 Backend reviewed

 Frontend reviewed

 Design finalized (Step 4)

 Frontend implemented

 Tested locally

 PR opened

 Merged