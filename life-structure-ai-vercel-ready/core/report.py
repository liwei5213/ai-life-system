import re
from datetime import datetime

from core.structure import build_life_structure_model


def build_preview_report(
    structure: str,
    psychology_state: dict[str, str] | None = None,
    birth_chart: dict[str, object] | None = None,
    life_model: dict[str, object] | None = None,
) -> str:
    state_hint = _build_state_hint(psychology_state or {})
    preview_points = _build_preview_points(structure)
    model = life_model or {}
    return (
        _report_heading("①", "结构类型结论", "先看见你当前人生节奏的基础底色")
        + "\n"
        f"你的人生结构呈现为「{structure}」。"
        f"{_model_summary(model)}\n\n"
        + _report_heading("②", "三阶段人生模型", "把你的成长节奏放回时间线里")
        + "\n"
        f"{_format_stage_model(model)}\n\n"
        + _report_heading("③", "当前所处阶段判断", "理解你现在为什么会出现这些感受")
        + "\n"
        f"{_format_current_stage(model)}\n\n"
        + _report_heading("④", "行为倾向分析", "看见选择、情绪、关系和事业里的细微模式")
        + "\n"
        f"{_format_behavior_tendency(model)}"
        f"{state_hint}"
        "\n\n"
        + _report_heading("🔒", "未解释部分提示", "更深层的变化节点仍保留在完整报告中")
        + "\n"
        "你的完整人生结构中，还存在更深层的变化节点分析（需付费解锁）。"
        f"\n\n{preview_points}"
        "\n\n免费版先为你呈现已经浮现出来的核心线索；更具体的未来3年节奏、情感关键节点、事业突破点、风险提示与行动建议，会在完整报告中继续展开。"
    )


def pay_unlock(
    structure: str,
    birth_time: str = "",
    gender: str = "",
    psychology_state: dict[str, str] | None = None,
    birth_chart: dict[str, object] | None = None,
    life_model: dict[str, object] | None = None,
) -> str:
    profile = _build_life_profile(
        structure=structure,
        birth_time=birth_time,
        gender=gender,
        psychology_state=psychology_state or {},
        birth_chart=birth_chart,
        life_model=life_model,
    )
    return _paid_immersive_report(profile)


def _build_life_profile(
    structure: str,
    birth_time: str,
    gender: str,
    psychology_state: dict[str, str],
    birth_chart: dict[str, object] | None = None,
    life_model: dict[str, object] | None = None,
) -> dict[str, object]:
    birth_year = _extract_birth_year(birth_time)
    current_year = datetime.now().year
    age = current_year - birth_year if birth_year else None
    model = life_model or _safe_life_model(birth_time, gender)
    normalized_structure = str(model.get("structure_type") or _normalize_paid_structure(structure, birth_time))

    return {
        "structure": normalized_structure,
        "raw_structure": structure,
        "birth_time": birth_time,
        "birth_year": birth_year,
        "current_year": current_year,
        "age": age,
        "gender": gender,
        "psychology_state": psychology_state,
        "birth_chart": birth_chart or {},
        "life_model": model,
        "current_stage": model.get("current_stage") or _current_stage(age),
    }


def _extract_birth_year(birth_time: str) -> int | None:
    match = re.search(r"(19\d{2}|20\d{2})", birth_time)
    if not match:
        return None
    return int(match.group(1))


def _safe_life_model(birth_time: str, gender: str) -> dict[str, object]:
    if not birth_time:
        return {}
    try:
        return build_life_structure_model(birth_time, gender)
    except ValueError:
        return {}


def _model_summary(model: dict[str, object]) -> str:
    summary = model.get("structure_summary")
    return f"{summary}" if isinstance(summary, str) and summary else ""


def _format_stage_model(model: dict[str, object]) -> str:
    stages = model.get("stage_model")
    if not isinstance(stages, list):
        return (
            "- 0-20：形成期（环境影响）\n"
            "- 20-35：选择期（关键决策）\n"
            "- 35+：定型期（结果显现）"
        )

    lines = []
    for stage in stages:
        if not isinstance(stage, dict):
            continue
        lines.append(
            f"- {stage.get('range')}：{stage.get('name')}（{stage.get('theme')}）"
            f"：{stage.get('description')}"
        )
    return "\n".join(lines)


def _format_current_stage(model: dict[str, object]) -> str:
    stage = model.get("current_stage")
    if not isinstance(stage, dict):
        return "当前阶段需要结合完整出生时间继续判断。"
    return (
        f"你当前更接近「{stage.get('name')}」。"
        f"{stage.get('description')}"
        f"这一阶段常见的卡点是：{stage.get('issue')}"
    )


def _format_behavior_tendency(model: dict[str, object]) -> str:
    behavior = model.get("behavior_tendency")
    if not isinstance(behavior, dict):
        return (
            "- 决策风格：需要更多时间线索确认。\n"
            "- 情绪模式：适合先观察近期状态波动。\n"
            "- 关系模式：适合从安全感与边界感中识别。\n"
            "- 事业节奏：适合从阶段任务中逐步确认。"
        )
    return (
        f"- 决策风格：{behavior.get('decision_style')}\n"
        f"- 情绪模式：{behavior.get('emotion_mode')}\n"
        f"- 关系模式：{behavior.get('relationship_mode')}\n"
        f"- 事业节奏：{behavior.get('career_rhythm')}\n"
        f"- 时段倾向：{behavior.get('time_segment_hint')}"
    )


