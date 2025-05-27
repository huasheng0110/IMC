import json

with open('app/database/knowledge_base.json', encoding='utf-8') as f:
    kb = json.load(f)

def get_local_knowledge(query):
    for symptom, disease in kb.get('symptom_to_disease', {}).items():
        if symptom in query:
            return f"根据您的描述，可能的疾病为：{disease}"
    return "未找到相关疾病，请提供更多信息。"
