# GitHub Profile README 操作手册

本目录就是你的个人主页仓库，仓库名必须是 **`JAY201368`**（和用户名完全一致，大小写一致），`README.md` 放根目录，GitHub 才会把它渲染在 `github.com/JAY201368` 顶部。

---

## 1. 三条命令发布

```bash
cd ~/Desktop/JAY201368      # 仓库已 git init 并暂存，可直接提交
git commit -m "feat: profile readme"
gh repo create JAY201368 --public --source=. --remote=origin --push
```

`gh` 已经以 `JAY201368` 登录且有 `repo` + `workflow` 权限，上面最后一条会直接建仓并推送。

推送完成后访问 <https://github.com/JAY201368> 即可看到主页。若显示的是旧内容，等 1～2 分钟或强刷（⌘⇧R）。

---

## 2. 首次发布后必须做的一步

贡献蛇（README 底部那段）现在是**注释状态**，因为 `output` 分支还不存在，直接放出来会是裂图。

```bash
gh workflow run snake.yml
gh run watch          # 等它跑完（约 1 分钟）
```

跑完后，把 `README.md` 里 `<!-- 贡献蛇：…` 到 `-->` 这对注释去掉（整段保留，只删注释符号），再 `git commit -am "feat: snake" && git push` 即可。

可选：3D 贡献图

```bash
gh workflow run 3d-contrib.yml
```

跑完后把 README 里“可选：3D 贡献图”那段注释放开，URL 保持不变（它会把图提交到 `main` 的 `profile-3d-contrib/` 下）。

---

## 3. 每个区块怎么改

| 区块 | 现在用的东西 | 想改什么 |
| :-- | :-- | :-- |
| 顶部渐变横幅 | `capsule-render`（`type=waving`） | `color=0:..,40:..,100:..` 三段色；`type=rect/cylinder/soft` 换形状；`animation=twinkling/blinking` |
| 打字机一行 | `readme-typing-svg` | `lines=` 用 `;` 分隔多条；`font=` 换字体；亮/暗两版只差 `color=` |
| 徽章 | `shields.io` + `komarev` 访问量 | 格式：`https://img.shields.io/badge/<左>-<右>-<色>?style=flat-square&logo=<图标名>` |
| What I work on | Markdown 表格 | 直接加行，别超过 4 行，主页不是简历 |
| Selected work | 4 张卡 = 你 pin 的 4 个仓库 | 换仓库就替换链接/`<sub>` 描述/`项目页 ↗` 地址 |
| Toolbox | `skillicons.dev` | `i=` 里的缩写名，逗号分隔；不认的图标去官网图标表查 |
| 数据卡 | `github-profile-summary-cards` | `theme=` 换配色：`default / github / tokyonight / blue_green / radical` |
| 连续贡献 | `streak-stats.demolab.com` | `date_format` 可删；`hide_border=true` 保持无边框 |
| 提交曲线 | `github-readme-activity-graph` | `days=90` 控制跨度；`area=true` 填充；`theme=` |
| 页脚 | `capsule-render`（`section=footer`） | 与顶部用同一组色，视觉才闭环 |

**没用的：`github-readme-stats`。** 公共实例（含各种 vercel 镜像）当前被限流，返回 “Something went wrong”。这个主页改用 `github-profile-summary-cards` + `streak-stats` 覆盖同样的信息。要真用 stats 卡，就 fork 一个实例并填自己的 token（见第 5 节）。

---

## 4. 排错清单

- **图不显示 / 显示裂图**：先在浏览器里直接打开那个图片 URL。403/404 说明仓库或分支不存在（最常见：snake 还没跑、仓库不是 public）。503/402 说明第三方服务被限流，换服务或过会儿再试。
- **改了地址但主页没变**：GitHub 图片走 `camo.githubusercontent.com` 缓存。加个无意义参数强制刷新，比如结尾追 `&v=2`。
- **深浅色模式**：README 里的 `<picture>` + `prefers-color-scheme` 是 GitHub 官方支持的写法，两个 `srcset` 必须都可用，否则暗色下裂图。
- **网络**：本机代理 `http://127.0.0.1:7890`。`git`/`gh` 走 HTTPS 时若卡住：`export https_proxy=http://127.0.0.1:7890`。GitHub Actions 在境外，不需要代理。
- **表格右侧留白**：Markdown 表格宽度由内容决定，列宽靠内容长度接近；`<br>` 换行比空格更稳。
- **Markdown 表格里不能写标题/多段落**，只能用行内 HTML：`<br>` `<sub>` `<code>` `<a>` `<strong>`。

---

## 5. 可选进阶（按需，别一次全上）

**自建 stats 实例**（解决限流、能统计私有仓库）

1. Fork `anuraghazra/github-readme-stats` → Vercel 导入 → 环境变量 `PAT_1=<你的 classic token>`。
2. README 里把 `github-profile-summary-cards.vercel.app` 换成你的域名，参数不变。

**补回博客链接**：你的 GitHub 资料里填的是 `www.jay201368.blog`，但目前该域名**没有 DNS 记录**（`dig` 查不到），所以主页里我暂时没放这个链接，避免死链。域名恢复后在徽章那行加：

```md
[![Blog](https://img.shields.io/badge/blog-jay201368.blog-0ea5e9?style=flat-square&logo=rss&logoColor=white)](https://www.jay201368.blog)
```

**WakaTime 编码时长**：装 `WakaTime` 插件 → 开 `wakatime` 的 GitHub 集成 → 把生成的卡片贴到 Numbers 区块上方。

**低层彩蛋**：`capsule-render` 的 `text` 可以换成中文，但部分字体不支持，建议保持英文 ID。

---

## 6. 三条内容原则（比花活重要）

1. **一屏之内说清你是谁**：标题 + 一句话 + 徽章，够了。招生官/面试官不往下滚。
2. **只展示你能解释的项目**：这 4 个 pin 各有 live 页面，卡片里都给了 ↗，比堆 20 个徽章有效。
3. **数据卡是装饰，不是成绩单**：贡献图稀疏时它只会暴露稀疏。等积累起来再让它当主角。
