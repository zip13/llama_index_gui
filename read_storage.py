import json

# 打开你的文件
with open('./storage/docstore.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 现在 'data' 是一个Python字典，它包含了你的JSON文件中的数据
# 可以打印出来查看
print('output:')
# 将Python字典进行格式化
formatted_data = json.dumps(data, indent=4, ensure_ascii=False)

# 输出格式化后的数据
print(formatted_data)
