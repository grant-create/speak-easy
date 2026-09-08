# Speak Easy

A small Django app for learning a language through short, focused lessons —
phrases, pronunciation, word breakdowns, conjugation tables, and review
quizzes — instead of a big vocabulary list up front.

## Stack

Django 5.2, sqlite, no JS framework — server-rendered templates. Apps are
split by domain: `accounts`, `languages`, `lessons`, `progress`,
`pageview_analytics`.

## Working with AI tools

I build this with Claude Code day to day. The repo carries a
[`CLAUDE.md`](./CLAUDE.md) at the root — the conventions file Claude Code
reads automatically at the start of a session, covering this project's app
structure, model conventions (e.g. `JSONField` for small display-only
structured data like word breakdowns and conjugation tables), comment
style, and how migrations/fixtures ship together. I keep one of these per
personal repo, each scoped to that project's actual risk level — this one
lets Claude commit and push on request since there's no real user data or
money involved, while a trading repo I maintain requires me to review
every change before anything gets staged.

In practice: I drive lesson content, curriculum structure, and UX
decisions myself, and lean on Claude Code for the repetitive implementation
work — new CRUD apps, migrations + matching fixtures, template
boilerplate — reviewing diffs the same way I would a teammate's PR before
anything ships.

## Content planning notes

Early brainstorming on lesson ordering/curriculum structure — kept as-is
since it's still shaping how lessons get built out.

> I wonder what the quickest way to learn a language is. I've been
> thinking it's something like this: learn the useful parts and use them,
> then slowly add new words. Maybe this can be used as an AI prompt —
> fill this guide in with the language `<language>`.
>
> **Learn sentence phrasing** — noun, verb, adverb.
>
> **Learn useful phrases** (how English speakers actually say these, not
> a direct translation): hello, goodbye, please, thank you; I would
> like/can I have/where is…; what's up, bathroom, hotel; I'm doing well
> and you?; how do you say?
>
> **Learn:** this, that, there / this one, that one, here, there.
>
> **Useful verbs:** I like, I want, I know.
>
> After that, move on to conversation — more nouns and verbs, then past
> and future tense: how to talk about before, now, later.
