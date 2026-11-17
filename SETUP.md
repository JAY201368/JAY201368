# 设计手册 · 深绿米色手绘版

主页：<https://github.com/JAY201368>
仓库：<https://github.com/JAY201368/JAY201368>（public）

**一句话原则：所有视觉资产都是本仓库自绘的 SVG，不依赖第三方主题。** 第三方只保留两张数据卡（连续贡献、提交曲线），并把它们的配色改到同一套色板里。

---

## 1. 设计语言

| 令牌 | 色值 | 用途 |
| :-- | :-- | :-- |
| `INK` | `#1F3B2C` | 深绿墨色：线稿、正文、深色底 |
| `INK2` | `#33543F` | 次级绿：辅助文字 |
| `PAPER` | `#F4EBD5` | 米色纸：所有卡片底 |
| `RUST` | `#A9472B` | 赭红：印章、编号、强调箭头 |
| `GOLD` | `#B8873A` | 芥末金：页脚、装饰线、衬线下的手绘横线 |

字体只有两套，且**必须是系统字体栈**（SVG 以 `<img>` 方式加载，不能拉外部字体）：

- 衬线：`Georgia, 'Iowan Old Style', 'Palatino Linotype', Palatino, serif`
- 打字机：`'Courier New', 'Nimbus Mono PS', ui-monospace, monospace`

手绘感靠三件事：

1. **抖动描边**：`rough_rect()` / `rough_line()` 沿路径取点后随机偏移 ±1.1px，再叠一条偏移 7px 的内框（透明度 .3），像用笔画了两遍。
2. **位移滤镜**：`feTurbulence` + `feDisplacementMap`（`rough` / `rough2`），让直线轻微发抖。
3. **纸面颗粒**：一层黑色 `feTurbulence` 颗粒，透明度 5%（深色底 9%），避免大片纯色显得像网页而不是印刷品。

---

## 2. 资产清单（`assets/`）

| 文件 | 尺寸 | 说明 |
| :-- | :-- | :-- |
| `hero.svg` | 1200×372 | 深绿横幅：双层手绘框、四角裁切线、左边相机线稿、右边终端线稿、衬线大名 |
| `stamp.svg` | 600×118 | 赭红橡皮章，旋转 −2.4°，实际显示 300px |
| `rule.svg` | 1200×46 | 分隔线 + 中央太阳纹，用赭红所以深浅色都可见 |
| `notes.svg` | 800×536 | "Field notes" 纸卡：AGENTS / PHOTOGRAPHY / SYSTEMS 三段 + TOOLS 行 |
| `card-*.svg` | 800×230 | 4 张项目卡，每张一整块可点击区域（外面套 `<a>`） |
| `footer.svg` | 1200×240 | 深绿收尾幅：横线 + 菱形装饰 + 斜体引言 |

全部由 `tools/build_assets.py` 生成。**改文案、改配色都改脚本，不要手改 SVG。**

```bash
python3 tools/build_assets.py     # 重新生成 assets/*.svg
```

脚本里改这三处就够：

- 顶部 `INK / PAPER / RUST / GOLD` → 整体换肤
- `notes()` 里的 `rows` → 中间那张纸卡的文案
- `main()` 里的 `card(...)` 调用 → 项目卡的标题、描述、标签、图标

---

## 3. README 结构

```text
hero.svg
stamp.svg
rule.svg
## What I work on   →  notes.svg
## Selected work    →  card-maestro / codingagentneo / hikaridaily / zf2lumix
## Numbers          →  streak-stats + activity-graph（改配色后的第三方卡）
footer.svg
```

README 里几乎没有可读文字——所有 copy 都烘进了 SVG，靠 `alt` 文本兜底（无障碍和搜索引擎读的是 alt，改文案时别漏）。

---

## 4. 两张数据卡

**连续贡献**（`streak-stats.demolab.com`）参数一一对应色板：

```text
background=F4EBD5  纸底      border=1F3B2C  边框
stroke=1F3B2C      分隔线    ring=A9472B    当前连续的外环
fire=A9472B        火苗      currStreakNum=1F3B2C / sideNums=1F3B2C  数字
currStreakLabel=A9472B  sideLabels=33543F  dates=6B7F6E
border_radius=3     disable_animations=true
```

`disable_animations=true` 是必须的：该服务默认把文字设成 `opacity:0` 再用动画淡入，遇到「减少动态效果」的系统设置或慢网络时会一直空白。

**提交曲线**（`github-readme-activity-graph`）：`bg_color=F4EBD5` `color=1F3B2C` `line=1F3B2C` `point=A9472B` `area=true` `area_color=33543F` `radius=3`，出来就是一张米色方格纸。

为什么换掉上一版的东西：

- `github-readme-stats` 公共实例长期 503，放弃；
- `github-profile-summary-cards` 只能选预设主题，调不出米色 + 深绿，放弃；
- `skillicons.dev` 是扁平现代风，和手绘语言冲突，换成纸卡里的 TOOLS 文字行；
- `readme-typing-svg` 的打字机动画在这种静态印刷语言里像异物，删掉；
- `shields.io` 徽章同理删掉，身份信息交给橡皮章。

---

## 5. 排错

- **图不显示**：README 用相对路径 `assets/xxx.svg`，GitHub 会重写成 `/user/repo/raw/...`。改文件名后要同步改 README，否则 404。
- **改了 SVG 主页没变**：图片走 `camo.githubusercontent.com` 缓存，等 1～2 分钟，或在 README 的 URL 后加 `?v=2`。
- **文字位置跑偏**：SVG 字体是系统字体，Windows 上的 Georgia 和 macOS 上宽度略有差异。留 20px 余量，别让文本顶到边框。
- **深色模式**：纸卡本身就是米色，两种主题都成立，所以不需要 `<picture>`；只有纯线稿才需要双版本（现在没有）。
- **网络**：本机代理 `http://127.0.0.1:7890`；`git push` 卡住时 `export https_proxy=http://127.0.0.1:7890`。GitHub Actions（如果以后加）在境外，不需要代理。

---

## 6. 还能加什么

- **新项目卡**：复制 `main()` 里任意一条 `card(...)`，加一个 `ICONS` 线稿（80×80 视口内画），重新生成。
- **博客链接**：域名 `www.jay201368.blog` 目前没有 DNS 记录，所以主页里没放；恢复后可以做成一张小纸签 SVG，或直接在正文加一行 markdown 链接。
- **贡献蛇 / 3D 图**：暂时不建议（数据太稀疏，会把「大部分格子是灰的」放大成视觉主体）。等每天都有绿格子再考虑，历史提交里有可复用的配置。

---

## 7. 内容原则

1. 一屏之内说清你是谁：横幅 + 印章 + 一句话。
2. 只放你能解释的项目，四张卡刚好，每张只有一个 `↗`。
3. 数据卡是装饰，别让它当主角；稀疏的图不如不放。
