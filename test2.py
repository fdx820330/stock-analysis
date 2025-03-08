import os

# 示例数据
data = [
    "DeepSeek|688561",
    "DeepSeek|688590",
    "DeepSeek|688609",
    "DeepSeek|688620",
    "DeepSeek|688777",
    "DeepSeek|839493",
    "DeepSeek|839790",
    "DeepSeek|872953",
    "AI医疗|000710",
    "AI医疗|002044",
    "AI医疗|002524",
    "AI医疗|002524",
    "AI医疗|002524",
    "AI医疗|002777",
    "AI医疗|300143"
]

# 定义一个字典来存储合并后的数据
merged_data = {}

# 遍历数据，将同类的股票代码合并并剔除重复数据
for line in data:
    block_name, stock_code = line.split("|")
    if block_name not in merged_data:
        merged_data[block_name] = []
    # 检查股票代码是否已经存在，不存在则添加
    if stock_code not in merged_data[block_name]:
        merged_data[block_name].append(stock_code)

# 输出合并后的数据到文件
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for block_name, stock_codes in merged_data.items():
    file_name = os.path.join(output_dir, f"{block_name}.txt")
    with open(file_name, "w", encoding="utf-8") as file:
        for stock_code in stock_codes:
            file.write(stock_code + "\n")
    print(f"概念板块 [{block_name}] 个股已保存至 {file_name}")