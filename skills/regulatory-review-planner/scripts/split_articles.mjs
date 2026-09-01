#!/usr/bin/env node

import { readFile, writeFile } from "node:fs/promises";

const inputPath = process.argv[2];
const outputPath = process.argv[3] || "draft_articles.json";

if (!inputPath) {
  console.error("用法：node scripts/split_articles.mjs <输入文本.txt> [输出JSON文件.json]");
  process.exit(1);
}

const text = await readFile(inputPath, "utf8");
const normalized = text.replace(/\r\n/g, "\n").trim();

const articleStartPattern = /(^|\n)([ \t　]*第[一二三四五六七八九十百千万零〇\d]+条(?:[ \t　]*[。.:：、）)]?|[ \t　]+))/g;
const articleMatches = [...normalized.matchAll(articleStartPattern)];
const parts = articleMatches
  .map((match, index) => {
    const start = match.index + match[1].length;
    const end = index + 1 < articleMatches.length
      ? articleMatches[index + 1].index
      : normalized.length;
    return normalized.slice(start, end);
  })
  .map((part) => part.trim())
  .filter(Boolean);

const draftArticles = parts.length > 1 ? parts : normalized.split(/\n{2,}/).map((p) => p.trim()).filter(Boolean);

await writeFile(
  outputPath,
  `${JSON.stringify({ draft_articles: draftArticles }, null, 2)}\n`,
  "utf8",
);

console.log(
  JSON.stringify(
    {
      inputPath,
      outputPath,
      draftArticles: draftArticles.length,
    },
    null,
    2,
  ),
);
