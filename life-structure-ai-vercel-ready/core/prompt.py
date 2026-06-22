FORBIDDEN_REPLACEMENTS = {
    "一定会": "可能会",
    "必定会": "可能会",
    "必然会": "可能会",
    "肯定会": "可能会",
    "必将": "可能会",
    "注定": "呈现出",
    "必然": "较容易",
}


def build_report_messages(structure: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": (
                "你是一名人生结构分析报告助手。"
                "请基于用户给出的命格结构生成中文分析报告。"
                "报告必须使用结构、趋势、可能性表达，不允许使用预测性或绝对化语言，"
                "例如“一定会”“必然会”“注定”“肯定会”。"
                "内容应温和、理性、可参考，不要宣称确定未来。"
            ),
        },
        {
            "role": "user",
            "content": (
                f"命格结构：{structure}\n\n"
                "请生成一份“人生结构分析报告”，必须包含以下五个小标题：\n"
                "1. 性格分析\n"
                "2. 事业方向\n"
                "3. 情感模式\n"
                "4. 人生节奏\n"
                "5. 总结一句话\n\n"
                "请使用“可能”“倾向”“更容易”“适合关注”“有机会呈现”等表达。"
            ),
        },
    ]


def build_fallback_report(structure: str) -> str:
    return (
        f"人生结构分析报告：{structure}\n\n"
        "性格分析\n"
        "这个结构通常体现出较强的自我观察能力，可能更容易在变化中寻找自己的节奏，"
        "也适合通过复盘来提升判断力。\n\n"
        "事业方向\n"
        "事业发展上更适合关注长期积累、能力沉淀和阶段性突破，可能在清晰目标与稳定执行结合时呈现更好的状态。\n\n"
        "情感模式\n"
        "情感关系中可能更重视理解、尊重和安全感，适合在沟通中表达真实需求，同时保留彼此成长空间。\n\n"
        "人生节奏\n"
        "人生节奏可能呈现阶段性变化，适合用结构化计划承接变化，并在关键节点主动调整方向。\n\n"
        "总结一句话\n"
        "你的结构更适合在稳定积累中观察机会，并通过阶段性调整形成自己的成长路径。"
    )


def soften_predictive_language(text: str) -> str:
    result = text
    for forbidden, replacement in FORBIDDEN_REPLACEMENTS.items():
        result = result.replace(forbidden, replacement)
    return result
