系统设计：
- 楼层为 1..5
- 3台电梯

---

假设：
- 不考虑负载问题，即电梯的容量为正无穷
- 暂时不建模开关门按钮
- 电梯维持开门的时间默认为一个状态，与电梯移动一个楼层的时间相等

Cabin 接受的 move 信号：
- 目标楼层 与 当前楼层 之间的 相对方向

Cabin 接受的 stop 信号由两方面因素决定：
- 一方面因素是 Cabin 对象本身：为了处理 Cabin 的内部请求，向 Controller 发送信号 inner_stop，表示我下一个状态要停下来开门了
- 另一方面因素来自只有 Controller 可见的外部请求，Controller 判定这个即将路过的 Cabin 有义务相应对应楼层的外部请求，则发送 stop 信号将其拦截

区分 move = 0 与 stop = true：
- move = 0 等价于 电梯处于 idle 态，此时 door = closed，电梯的请求队列为空，电梯静置
- stop = true 的意思是向**运行中**的电梯发送中断信号，此时 door = open，电梯的请求队列非空


原本，模型的设计使用了 INVAR 语句来确保满足假设“外部请求会对应至少一个内部请求”。
但事实上，这个假设在现实中是不能被保证的
（举个例子，你在 1 楼准备坐电梯上行，但中途改变了主意，走楼梯去了，那么这个时候外部请求并不会转化为内部请求）。
因此，将 INVAR 的部分全部删除。在我们仔细地修改了模型状态以及转移之后，不加上 INVAR 的模型依然能够满足 SPEC。

添加了门（stop信号）之后，电梯会一直卡在一个楼层动不了:
- 原因: 外部请求不断刷新（想象一下门外有个捣乱者，每次电梯准备关门了就按一次按钮使电梯门再次打开）
- fix: 不能只在按钮为 on 时发送 reset 信号！

---

新增 `2lift.smv`，由于 BDD 模型检测会状态爆炸，无法在可接受时间内验证 SPEC，
因此换成 BMC，并限制一定的步数 k，验证 k 步内 SPEC 的正确性
运行示例: `./NuSMV -bmc -bmc_length 10 2lift.smv`