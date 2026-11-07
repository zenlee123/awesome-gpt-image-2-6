# 标注花瓶后局部换色

[← 目录](../README.zh-CN.md) · [Gallery](../GALLERY.zh-CN.md)

`docs-vase-markup` · 圈选与标记编辑 · **玩法改写简报**

| 信息 | 记录 |
| --- | --- |
| Model / 模型 | GPT Image 2.6 · flare,sunburst |
| Evidence / 核验 | 已核对官方页面 |
| Reproduced / 独立复现 | No / 否 |
| Date / 日期 | 2026-11-07 |

**OpenAI** · [Original source / 原始来源](https://developers.openai.com/api/docs/guides/image-prompting#guide-an-edit-with-markup) · [Discovered via / 发现来源](https://github.com/RaphaelAI-OpenLab/awesome-gpt-image-2-6)

## 输入与准备

提供原始图片及同尺寸透明 PNG 标记图。

下方参考图来自原始来源；实际使用时可替换成你有权使用的素材。

## 可复制提示词

以下是本仓库根据来源玩法撰写的精简改写简报，不是作者原始措辞。来源图片展示原玩法，不代表这份改写提示词的实测结果。

```text
仅把标记花瓶改成钴蓝色，保留形状、枝干和厨房，移除标记。
```

<details>
<summary>English</summary>

```text
Recolor only the marked vase cobalt blue. Preserve its shape, stems and kitchen; remove the markup.
```

</details>

## 使用方法

1. 先核对原文中的输入素材、模型变体与输出格式。
2. 有提示词时按需替换主体和文字；仅链接案例先阅读来源。
3. 初次只做一处修改，再检查文字、身份、几何与未修改区域。
4. 需要 GIF / SVG 时在工具中选择相应格式；文字指令不代替 API 参数。

## 来源效果与参考图

**Output / 结果** — 将餐桌花瓶改为钴蓝色并移除红色标记的厨房图像（GPT Image 2.6 Flare 输出）

<img src="https://developers.openai.com/images/platform/guides/image-prompting/markup-vase-gpt-image-2-6-flare.webp" width="560" alt="将餐桌花瓶改为钴蓝色并移除红色标记的厨房图像（GPT Image 2.6 Flare 输出）" loading="lazy">

**Output / 结果** — 将餐桌花瓶改为钴蓝色并移除红色标记的厨房图像（GPT Image 2.6 Sunburst 输出）

<img src="https://developers.openai.com/images/platform/guides/image-prompting/markup-vase-gpt-image-2-6-sunburst.webp" width="560" alt="将餐桌花瓶改为钴蓝色并移除红色标记的厨房图像（GPT Image 2.6 Sunburst 输出）" loading="lazy">

**Reference / 参考图** — 参考输入图：餐桌上条纹花瓶被红圈标记的厨房照片

<img src="https://developers.openai.com/images/platform/guides/image-prompting/markup-vase-input-gpt-image-2-6.webp" width="560" alt="参考输入图：餐桌上条纹花瓶被红圈标记的厨房照片" loading="lazy">

这些是来源发布的效果，不是本仓库实测结果。第三方媒体保留各自权利。

[More in 圈选与标记编辑 / 同类玩法](../categories/markup.zh-CN.md)