def _normalize_paid_structure(structure: str, birth_time: str) -> str:
    mapping = {
        "早发突破型": "早发型结构",
        "晚成积累型": "稳定积累型",
        "稳定型结构": "稳定积累型",
        "阶段跃迁型": "后发型结构",
        "后发爆发型": "后发型结构",
        "波动型结构": "波动成长型",
    }
    if structure:
        return mapping.get(structure, structure)
    model = _safe_life_model(birth_time, "")
    return str(model.get("structure_type") or "波动成长型")


def _current_stage(age: int | None) -> dict[str, str]:
    if age is None:
        return {
            "name": "阶段信息待确认",
            "range": "需要更完整的出生时间",
            "feature": "当前更适合先从反复出现的状态、选择方式和关系模式中观察人生节奏。",
            "issue": "容易出现的问题，是对自身阶段定位不清，导致选择时反复摇摆。",
        }
    if age <= 20:
        return {
            "name": "形成期",
            "range": "0-20",
            "feature": "这个阶段更像人生底层感受的形成期，家庭、学习、早期关系会影响你理解世界的方式。",
            "issue": "容易出现的问题，是把外界评价过早内化，导致自我节奏还没形成就开始怀疑自己。",
        }
    if age <= 35:
        return {
            "name": "选择期",
            "range": "20-35",
            "feature": "这个阶段会不断出现方向选择，事业、关系、城市、身份感都可能进入重新排序。",
            "issue": "容易出现的问题，是一边想稳定，一边又感到旧路径不完全适合自己。",
        }
    return {
        "name": "定型期",
        "range": "35+",
        "feature": "这个阶段更强调把过去的经验整理成稳定影响力，人生节奏会从探索转向定型与取舍。",
        "issue": "容易出现的问题，是惯性太强，明明感到需要调整，却仍沿用旧的判断方式。",
    }


def _paid_immersive_report(profile: dict[str, object]) -> str:
    return "\n\n".join(
        [
            _immersive_overall_section(profile),
            _immersive_inner_structure_section(profile),
            _immersive_stage_section(profile),
            _immersive_current_stage_section(profile),
            _immersive_future_section(profile),
            _immersive_action_section(profile),
        ]
    )


def _immersive_overall_section(profile: dict[str, object]) -> str:
    structure = str(profile["structure"])
    stage = profile["current_stage"]
    behavior = _profile_behavior(profile)
    pattern = _structure_story_profile(structure)
    stage_name = _stage_value(stage, "name", "当前阶段")
    stage_description = _stage_value(stage, "description", _stage_value(stage, "feature", "你正在经历的状态需要从节奏里慢慢辨认。"))

    return (
        _report_heading("①", "总体人生结构判断", "先看见你整个人生节奏的底色")
        + "\n"
        f"从你提供的时间线索来看，你的人生节奏更接近「{structure}」这一类结构。这里并不是要给你贴上固定标签，而是尝试顺着你的阶段感、选择方式和情绪流动，慢慢看见你一路以来是怎样和变化相处的。"
        f"{pattern['overall']}你可能会发现，很多真正影响你的变化，并不是以很剧烈的方式出现。它们更像是某个普通的夜晚里，心里忽然泛起的一点空、一点紧，或者是一种“我好像不能再这样下去”的微弱感觉。"
        f"这种状态通常意味着，你并不是简单地往前走，而是在一次次经历里，细细辨认什么让你安心，什么让你委屈，什么又在悄悄消耗你。\n\n"
        f"从当前阶段看，你更容易处在「{stage_name}」的气场里。{stage_description}"
        f"在做选择时，你内心可能会这样拉扯：{_soften_behavior_text(behavior.get('decision_style', '在选择前会反复衡量自己的真实感受。'))}"
        f"很多人在这个阶段都会有类似感受：表面上还在照常生活，心里却像有一盏小灯一直亮着，提醒自己过去的方式可能已经不够用了。"
        "这份报告更想陪你做的，不是急着判断你该往哪里去，而是把那些反复出现的感受、迟疑、期待和关系模式，轻轻放回同一条人生结构里，让你看见自己其实一直在努力靠近更真实的生活。"
    )


def _immersive_inner_structure_section(profile: dict[str, object]) -> str:
    structure = str(profile["structure"])
    behavior = _profile_behavior(profile)
    pattern = _structure_story_profile(structure)
    state_text = _psychology_state_narrative(profile)

    return (
        _report_heading("②", "性格与内在心理结构", "看见你为什么会这样感受、犹豫与保护自己")
        + "\n"
        f"你的内在安全感，可能并不只是来自别人说你好、认可你、需要你，更来自一种很细微的确认：我有没有在自己的节奏里，我有没有被好好理解，我是不是可以不用那么用力也被接住。{pattern['security']}"
        f"你可能会发现，当外界要求你马上给出答案、立刻做决定，或者关系里有人不断靠近你的边界时，你心里会出现一种说不清的紧绷感。"
        f"它不一定会立刻变成情绪爆发，更多时候像是一层轻轻的抵抗：你还在回应别人，但心里已经悄悄往后退了一步。你的情绪反应更像这样：{_soften_behavior_text(behavior.get('emotion_mode', '情绪会随着阶段压力出现细微起伏。'))}"
        "有时候你看起来很平静，甚至还能把事情安排好，可内在其实已经开始反复想：我这样是不是太敏感了，我是不是应该再忍一忍，还是我真的已经不舒服了。\n\n"
        f"在做选择时，你可能会经历这样的过程：{_soften_behavior_text(behavior.get('decision_style', '需要在感受和现实之间找到平衡。'))}"
        "这种拉扯会让你一边想保持理性，一边又很难忽视身体和情绪里那些细小的提醒。外界压力越强，你越可能先把自己收紧，把真实需求藏起来，等到积累到某个临界点，又突然很想离开、改变、重新开始。"
        f"{state_text}"
        "你需要温柔看见的是，那些犹豫并不说明你不坚定，那些情绪起伏也不说明你不成熟。很多时候，它们只是你内心很诚实的部分，在用一种不太响亮、却很真实的方式提醒你：有些旧的解释，已经不能再安放现在的你了。"
    )


