import re
from abc import ABC, abstractmethod

class AbsUtils(ABC):
    @abstractmethod
    def match_chinese_characters(text):
        text_re = re.sub(r'\(.*?\)','',text)
        text_re = re.sub(r'\（.*?\）','',text_re)
        pattern = re.compile(r'[\u4e00-\u9fa5]{3,}')
        result = pattern.findall(text_re)
        res_list = []
        res_list.append(text)
        res_list.extend(result)
        
        print(res_list)
        return res_list

if __name__ == '__main__':
    content_text = """维生素C针
4+7@2.25注射用哌拉西林钠他唑巴坦钠
注射用甲泼尼龙琥珀酸钠
4+7⑤(华夏)左氧氟沙星氯化钠注射液
艾司唑仑片
4+7⑦ (奈特)硝苯地平控释片
4+7@帕立骨化醇注射液
4+7(瑞夫恩)恩替卡韦分散片
(星新忆)注射用吡拉西坦
"""
    cont_list = content_text.splitlines()
    # print(cont_list)
    result = map(AbsUtils.match_chinese_characters,cont_list)
    res_list = list(result)
    print("处理完的结果:",res_list)