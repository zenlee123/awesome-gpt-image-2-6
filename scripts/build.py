#!/usr/bin/env python3
"""Validate the catalogue and render Markdown. Python standard library only."""
import argparse
from collections import Counter
from datetime import date
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parents[1]
REPO = 'https://github.com/zenlee123/awesome-gpt-image-2-6'
CATEGORIES = {
    'animation': ('GIF & animation', 'GIF 与角色动画'),
    'editing': ('Precise editing', '精确编辑'),
    'photography': ('Portraits & photography', '人像与摄影'),
    'posters': ('Posters & typography', '海报与文字排版'),
    'commerce': ('Product & commerce', '商品与电商'),
    'characters': ('Character consistency', '角色一致性'),
    'illustration': ('Illustration & dioramas', '插画与微缩场景'),
    'branding': ('Logos & SVG', 'Logo 与 SVG'),
    'infographics': ('Infographics', '信息图'),
}
STATUSES = {
    'official-page-checked': ('Official page checked', '官方页面已核对'),
    'creator-post-checked': ('Creator post checked', '原作者帖子已核对'),
    'secondary-only': ('Secondary collection only', '仅核对二手收录'),
    'original-unverified': ('Original, untested template', '原创未实测模板'),
}


def validate(data):
    assert isinstance(data, list) and data, 'Empty catalogue'
    ids = set()
    for p in data:
        pid = p['id']
        assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', pid), pid
        assert pid not in ids, f'Duplicate: {pid}'
        ids.add(pid)
        assert p['category'] in CATEGORIES, pid
        assert p['model'] == 'gpt-image-2.6', pid
        assert p['source_status'] in STATUSES, pid
        assert isinstance(p['reproduced'], bool), pid
        assert isinstance(p['media_urls'], list), pid
        assert p['creator'].strip(), pid
        for field in ('title', 'prompt', 'requirements'):
            assert all(p[field][lang].strip() for lang in ('en', 'zh')), (pid, field)
        date.fromisoformat(p['observed_on'])
        if p['origin'] == 'curated':
            assert p['source_url'] and p['via_url'], pid
            assert p['prompt_kind'] == 'editorial-adaptation', pid
            assert p['source_status'] != 'original-unverified', pid
        else:
            assert p['origin'] == 'original-template', pid
            assert p['prompt_kind'] == 'original-template', pid
            assert p['source_status'] == 'original-unverified', pid
        for url in [p.get('source_url'), p.get('via_url'), *p['media_urls']]:
            if url:
                assert urlparse(url).scheme == 'https' and urlparse(url).netloc, (pid, url)
        if p['reproduced']:
            assert all(p['reproduction'].get(k) for k in
                       ('model', 'settings', 'date', 'attempts', 'inputs', 'output')), pid
        if p['popularity'] is not None:
            pop = p['popularity']
            assert all(k in pop for k in ('metric', 'count', 'url', 'observed_on')), pid
            assert isinstance(pop['count'], int) and pop['count'] >= 0, pid
            assert urlparse(pop['url']).scheme == 'https', pid
            date.fromisoformat(pop['observed_on'])


