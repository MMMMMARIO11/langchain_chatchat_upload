from datetime import datetime
import pymongo
import requests
import json

# MongoDB 连接信息
MONGO_URI = 'mongodb://192.168.1.148:27017/'
MONGO_DATABASE = 'xxqg'

# API 服务器地址和接口路径
API_URL = 'http://192.168.1.99:7861/knowledge_base/upload_docs'
# 'http://192.168.1.117:7861/docs#/Knowledge%20Base%20Management/upload_docs_knowledge_base_upload_docs_post'

# 连接 MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DATABASE]


def export_collection_to_json(collection_name, json_nums):
    # 给数据库中的每个文档添加标签和时间戳，并导出为 JSON 文件
    for i in range(1, json_nums + 1):
        collection_name_index = f"{collection_name}_{i}"
        collection = db[collection_name_index]

        cursor = collection.find()  # 查找所有数据

        # 更新每个文档
        for document in cursor:
            # 添加 'exported' 标签和时间戳字段
            update_result = collection.update_one(
                {'_id': document['_id']},
                {
                    '$set': {
                        'exported': True,
                        'export_timestamp': datetime.now().isoformat()
                    }
                }
            )
            if update_result.modified_count > 0:
                print(f"Document with _id {document['_id']} updated successfully.")
            else:
                print(f"Failed to update document with _id {document['_id']}.")

        # 导出集合数据为 JSON 文件
        cursor = collection.find()
        output_file = f"xxqg_output_{i}.json"
        with open(output_file, 'a', encoding='utf-8') as f:
            for document in cursor:
                # 删除原始数据库中的额外字段
                del document['_id']
                del document['exported']
                del document['export_timestamp']

                # 将文档转换为 JSON 字符串并写入文件
                json.dump(document, f, ensure_ascii=False)
                f.write('\n')


def upload_file_to_api(file_path, knowledge_base_name, index):
    #   上传文件到 API
    with open(file_path, 'rb') as f:
        files_name = f"init_output_{index}.json"
        files = {
            'files': (files_name, f)
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
    json_nums = 4
    collection_name_actual = 'xxqg'  # 替换为实际的集合名称
    knowledge_base_name_actual = 'xxqg'  # 替换为实际的知识库名称

    # 导出集合数据为 JSON 文件
    export_collection_to_json(collection_name_actual, json_nums)
    # 上传 JSON 文件到知识库
    for i in range(1, json_nums + 1):
        file_path = f"xxqg_output_{i}.json"
        upload_file_to_api(file_path, knowledge_base_name_actual, i)


