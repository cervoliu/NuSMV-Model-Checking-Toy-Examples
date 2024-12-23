# A

引入状态变量 state 表示当前算法处于哪个阶段（类似于 program counter 的作用）

state 可能取值为 select, swap 以及 end，分别表示选择第 i 个最小值，交换当前位置与最小值位置，结束状态。

正确性应该表示为算法一定会终止，且终止时满足
$$ arr[0] \leq arr[1], arr[1] \leq arr[2], \dots $$

以 $len=3$ 为例，正确性的 LTL spec 为

$$ F (state = end) \land G (state = end \rightarrow arr[0] \leq arr[1] \land arr[1] \leq arr[2]) $$

## a1

该算法是正确的，总能终止:
```
-- specification  F state = end  is true
-- specification  G (state = end -> (arr[0] <= arr[1] & arr[1] <= arr[2]))  is true
```

## a2

有时正确，有时不正确:

```c++
line 1: int i, j;
line 2: int len = arr.size();
line 3: for (i = 0; i < len - 1; i++)
line 4:     min_idx = 0; // 将每轮循环 min_idx 初始值从 i 改成 0 
line 5:     for (j = i + 1; j < len; j++)
line 6:         if (arr[j] < arr[min_idx])
line 7:             min_idx = j;
line 8:     swap(arr[i], arr[min_idx]);
```

正确的例子: arr = {1, 2, 3}

不正确的例子: arr = {2, 3, 1}

```
-- specification  F state = end  is true
-- specification  G (state = end -> (arr[0] <= arr[1] & arr[1] <= arr[2]))  is false
-- as demonstrated by the following execution sequence
Trace Description: LTL Counterexample 
Trace Type: Counterexample 
  -> State: 1.1 <-
    arr[0] = 2
    arr[1] = 2
    arr[2] = 1
    i = 0
    j = 1
    min_idx = 0
    state = select
  -> State: 1.2 <-
    j = 2
  -> State: 1.3 <-
    j = 3
    min_idx = 2
    state = swap
  -> State: 1.4 <-
    arr[0] = 1
    arr[2] = 2
    i = 1
    j = 2
    min_idx = 0
    state = select
  -> State: 1.5 <-
    j = 3
    state = swap
  -> State: 1.6 <-
    arr[0] = 2
    arr[1] = 1
    i = 2
    state = select
  -- Loop starts here
  -> State: 1.7 <-
    state = end
  -- Loop starts here
  -> State: 1.8 <-
  -> State: 1.9 <-
```

## a3

有时能终止，有时不能终止:

```c++
line 1: int i, j;
line 2: int len = arr.size();
line 3: for (i = 0; i < len - 1; i++)
line 4:     min_idx = i;
line 5:     for (j = i + 1; true; j++)
line 6:         if (arr[j] < arr[min_idx])
line 7:             min_idx = j;
line 8:             break;
line 9:     swap(arr[i], arr[min_idx]);
```

能终止的例子: arr = {2, 3, 1}

不能终止的例子: arr = {1, 2, 3}


# B

选择一个简单的计算数组元素的和的算法:

```C
int sum = 0;
for (int i = 0; i < n; i++) {
    sum += arr[i];
}
```

正确性 spec: 
```
LTLSPEC G (-16 <= sum & sum <= 15);

LTLSPEC G (state = end -> sum = (arr[0] + arr[1] + arr[2]));
```

## b1

会出现溢出的情况.

```
CTLSPEC AG !overflow;
```
会找出反例，说明存在一个状态 overflow 为 true.

## b2

当加法不溢出时，算法是正确的.
```
-- specification  G ((!overflow & state = end) -> sum = (arr[0] + arr[1]) + arr[2])  is true
```

## b3

如果加减法真的溢出了，该算法是错误的。反例:
```
-- specification  G (state = end -> sum = (arr[0] + arr[1]) + arr[2])  is false
-- as demonstrated by the following execution sequence
Trace Description: LTL Counterexample 
Trace Type: Counterexample 
  -> State: 1.1 <-
    arr[0] = 15
    arr[1] = 15
    arr[2] = -14
    sum = 0
    i = 0
    state = start
    temp = 15
  -> State: 1.2 <-
    state = loop
  -> State: 1.3 <-
    sum = 15
    i = 1
    temp = 30
  -> State: 1.4 <-
    sum = -2
    i = 2
    temp = -16
  -> State: 1.5 <-
    sum = -16
    i = 3
  -- Loop starts here
  -> State: 1.6 <-
    state = end
  -- Loop starts here
  -> State: 1.7 <-
  -> State: 1.8 <-
```