def case_page(p, lang):
    zh = lang == 'zh'
    home = '../README.zh-CN.md' if zh else '../README.md'
    page = f"# {p['title'][lang]}\n\n[{'返回目录' if zh else 'Back to collection'}]({home})\n\n"
    page += f"`{p['id']}` · {CATEGORIES[p['category']][int(zh)]}\n\n"
    page += f"- {'模型归属' if zh else 'Model attribution'}: GPT Image 2.6; {'具体变体未指定' if zh else 'variant unspecified'}\n"
    page += f"- {'核验状态' if zh else 'Evidence'}: {STATUSES[p['source_status']][int(zh)]}\n"
    page += f"- {'独立复现' if zh else 'Independently reproduced'}: {'Yes' if p['reproduced'] else 'No'}\n"
    page += f"- {'收录日期' if zh else 'Recorded'}: {p['observed_on']}\n"
    pop = p['popularity']
    page += f"- {'热度' if zh else 'Popularity'}: " + (f"{pop['metric']}: {pop['count']} ({pop['observed_on']})" if pop else ('未核验，不作热门排名' if zh else 'Unverified; no popularity ranking')) + '\n'
    if p.get('source_url'):
        page += f"- {'原作者/原始来源' if zh else 'Creator / primary source'}: [{p['creator']}]({p['source_url']})\n"
        page += f"- {'发现来源' if zh else 'Discovered via'}: [EvoLink]({p['via_url']})\n"
    page += f"\n## {'准备材料' if zh else 'Inputs'}\n\n{p['requirements'][lang]}\n"
    page += f"\n## {'可复制提示词' if zh else 'Copy-ready prompt'}\n\n"
    if p['origin'] == 'curated':
        page += ('以下为中英文整理版，包含翻译、改写或保留原句；来源原文（如收录）见下方。\n\n' if zh else 'Edited bilingual version: translated, adapted or retained from the source. The recorded original, where included, appears below.\n\n')
    else:
        page += ('本仓库原创模板，未实测。使用前替换所有 `{变量}`。\n\n' if zh else 'Original repository template, untested. Replace every `{placeholder}` before use.\n\n')
    page += f"```text\n{p['prompt'][lang]}\n```\n"
    page += f"\n<details>\n<summary>{'English version' if zh else '简体中文版本'}</summary>\n\n```text\n{p['prompt']['en' if zh else 'zh']}\n```\n\n</details>\n"
    if p.get('original_prompt'):
        page += f"\n## {'来源所载原文' if zh else 'Prompt as recorded by source'}\n\n```text\n{p['original_prompt']}\n```\n"
        if p['source_status'] == 'secondary-only':
            page += ('\n原文来自二手收录；本次未直接读取原帖。\n' if zh else '\nTranscribed from the secondary collection; the original post was not directly retrieved.\n')
    if p['media_urls']:
        page += f"\n## {'来源预览' if zh else 'Source preview'}\n\n"
        stills = [u for u in p['media_urls'] if not u.endswith('.mp4')]
        videos = [u for u in p['media_urls'] if u.endswith('.mp4')]
        # A list preserves input/output order without inventing media role labels.
        for i, u in enumerate(stills, 1):
            page += f'<img src="{u}" alt="{p["id"]} source image {i}" width="420">\n\n'
        for i, u in enumerate(videos, 1):
            page += f"[{'查看来源动画' if zh else 'View source animation'} {i}]({u})\n\n"
        page += ('预览顺序沿用来源；包括参考图、结果或对比图。输入/输出角色以原始来源说明为准。图片并非本仓库实测结果，版权归各权利人。\n' if zh else 'Images follow the source order and may include inputs, outputs or comparisons; consult the source for their roles. These are not repository-generated results. Rights remain with their owners.\n')
    return page


