
from pytdx.hq import TdxHq_API
from pytdx.exhq import TdxExHq_API
from pytdx.params import TDXParams
import os
from datetime import datetime
import json
import shutil
import pandas as pd
from pytdx.config.hosts import hq_hosts


# 配置文件存储目录
current_date = datetime.now().strftime('%Y%m%d')
OUTPUT_DIR_PRE = f"./result_pre"
os.makedirs(OUTPUT_DIR_PRE, exist_ok=True)
OUTPUT_DIR_NOW = f"./result_now"
os.makedirs(OUTPUT_DIR_NOW, exist_ok=True)
OUTPUT_DIR = f"./result_{current_date}"
os.makedirs(OUTPUT_DIR, exist_ok=True)



def load_config(config_path):
	with open(config_path, 'r', encoding='utf-8') as f:
		return json.load(f)


def get_concept_blocks(ip,port):
    """获取通达信概念板块列表"""
    api = TdxHq_API()
    with api.connect(ip, port):  # 连接行情服务器
        blocks = api.get_and_parse_block_info(TDXParams.BLOCK_GN)  # 获取板块数据
    return blocks

def get_stocks_in_block(block_name, blocks):
    """获取指定概念板块的个股"""
    for block in blocks:
        if block['blockname'] == block_name:
            return block['code']
    return []



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



server_ip = ""
server_port = ""
merged_data = {}



def get_data_from_remote():
    config = load_config("tdx_config.json")
    if config:
        server_ip = config.get('Server', {}).get('ip', '115.238.90.165')
        server_port = config.get('Server', {}).get('port', 7709)
    code = ""
    concept_blocks = get_concept_blocks(server_ip, server_port)
    if concept_blocks:
        print("概念板块列表:")
        for block in concept_blocks:
            # print(block['blockname']+"|"+block['code'])
            blockname = block['blockname']
            blockcode = block['code']

            if isinstance(blockcode, str):
                if blockcode.startswith(('600', '601', '603')):
                    code = f"SH{blockcode}"
                elif blockcode.startswith(('000', '001', '002', '003', '300', '301')):
                    code = f"SZ{blockcode}"
                elif blockcode.startswith(('43', '83', '87', '88')):
                    code = f"BJ{blockcode}"
            if blockname not in merged_data:
                merged_data[blockname] = []
            if code not in merged_data[blockname]:
                merged_data[blockname].append(code)
            # stocks = get_stocks_in_block(block['blockname'], concept_blocks)
            # print("code ="+stocks)

        for block_name, stock_codes in merged_data.items():
            filename = os.path.join(OUTPUT_DIR_NOW, f"{block_name}.txt")
            with open(filename, "w", encoding="utf-8") as file:
                for stock_code in stock_codes:
                    file.write(stock_code + "\n")
            print(f"概念板块 [{block_name}] 个股已保存至 {filename}")
        # 如果比较的结果是两个目录的内容一样
        compare_directories(OUTPUT_DIR_NOW, OUTPUT_DIR_PRE, OUTPUT_DIR)
        copy_directory(OUTPUT_DIR_NOW, OUTPUT_DIR_PRE)


    else:
        print("未能获取概念板块信息")


def get_block_data(concept_block_name):
    config = load_config("tdx_config.json")
    if config:
        server_ip = config.get('Server', {}).get('ip', '115.238.90.165')
        server_port = config.get('Server', {}).get('port', 7709)
    block_df = get_concept_blocks(server_ip, server_port)
    #print(block_df)
    #concept_block = next((block for block in block_df if block['blockname'] == concept_block_name), None)
    concept_block = [block for block in block_df if concept_block_name in block['blockname']]
    print(concept_block)
    api = TdxHq_API()
    try:
        if api.connect(server_ip, server_port):
            if concept_block:
                all_k_data = []
                # 遍历板块内的成分股
                for block in concept_block:

                    stock_code = block['code']
                    #print(stock_code)
                    market = 0 if stock_code.startswith(('0', '3')) else 1
                    # 获取 5 分钟 K 线数据，这里获取最新的 1 根 K 线
                    k_data = api.get_security_bars(4, market, stock_code, 0, 1)
                    if k_data:
                        df = pd.DataFrame(k_data)
                        df['stock_code'] = stock_code
                        all_k_data.append(df)
                if all_k_data:
                    combined_df = pd.concat(all_k_data, ignore_index=True)
                    # 格式化日期时间
                    combined_df['datetime'] = pd.to_datetime(
                        combined_df['year'] * 100000000 + combined_df['month'] * 1000000 + combined_df['day'] * 10000 +
                        combined_df['hour'] * 100 + combined_df['minute'], format='%Y%m%d%H%M')
                    # 计算板块行情
                    # 1. 计算加权平均价格（以成交量为权重）
                    combined_df['weighted_open'] = combined_df['open'] * combined_df['vol']
                    combined_df['weighted_close'] = combined_df['close'] * combined_df['vol']

                    total_vol = combined_df['vol'].sum()
                    open_price = combined_df['weighted_open'].sum() / total_vol
                    close_price = combined_df['weighted_close'].sum() / total_vol

                    # 2. 计算最高价和最低价
                    high_price = combined_df['high'].max()
                    low_price = combined_df['low'].min()

                    # 3. 计算总成交量和总成交额
                    total_amount = combined_df['amount'].sum()
                    total_vol = combined_df['vol'].sum()

                    # 4. 计算振幅、涨跌和涨幅
                    amplitude = ((high_price - low_price) / open_price) * 100
                    change = close_price - open_price
                    change_percent = (change / open_price) * 100

                    # 5. 获取最新时间
                    latest_datetime = combined_df['datetime'].max()

                    # 返回板块行情数据
                    result_df = pd.DataFrame({
                        'block_name': [concept_block_name],
                        'datetime': [latest_datetime],
                        '开盘': [open_price],
                        '最高': [high_price],
                        '最低': [low_price],
                        '收盘': [close_price],
                        '总量': [total_vol],
                        '总额': [total_amount],
                        '振幅': [amplitude],
                        '涨跌': [change],
                        '涨幅': [change_percent]
                    })
                    return result_df
                else:
                    print("未获取到该概念板块内任何股票的 5 分钟行情数据。")
            else:
                print(f"未找到名为 {concept_block_name} 的概念板块。")
        else:
            print("无法连接到行情服务器。")
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
       # 断开连接
       api.disconnect()




if __name__ == "__main__":
    #get_data_from_remote()
    concept_block_name = "DeepSeek";
    quotes = get_block_data(concept_block_name)
    print(pd.DataFrame(quotes).to_csv())
    if quotes is not None:
        # 输出到 CSV 文件
        csv_file_name = f"{concept_block_name}_5min_quotes.csv"
        quotes.to_csv(csv_file_name, index=False)
        print(f"数据已成功保存到 {csv_file_name} 文件中。")
    else:
        print("未获取到有效数据，无法保存到文件。")
