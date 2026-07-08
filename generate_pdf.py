from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Frame, Table, TableStyle
import os
import datetime

FONT_PATH = r"C:\Windows\Fonts\simhei.ttf"
FONT_NAME = "SimHei"
pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))

W, H = A4
MARGIN = 2.54 * cm
PAGE_W = W - 2 * MARGIN
DARK_BG = HexColor("#1a1a2e")
DARK_SECONDARY = HexColor("#16213e")
ACCENT = HexColor("#e94560")
ACCENT2 = HexColor("#0f3460")
TEXT_LIGHT = HexColor("#e0e0e0")
TEXT_WHITE = white

OUTPUT = os.path.join(os.path.dirname(__file__), "项目介绍.pdf")


def draw_bg(c, color=DARK_BG):
    c.setFillColor(color)
    c.rect(0, 0, W, H, fill=1, stroke=0)


def draw_accent_line(c, y, w=60, color=ACCENT):
    c.setStrokeColor(color)
    c.setLineWidth(2)
    c.line(MARGIN, y, MARGIN + w, y)


def wrap_text(text, font_name, font_size, max_width):
    c = canvas.Canvas(None, pagesize=A4)
    c.setFont(font_name, font_size)
    lines = []
    for para in text.split("\n"):
        if not para:
            lines.append("")
            continue
        words = list(para)
        line = ""
        for ch in words:
            test = line + ch
            if c.stringWidth(test, font_name, font_size) > max_width:
                lines.append(line)
                line = ch
            else:
                line = test
        lines.append(line)
    return lines


def draw_cover(c):
    draw_bg(c, HexColor("#0f0f23"))
    for i in range(20):
        x = (i * 137 + 50) % int(W)
        y = (i * 211 + 30) % int(H)
        c.setFillColor(Color(1, 1, 1, 0.04))
        c.circle(x, y, 2, fill=1, stroke=0)

    c.setFillColor(HexColor("#e94560"))
    c.setFont(FONT_NAME, 44)
    title = "明日方舟狼人杀"
    tw = c.stringWidth(title, FONT_NAME, 44)
    c.drawString((W - tw) / 2, H - 180, title)

    c.setFont(FONT_NAME, 18)
    sub = "AI Edition"
    sw = c.stringWidth(sub, FONT_NAME, 18)
    c.setFillColor(HexColor("#a0a0b0"))
    c.drawString((W - sw) / 2, H - 230, sub)

    c.setStrokeColor(HexColor("#e94560"))
    c.setLineWidth(1)
    line_y = H - 260
    c.line(MARGIN + 60, line_y, W - MARGIN - 60, line_y)

    c.setFont(FONT_NAME, 14)
    tagline = "与 9 个 AI 对手展开一场明日方舟主题的狼人杀对决"
    tagw = c.stringWidth(tagline, FONT_NAME, 14)
    c.setFillColor(HexColor("#c0c0d0"))
    c.drawString((W - tagw) / 2, line_y - 40, tagline)

    features = [
        "单页 Web 应用 · 无需后端 · 纯前端运行",
        "AI 驱动 · 角色扮演 · 沉浸式策略博弈",
        "3D 动画 · 昼夜特效 · 完整狼人杀规则",
    ]
    c.setFont(FONT_NAME, 11)
    for i, ft in enumerate(features):
        fw = c.stringWidth(ft, FONT_NAME, 11)
        c.setFillColor(HexColor("#808090"))
        c.drawString((W - fw) / 2, line_y - 80 - i * 22, ft)

    c.setFont(FONT_NAME, 10)
    info = "作者: @不自动售货机 (Bilibili)"
    iw = c.stringWidth(info, FONT_NAME, 10)
    c.setFillColor(HexColor("#606070"))
    c.drawString((W - iw) / 2, 100, info)

    info2 = f"生成日期: {datetime.date.today().strftime('%Y-%m-%d')}"
    iw2 = c.stringWidth(info2, FONT_NAME, 10)
    c.drawString((W - iw2) / 2, 75, info2)