def _immersive_stage_section(profile: dict[str, object]) -> str:
    structure = str(profile["structure"])
    pattern = _structure_story_profile(structure)

    return (
        _report_heading("③", "人生阶段结构分析", "把过去、现在与未来放回同一条成长线里")
        + "\n"
        "0-20岁更像心理底色慢慢形成的时期。这个阶段里，环境、家庭评价、学习经历和早期关系，会一点点影响你如何理解安全感。你可能很早就学会观察别人的表情和语气，知道什么时候该懂事，什么时候该把自己的想法先放一放。那时候的你，也许并不总能清楚说出委屈，只是会在心里慢慢形成一种感觉：什么样的自己更容易被喜欢，什么样的表达最好不要太明显。行为上，这一阶段更容易出现适应、模仿、压住真实需求，或者通过某种擅长的事情来获得被看见的感觉。\n\n"
        "20-35岁是关键选择期。很多人在这个阶段都会忽然意识到，自己不能只是顺着过去往前走了。方向、关系、城市、事业节奏、身份感，都可能开始重新排列。你可能会一边想抓住确定性，一边又被新的可能性轻轻牵动；一边告诉自己要现实一点，一边又很难忽略心里那个“不想将就”的声音。"
        f"{pattern['choice']}在行为上，这一阶段往往不是一下子变得清楚，而是不断试探、比较、投入，又在感到不舒服时慢慢退回来，重新确认自己到底要什么。\n\n"
        "35岁之后更接近定型期，但这里的定型并不是停止变化，而是你开始更懂得哪些东西值得留下。到了这一阶段，你可能会更在意长期价值、内在稳定和关系质量，也更能分辨一件事是在滋养你，还是只是在消耗你。行为上会从“寻找方向”慢慢转向“筛选方向”，从急着证明自己，转向更愿意照顾自己的节奏。"
    )


def _immersive_current_stage_section(profile: dict[str, object]) -> str:
    stage = profile["current_stage"]
    behavior = _profile_behavior(profile)
    stage_name = _stage_value(stage, "name", "当前阶段")
    issue = _stage_value(stage, "issue", "容易在选择中出现反复，需要用阶段目标稳定节奏。")

    return (
        _report_heading("④", "当前阶段深度解析", "解释你此刻的拉扯、困惑和正在松动的旧节奏")
        + "\n"
        f"你现在更接近「{stage_name}」的心理场域。这个阶段最明显的感受，往往不是单纯的忙，也不是单纯的不确定，而是心里开始同时出现几个很细小的声音：一个声音希望生活稳定下来，一个声音又想重新选择，还有一个声音会在安静的时候问自己，我是不是已经忍了太久，或者错过了什么。"
        "你可能会发现，很多事情表面上只是工作、关系或生活安排的问题，可真正触动你的，是更深处的自我感受：我到底适合什么，我还要不要继续这样走，我是不是可以换一种不那么委屈自己的方式。\n\n"
        f"当前阶段更容易出现的内在冲突是：{issue}"
        f"这种困惑之所以会出现，并不是因为你想太多，而是你的行为模式正在从旧节奏里慢慢松动，新的节奏却还没有完全站稳。你在行动上可能会表现为：{_soften_behavior_text(behavior.get('career_rhythm', '先观察，再尝试，再逐步确认方向。'))}"
        f"在关系里，你也可能会出现这样的细微状态：{_soften_behavior_text(behavior.get('relationship_mode', '既需要连接，也需要保留自己的空间。'))}"
        "其实这种状态并不罕见，很多人在这个阶段都会误以为自己是在退步，或者变得不像从前那样果断。但更温柔地看，你也许只是在重新整理人生的优先级。困惑并不代表方向消失，它更像是旧答案慢慢失效之后，新答案还没有完全长出来的中间地带。"
    )


def _immersive_future_section(profile: dict[str, object]) -> str:
    structure = str(profile["structure"])
    current_year = int(profile["current_year"])
    pattern = _structure_story_profile(structure)

    return (
        _report_heading("⑤", "未来趋势与关键变化", "观察接下来几年里可能慢慢浮现的选择信号")
        + "\n"
        f"从未来一段时间看，{current_year}-{current_year + 3}年更适合被理解为一个阶段性变化窗口。这里不需要用绝对结果去判断，更适合安静观察：你的节奏会不会在某些关系、选择或生活安排里，慢慢出现新的偏移。"
        f"你可能会发现，自己对一些事情的忍耐度开始变化。过去还能说服自己继续的事情，之后可能会越来越难再勉强；而一些一开始看起来不够确定的机会，却可能让你心里重新有一点亮起来的感觉。"
        f"{pattern['future']}这种趋势并不是催促你立刻推翻现有生活，而是温柔提醒你，可以开始分辨哪些选择真的让你安定，哪些只是暂时让焦虑安静下来。\n\n"
        +
        _report_heading("🔒", "未解锁提示模块", "更深层的节点、关系触发点与事业变量仍可继续展开")
        + "\n"
        "更深层的人生关键节点分析与情感模式拆解，需要完整版本解锁。"
        "在当前报告中，你已经能看见主要结构、阶段节奏与行为倾向；如果继续向下拆，会进入更具体的年份节点、关系触发点和事业变化变量，那些内容会更贴近你在现实生活中真正会遇到的转折细节。"
    )


