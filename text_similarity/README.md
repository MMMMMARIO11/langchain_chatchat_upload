# 文本相似度比较

本项目参考 ModelScope 平台上的开源项目 StructBERT 文本相似度模型的 Python 示例实现，主要目的是实现将新爬取的文章内容和mongodb数据库已有文本进行相似度比对，并决定是否录入。

## 简介

StructBERT 中文文本相似度模型是在structbert-large-chinese预训练模型的基础上训练出来的相似度匹配模型。本项目提供了下载预训练模型、测试模型有效性和使用主程序文件的示例。

## 安装依赖

使用 Python 环境为 3.12.4 版本，所安装依赖库已在 requirements.txt 列出

特别注意：modelscope所需环境需要引入 ModelScope Library 

```bash
pip install modelscope
```
最好在虚拟环境中安装modelscope库，避免影响本地编译器环境，比如通过pycharm新建项目中的虚拟环境

运行过程可能提示缺少某一个库而报错，按照报错提示通过 pip install 指令逐一安装对应的库即可

## 下载预训练模型

使用 modeldownload.py 文件可以将开源项目中预训练好的 StructBERT 模型下载到本地，并保存在 model_large 文件夹中。确保在下载之前已经准备好存储模型的路径和目录。
```bash
download_location = r'text_similarity\model_large'
model_dir = snapshot_download('iic/nlp_structbert_sentence-similarity_chinese-large', cache_dir=download_location)
```
## 测试模型有效性
使用 model_large.py 文件可以测试下载的模型的有效性。该文件包含了对模型进行简单测试的示例。
```bash
semantic_cls = pipeline(Tasks.sentence_similarity, model=r'\text_similarity\model_large\iic\nlp_structbert_sentence-similarity_chinese-large')
input=('英雄联盟什么英雄最好', '英雄联盟最好英雄是什么')
semantic_cls(input)
print(semantic_cls(input))
```
## 主程序文件
main.py 包含了整个项目的主程序逻辑。各个函数的功能已在代码中有详细注释。

## 参考链接
模型信息和训练数据来源：StructBERT 文本相似度模型 - 中文 - 通用 - Large
ModelScope 平台：https://modelscope.cn/models/iic/nlp_structbert_sentence-similarity_chinese-large




