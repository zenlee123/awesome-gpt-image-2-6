# Prompt playbook / 玩法使用手册

## Pick the right entry / 先选对入口

- **Copy-ready prompt / 双语提示词**: paste, then adjust the subject or exact text.
- **Recreation brief / 玩法改写简报**: a shorter editor-written starting point;
  the source preview is inspiration, not a promised reproduction.
- **Source link / 原文入口**: follow the original page. Do not assume the author
  shared a complete prompt or all settings.

## Six useful workflows / 六种可直接上手的组合

| Goal / 目标 | Start here / 起点 | Prepare / 准备 | Inspect / 检查 |
| --- | --- | --- | --- |
| Reaction GIF / 表情包 | [Rice sticker](../cases/rice-sticker.md) | Character reference / 角色图 | Face, motion and exact caption / 脸、动作、字幕 |
| Product campaign / 商品广告 | [Product hero](../cases/product-hero.md) | Product photo and real copy / 商品图与真实文案 | Shape and label preservation / 形状与标签 |
| Outfit replacement / 试衣 | [Outfit](../cases/docs-outfit.md) | Person + separate clothing references / 人像与服饰图 | Identity, sleeves and seams / 身份、袖口、接缝 |
| Local correction / 局部修改 | [Marked vase](../cases/docs-vase-markup.md) | Original + transparent markup / 原图与透明标记层 | Unchanged surroundings / 周围区域 |
| Brand vector / 品牌矢量 | [Coffee logo](../cases/community-lightlyn-coffee-logo-svg.md) | Brand name and two colors / 名称与双色 | Actual SVG paths and legible text / 矢量路径与文字 |
| Dense information / 信息排版 | [Conference agenda](../cases/community-moss-design-summit-agenda.md) | Checked times and session names / 核准时间与议程 | Every row and reading order / 逐行内容与顺序 |

## Write a brief / 写提示词

先写用途与画面比例，再写主体、布局、材质和光线。必须出现的文字用引号标注；
编辑任务同时列出“要改什么”和“必须保留什么”。多张参考图分别说明角色，例如
图一保留身份、图二提供服装、图三提供背景。每次迭代只改变一个目标。

State the intended use and composition first. Assign each reference one role.
Quote exact on-image text and specify what an edit must preserve. Change one
requirement per iteration so you can judge its effect.

## Model and output controls / 模型与输出控制

[The official guide](https://developers.openai.com/api/docs/guides/image-prompting)
explains Flare, Sunburst, quality, complexity and output formats. Match the API
parameters to the selected model; a prompt saying “SVG” or “GIF” does not by
itself select that output format. App interfaces and API capabilities may differ.

For GIFs, describe a short action and its return to the starting pose. For SVGs,
prefer simple geometry and check the actual returned file. For product edits,
separate preserving the package from adapting lighting to a new scene.

做 GIF 时写清短动作及如何回到首帧。做 SVG 时检查实际返回文件，而不是只看预览。
商品换背景时把“保留商品形状和文字”与“调整光照匹配环境”分开描述。

## Save useful evidence / 保存可复用记录

Keep the exact model, date, prompt, required references, output settings,
number of attempts, result and a short failure note. A striking preview is
not enough to establish repeatability. Never put credentials in a prompt file.

提交案例时保留模型、日期、提示词、参考图来源、输出设置、尝试次数、结果和失败点。
这比简单写“效果很好”更容易让下一位使用者复现。
