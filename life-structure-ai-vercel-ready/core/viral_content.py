EMOTION_PROFILES = {
    "迷茫": {
        "scene": "夜晚城市 / 空街 / 只有一盏灯亮着的房间",
        "social": "就业压力上升、行业变化加速，让很多年轻人开始重新思考自己到底适合什么样的生活。",
        "public": "很多公众人物在高压阶段，也会经历阶段性的方向重构与迷茫期，只是外界常常只看见结果，看不见中间那段拉扯。",
        "micro": "心里像有一团雾，明明每天都在做事，却总觉得方向隔着一层看不清的玻璃。",
    },
    "焦虑": {
        "scene": "人群模糊 / 快速移动光影 / 地铁站里匆忙经过的人",
        "social": "节奏越来越快，行业规则不断变化，很多人表面上还在努力，心里却开始担心自己是不是跟不上。",
        "public": "很多被看见的人，也会在高曝光和高压力里经历节奏失衡，只是他们往往需要把脆弱藏得更深。",
        "micro": "身体像一直绷着一根线，哪怕没有真正发生什么，心里也会先替未来紧张起来。",
    },
    "转折": {
        "scene": "日出 / 山顶 / 光穿云层 / 清晨拉开的窗帘",
        "social": "当外部环境变化加快，越来越多人会在某个阶段突然意识到，过去那套生活方式可能需要重新调整。",
        "public": "很多公众人物的转型，并不是一夜之间发生的，而是经历过一段不确定、试探和重新定位之后，才慢慢被看见。",
        "micro": "有些念头不是突然冒出来的，而是在很多个安静瞬间里，一点点把你推向新的选择。",
    },
    "压抑": {
        "scene": "雨天 / 室内窗边 / 没开灯的房间 / 玻璃上的水痕",
        "social": "现实压力、关系期待和工作节奏叠在一起时，很多人会把真正的感受先压下去，直到某个瞬间才发现自己已经很累。",
        "public": "很多外表稳定的人，也可能在长期高压里经历情绪低谷，只是这些部分很少被放到台前讲。",
        "micro": "你可能说不出哪里不舒服，只是突然不想回复消息，也不想解释自己为什么沉默。",
    },
}


STRUCTURE_PROFILES = {
    "早发型结构": {
        "rhythm": "前期容易被机会、变化和行动感推着往前走",
        "pain": "越想尽快打开局面，越容易在某些时刻忽然怀疑方向",
        "mirror": "你可能会一边很想往前冲，一边又在夜里反复问自己，这条路到底是不是自己真正想要的。",
    },
    "稳定积累型": {
        "rhythm": "节奏更像慢慢蓄力，很多结果不会立刻显现",
        "pain": "越是长期坚持，越可能在看不到反馈时感到委屈和不安",
        "mirror": "你可能会习惯把很多压力放在心里，表面上很稳，内在却一直在等一个被看见的时刻。",
    },
    "后发型结构": {
        "rhythm": "前期容易混沌，方向常常要经过一段试探后才慢慢清晰",
        "pain": "越急着给自己答案，越容易觉得自己是不是落后了",
        "mirror": "你可能会在某些阶段很怀疑自己，但真正的变化往往就在这种不确定里慢慢成形。",
    },
    "波动成长型": {
        "rhythm": "阶段起伏更明显，常常通过变化、调整和重新选择靠近真实方向",
        "pain": "越想稳定下来，越容易被内在的变化感再次拉回去",
        "mirror": "你可能会反复经历靠近、犹豫、退后和重新选择，好像人生一直在提醒你看见某个模式。",
    },
}


def generate_viral_content(
    structure: str = "波动成长型",
    emotion: str = "迷茫",
    platform: str = "小红书",
    audience: str = "正在经历人生转折的人",
) -> dict[str, object]:
    structure_profile = STRUCTURE_PROFILES.get(structure, STRUCTURE_PROFILES["波动成长型"])
    emotion_profile = EMOTION_PROFILES.get(emotion, EMOTION_PROFILES["迷茫"])

    titles = _build_titles(structure, emotion)
    opening = _build_opening(emotion_profile, audience)
    structure_explanation = _build_structure_explanation(structure_profile)
    emotional_deepening = _build_emotional_deepening(structure_profile, emotion_profile)
    reality_mapping = _build_reality_mapping(emotion_profile)
    visual_scene = _build_visual_scene(emotion, emotion_profile, platform)
    user_mirror = _build_user_mirror(structure_profile, audience)

    return {
        "platform": platform,
        "audience": audience,
        "structure": structure,
        "emotion": emotion,
        "titles": titles,
        "emotional_opening": opening,
        "structure_explanation": structure_explanation,
        "emotional_deepening": emotional_deepening,
        "reality_mapping": reality_mapping,
        "visual_scene": visual_scene,
        "user_mirror": user_mirror,
        "content": _format_content(
            titles=titles,
            opening=opening,
            structure_explanation=structure_explanation,
            emotional_deepening=emotional_deepening,
            reality_mapping=reality_mapping,
            visual_scene=visual_scene,
            user_mirror=user_mirror,
        ),
    }