def _immersive_action_section(profile: dict[str, object]) -> str:
    behavior = _profile_behavior(profile)

    return (
        _report_heading("⑥", "行动建议与心理安抚", "把理解落回生活里，温柔地重新调整自己的节奏")
        + "\n"
        "接下来最重要的，或许不是逼自己立刻做出一个完美决定，而是先把自己的节奏轻轻找回来。你可以先观察三件小事：哪些关系让你反复感到累，哪些选择让你迟迟不敢推进，哪些瞬间又会让你突然觉得自己好像还有力量。"
        f"你的事业和生活推进方式，可以温柔参考这一点：{_soften_behavior_text(behavior.get('career_rhythm', '用小范围尝试确认方向，再逐步扩大投入。'))}"
        "如果你发现自己总是在同一种问题里绕回来，请先不要急着责备自己。可以试着看一看，每次它出现之前，是否都有相似的情绪、相似的关系压力，或者相似的自我怀疑。重复并不一定说明你没有成长，很多时候只是因为新的选择还没有被你稳稳接住。\n\n"
        "你的困惑更多来自结构，而不是能力问题。"
        "这并不说明你有问题，也不说明你不够好。你只是处在一个需要重新整理内在秩序的阶段。很多人在这个阶段都会对自己变得很严格，甚至把短暂的迟疑看成失败。请尽量温和一点看待自己：真正稳定的人生节奏，不是从不摇晃，而是在摇晃之后，仍然能慢慢回到自己的主线。"
    )


def _profile_behavior(profile: dict[str, object]) -> dict[str, str]:
    model = profile.get("life_model")
    if isinstance(model, dict):
        behavior = model.get("behavior_tendency")
        if isinstance(behavior, dict):
            return {str(key): str(value) for key, value in behavior.items()}
    return {}


