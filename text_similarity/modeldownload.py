from modelscope import snapshot_download

# 根据下载下来的本地项目路径指定下载位置的目录路径，之后modelpath需要参考这个路径
download_location = r'\text_similarity\model_large'

# 使用 snapshot_download 函数下载模型到指定位置
model_dir = snapshot_download('iic/nlp_structbert_sentence-similarity_chinese-large', cache_dir=download_location)
