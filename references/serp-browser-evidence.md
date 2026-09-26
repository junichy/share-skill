# Google SERP browser evidence

Use this reference when article or query-ownership decisions need the actual
Google results shown in the user's browser.

Start normal research with [keyword-source-research.md](keyword-source-research.md). This browser
procedure is conditional, not a prerequisite for accepting a dated keyword-source snapshot.
Use it for actual-screen claims, SERP-feature layout or material discrepancies.

## Surface

Use the user's requested browser and the available runtime's documented browser
tools. Prefer an existing tab for the exact query when available; otherwise
open a new tab. Read the tool's returned state before further actions. If the
user requests native Computer Use, use that surface under its own instructions.

Refresh the target state before a UI action when another agent may have changed
it. Keep evidence page-backed: visible results, their links, screenshots, and
supported DOM readout. Do not read cookies, browser storage, or profile files.

## What to retain

Record the capture time, exact query and URL, visible language/location or
personalization context, and observed organic results. Use explicit query,
language, region, and personalization URL parameters when supported, but do not
claim they remove all ranking variation.

Keep ads, AI Overview, PAA, image/video packs, and sitelinks separate from organic
rank. Explain missing ranks and duplicate URL fragments. Extract only evidence
needed for the selected editorial workflow, and distinguish ranking observation
from an inference about why a page ranks.

## When observation fails

Retry once on the selected surface after refreshing state. Classify the actual
failure: connector/tab binding, native control, denied permission, CAPTCHA, or
network access. Do not bypass a permission denial or CAPTCHA.

An alternative control surface may be used only within the user's browser and
permission rules and only if it preserves the required evidence. Web search,
curl, or a search API cannot silently replace the observed Google result order.
If that observation remains unavailable, report the missing evidence and
continue only work that does not depend on it.
