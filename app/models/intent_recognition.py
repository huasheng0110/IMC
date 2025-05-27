import joblib

vectorizer = joblib.load('app/models/vectorizer.pkl')
clf = joblib.load('app/models/intent_model.pkl')

# 简化后的预测函数（规则优先，模型辅助）
def predict_intent(user_input):
    # 规则优先
    if any(kw in user_input for kw in ['你好', '您好', '哈喽', '嗨', '早上好', '晚上好']):
        return '问候'
    if any(kw in user_input for kw in ['挂号', '预约']):
        return '挂号'
    if any(kw in user_input for kw in ['头疼', '感冒', '发烧', '恶心', '疼', '咳嗽']):
        return '问诊'
    if any(kw in user_input for kw in ['药', '吃什么', '买药']):
        return '用药'

    # 模型预测
    X_input = vectorizer.transform([user_input])
    pred = clf.predict(X_input)[0]
    return pred