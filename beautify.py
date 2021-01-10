#! /usr/bin/env python3

import pandas as pd

def parse_que(que):
    return que

def parse_ans(ans):
    return ans

def parse_qa(qa_list):
    results = []
    # 遍历一个对话，将解析的对话列表作为一个字典，存入results
    for item in qa_list:
        piece = {}
        # 若某条对话是空字符或None则跳过
        if not item:
            continue
        # 表示提问者，这一条为问题
        if '***' in item:
            piece['desc'] = parse_que(item)
            piece['is_que'] = 1
        # 这一条为回答
        else:
            piece['desc'] = parse_ans(item)
            piece['is_que'] = 0
        # 将此条加入结果集
        results.append(piece)
    return results

def main():
    file_path = 'src/SampleData_NOC_2017.csv'
    # data = pd.read_csv(file_path)
    # content = data['Content']
    head = pd.read_csv(file_path).head(20)
    content = head['Content']
    delimiter = '【###】>'

    print(len(content))
    # for item in content:
    #     print(item)
    #     print()
    # print()
    print()

    for item in content:
        qa = item.split(delimiter)
        results = parse_qa(qa)

        # for res in results:
        #     print(res)
        for res in results:
            if res.get('is_que'):
                print('q:', res.get('desc'))
            else:
                print('a:', res.get('desc'))
        print()

if __name__ == '__main__':
    main()