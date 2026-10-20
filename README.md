# Qianshao 前哨

`frontier-interview-writer` 是一个面向中文深度内容的 Codex Skill。它将创始人、管理者、研究者与业务操盘手的访谈、播客、演讲或事件材料，重组为有来源、有取舍、有边界感的中文特稿。

## 适用场景

- 「前哨」栏目文章
- 海外长访谈转中文深度稿
- 创始人访谈、长视频或播客的主题化重组
- 基于一手来源的产品、组织、商业或投资信号解读

它不用于生成逐字稿、完整翻译或无来源的行业判断。

## 安装

```bash
git clone https://github.com/JoyaJames/Qianshao.git ~/.codex/skills/frontier-interview-writer
```

重启 Codex 后，可直接使用 `$frontier-interview-writer`。

## 仓库结构

```text
Qianshao/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── frontier-writing-dna.md
│   ├── editorial-logic.md
│   └── anti-template.md
└── scripts/
    └── article_rhythm_audit.py
```

## 核心原则

- 区分可验证事实、来源主张与编辑推断。
- 不用时间先后代替因果证明。
- 保留来源中的不确定性，不虚构场景、引语、亲历体验或行业共识。
- 用一条中心论点组织材料，不按原访谈顺序机械搬运。

## 节奏检查

```bash
python3 scripts/article_rhythm_audit.py path/to/draft.md
```

该脚本只生成人工复核提示，不会根据分数机械改写文章。

## License

MIT
