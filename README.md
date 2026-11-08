# KK的博客

博客使用 [Hugo Extended](https://gohugo.io/) 和 [OINK](https://oink.pgsty.com/)，文章源文件位于 `content/blog/post/`。历史文章保留原来的 `/年/月/日/文章名.html` 地址，请不要随意修改其 `url`、标题或日期：外部链接和 Utterances 评论可能依赖这些信息。

## 写作与预览

需要 Git、Go 1.27.3 或更新版本、Hugo Extended 0.168.0 或更新版本。首次构建需要联网下载固定版本的 OINK 主题。

在 `content/blog/post/` 新建 Markdown 文件，例如：

```markdown
---
title: 文章标题
date: 2026-11-02
author: spin6lock
tags: [技术]
---

文章正文。
```

也可运行 `python3 compose.py`，按提示输入文章标题和 tag（多个用英文或中文逗号分隔，留空表示无标签）。也支持 `python3 compose.py "文章标题"` 跳过标题询问。脚本会将标题、tag、当前日期和默认作者等 metadata 写入文件，再打开 `$EDITOR` 指定的编辑器（默认 `vim`）；编辑完成后为新文章调整中英文间距，然后自动提交并推送。提交或推送失败时脚本会停止。

新文章如需指定固定链接，可在 front matter 中添加 `url: /2026/11/02/example.html`。本地预览：

```sh
hugo server
```

打开 <http://localhost:1313/>。发布前也可检查生产构建：

```sh
hugo --cleanDestinationDir --gc --minify --environment production --printPathWarnings
```

## 发布

推送到 `master` 后，GitHub Actions 自动构建并发布到 GitHub Pages，无需提交 `public/`。仓库的 **Settings → Pages → Source** 应设为 **GitHub Actions**。评论继续使用原有的 Utterances 仓库及文章标题映射，评论区明暗模式随站点切换；统计配置在 `hugo.yaml`。
