from datetime import datetime


STRUCTURE_TYPES = {
    "early": {
        "name": "早发型结构",
        "summary": "早期人生变化明显，20-30岁容易出现方向转折。",
    },
    "stable": {
        "name": "稳定积累型",
        "summary": "人生节奏相对平稳，成果更容易延迟出现。",
    },
    "late": {
        "name": "后发型结构",
        "summary": "前期容易混沌，30岁后方向感逐渐清晰。",
    },
    "wave": {
        "name": "波动成长型",
        "summary": "人生阶段起伏明显，容易经历多次方向变化。",
    },
}


STAGE_MODEL = [
    {
        "range": "0-20",
        "name": "形成期",
        "theme": "环境影响",
        "description": "这一阶段更容易形成安全感、表达方式和对外界评价的感受底色。",
    },
    {
        "range": "20-35",
        "name": "选择期",
        "theme": "关键决策",
        "description": "这一阶段更容易遇到事业方向、关系取舍、城市变化和身份转换。",
    },
    {
        "range": "35+",
        "name": "定型期",
        "theme": "结果显现",
        "description": "这一阶段更适合把过去经验整理成稳定影响力，逐渐确认长期适合自己的路径。",
    },
]


def classify_structure(birth_time: str) -> str:
    try:
        return str(build_life_structure_model(birth_time).get("structure_type", "未知结构"))
    except ValueError:
        return "未知结构"


def build_life_structure_model(
    birth_time: str,
    gender: str = "",
    current_year: int | None = None,
) -> dict[str, object]:
    birth_dt = _parse_birth_time(birth_time)
    year_feature = birth_dt.year % 4
    hour_feature = _hour_feature(birth_dt.hour)
    minute_feature = birth_dt.minute // 15
    rhythm_index = (year_feature + hour_feature["weight"] + minute_feature + birth_dt.month) % 4
    structure_key = ["early", "stable", "late", "wave"][rhythm_index]
    structure = STRUCTURE_TYPES[structure_key]

    age = (current_year or datetime.now().year) - birth_dt.year
    current_stage = _current_stage(age)
    behavior_tendency = _behavior_tendency(structure_key, hour_feature["name"], gender)

    return {
        "structure_type": structure["name"],
        "structure_summary": structure["summary"],
        "stage_model": STAGE_MODEL,
        "current_stage": current_stage,
        "behavior_tendency": behavior_tendency,
        "rhythm_tags": _rhythm_tags(structure_key, hour_feature["name"], minute_feature),
        "time_features": {
            "birth_year": str(birth_dt.year),
            "time_segment": hour_feature["name"],
            "minute_rhythm": _minute_rhythm(minute_feature),
        },
    }


def _parse_birth_time(birth_time: str) -> datetime:
    value = birth_time.strip()
    for pattern in ("%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M", "%Y-%m-%d"):
        try:
            parsed = datetime.strptime(value, pattern)
            if parsed.year < 1900 or parsed.year > datetime.now().year:
                raise ValueError("birth year out of range")
            return parsed
        except ValueError:
            continue
    raise ValueError("invalid birth time")


def _hour_feature(hour: int) -> dict[str, object]:
    if 5 <= hour <= 10:
        return {"name": "启动时段", "weight": 0}
    if 11 <= hour <= 16:
        return {"name": "承接时段", "weight": 1}
    if 17 <= hour <= 22:
        return {"name": "转换时段", "weight": 2}
    return {"name": "沉淀时段", "weight": 3}


def _minute_rhythm(minute_feature: int) -> str:
    return ["前段启动", "中段承接", "后段调整", "末段转换"][minute_feature]


def _current_stage(age: int) -> dict[str, str]:
    if age <= 20:
        return {
            "range": "0-20",
            "name": "形成期",
            "theme": "环境影响",
            "description": "你目前更接近人生底层感受的形成阶段，外界评价、家庭环境和早期关系更容易影响自我判断。",
            "issue": "容易把他人的评价过早内化，需要慢慢建立属于自己的节奏。",
        }
    if age <= 35:
        return {
            "range": "20-35",
            "name": "选择期",
            "theme": "关键决策",
            "description": "你目前更接近方向选择频繁出现的阶段，事业、关系和生活方式都可能进入重新排序。",
            "issue": "容易一边想稳定，一边又感到旧路径不完全适合自己。",
        }
    return {
        "range": "35+",
        "name": "定型期",
        "theme": "结果显现",
        "description": "你目前更接近经验整合与长期价值显现的阶段，适合把过去经历沉淀成稳定影响力。",
        "issue": "容易受惯性影响，明明感到需要调整，却仍沿用旧判断方式。",
    }


def _behavior_tendency(structure_key: str, time_segment: str, gender: str) -> dict[str, str]:
    base = {
        "early": {
            "decision_style": "偏快，适合先行动再复盘，但需要保留校准空间。",
            "emotion_mode": "偏外放，情绪变化容易推动行动。",
            "relationship_mode": "偏独立，也会在重要关系里期待及时回应。",
            "career_rhythm": "冲刺型，适合快速反馈、主动争取和阶段性突破。",
        },
        "stable": {
            "decision_style": "偏稳，适合在充分观察后做长期选择。",
            "emotion_mode": "偏稳定，也可能把压力放在心里慢慢消化。",
            "relationship_mode": "偏理性，重视长期陪伴、现实承诺和安全感。",
            "career_rhythm": "积累型，适合深耕、复利和逐步建立信任。",
        },
        "late": {
            "decision_style": "前期容易犹豫，方向清晰后推进力会增强。",
            "emotion_mode": "偏压抑，需要通过阶段复盘看见真实需求。",
            "relationship_mode": "偏理性与谨慎，重要关系会影响阶段选择。",
            "career_rhythm": "积累后突破型，适合先沉淀能力，再寻找转向窗口。",
        },
        "wave": {
            "decision_style": "容易反复比较，适合用小步试错降低选择压力。",
            "emotion_mode": "偏波动，状态变化会明显影响判断。",
            "relationship_mode": "偏反复，靠近与退后之间需要更清晰的边界。",
            "career_rhythm": "试错型，适合在变化中整理能力和方向。",
        },
    }[structure_key]

    segment_hint = {
        "启动时段": "你的行动启动感较强，适合把想法尽快落到小范围尝试里。",
        "承接时段": "你的承接能力较明显，适合在稳定节奏里放大优势。",
        "转换时段": "你对阶段变化较敏感，适合定期整理旧选择是否仍然适合。",
        "沉淀时段": "你的内在消化能力较强，适合在安静复盘后再做关键决定。",
    }[time_segment]

    gender_hint = "性别信息只作为表达方式的辅助线索，不作为结论。"

    return {
        **base,
        "time_segment_hint": segment_hint,
        "gender_hint": gender_hint,
    }


def _rhythm_tags(structure_key: str, time_segment: str, minute_feature: int) -> list[str]:
    structure_tag = {
        "early": "前期启动",
        "stable": "稳定累积",
        "late": "后段清晰",
        "wave": "阶段起伏",
    }[structure_key]
    return [structure_tag, time_segment, _minute_rhythm(minute_feature)]
