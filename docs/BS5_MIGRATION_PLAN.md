# Plan: Migrate ckanext-dia_theme from Bootstrap 3 to Bootstrap 5 (CKAN 2.11 Compatibility)

## Context

CKAN 2.10.x includes a Bootstrap 3 backwards-compatibility layer (`templates-bs3/`), but **CKAN 2.11 removes it entirely** and only ships Bootstrap 5 templates. The `ckanext-dia_theme` extension currently overrides CKAN's BS3 templates and bundles a custom "RUA" design system CSS (`rua-pattern-library` v1.3.1 from `data-govt-nz/rua`) that is built on top of Bootstrap 3.3.7.

**Good news:** CKAN core BS5 templates preserve all the same Jinja2 block names as BS3, so the template override structure remains compatible. The main work is CSS/Bootstrap conflict resolution, template class updates, and upgrading the RUA dependency.

---

## Scope Summary

| Area | Count | Risk |
|------|-------|------|
| Template files in dia_theme | 33 | Medium |
| LESS source files | 5 | Medium |
| RUA design system (external repo) | Separate project | **High** |
| Other extensions with BS3 deps | 6 of 12 | Medium |
| Legacy color theme CSS (public/) | 5 files | Low (superseded, can remove) |

---

## Phase 1: Upgrade RUA Pattern Library (Separate Project — Prerequisite)

**This is the critical-path item.** The RUA design system (`data-govt-nz/rua`, currently v1.3.1) bundles the full Bootstrap 3.3.7 CSS. When CKAN 2.11 loads its own Bootstrap 5, both will be active, causing conflicts.

### Approach: Rebuild RUA on Bootstrap 5

Since the RUA source repo is available at `data-govt-nz/rua`, the cleanest path is:

1. **Clone `data-govt-nz/rua`** and create a BS5 migration branch
2. **Replace the Bootstrap 3.3.7 base** with Bootstrap 5.x
3. **Update RUA component styles** to use BS5 conventions:
   - Grid: `col-xs-*` → `col-*`
   - Utilities: `pull-left/right` → `float-start/end`, `sr-only` → `visually-hidden`
   - Components: `panel` → `card`, `label` → `badge`, `well` → removed
   - Data attributes: `data-toggle` → `data-bs-toggle`, `data-target` → `data-bs-target`
4. **Update RUA JavaScript** (`rua.js`) — check for BS3 jQuery plugin dependencies (`$.fn.collapse`, `$.fn.tooltip`, etc.) and migrate to BS5's vanilla JS API
5. **Publish a new RUA version** (e.g., v2.0.0) and update `package.json` dependency

### Alternative: Strip Bootstrap from RUA

If rebuilding RUA is too large a scope, we can:
- Extract only the RUA-specific styles (custom components, fonts, banners) from the compiled `rua.css`
- Remove the BS3 base layer (normalize, grid, components)
- Let CKAN's BS5 handle the framework layer
- This is more fragile but faster

### Update in dia_theme after RUA upgrade:
- `package.json` line 10: Update `rua-pattern-library` version
- Run `npm run rua` to pull new RUA dist files
- Verify all RUA classes still work with BS5 base

---

## Phase 2: Template Updates (33 files)

### 2a: Core Layout Templates (Highest Priority)

**`templates/base.html`** — `{% ckan_extends %}`
- Remove IE conditional comments (lines 5-8), replace with simple `<html lang="en">`
- Asset loading blocks (`styles`, `scripts`) — no changes needed

**`templates/page.html`** — extends `base.html`
- Line 27: Flash alerts — `alert fade in {{ category }}` → `alert alert-dismissible fade show {{ category }}`
- Lines 58, 99: `col-md-9`, `col-md-3` — **no change** (same in BS5)
- Skip link (line 6) uses custom classes — **no change needed**

**`templates/header_base.html`** — fully custom (not ckan_extends)
- Uses all RUA classes (`site-header`, `button-icon`, `navicon`, `data-rua-*`). **No BS3 classes.**
- Line 123: Verify `{% url_for controller='dataset', action='search' %}` works in 2.11 (may need `'dataset.search'` named route)

