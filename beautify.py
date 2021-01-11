import pandas as pd
import re


def parse_nothing(text):
    return text

def parse_que(que):
    results = {}
    # 统一分隔符避免分割错误
    que = que.replace(':', '：')
    # 所有的键
    keys = ['状态', '咨询标题', '疾病', '时长', '怀孕情况', '过敏史', '病情描述', '希望提供的帮助',
            '所就诊医院科室', '治疗情况', '医院科室', '好大夫在线友情提示',
            '如何上传', '治疗过程', '用药情况', '药物名称', '服用说明', '既往病史', '检查资料']
    for k in keys:
        temp = k+'：'
        # 若此键在问题中，则将其作为分隔符分成两部分
        # 取第二部分，再用'：'分开，取第一部分
        # 再将目标后部分的键去掉
        # 如:
        #   状态：就诊前2017-01-15咨询标题：咨询标题：需要手术吗疾病
        # 分割后为:
        #   就诊前2017-04-11咨询标题
        if temp in que:
            # 分割两次，先后取第二、第一部分
            nearly_target = que.split(temp)[1].split('：')[0]

            target = nearly_target
            for m in keys:
                # 去掉后部分的键
                ptn = re.compile(r'(.*)(%s$)' % m)
                res = re.search(ptn, target)
                # 若键存在，取group 1
                if res:
                    target = res.group(1)
                    break
            # 过滤无用键值
            if k not in ['好大夫在线友情提示', '如何上传']:
                results[k] = target

    # 分离时间
    ptn = re.compile(r'(.*?)(\d{4}-\d{2}-\d{2})(.*)')
    text = results.get('状态')
    results['状态'] = re.search(ptn, text).group(1)
    results['时间'] = re.search(ptn, text).group(2)
    # 若是追问，分离追问内容
    temp = re.search(ptn, text).group(3)
    if temp:
        results['内容'] = temp
    return results

def parse_ans(ans):
    results={}
    key=['医师','内容']
    tempstr=ans.split('大夫',1)[0]
    results[key[0]]=tempstr
    ans=ans.split('医师')
    if len(ans)==1:
        ans=['0','没回复大夫']
        tempstr='大夫'
    if '问题由' in ans[1]:
        tempstr='问题由'
    results[key[1]]=ans[1].split(tempstr)[0]
    if results['内容']=='没回复':
        results['医师']='机器人'
    return results

def parse_qa(qa_list):
    results = []
    # 遍历一个对话，将解析的对话列表作为一个字典，存入results
    for i, item in enumerate(qa_list):
        piece = {}
        # 若某条对话是空字符或None则跳过
        if not item:
            continue
        # 表示提问者，这一条为问题
        if '***' in item:
            piece['is_que'] = 1
            # piece['desc'] = parse_nothing(item)
            piece['desc'] = parse_que(item)
        # 这一条为回答
        else:
            piece['is_que'] = 0
            piece['desc'] = parse_ans(item)
        # 将此条加入结果集
        results.append(piece)
    return results

def main():
    file_path = 'src/SampleData_NOC_2017.csv'
    # data = pd.read_csv(file_path)
    # content = data['Content']
    head = pd.read_csv(file_path,encoding='gb18030').head(400)
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

        for res in results:
            # if res.get('is_que'):
            #     print(res.get('desc'))
            print(res)
        print()

if __name__ == '__main__':
    main()