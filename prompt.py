EXAM_PROFILES = {
    "CET-4": {
        "name": "CET-4 Writing",
        "essay_scale": "Full score: 15. Use the CET holistic writing rubric. Focus on task response, completeness, organization, coherence, and language accuracy.",
        "translation_scale": "Full score: 15. Use the CET-4 translation standard. Focus on information completeness, grammar accuracy, natural expression, spelling, and punctuation.",
        "level_note": "Judge the answer at CET-4 level. Do not raise the standard to academic or professional writing.",
    },
    "CET-6": {
        "name": "CET-6 Writing",
        "essay_scale": "Full score: 15. Use the CET holistic writing rubric, with higher expectations for vocabulary precision, sentence complexity, and argument development than CET-4.",
        "translation_scale": "Full score: 15. Use the CET-6 translation standard. Focus on complex sentence handling, accurate cultural information transfer, and natural collocations.",
        "level_note": "Judge the answer at CET-6 level and point out whether the expression reaches mature college English.",
    },
    "TOEFL": {
        "name": "TOEFL Writing",
        "essay_scale": "Use TOEFL Writing expectations. Give an estimated 0-30 score and explain the closest 0-5 band performance.",
        "translation_scale": "TOEFL does not normally test translation. If translation is submitted, give a 0-30 reference score based on academic English transfer, accuracy, and naturalness.",
        "level_note": "Focus on idea development, logical progression, language control, and clarity of academic expression.",
    },
    "IELTS": {
        "name": "IELTS Writing",
        "essay_scale": "Use IELTS Writing criteria and give a 0-9 reference band: Task Response/Achievement, Coherence and Cohesion, Lexical Resource, and Grammar Range and Accuracy.",
        "translation_scale": "IELTS does not normally test translation. If translation is submitted, give a 0-9 reference band based on accuracy, coherence, vocabulary, and grammar.",
        "level_note": "Focus on task response, paragraph progression, lexical resource, and grammatical range.",
    },
    "GRE": {
        "name": "GRE Analytical Writing",
        "essay_scale": "Use GRE Analytical Writing expectations and give a 0-6 score. Focus on argument quality, critical analysis, organization, and language control.",
        "translation_scale": "GRE does not normally test translation. If translation is submitted, give a 0-6 reference score based on graduate-level English expression, accuracy, and clarity.",
        "level_note": "Focus on analytical depth, evidence quality, and precision of expression. Do not judge it as a CET template essay.",
    },
}

TASK_TYPES = {
    "essay": "Essay grading",
    "translation": "Translation grading",
}


def build_prompt(task_text, answer_text, knowledge, exam_type="CET-4", task_type="essay"):
    profile = EXAM_PROFILES.get(exam_type, EXAM_PROFILES["CET-4"])

    if task_type == "translation":
        return _build_translation_prompt(task_text, answer_text, knowledge, profile)
    return _build_essay_prompt(task_text, answer_text, knowledge, profile)


def _common_header(knowledge, profile):
    return f"""
You are a strict and professional English exam grader.

Grading principles:
- Point out real problems directly. Do not write empty encouragement.
- Follow the selected exam type. Do not mix rubrics from other exams.
- First judge whether the answer completes the task, then evaluate language quality.
- If the text appears to contain obvious OCR mistakes, mark them as "possible OCR error" and do not over-penalize them as real student errors.

Current exam: {profile["name"]}
Rubric note: {profile["level_note"]}

Reference knowledge base below may be used only to support expression advice. It must not override the current exam rubric:
{knowledge}
"""


def _build_essay_prompt(topic, essay, knowledge, profile):
    return f"""
{_common_header(knowledge, profile)}

[Essay grading rule]
{profile["essay_scale"]}

[Essay prompt]
{topic}

[Student essay]
{essay}

Please output in Chinese with the following structure:

一、总评判分
- 内容完成度：
- 结构与连贯：
- 语言准确度：
- 词汇与句式：
- 题意符合程度：
- 总分：

二、核心问题
列出 3-6 个最影响得分的问题，按重要程度排序。

三、逐句修改
选择最需要修改的句子。每条使用以下格式：
原句：
问题：
修改：

四、润色后的全文
保留学生原意，提升表达质量，不要改成与题目无关的模板文。

五、下次写作建议
给出 3 条具体、可执行的建议。

六、词汇与句型积累
这一部分必须使用 Markdown 格式输出，包含以下小标题和表格：

### 关键词汇
| 表达 | 词性 / 功能 | 中文含义 | 适用语境 | 例句 |
| --- | --- | --- | --- | --- |

### 高分短语
| 短语 | 中文含义 | 可替换表达 | 例句 |
| --- | --- | --- | --- |

### 高级句型
| 句型 | 用法 | 示例 |
| --- | --- | --- |

### 话题拓展
- 用 Markdown bullet list 给出 3-5 个可拓展观点或素材。"""


def _build_translation_prompt(source_text, translation, knowledge, profile):
    return f"""
{_common_header(knowledge, profile)}

[Translation grading rule]
{profile["translation_scale"]}

[Source text / prompt]
{source_text}

[Student translation]
{translation}

Please output in Chinese with the following structure:

一、总评判分
- 信息完整度：
- 准确性：
- 语法与句法：
- 用词与搭配：
- 自然度：
- 总分：

二、漏译、误译与硬译
列出主要问题，并说明为什么影响得分。

三、逐句修改
每条使用以下格式：
原文：
学生译文：
问题：
建议译文：

四、参考译文
给出一版自然、准确、符合当前考试水平的参考译文。

五、翻译提升建议
给出 3 条具体建议，优先针对中英结构差异、动词选择、从句和非谓语处理。

六、表达积累
这一部分必须使用 Markdown 格式输出，包含以下小标题和表格：

### 关键词汇
| 表达 | 词性 / 功能 | 中文含义 | 适用语境 | 例句 |
| --- | --- | --- | --- | --- |

### 翻译短语
| 中文表达 | 推荐译法 | 不推荐译法 | 说明 |
| --- | --- | --- | --- |

### 句式转换
| 中文结构 | 英文处理方式 | 示例 |
| --- | --- | --- |

### 易错提醒
- 用 Markdown bullet list 给出 3-5 条本题相关提醒。"""
