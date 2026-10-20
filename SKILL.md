---
name: frontier-interview-writer
description: Turn founder, executive, researcher, and operator interviews, podcasts, talks, transcripts, or source-led incident material into a Chinese editorial feature with visible sources, selective restructuring, and bounded industry judgment. Use for 前哨栏目、海外长访谈转中文文章、创始人访谈改写、长视频转深度稿、访谈重组、信号型行业文章, or when the user wants a sourced narrative article rather than a summary, translation, or dialogue transcript.
---

# Frontier Interview Writer

Turn first-hand interviews and related evidence into a readable Chinese feature. Act as a signal interpreter: select, verify, restructure, explain, and question without manufacturing certainty.

## Route the request

- Use **interview-led mode** when one interview, podcast, or talk supplies most of the article.
- Use **incident-led mode** when a dated event, product release, or company action is the evidence spine and interviews explain it.
- Use **research-led mode** only when primary documents and several attributed sources are available. Do not disguise a thin source set as a reported feature.
- If the user wants a cleaned dialogue transcript, timestamped notes, or full translation, use a transcript or translation workflow first. Apply this skill only when editorial restructuring and independent judgment are requested.

For every writing or revision task, read [frontier-writing-dna.md](references/frontier-writing-dna.md). When multiple source types, causality, or external evidence are involved, also read [editorial-logic.md](references/editorial-logic.md). After the factual and structural pass is stable, read [anti-template.md](references/anti-template.md).

## Workflow

### 1. Build the source ledger

Record the original title, speaker, host or publisher, publication date, URL, transcript status, and any timestamps used. Separate material into:

- verified events and independently checkable facts;
- attributed claims from the interview or document;
- editorial inference.

Do not place quotation marks around a translated paraphrase. Keep speaker attribution near consequential claims. Verify names, companies, products, numbers, dates, and specialist terms against primary sources where possible.

If the source is third-party copyrighted material, write a transformative feature or detailed digest. Do not reproduce a full transcript or substitute translation.

### 2. Apply the topic gate

Proceed only when the material contains at least three of these:

- direct experience making product, growth, organization, investment, or business decisions;
- two or more verifiable cases, actions, or numbers;
- a judgment that has not already become an industry slogan;
- a clear connection to the target readers' current decisions;
- enough evidence for the editor to add a bounded second-order judgment.

Reject promotional interviews, motivational talk, and material that yields only isolated quotes.

### 3. Write the editorial brief before drafting

Privately define:

```text
Core question: what does this article help the reader understand?
Primary line: what changes from the opening to the ending?
Evidence spine: which event, decision, or sequence carries the article?
Source contribution: what does the interview explain that public facts do not?
Editorial contribution: what can be inferred, compared, or questioned?
Boundary: what remains unproven or unresolved?
```

If these lines cannot be written clearly, gather more evidence or narrow the story.

### 4. Restructure by argument

Do not preserve the source's chronology by default. Group material around four to six questions. Choose one or two load-bearing sections and allow them more space than background sections.

For each section:

1. establish the question, action, or conflict;
2. supply a case, number, decision, or scene;
3. explain why it changes the reader's understanding;
4. state uncertainty or a counterexample when needed.

Do not force every section to use the same sequence or end with a takeaway.

### 5. Draft the standard article shape

- **Title:** person or company plus an underappreciated change, or a supported judgment plus what it changes. Keep tension; do not invent causality.
- **Editorial note:** 80–180 Chinese characters naming the source and the question pursued. If the article opens with a strong scene, reduce this to a short note.
- **Body:** four to six unevenly weighted sections organized by argument.
- **Frontier observation:** close one main line. Connect the evidence to a concrete choice for the target readers; state what remains uncertain.
- **Sources:** list the original program or document, link, date, speaker and host. Add timestamps for important quotations and independent links for external data.

Treat the following only as a starting range, not a quota: source-based material often supplies about 65%–75% of the article, editorial explanation about 20%–30%, and scene-setting about 5%–10%.

### 6. Revise in the right order

Run these passes separately:

1. **Evidence:** verify facts, attribution, translation, dates, numbers, and links.
2. **Logic:** audit the primary line, source layers, and every causal verb.
3. **Structure:** move or cut sections that do not serve the central question.
4. **Language:** replace abstract labels with people, actions, processes, and consequences.
5. **Rhythm:** remove repeated paragraph shapes, generic connectors, and section-by-section elevation.

Run the bundled warning script on Markdown drafts:

```bash
python3 scripts/article_rhythm_audit.py path/to/draft.md
```

Use warnings to locate passages for human review. Never rewrite mechanically to satisfy a score.

## Non-negotiable boundaries

- Keep fact, attribution, and inference distinguishable.
- Treat time order as chronology, not proof of causality.
- Preserve uncertainty from the source.
- Never invent first-hand use, access, emotion, scenes, quotations, or industry consensus.
- Explain an English or technical term briefly at first mention; use the shortest accurate form afterward.
- Keep only numbers that establish scale, timing, comparison, threshold, or consequence.
- Prefer complete reasoning paragraphs over a chain of slogans or single-sentence “golden quotes.”
- Let the ending resolve the opening question once. Do not append a generic list of lessons.

## Delivery check

Before returning the article, confirm:

- the original source and key timestamps are visible;
- the title does not overstate causality or certainty;
- each core section contains concrete evidence;
- consequential claims have nearby attribution;
- editorial judgment adds context, conditions, or counterexamples;
- the final observation follows from the article's evidence;
- formulaic prose and repetitive section shapes have been reviewed;
- unknowns are stated instead of silently filled.
