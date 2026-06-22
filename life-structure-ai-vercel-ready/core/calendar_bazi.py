from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

LUNAR_INFO = [
    0x04BD8, 0x04AE0, 0x0A570, 0x054D5, 0x0D260, 0x0D950, 0x16554, 0x056A0, 0x09AD0, 0x055D2,
    0x04AE0, 0x0A5B6, 0x0A4D0, 0x0D250, 0x1D255, 0x0B540, 0x0D6A0, 0x0ADA2, 0x095B0, 0x14977,
    0x04970, 0x0A4B0, 0x0B4B5, 0x06A50, 0x06D40, 0x1AB54, 0x02B60, 0x09570, 0x052F2, 0x04970,
    0x06566, 0x0D4A0, 0x0EA50, 0x06E95, 0x05AD0, 0x02B60, 0x186E3, 0x092E0, 0x1C8D7, 0x0C950,
    0x0D4A0, 0x1D8A6, 0x0B550, 0x056A0, 0x1A5B4, 0x025D0, 0x092D0, 0x0D2B2, 0x0A950, 0x0B557,
    0x06CA0, 0x0B550, 0x15355, 0x04DA0, 0x0A5D0, 0x14573, 0x052D0, 0x0A9A8, 0x0E950, 0x06AA0,
    0x0AEA6, 0x0AB50, 0x04B60, 0x0AAE4, 0x0A570, 0x05260, 0x0F263, 0x0D950, 0x05B57, 0x056A0,
    0x096D0, 0x04DD5, 0x04AD0, 0x0A4D0, 0x0D4D4, 0x0D250, 0x0D558, 0x0B540, 0x0B6A0, 0x195A6,
    0x095B0, 0x049B0, 0x0A974, 0x0A4B0, 0x0B27A, 0x06A50, 0x06D40, 0x0AF46, 0x0AB60, 0x09570,
    0x04AF5, 0x04970, 0x064B0, 0x074A3, 0x0EA50, 0x06B58, 0x055C0, 0x0AB60, 0x096D5, 0x092E0,
    0x0C960, 0x0D954, 0x0D4A0, 0x0DA50, 0x07552, 0x056A0, 0x0ABB7, 0x025D0, 0x092D0, 0x0CAB5,
    0x0A950, 0x0B4A0, 0x0BAA4, 0x0AD50, 0x055D9, 0x04BA0, 0x0A5B0, 0x15176, 0x052B0, 0x0A930,
    0x07954, 0x06AA0, 0x0AD50, 0x05B52, 0x04B60, 0x0A6E6, 0x0A4E0, 0x0D260, 0x0EA65, 0x0D530,
    0x05AA0, 0x076A3, 0x096D0, 0x04BD7, 0x04AD0, 0x0A4D0, 0x1D0B6, 0x0D250, 0x0D520, 0x0DD45,
    0x0B5A0, 0x056D0, 0x055B2, 0x049B0, 0x0A577, 0x0A4B0, 0x0AA50, 0x1B255, 0x06D20, 0x0ADA0,
]

STEMS = "甲乙丙丁戊己庚辛壬癸"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"
ZODIAC = "鼠牛虎兔龙蛇马羊猴鸡狗猪"
CN_MONTHS = ["正", "二", "三", "四", "五", "六", "七", "八", "九", "十", "冬", "腊"]
CN_DAYS = [
    "初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
    "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
    "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十",
]


@dataclass
class LunarDate:
    year: int
    month: int
    day: int
    is_leap: bool


def build_birth_chart(birth_time: str) -> dict[str, object]:
    dt = datetime.strptime(birth_time, "%Y-%m-%d %H:%M")
    lunar = solar_to_lunar(dt.date())
    bazi = build_bazi(dt, lunar)
    lunar_text = format_lunar(lunar)
    return {
        "solar_birth": birth_time,
        "lunar_birth": lunar_text,
        "lunar": {
            "year": lunar.year,
            "month": lunar.month,
            "day": lunar.day,
            "is_leap": lunar.is_leap,
        },
        "bazi": bazi,
        "summary": (
            f"公历 {birth_time} 已转换为 {lunar_text}。"
            f"命盘四柱参考为：{bazi['year']}年、{bazi['month']}月、{bazi['day']}日、{bazi['hour']}时。"
        ),
    }


def solar_to_lunar(solar_date: date) -> LunarDate:
    base = date(1900, 1, 31)
    offset = (solar_date - base).days
    if offset < 0:
        raise ValueError("仅支持 1900-01-31 之后的日期")

    lunar_year = 1900
    while lunar_year < 2050:
        days = _lunar_year_days(lunar_year)
        if offset < days:
            break
        offset -= days
        lunar_year += 1

    leap = _leap_month(lunar_year)
    lunar_month = 1
    is_leap = False

    while lunar_month <= 12:
        days = _leap_days(lunar_year) if is_leap else _month_days(lunar_year, lunar_month)
        if offset < days:
            break
        offset -= days

        if leap == lunar_month and not is_leap:
            is_leap = True
        else:
            if is_leap:
                is_leap = False
            lunar_month += 1

    return LunarDate(lunar_year, lunar_month, offset + 1, is_leap)


def build_bazi(dt: datetime, lunar: LunarDate) -> dict[str, str]:
    year_index = (lunar.year - 4) % 60
    year_stem_index = year_index % 10
    month_stem_index = ((year_stem_index % 5) * 2 + lunar.month + 1) % 10
    month_branch_index = (lunar.month + 1) % 12
    day_index = (_julian_day(dt.date()) + 49) % 60
    day_stem_index = day_index % 10
    hour_branch_index = ((dt.hour + 1) // 2) % 12
    hour_stem_index = ((day_stem_index % 5) * 2 + hour_branch_index) % 10

    return {
        "year": _ganzhi(year_index),
        "month": STEMS[month_stem_index] + BRANCHES[month_branch_index],
        "day": _ganzhi(day_index),
        "hour": STEMS[hour_stem_index] + BRANCHES[hour_branch_index],
    }


def format_lunar(lunar: LunarDate) -> str:
    leap = "闰" if lunar.is_leap else ""
    return f"农历{lunar.year}年{leap}{CN_MONTHS[lunar.month - 1]}月{CN_DAYS[lunar.day - 1]}（{ZODIAC[(lunar.year - 4) % 12]}年）"


def _lunar_year_days(year: int) -> int:
    total = 348
    info = LUNAR_INFO[year - 1900]
    for month_index in range(12):
        if info & (0x8000 >> month_index):
            total += 1
    return total + _leap_days(year)


def _leap_month(year: int) -> int:
    return LUNAR_INFO[year - 1900] & 0xF


def _leap_days(year: int) -> int:
    if _leap_month(year):
        return 30 if (LUNAR_INFO[year - 1900] & 0x10000) else 29
    return 0


def _month_days(year: int, month: int) -> int:
    return 30 if (LUNAR_INFO[year - 1900] & (0x10000 >> month)) else 29


def _ganzhi(index: int) -> str:
    return STEMS[index % 10] + BRANCHES[index % 12]


def _julian_day(value: date) -> int:
    year = value.year
    month = value.month
    day = value.day
    if month <= 2:
        year -= 1
        month += 12
    a = year // 100
    b = 2 - a + a // 4
    return int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + b - 1524
