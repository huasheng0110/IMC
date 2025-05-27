# app/models/disease_search.py

import re

DISEASE_DB = {
    "感冒": "感冒是一种常见的呼吸道疾病，主要症状包括咳嗽、流鼻涕和发热。常用药物有：对乙酰氨基酚、感冒灵、板蓝根、维C银翘片等。",
    "高血压": "高血压是一种常见的慢性疾病，需要控制饮食和服药。常用药物有：硝苯地平、厄贝沙坦、氨氯地平等。",
    "糖尿病": "糖尿病是一种代谢性疾病，患者需要控制血糖水平。常用药物有：二甲双胍、格列美脲、胰岛素等。",
    "咳嗽": "咳嗽可能由多种原因引起，常用药物有：止咳糖浆、氨溴索、右美沙芬等。",
    "发烧": "发烧是多种疾病的常见症状，常用药物有：对乙酰氨基酚、布洛芬等。",
    "头疼": "头疼常见于感冒、偏头痛等，常用药物有：对乙酰氨基酚、布洛芬等。",
    "胃痛": "胃痛可能与胃炎、胃溃疡等有关，常用药物有：奥美拉唑、雷尼替丁、铝碳酸镁等。"
}

def search_disease(user_input):
    # 尝试解析“年龄:xx, 性别:xx, 症状:xx”格式
    symptom = None
    match = re.search(r"症状[:：]\s*([^\s,，]+)", user_input)
    if match:
        symptom = match.group(1)
        # 尝试用症状关键词匹配疾病库
        for disease, desc in DISEASE_DB.items():
            if symptom in disease or disease in symptom:
                return f"根据您的症状“{symptom}”，建议：{desc}"
        return f"未找到与症状“{symptom}”相关的疾病信息，请咨询专业医生。"
    # 兼容原有的直接疾病关键词查询
    for disease, desc in DISEASE_DB.items():
        if disease in user_input:
            return f"{disease}: {desc}"
    # 针对“xxx吃什么药”类问题
    if "吃什么药" in user_input:
        for disease in DISEASE_DB:
            if disease in user_input:
                desc = DISEASE_DB[disease]
                if "常用药物有：" in desc:
                    return f"{disease}常用药物推荐：{desc.split('常用药物有：')[1]}"
    return "未找到相关疾病信息，请重新输入。"