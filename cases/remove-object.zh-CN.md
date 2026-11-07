# 移除物体并保留场景

[← 目录](../README.zh-CN.md) · [Gallery](../GALLERY.zh-CN.md)

`remove-object` · 精确图片编辑 · **双语提示词**

| 信息 | 记录 |
| --- | --- |
| Model / 模型 | GPT Image 2.6 · flare,sunburst |
| Evidence / 核验 | 已核对官方页面 |
| Reproduced / 独立复现 | No / 否 |
| Date / 日期 | 2026-11-07 |

**@OpenAI** · [Original source / 原始来源](https://developers.openai.com/api/docs/guides/image-prompting#remove-an-object) · [Discovered via / 发现来源](https://github.com/Evolink-AI/awesome-gpt-image-2-6-prompts-and-api/blob/codex/gpt-image-2-5-prompts/cases/gpt-image-2-6.md#gpt-image-2-6-case-252)

## 输入与准备

上传含待移除物体的照片；先保存原图用于比较。

## 可复制提示词

中英文整理版；翻译或改写不代表本仓库已经独立复现。

```text
移除男子手中的花，保留人物、手势、背景、构图和光照，其他内容不变。
```

<details>
<summary>English</summary>

```text
Remove the flower from the man's hand. Preserve the person, hand pose, background, framing, and lighting. Change nothing else.
```

</details>

<details>
<summary>已收录的来源原句</summary>

```text
Remove the flower from man's hand. Do not change anything else.
```

</details>

## 使用方法

1. 先核对原文中的输入素材、模型变体与输出格式。
2. 有提示词时按需替换主体和文字；仅链接案例先阅读来源。
3. 初次只做一处修改，再检查文字、身份、几何与未修改区域。
4. 需要 GIF / SVG 时在工具中选择相应格式；文字指令不代替 API 参数。

## 来源效果与参考图

**Source / 来源** — 来源素材 1

<img src="https://pub-62cf7640cd0f4066b60933bd2e9b85ef.r2.dev/github-repo-media/awesome-gpt-image-2-5-prompts/assets/gpt-image-2-6/man-with-blue-hat.webp" width="560" alt="来源素材 1" loading="lazy">

**Source / 来源** — 来源素材 2

<img src="https://pub-62cf7640cd0f4066b60933bd2e9b85ef.r2.dev/github-repo-media/awesome-gpt-image-2-5-prompts/assets/gpt-image-2-6/man-with-no-flower-gpt-image-2-6-flare.webp" width="560" alt="来源素材 2" loading="lazy">

**Source / 来源** — 来源素材 3

<img src="https://pub-62cf7640cd0f4066b60933bd2e9b85ef.r2.dev/github-repo-media/awesome-gpt-image-2-5-prompts/assets/gpt-image-2-6/man-with-no-flower-gpt-image-2-6-sunburst.webp" width="560" alt="来源素材 3" loading="lazy">

这些是来源发布的效果，不是本仓库实测结果。第三方媒体保留各自权利。

[More in 精确图片编辑 / 同类玩法](../categories/editing.zh-CN.md)
