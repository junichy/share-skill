# blog-agent

A standalone Codex skill for blog article research, writing, revision, SEO
diagnosis, and draft handoff. The skill instructions are in [SKILL.md](SKILL.md).

## Install

Clone this repository as a skill folder:

```sh
git clone https://github.com/junichy/blog-agent-standalone.git ~/.agents/skills/blog-agent
```

If `~/.agents/skills/blog-agent` already exists, choose a different local folder
or move that installation first. Invoke the skill with `$blog-agent` in Codex.

The skill has no required companion skills, MCP servers, paid keyword tools, or
writing-model API. GSC and project publishing connections are used only when
the requested work needs them and the project already provides access. The
optional check scripts use Python's standard library.

## Scope

Project editorial rules and the user's authorization govern saving, external
ledger updates, scheduling, and publication. A skill installation does not
grant those actions. Research snapshots, GSC metrics, live SERP observations,
saved drafts, and published pages remain separate evidence states.
