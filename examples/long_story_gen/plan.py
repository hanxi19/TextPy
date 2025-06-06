import logging
import json

from textpy import code, text

CACHE_DIR = "./cache"

metadata = {
    "main_character": "张三",
    "main_character_description": "出身贫寒，但是修炼天赋极高，性格坚毅不拔，渴望通过修炼改变命运。",
    "main_setting": "一个充满修仙者的世界，修炼者通过吸收天地灵气来提升自己的修为，争夺资源和地位。",
    "characters": [],
    "settings":[]
}

outline_template = {
    "第1卷": {
        "description": "<宗门名称>",
        "contents": {
            "第1部": {
                "description": "<主角名字>加入<宗门名称>",
                "contents": {
                    "第1章": {
                        "description": "张三在家乡的贫困生活中，渴望改变命运，决定前往宗门。",
                        "caracters": ["张三","张三的父亲","张三的母亲","地主","..."],
                        "settings": ["张三的家乡","张三的家","地主的庄园","..."],
                        "contents": {
                            "第1节": {
                                "description": "张三家里的贫困生活",
                                "caracters": ["张三","张三的父亲","张三的母亲","地主","..."],
                                "settings": ["张三的家乡","张三的家","地主的庄园","..."],
                                "contents": {
                                    "第1段": "张三的家境贫寒。",
                                    "第2段": "父母辛苦劳作。",
                                    "第3段": "地主的压迫让张三感到愤怒。",
                                    "第4段": "...",
                                }
                            }
                        }
                    }
                }
            },
            "第2部": {
                "description": "<主角名字>因为弱小受到打压",
                "contents": {}
            },
            "第3部": {
                "description": "<主角名字>被强迫接收危险的任务，离开<宗门名称>完成任务",
                "contents": {}
            },
            "第4部": {
                "description": "<主角名字>在外界偶遇机缘。",
                "contents": {}
            },
            "第5部": {
                "description": "<主角名字>疯狂修炼，实力大涨",
                "contents": {}
            },
            "第6部": {
                "description": "<主角名字>回到<宗门名称>，打败了原先打压他的人，受到尊敬",
                "contents": {}
            },
            "第7部": {
                "description": "<主角名字>决定离开宗门，寻找更大的机缘",
                "contents": {}
            }
        }
    },
}

@text(cache=CACHE_DIR)
# 你是一名长篇小说大纲生成助手，专注于协助用户分阶段、分层级地生成完整的长篇小说大纲。
# metadata包含小说的主要角色、背景设定等元数据，用于生成更具针对性的内容。
# parent_desc前一层级的概要
# context上文内容，如果context不为空，则当前要生成的内容必须与context衔接自然。
# outline当前已生成的大纲信息。
# characters当前层级的角色信息，为空时则忽略，不为空时，必须根据characters中的角色生成剧情。
# settings当前层级的设定信息，为空时则忽略，不为空时，必须根据settings中的设定生成剧情。
# 必须按照metadata中提供的设定来生成内容，确保与小说整体风格和设定一致。
# 例如，若上一层级（parent_desc）概要为“张三加入宗门”，则本层级可细化为“张三离开家乡”“张三在路上遇到老者”“老者传授张三修炼知识”“张三到达宗门”“张三参加考核”等，将“张三加入宗门”拆解为若干具体情节概要。
# 每一层级的内容仅需比上一层级更细致，生成概要而非具体情节，不需展开详细描写。
# 只能生成与当前parent_desc相关的内容，不能涉及到其它层级（outline）的内容。
# 确保每一层级内容均与上一层级概要紧密相关。
# 输出格式为：当前层级下所有子内容概要的列表，每个元素为一个概要字符串，仅返回该列表，不包含其他说明或格式，列表长度为3到5，每个元素字数在15到20字之间。
# 尽量拉长每个子内容的时间跨度，避免过于密集的情节安排导致下一层级内容生成重复
# 如对于“张三加入大大宗”这个层级，不应该直接生成“张三被大大宗山门震撼”，而是生成“张三历经艰难险阻，终于抵达大大宗山门，被其宏伟气势所震撼”
# 对于“张三历经艰难险阻，终于抵达大大宗山门，被其宏伟气势所震撼”，应该先写“历经艰难险阻”，再写“抵达大大宗山门”，再写“被其宏伟气势所震撼”，而不是直接给一个“山门震撼”
# 必须在输入中添加{metadata}，{context}，{parent_desc},{characters}，{settings}等格式的变量，以便后续将实际值传入。
def plot(*, metadata:dict, parent_desc:str, context:str, characters:dict|None, settings:dict|None, outline:dict) -> str:...

@text(cache=CACHE_DIR)
# 你是一个小说角色生成助手，专注于根据任务和元数据生成小说角色以及详细描述。
# metadata包含小说的主要角色、背景设定等元数据，用于生成更具针对性的内容。
# context当前上下文信息，前一层级的概要。
# 必须按照metadata中提供的设定来生成内容，确保与小说整体风格和设定一致。
# 你需要根据context中的信息，自行决定是否需要生成新的角色或对现有角色进行扩展。
# 如“张三在家乡的贫困生活中”，你可以添加如下角色
# - 张狗蛋：张三的父亲，辛勤劳作，支持张三的决定。
# - 李花：张三的母亲，温柔善良，关心张三的未来。
# - 王富贵：张三家乡的地主，压迫张三一家，成为张三修炼的动力。
# 生成的角色需要保证能够与当前情节紧密相关，让剧情顺利推进，并且符合小说的整体设定和风格。
# 同时筛选metadata中已有的角色，确保它们与当前情节相关。
# 输出格式为：一个字典，包含这段剧情出场的所有角色信息，键为角色名称，值为一句话角色描述，不超过20字。
# 必须在输入中添加{metadata}，{context}，{characters}，{settings}等格式的变量，用于标识变量的位置，以便后续将实际值传入。
def character(*, metadata:dict, context:str) -> dict:...

@text(cache=CACHE_DIR)
# 你是一个小说设定生成助手，专注于根据任务和元数据生成小说设定。
# metadata包含小说的主要角色、背景设定等元数据，用于生成更具针对性的内容。
# context当前上下文信息，前一层级的概要。
# 必须按照metadata中提供的设定来生成内容，确保与小说整体风格和设定一致。
# 你需要根据context中的信息，自行决定是否需要生成新的设定或对现有设定进行扩展。
# 如“在外界偶遇机缘”，你可以添加如下设定
# - 九阳真经：传说中的顶级功法，能够快速提升修为，淬炼肉身。
# - 紫霄剑：宗门镇派法宝，威力无穷，只有宗门天才弟子方可掌控。
# - 天机秘境：每隔十年开启一次，内藏无数机缘与危险，是修士历练与寻宝的圣地。
# - 灵脉洞天：蕴含丰富天地灵气的修炼宝地，常为各大势力争夺。
# - 乾坤袋：储物法宝，可装载大量物品，是修士必备之物。
# - 破虚符：一次性消耗类法宝，可在危急时刻撕裂空间逃生。
# 生成的设定需要保证能够与当前情节紧密相关，让剧情顺利推进，并且符合小说的整体设定和风格。
# 输出格式为：一个字典，键为名称，值为一句话描述，包含这段剧情所需要的地点、物品、功法、秘境等与修仙世界相关的元素，而不是对场景的总结，不超过20字。
# 必须在输入中添加{metadata}，{context}等格式的变量，用于标识变量的位置，以便后续将实际值传入。
def setting(*, metadata:dict, context:str) -> dict:...



