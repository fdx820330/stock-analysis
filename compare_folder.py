import os
import shutil
from datetime import datetime

current_date = datetime.now().strftime('%Y%m%d')
OUTPUT_DIR_PRE = f"./result_pre"
os.makedirs(OUTPUT_DIR_PRE, exist_ok=True)
OUTPUT_DIR_NOW = f"./result_now"
os.makedirs(OUTPUT_DIR_NOW, exist_ok=True)
OUTPUT_DIR = f"./result_{current_date}"
os.makedirs(OUTPUT_DIR, exist_ok=True)




def compare_txt_files(file1_path, file2_path):
    """
    比较两个文本文件的内容，逐行比较
    :param file1_path: 第一个文件的路径
    :param file2_path: 第二个文件的路径
    :return: 不同的行信息
    """
    differences = []
    try:
        with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
            lines1 = file1.readlines()
            lines2 = file2.readlines()
            max_lines = max(len(lines1), len(lines2))
            for i in range(max_lines):
                line1 = lines1[i].strip() if i < len(lines1) else None
                line2 = lines2[i].strip() if i < len(lines2) else None
                if line1 != line2:
                    differences.append(f"Line {i + 1}: File1: {line1}, File2: {line2}")
    except FileNotFoundError:
        print("文件未找到，请检查文件路径。")
    return differences


def compare_directories(newest, pre, output_dir):
    """
    比较两个目录中同名 .txt 文件的内容，并将不同的文件复制到输出目录
    :param newest: 第一个目录的路径
    :param pre: 第二个目录的路径
    :param output_dir: 输出目录的路径
    """
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    clear_specific_files(OUTPUT_DIR,".txt")
    newest_files1 = [f for f in os.listdir(newest) if f.endswith('.txt')]
    pre_files2 = [f for f in os.listdir(pre) if f.endswith('.txt')]

    # 检查是否有一个文件夹为空
    """if not newest_files1 and pre_files2:
        print(f"目录 {newest} 为空，目录 {pre} 有 .txt 文件，判定为不同。")

        for file in pre_files2:
            file2_path = os.path.join(pre, file)
            shutil.copy2(file2_path, os.path.join(output_dir, file))
        return"""
    if newest_files1 and not pre_files2:
        print(f"目录 {pre} 为空，目录 {newest} 有 .txt 文件，判定为不同。")
        for file in newest_files1:
            file1_path = os.path.join(newest, file)
            shutil.copy2(file1_path, os.path.join(output_dir, file))
        return
    if not newest_files1 and not pre_files2:
        print("两个目录都没有 .txt 文件，判定为相同。")
        return

    common_files = set(newest_files1).intersection(set(pre_files2))

    # 找出只在 dir1 中的新增文件
    new_files_in_dir1 = set(newest_files1).difference(set(pre_files2))


    # 处理 dir1 中的新增文件
    for file in new_files_in_dir1:
        print(f"文件 {file} 是目录 {newest} 中的新增文件，判定为不同。")
        file1_path = os.path.join(newest, file)
        shutil.copy2(file1_path, os.path.join(output_dir, file))


    for file in common_files:
        file1_path = os.path.join(newest, file)
        file2_path = os.path.join(pre, file)
        differences = compare_txt_files(file1_path, file2_path)
        if differences:
            print(f"文件 {file} 存在差异:")
            for diff in differences:
                print(diff)
            # 复制不同的文件到输出目录
            shutil.copy2(file1_path, os.path.join(output_dir, file))
        else:
            print(f"文件 {file} 内容相同。")


def copy_directory(source_dir, destination_dir):
    clear_specific_files(destination_dir, ".txt")
    try:
        # 检查源目录是否存在
        if not os.path.exists(source_dir):
            print(f"源目录 {source_dir} 不存在。")
            return
        # 如果目标目录已存在，先删除它
        if os.path.exists(destination_dir):
            shutil.rmtree(destination_dir)
        # 递归复制源目录到目标目录
        shutil.copytree(source_dir, destination_dir)
        print(f"成功将目录 {source_dir} 的内容拷贝到 {destination_dir}。")
    except Exception as e:
        print(f"拷贝过程中出现错误: {e}")

def clear_specific_files(directory_path, file_extension):
    """
    清除指定目录下指定类型的文件
    :param directory_path: 要清除内容的目录路径
    :param file_extension: 要清除的文件扩展名，如 '.txt'
    """
    if not os.path.exists(directory_path):
        print(f"指定的目录 {directory_path} 不存在。")
        return
    try:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith(file_extension):
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
        print(f"目录 {directory_path} 下的 {file_extension} 文件已成功清除。")
    except Exception as e:
        print(f"清除目录 {directory_path} 下 {file_extension} 文件时出错: {e}")

if __name__ == "__main__":
    compare_directories(OUTPUT_DIR_NOW,OUTPUT_DIR_PRE,OUTPUT_DIR)
    copy_directory(OUTPUT_DIR_NOW, OUTPUT_DIR_PRE)
