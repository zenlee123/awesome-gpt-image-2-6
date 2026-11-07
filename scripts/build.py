#!/usr/bin/env python3
"""Validate source metadata and render a bilingual prompt collection."""
import argparse
from collections import Counter
from datetime import date
from html import escape
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse, unquote

ROOT=Path(__file__).resolve().parents[1]
REPO='https://github.com/zenlee123/awesome-gpt-image-2-6'
CATEGORIES={
 'animation':('GIF & animation','GIF 与角色动画'),
 'editing':('Precise image editing','精确图片编辑'),
 'markup':('Markup-guided edits','圈选与标记编辑'),
 'photography':('Portraits & photography','人像与摄影'),
 'fashion':('Fashion & virtual try-on','时尚与虚拟试衣'),
 'posters':('Posters & typography','海报与文字排版'),
 'commerce':('Product & commerce','商品与电商'),
 'packaging':('Packaging & labels','包装与标签'),
 'food':('Food & restaurants','美食与餐饮'),
 'characters':('Characters & consistency','角色设计与一致性'),
 'illustration':('Illustration & dioramas','插画与微缩场景'),
 'branding':('Logos & SVG assets','Logo 与 SVG 素材'),
 'infographics':('Infographics & slides','信息图与演示页面'),
 'interiors':('Interiors & architecture','室内与建筑'),
 'interfaces':('UI & interface concepts','UI 与界面概念'),
 'fantasy':('Fantasy & surreal worlds','奇幻与超现实场景'),
 'storyboards':('Comics & storyboards','漫画与故事分镜'),
}
STATUSES={
 'official-page-checked':('Official page checked','已核对官方页面'),
 'publisher-page-checked':('Publisher page checked','已核对发布者页面'),
 'creator-post-checked':('Creator post checked','已核对作者原帖'),
 'secondary-only':('Secondary source only','仅核对二手来源'),
 'original-unverified':('Original, untested','原创未实测'),
}
FEATURED=['baroque-gallery','rice-sticker','blink-sway','docs-bakery-svg','made-flare-noodle-menu','made-sunburst-turntable-diagram','docs-room-chairs','community-moss-design-summit-agenda','yir-flavor-lineup','community-ophanim-coastal-lookout','docs-pet-comic','community-lightlyn-weather-icons-svg']


def url_ok(url):
 return isinstance(url,str) and urlparse(url).scheme=='https' and bool(urlparse(url).netloc)


def validate(data):
 assert isinstance(data,list) and data,'Empty catalogue'
 ids=set()
 for p in data:
  pid=p['id']; assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',pid),pid
  assert pid not in ids,f'Duplicate ID: {pid}';ids.add(pid)
  assert p['category'] in CATEGORIES,pid
  assert p['model']=='gpt-image-2.6',pid
  assert p['source_status'] in STATUSES,pid
  assert type(p['reproduced']) is bool,pid
  assert isinstance(p['media_urls'],list),pid
  assert p['creator'].strip(),pid
  for field in ('title','requirements'):
   assert all(p[field][lang].strip() for lang in ('en','zh')),(pid,field)
  date.fromisoformat(p['observed_on'])
  if p['origin']=='curated':
   assert url_ok(p['source_url']) and url_ok(p['via_url']),pid
   assert p['source_status']!='original-unverified',pid
   assert p['prompt_kind'] in ('source-linked','editorial-adaptation','editorial-recreation'),pid
  else:
   assert p['origin']=='original-template' and p['prompt_kind']=='original-template',pid
  if p['prompt'] is not None:
   assert all(p['prompt'][lang].strip() for lang in ('en','zh')),pid
  else:assert p['prompt_kind']=='source-linked',pid
  for url in p['media_urls']:assert url_ok(url),(pid,url)
  for m in p.get('media',[]):assert url_ok(m['url']),(pid,m)
  if p['reproduced']:
   assert all(p['reproduction'].get(k) for k in ('model','settings','date','attempts','inputs','output')),pid
  if p['popularity'] is not None:
   pop=p['popularity']
   assert pop['metric']=='views' and type(pop['count']) is int and pop['count']>=0,pid
   assert url_ok(pop['url']),pid
   date.fromisoformat(pop['observed_on'])
 assert set(FEATURED)<=ids,'Featured ID missing'


