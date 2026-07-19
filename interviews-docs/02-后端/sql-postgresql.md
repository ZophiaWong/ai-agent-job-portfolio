# SQL 与 PostgreSQL：查询、事务和执行计划

主要能力：`C12.01`。

关联能力：`C07.03`。本题按[统一练习协议](../practice-protocol.md)练习。

## 冷启动：先写 SQL，再推演

以下练习采用 PostgreSQL 语法和默认行为作为假设。仓库不引入数据库依赖；如果你没有 PostgreSQL 或 `psql`，只做确定性手工推演，不要把这份笔记写成已执行证据。

把下面 fixture 保存为 `sql-postgresql-cold.sql`：

```sql
CREATE TABLE accounts (
    account_id bigint PRIMARY KEY,
    org_id bigint NOT NULL,
    name text NOT NULL
);

CREATE TABLE payments (
    payment_id bigint PRIMARY KEY,
    account_id bigint NOT NULL REFERENCES accounts(account_id),
    status text NOT NULL,
    amount numeric(12, 2) NOT NULL,
    paid_at timestamptz NOT NULL
);

INSERT INTO accounts VALUES
    (1, 10, 'A'), (2, 10, 'B'), (3, 20, 'C');

INSERT INTO payments VALUES
    (101, 1, 'paid',    80, '2026-07-01T08:00:00Z'),
    (102, 1, 'paid',    30, '2026-07-02T08:00:00Z'),
    (103, 2, 'failed', 200, '2026-07-03T08:00:00Z'),
    (104, 3, 'paid',   120, '2026-07-04T08:00:00Z'),
    (105, 3, 'paid',    10, '2026-07-05T08:00:00Z');
```

在文件中继续写下面三部分，答案和推演记录到 `sql-postgresql-reasoning.md`。

1. 用 `JOIN`、`GROUP BY`、`HAVING` 和窗口函数 `OVER (...)` 找出已支付总额不小于 100 的账户，并在各自组织内按总额排名。先写预期行，再逐步推演 JOIN 和分组后的中间结果。
2. 写一个 `TRANSACTION`事务，用带条件的 `UPDATE ... RETURNING` 将账户 1 的两笔已支付记录改为 `refunded`。分析 PostgreSQL 默认隔离级别下两个会话同时执行该语句的结果，以及失败时如何回滚。
3. 候选索引是 `CREATE INDEX ... ON payments (account_id, paid_at) WHERE status = 'paid'`。为查询加上 `EXPLAIN`，写出你期望观察的计划节点或计划属性，再说明小表为什么仍可能选顺序扫描。

有 PostgreSQL 环境时，可用一个临时库运行 fixture 和查询，保留 `psql` 输出与 `EXPLAIN (ANALYZE, BUFFERS)` 计划。没有环境时，产物只能标为 inspectable：检查语法、预期结果和计划推理，不得标为 runnable 或 executed。

## 迁移题

新需求要保留每个账户，即使它没有已支付记录，并显示总额 0。改写 JOIN 和过滤条件，然后重新列出预期结果。说明把 `status = 'paid'` 放在 `ON` 或 `WHERE` 子句会怎样改变行集。

## 延迟复测与证据边界

三天后换一组 fixture，从空白文件重写查询和事务，存为 `sql-postgresql-retest.sql`。阅读完 SQL 不能证明掌握；提示后改对的查询不算独立证据。只有实际保留的数据库输出才是执行证据，手工推演要单独标注。

<!-- 练习分隔线：完成冷答后再继续 -->

## 参考查询

一种写法是先聚合，再在聚合结果上计算排名：

```sql
WITH totals AS (
    SELECT
        a.account_id,
        a.org_id,
        a.name,
        SUM(p.amount) AS paid_total
    FROM accounts AS a
    JOIN payments AS p ON p.account_id = a.account_id
    WHERE p.status = 'paid'
    GROUP BY a.account_id, a.org_id, a.name
    HAVING SUM(p.amount) >= 100
)
SELECT
    account_id,
    org_id,
    name,
    paid_total,
    ROW_NUMBER() OVER (PARTITION BY org_id ORDER BY paid_total DESC, account_id) AS org_rank
FROM totals
ORDER BY org_id, org_rank;
```

预期两行：A 的 `paid_total` 为 110，C 为 130；两者在各自组织内的 `org_rank` 都是 1。B 只有 `failed` 记录，不进入聚合结果。

## 参考事务

```sql
BEGIN; -- TRANSACTION starts here

UPDATE payments
SET status = 'refunded'
WHERE account_id = 1 AND status = 'paid'
RETURNING payment_id;

COMMIT;
-- 任一语句失败时，客户端应 ROLLBACK，而不是继续提交。
```

普通 `UPDATE` 会对它实际更新的行加锁，这道题不需要为了加锁而先 `SELECT`。在默认的 `READ COMMITTED` 下，第二个会话遇到正在更新的目标行时会等待。第一个会话提交后，第二个会话对行的新版本重新检查 `WHERE` 条件；`status` 已经是 `refunded`，因此这次 `RETURNING` 通常返回 0 行。调用方应将“更新两行”和“更新零行”定义成明确的业务结果。

### `FOR UPDATE` 用在先读后决策的事务

当事务必须先读取余额，再根据读值修改多行，以维护跨行业务不变量时，可以在事务中使用 `SELECT ... FOR UPDATE`。这和本题的单条条件更新不是同一个场景。如果不变量涉及尚不存在的行或跨多条查询的谓词，还需根据并发契约考虑 `SERIALIZABLE` 和重试。

## EXPLAIN 和索引评分要点

```sql
CREATE INDEX payments_paid_account_time_idx
    ON payments (account_id, paid_at)
    WHERE status = 'paid';

EXPLAIN
SELECT payment_id, amount, paid_at
FROM payments
WHERE account_id = 1 AND status = 'paid'
ORDER BY paid_at DESC;
```

候选计划可能出现部分索引的 `Index Scan`，且索引顺序可以服务 `account_id` 过滤和 `paid_at` 排序。这不是固定答案：fixture 只有几行，规划器选 `Seq Scan` 很正常。没有 PostgreSQL 统计信息和实际计划时，这只是可检查的推理。

| 等级 | 可观察表现 |
| --- | --- |
| 0–1 | 只能复述语法，写不出预期行。 |
| 2 | 查询大致正确，但没有解释 JOIN 中间结果、事务失败或计划属性。 |
| 3 | 能推导预期行，说清锁、回滚、索引和规划器选择，并正确标注执行与手工检查的边界。 |
| 4 | 变更数据保留或并发约束后，能重新选 JOIN、事务级别和索引，并用实际计划校正预测。 |
