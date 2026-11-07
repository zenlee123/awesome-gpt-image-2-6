# Contributing / 如何投稿

Help build a source-backed collection of GPT Image 2.6 workflows.
欢迎提交有来源、可复用的 GPT Image 2.6 提示词玩法。

1. Open a prompt submission issue or edit `data/prompts.json` in a pull request.
2. Include the original post URL, creator, model attribution, full prompt or
   a clearly labeled adaptation, required inputs and result link.
3. Distinguish an official example, a creator claim, an independently reproduced
   result and an original untested template. Do not relabel 2.5 examples as 2.6.
4. Never invent popularity numbers. Supply metric, count, permalink and observation
   date for popularity claims. Without evidence, leave `popularity` as `null`.
5. Do not upload private references, API keys, paid prompt packs or media without
   permission. Linking a source is sufficient; a public post is not a media license.
6. Run `python3 scripts/build.py`, then `python3 scripts/build.py --check`.
   Commit the regenerated Markdown with the JSON changes.

## Editorial rules / 编辑约定

- `data/prompts.json` is the single source of truth; `README*` and `cases/*.md`
  are generated. Edit the generator for layout changes.
- Stable `id`: lowercase ASCII words separated by hyphens. Never recycle an ID.
- Every prompt needs `title`, `category`, `model`, `creator`, `requirements`,
  bilingual `prompt`, `origin`, `source_status`, `observed_on`, `reproduced` and
  `media_urls`. See existing entries for the exact schema.
- `source_status`: `official-page-checked`, `creator-post-checked`,
  `secondary-only`, or `original-unverified`.
- `reproduced` means independently regenerated and reviewed, not merely reposted.
  When setting it to true, also provide `reproduction` with model, settings,
  test date, attempts, input provenance and output evidence.
- For a popularity object, provide `metric`, `count`, `url`, `observed_on`.
  A count records a dated snapshot, not a universal ranking.
- `prompt_kind`: `editorial-adaptation` or `original-template`.
- Preserve source-language short prompts in `original_prompt` only when permitted;
  otherwise link to the source. Translations and rewrites must be labeled.
- Keep JSON schema changes compatible or describe the migration in the PR.

## Corrections and removal / 更正与移除

Open a correction issue with the affected ID, correct attribution and supporting
link. Rights holders may request media removal or source corrections there.
Do not post personal identity documents publicly; a link to the original work
and the requested change is enough to start a review.