def name(p,lang):return p['title'][lang]
def suff(lang):return '.zh-CN' if lang=='zh' else ''
def case_link(p,lang,prefix='cases/'):return f'{prefix}{p["id"]}{suff(lang)}.md'
def category_name(cat,lang):return CATEGORIES[cat][lang=='zh']
def status_name(p,lang):return STATUSES[p['source_status']][lang=='zh']
def prompt_label(p,lang):
 if not p['prompt']:return 'Source link' if lang=='en' else '原文入口'
 if p['origin']=='original-template':return 'Original template' if lang=='en' else '原创模板'
 if p['prompt_kind']=='editorial-recreation':return 'Recreation brief' if lang=='en' else '玩法改写简报'
 return 'Bilingual prompt' if lang=='en' else '双语提示词'


def media(p):
 if p.get('media'):return p['media']
 return [{'url':u,'role':'source','kind':'video' if u.endswith('.mp4') else 'image','caption':{'en':f'Source media {i}','zh':f'来源素材 {i}'}} for i,u in enumerate(p['media_urls'],1)]


def preview(p):
 items=media(p)
 outputs=[m for m in items if m.get('role')=='output']
 pool=outputs or items
 still=[m for m in pool if m.get('kind') not in ('video','mp4') and not re.search(r'\.(mp4|webm)(?:\?|$)',m['url'])]
 if p['id']=='rice-sticker':still=list(reversed(still))
 return still[0]['url'] if still else None


def card(p,lang,prefix='cases/'):
 title=escape(name(p,lang));link=case_link(p,lang,prefix);image=preview(p)
 visual=f'<img src="{escape(image,quote=True)}" width="240" alt="{title}" loading="lazy">' if image else ('▶ Open animation / source' if lang=='en' else '▶ 查看动画 / 来源')
 return f'[{visual}]({link})<br>**[{title}]({link})**<br>{prompt_label(p,lang)}'


def grid(items,lang,prefix='cases/'):
 s='| | | |\n| --- | --- | --- |\n'
 for i in range(0,len(items),3):
  cells=[card(p,lang,prefix) for p in items[i:i+3]]
  s+='| '+' | '.join(cells+['']*(3-len(cells)))+' |\n'
 return s+'\n'


def intro_note(p,lang):
 if p['origin']=='original-template':
  return 'Original untested template. Replace every `{placeholder}` before use.' if lang=='en' else '原创未实测模板。使用前替换所有 `{变量}`。'
 if p['prompt_kind']=='editorial-recreation':
  return 'This is our concise recreation brief inspired by the sourced workflow, not the creator’s original wording. Source images show the original workflow, not a tested result of this brief.' if lang=='en' else '以下是本仓库根据来源玩法撰写的精简改写简报，不是作者原始措辞。来源图片展示原玩法，不代表这份改写提示词的实测结果。'
 return 'Bilingual edited version; a translation or adaptation is not an independently reproduced result.' if lang=='en' else '中英文整理版；翻译或改写不代表本仓库已经独立复现。'


def prompt_block(p,lang):
 return f'{intro_note(p,lang)}\n\n```text\n{p["prompt"][lang]}\n```\n\n'


