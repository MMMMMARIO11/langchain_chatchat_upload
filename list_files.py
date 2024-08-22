import requests

API_URL = 'http://192.168.1.117:7861/knowledge_base/list_files'

# 替换为实际的知识库名称
knowledge_base_name = '学习强国'

# 构建查询参数
params = {
    'knowledge_base_name': knowledge_base_name
}

try:
    response = requests.get(API_URL, params=params)

    # 检查响应状态码
    if response.status_code == 200:
        print("请求成功！")
        print(response.json())  # 打印响应数据
    else:
        print(f"请求失败，状态码：{response.status_code}")
        print(response.text)  # 打印响应内容

except requests.exceptions.RequestException as e:
    print(f"请求发生异常：{e}")
