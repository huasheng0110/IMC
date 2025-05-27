import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

# 示例数据集（补充了问候、症状、用药、挂号相关语料）
corpus = [
    # 问候相关
    "你好", "您好", "哈喽", "嗨", "早上好", "晚上好", "在吗", "请问在吗",

    # 挂号相关
    "挂号", "我想挂号", "我要预约挂号", "我想看医生", "怎么预约挂号", "帮我挂个号", "挂号流程是什么",
    "如何挂号", "挂号需要什么证件", "挂号窗口在哪里", "挂号收费吗", "挂号要排队吗", "挂号时间是几点",
    "挂号怎么操作", "我要预约医生", "预约挂号", "怎么预约专家号",

    # 问诊相关
    "头疼怎么办", "头疼是什么原因", "头疼要紧吗", "我感冒了", "感冒怎么处理", "胃痛怎么办", "肚子疼怎么缓解",
    "感冒了需要看医生吗", "高血压怎么治疗", "糖尿病要注意什么", "失眠怎么调理", "小孩发烧怎么办", "咽喉痛吃什么药",
    "皮肤过敏怎么办", "牙疼怎么处理", "我头疼", "我发烧了怎么办", "流鼻涕怎么办", "小孩咳嗽需要去医院吗", "咳嗽可以自己好吗",

    # 用药相关
    "发烧吃什么药", "我要买布洛芬", "咳嗽吃什么", "我要买退烧药", "我要买感冒药", "我要买止咳药", "我要买降压药",
    "我要买胰岛素", "我要买阿莫西林", "我要买维生素C", "哪里可以买药", "买药需要处方吗",
]

labels = [
    # 问候
    *["问候"] * 8,

    # 挂号
    *["挂号"] * 17,

    # 问诊
    *["问诊"] * 20,

    # 用药
    *["用药"] * 12,
]

# 加载或训练 vectorizer
vectorizer_path = 'app/models/vectorizer.pkl'
if os.path.exists(vectorizer_path):
    vectorizer = joblib.load(vectorizer_path)
    print("已加载 vectorizer.pkl")
else:
    print("未找到 vectorizer.pkl，重新训练...")
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    vectorizer.fit(corpus)
    os.makedirs('app/models', exist_ok=True)
    joblib.dump(vectorizer, vectorizer_path)
    print("已保存 vectorizer.pkl")

X = vectorizer.transform(corpus)

# 训练意图分类模型
clf = LinearSVC()
clf.fit(X, labels)

# 保存模型
model_path = 'app/models/intent_model.pkl'
joblib.dump(clf, model_path)
print(f"意图识别模型已保存到 {model_path}")