def case_page(p,lang):
 zh=lang=='zh';s=f'# {name(p,lang)}\n\n[← {"目录" if zh else "Collection"}](../README{suff(lang)}.md) · [Gallery](../GALLERY{suff(lang)}.md)\n\n'
 s+=f'`{p["id"]}` · {category_name(p["category"],lang)} · **{prompt_label(p,lang)}**\n\n'
 variant=p.get('variant','unspecified')
 s+=f'| {"信息" if zh else "Field"} | {"记录" if zh else "Record"} |\n| --- | --- |\n'
 fields=[('Model / 模型',f'GPT Image 2.6 · {variant}'),('Evidence / 核验',status_name(p,lang)),('Reproduced / 独立复现','Yes / 是' if p['reproduced'] else 'No / 否'),('Date / 日期',p['observed_on'])]
 for a,b in fields:s+=f'| {a} | {b} |\n'
 if p.get('source_url'):
  s+=f'\n**{p["creator"]}** · [Original source / 原始来源]({p["source_url"]}) · [Discovered via / 发现来源]({p["via_url"]})\n'
 pop=p['popularity']
 if pop:
  s+=f'\nX views / 帖子浏览量：**{pop.get("display",pop["count"])}** ({pop["observed_on"]}). '
  s+=('Rounded display values are approximate; this measures the whole post, not this individual output.\n' if not zh else '平台缩写为约数；统计的是整条帖子，不是单个输出效果。\n')
 s+=f'\n## {"输入与准备" if zh else "Inputs & preparation"}\n\n{p["requirements"][lang]}\n'
 refs=[m for m in media(p) if m.get('role') in ('reference','input')]
 if refs:
  s+=('\nReference images below are source examples; supply your own authorized inputs.\n' if not zh else '\n下方参考图来自原始来源；实际使用时可替换成你有权使用的素材。\n')
 if p['prompt']:
  s+=f'\n## {"可复制提示词" if zh else "Copy-ready prompt"}\n\n'+prompt_block(p,lang)
  s+=f'<details>\n<summary>{"English" if zh else "简体中文"}</summary>\n\n```text\n{p["prompt"]["en" if zh else "zh"]}\n```\n\n</details>\n'
 else:
  s+=f'\n## {"提示词状态" if zh else "Prompt availability"}\n\n'
  known=p.get('source_prompt_status')=='source-only'
  s+=(('原始提示词在来源页面查看，本页未转载；可通过上方原文入口使用。' if known else '来源未提供可核实的完整提示词。本页保留效果与来源，不编造作者原文。') if zh else ('The source records a public prompt; follow the original-source link. It is not republished here.' if known else 'A complete source prompt was not verified. This page preserves the example and its provenance without inventing the creator’s wording.'))+'\n'
 if p.get('original_prompt'):
  s+=f'\n<details>\n<summary>{"已收录的来源原句" if zh else "Recorded source wording"}</summary>\n\n```text\n{p["original_prompt"]}\n```\n\n</details>\n'
 s+=f'\n## {"使用方法" if zh else "Workflow"}\n\n'
 if zh:
  s+='1. 先核对原文中的输入素材、模型变体与输出格式。\n2. 有提示词时按需替换主体和文字；仅链接案例先阅读来源。\n3. 初次只做一处修改，再检查文字、身份、几何与未修改区域。\n4. 需要 GIF / SVG 时在工具中选择相应格式；文字指令不代替 API 参数。\n'
 else:
  s+='1. Check inputs, model variant and output format at the source.\n2. Customize the brief, or read the original prompt for source-link entries.\n3. Iterate one change at a time; inspect text, identity, geometry and preserved regions.\n4. Select GIF / SVG in your tool when needed; prompt wording does not set API parameters.\n'
 if media(p):
  s+=f'\n## {"来源效果与参考图" if zh else "Source outputs & references"}\n\n'
  for m in media(p):
   caption=m.get('caption',{}).get(lang,m.get('role','source'))
   label={'reference':'Reference / 参考图','input':'Input / 输入','output':'Output / 结果','source':'Source / 来源'}.get(m.get('role'),'Source / 来源')
   s+=f'**{label}** — {caption}\n\n'
   if m.get('kind') in ('video','mp4') or re.search(r'\.(mp4|webm)(?:\?|$)',m['url']):
    s+=f'[▶ Play source animation / 播放来源动画]({m["url"]})\n\n'
   else:s+=f'<img src="{escape(m["url"],quote=True)}" width="560" alt="{escape(caption,quote=True)}" loading="lazy">\n\n'
  s+=('Source outputs are not results generated by this repository. Third-party media retain their rights.\n' if not zh else '这些是来源发布的效果，不是本仓库实测结果。第三方媒体保留各自权利。\n')
 related='../categories/'+p['category']+suff(lang)+'.md'
 s+=f'\n[More in {category_name(p["category"],lang)} / 同类玩法]({related})\n'
 return s


