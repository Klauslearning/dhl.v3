# DHL CSV Generator - 智能记忆系统

一个带有智能记忆功能的 DHL 发货 CSV 文件生成器，能够自动记住和填充海关编码、重量和产地信息。

## 🚀 主要功能

### 智能记忆系统
- **海关编码 (Commodity Code)**: 自动匹配和填充 HS 编码
- **重量 (Weight)**: 智能估算和记忆商品重量
- **产地 (Country of Origin)**: 自动填充商品原产国

### 匹配优先级
1. **完整 SKU 匹配** - 最精确的匹配方式
2. **关键词匹配** - 基于商品描述的智能匹配
3. **品牌匹配** - 最低优先级的匹配方式

### 默认重量估算
系统会根据商品描述自动估算重量：

| 商品类别 | 默认重量 (kg) |
|---------|-------------|
| 鞋子 (Shoes) | 1.3 |
| 外套 (Jacket) | 1.5 |
| 服装 (Clothes) | 0.7 |
| 配饰 (Accessories) | 0.3 |
| 其他 | 0.5 |

## 📋 使用方法

### 1. 上传文件
- 支持 Excel (.xlsx, .xls) 和 Numbers 文件
- 系统会自动添加必要的列

### 2. 智能填充
- 系统会自动检查记忆数据库
- 匹配到的商品会自动填充相关信息
- 未匹配的商品会显示默认重量

### 3. 编辑表格
- 手动编辑任何字段
- 系统会记住您的输入
- 下次遇到相同商品时自动填充

### 4. 导出 CSV
- 生成符合 DHL 格式的 CSV 文件
- 所有编辑的数据自动保存到记忆数据库

## 🗄️ 记忆数据库

### 文件位置
`data/sku_memory_db.csv`

### 数据格式
```csv
SKU,Brand,Item Description,Commodity Code,Weight,Country of Origin
M46234,LV,LV SPEEDY BAG,42022100,0.9,CN
1234567,GUCCI,GUCCI BELT,4203301000,0.3,IT
```

### 记忆逻辑
- **一次输入，永久记忆**: 手动输入的任何值都会被记住
- **智能匹配**: 使用多种匹配策略找到最相关的记录
- **自动更新**: 每次导出时自动更新记忆数据库

## 🔧 技术特性

### 匹配算法
- **精确匹配**: 完整 SKU 匹配
- **模糊匹配**: 基于商品描述的关键词匹配
- **品牌匹配**: 作为最后的匹配选项

### 数据验证
- 重量字段支持小数输入
- 产地字段提供常用国家代码选择
- 海关编码字段支持文本输入

### 用户界面
- 实时状态提示
- 智能记忆数据库信息显示
- 一键清空记忆数据库功能

## 📦 安装和运行

### 依赖安装
```bash
pip install streamlit pandas openpyxl
```

### 运行应用
```bash
streamlit run app.py
```

## 🎯 使用场景

### 适合的用户
- 经常处理 DHL 发货的电商卖家
- 需要重复输入相同商品信息的用户
- 希望提高工作效率的物流人员

### 工作流程
1. 上传包含商品信息的 Excel 文件
2. 系统自动填充已知商品的信息
3. 手动补充未知商品的信息
4. 导出 DHL 格式的 CSV 文件
5. 系统自动记住所有输入，下次使用

## 🔄 数据持久化

### 自动保存
- 每次导出 CSV 时自动保存记忆数据
- 支持增量更新，不会覆盖现有数据
- 数据以 CSV 格式存储，便于备份和迁移

### 数据安全
- 本地存储，数据不会上传到云端
- 支持手动清空记忆数据库
- 数据格式简单，易于理解和维护

## 📈 性能优化

### 匹配效率
- 使用正则表达式进行关键词提取
- 设置最小匹配阈值 (30%) 避免误匹配
- 优先使用精确匹配，提高响应速度

### 内存管理
- 按需加载记忆数据
- 避免重复计算
- 优化数据结构，减少内存占用

## 🛠️ 自定义配置

### 修改默认重量
编辑 `utils.py` 中的 `get_default_weight` 函数

### 添加国家代码
修改 `app.py` 中的 `Country of Origin` 选项列表

### 调整匹配阈值
修改 `utils.py` 中的匹配分数阈值 (当前为 0.3)

## 📞 支持

如有问题或建议，请检查：
1. 文件格式是否正确
2. 记忆数据库是否损坏
3. 依赖包是否正确安装

---

**版本**: 2.0  
**更新日期**: 2024  
**功能**: 智能记忆系统 + DHL CSV 生成