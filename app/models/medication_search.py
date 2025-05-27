# app/models/medication_search.py

def search_medication(user_input):
    """
    简单基于关键词的用药推荐函数
    """
    # 药物推荐字典
    medication_db = {
        '感冒': '您可以服用感冒药，如对乙酰氨基酚、布洛芬、连花清瘟等。',
        '发烧': '建议服用退烧药，如对乙酰氨基酚或布洛芬。',
        '头疼': '可服用止痛药，如布洛芬、对乙酰氨基酚。',
        '咳嗽': '推荐止咳药，如右美沙芬、氨溴索。',
        '流鼻涕': '建议服用抗过敏药，如氯雷他定、赛庚啶。',
        '喉咙痛': '可以含服含片，如六神丸、金嗓子喉片。',
        '鼻塞': '可以使用滴鼻液，如生理盐水、滴鼻净。'
    }

    # 匹配关键词
    for keyword, recommendation in medication_db.items():
        if keyword in user_input:
            return recommendation

    # 没有匹配到时的兜底回答
    return '请问您具体的症状是什么？我可以为您推荐合适的药物。'
