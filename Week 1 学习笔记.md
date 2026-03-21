# Week 1 学习笔记

# 一、JSON库

### 1.1 JSON是什么、有什么特点

JSON（JavaScript Object Notation）是一种轻量级的数据交换格式，基于 JavaScript 对象语法，但独立于编程语言。它具有易读易写、解析效率高的特点，广泛用于前后端数据传输、配置文件存储等场景，具有以下特点：

- 纯文本格式，跨平台兼容；
- 层级结构清晰（键值对、数组）；
- 支持多种编程语言（Python、Java、JavaScript 等）；
- 比 XML 更简洁，解析速度更快。



### 1.2 JSON 语法规则

#### 1.2.1 基本语法

1. 数据以键值对（key: value） 形式存在，键必须是字符串，值支持多种类型
2. 数据由逗号`,`分隔
3. 使用斜杆 `\\` 来转义字符
4. 大括号`{}`表示对象，中括号 `[]` 表示数组（列表）
5. 字符串必须用双引号`""`包裹，不能用单引号`''`  

#### 1.2.2 支持的数据类型

| 类型   | 示例                | 说明                                            |
| ------ | ------------------- | ----------------------------------------------- |
| 字符串 | `"name": "Vincent"` | 双引号包裹的文本                                |
| 数字   | `"age": 20`         | 可以是整型或者浮点型                            |
| 布尔值 | `"flag":true`       | true / false                                    |
| 数组   | `"list": [1,2,3]`   | 有序集合，可嵌套                                |
| 空值   | `"runoob":null`     | 表示空值（无对应 Python 类型，解析后为 `None`） |
| 对象   | `"obj": {"a": "b"}` | 无序键值对集合，可嵌套                          |

#### 1.2.3 例（作业测试数据节选）

```json
{
    "group_name": "2d_task_1",
    "vectors": [[1,3],[1,2],[2,4],[3,1],[4,3],[5,5],[6,2],[7,7],[8,6],[9,8],[10,9]],
    "ori_axis": [[1,0],[0,1]],
    "tasks": [
        { "type": "axis_angle" },
        { "type": "change_axis", "obj_axis": [[2,1],[1,2]] },
        { "type": "area" },
        { "type": "axis_projection" },
        { "type": "axis_angle"}
    ]
}
```



### 1.3 Python 操作 JSON

