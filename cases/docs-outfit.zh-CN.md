# 保留人物身份换装

[← 目录](../README.zh-CN.md) · [Gallery](../GALLERY.zh-CN.md)

`docs-outfit` · 时尚与虚拟试衣 · **玩法改写简报**

| 信息 | 记录 |
| --- | --- |
| Model / 模型 | GPT Image 2.6 · flare,sunburst |
| Evidence / 核验 | 已核对官方页面 |
| Reproduced / 独立复现 | No / 否 |
| Date / 日期 | 2026-11-07 |

**OpenAI** · [Original source / 原始来源](https://developers.openai.com/api/docs/guides/image-prompting#preserve-identity-and-change-clothing) · [Discovered via / 发现来源](https://github.com/RaphaelAI-OpenLab/awesome-gpt-image-2-6)

## 输入与准备

请提供下方描述对应的主体或场景参考图。

下方参考图来自原始来源；实际使用时可替换成你有权使用的素材。

## 可复制提示词

以下是本仓库根据来源玩法撰写的精简改写简报，不是作者原始措辞。来源图片展示原玩法，不代表这份改写提示词的实测结果。

```text
图一用于身份，其余图片用于服装。只替换穿搭，保留脸部、姿态和环境。
```

<details>
<summary>English</summary>

```text
Use image one for identity and the others for clothing. Replace the outfit; preserve face, pose and setting.
```

</details>

## 使用方法

1. 先核对原文中的输入素材、模型变体与输出格式。
2. 有提示词时按需替换主体和文字；仅链接案例先阅读来源。
3. 初次只做一处修改，再检查文字、身份、几何与未修改区域。
4. 需要 GIF / SVG 时在工具中选择相应格式；文字指令不代替 API 参数。

## 来源效果与参考图

**Output / 结果** — 博物馆中的女子换上参考服装后的图像（GPT Image 2.6 Flare 输出）

<img src="https://developers.openai.com/images/platform/guides/image-prompting/outfit-gpt-image-2-6-flare.webp" width="560" alt="博物馆中的女子换上参考服装后的图像（GPT Image 2.6 Flare 输出）" loading="lazy">

**Output / 结果** — 博物馆中的女子换上参考服装后的图像（GPT Image 2.6 Sunburst 输出）

<img src="https://developers.openai.com/images/platform/guides/image-prompting/outfit-gpt-image-2-6-sunburst.webp" width="560" alt="博物馆中的女子换上参考服装后的图像（GPT Image 2.6 Sunburst 输出）" loading="lazy">

**Reference / 参考图** — 参考输入图：灰色长靴服装参考

<img src="https://developers.openai.com/images/platform/guides/image-prompting/boots.webp" width="560" alt="参考输入图：灰色长靴服装参考" loading="lazy">

**Reference / 参考图** — 参考输入图：米色西装外套服装参考

<img src="https://developers.openai.com/images/platform/guides/image-prompting/jacket.webp" width="560" alt="参考输入图：米色西装外套服装参考" loading="lazy">

**Reference / 参考图** — 参考输入图：白色背心服装参考

<img src="https://developers.openai.com/images/platform/guides/image-prompting/tank-top.webp" width="560" alt="参考输入图：白色背心服装参考" loading="lazy">

**Reference / 参考图** — 参考输入图：用作人物身份参考的博物馆女子照片

<img src="https://developers.openai.com/images/platform/guides/image-prompting/woman-in-museum.webp" width="560" alt="参考输入图：用作人物身份参考的博物馆女子照片" loading="lazy">

这些是来源发布的效果，不是本仓库实测结果。第三方媒体保留各自权利。

[More in 时尚与虚拟试衣 / 同类玩法](../categories/fashion.zh-CN.md)