def draw_header(c, title):
    c.setFillColor(HexColor("#e94560"))
    c.setFont(FONT_NAME, 22)
    c.drawString(MARGIN, H - MARGIN - 20, title)
    c.setStrokeColor(HexColor("#e94560"))
    c.setLineWidth(1.5)
    c.line(MARGIN, H - MARGIN - 35, MARGIN + 80, H - MARGIN - 35)
    c.setStrokeColor(HexColor("#0f3460"))
    c.setLineWidth(0.5)
    c.line(MARGIN + 80, H - MARGIN - 35, W - MARGIN, H - MARGIN - 35)


def draw_page_number(c, num, total):
    c.setFillColor(HexColor("#606070"))
    c.setFont(FONT_NAME, 8)
    text = f"{num} / {total}"
    tw = c.stringWidth(text, FONT_NAME, 8)
    c.drawString(W - MARGIN - tw, MARGIN / 2, text)


def draw_footer(c):
    c.setStrokeColor(HexColor("#0f3460"))
    c.setLineWidth(0.5)
    c.line(MARGIN, MARGIN / 2 + 8, W - MARGIN, MARGIN / 2 + 8)


def draw_body_text(c, x, y, text, font_size=11, color=TEXT_LIGHT, line_spacing=18, max_width=None):
    if max_width is None:
        max_width = PAGE_W
    c.setFillColor(color)
    c.setFont(FONT_NAME, font_size)
    lines = []
    for para in text.split("\n"):
        if not para:
            lines.append("")
            continue
        chars = list(para)
        line = ""
        for ch in chars:
            test = line + ch
            if c.stringWidth(test, FONT_NAME, font_size) > max_width:
                if line:
                    lines.append(line)
                line = ch
            else:
                line = test
        lines.append(line)
    for line in lines:
        if y < MARGIN:
            return y
        c.drawString(x, y, line)
        y -= line_spacing
    return y + line_spacing


def draw_bullet(c, x, y, items, font_size=10, color=TEXT_LIGHT, line_spacing=20, bullet="  "):
    c.setFillColor(color)
    c.setFont(FONT_NAME, font_size)
    for item in items:
        if y < MARGIN:
            return y
        text = f"{bullet}{item}"
        chars = list(text)
        line = ""
        lines = []
        for ch in chars:
            test = line + ch
            if c.stringWidth(test, FONT_NAME, font_size) > PAGE_W - 10:
                if line:
                    lines.append(line)
                line = ch
            else:
                line = test
        lines.append(line)
        for ln in lines:
            if y < MARGIN:
                return y
            c.drawString(x + 5, y, ln)
            y -= line_spacing
        y -= 3
    return y


def draw_table(c, x, y, data, col_widths, font_size=9):
    nrows = len(data)
    ncols = len(col_widths)
    row_h = 22
    total_h = nrows * row_h
    if y - total_h < MARGIN:
        return y

    for ri, row in enumerate(data):
        ry = y - ri * row_h - 2
        if ri % 2 == 0:
            c.setFillColor(Color(0.09, 0.09, 0.18, 0.5))
        else:
            c.setFillColor(Color(0.13, 0.13, 0.24, 0.5))
        c.rect(x, ry - 2, sum(col_widths), row_h, fill=1, stroke=0)

    for ri, row in enumerate(data):
        ry = y - ri * row_h
        cx = x
        c.setFont(FONT_NAME, font_size)
        for ci, cell in enumerate(row):
            if ri == 0:
                c.setFillColor(ACCENT)
            else:
                c.setFillColor(TEXT_LIGHT)
            c.drawString(cx + 4, ry + 2, str(cell))
            cx += col_widths[ci]

    c.setStrokeColor(HexColor("#0f3460"))
    c.setLineWidth(0.5)
    c.rect(x, y - nrows * row_h, sum(col_widths), nrows * row_h, fill=0, stroke=1)

    return y - nrows * row_h - 15


def draw_section_title(c, y, text, font_size=14):
    c.setFillColor(ACCENT)
    c.setFont(FONT_NAME, font_size)
    c.drawString(MARGIN, y, text)
    c.setStrokeColor(HexColor("#e94560"))
    c.setLineWidth(0.8)
    c.line(MARGIN, y - 4, MARGIN + 50, y - 4)
    return y - 22


