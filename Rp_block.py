import os
import json
from datetime import datetime


def load_config(config_path):
	with open(config_path, 'r', encoding='utf-8') as f:
		return json.load(f)


def replace_first_digit(line, mapping):
	for key, value in mapping.items():
		if line.startswith(key):
			return line.replace(key, value, 1)
	return line


def process_files(input_dir, output_dir, mapping, log_file):
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	updated_files = []

	for file_name in os.listdir(input_dir):
		input_path = os.path.join(input_dir, file_name)
		output_path = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.txt")

		if os.path.isfile(input_path):
			with open(input_path, 'r', encoding='utf-8') as f:
				original_lines = f.readlines()

			updated_lines = [replace_first_digit(line, mapping) for line in original_lines]

			if updated_lines != original_lines:
				updated_files.append(file_name)
				with open(output_path, 'w', encoding='utf-8') as f:
					f.writelines(updated_lines)
				print(f"✅ 更新文件: {output_path}")
			else:
				print(f"⚠️ 无变化: {file_name}")

	log_message = f"\n执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
	log_message += "更新的文件:\n" + ("\n".join(updated_files) if updated_files else "无文件更新") + "\n"

	# 追加写入日志文件
	with open(log_file, 'a', encoding='utf-8') as log:
		log.write(log_message)

	print("\n📄 处理结果已记录到:", log_file)


if __name__ == "__main__":
	config_path = "config.json"
	log_file = "update_log.txt"
	config = load_config(config_path)
	process_files(config["input_dir"], config["output_dir"], config["mapping"], log_file)