def _report_heading(number: str, title: str, subtitle: str) -> str:
    return (
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"【{number} {title}】\n"
        f"{subtitle}\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )


def _soften_behavior_text(text: object) -> str:
    value = str(text or "").strip()
    replacements = {
        "偏波动，状态变化会明显影响判断。": "状态变化时，心里的波纹会比较明显，也更容易影响当下的判断。",
        "偏外放，情绪变化容易推动行动。": "情绪一旦被触动，行动感也会跟着被推起来，很难完全装作没事。",
        "偏稳定，也可能把压力放在心里慢慢消化。": "表面常常能保持稳定，但压力可能会被你放在心里慢慢消化。",
        "偏压抑，需要通过阶段复盘看见真实需求。": "有些真实需要可能会先被你压下去，直到回头复盘时才慢慢浮出来。",
        "偏反复，靠近与退后之间需要更清晰的边界。": "在靠近和退后之间，你可能会有细微的反复，因此更需要清楚又温柔的边界。",
        "偏理性，重视长期陪伴、现实承诺和安全感。": "你会更在意长期陪伴、现实承诺和稳定的安全感，而不是短暂热烈。",
        "偏独立，也会在重要关系里期待及时回应。": "你看起来比较独立，但在真正重要的关系里，也会很在意对方是否及时回应你。",
        "偏理性与谨慎，重要关系会影响阶段选择。": "你在关系里会比较谨慎，但真正重要的人，仍然会影响你对阶段选择的感受。",
        "试错型，适合在变化中整理能力和方向。": "你不需要一次走到位，更适合在小范围尝试里，一点点整理能力和方向。",
        "冲刺型，适合快速反馈、主动争取和阶段性突破。": "当你看见反馈和机会时，内在动力会更容易被点亮，适合在阶段里主动争取。",
        "积累型，适合深耕、复利和逐步建立信任。": "你更适合在持续深耕里慢慢建立信任，让能力随着时间被看见。",
        "积累后突破型，适合先沉淀能力，再寻找转向窗口。": "你更适合先把能力安静沉淀下来，再等到合适窗口时温柔而坚定地转向。",
    }
    return replacements.get(value, value)


def _stage_value(stage: object, key: str, fallback: str) -> str:
    if isinstance(stage, dict):
        value = stage.get(key)
        if value:
            return str(value)
    return fallback


def _structure_story_profile(structure: str) -> dict[str, str]:
    profiles = {
        "早发型结构": {
            "overall": "你的人生节奏里，可能一直带着一种想要先往前走的力量。很多时候，你并不是完全想清楚了才行动，而是在行动之后，才慢慢听见自己真正想要什么。",
            "security": "你更容易从行动感、回应感和自我掌控感里获得安全感；当事情长期停住、没有反馈时，心里可能会慢慢浮出一种不安，好像自己正在被困住。",
            "choice": "你在选择期里，往往容易先被某个机会、某种可能性轻轻点亮，然后再通过现实反馈一点点筛选方向。",
            "future": "未来趋势更偏向主动打开局面，但关键并不是一次就选到最正确，而是允许自己边走边修正。",
        },
        "稳定积累型": {
            "overall": "你的节奏更像慢慢蓄力。很多变化一开始未必明显，却会在日复一日的坚持里，悄悄长成属于你的稳定方向。",
            "security": "你更容易从稳定关系、持续积累和长期被信任中获得安全感；过于快速的变化，可能会让你本能地想先停一停、看一看。",
            "choice": "你在选择期里未必急着显现锋芒，但会通过一次次持续投入，慢慢建立自己的底气。",
            "future": "未来趋势更偏向成果逐渐浮现，适合把已经积累的能力，转化成更清晰、更被看见的表达。",
        },
        "后发型结构": {
            "overall": "你的节奏可能并不急着在前期定型。人生方向往往要经过一段混沌、试探和自我怀疑之后，才会一点点浮现出更清楚的主线。",
            "security": "你更容易从方向感和阶段确认中获得安全感；当角色、关系或目标变得模糊时，内心可能会出现一种悬着的感觉。",
            "choice": "你在选择期里，可能会先经历一段不确定，随后在某个很具体的时刻突然明白：有些东西真的不再适合自己了。",
            "future": "未来趋势更偏向重新定位，某些阶段性变化可能会促使你整理旧路径，也可能让你看见以前忽略的新空间。",
        },
        "波动成长型": {
            "overall": "你的节奏里可能带着比较明显的起伏感。你的人生未必是沿着单一路径稳定推进，而是常常在变化、调整和重新选择里，慢慢靠近更真实的方向。",
            "security": "你更容易从被理解、可调整的空间和内在自由感里获得安全感；当环境过于僵硬时，心里的波纹会变得更明显。",
            "choice": "你在选择期里，可能会更频繁地比较不同可能，也会在反复试错之后，慢慢长出自己的判断力。",
            "future": "未来趋势更偏向在变化中整理方向，波动本身也许会成为你识别真正需求的重要信号。",
        },
    }
    return profiles.get(structure, profiles["波动成长型"])


def _psychology_state_narrative(profile: dict[str, object]) -> str:
    state = profile.get("psychology_state")
    if not isinstance(state, dict) or not state:
        return "如果你暂时还说不清自己的状态，也没有关系。有些变化本来就不是一下子能命名的，它们常常先停在胸口，像一种淡淡的闷、一点点失重感，等你慢慢回看时才变得清楚。"

    parts = []
    if state.get("current_state") in {"有变化但不确定方向", "正在转折期", "比较混乱"}:
        parts.append("你对当前状态的不确定感，可能并不是混乱本身，而是内在已经开始对旧节奏产生反应，只是新的方向还没有温柔地落下来。")
    if state.get("old_pattern") in {"会反复出现", "偶尔会重来"}:
        parts.append("那些反复回来的熟悉状态，通常不是偶然；它们更像心里某个还没被好好安放的角落，在一次次提醒你回头看见自己。")
    if state.get("love_change") in {"明显变化", "有些变化"}:
        parts.append("重要关系后的变化，可能会让你的表达方式、防御方式和安全感来源都变得不一样，有些人离开之后，留下的并不只是回忆，还有你对自己的重新理解。")
    if state.get("memory_connection") in {"经常会", "偶尔会"}:
        parts.append("当你偶尔想起很久没联系的人，或某些已经无法再见的人，那种突然涌上来的柔软感，往往也在说明你心里仍保留着很深的连接能力。")

    if not parts:
        return "你目前的回答更接近平稳观察状态，这通常意味着你可以不用急着给自己答案，而是从细微的偏好、状态和选择变化里，慢慢辨认真正让你舒服的节奏。"
    return "".join(parts)


def _paid_intro(profile: dict[str, object]) -> str:
    structure = str(profile["structure"])
    birth_time = str(profile["birth_time"] or "未填写完整")
    gender = str(profile["gender"] or "未指定")
    return (
        f"① 人生结构类型\n"
        f"你的结构类型：{structure}\n"
        f"输入线索：出生时间 {birth_time}，性别 {gender}。\n"
        f"出生时间已完成内部标准化，报告将围绕你的结构、节奏与阶段展开。\n"
        f"这个标签不是对人生做结论，而是用来描述你更容易呈现出的节奏、选择倾向和阶段变化方式。"
    )


def _paid_three_stage_section(profile: dict[str, object]) -> str:
    return (
        "② 三阶段人生结构\n"
        "0-20：形成期（环境影响）\n"
        "这一段更容易形成安全感、表达方式和对外界评价的敏感度。很多后来的选择习惯，会在这个阶段留下底色。\n\n"
        "20-35：选择期（关键决策）\n"
        "这一段更容易遇到事业方向、关系取舍、城市变化和身份转换。它决定的不是单一结果，而是你如何建立自己的主线。\n\n"
        "35+：定型期（结果显现）\n"
        "这一段更适合把过去的经验变成长期价值。人生会逐渐从追求更多可能，转向确认什么才真正适合自己。"
    )


def _paid_current_stage_section(profile: dict[str, object]) -> str:
    stage = profile["current_stage"]
    assert isinstance(stage, dict)
    age = profile["age"]
    age_line = f"按当前年份推算，你大约处于 {age} 岁附近。" if age is not None else "由于出生年份不完整，当前阶段需要结合你的状态进一步确认。"
    feature = stage.get("feature") or stage.get("description") or "当前阶段适合从结构、节奏和模式中继续观察。"
    issue = stage.get("issue") or "容易在选择中出现反复，需要用阶段目标稳定节奏。"
    behavior = profile.get("life_model", {})
    behavior_text = _format_behavior_tendency(behavior) if isinstance(behavior, dict) else ""
    return (
        "③ 当前所处阶段判断\n"
        f"{age_line}\n"
        f"当前阶段：{stage['name']}（{stage['range']}）\n"
        f"核心特点：{feature}\n"
        f"容易出现的问题：{issue}\n\n"
        "行为倾向模型\n"
        f"{behavior_text}"
    )


def _paid_turning_points_section(profile: dict[str, object]) -> str:
    birth_year = profile["birth_year"]
    current_year = int(profile["current_year"])
    if isinstance(birth_year, int):
        periods = [
            f"{birth_year + 20}-{birth_year + 22}",
            f"{birth_year + 29}-{birth_year + 32}",
            f"{current_year}-{current_year + 3}",
        ]
    else:
        periods = ["近期1-2年", "下一次关系或事业选择期", "未来3年"]

    structure = str(profile["structure"])
    focus = {
        "早发型结构": "更适合通过主动尝试打开局面，但需要避免只靠冲劲推进。",
        "稳定积累型": "更适合通过持续积累形成转折，关键是识别何时该把能力显露出来。",
        "后发型结构": "更容易在阶段变化中迎来明显推进，关键是看见旧路径何时需要更新。",
        "波动成长型": "更容易在起伏后重新找到方向，关键是把变化整理成判断力。",
    }.get(structure, "更适合从阶段变化中观察自己的方向。")

    return (
        "④ 关键人生转折点\n"
        f"- {periods[0]}：这个时间段可能更像底层节奏的形成或第一次方向感变化，适合回看当时的选择如何影响现在。\n"
        f"- {periods[1]}：这个时间段可能更容易出现关系、事业或生活方式的重新排序，某些看似被动的变化，会推动你看见真正的需求。\n"
        f"- {periods[2]}：未来3年的趋势更适合围绕“取舍”展开。{focus}"
    )


def _paid_relationship_section(profile: dict[str, object]) -> str:
    state = profile["psychology_state"]
    assert isinstance(state, dict)
    love_change = state.get("love_change", "")
    memory_connection = state.get("memory_connection", "")

    if love_change in {"明显变化", "有些变化"}:
        relationship_core = "你在重要关系后的变化较明显，说明关系对你的自我表达和安全感节奏影响较深。"
    elif memory_connection in {"经常会", "偶尔会"}:
        relationship_core = "你对旧关系和过往牵挂仍有感应，说明你并不是轻易切断情绪连接的人。"
    else:
        relationship_core = "你的关系模式更适合从安全感、回应方式和边界感三个方向观察。"

    return (
        "⑤ 情感/关系模式\n"
        f"{relationship_core}\n"
        "- 重复关系模式：可能会在熟悉的人身上寻找安全感，又在关系靠近后感到某种压力。\n"
        "- 情绪选择倾向：容易被“被理解”“被稳定回应”“对方是否愿意一起成长”影响选择。\n"
        "- 容易陷入的关系循环：一边期待深度连接，一边又可能因为害怕失衡而提前防御。"
    )


def _paid_career_section(profile: dict[str, object]) -> str:
    structure = str(profile["structure"])
    advice = {
        "早发型结构": (
            "适合的节奏：快启动、快反馈、边做边校准。\n"
            "不适合的路径类型：长期没有反馈、无法主动争取空间的路径。\n"
            "决策风格建议：先做小范围尝试，再用结果筛选方向，不要把一次选择看得过重。"
        ),
        "稳定积累型": (
            "适合的节奏：稳步积累、持续深耕、用时间换取可信度。\n"
            "不适合的路径类型：频繁切换、短期刺激强但缺少沉淀的路径。\n"
            "决策风格建议：每年固定复盘一次能力资产，看哪些能力正在形成长期价值。"
        ),
        "后发型结构": (
            "适合的节奏：先观察，再集中突破，适合在阶段转换时重新定位。\n"
            "不适合的路径类型：过早给自己定死方向，或长期困在不再适合的角色里。\n"
            "决策风格建议：当你连续感到旧路径消耗变大时，可以开始准备下一阶段的转向。"
        ),
        "波动成长型": (
            "适合的节奏：弹性迭代，在变化中积累判断力。\n"
            "不适合的路径类型：高度僵化、对情绪和状态没有容错空间的路径。\n"
            "决策风格建议：把每次波动后得到的经验写下来，形成自己的选择标准。"
        ),
    }
    return f"⑥ 事业路径建议\n{advice.get(structure, advice['波动成长型'])}"


def _paid_risk_section(profile: dict[str, object]) -> str:
    state = profile["psychology_state"]
    assert isinstance(state, dict)
    current_state = state.get("current_state", "")
    old_pattern = state.get("old_pattern", "")

    extra = []
    if current_state in {"有变化但不确定方向", "正在转折期", "比较混乱"}:
        extra.append("当前阶段容易把“不确定”误读成“自己不够好”，这会削弱行动感。")
    if old_pattern in {"会反复出现", "偶尔会重来"}:
        extra.append("某些旧模式反复出现时，适合先找触发点，而不是急着否定自己。")
    if not extra:
        extra.append("风险不在于变化本身，而在于没有记录变化背后的重复模式。")

    return (
        "⑦ 风险提示\n"
        "- 容易出现的决策偏差：在情绪强烈时过快判断，或在需要选择时反复拖延。\n"
        "- 容易重复的问题：同一种关系感受、同一种事业犹豫、同一种自我怀疑，可能以不同形式反复出现。\n"
        f"- 当前提醒：{''.join(extra)}"
    )


def _paid_comfort_section(profile: dict[str, object]) -> str:
    return (
        "⑧ 内生力窥探\n"
        "你的困惑是结构性的，不是能力问题。\n"
        "你的发展节奏是有规律的，只是这种规律常常要在回看时才会变得清楚。\n"
        "当前阶段的不确定性是正常的，它更像是人生进入下一段节奏前的整理期，而不是停滞。"
    )


def _paid_action_section(profile: dict[str, object]) -> str:
    stage = profile["current_stage"]
    assert isinstance(stage, dict)
    return (
        "⑨ 行动方向\n"
        f"- 先确认你当前最主要的阶段任务：{stage['name']}。\n"
        "- 接下来30天，建议记录三类信息：让你反复消耗的关系、让你迟迟不敢推进的选择、让你感到重新有力量的事情。\n"
        "- 接下来3个月，适合做一次方向筛选：保留能让你形成长期节奏的事，减少只带来短期情绪波动的投入。\n"
        "- 这份报告的重点不是替你决定人生，而是帮你看见结构、节奏、阶段、倾向、模式与趋势。"
    )


def _build_state_hint(psychology_state: dict[str, str]) -> str:
    if not psychology_state:
        return ""

    change_feeling = psychology_state.get("change_feeling", "")
    preference_shift = psychology_state.get("preference_shift", "")
    current_state = psychology_state.get("current_state", "")
    old_pattern = psychology_state.get("old_pattern", "")
    memory_connection = psychology_state.get("memory_connection", "")
    love_change = psychology_state.get("love_change", "")

    hints = []

    if change_feeling in {"经常有", "偶尔有"}:
        hints.append("你对生活整体感受的变化有一定觉察，这说明你的节奏并不只是被事件推动，也可能在被内在状态悄悄牵引。")
    if preference_shift in {"明显有", "有但不确定原因"}:
        hints.append("你曾经注意到偏好或风格的变化，这类细节往往会成为阶段转换前的微弱信号。")
    if current_state in {"有变化但不确定方向", "正在转折期", "比较混乱"}:
        hints.append("你当下的状态更接近变化之中，适合先看见自己的模式，再判断下一步该如何安放重心。")
    if old_pattern in {"会反复出现", "偶尔会重来"}:
        hints.append("你回看过去时能感到某些模式反复出现，这种重复感可能正是人生结构里值得被解读的线索。")
    if memory_connection in {"经常会", "偶尔会"}:
        hints.append("你对旧关系与过往牵挂仍有感应，这类回忆可能代表某些情绪节点还在影响你当下的状态。")
    if love_change in {"明显变化", "有些变化"}:
        hints.append("重要关系后的性格变化，往往会让一个人的表达方式、防御方式和安全感节奏被重新塑造。")

    if not hints:
        return "你目前的回答更接近平稳观察状态，适合从细微变化中慢慢辨认自己的节奏。"

    return "".join(hints)


def _build_preview_points(structure: str) -> str:
    points = {
        "早发型结构": [
            "未来3年趋势线索：你的节奏可能更偏向主动打开局面，关键不在于一开始就选择完美方向，而在于从行动中筛选真正适合自己的道路。",
            "情感关键节点线索：关系里容易因为推进速度、期待回应和安全感节奏出现分歧，某些重要关系会提醒你重新理解自己的表达方式。",
            "事业突破点线索：突破更可能来自一次明确的尝试、一次主动争取，或一次把过往经验重新整理成可复制能力的机会。",
        ],
        "稳定积累型": [
            "未来3年趋势线索：你的节奏可能更偏向稳定蓄力，许多变化不会立刻显现，但会在某个阶段逐渐形成清晰的结果。",
            "情感关键节点线索：关系里更容易被长期陪伴、现实承诺和稳定回应触动，真正影响你的往往不是热烈瞬间，而是持续感。",
            "事业突破点线索：突破更可能来自专业沉淀、资源累积和被信任的角色变化，适合观察自己在哪些事情上越来越稳。",
        ],
        "后发型结构": [
            "未来3年趋势线索：你的节奏可能出现阶段切换，某些看似突然的变化，其实是在提醒你旧模式已经不再完全适用。",
            "情感关键节点线索：关系状态可能随着人生阶段变化而变化，重要节点往往出现在身份、目标或生活方向重新排序的时候。",
            "事业突破点线索：突破更可能来自转型、升级或重新定位，当你愿意调整旧路径时，新的空间会更容易被看见。",
        ],
        "波动成长型": [
            "未来3年趋势线索：你的节奏可能带有起伏感，但起伏本身并不只是阻力，也可能是帮你识别真正方向的信号。",
            "情感关键节点线索：关系里容易被情绪状态、距离变化或内在安全感影响，某些牵挂会让你重新理解自己的需要。",
            "事业突破点线索：突破更可能来自适应变化后的重新选择，适合把经历过的波动整理成判断力和弹性。",
        ],
    }
    selected = points.get(
        structure,
        [
            "未来3年趋势线索：你的节奏仍需要更多信息辅助判断，但某些反复出现的状态值得被认真看见。",
            "情感关键节点线索：关系中的感受变化，可能会成为理解自身模式的重要入口。",
            "事业突破点线索：事业方向适合从优势、资源和阶段状态中逐步确认。",
        ],
    )
    return "已显现的关键线索：\n" + "\n".join(f"- {item}" for item in selected)


def _explain_structure(structure: str) -> str:
    descriptions = {
        "早发型结构": (
            "1. 人生结构解释（增强版）\n"
            "「早发型结构」的核心节奏在于较早显现自我驱动力，人生节奏中容易出现先行动、再修正的模式。"
            "这类结构往往适合在试错中打开局面，通过早期经验建立判断力。"
        ),
        "稳定积累型": (
            "1. 人生结构解释（增强版）\n"
            "「稳定积累型」的核心节奏在于厚积薄发，人生节奏更像由长期沉淀逐渐形成力量。"
            "这类结构通常不急于在早期定型，更适合通过持续积累获得稳定表达。"
        ),
        "后发型结构": (
            "1. 人生结构解释（增强版）\n"
            "「后发型结构」的核心节奏在于人生会呈现明显的阶段切换，重要变化常来自认知、环境或角色的升级。"
            "这类结构适合在关键节点主动复盘，并为下一阶段重新配置资源。"
        ),
        "波动成长型": (
            "1. 人生结构解释（增强版）\n"
            "「波动成长型」的核心节奏在于变化中成长，人生节奏可能更强调适应、调整与重新定位。"
            "这类结构适合把波动视为信息来源，并从变化中提炼稳定能力。"
        ),
    }
    return descriptions.get(
        structure,
        "1. 人生结构解释（增强版）\n当前结构信息较少，更适合先从出生时间线索中观察个人节奏，再逐步补充完整分析。",
    )


def _personality_section(structure: str) -> str:
    traits = {
        "早发型结构": [
            "行动意愿较强，容易通过尝试获得安全感。",
            "对机会变化较敏感，适合保持快速反馈机制。",
            "自我要求可能偏高，需要给成长留出缓冲空间。",
            "表达上较直接，适合学习更稳定的沟通节奏。",
        ],
        "稳定积累型": [
            "性格中带有稳健倾向，更重视长期价值。",
            "做决定时可能更依赖经验和现实验证。",
            "适合在熟悉领域深耕，逐渐形成不可替代性。",
            "情绪节奏相对内敛，需要主动表达真实需求。",
        ],
        "后发型结构": [
            "适应阶段变化的能力较明显，容易在转折中成长。",
            "思维中带有升级意识，适合定期重建目标。",
            "对环境反馈较敏锐，可能更容易看见下一步机会。",
            "需要避免频繁切换导致能量分散。",
        ],
        "波动成长型": [
            "感受力和调整力较强，容易从变化中获得经验。",
            "性格中可能带有探索倾向，适合保留一定弹性。",
            "对关系和环境氛围较敏感，需要建立稳定内核。",
            "成长常来自反复校准，而不是单一路径推进。",
        ],
    }
    selected = traits.get(structure, ["当前结构仍需更多信息辅助判断。"])
    lines = "\n".join(f"- {item}" for item in selected)
    return f"2. 性格分析（3-5条）\n{lines}"


def _career_section(structure: str) -> str:
    suggestions = {
        "早发型结构": "适合选择能快速反馈、允许试错和持续升级的事业路径，例如产品、销售、运营、创业型项目或需要主动开局的岗位。",
        "稳定积累型": "适合选择重视专业沉淀、经验复利和长期信任的事业路径，例如咨询、管理、技术、教育、研究或稳定型业务。",
        "后发型结构": "适合选择存在清晰成长台阶的事业路径，例如项目制工作、跨领域转型、管理晋升或需要阶段性突破的方向。",
        "波动成长型": "适合选择保留弹性、重视适应力和整合能力的事业路径，例如内容、品牌、自由职业、复合型岗位或变化型行业。",
    }
    return f"3. 事业路径建议\n{suggestions.get(structure, '事业方向适合先从优势能力和现实资源出发，逐步形成稳定路径。')}"


def _relationship_section(structure: str) -> str:
    patterns = {
        "早发型结构": "情感模式中可能更重视回应速度和共同成长，适合在关系中降低急于推进的节奏，给彼此留下理解空间。",
        "稳定积累型": "情感模式中可能更重视稳定、承诺和长期陪伴，适合通过持续沟通让关系温度逐渐显现。",
        "后发型结构": "情感模式中可能会随着人生阶段而变化，适合在重要转折期重新确认双方目标和相处方式。",
        "波动成长型": "情感模式中可能更容易受状态和环境影响，适合建立清晰边界，并用稳定沟通减少误解。",
    }
    return f"4. 情感模式分析\n{patterns.get(structure, '情感模式适合从安全感、沟通节奏和边界感三个方向观察。')}"


def _life_rhythm_section(structure: str) -> str:
    rhythms = {
        "早发型结构": "早期阶段适合打开局面，中期阶段适合筛选方向，后期阶段更适合把经验沉淀为稳定影响力。",
        "稳定积累型": "早期阶段适合学习和蓄力，中期阶段适合建立专业壁垒，后期阶段更容易呈现成熟稳定的个人价值。",
        "后发型结构": "人生节奏可能呈现数次明显切换，每一次跃迁都适合围绕能力升级、圈层变化和目标重组来观察。",
        "波动成长型": "人生节奏可能带有起伏感，适合用阶段计划承接变化，并在每次调整后提炼新的稳定模式。",
    }
    return f"5. 人生节奏（阶段分析）\n{rhythms.get(structure, '人生节奏适合以阶段复盘为主，观察每一段经历带来的结构变化。')}"


def _risk_section(structure: str) -> str:
    risks = {
        "早发型结构": "风险提示：容易因推进过快而忽略长期成本，适合在关键选择前增加复盘和验证。",
        "稳定积累型": "风险提示：容易因过度等待而错过表达窗口，适合在准备到一定程度后主动释放能力。",
        "后发型结构": "风险提示：容易在转折期出现方向感摇摆，适合用清晰目标降低切换成本。",
        "波动成长型": "风险提示：容易受外界变化影响节奏，适合建立固定习惯和稳定判断标准。",
    }
    return f"6. 风险提示\n{risks.get(structure, '风险提示：适合避免过度依赖单一判断，保持结构化复盘。')}"


def _life_label_section(structure: str) -> str:
    labels = {
        "早发型结构": "7. 一句总结人生标签\n在行动中开局，在复盘中成形。",
        "稳定积累型": "7. 一句总结人生标签\n以长期积累换取稳定绽放。",
        "后发型结构": "7. 一句总结人生标签\n每一次阶段切换，都是人生结构的重新展开。",
        "波动成长型": "7. 一句总结人生标签\n在变化中校准方向，在起伏中长出稳定力量。",
    }
    return labels.get(structure, "7. 一句总结人生标签\n在结构中理解自己，在节奏中形成方向。")
