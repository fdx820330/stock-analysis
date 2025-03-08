import os
from pytdx.hq import TdxHq_API
from pytdx.exhq import TdxExHq_API


def get_block_stocks():
	api = TdxExHq_API()
	block_stocks = {}

	with api.connect('106.14.95.149', 7727):
		blocks = api.get_and_parse_block_info(1)  # 获取概念板块数据

		for block in blocks:
			block_name = block['blockname']
			stocks = block['stocks']
			block_stocks[block_name] = stocks

	return block_stocks


def save_to_files(block_stocks, output_dir):
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	for block_name, stocks in block_stocks.items():
		output_file = os.path.join(output_dir, f"{block_name}.txt")
		with open(output_file, 'w', encoding='utf-8') as f:
			f.write("\n".join(stocks))
		print(f"导出: {output_file}, {len(stocks)} 只股票")


if __name__ == "__main__":
	output_dir = "C:\\Users\\flash\\Documents\\myData\\stock\\tdx_block\\exported"
	block_stocks = get_block_stocks()
	save_to_files(block_stocks, output_dir)
