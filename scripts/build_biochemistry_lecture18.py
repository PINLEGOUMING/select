#!/usr/bin/env python3
"""Build the checked translation question-bank payload without copying the source PDF."""

from __future__ import annotations

import json
import random
from pathlib import Path

from PIL import Image


SOURCE_PDF = Path("/Users/ray/Downloads/18翻译.pdf")
MIND_MAP = Path("/Users/ray/Downloads/生物化学思维导图 10.jpg")
OUTPUT = Path("src/data/biochemistry-lecture18-data.json")
IMAGE_OUTPUT = Path("public/biochemistry/lecture-pages/lecture-18-page-01.webp")
LECTURE_NUMBER = 18
TITLE = "生化 翻译"
TOPIC = "氨基酸与蛋白质"


# The source contains 14 numbered entries. Entries 5 and 6 each contain two
# stems; two other tightly related pairs are merged here, yielding 12 groups
# and 16 stems while preserving every original question and checked answer.
GROUPS = [
    {
        "title": "原核生物蛋白质合成概述",
        "source": "2016N26",
        "options": [
            "释放因子是 eRF",
            "一条 mRNA 可编码多种蛋白质（多顺反子）",
            "80S 核糖体参与蛋白质合成",
            "蛋白质在细胞核内合成、在胞质中加工",
        ],
        "stems": [("以下关于原核生物蛋白质合成的叙述中，正确的是", ["一条 mRNA 可编码多种蛋白质（多顺反子）"])],
        "note": "原核生物常见多顺反子 mRNA，核糖体为 70S，释放因子为 RF。",
    },
    {
        "title": "蛋白质生物合成的氨基酸原料",
        "source": "2025N24",
        "options": ["羟脯氨酸", "半胱氨酸", "硒代半胱氨酸", "甲硫氨酸"],
        "stems": [("可以作为蛋白质生物合成原料掺入多肽链中的氨基酸有", ["半胱氨酸", "硒代半胱氨酸", "甲硫氨酸"])],
        "note": "硒代半胱氨酸属于第 21 种编码氨基酸；羟脯氨酸由翻译后修饰形成。",
    },
    {
        "title": "翻译所需能量与 GTP 酶",
        "source": "2015N31、2014N27",
        "options": ["23S rRNA", "EF-G", "EF-Tu", "RF2", "ATP", "GTP", "CTP", "UTP"],
        "stems": [
            ("蛋白质生物合成时具有 GTP 酶活性的物质是", ["EF-Tu"]),
            ("参与蛋白质生物合成的能量物质有", ["ATP", "GTP"]),
        ],
        "note": "答案按本讲义真题口径核对：GTP 酶为 EF-Tu；翻译消耗 ATP 和 GTP。",
    },
    {
        "title": "核糖体的氨基酰-tRNA 结合位点",
        "source": "2005N24",
        "options": ["A 位", "P 位", "E 位", "核糖体结合位点"],
        "stems": [("在肽链合成中，原核生物核糖体结合新进入的氨基酰-tRNA 的位点是", ["A 位"])],
        "note": "A 位接纳新进入的氨基酰-tRNA，P 位结合肽酰-tRNA，E 位为出口。",
    },
    {
        "title": "肽酰转移酶与核酶",
        "source": "2017N25、2007N27",
        "options": ["氨基酰-tRNA 合成酶", "二硫键异构酶", "肽酰转移酶", "脱甲酰基酶", "脂肪酸", "RNA", "DNA", "多糖"],
        "stems": [
            ("由 RNA 发挥催化作用的酶是", ["肽酰转移酶"]),
            ("蛋白质生物合成时，肽酰转移酶的化学本质是", ["RNA"]),
        ],
        "note": "肽酰转移酶活性由核糖体大亚基 rRNA 承担，属于核酶。",
    },
    {
        "title": "翻译后形成和磷酸化的氨基酸",
        "source": "2000N23–24",
        "options": ["苏氨酸", "羟脯氨酸", "硒代半胱氨酸", "亮氨酸"],
        "stems": [
            ("蛋白质生物合成后经修饰形成的氨基酸是", ["羟脯氨酸"]),
            ("可以通过磷酸化修饰的氨基酸是", ["苏氨酸"]),
        ],
        "note": "羟脯氨酸由脯氨酸翻译后羟化形成；苏氨酸侧链羟基可被磷酸化。",
    },
    {
        "title": "常发生磷酸化的氨基酸残基",
        "source": "2018N25",
        "options": ["苏氨酸", "酪氨酸", "丝氨酸", "苯丙氨酸"],
        "stems": [("蛋白质中常发生磷酸化的氨基酸残基有", ["苏氨酸", "酪氨酸", "丝氨酸"])],
        "note": "丝氨酸、苏氨酸和酪氨酸均含可磷酸化的羟基。",
    },
    {
        "title": "蛋白质翻译后化学修饰",
        "source": "2005N25",
        "options": ["乙酰化", "甲基化", "形成二硫键", "形成硒代半胱氨酸"],
        "stems": [("蛋白质翻译后氨基酸的化学修饰方式有", ["乙酰化", "甲基化", "形成二硫键"])],
        "note": "硒代半胱氨酸可在翻译过程中直接掺入，不属于本题所列翻译后修饰。",
    },
    {
        "title": "热激蛋白的生理功能",
        "source": "2019N24",
        "options": ["参与蛋白质靶向运输", "促进新生多肽链的折叠", "作为酶参与蛋白质合成", "作为肽链合成起始的关键分子"],
        "stems": [("热激蛋白（热休克蛋白）的生理功能是", ["促进新生多肽链的折叠"])],
        "note": "热激蛋白属于分子伴侣，帮助新生多肽链正确折叠。",
    },
    {
        "title": "参与蛋白质折叠的分子",
        "source": "2008N27",
        "options": ["组蛋白", "伴侣蛋白", "细胞膜受体", "细胞骨架蛋白"],
        "stems": [("参与蛋白质折叠的蛋白质分子是", ["伴侣蛋白"])],
        "note": "分子伴侣为多肽链提供适宜的折叠环境，但不决定蛋白质一级结构。",
    },
    {
        "title": "蛋白质折叠与信号分子",
        "source": "2001N23–24",
        "options": ["泛素", "蛋白激酶", "逆转录酶", "热激（休克）蛋白"],
        "stems": [
            ("参与合成多肽链正确折叠的蛋白质是", ["热激（休克）蛋白"]),
            ("可作为信号传递分子开关的蛋白质是", ["蛋白激酶"]),
        ],
        "note": "热激蛋白参与折叠；蛋白激酶通过可逆磷酸化调控信号传递。",
    },
    {
        "title": "蛋白质生物合成的抑制与干扰",
        "source": "2013N26",
        "options": ["毒素", "泛素", "抗生素", "干扰素"],
        "stems": [("能够影响蛋白质生物合成的物质有", ["毒素", "抗生素", "干扰素"])],
        "note": "毒素、抗生素及干扰素可在不同环节影响翻译；泛素主要参与蛋白质降解标记。",
    },
]


