# TypeScript 类型收窄、泛型和结构化类型

## 一句话答案

TypeScript 类型系统是静态检查工具，不会自动带来运行时校验；类型收窄让代码在分支中获得更具体类型，泛型表达输入输出关系，结构化类型意味着“形状兼容即可赋值”。

## 核心机制

类型收窄基于控制流分析。`typeof`、`instanceof`、`in`、字面量比较、自定义 type guard 都能把 union type 收窄成更具体类型。好的收窄能减少 unsafe cast，让错误在编译期暴露。

泛型用于表达类型之间的关系，而不是让代码看起来高级。例如 `function first<T>(items: T[]): T | undefined` 表示返回值类型与数组元素类型一致。泛型约束 `extends` 可以限制可用属性。

TypeScript 是结构化类型系统，只要对象形状兼容就能赋值，不要求显式继承同一个类或接口。这很适合 JavaScript 生态，但也意味着过宽的类型可能误接收不该接收的对象。外部输入仍需要 zod、valibot、class-validator 等运行时校验。

## 常见追问

- `unknown` 和 `any` 区别？`unknown` 使用前必须收窄，`any` 放弃类型检查。
- interface 和 type 怎么选？多数对象契约用 interface，union、映射和组合类型常用 type；实际按团队规范。
- 泛型什么时候过度设计？当类型关系不需要复用或一个具体类型已足够清楚时。
- TypeScript 能防止线上收到坏 JSON 吗？不能，必须运行时校验。

## 代码例子

```ts
type ToolResult =
  | { ok: true; text: string }
  | { ok: false; error: string };

function render(result: ToolResult): string {
  if (result.ok) {
    return result.text;
  }
  return `failed: ${result.error}`;
}
```

```ts
function pluck<T, K extends keyof T>(item: T, key: K): T[K] {
  return item[key];
}

const value = pluck({ id: 1, name: "rag" }, "name");
```

## 易错点

- 用 `as SomeType` 逃避错误，掩盖真实类型不匹配。
- API 边界只写 TypeScript 类型，不做运行时 schema 校验。
- 泛型参数太多，调用方和维护者都看不懂。
- 忘记结构化类型的宽松性，把“形状兼容”误认为“业务语义兼容”。

## 实战判断

后端项目里，TypeScript 类型适合表达内部服务契约、DTO、配置形状和工具函数关系；外部输入必须用 runtime schema 校验。面试时可以强调 `unknown` 优于 `any`，union + narrowing 优于散落的布尔字段，泛型只在能保留输入输出关系时使用。

## 自测题

1. TypeScript 类型会在运行时自动校验吗？
   答：不会，编译后类型被擦除。
2. `unknown` 为什么比 `any` 安全？
   答：`unknown` 使用前必须收窄，`any` 会跳过类型检查。
3. 结构化类型是什么意思？
   答：只要对象形状兼容就可赋值，不要求显式继承。

## 参考链接

- [TypeScript Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)
- [TypeScript Generics](https://www.typescriptlang.org/docs/handbook/2/generics.html)