def home(data, lang):
    zh = lang == 'zh'
    curated = [p for p in data if p['origin'] == 'curated']
    templates = [p for p in data if p['origin'] == 'original-template']
    counts = Counter(p['category'] for p in data)
    s = '# Awesome GPT Image 2.6\n\n'
    s += '**' + ('面向全球创作者的 GPT Image 2.6 提示词玩法库。' if zh else 'A source-backed prompt collection for GPT Image 2.6 creators worldwide.') + '**\n\n'
    s += '[English](README.md) · [简体中文](README.zh-CN.md) · [JSON](data/prompts.json) · [Contribute](CONTRIBUTING.md)\n\n'
    s += f"![Curated cases](https://img.shields.io/badge/sourced_cases-{len(curated)}-2563eb) "
    s += f"![Original templates](https://img.shields.io/badge/original_templates-{len(templates)}-7c3aed) "
    s += '[![License](https://img.shields.io/badge/docs-CC_BY_4.0-16a34a)](LICENSE)\n\n'
    if zh:
        s += f'收录 **{len(curated)} 个有来源的案例 + {len(templates)} 个原创未实测模板**，覆盖局部编辑、角色 GIF、人像、海报、电商、SVG 与信息图。中英文提示词可直接复制。\n\n'
        s += '> 这是持续整理的公开玩法库，不是经验证的全球热门榜。7 个作者案例仅核对了二手收录，2 个官方案例已核对原文；全部尚未独立复现。2.5 案例不会混入 2.6 数量。详见 [来源与核验](docs/SOURCES.md)。\n\n'
        s += '## 快速开始\n\n1. 选择下方玩法，打开案例页。\n2. 按说明准备参考图，复制中文或英文提示词。\n3. 在支持 GPT Image 2.6 的工具中使用；模板需先替换 `{变量}`。\n4. 需要 GIF 或 SVG 时，同时选择工具支持的输出格式。\n\n'
    else:
        s += f'Explore **{len(curated)} sourced cases + {len(templates)} original untested templates** for editing, character GIFs, portraits, posters, products, SVG and infographics. Every entry includes English and Chinese prompts.\n\n'
        s += '> This is a growing collection, not a verified global viral ranking. Seven creator cases are secondary-source only; two official examples were checked against their source. None has been independently reproduced. GPT Image 2.5 cases are not counted as 2.6. Read the [source audit](docs/SOURCES.md).\n\n'
        s += '## Quick start\n\n1. Pick a workflow below and open its case page.\n2. Prepare the listed inputs and copy an English or Chinese prompt.\n3. Use a tool offering GPT Image 2.6; replace `{placeholders}` in templates.\n4. For GIF or SVG, also select the output format supported by your tool.\n\n'
    s += '## ' + ('玩法预览' if zh else 'Workflow previews') + '\n\n'
    s += '| ' + ('画框海报 | 吃饭表情包 | 眨眼角色' if zh else 'Gallery poster | Rice sticker | Blinking character') + ' |\n| --- | --- | --- |\n'
    preview_ids = ['baroque-gallery', 'rice-sticker', 'blink-sway']
    cells = []
    for pid in preview_ids:
        p = next(p for p in data if p['id'] == pid)
        stills = [u for u in p['media_urls'] if u.endswith('.jpg')]
        # Rice source starts with its reference; the last still is the output poster.
        img = stills[-1] if pid == 'rice-sticker' else stills[0]
        suffix = '.zh-CN' if zh else ''
        cells.append(f'[<img src="{img}" width="240" alt="{p["id"]}">](cases/{pid}{suffix}.md)')
    s += '| ' + ' | '.join(cells) + ' |\n\n'
    s += ('以上是来源预览，非本仓库实测。\n\n' if zh else 'Source previews, not results generated by this repository.\n\n')
    s += '## ' + ('分类导航' if zh else 'Categories') + '\n\n'
    s += '| ' + ('分类 | 条目数' if zh else 'Category | Entries') + ' |\n| --- | ---: |\n'
    for cat, names in CATEGORIES.items():
        entries = [p for p in data if p['category'] == cat]
        suffix = '.zh-CN' if zh else ''
        s += f'| [{names[int(zh)]}](cases/README{suffix}.md#{cat}) | {counts[cat]} |\n'
    for title, items in [(('有来源的 2.6 案例' if zh else 'Sourced 2.6 cases'), curated), (('原创模板 · 未实测' if zh else 'Original templates · untested'), templates)]:
        s += f'\n## {title}\n\n'
        s += '| ' + ('玩法 | 分类 | 来源状态' if zh else 'Workflow | Category | Evidence') + ' |\n| --- | --- | --- |\n'
        for p in items:
            suffix = '.zh-CN' if zh else ''
            s += f'| [{p["title"][lang]}](cases/{p["id"]}{suffix}.md) | {CATEGORIES[p["category"]][int(zh)]} | {STATUSES[p["source_status"]][int(zh)]} |\n'
    s += '\n## ' + ('模型与资料' if zh else 'Model & resources') + '\n\n'
    s += '- [OpenAI image generation guide](https://developers.openai.com/api/docs/guides/image-generation)\n'
    s += '- [OpenAI image prompting guide](https://developers.openai.com/api/docs/guides/image-prompting)\n'
    s += '- [OpenAI release notes](https://developers.openai.com/api/docs/changelog)\n'
    s += '- [Source audit / 来源核验](docs/SOURCES.md)\n'
    s += '- [Reference collection by EvoLink](https://github.com/Evolink-AI/awesome-gpt-image-2-6-prompts-and-api)\n\n'
    s += ('官方模型包含 `gpt-image-2.6-sunburst` 与 `gpt-image-2.6-flare`。API 与格式能力以官方文档和账号实际开放情况为准。\n\n' if zh else 'Official models include `gpt-image-2.6-sunburst` and `gpt-image-2.6-flare`. Consult current official documentation and your account for API and format availability.\n\n')
    s += '## ' + ('参与维护' if zh else 'Keep the collection useful') + '\n\n'
    s += f'[Submit a prompt / 投稿]({REPO}/issues/new?template=prompt.yml) · [Corrections / 更正]({REPO}/issues/new?template=correction.yml)\n\n'
    s += ('维护方式：修改 JSON → 运行生成器 → 提交 PR。无需安装依赖。\n\n' if zh else 'Maintenance: edit JSON → run the generator → open a PR. No dependencies required.\n\n')
    s += '```sh\npython3 scripts/build.py\npython3 scripts/build.py --check\n```\n\n'
    s += ('这是一次人工整理的首版，不承诺自动更新。欢迎补充有原始出处、版本证据与日期明确的热度数据的新案例。\n\n' if zh else 'This is a manually curated initial edition, not an automated feed. Contributions with original sources, model evidence and dated popularity metrics are welcome.\n\n')
    s += '## ' + ('致谢与许可' if zh else 'Credits & license') + '\n\n'
    s += ('感谢 EvoLink 的来源整理，以及各案例原作者。文档、翻译和原创模板采用 CC BY 4.0，生成脚本采用 MIT。第三方提示词和媒体保留各自权利，见 [LICENSE](LICENSE)。\n\n' if zh else 'Thanks to EvoLink for source discovery and to every credited creator. Documentation, translations and original templates: CC BY 4.0. Generator code: MIT. Third-party prompts and media retain their owners’ rights; see [LICENSE](LICENSE).\n\n')
    s += f"{'最近整理' if zh else 'Last curated'}: {max(p['observed_on'] for p in data)}\n"
    return s


