import os
import json


def process_files(input_dir, output_dir):
	# 加载输入配置文件
	input_config = json.load(open("input_config.json", "r"))
	# 加载输出配置文件
	output_config = json.load(open("output_config.json", "r"))

	# 生成输入和输出的文件名列表
	input_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir)]
	output_base_names = {os.path.basename(file) for file in os.listdir(output_dir)}

	# 根据配置文件中的映射规则，调整输出文件名
	desired_output_names = set()
	with open(input_config['file_mapping'], 'r') as f:
		mapping = eval(f.read())
	for key, value in mapping.items():
		if isinstance(value, str):
			desired_output_names.update([f"{key}-{value}.txt"])

	output_files = [os.path.join(output_dir, name) for name in desired_output_names]

	# 比较输入和输出文件数量
	input_basename_set = {os.path.basename(file) for file in input_files}
	output_basename_set = {os.path.basename(file) for file in output_files}

	if len(input_files) != len(output_files):
		missing_output_files = input_basename_set - output_basename_set

		# 根据配置，是否继续处理可能有修改的情况
		continue_processing = input("是否继续处理可能的修改？(y/N): ").strip().lower()
		if not (continue_processing == 'y' or continue_processing == 'yes'):
			print("🛑 处理取消。")
			return []

	# 定义日志信息
	log_message_start = f"操作: 输入文件数：{len(input_files)}, 输出文件数：{len(output_files)}"

	updated_files = []

	for file_name in os.listdir(input_dir):
		input_path = os.path.join(input_dir, file_name)
		if not os.path.isfile(input_path) or file_name.endswith('.txt'):
			continue

		# 根据映射规则，确定目标文件名
		target_file = None
		with open(input_config['file_mapping'], 'r') as f:
			mapping_dict = eval(f.read())
		for key, value in mapping_dict.items():
			if isinstance(value, str):
				if f"{key}-{value}.txt" == file_name:
					target_file = os.path.join(output_dir, f"{key}-{value}.txt")
					break

		if not target_file:
			continue  # 没有对应的输出文件，跳过

		try:
			with open(input_path, 'r', encoding='utf-8') as f:
				content = f.read()

			# 这里可以添加内容转换逻辑
			new_content = content  # 示例：不进行任何转换

			with open(target_file, 'w', encoding='utf-8') as f:
				f.write(new_content)

		except Exception as e:
			print(f"错误处理文件：{file_name}. 错误信息：{str(e)}")

	# 输出日志
	log_message = f"{log_message_start} - 成功处理所有文件转换。"
	print(log_message)

	return updated_files