def save_mind_map() -> None:
    if not MIND_MAP.is_file():
        raise FileNotFoundError(f"Missing supplied mind map: {MIND_MAP}")
    with Image.open(MIND_MAP) as image:
        image = image.convert("RGB")
        if image.width > 2200:
            height = round(image.height * 2200 / image.width)
            image = image.resize((2200, height), Image.Resampling.LANCZOS)
        IMAGE_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        image.save(IMAGE_OUTPUT, "WEBP", quality=88, method=6, exact=True)


def build_group(spec: dict, index: int) -> dict:
    original_options = spec["options"]
    if len(original_options) != len(set(original_options)):
        raise ValueError(f"Group {index} contains duplicate options")
    shuffled = original_options.copy()
    random.Random(30600 + LECTURE_NUMBER * 100 + index).shuffle(shuffled)
    if shuffled == original_options and len(shuffled) > 1:
        shuffled = shuffled[1:] + shuffled[:1]
    key_for = {label: chr(65 + position) for position, label in enumerate(shuffled)}
    stems = []
    for number, (text, answer_labels) in enumerate(spec["stems"], 1):
        if not set(answer_labels).issubset(key_for):
            raise ValueError(f"Group {index} stem {number} has an unknown answer")
        answers = [key_for[label] for label in answer_labels]
        stems.append({
            "number": number,
            "text": text.replace("（多选）", "").strip(),
            "answerRaw": "、".join(answers),
            "answer": answers,
            "answerMode": "多选" if len(answers) > 1 else "单选",
        })
    return {
        "id": f"bio-18-{index:02d}",
        "page": index,
        "title": spec["title"],
        "kind": "B",
        "kindLabel": "B型题",
        "options": [{"key": chr(65 + position), "label": label} for position, label in enumerate(shuffled)],
        "stems": stems,
        "sourceText": spec["source"],
        "reviewState": "已按《18翻译》、精编版生化合集与思维导图核对",
        "reviewIssues": [],
        "reviewNotes": [spec["note"]],
        "topic": TOPIC,
        "lectureIds": ["lecture-18"],
        "optionShuffleVersion": 1,
        "lectureEvidence": {
            "lectureId": "lecture-18",
            "lectureNumber": LECTURE_NUMBER,
            "lectureTitle": TITLE,
            "page": 1,
            "image": "biochemistry/lecture-pages/lecture-18-page-01.webp",
            "title": "第 18 讲《生化 翻译》· 思维导图第 275 页",
            "description": "翻译体系、能量、起始延长终止、翻译后加工及翻译干扰。点击可查看对应思维导图。",
            "method": "以《18翻译》真题解析和《精编版》生化合集翻译章节为主，结合思维导图逐项复核。",
        },
    }


def main() -> None:
    if not SOURCE_PDF.is_file():
        raise FileNotFoundError(f"Missing source PDF: {SOURCE_PDF}")
    save_mind_map()
    groups = [build_group(spec, index) for index, spec in enumerate(GROUPS, 1)]
    stem_count = sum(len(group["stems"]) for group in groups)
    if len(groups) != 12 or stem_count != 16:
        raise ValueError(f"Expected 12 groups and 16 stems, found {len(groups)} and {stem_count}")
    payload = {
        "meta": {
            "title": "生物化学第 18 讲题库",
            "sourceLabel": "生化第 18 讲《翻译》真题",
            "sourcePages": 12,
            "lectureCount": 1,
            "groupCount": len(groups),
            "stemCount": stem_count,
            "correctionGroupCount": 0,
            "generatedBy": "scripts/build_biochemistry_lecture18.py",
            "siteIntegrated": True,
            "lectureLinked": True,
            "answerNote": "完整收录《18翻译》14 个编号条目的 16 个题干；按知识点整理为 12 组，选项已重新打散，答案按精编版讲义逐项复核。",
        },
        "topics": ["全部", TOPIC, "综合"],
        "pages": [{"page": group["page"], "image": "", "topic": TOPIC, "searchText": group["title"]} for group in groups],
        "groups": groups,
        "lectures": [{"id": "lecture-18", "number": LECTURE_NUMBER, "title": TITLE, "pageCount": 1}],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
