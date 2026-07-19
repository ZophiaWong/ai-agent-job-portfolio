# CommonJS 与 ESM

## 一句话答案

CommonJS 使用 `require/module.exports`，主要是运行时同步加载；ESM 使用 `import/export`，是标准模块系统，支持静态分析和 top-level await。面试重点是能解释两者加载方式、互操作和 package 配置边界。

## 核心机制

CommonJS 是 Node 早期模块系统。`require()` 在运行时执行，模块首次加载后会缓存 `module.exports`。它适合历史生态和同步加载，但静态分析能力弱。

ESM 是 JavaScript 标准模块系统。`import` / `export` 在语法层面声明依赖，便于 tree shaking、静态分析和跨运行时兼容。Node 中是否按 ESM 解释，受文件扩展名 `.mjs/.cjs`、`package.json` 的 `"type": "module"` 或 `"type": "commonjs"` 影响。

互操作有边界：ESM 可以用 `import` 引入 CommonJS default-like 导出，但命名导出推断有限；CommonJS 引入 ESM 通常需要动态 `import()`。真实项目中常见问题是测试、构建工具、tsconfig、package type 不一致。

现代 Node 的例外也要说清版本：`require(esm)` 在 **v20.17.0**（及 v22.0.0）加入，Node **v20.19.0** 起不再
默认显示实验警告、也不再需要 `--experimental-require-module`。即使在支持它的版本，目标 ESM 和它的整个
依赖图也必须**完全同步**，即不含 **top-level await**；否则会抛 `ERR_REQUIRE_ASYNC_MODULE`，应改用
`import()`。维护跨版本包时，先锁定实际 Node 版本和 package `type`，不要把这个例外当成通用兼容策略。

## 常见追问

- CJS 是否可以动态加载？可以，`require()` 可以放在条件分支里。
- ESM 为什么更利于工具链？依赖关系是静态语法，便于分析和优化。
- `__dirname` 在 ESM 中还能直接用吗？不能，需要通过 `import.meta.url` 推导。
- 为什么包升级后 `require()` 报错？可能该包变成 ESM-only；在不满足同步 `require(esm)` 条件或旧 Node 上，应使用 `import()` 或调整模块边界。

## 代码例子

```js
// CommonJS
const path = require("node:path");

module.exports = {
  joinRoot(name) {
    return path.join(process.cwd(), name);
  },
};
```

```js
// ESM
import path from "node:path";

export function joinRoot(name) {
  return path.join(process.cwd(), name);
}
```

## 易错点

- 同一个项目里随意混用 CJS 和 ESM，导致测试、构建、运行环境行为不一致。
- 忽略 `package.json` 的 `"type"`，以为 `.js` 文件总是 CommonJS。
- 在 ESM 中直接使用 `__filename`、`__dirname`。
- 忽略 `require(esm)` 的 Node 版本、完全同步和无 top-level await 条件。

## 实战判断

新项目如果工具链支持，优先 ESM；维护旧 Node 项目时尊重既有 CJS，不为了形式迁移破坏稳定性。TypeScript 项目要同时检查 `module`、`moduleResolution`、运行时 Node 版本和 package type。面试回答时强调模块系统不是语法偏好，而是运行时和工具链契约。

## 自测题

1. CommonJS 模块首次加载后会怎样？
   答：执行模块并缓存 `module.exports`。
2. ESM 的主要优势是什么？
   答：标准化、静态依赖、便于工具分析和跨运行时。
3. Node 如何判断 `.js` 是 CJS 还是 ESM？
   答：主要看最近 package.json 的 `"type"` 字段。

## 参考链接

- [Node.js Modules: CommonJS](https://nodejs.org/api/modules.html)
- [Node.js ECMAScript Modules](https://nodejs.org/api/esm.html)

访问日期：2026-07-19。