def category_index(data, lang):
    zh = lang == 'zh'
    suffix = '.zh-CN' if zh else ''
    s = '# ' + ('按分类浏览' if zh else 'Browse by category') + '\n\n'
    s += f'[Back / 返回](../README{suffix}.md)\n\n'
    for cat, names in CATEGORIES.items():
        s += f'<a id="{cat}"></a>\n\n## {names[int(zh)]}\n\n'
        for p in data:
            if p['category'] == cat:
                s += f'- [{p["title"][lang]}]({p["id"]}{suffix}.md) — {STATUSES[p["source_status"]][int(zh)]}\n'
        s += '\n'
    return s


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='validate without writing')
    args = parser.parse_args()
    data = json.loads((ROOT / 'data/prompts.json').read_text())
    validate(data)
    outputs = {ROOT / 'README.md': home(data, 'en'), ROOT / 'README.zh-CN.md': home(data, 'zh')}
    outputs[ROOT / 'cases/README.md'] = category_index(data, 'en')
    outputs[ROOT / 'cases/README.zh-CN.md'] = category_index(data, 'zh')
    for p in data:
        outputs[ROOT / 'cases' / (p['id'] + '.md')] = case_page(p, 'en')
        outputs[ROOT / 'cases' / (p['id'] + '.zh-CN.md')] = case_page(p, 'zh')
    stale = []
    for path, content in outputs.items():
        if args.check:
            if not path.exists() or path.read_text() != content:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
    assert not stale, f'Regenerate stale files: {stale}'
    known = set(outputs)
    for path in ROOT.rglob('*.md'):
        content = outputs.get(path, path.read_text())
        for target in re.findall(r'\]\(([^)]+)\)', content):
            if urlparse(target).scheme or target.startswith('#'):
                continue
            local = (path.parent / unquote(target.split('#')[0])).resolve()
            assert local in known or local.exists(), f'Broken link: {path.name} -> {target}'
    print(f'OK: {len(data)} entries, {len(outputs)} generated pages, local links valid')


if __name__ == '__main__':
    try:
        main()
    except (AssertionError, KeyError, ValueError) as exc:
        print(f'Validation failed: {exc}', file=sys.stderr)
        sys.exit(1)
