# 📌 Dog-Eared — Feature Session
## feature/inbox-auto-tiktok-source

### 🎯 Goal
When an intake item is created with a TikTok URL and no source_id, automatically find-or-create a canonical TikTok Source and attach it to the intake item.

### ✅ Scope (V1)
- Backend-only change
- No schema changes
- No scraping/enrichment
- No changes to Owned flow

### 🔧 Implementation
- Updated `POST /intake`:
  - If `payload.source_id` is null AND `source_post_url` contains `tiktok.com`:
    - Query `Source` for `(user_id, type="tiktok")`
    - Create `Source(type="tiktok", name="TikTok")` if missing
    - Set `IntakeItem.source_id` to that Source

### 🧪 Tests
- TikTok URL intake returns non-null `source_id`
- Second TikTok URL intake returns the same `source_id` (no duplicates)
- Non-TikTok URL does not auto-attach a source

### 📈 Notes
- UI still infers “TikTok” badge from URL. Future polish could join Source to return `source_name` in intake responses.