#导入qstock模块
import qstock as qs


if __name__ == "__main__":
	# 获取概念板块最新行情指标
	df = qs.realtime_data('概念板块')
	# 查看前几行
	df.head()