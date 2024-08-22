from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import pymongo


def compute_similarity(text1, text2, model_path):  #比较两个text的文本相似度，返回similarity_score
    model = pipeline(Tasks.sentence_similarity, model=model_path)
    input_texts = (text1, text2)
    scores = model(input_texts)
    similarity_score=scores['scores'][0]
    return similarity_score
def connect_to_mongodb(database_name, collection_name):  #连接远程Mongodb数据库
    client = pymongo.MongoClient('mongodb://localhost:27017/')  #Mongodb数据库地址
    db = client[database_name]
    collection = db[collection_name]
    return collection

def get_existing_texts(collection):  #返回对应collection中的所有文章内容
    existing_texts = []
    cursor = collection.find({}, {'text': 1})  # 获取所有文章的text字段内容
    for doc in cursor:
        existing_texts.append(doc['text'])
    return existing_texts


def main():
    # 连接到MongoDB
    database_name = 'news_database'
    collection_name = 'news_collection'
    collection = connect_to_mongodb(database_name, collection_name)

    # 获取已有的文章内容
    existing_texts = get_existing_texts(collection)

    # 假设新文章的内容存储在变量 new_article_text 中
    new_article_text = "新文章的内容..."
    # 设置为模型所在位置
    model_path = ''


    # 设置相似度阈值
    similarity_threshold = 0.75 #当两篇文章相似度大于0.75时判断为相似，不写入数据库，可以自行调整

    # 计算新文章与已有文章的相似度
    for existing_text in existing_texts:
        similarity_score = compute_similarity(existing_text, new_article_text, model_path)  #将新文章内容与数据库中已有文章一一比较相似度
        if similarity_score >= similarity_threshold:
            print(f"新文章与已有文章相似度为 {similarity_score:.2f}，不写入数据库。")  #当相似度大于0.75时，判断为相似，不写入数据库
            break
    else:
        # 如果没有相似文章，则将新文章写入数据库
        print("新文章与已有文章相似度低，写入数据库。")
        collection.insert_one({'text': new_article_text})


if __name__ == '__main__':
    main()
