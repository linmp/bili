接下来要有几十题学习python的基础题



题目来源：[菜鸡教程](https://www.runoob.com/python/python-100-examples.html)的Python 100例

版权归菜鸟教程





**Python 练习实例1**

**题目：**有四个数字：1、2、3、4，能组成多少个互不相同且无重复数字的三位数？各是多少？

**Python 练习实例2**

**题目：**企业发放的奖金根据利润提成。利润(I)低于或等于10万元时，奖金可提10%；利润高于10万元，低于20万元时，低于10万元的部分按10%提成，高于10万元的部分，可提成7.5%；20万到40万之间时，高于20万元的部分，可提成5%；40万到60万之间时高于40万元的部分，可提成3%；60万到100万之间时，高于60万元的部分，可提成1.5%，高于100万元时，超过100万元的部分按1%提成，从键盘输入当月利润I，求应发放奖金总数？

# Python 练习实例3

**题目：**一个整数，它加上100后是一个完全平方数，再加上168又是一个完全平方数，请问该数是多少？

**程序分析：**

假设该数为 x。

1、则：x + 100 = n2, x + 100 + 168 = m2

2、计算等式：m2 - n2 = (m + n)(m - n) = 168

3、设置： m + n = i，m - n = j，i * j =168，i 和 j 至少一个是偶数

4、可得： m = (i + j) / 2， n = (i - j) / 2，i 和 j 要么都是偶数，要么都是奇数。

5、从 3 和 4 推导可知道，i 与 j 均是大于等于 2 的偶数。

6、由于 i * j = 168， j>=2，则 **1 < i < 168 / 2 + 1**。

7、接下来将 i 的所有数字循环计算即可。

# Python 练习实例4

[![Python 100例](https://www.runoob.com/images/up.gif) Python 100例](https://www.runoob.com/python/python-100-examples.html)

**题目：**输入某年某月某日，判断这一天是这一年的第几天？

**程序分析：**以3月5日为例，应该先把前两个月的加起来，然后再加上5天即本年的第几天，特殊情况，闰年且输入月份大于2时需考虑多加一天：



# Python 练习实例5

[![Python 100例](https://www.runoob.com/images/up.gif) Python 100例](https://www.runoob.com/python/python-100-examples.html)

**题目：**输入三个整数x,y,z，请把这三个数由小到大输出。

**程序分析：**我们想办法把最小的数放到x上，先将x与y进行比较，如果x>y则将x与y的值进行交换，然后再用x与z进行比较，如果x>z则将x与z的值进行交换，这样能使x最小。



# Python 练习实例6

[![Python 100例](https://www.runoob.com/images/up.gif) Python 100例](https://www.runoob.com/python/python-100-examples.html)

**题目：**斐波那契数列。 

**程序分析：**斐波那契数列（Fibonacci sequence），又称黄金分割数列，指的是这样一个数列：0、1、1、2、3、5、8、13、21、34、……。

在数学上，费波那契数列是以递归的方法来定义：

```
F0 = 0     (n=0)
F1 = 1    (n=1)
Fn = F[n-1]+ F[n-2](n=>2)
```



# Python 练习实例7

[![Python 100例](https://www.runoob.com/images/up.gif) Python 100例](https://www.runoob.com/python/python-100-examples.html)

**题目：**将一个列表的数据复制到另一个列表中。

**程序分析：**使用列表[:]。



# Python 练习实例8

[![Python 100例](https://www.runoob.com/images/up.gif) Python 100例](https://www.runoob.com/python/python-100-examples.html)

**题目：**输出 9*9 乘法口诀表。

**程序分析：**分行与列考虑，共9行9列，i控制行，j控制列。

程序源代码：



# Python 练习实例9

[![Python 100例](https://www.runoob.com/images/up.gif) Python 100例](https://www.runoob.com/python/python-100-examples.html)

**题目：**暂停一秒输出。 

**程序分析：**使用 time 模块的 sleep() 函数。

程序源代码：





# Python 练习实例10

[![Python 100例](https://www.runoob.com/images/up.gif) Python 100例](https://www.runoob.com/python/python-100-examples.html)

**题目：**暂停一秒输出，并格式化当前时间。 

**程序分析：**无。

程序源代码：



# Python 练习实例11

[![Python 100例](https://www.runoob.com/images/up.gif) Python 100例](https://www.runoob.com/python/python-100-examples.html)

**题目：**古典问题：有一对兔子，从出生后第3个月起每个月都生一对兔子，小兔子长到第三个月后每个月又生一对兔子，假如兔子都不死，问每个月的兔子总数为多少？ 

**程序分析：**兔子的规律为数列1,1,2,3,5,8,13,21....



# Python 练习实例12

[![Python 100例](https://www.runoob.com/images/up.gif) Python 100例](https://www.runoob.com/python/python-100-examples.html)

**题目：**判断101-200之间有多少个素数，并输出所有素数。

**程序分析：**判断素数的方法：用一个数分别去除2到sqrt(这个数)，如果能被整除，则表明此数不是素数，反之是素数。 　　　　





# Python 练习实例13

[![Python 100例](https://www.runoob.com/images/up.gif) Python 100例](https://www.runoob.com/python/python-100-examples.html)

**题目：**打印出所有的"水仙花数"，所谓"水仙花数"是指一个三位数，其各位数字立方和等于该数本身。例如：153是一个"水仙花数"，因为153=1的三次方＋5的三次方＋3的三次方。

**程序分析：**利用for循环控制100-999个数，每个数分解出个位，十位，百位。

程序源代码：





# Python 练习实例14

[![Python 100例](https://www.runoob.com/images/up.gif) Python 100例](https://www.runoob.com/python/python-100-examples.html)

**题目：**将一个正整数分解质因数。例如：输入90,打印出90=2*3*3*5。

**程序分析：**对n进行分解质因数，应先找到一个最小的质数k，然后按下述步骤完成：
 (1)如果这个质数恰等于n，则说明分解质因数的过程已经结束，打印出即可。
 (2)如果n<>k，但n能被k整除，则应打印出k的值，并用n除以k的商,作为新的正整数你n,重复执行第一步。
 (3)如果n不能被k整除，则用k+1作为k的值,重复执行第一步。

程序源代码：





# Python 练习实例15

[![Python 100例](https://www.runoob.com/images/up.gif) Python 100例](https://www.runoob.com/python/python-100-examples.html)

**题目：**利用条件运算符的嵌套来完成此题：学习成绩>=90分的同学用A表示，60-89分之间的用B表示，60分以下的用C表示。

**程序分析：**程序分析：(a>b)?a:b这是条件运算符的基本例子。



# Python 练习实例16

[![Python 100例](https://www.runoob.com/images/up.gif) Python 100例](https://www.runoob.com/python/python-100-examples.html)

**题目：**输出指定格式的日期。

**程序分析：**使用 datetime 模块。



# Python 练习实例17

[![Python 100例](https://www.runoob.com/images/up.gif) Python 100例](https://www.runoob.com/python/python-100-examples.html)

**题目：**输入一行字符，分别统计出其中英文字母、空格、数字和其它字符的个数。

**程序分析：**利用 while 或 for 语句,条件为输入的字符不为 '\n'。



# Python 练习实例18

[![Python 100例](https://www.runoob.com/images/up.gif) Python 100例](https://www.runoob.com/python/python-100-examples.html)

**题目：**求s=a+aa+aaa+aaaa+aa...a的值，其中a是一个数字。例如2+22+222+2222+22222(此时共有5个数相加)，几个数相加由键盘控制。

**程序分析：**关键是计算出每一项的值。



# Python 练习实例19

[![Python 100例](https://www.runoob.com/images/up.gif) Python 100例](https://www.runoob.com/python/python-100-examples.html)

**题目：**一个数如果恰好等于它的因子之和，这个数就称为"完数"。例如6=1＋2＋3.编程找出1000以内的所有完数。

**程序分析：**请参照程序[Python 练习实例14](https://www.runoob.com/python/python-exercise-example14.html)。









# Python 练习实例20

[![Python 100例](https://www.runoob.com/images/up.gif) Python 100例](https://www.runoob.com/python/python-100-examples.html)

**题目：**一球从100米高度自由落下，每次落地后反跳回原高度的一半；再落下，求它在第10次落地时，共经过多少米？第10次反弹多高？