def popular_table(data,lang):
 zh=lang=='zh';seen=set();items=[]
 for p in sorted([p for p in data if p['popularity']],key=lambda p:p['popularity']['count'],reverse=True):
  url=p['popularity']['url']
  if url not in seen:seen.add(url);items.append(p)
 s='| '+('已追踪帖子 | 浏览量快照 | 核验日' if zh else 'Tracked post | View snapshot | Checked')+' |\n| --- | ---: | --- |\n'
 for p in items[:6]:
  pop=p['popularity'];s+=f'| [{name(p,lang)}]({case_link(p,lang)}) | {pop.get("display",pop["count"])} | {pop["observed_on"]} |\n'
 s+=('\n仅比较本库已追踪的帖子；不是全网榜单。缩写数值为约数，同一帖子仅出现一次。\n\n' if zh else '\nThis compares tracked posts only, not the whole web. Abbreviated counts are approximate; shared posts appear once.\n\n')
 return s


def home(data,lang):
 zh=lang=='zh';curated=[p for p in data if p['origin']=='curated'];ready=[p for p in data if p['prompt']];counts=Counter(p['category'] for p in data)
 author_count=len(set(p['creator'] for p in curated));source_only=len([p for p in curated if not p['prompt']]);byid={p['id']:p for p in data}
 s='# Awesome GPT Image 2.6\n\n'
 s+=('**收集全球公开玩法，把灵感变成可用的提示词。**\n\n' if zh else '**Explore sourced workflows. Find a visual idea. Copy a useful prompt.**\n\n')
 s+='[English](README.md) · [简体中文](README.zh-CN.md) · [Visual gallery](GALLERY.md) · [全部提示词](PROMPTS.zh-CN.md) · [JSON](data/prompts.json)\n\n'
 s+=f'![Sources](https://img.shields.io/badge/source_workflows-{len(curated)}-2563eb) ![Prompts](https://img.shields.io/badge/bilingual_briefs-{len(ready)}-7c3aed) ![Categories](https://img.shields.io/badge/categories-{len(counts)}-059669) [![License](https://img.shields.io/badge/docs-CC_BY_4.0-475569)](LICENSE)\n\n'
 if zh:
  s+=f'**{len(curated)} 个来源玩法 · {len(ready)} 份可复制双语提示词/简报 · {len(counts)} 个分类 · {author_count} 个作者/发布者署名。**\n\n'
  s+=f'覆盖角色 GIF、圈选编辑、广告与包装、食物摄影、试衣、SVG、室内改造、漫画、信息图和超现实场景。{source_only} 个仅来源条目提供效果与原文入口，不冒充完整提示词。\n\n'
 else:
  s+=f'**{len(curated)} source workflows · {len(ready)} copy-ready bilingual prompts/briefs · {len(counts)} categories · {author_count} credited creators/publishers.**\n\n'
  s+=f'GIFs, markup edits, ads, packaging, food, fashion, SVG, interiors, comics, infographics and surreal worlds. {source_only} source-link entries provide outputs and provenance without pretending to include complete prompts.\n\n'
 s+='## '+('从这里开始' if zh else 'Start here')+'\n\n'
 s+=f'- [🖼 {"看全部效果图" if zh else "Browse the visual gallery"}](GALLERY{suff(lang)}.md)\n- [📋 {"直接复制提示词" if zh else "Copy prompts and recreation briefs"}](PROMPTS{suff(lang)}.md)\n- [🧭 {"按任务选玩法" if zh else "Choose by task"}](cases/README{suff(lang)}.md)\n- [🛠 {"输入、参数与迭代方法" if zh else "Inputs, settings and iteration"}](docs/PLAYBOOK.md)\n\n'
 s+='## '+('精选效果' if zh else 'Featured workflows')+'\n\n'+grid([byid[x] for x in FEATURED],lang)
 s+=('预览来自已署名来源，不是本仓库生成。改写简报不等于原作者提示词，具体标记见详情页。\n\n' if zh else 'Previews are credited source outputs. Recreation briefs are editorial rewrites, not the creators’ exact prompts. See each detail page.\n\n')
 s+='## '+('已追踪热度' if zh else 'Tracked community interest')+'\n\n'+popular_table(data,lang)
 s+='## '+('玩法分类' if zh else 'Browse by task')+'\n\n| '+('分类 | 来源案例 | 可复制提示词 / 简报' if zh else 'Category | Source workflows | Copy-ready briefs')+' |\n| --- | ---: | ---: |\n'
 for cat in CATEGORIES:
  items=[p for p in data if p['category']==cat]
  if not items:continue
  s+=f'| [{category_name(cat,lang)}](categories/{cat}{suff(lang)}.md) | {sum(p["origin"]=="curated" for p in items)} | {sum(bool(p["prompt"]) for p in items)} |\n'
 s+='\n## '+('如何读核验标签' if zh else 'How to read the labels')+'\n\n'
 if zh:
  s+='- **已核对原帖/发布者页面**：读取了来源的模型归属；不等于独立复现。\n- **玩法改写简报**：本库根据公开玩法撰写，原始效果不证明改写提示词能复现。\n- **原文入口**：完整提示词在来源查看，或未公开；详情页会区分。\n- **原创未实测**：可编辑起点，尚未生成验证。\n\n'
 else:
  s+='- **Source checked**: model attribution was read at the original page; no independent reproduction implied.\n- **Recreation brief**: our rewrite inspired by the workflow; the source image does not validate the rewrite.\n- **Source link**: follow the original page for the prompt, or see the missing-prompt note.\n- **Original, untested**: an editable starting point without generated validation.\n\n'
 s+=f'[Source audit / 来源核验](docs/SOURCES.md) · [Legacy 2.5 references / 旧版资料](docs/LEGACY.md)\n\n'
 s+='## '+('参与维护' if zh else 'Contribute')+'\n\n'
 s+=f'[Submit a workflow / 投稿]({REPO}/issues/new?template=prompt.yml) · [Correct attribution / 更正]({REPO}/issues/new?template=correction.yml) · [Guide](CONTRIBUTING.md)\n\n'
 s+='```sh\npython3 scripts/build.py\npython3 scripts/build.py --check\n```\n\n'
 s+=('维护方式为人工研究与整理，未设置自动采集任务。生成器会校验数据、分类与内部链接。\n\n' if zh else 'Research is manually curated; no automated collection job is configured. The generator validates metadata, categories and internal links.\n\n')
 s+='## '+('致谢与许可' if zh else 'Credits & license')+'\n\n'
 s+='[EvoLink](https://github.com/Evolink-AI/awesome-gpt-image-2-6-prompts-and-api) · [Raphael OpenLab](https://github.com/RaphaelAI-OpenLab/awesome-gpt-image-2-6) · [OpenAI documentation](https://developers.openai.com/api/docs/guides/image-prompting) · every credited creator.\n\n'
 s+='Repository documentation: CC BY 4.0. Code: MIT. Imported catalogue metadata: MIT, credited in [attribution notes](docs/ATTRIBUTION.md). Third-party prompts and media retain their owners’ rights. [License](LICENSE).\n\nLast curated / 最近整理: **2026-11-07**\n'
 return s