def generate_viral_content_batch(
    structure: str = "波动成长型",
    emotions: list[str] | None = None,
    platform: str = "小红书",
    audience: str = "正在经历人生转折的人",
) -> list[dict[str, object]]:
    selected_emotions = emotions or ["迷茫", "焦虑", "转折", "压抑"]
    return [
        generate_viral_content(
            structure=structure,
            emotion=emotion,
            platform=platform,
            audience=audience,
        )
        for emotion in selected_emotions
    ]


def _build_titles(structure: str, emotion: str) -> list[str]:
    return [
        f"为什么你越努力，越觉得自己卡在{emotion}里？",
        f"你的人生可能不是出了问题，而是正在进入{structure}的节奏",
        "有些人的人生，不是突然迷路，而是结构正在换方向",
    ]


def _build_opening(emotion_profile: dict[str, str], audience: str) -> str:
    return (
        f"你可能会发现，自己明明已经很努力了，却还是会在某些时刻突然停下来。"
        f"不是不想继续，也不是完全没有方向，而是心里会出现一种很细微的空白感。"
        f"尤其是{audience}，常常会在白天把事情处理得很好，到了夜里却突然觉得，自己好像被困在一个说不清的位置。"
        f"{emotion_profile['micro']}"
    )


def _build_structure_explanation(profile: dict[str, str]) -> str:
    return (
        "很多时候，人生的卡顿并不一定来自你不够努力，而是来自节奏和结构正在变化。"
        f"有些人的人生节奏是{profile['rhythm']}。"
        "当旧的模式还能勉强维持，但新的方向还没有真正清晰时，人就会出现一种微妙的停顿感。"
        "这不是结论，也不是对你下定义，而是一种可以被观察的结构：你怎样选择，怎样退后，怎样在关系和事业里反复确认自己的位置。"
    )


def _build_emotional_deepening(profile: dict[str, str], emotion_profile: dict[str, str]) -> str:
    return (
        f"真正让人难受的，往往不是某一件具体的事，而是那种反复拉扯的感觉。"
        f"你可能会一边告诉自己要理性一点，一边又很难忽视心里那阵轻轻的酸胀。"
        f"{profile['pain']}。"
        "有时候你会很想解释自己为什么累，可话到嘴边又觉得，好像没有哪一句能说完整。"
        f"{emotion_profile['micro']}"
        "这种微小的情绪变化，常常比外在事件更真实，因为它提醒你，内在已经开始对旧节奏产生反应。"
    )


def _build_reality_mapping(emotion_profile: dict[str, str]) -> str:
    return (
        "现实里，这并不是少数人才会经历的状态。"
        f"{emotion_profile['social']}"
        f"{emotion_profile['public']}"
        "所以，当你觉得自己好像卡住了，也许不只是个人问题，而是很多人都在经历的阶段性重构。"
        "只是每个人表现出来的方式不同：有人换行业，有人离开一段关系，有人开始重新整理生活，有人只是突然不想再勉强自己。"
    )


def _build_visual_scene(emotion: str, emotion_profile: dict[str, str], platform: str) -> str:
    return (
        f"【推荐配图场景】{emotion_profile['scene']}。\n"
        f"如果发布在{platform}，画面可以尽量留白，不要太满。"
        f"{emotion}这种情绪更适合用光线、背影、窗边、街道和远景来表达。"
        "让画面先替用户说出那种说不清的感受，文字再慢慢把她带进内容里。"
    )


def _build_user_mirror(profile: dict[str, str], audience: str) -> str:
    return (
        f"如果你处在这种结构里，你可能会在很多时候，明明做了很多努力，却仍然觉得方向不够清晰。"
        f"{profile['mirror']}"
        f"你可能不是没有能力，也不是不够清醒，只是正处在一个需要重新理解自己节奏的阶段。"
        f"对{audience}来说，真正重要的不是立刻找到答案，而是先看见自己反复出现的模式。"
        "如果你想了解自己的结构类型，可以测一下你的模式。"
    )


def _format_content(
    titles: list[str],
    opening: str,
    structure_explanation: str,
    emotional_deepening: str,
    reality_mapping: str,
    visual_scene: str,
    user_mirror: str,
) -> str:
    return "\n\n".join(
        [
            "① 爆款标题（3个）\n" + "\n".join(f"- {title}" for title in titles),
            "② 情绪开场\n" + opening,
            "③ 结构解释\n" + structure_explanation,
            "④ 情绪深化\n" + emotional_deepening,
            "⑤ 现实映射模块\n" + reality_mapping,
            "⑥ 情绪风景映射模块\n" + visual_scene,
            "⑦ 用户代入镜像模块\n" + user_mirror,
        ]
    )
