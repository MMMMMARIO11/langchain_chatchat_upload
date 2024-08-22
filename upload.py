from datetime import datetime
import pymongo
import requests
import json
import pymysql

# MongoDB 连接信息
MONGO_URI = 'mongodb://192.168.1.148:27017/'
MONGO_DATABASE = 'xxqg'

# API 服务器地址和接口路径
API_URL = 'http://192.168.1.99:7861/knowledge_base/upload_docs'
# 'http://192.168.1.117:7861/docs#/Knowledge%20Base%20Management/upload_docs_knowledge_base_upload_docs_post'

# 连接 MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DATABASE]

# mysql数据库配置
mysql_host = '192.168.1.148'
mysql_port = 3306
mysql_user = 'root'
mysql_password = 'Fengjiaqi1'
mysql_database = 'rag_data'

# 连接到MySQL数据库
connection = pymysql.connect(
    host=mysql_host,
    port=mysql_port,
    user=mysql_user,
    password=mysql_password,
    database=mysql_database,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

def export_collection_to_json(collection_name, output_file ,json_nums):
    #  给数据库中的每个文档添加标签和时间戳，并导出为 JSON 文件

    for i in range(1, json_nums + 1):
        collection_name_index = f"{collection_name}_{i}"
        collection = db[collection_name_index]

        with connection.cursor() as cursor:
            #  查询 '上一次json_{i}列表总项数' 列的数据
            jsonlist_index = f"json_{i}列表更新项数"
            sql_select_articles_to_scrape = f"SELECT `{jsonlist_index}` FROM jsonlist_count"
            cursor.execute(sql_select_articles_to_scrape)

            # 获取查询结果
            result = cursor.fetchone()
            articles_to_scrape = int(result[jsonlist_index])
            #   选取更新的文章
            print(f"json_{i}列表更新项数: {articles_to_scrape}")

            if articles_to_scrape > 0:
                documents = collection.find().sort([('_id', -1)]).limit(articles_to_scrape)

                # 更新导出的文档
                for document in documents:
                    # 添加 'exported' 标签和时间戳字段
                    update_result = collection.update_one(
                        {'_id': document['_id']},
                        {
                            '$set': {
                                'exported': True,
                                'export_timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                            }
                        }
                    )

                    if update_result.modified_count > 0:
                        print(f"Document with _id {document['_id']} updated successfully.")
                    else:
                        print(f"Failed to update document with _id {document['_id']}.")

                # 导出集合数据为 JSON 文件

                documents = collection.find().sort([('_id', -1)]).limit(articles_to_scrape)
                with open(output_file, 'a', encoding='utf-8') as f:
                    for document in documents:
                        # 删除原始数据库中的额外字段
                        del document['_id']
                        del document['exported']
                        del document['export_timestamp']

                        # 将文档转换为 JSON 字符串并写入文件
                        json.dump(document, f, ensure_ascii=False)
                        f.write('\n')

def upload_file_to_api(file_path, knowledge_base_name, json_nums):
    # 上传文件到 API
    today = datetime.now().strftime("%Y%m%d")
    #  文件名加上日期
    with open(file_path, 'rb') as f:
        files = {
            'files': (f'xxqg_update_{today}.json', f)
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

        if response.status_code == 200:
            with connection.cursor() as cursor:
                # 准备插入的数据
                spider_status = '导入成功'
                crawl_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

                # 插入数据的 SQL 语句
                sql_insert_log = "INSERT INTO kb_log (`导入langchain_chatchat知识库状态`, `导入知识库时间`) VALUES (%s, %s)"
                cursor.execute(sql_insert_log, (spider_status, crawl_time))
                # 导入成功后更新列表项数为0，直到下一次爬取再更新需要爬取的文章数量

                for i in range(1, json_nums + 1):
                    jsonlist_index = f"json_{i}列表更新项数"
                    sql_update_articles_to_scrape = f"UPDATE jsonlist_count SET `{jsonlist_index}` = '0'"
                    cursor.execute(sql_update_articles_to_scrape)

                # 提交数据库事务
            connection.commit()
            connection.close()  # 关闭数据库连接
        else:
            with connection.cursor() as cursor:
                # 准备插入的数据
                spider_status = '导入失败'
                crawl_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

                # 插入数据的 SQL 语句
                sql_insert_log = "INSERT INTO kb_log (`导入langchain_chatchat知识库状态`, `导入知识库时间`) VALUES (%s, %s)"
                cursor.execute(sql_insert_log, (spider_status, crawl_time))

                # 提交数据库事务
            connection.commit()
            connection.close()  # 关闭数据库连接




if __name__ == '__main__':
    json_nums = 4
    #  定义所需栏目json链接数量
    collection_name = 'xxqg'
    today = datetime.now().strftime("%Y%m%d")
    f'xxqg_output_update{today}.json'
    output_file = f'xxqg_output_update{today}.json'
    knowledge_base_name = 'xxqg'  # 替换为实际的知识库名称

    # 导出集合数据为 JSON 文件
    export_collection_to_json(collection_name, output_file, json_nums)

    # 上传 JSON 文件到知识库
    upload_file_to_api(output_file, knowledge_base_name, json_nums)