def listing(data,lang,mode):
 zh=lang=='zh';suffx=suff(lang)
 title=('全部效果图' if zh else 'Visual gallery') if mode=='gallery' else ('可复制提示词与简报' if zh else 'Copy-ready prompts & briefs')
 s=f'# {title}\n\n[← Home / 首页](README{suffx}.md)\n\n'
 if mode=='gallery':s+=('来源案例与原创模板分开标记；没有图片的条目不会展示虚构效果。\n\n' if zh else 'Source examples and original templates are labeled separately. Missing images are not replaced with fabricated results.\n\n')
 else:s+=('这里集中展示全部可复制文本。改写版本与原创模板均未独立实测，输入要求和来源见详情。\n\n' if zh else 'All copy-ready text in one place. Recreation briefs and original templates are untested; open the details for inputs and sources.\n\n')
 for cat in CATEGORIES:
  items=[p for p in data if p['category']==cat and (mode=='gallery' or p['prompt'])]
  if not items:continue
  s+=f'<a id="{cat}"></a>\n\n## {category_name(cat,lang)}\n\n'
  if mode=='gallery':s+=grid(items,lang)
  else:
   for p in items:
    s+=f'### [{name(p,lang)}]({case_link(p,lang)})\n\n'+prompt_block(p,lang)
 return s