**`templates/header.html`** — extends `header_base.html`
- **No changes needed**

**`templates/footer.html`** — fully custom
- Lines 127, 130: `col-md-3`, `col-md-9` — **no change** (same in BS5)

### 2b: Group/Organization Templates

**`templates/group/index.html`** and **`templates/organization/index.html`**
- `col-xs-12` → `col-12` (BS5 dropped the `-xs-` infix)
- Verify parent template compatibility (check `request.params` → `request.args`)

### 2c: Templates Using `{% ckan_extends %}` (Audit Each)

These inherit from CKAN core BS5 templates. Main concern is whether blocks they override reference classes that changed:

| Template | Override Blocks | Likely Changes |
|----------|----------------|----------------|
| `package/search.html` | links, pre_primary, secondary_content, form | Audit for BS3 classes |
| `package/read_base.html` | links | Minimal — likely none |
| `package/snippets/info.html` | nums, follow_button | Audit for class changes |
| `package/snippets/resource_item.html` | resource_item_title, description | Check badge/label classes |
| `package/snippets/resource_edit_form.html` | basic_fields | Check form classes |
| `package/snippets/resource_view.html` | resource_view | Audit |
| `scheming/package/read.html` | package_notes, package_additional_info | Audit |
| `scheming/package/resource_read.html` | multiple blocks | Audit |
| `scheming/package/snippets/additional_info.html` | package_additional_info | Audit |
| `group/snippets/info.html` | nums, follow | Audit |
| `admin/index.html` | primary_content_inner, secondary_content | Audit |
| `user/dashboard_organizations.html` | page_primary_action, primary_content_inner | Audit |
| `user/snippets/api_token_list.html` | token_cell_actions | Audit |
| `error_document_template.html` | primary | Audit |

### 2d: Custom Snippets (Not ckan_extends)

These are fully custom HTML — mainly need to check for BS3 utility classes:
- `snippets/search_form.html` — Check for `input-group-btn`, `btn-default`
- `snippets/package_item.html` — Check for `label label-*` → `badge bg-*`
- `snippets/header_navigation_items.html` — Custom RUA classes, likely no changes
- Other snippets (`organization.html`, `rights.html`, `metadata_created.html`, `home_breadcrumb_item.html`, `language_selector.html`, `user_reg_disabled.html`) — audit each
- `home/layout1.html`, `home/snippets/search.html`, `home/snippets/stats.html` — audit

---

## Phase 3: CSS/LESS Updates

### Files to modify:
- `less/dia_custom.less` — Main custom styles (~1367 lines)
- `less/dia_new.less` — CKAN 2.7 era modifications
- `less/diamixins.less` — LESS mixins
- `less/focus.less` — Accessibility focus styles
- `fanstatic/dia_custom.css` — Compiled output (regenerate from LESS)

### Key CSS changes:

| Pattern | BS3 | BS5 | Files |
|---------|-----|-----|-------|
| Grid | `col-xs-*` | `col-*` | templates, CSS |
| Labels/Badges | `.label`, `.label-default` | `.badge`, `.bg-secondary` | `dia_custom.css` (lines 29-53, 695-704) |
| Wells | `.well` | removed (use custom) | `dia_custom.less` line 871 |
| Buttons | `btn-default` | `btn-secondary` | audit all |
| Accessibility | `sr-only` | `visually-hidden` | audit |
| Old grid refs | `.span4`, `.span8`, `.span3`, `.span6` | remove or replace | `dia_custom.less`, `dia_custom.css` |

### CSS cleanup:
- Remove vendor-prefixed `-webkit-border-radius`, `-moz-border-radius`, etc. (unnecessary for BS5 browser targets)
- Remove `-webkit-box-shadow`, `-moz-box-shadow` prefixes
- Clean up old `.masthead`, `.account-masthead` selectors that reference the old CKAN header (now using RUA `site-header`)

### Recompile:
```bash
npm run css  # lessc main.less → dia_custom.css
```

---

## Phase 4: JavaScript Audit