> 下面关于用py操作json的知识主要来自菜鸟教程[^《Python3 JSON》] （*此处有脚注哦*）
>
> [^《Python3 JSON》]: [Python3 JSON 数据解析 | 菜鸟教程](https://www.runoob.com/python3/python3-json.html)

Python 内置json库，无需额外安装，可实现 JSON 字符串与 Python 数据结构的相互转换。

#### 1.3.1 核心函数

| 方法           | 作用                         | 入参说明                       |
| -------------- | ---------------------------- | ------------------------------ |
| `json.dumps()` | Python 对象 → JSON 字符串    | `ensure_ascii=False`：保留中文 |
| `json.loads()` | JSON 字符串 → Python 对象    | 入参为合法 JSON 字符串         |
| `json.dump()`  | Python 对象 → 写入 JSON 文件 | 入参：对象 + 文件句柄          |
| `json.load()`  | 读取 JSON 文件 → Python 对象 | 入参为文件句柄                 |

#### 1.3.2 代码

##### a) 读取 JSON 文件（`data.json`）

```python
import json

#读取JSON文件
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

#print第一个任务组的信息
first_group = data[0]
print("组名：", first_group["group_name"])
print("原始向量：", first_group["vectors"])
print("原始坐标轴：", first_group["ori_axis"])
print("任务列表：", first_group["tasks"])
```

输出：

```
组名： 2d_task_1
原始向量： [[1, 3], [1, 2], [2, 4], [3, 1], [4, 3], [5, 5], [6, 2], [7, 7], [8, 6], [9, 8], [10, 9]]
原始坐标轴： [[1, 0], [0, 1]]
任务列表： [{'type': 'axis_angle'}, {'type': 'change_axis', 'obj_axis': [[2, 1], [1, 2]]}, {'type': 'area'}, {'type': 'axis_projection'}, {'type': 'axis_angle'}]
```

##### b) Python 对象转 JSON 字符串/文件

```python
import json

#构造一个Python对象
task_data = {
    "group_name": "2d_task_demo",
    "vectors": [[1,3],[2,4]],
    "ori_axis": [[1,0],[0,1]],
    "tasks": [{"type": "axis_projection"}]
}

#转JSON字符串
json_str = json.dumps(task_data, ensure_ascii=False, indent=4)  # indent 格式化输出
print("JSON 字符串：\n", json_str)

#写入JSON文件
with open("data1.json", "w", encoding="utf-8") as f:
    json.dump(task_data, f, ensure_ascii=False, indent=4)
```

#### 1.3.3 注意事项

1. JSON 键必须是双引号字符串，Python 字典的键可以是单引号/无引号，转换时会自动统一；
2. JSON 不支持 Python 的 `tuple`（元组），`dumps` 时会自动转为数组（`list`）；
3. 读取超大 JSON 文件时，避免直接 `json.load()`，可分段解析（防止内存溢出）；
4. 处理多维向量/坐标轴时，JSON 数组与 Python 列表完全兼容，可直接遍历/运算。



### 1.4 JSON小结

1. JSON 是轻量级数据格式，核心是键值对和数组，与 Python 字典/列表高度兼容；
2. Python `json` 库的 `load/dump`（文件）、`loads/dumps`（字符串）是核心操作；
3. 结合任务场景，需重点掌握多维数组（向量、坐标轴）的解析与类型转换（如转 `numpy` 数组）；
4. JSON 操作是后续实现“坐标系转移、投影、夹角、面积”等任务的基础，需熟练掌握格式解析与数据提取



---



# 二、线性代数

### 2.1 矩阵定义（与行列式的差别）

- **矩阵**：由 $m \times n$ 个数排成的 $m$ 行 $n$ 列的数表，本质是**数表**，形状可方可长。 
- **行列式**：是 $n$ 阶方阵对应的一个**数值**，是特定运算的结果。 
- **同型矩阵**：行数、列数完全相同的两个矩阵。 
- **矩阵相等**：同型矩阵中，对应位置的元素完全相等。



### 2.2 特殊的矩阵 

1. **方阵**：行数 = 列数的矩阵（$n$ 阶方阵）。

2. **列矩阵（列向量）**：只有一列的矩阵，不加区分时可直接看作向量。

3. **零矩阵**：所有元素都为0的矩阵，记作 $O$。 

4. **负矩阵**：将矩阵 $A$ 中所有元素取相反数得到的矩阵，记作 $-A$。

5. **三角矩阵**   

   - **上三角矩阵**：主对角线以下元素全为 $0$。

   - **下三角矩阵**：主对角线以上元素全为 $0$。例：  $$      \begin{bmatrix}      1 & 2 & 3 \\      0 & 1 & 4 \\      0 & 0 & 5      \end{bmatrix}      $$ 

6. **对角矩阵**：既是上三角又是下三角矩阵，非主对角线元素全为 $0$。记作：$\text{diag}(a_1,a_2,\dots,a_n)$     例：$$      \begin{bmatrix}      1 & 0 & 0 \\      0 & 2 & 0 \\      0 & 0 & 3      \end{bmatrix}      = \text{diag}(1,2,3)      $$ 

7. **数量矩阵**：对角线上元素全相等的对角矩阵。例： $$      \begin{bmatrix}      a & 0 & 0 & 0 \\      0 & a & 0 & 0 \\      0 & 0 & a & 0 \\      0 & 0 & 0 & a      \end{bmatrix}      $$ 

8. **单位矩阵**：对角线上元素全为 $1$ 的对角矩阵，记作 $E$（或 $I$）。例： $$      E_3 = \begin{bmatrix}      1 & 0 & 0 \\      0 & 1 & 0 \\      0 & 0 & 1      \end{bmatrix}      $$ 



### 2.3 矩阵的运算 

#### 2.3.1 矩阵加法 

**前提**：只有**同型矩阵**才能相加。 

**规则**：对应位置的元素相加。 



#### 2.3.2 矩阵减法

与加法同理，对应位置元素相减（$A - B = A + (-B)$）。 例：  $$  \begin{bmatrix}  1 & 1 & 4 \\  -2 & 2 & 8 \\  -3 & 3 & 12  \end{bmatrix}  $$



#### 2.3.3 矩阵的数乘 

**定义**：数 $k$ 与矩阵 $A=(a_{ij})_{m \times n}$ 相乘，结果为 $kA=(ka_{ij})_{m \times n}$。 

**规则**：数 $k$ 乘以矩阵的**每一个元素**。 



#### 2.3.4 矩阵相乘 

**前提**：左边矩阵的**列数** = 右边矩阵的**行数**。

**结果矩阵形状**：行数 = 左矩阵行数，列数 = 右矩阵列数。例：$A_{3 \times 5} \cdot B_{5 \times 4} = C_{3 \times 4}$ 

**计算规则**：结果矩阵第 $i$ 行第 $j$ 列的元素 = 左矩阵第 $i$ 行与右矩阵第 $j$ 列对应元素乘积之和。 

**性质**：一般不满足交换律：$AB \neq BA$；若 $AB = BA$，则称矩阵 $A$、$B$ 可交换



#### 2.3.5 矩阵转置 

**定义**：将矩阵 $A$ 的行与列互换得到的新矩阵，记作 $A^T$（或 $A'$）。 

**规则**：若 $A=(a_{ij})_{m \times n}$，则 $A^T=(a_{ji})_{n \times m}$。 

**性质**： $(A^T)^T = A (A+B)^T = A^T + B^T$  - $(kA)^T = kA^T$  - $(AB)^T = B^T A^T$（转置反序律） 例：若 $A = \begin{bmatrix}1 & 2 \\ 3 & 4 \\ 5 & 6\end{bmatrix}$，则 $A^T = \begin{bmatrix}1 & 3 & 5 \\ 2 & 4 & 6\end{bmatrix}$。 



#### 2.3.6 逆矩阵 

**定义**：对于 $n$ 阶方阵 $A$，若存在 $n$ 阶方阵 $B$，使得 $AB = BA = E$，则称 $A$ 可逆，$B$ 为 $A$ 的逆矩阵，记作 $A^{-1}$。 

**前提**：$A$ 的行列式 $|A| \neq 0$（$A$ 为非奇异矩阵/满秩矩阵）。 

**求法**（伴随矩阵法）：$A^{-1} = \frac{1}{|A|} A^*$（$A^*$ 为 $A$ 的伴随矩阵）。 

**性质**：若 $A$ 可逆，则 $A^{-1}$ 唯一  $(A^{-1})^{-1} = A$；  - $(kA)^{-1} = \frac{1}{k}A^{-1}$（$k \neq 0$）；  - $(AB)^{-1} = B^{-1}A^{-1}$（逆矩阵反序律）；  - $(A^T)^{-1} = (A^{-1})^T$。



### 2.4 矩阵与向量的核心关系
#### 2.4.1 向量的矩阵表示
1. 列向量：$n$维向量$\boldsymbol{x} = \begin{bmatrix}x_1\\x_2\\\vdots\\x_n\end{bmatrix}$，本质$n×1$矩阵
2. 行向量：$n$维向量$\boldsymbol{x}^T = \begin{bmatrix}x_1&x_2&\dots&x_n\end{bmatrix}$，本质$1×n$矩阵
3. 本质关联：**有限维向量就是特殊矩阵**，所有矩阵运算均可兼容向量运算

#### 2.4.2 矩阵分块与向量组
1. 任意$m×n$矩阵$A$：可按列分块$A=[{\alpha}_1,{\alpha}_2,\dots,{\alpha}_n]$（${\alpha}_i$为$m$维列向量）
2. 矩阵乘法向量解读：$A_{m×n}\boldsymbol{x}_{n×1} = x_1\boldsymbol{\alpha}_1+x_2\boldsymbol{\alpha}_2+\dots+x_n\boldsymbol{\alpha}_n$，即：矩阵乘列向量 = 矩阵列向量的线性组合

#### 2.4.3 秩与向量线性相关性
1. 矩阵的秩$r(A)$：等于矩阵线性无关列（行）向量的最大个数
2. 满秩矩阵：$n$阶方阵$r(A)=n$ ⇨ 列向量线性无关 ⇨ 矩阵可逆



### 2.5 线性变换

#### 2.5.1 基础定义
1. 线性变换规则：满足**可加性**$T(\boldsymbol{\alpha}+\boldsymbol{\beta})=T(\boldsymbol{\alpha})+T(\boldsymbol{\beta})$、**数乘性**$T(k\boldsymbol{\alpha})=kT(\boldsymbol{\alpha})$
2. 核心定理：**任意有限维线性变换，都可唯一对应一个矩阵**
   - 变换表达：$T(\boldsymbol{x}) = A\boldsymbol{x}$（$A$为线性变换的表征矩阵）

#### 2.5.2 常见基础线性变换
1. 恒等变换：矩阵$E=\begin{bmatrix}1&0\\0&1\end{bmatrix}$，向量保持不变
2. 伸缩变换：矩阵$\begin{bmatrix}k_1&0\\0&k_2\end{bmatrix}$，$x$轴伸缩$k_1$倍，$y$轴伸缩$k_2$倍
3. 旋转变换（逆时针旋转$\theta$）：$A=\begin{bmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{bmatrix}$
4. 投影变换：向$x$轴投影$\begin{bmatrix}1&0\\0&0\end{bmatrix}$

#### 2.5.3 复合线性变换
- 先后执行变换$T_1、T_2$，总表征矩阵：$A=A_2A_1$（**右矩阵先变换，左矩阵后变换**，与乘法顺序一致）



### 2.6 向量点乘与叉乘

#### 2.6.1 向量点乘（内积/数量积）
仅限**同维度行/列向量**，结果为**标量**
1. 代数定义（n维）：
   $\boldsymbol{a}·\boldsymbol{b} = a_1b_1+a_2b_2+\dots+a_nb_n = \boldsymbol{a}^T\boldsymbol{b}$
2. 几何定义（2/3维）：
   $\boldsymbol{a}·\boldsymbol{b}=|\boldsymbol{a}||\boldsymbol{b}|\cos\theta$（$\theta$为两向量夹角）
3. 核心性质
   - 交换律：$\boldsymbol{a}·\boldsymbol{b}=\boldsymbol{b}·\boldsymbol{a}$
   - 模长计算：$|\boldsymbol{a}|=\sqrt{\boldsymbol{a}·\boldsymbol{a}}$
   - 垂直判定：$\boldsymbol{a}⊥\boldsymbol{b} ⇨ \boldsymbol{a}·\boldsymbol{b}=0$
4. 矩阵关联：内积可直接转化为行向量乘列向量矩阵运算

#### 2.6.2 向量叉乘（外积/向量积）
**仅限3维向量**，结果为**新3维向量**
1. 代数定义：设$\boldsymbol{a}=(a_1,a_2,a_3),\boldsymbol{b}=(b_1,b_2,b_3)$
   $$\boldsymbol{a}×\boldsymbol{b}=\begin{vmatrix}\boldsymbol{i}&\boldsymbol{j}&\boldsymbol{k}\\a_1&a_2&a_3\\b_1&b_2&b_3\end{vmatrix}$$
2. 几何意义
   - 模长：$|\boldsymbol{a}×\boldsymbol{b}|=|\boldsymbol{a}||\boldsymbol{b}|\sin\theta$
   - 方向：垂直于$\boldsymbol{a}、\boldsymbol{b}$构成的平面
3. 核心性质
   - 反交换律：$\boldsymbol{a}×\boldsymbol{b}=-\boldsymbol{b}×\boldsymbol{a}$（不满足交换律）
   - 平行判定：$\boldsymbol{a}∥\boldsymbol{b} ⇨ \boldsymbol{a}×\boldsymbol{b}=\boldsymbol{0}$



### 2.7 矩阵求导

#### 2.7.1 三大求导基础类型
1. 标量对向量求导：$y$为标量，$\boldsymbol{x}$为$n$维列向量，结果为梯度向量
2. 向量对矩阵求导：常用布局为**分子布局**
3. 标量对矩阵求导：最常用，适配损失函数优化

#### 2.7.2 必备基础求导公式
设$A、B$为常数矩阵，$\boldsymbol{x}、\boldsymbol{y}$为列向量，$y$为标量
1. 线性基础公式
   - $\frac{\partial (A\boldsymbol{x})}{\partial \boldsymbol{x}} = A^T$
   - $\frac{\partial (\boldsymbol{x}^TA\boldsymbol{x})}{\partial \boldsymbol{x}} = (A+A^T)\boldsymbol{x}$（二次型核心）
2. 内积专项公式
   - $\frac{\partial (\boldsymbol{a}^T\boldsymbol{x})}{\partial \boldsymbol{x}} = \boldsymbol{a}$
3. 迹函数求导（矩阵常用）
   - $\frac{\partial \mathrm{tr}(AX)}{\partial X} = A^T$

#### 2.7.3 核心求导运算法则
1. 加减法则：$\frac{\partial (f±g)}{\partial X}=\frac{\partial f}{\partial X}±\frac{\partial g}{\partial X}$
2. 乘积法则：兼容矩阵乘法维度规则，不可随意交换顺序

例：

​	设$\boldsymbol{x}=\begin{bmatrix}x_1\\x_2\end{bmatrix}$，$y=x_1^2+2x_1x_2$

​	梯度求导：$\frac{\partial y}{\partial \boldsymbol{x}}=\begin{bmatrix}2x_1+2x_2\\2x_1\end{bmatrix}$



---

# 三、多元微分学

### 3.1 多元微分学是什么

多元微分学是一元函数微积分在多元函数中的推广，核心在于将“变化率”和“增量线性逼近”从一维拓展到多维空间。它建立在**极限**与**连续**的基础上，核心目标是**研究多元函数在某点附近的变化规律**。

主要知识点：

1. **极限与连续** → 奠定分析基础  
2. **偏导数** → 描述沿坐标轴方向的变化率  
3. **全微分** → 用线性函数（切平面）逼近函数增量，是“可微性”的体现  
4. **方向导数与梯度** → 描述沿任意方向的变化率及最速方向



### 3.2 基础概念：从邻域到极限

#### 3.2.1 邻域（Neighborhood）
- $$
  U(P_0,\delta) = \left\{ (x,y) \mid \sqrt{(x-x_0)^2 + (y-y_0)^2} < \delta \right\}
  $$
  
- **去心邻域**：不包含中心点 $P_0$，用于定义极限（排除点本身的影响）。 

- **意义**：为讨论“点附近的性态”提供几何范围，多元极限要求 $P$ 以**任意路径**趋近 $P_0$ 时函数值趋于同一常数。

#### 3.2.2 二重极限
- **定义**： 
  $$
  \lim_{(x,y)\to(x_0,y_0)} f(x,y) = A \quad \text{若} \quad \forall \varepsilon>0,\exists \delta>0, \text{当 } 0<|PP_0|<\delta \text{ 时 } |f(x,y)-A|<\varepsilon
  $$
  
  
- **关键点**：趋近方式有无穷多种（直线、曲线、螺旋等）。极限存在必须要求所有路径下的极限值相等。  

- **判别方法**：  
  - 若找到两条不同路径使极限值不同，则极限不存在。  
  - 常用**夹逼准则**、**等价无穷小替换**等一元函数技巧，但**不能使用洛必达法则**（多元函数无直接对应形式）。

#### 3.2.3 连续性
- **定义**：

$$
\displaystyle \lim_{(x,y)\to(x_0,y_0)} f(x,y) = f(x_0,y_0)
$$

- 若函数在区域内每点连续，则称在区域内连续。  
- 与一元区别：多元函数可能在某点沿每个方向（包括x轴、y轴方向）都连续，但整体仍不连续（例如路径依赖的特殊构造）。



### 3.3 偏导数

#### 3.3.1 定义与几何意义
- **对 $x$ 的偏导**：固定 $y=y_0$，视 $z=f(x,y_0)$ 为一元函数在 $x_0$ 处的导数： 

$$
f_x'(x_0,y_0) = \lim_{\Delta x\to 0} \frac{f(x_0+\Delta x, y_0) - f(x_0,y_0)}{\Delta x}
$$

- **几何意义**：曲面 $z=f(x,y)$ 被平面 $y=y_0$ 截得的曲线在点 $(x_0,y_0)$ 处的切线斜率。  
- **偏导函数**：若区域上每点都存在偏导，则得到偏导函数 $\frac{\partial f}{\partial x}$。

#### 3.3.2 高阶偏导数
- **定义**：对偏导函数再求偏导，得到二阶偏导。混合偏导如 $\frac{\partial^2 f}{\partial x \partial y}$ 表示先对 $x$ 后对 $y$ 求导。  
- **重要定理**：若两个混合偏导在区域上**连续**，则它们相等（与求导顺序无关），可简化计算。

#### 3.3.3 偏导与连续的关系
**偏导存在 ≠ 连续**。反例:
$$
f(x,y) = \begin{cases} \frac{xy}{x^2+y^2}, & (x,y)\neq(0,0) \\ 0, & (0,0) \end{cases}
$$
在 $(0,0)$ 处偏导存在（均为0），但函数不连续（沿 $y=x$ 方向极限为 $1/2$）。



### 3.4 全微分

#### 3.4.1 核心思想
用**线性函数**（切平面）近似代替曲面，其误差是比 $\rho = \sqrt{(\Delta x)^2+(\Delta y)^2}$ 更高阶的无穷小。  

- **全增量**：$\Delta z = f(x_0+\Delta x, y_0+\Delta y) - f(x_0, y_0)$  

- **可微定义**：若存在常数 $A,B$ 使得 

$$
\Delta z = A\Delta x + B\Delta y + o(\rho) \quad (\rho\to 0)
$$

​		则称函数在点处**可微**，全微分为 $\mathrm{d}z = A\,\mathrm{d}x + B\,\mathrm{d}y$。

#### 3.4.2 可微的必要条件与充分条件
- **必要条件**：可微 ⇒ 偏导数存在，且 $A = f_x'(x_0,y_0),\ B = f_y'(x_0,y_0)$。  
- **充分条件**：若偏导数在点 $(x_0,y_0)$ 的某邻域内存在且在该点**连续**，则函数在该点可微。  
  - 注：偏导连续是**充分不必要**条件，即存在偏导且可微但偏导不连续的例子。

#### 3.4.3 可微的判别步骤
1. 计算偏导数 $f_x'(x_0,y_0),\ f_y'(x_0,y_0)$（若不存在则不可微）。 
2. 考察极限：

$$
\lim_{(\Delta x,\Delta y)\to(0,0)} \frac{\Delta z - \left[ f_x'(x_0,y_0)\Delta x + f_y'(x_0,y_0)\Delta y \right]}{\sqrt{(\Delta x)^2+(\Delta y)^2}} \stackrel{?}{=} 0
$$

​	若极限为0，则函数可微。

#### 3.4.4 一元与多元概念关系图
| 一元函数    | 多元函数        | 关系                                                         |
| ----------- | --------------- | ------------------------------------------------------------ |
| 可导        | 偏导存在        | 多元中偏导存在是比可微弱的条件                               |
| 可微        | 全微分存在      | 多元中全微分存在是更强的要求（保证沿所有方向的变化线性逼近） |
| 可导 ⇔ 可微 | 偏导存在 ⇏ 可微 | 多元中偏导存在不一定可微（需加上连续性等条件）               |
| 可导 ⇒ 连续 | 偏导存在 ⇏ 连续 | 多元偏导存在不能推出连续                                     |



### 3.5 方向导数与梯度

#### 3.5.1 方向导数
- 沿单位向量 $\mathbf{l}=(\cos\alpha,\cos\beta)$ 的方向导数为：
  $
  \frac{\partial f}{\partial l} = \lim_{t\to 0^+} \frac{f(x_0+t\cos\alpha, y_0+t\cos\beta)-f(x_0,y_0)}{t}
  $
- 若函数可微，则方向导数存在且：
  $
  \frac{\partial f}{\partial l} = f_x \cos\alpha + f_y \cos\beta
  $

#### 3.5.2 梯度
- 梯度向量 $\nabla f = (f_x, f_y)$。  
- **几何意义**：函数在某点沿梯度方向的方向导数最大，值为 $|\nabla f|$；沿负梯度方向下降最快。



### 3.6 小结

| 概念               | 核心作用                   | 判别关键               | 与一元区别             |
| ------------------ | -------------------------- | ---------------------- | ---------------------- |
| **极限**           | 定义多元函数逼近的基础     | 所有路径逼近一致       | 路径无穷多，必须验证   |
| **连续**           | 保证局部值无突变           | 极限值等于函数值       | 偏导存在不能保证连续   |
| **偏导数**         | 沿坐标轴方向的变化率       | 固定其他变量，一元导数 | 存在性弱于可微         |
| **全微分**         | 用切平面局部线性逼近       | 误差是高阶无穷小       | 是比偏导存在更强的条件 |
| **方向导数与梯度** | 任意方向的变化率及最速方向 | 可微时可线性计算       | 多元特有，用于优化     |



---