def category_page(data,cat,lang):
 items=[p for p in data if p['category']==cat]
 s=f'# {category_name(cat,lang)}\n\n[← Home / 首页](../README{suff(lang)}.md) · [All prompts / 全部提示词](../PROMPTS{suff(lang)}.md)\n\n'
 s+=grid(items,lang,'../cases/')
 return s


def category_index(data,lang):
 s=f'# {"按分类浏览" if lang=="zh" else "Browse by category"}\n\n[← Home / 首页](../README{suff(lang)}.md)\n\n'
 for cat in CATEGORIES:
  items=[p for p in data if p['category']==cat]
  if not items:continue
  s+=f'<a id="{cat}"></a>\n\n## [{category_name(cat,lang)}](../categories/{cat}{suff(lang)}.md)\n\n'
  for p in items:s+=f'- [{name(p,lang)}]({case_link(p,lang,"")}) · {prompt_label(p,lang)}\n'
  s+='\n'
 return s


def check_links(outputs):
 known=set(outputs)
 for path in sorted(set(ROOT.rglob('*.md'))|known):
  if '.git' in path.parts:continue
  content=outputs[path] if path in outputs else path.read_text()
  for target in re.findall(r'\]\(([^)]+)\)',content):
   if urlparse(target).scheme or target.startswith('#'):continue
   location,_,anchor=target.partition('#')
   local=(path.parent/unquote(location)).resolve()
   assert local in known or local.exists(),f'Broken link: {path.relative_to(ROOT)} -> {target}'
   if anchor and local.suffix=='.md':
    body=outputs[local] if local in outputs else local.read_text()
    assert f'id="{anchor}"' in body,f'Missing explicit anchor: {target}'


def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
 data=json.loads((ROOT/'data/prompts.json').read_text());validate(data)
 outputs={}
 for lang in ('en','zh'):
  sf=suff(lang)
  outputs[ROOT/f'README{sf}.md']=home(data,lang)
  outputs[ROOT/f'GALLERY{sf}.md']=listing(data,lang,'gallery')
  outputs[ROOT/f'PROMPTS{sf}.md']=listing(data,lang,'prompts')
  outputs[ROOT/f'cases/README{sf}.md']=category_index(data,lang)
  for cat in CATEGORIES:
   if any(p['category']==cat for p in data):outputs[ROOT/f'categories/{cat}{sf}.md']=category_page(data,cat,lang)
  for p in data:outputs[ROOT/f'cases/{p["id"]}{sf}.md']=case_page(p,lang)
 check_links(outputs)
 stale=[]
 for path,content in outputs.items():
  if args.check:
   if not path.exists() or path.read_text()!=content:stale.append(str(path.relative_to(ROOT)))
  else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content,encoding='utf-8')
 assert not stale,f'Regenerate stale files: {stale}'
 print(f'OK: {len(data)} entries, {sum(bool(p["prompt"]) for p in data)} bilingual briefs, {len(outputs)} pages; metadata and internal links valid')

if __name__=='__main__':
 try:main()
 except (AssertionError,KeyError,ValueError) as exc:print(f'Validation failed: {exc}',file=sys.stderr);sys.exit(1)
