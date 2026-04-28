# Multi-Agent 设计中碰到的一些问题

主要针对 [@lidangzzz](https://www.youtube.com/@lidangzzz) 这个视频中的一些问题做出了整理与回答：

> source video: https://youtu.be/34wpQakf0h8?t=2770

## 一、单个 Agent 的能力设计

1. 你会给一个 agent 接入 function calling 吗？
2. 你会给一个 agent 准备一份 markdown，并明确告诉它 markdown 在哪个位置吗？

## 二、multi-agent 的生成与监督

3. 如何正确地 spawn 一个 agent？
4. 你会让一个 agent 去生成几个 agent，然后再由这个 agent 去 supervise 其他 agent 吗？

## 三、定时 action / cron 驱动的 agent 工作流

5. 如何让一个 action cron 在每天 9 点、10 点、11 点分别定时汇报一次？
6. 在这些定时汇报任务中，可以用什么样的 skills 去 fetch 哪些信息？
7. 如果 agent 需要 drive browser、内部软件，或者通过 screenshot / computer use 获取信息，应该如何设计？
8. 获取到的信息，如何复制粘贴到指定位置，再作为 memory 写回 agent markdown？
9. 获取到的信息，如何复制粘贴到指定位置，再作为 memory 写回 agent markdown？

## 四、framework / SDK / orchestration

10. 如何通过 framework 或 SDK 去协调和调度 multi-agent？
