# dialogue_manager.py

import re
from app.models.disease_search import search_disease
from app.models.medication_search import search_medication
from app.models.deepseek_api import ask_deepseek  # 假设这是调用 DeepSeek 的封装函数
from app.services.knowledge_base import get_local_knowledge  # 你刚写的本地知识库检索函数


class DialogueManager:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dialogue_state = {
            'intent': None,
            'symptoms': [],
            'duration': None,
            'additional': [],
            'need_more_info': True
        }
        self.dialogue_history = []

    def extract_info(self, user_input):
        duration_keywords = ['天', '小时', '周']
        additional_keywords = ['发烧', '恶心', '头晕', '流鼻涕', '咳嗽']

        # 简单规则匹配
        if any(kw in user_input for kw in duration_keywords):
            self.dialogue_state['duration'] = user_input
        for kw in additional_keywords:
            if kw in user_input and kw not in self.dialogue_state['additional']:
                self.dialogue_state['additional'].append(kw)
        # 症状收集（简化示例）
        if '头疼' in user_input or '感冒' in user_input:
            self.dialogue_state['symptoms'].append(user_input)

    def is_meaningless_input(self, user_input):
        # 过滤空字符串、纯空格
        if not user_input or not user_input.strip():
            return True
        # 过滤纯标点符号
        if re.fullmatch(r'[\W_]+', user_input.strip()):
            return True
        # 过滤少于3个字符且无中文无数字无字母的（避免无意义短字符）
        if len(user_input.strip()) < 3 and not re.search(r'[\u4e00-\u9fa5a-zA-Z0-9]', user_input):
            return True
        # 过滤类似“sss”、“aaa”等连续相同字符（长度3以上）
        if re.fullmatch(r'(.)\1{2,}', user_input.strip().lower()):
            return True
        # 过滤仅包含数字或无实际症状含义的短数字
        if user_input.strip().isdigit() and len(user_input.strip()) < 4:
            return True
        # 过滤常见无意义英文输入
        if user_input.strip().lower() in ['asdf', 'asdfgh', 'qwer', 'zxcv', 'test', '123', '1234', '111', '222']:
            return True
        return False

    def update(self, user_input, intent):
        self.dialogue_history.append({'user': user_input})
        self.dialogue_state['intent'] = intent
        self.extract_info(user_input)

        if self.is_meaningless_input(user_input):
            result = "抱歉，我没太理解您的输入，请尽量详细描述您的症状，例如“头疼三天，伴有发烧”。"
            self.dialogue_history.append({'bot': result})
            self.dialogue_state['need_more_info'] = True
            return result

        if intent == '问候':
            result = "您好！很高兴为您服务，请问有什么可以帮您？"
            self.dialogue_history.append({'bot': result})
            self.dialogue_state['need_more_info'] = True
            return result

        # 用药意图或包含“药”字，优先本地知识库 + DeepSeek补充
        if '药' in user_input or intent == '用药':
            local_know = get_local_knowledge(user_input)
            # 调用DeepSeek时，将本地知识拼接入上下文
            deepseek_context = f"{local_know}\n用户问题：{user_input}"
            deepseek_answer = ask_deepseek(deepseek_context)

            # 选用DeepSeek回答（失败则fallback本地知识）
            result = deepseek_answer if "医疗服务引擎暂时不可用" not in deepseek_answer else local_know

            self.dialogue_state['need_more_info'] = False
            self.dialogue_history.append({'bot': result})
            return result

        # 诊断意图：先本地搜索，信息不全时引导提问，信息足时调用DeepSeek补充
        if intent == '问诊':
            if self.dialogue_state['duration'] and self.dialogue_state['symptoms']:
                query = ' '.join(self.dialogue_state['symptoms'] + [self.dialogue_state['duration']] + self.dialogue_state['additional'])
                local_result = search_disease(query)

                # 调用DeepSeek补充答案
                deepseek_context = f"疾病信息：{local_result}\n用户问题：{user_input}"
                deepseek_answer = ask_deepseek(deepseek_context)

                result = deepseek_answer if "医疗服务引擎暂时不可用" not in deepseek_answer else local_result

                self.dialogue_history.append({'bot': result})
                self.dialogue_state['need_more_info'] = False
                return result
            else:
                self.dialogue_state['need_more_info'] = True
                result = "请问您的症状持续了多长时间？是否有发烧、恶心等伴随症状？"
                self.dialogue_history.append({'bot': result})
                return result

        # 其他情况：优先本地搜索，DeepSeek补充
        local_result = search_disease(user_input)
        deepseek_context = f"疾病信息：{local_result}\n用户问题：{user_input}"
        deepseek_answer = ask_deepseek(deepseek_context)

        result = deepseek_answer if "医疗服务引擎暂时不可用" not in deepseek_answer else local_result
        self.dialogue_history.append({'bot': result})
        return result

    def get_history(self):
        return self.dialogue_history
