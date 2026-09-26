# share-skill

A repository for sharing Codex skills. It currently contains
[blog-agent](.agents/skills/blog-agent/SKILL.md), for blog article research,
writing, revision, SEO diagnosis, and draft handoff.

## Install

Clone the repository, then link the skill into your user skill directory:

```sh
git clone https://github.com/junichy/share-skill.git
ln -s "$PWD/share-skill/.agents/skills/blog-agent" ~/.agents/skills/blog-agent
```

Run these commands from the directory where you want to keep the clone. If
`~/.agents/skills/blog-agent` already exists, choose another installation path
or remove the old installation deliberately before linking. Invoke the skill
with `$blog-agent` in Codex.

The skill has no required companion skills, MCP servers, paid keyword tools, or
writing-model API. GSC and project publishing connections are used only when
the requested work needs them and the project already provides access. The
optional check scripts use Python's standard library.

## Scope

Project editorial rules and the user's authorization govern saving, external
ledger updates, scheduling, and publication. A skill installation does not
grant those actions. Research snapshots, GSC metrics, live SERP observations,
saved drafts, and published pages remain separate evidence states.
