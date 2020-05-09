## 0.概念

### 0.1 逻辑结构｜存储结构

 **逻辑结构**：数据元素之间的关系，逻辑上的关系，与存储方式无关

- 集合结构 独立但有整体关系(属于同一个集合的整体关系)
- 线性结构　一对一
- 树状结构　一对多
- 图状结构　多对多

**存储结构**：存储的方式,元素之间的存储位置关系

- 顺序存储 (数据一个接着一个贴在一起的)
- 链式存储(每个数据不一定贴在一起，但是当前数据有下一个数据的位置)



### 0.2 算法的复杂度

**时间复杂度**：

- 常量O(1) | [判断或者运算一次]
- 对数O(log2n) | [二分搜索]
- 线性O(n) | [无序数组的搜索]
- 线性对数O(nlog2n) | [快速排序]
- k次方O(n**k) | [冒泡排序...]

最好、最坏、平均时间复杂度(所以可能情况的概率平均复杂度)



**空间复杂度**：

- 辅助空间相对于输入数据量而言的所占的存储大小



[leetcode之001](https://leetcode-cn.com/problems/two-sum/)

暴力破解：

```python
class Solution:
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        length = len(nums)
        for i in range(length):
            for j in range(i + 1, length):
                if nums[i] + nums[j] == target:
                    return [i, j]
        
```

>时间复杂度为O(n^2) 
>空间复杂度：O(1)



用空间换时间：字典提高速度

```python
class Solution:
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        temp = {}
        length = len(nums)
        for index in range(length):  # 循环拿下标
            if target - nums[index] in temp:  # 判断互补数据是否已经存起来
                i, j = temp[target - nums[index]], index  # 拿出下标
                return [i, j]
            else:
                temp[nums[index]] = index
```

>时间复杂度为O(n) 
>空间复杂度    O(n)



> 尝试一波
>
> [剑指offer之03](https://leetcode-cn.com/problems/shu-zu-zhong-zhong-fu-de-shu-zi-lcof/)
> [剑指offer之05](https://leetcode-cn.com/problems/ti-huan-kong-ge-lcof/)



## 1. 顺序表

**顺序表**，将元素顺序地存放在一块连续的存储区里，元素间的顺序关系由它们的存储顺序自然表示。
**链表**，将元素存放在通过链接构造起来的一系列存储块中。

最常用的数据运算有五种：

- 插入
- 删除
- 修改
- 查找
- 排序

### 1.1 顺序表的操作

### 1.2 Python的顺序表

### 1.3 单向链表的操作

### 1.4 双向链表的概念及操作

## 2. 栈与队列

### 2.1 栈结构实现

### 2.2 队列实现

### 2.3 双端队列实现

## 3. 排序

### 3.1 冒泡排序

### 3.2 选择排序

### 3.3 插入排序

### 3.4 快速排序

### 3.5 希尔排序

### 3.6 归并排序



## 4. 树

### 4.1 二叉树

### 4.2 二叉树的操作