### Files:
- `fanstatic/dia_custom.js` — Uses `data-rua-*` attributes (RUA's own system), **not BS3**. Likely no changes.
- `fanstatic/banner.js` — AJAX banner loading. No BS3 deps.
- `fanstatic/rua/js/rua.js` — Handled by RUA upgrade (Phase 1)

### Check for:
- Any `data-toggle` / `data-target` references → update to `data-bs-toggle` / `data-bs-target`
- Any jQuery BS3 plugin calls (`.collapse()`, `.tooltip()`, `.modal()`)

---

## Phase 5: Clean Up Legacy Files

- **Remove** the 5 superseded color theme CSS files in `public/`:
  - `main.css`, `fuchsia.css`, `red.css`, `green.css`, `maroon.css` (~10,600 lines each)
- **Remove** any template references to these files
- Confirm CKAN config doesn't reference them via `ckan.base_public_folder` or similar

---

## Phase 6: Other Extension Patches

6 other extensions have BS3 dependencies. These may need patches (applied via `patches/` directory):

| Extension | BS3 Usage | Severity |
|-----------|-----------|----------|
| **ckanext-harvest** | `btn-default`, `data-toggle` in 4 templates | Medium |
| **ckanext-scheming** | `panel panel-default`, `panel-heading`, `panel-body`, `btn-default` | **High** |
| **ckanext-protected_resources** | `btn btn-default` in 1 template | Low |
| **ckanext-security** | `btn btn-default pull-left` in 1 template | Low |
| **ckanext-geoview** | `panel` in vendor CSS, bundled BS2 CSS | Low (vendor code) |
| **ckanext-spatial** | `sr-only` in vendor Leaflet CSS | Low (vendor code) |

**Approach:** Create patches in `patches/<extension>/` for each, following the existing patching pattern (`scripts/apply_patches.sh`). The scheming and harvest extensions are the highest priority since they affect core dataset creation/editing workflows.

---

## Phase 7: Testing & Verification

**Approach:** Test against the current CKAN 2.10.9 with the BS3 compatibility flag disabled. This validates BS5 template compatibility without requiring a full CKAN version upgrade.

### Config change for testing:
In `containers/ckan/ckan.ini.mako-template` (lines 146-148), change:
```ini
# Before (current):
ckan.base_public_folder=public-bs3
ckan.base_templates_folder=templates-bs3

# After (for BS5 testing):
ckan.base_public_folder=public
ckan.base_templates_folder=templates
```

### Test steps:
1. **Rebuild containers** after config change: `docker compose build ckan && docker compose up -d`
2. **Visual regression** — check key pages:
   - Home page, Dataset search, Dataset detail, Resource view
   - Organization list, Group list
   - Dataset create/edit forms
   - Admin panel, Login page
3. **Functional tests**: `docker compose -f docker-compose-circle.yml up ckan-functional-tests`
4. **Browser console** — check for JS errors (missing BS3 plugins, etc.)
5. **Responsive testing** — mobile/tablet layouts
6. **Accessibility** — skip links, focus states, ARIA attributes

### Iterative testing:
The config change can be made early (even before starting migration work) to see the current state of breakage with BS5 templates. This gives a clear picture of what needs fixing and allows incremental validation as each phase is completed.

---

## Execution Order

```
Phase 7 (baseline): Disable BS3 flag on 2.10.9, see current breakage
    ↓
Phase 1: RUA upgrade (separate repo, prerequisite)
    ↓
Phase 2 + 3 + 4: Templates + CSS + JS (parallel, in this repo)
    ↓
Phase 5: Legacy cleanup
    ↓
Phase 6: Other extension patches
    ↓
Phase 7 (final): Full regression testing
```

**Start with Phase 7 as a baseline** — disable the BS3 flag on CKAN 2.10.9 to see the current state of breakage. This gives a clear picture of what needs fixing and provides a before/after comparison as each phase is completed.

Phase 1 (RUA) is the critical path for actual fixes and should start first. Phases 2-4 can begin in parallel once the RUA upgrade approach is decided, since most template changes are independent of RUA.

---

## Open Question

- **RUA rebuild scope:** Should we handle the RUA repo upgrade as part of this effort, or treat it as a separate workstream? The RUA rebuild is potentially the largest piece of work depending on how tightly coupled its component styles are to BS3.
