# Working in this repo

Speak Easy is a Django language-learning app (lessons, phrases, quizzes,
per-user favorites/progress). This file is what I hand Claude Code so it
picks up this project's conventions instead of guessing at them from
scratch every session — the same file lives at the root of my other
personal projects, each tuned to that repo's own risk level.

## Stack

- Django 5.2, `python-dotenv` for config, sqlite locally.
- Run everything through the venv: `.venv/bin/python manage.py <command>`.
- Apps are split by domain, not by layer: `accounts`, `languages`,
  `lessons`, `progress`, `pageview_analytics`. A new feature usually means
  a new app, not a new folder inside an existing one.

## Conventions Claude should follow here

- **Comments: one line max, only when the *why* isn't obvious from the
  code.** No docstring blocks, no restating what a function does. See
  `lessons/models.py` for the pattern already in use (`# in target
  language`, not a paragraph explaining the field).
- Structured per-row data (`word_breakdown`, `conjugations` on `Phrase`)
  is stored as `JSONField`, not a separate related table — these are
  small, display-only, never queried into individually. Keep new
  structured fields consistent with that unless something needs to be
  filtered/joined on.
- Every model gets an explicit `Meta.ordering`; don't rely on insertion
  order.
- New migrations that also need seed content ship with a matching fixture
  in the same commit (see the `languages`/`lessons` fixture history) —
  not a separate follow-up commit.
- `pageview_analytics` here is a vendored copy, not a shared package —
  it's fine to modify freely for this project without worrying about
  other repos that also carry a copy of it.

## Workflow

- Low-stakes repo (no real user data, no money moving) — Claude commits
  and pushes on request without a review-first gate, unlike my
  trading-related repos where nothing gets staged without me looking at
  it first.
- Before a model/behavior change ships, run the app's `tests.py`, not
  just a manual click-through.
- I use Claude Code for the actual implementation work (models, views,
  templates, migrations) and lean on it most for the repetitive parts —
  new CRUD app scaffolding, fixture data, template boilerplate — while I
  drive the actual lesson content and UX decisions.