def main():
    TOTAL_PAGES = 9
    c = canvas.Canvas(OUTPUT, pagesize=A4)

    def new_page():
        c.showPage()

    def page_content(num):
        draw_bg(c)
        draw_page_number(c, num, TOTAL_PAGES)
        draw_footer(c)

    draw_cover(c)
    new_page()

    page_content(2)
    draw_header(c, "一、项目简介")
    y = H - MARGIN - 60
    texts = [
        "明日方舟狼人杀（AI版）是一款创新的单页 Web 应用，将经典桌游狼人杀与明日方舟角色主题相结合，由 AI 驱动 9 名电脑对手与你展开策略博弈。",
        "项目核心理念：",
        "只需一个浏览器和 API 密钥，即可随时随地享受与 AI 进行狼人杀的乐趣。不需要安装任何软件、不需要搭建后端服务器、不需要凑齐线下玩家。",
    ]
    for t in texts:
        y = draw_body_text(c, MARGIN, y, t, font_size=11, line_spacing=22)
        y -= 8

    y = draw_section_title(c, y - 5, "核心亮点")
    highlights = [
        "单个 HTML 文件即开即玩，零依赖零构建",
        "支持 DeepSeek / OpenAI / 任意兼容 API 的大语言模型",
        "9 个 AI 玩家各自拥有角色人格、策略思维和角色扮演能力",
        "完整的 10 人标准狼人杀规则，含守卫、女巫、猎人、预言家",
        "精美的 3D 卡牌翻转动画、昼夜特效、浮动背景卡牌",
        "完全本地运行，无需后端服务器",
    ]
    y = draw_bullet(c, MARGIN, y, highlights, font_size=10, line_spacing=20)
    new_page()

    page_content(3)
    draw_header(c, "二、技术栈")
    y = H - MARGIN - 60

    tech_data = [
        ["类别", "技术 / 工具"],
        ["编程语言", "JavaScript (ES6+), HTML5, CSS3"],
        ["框架", "无 — 纯原生单页应用"],
        ["后端", "无 — 完全浏览器端运行"],
        ["AI 大模型", "OpenAI 兼容 API（默认 DeepSeek）"],
        ["存储", "浏览器 localStorage"],
        ["构建工具", "无 — 无需打包、无需编译"],
        ["图片处理", "Python 3 辅助脚本 (gen_img.py)"],
        ["运行环境", "任意现代浏览器（Chrome / Firefox / Edge / Safari）"],
    ]
    cw = [120, PAGE_W - 120]
    y = draw_table(c, MARGIN, y, tech_data, cw, font_size=10)
    y -= 10

    y = draw_section_title(c, y, "架构特点")
    arch_items = [
        "整个应用仅由一个 index.html 文件构成（约 2200 行），CSS 和 JavaScript 全部内嵌其中",
        "浏览器直接调用 OpenAI 兼容 API，AI 响应在客户端解析和执行",
        "无需任何服务端部署，打开 HTML 文件即可运行",
        "角色形象、游戏状态、对话历史均在内存中维护，配置信息持久化到 localStorage",
    ]
    y = draw_bullet(c, MARGIN, y, arch_items)
    new_page()

    page_content(4)
    draw_header(c, "三、功能特色")
    y = H - MARGIN - 60

    sections = [
        ("  游戏功能", [
            "10 人标准狼人杀：3 狼人 + 预言家 + 女巫 + 猎人 + 守卫 + 3 村民",
            "完整的昼夜循环：夜间行动（守卫→狼人→预言家→女巫）→ 白天发言 → 投票 → 处决",
            "守卫不能连续两晚守护同一目标，女巫不可自救，女巫解药与守卫守护冲突规则",
            "猎人被女巫毒杀时无法发动技能",
            "首夜保护机制：玩家第一晚不会死亡",
            "平票 PK 发言及第二轮投票",
        ]),
        ("  AI 智能", [
            "每位 AI 玩家拥有独立人格和策略，根据角色身份制定行动方案",
            "AI 发言需遵循身份约束：狼人不可自曝身份，神职不可泄漏查验信息",
            "AI 维护对其他玩家的信任/怀疑矩阵，动态调整策略",
            "投票阶段 AI 综合分析发言内容、投票倾向和夜间信息",
        ]),
        ("  用户界面", [
            "3D 卡牌翻转动画 — 身份揭晓仪式感十足",
            "日夜交替色彩滤镜 — 白天暖色、夜晚冷色",
            "浮动背景卡牌 — 增强沉浸感",
            "游戏日志抽屉 — 随时查看历史记录",
            "桌面阅读模式 — 显示投票压力和倾向",
            "Toast 消息提示 — 关键事件即时反馈",
            "终局总结回顾 — 夜间行动、投票流向、转折点分析",
        ]),
    ]
    for title, items in sections:
        y = draw_section_title(c, y, title)
        y = draw_bullet(c, MARGIN, y, items)
        y -= 5
    new_page()

    page_content(5)
    draw_header(c, "四、架构设计")
    y = H - MARGIN - 60

    texts = [
        "游戏采用事件驱动架构，核心状态机控制游戏流程。每次阶段转换由 JavaScript 异步函数编排，AI 调用通过 Promise 链串行执行。",
    ]
    for t in texts:
        y = draw_body_text(c, MARGIN, y, t, font_size=11, line_spacing=22)
        y -= 5

    y = draw_section_title(c, y, "游戏流程")
    flow_data = [
        ["阶段", "说明"],
        ["初始化", "分配角色、明日方舟角色、AI 人格"],
        ["摸牌仪式", "3D 卡牌翻转展示玩家身份"],
        ["夜晚", "守卫守护 → 狼人杀人 → 预言家查验 → 女巫救/毒"],
        ["死亡宣告", "公布夜间死亡结果，遗言"],
        ["白天发言", "按顺序发言，讨论投票意向"],
        ["投票处决", "投票 → 平票 PK → 处决 → 猎人开枪"],
        ["胜负判定", "狼人 / 好人阵营是否达成胜利条件"],
        ["循环", "未结束则进入下一夜 → 白天"],
    ]
    cw = [80, PAGE_W - 80]
    y = draw_table(c, MARGIN, y, flow_data, cw, font_size=10)
    y -= 10

    y = draw_section_title(c, y, "AI 集成架构")
    ai_items = [
        "buildMsgs() — 构建包含完整游戏上下文的系统提示 + 用户提示",
        "callDeepSeek() — 调用 OpenAI 兼容 API，支持流式/非流式",
        "aiJson() — 解析 AI 的 JSON 格式响应（行动决策或发言内容）",
        "每个 AI 调用均包含角色身份、历史发言、存活状态、信任矩阵等上下文",
    ]
    y = draw_bullet(c, MARGIN, y, ai_items)
    new_page()

    page_content(6)
    draw_header(c, "五、游戏规则")
    y = H - MARGIN - 60

    y = draw_section_title(c, y, "角色配置")
    role_data = [
        ["阵营", "角色", "人数", "技能"],
        ["狼人", "狼人", "3", "每晚共同选择一名玩家击杀"],
        ["神职", "预言家", "1", "每晚查验一名玩家身份阵营"],
        ["神职", "女巫", "1", "1 瓶解药救活死者，1 瓶毒药毒杀玩家"],
        ["神职", "猎人", "1", "被处决或夜间被杀时可开枪带走一人"],
        ["神职", "守卫", "1", "每晚守护一名玩家免于被狼人杀害"],
        ["村民", "村民", "3", "白天投票处决狼人"],
    ]
    cw = [60, 80, 50, PAGE_W - 190]
    y = draw_table(c, MARGIN, y, role_data, cw, font_size=10)
    y -= 5

    y = draw_section_title(c, y, "明日方舟角色")
    char_data = [
        ["编号", "角色", "说明"],
        ["1", "博士", "罗德岛的指挥官"],
        ["2", "祭司", "神秘的祭祀者"],
        ["3", "阿米娅", "罗德岛的公开领袖"],
        ["4", "凯尔希", "罗德岛的医疗主管"],
        ["5", "维什戴尔", "雇佣兵狙击手"],
        ["6", "黍", "岁家代理人"],
        ["7", "特蕾西娅", "萨卡兹的魔王"],
        ["8", "能天使", "企鹅物流的快乐信使"],
        ["9", "Mon3tr", "凯尔希的召唤物"],
        ["10", "德克萨斯", "企鹅物流的资深干员"],
    ]
    cw = [40, 80, PAGE_W - 120]
    y = draw_table(c, MARGIN, y, char_data, cw, font_size=10)
    new_page()

    page_content(7)
    draw_header(c, "六、AI 设计亮点")
    y = H - MARGIN - 60

    y = draw_section_title(c, y, "Prompt 工程")
    prompt_items = [
        "系统提示严格定义身份和规则，禁止 AI 泄露私人信息",
        "狼人阵营知道同伴身份，好人阵营只知道自己的身份",
        "AI 发言内容限制在合理游戏讨论范围内，排除场外信息",
        "每个决策要求 AI 先进行内部推理（reasoning），再输出最终决定",
        "通过 JSON 结构化输出确保程序可解析",
    ]
    y = draw_bullet(c, MARGIN, y, prompt_items)
    y -= 5

    y = draw_section_title(c, y, "信息安全")
    security_items = [
        "狼人不能声称自己是好人阵营的神职角色",
        "AI 不能泄露自己的真实身份（狼人不能自曝）",
        "预言家不能伪造查验结果",
        "死亡玩家不能发言或泄露身份信息",
    ]
    y = draw_bullet(c, MARGIN, y, security_items)
    y -= 5

    y = draw_section_title(c, y, "信任/怀疑矩阵")
    matrix_items = [
        "每个 AI 维护对其他存活玩家的信任度和怀疑度数值",
        "矩阵影响 AI 的发言策略和投票决策",
        "夜间行动信息、白天发言内容、投票模式共同驱动矩阵更新",
        "AI 会引用其他玩家的言行作为怀疑或信任的依据",
    ]
    y = draw_bullet(c, MARGIN, y, matrix_items)
    new_page()

    page_content(8)
    draw_header(c, "七、目录结构")
    y = H - MARGIN - 60

    file_data = [
        ["文件", "说明"],
        ["index.html", "主应用文件（约 2210 行，含全部 HTML/CSS/JS）"],
        ["gen_img.py", "Python 辅助脚本（base64 编码图片）"],
        ["1.png ~ 10.png", "10 名明日方舟角色头像"],
        ["系统.png", "系统 / 默认头像"],
        ["村民.png", "村民角色卡牌"],
        ["狼人.png", "狼人角色卡牌"],
        ["猎人.png", "猎人角色卡牌"],
        ["女巫.png", "女巫角色卡牌"],
        ["守卫.png", "守卫角色卡牌"],
        ["预言家.png", "预言家角色卡牌"],
    ]
    cw = [100, PAGE_W - 100]
    y = draw_table(c, MARGIN, y, file_data, cw, font_size=10)
    y -= 10

    y = draw_section_title(c, y, "项目仓库")
    repo_items = [
        "GitHub: github.com/rarararar-max/Langrensha-mingrifangzhou",
        "Bilibili: @不自动售货机 (space.bilibili.com/599298)",
    ]
    y = draw_bullet(c, MARGIN, y, repo_items)
    new_page()

    page_content(9)
    draw_header(c, "八、使用说明")
    y = H - MARGIN - 60

    y = draw_section_title(c, y, "快速开始")
    steps = [
        "1. 打开 index.html 文件（任意现代浏览器）",
        "2. 在设置页面输入 API Key 和模型参数",
        "3. 支持 DeepSeek / OpenAI / 自定义端点",
        "4. 可选择自定义角色头像和人格描述",
        "5. 点击「开始游戏」即可体验",
        "6. 通过摸牌仪式查看自己的身份",
        "7. 跟随游戏提示完成每个阶段的操作",
    ]
    y = draw_bullet(c, MARGIN, y, steps)
    y -= 10

    y = draw_section_title(c, y, "配置说明")
    config_items = [
        "AI 模型: 默认 deepseek-v4-flash，可切换任意模型",
        "API 地址: 默认 api.deepseek.com，支持自定义",
        "温度参数: 控制 AI 输出随机性（0.1 ~ 1.0）",
        "角色定制: 可在设置页面修改角色名称、头像、人格描述",
        "所有配置自动保存至浏览器 localStorage",
    ]
    y = draw_bullet(c, MARGIN, y, config_items)
    y -= 10

    y = draw_section_title(c, y, "环境要求")
    env_items = [
        "任意现代浏览器（Chrome 90+ / Firefox 88+ / Edge 90+ / Safari 14+）",
        "有效的 OpenAI 兼容 API 密钥",
        "可选的网络连接（用于调用 AI API）",
    ]
    draw_bullet(c, MARGIN, y, env_items)

    c.save()
    print(f"PDF generated: {OUTPUT}")


if __name__ == "__main__":
    main()
