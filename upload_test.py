from datetime import datetime
import pymongo
import requests
import json


# API 服务器地址和接口路径
API_URL = 'http://192.168.1.99:7861/knowledge_base/upload_docs'
# 'http://192.168.1.117:7861/docs#/Knowledge%20Base%20Management/upload_docs_knowledge_base_upload_docs_post'


def upload_file_to_api(file_path, knowledge_base_name):
    #   上传文件到 API
    with open(file_path, 'rb') as f:
        files = {
            'files': ('test_output_5.txt', f)
        }
        data = {
            'knowledge_base_name': knowledge_base_name,
            'override': False,  # 根据需求设置是否覆盖已有文件
            'to_vector_store': True,  # 进行向量化
            'chunk_size': 750,
            'chunk_overlap': 150,
            'zh_title_enhance': False,
            'docs': '',
            'not_refresh_vs_cache': False

        }

        response = requests.post(API_URL, files=files, data=data)

        # 打印响应结果
        print(response.status_code)
        print(response.json())


if __name__ == '__main__':
    #   设置上传json列表数量
    knowledge_base_name_actual = 'xxqg'  # 替换为实际的知识库名称
    file_path = 'test.txt'
    upload_file_to_api(file_path, knowledge_base_name_actual)


