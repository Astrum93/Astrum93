"""Astrum93 프로필 README용 '앱 화면' SVG 생성기.

사용법: python3 -I gen_profile_svgs.py <출력 폴더> <아바타 PNG> <스토어 아이콘 폴더(user.png, partner.png)> [dark|light]
  다크: python3 scripts/gen_profile_svgs.py assets scripts/src/avatar.png scripts/src dark
  라이트: python3 scripts/gen_profile_svgs.py assets/light scripts/src/avatar.png scripts/src light
  README는 <picture>로 GitHub 테마(라이트/다크)에 맞는 세트를 보여준다.
(아바타는 SVG 안에 base64로 넣는다. README의 <img>로 띄운 SVG는 외부 이미지를 불러오지 못하기 때문)
"""
import base64
import os
import re
import sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
with open(sys.argv[2], "rb") as f:
    AVATAR = "data:image/png;base64," + base64.b64encode(f.read()).decode()

W = 420
THEME = sys.argv[4] if len(sys.argv) > 4 else "dark"
DARK = {
    "bg": "#0F1218",
    "surface": "#161A22",
    "surface2": "#1E2330",
    "border": "#262C3A",
    "notif": "#232838",
    "text": "#EEF0F6",
    "sub": "#98A1B3",
    "faint": "#5E677A",
    "purple": "#8B7CF6",
    "teal": "#2DD4BF",
    "pink": "#F472B6",
    "amber": "#FBBF24",
    "green": "#34D399",
    "red": "#F87171",
    "blue": "#60A5FA",
}
# GitHub 라이트 테마(흰 배경)에서 읽히도록 카드는 밝게, 강조색은 한 톤 진하게
LIGHT = {
    "bg": "#F2F4F7",
    "surface": "#FFFFFF",
    "surface2": "#F1F3F7",
    "border": "#D0D7DE",
    "notif": "#F6F8FA",
    "text": "#1F2328",
    "sub": "#59636E",
    "faint": "#8C959F",
    "purple": "#6D5BD0",
    "teal": "#0F9488",
    "pink": "#DB2777",
    "amber": "#B45309",
    "green": "#15803D",
    "red": "#DC2626",
    "blue": "#2563EB",
}
C = LIGHT if THEME == "light" else DARK
FONT = ("Pretendard, 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', "
        "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif")


def text_w(s, size):
    """대략적인 글자 폭 계산 (칩 너비용)."""
    w = 0.0
    for ch in s:
        if ord(ch) > 0x3000:
            w += size * 0.98
        elif ch == " ":
            w += size * 0.30
        elif ch.isupper():
            w += size * 0.66
        else:
            w += size * 0.56
    return w


def svg(h, body, defs="", style=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">
<style>
  text {{ font-family: {FONT}; }}
  .t {{ fill: {C['text']}; }}
  .s {{ fill: {C['sub']}; }}
  .f {{ fill: {C['faint']}; }}
  .b {{ font-weight: 700; }}
{style}
</style>
<defs>{defs}</defs>
{body}
</svg>
"""


def panel(h, rx=22):
    return (f'<rect x="1" y="1" width="{W-2}" height="{h-2}" rx="{rx}" '
            f'fill="{C["surface"]}" stroke="{C["border"]}" stroke-width="1.5"/>')


def chip(x, y, label, color, size=11):
    w = text_w(label, size) + 18
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="20" rx="10" fill="{color}" fill-opacity="0.16" '
            f'stroke="{color}" stroke-opacity="0.45"/>'
            f'<text x="{x + w/2:.1f}" y="{y + 14}" font-size="{size}" text-anchor="middle" fill="{color}" '
            f'font-weight="600">{label}</text>', w)


def chips(x, y, items, gap=6, max_x=None):
    out, cx, cy = [], x, y
    for label, color in items:
        w = text_w(label, 11) + 18
        if max_x and cx + w > max_x:
            cx, cy = x, cy + 26
        s, w = chip(cx, cy, label, color)
        out.append(s)
        cx += w + gap
    return "".join(out)


def _save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)


# --- 폰 프레임 ------------------------------------------------------------------
# README에서 모든 조각을 <br>로 이어 붙이고 img에 align="top"을 주면 조각 사이 틈이 0이 된다.
# 그래서 각 조각이 폰 몸체(베젤)와 화면 배경을 함께 그리면, 이어 붙였을 때 폰 한 대가 된다.
# 폰 몸체: 라이트 테마는 검정 폰, 다크 테마는 GitHub 다크 배경(#0d1117)과 구분되도록 티타늄 그레이
BODY, EDGE = ("#111318", "#2B2F38") if THEME == "light" else ("#252A35", "#4A5163")
BZ = 10                               # 베젤 두께
PADX = BZ + 12                        # 화면 안쪽 여백까지 포함한 카드 시작 x
WO = W + PADX * 2                     # 폰 전체 폭 (464)
R_OUT, R_SCR = 56, 46                 # 바깥 / 화면 모서리 반경


def _inner(content, x, y):
    m = re.match(r'<svg xmlns="http://www.w3.org/2000/svg" width="(\d+)" height="([\d.]+)" viewBox="0 0 \d+ [\d.]+">', content)
    h = float(m.group(2))
    return content.replace(m.group(0), f'<svg x="{x}" y="{y}" width="{W}" height="{h:g}" viewBox="0 0 {W} {h:g}">', 1), h


def _outer(H, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{WO}" height="{H:g}" viewBox="0 0 {WO} {H:g}">'
            f'{body}</svg>\n')


def frame(content, kind="mid", pad=(6, 6)):
    """카드 SVG를 폰 화면 한 줄로 감싼다. kind: top(폰 윗부분) / mid."""
    if kind == "top":
        pt, pb = BZ + 2, pad[1]
        inner, h = _inner(content, PADX, pt)
        H = pt + h + pb
        shell = (f'<path d="M0 {H} V{R_OUT} Q0 0 {R_OUT} 0 H{WO-R_OUT} Q{WO} 0 {WO} {R_OUT} V{H} Z" fill="{BODY}"/>'
                 f'<path d="M0.75 {H} V{R_OUT} Q0.75 0.75 {R_OUT} 0.75 H{WO-R_OUT} Q{WO-0.75} 0.75 {WO-0.75} {R_OUT} V{H}" '
                 f'fill="none" stroke="{EDGE}" stroke-width="1.5"/>'
                 f'<path d="M{BZ} {H} V{BZ+R_SCR} Q{BZ} {BZ} {BZ+R_SCR} {BZ} H{WO-BZ-R_SCR} Q{WO-BZ} {BZ} {WO-BZ} {BZ+R_SCR} V{H} Z" '
                 f'fill="{C["bg"]}"/>')
    else:
        pt, pb = pad
        inner, h = _inner(content, PADX, pt)
        H = pt + h + pb
        shell = (f'<rect width="{WO}" height="{H}" fill="{BODY}"/>'
                 f'<path d="M0.75 0 V{H} M{WO-0.75} 0 V{H}" stroke="{EDGE}" stroke-width="1.5"/>'
                 f'<rect x="{BZ}" width="{WO-2*BZ}" height="{H}" fill="{C["bg"]}"/>')
    return _outer(H, shell + inner)


def write(name, content, kind="mid", pad=(6, 6)):
    _save(name, frame(content, kind, pad))


# 1. AppBar + 상태바 (폰 윗부분) ----------------------------------------------
h = 108
body = f"""
<rect x="160" y="6" width="100" height="30" rx="15" fill="#000"/>
<text x="34" y="32" font-size="15" class="t b">9:41</text>
<g fill="{C['text']}">
  <rect x="318" y="26" width="3" height="6" rx="1"/><rect x="323" y="23" width="3" height="9" rx="1"/>
  <rect x="328" y="20" width="3" height="12" rx="1"/><rect x="333" y="17" width="3" height="15" rx="1"/>
</g>
<path d="M343 22 q8 -7 16 0 M346 26 q5 -4 10 0" stroke="{C['text']}" stroke-width="2" fill="none" stroke-linecap="round"/>
<circle cx="351" cy="30" r="1.8" fill="{C['text']}"/>
<rect x="366" y="19" width="24" height="12" rx="3.5" fill="none" stroke="{C['text']}" stroke-opacity="0.6" stroke-width="1.2"/>
<rect x="368" y="21" width="17" height="8" rx="2" fill="{C['green']}"/>
<rect x="391" y="23" width="2" height="4" rx="1" fill="{C['text']}" fill-opacity="0.6"/>

<g stroke="{C['text']}" stroke-width="2.4" stroke-linecap="round">
  <line x1="28" y1="72" x2="46" y2="72"/><line x1="28" y1="79" x2="46" y2="79"/><line x1="28" y1="86" x2="40" y2="86"/>
</g>
<text x="62" y="86" font-size="22" class="t b">Astrum93</text>
<text x="166" y="86" font-size="13" class="f">.dev</text>
<circle cx="346" cy="78" r="8" fill="none" stroke="{C['text']}" stroke-width="2.2"/>
<line x1="352" y1="84" x2="358" y2="90" stroke="{C['text']}" stroke-width="2.4" stroke-linecap="round"/>
<path d="M378 86 v-7 a8 8 0 0 1 16 0 v7 l2 3 h-20 z" fill="none" stroke="{C['text']}" stroke-width="2.2" stroke-linejoin="round"/>
<circle cx="386" cy="92" r="2" fill="{C['text']}"/>
<circle cx="394" cy="70" r="4.5" fill="{C['red']}">
  <animate attributeName="r" values="4.5;6;4.5" dur="1.6s" repeatCount="indefinite"/>
</circle>
"""
write("appbar.svg", svg(h, body), kind="top")

# 배너의 "NOW CODING" 문구 (scripts/update_now_coding.py가 매일 갱신). 음파 그림(x=210~)과 겹치지 않게 자른다.
_now_path = os.path.join(sys.argv[3], "now_coding.txt")
NOW_CODING = open(_now_path, encoding="utf-8").read().strip() if os.path.exists(_now_path) else "music_is_life"
while text_w(NOW_CODING, 15) * 1.08 > 180 and len(NOW_CODING) > 4:
    NOW_CODING = NOW_CODING[:-2].rstrip() + "…"
    NOW_CODING = NOW_CODING.replace("……", "…")
NOW_CODING = NOW_CODING.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# 2. 프로필 -----------------------------------------------------------------
h = 300
lines = [
    "Flutter로 구조가 탄탄한 앱을 만들어요",
    "GetX · Bloc · Riverpod 다 써봤어요",
    "Clean Architecture를 좋아합니다",
    "Music is Life 🎧",
]
n = len(lines)
typing = ""
for i, line in enumerate(lines):
    s = i / n
    seg = 1 / n
    a, b, c = s, s + seg * 0.35, s + seg * 0.92
    if i == 0:
        kt = f"0;{b:.4f};{c:.4f};{c+0.0001:.4f};1"
        vals = "0;300;300;0;0"
    elif i == n - 1:
        kt = f"0;{a:.4f};{b:.4f};{c:.4f};1"
        vals = "0;0;300;300;0"
    else:
        kt = f"0;{a:.4f};{b:.4f};{c:.4f};{c+0.0001:.4f};1"
        vals = "0;0;300;300;0;0"
    # 애니메이션을 지원하지 않는 렌더러(예: GitHub 모바일 앱)에서는 기본값이 그대로 보인다.
    # 그래서 기본값은 "첫 문구만 보임"으로 두고, 애니메이션이 될 때만 문구가 바뀌게 한다.
    base_w = 300 if i == 0 else 0
    typing += f"""
<clipPath id="tc{i}"><rect x="52" y="214" width="{base_w}" height="26">
  <animate attributeName="width" values="{vals}" keyTimes="{kt}" dur="{n*3.2}s" repeatCount="indefinite"/>
</rect></clipPath>"""


def _type_text(i, line):
    a, c = i / n, i / n + (1 / n) * 0.92
    if i == 0:
        vis, op = f'values="1;0" keyTimes="0;{c:.4f}"', 1
    else:
        vis, op = f'values="0;1;0" keyTimes="0;{a:.4f};{c:.4f}"', 0
    # clip을 지원하지 않는 렌더러에서도 문구가 겹치지 않도록 opacity로 한 번 더 보이고 숨긴다
    return (f'<text x="52" y="232" font-size="14.5" class="t" opacity="{op}" clip-path="url(#tc{i})">{line}'
            f'<animate attributeName="opacity" {vis} calcMode="discrete" dur="{n*3.2}s" repeatCount="indefinite"/></text>')


type_texts = "".join(_type_text(i, line) for i, line in enumerate(lines))
defs = f"""
<linearGradient id="banner" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="{C['purple']}"/><stop offset="0.55" stop-color="#5B5BD6"/><stop offset="1" stop-color="{C['teal']}"/>
</linearGradient>
<linearGradient id="avatar" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="{C['pink']}"/><stop offset="1" stop-color="{C['purple']}"/>
</linearGradient>
<clipPath id="top"><rect x="1" y="1" width="{W-2}" height="120" rx="22"/></clipPath>
<clipPath id="avatarClip"><circle cx="70" cy="104" r="37"/></clipPath>
{typing}
"""
wave = ""
for k in range(14):
    x = 210 + k * 14
    hh = [18, 30, 22, 40, 26, 34, 16, 28, 38, 20, 32, 24, 36, 18][k]
    wave += (f'<rect x="{x}" y="{60-hh/2}" width="6" height="{hh}" rx="3" fill="#fff" fill-opacity="0.28">'
             f'<animate attributeName="height" values="{hh};{hh*0.4:.0f};{hh}" dur="{0.9 + (k % 4) * 0.25:.2f}s" repeatCount="indefinite"/>'
             f'<animate attributeName="y" values="{60-hh/2};{60-hh*0.2:.0f};{60-hh/2}" dur="{0.9 + (k % 4) * 0.25:.2f}s" repeatCount="indefinite"/>'
             f'</rect>')
body = panel(h) + f"""
<g clip-path="url(#top)">
  <rect x="0" y="0" width="{W}" height="96" fill="url(#banner)"/>
  {wave}
  <text x="24" y="28" font-size="12" fill="#fff" fill-opacity="0.85" font-weight="600">♪ NOW CODING</text>
  <text x="24" y="47" font-size="15" fill="#fff" font-weight="700">{NOW_CODING}</text>
</g>
<circle cx="70" cy="104" r="42" fill="{C['surface']}"/>
<circle cx="70" cy="104" r="37" fill="url(#avatar)"/>
<image x="33" y="67" width="74" height="74" clip-path="url(#avatarClip)" preserveAspectRatio="xMidYMid slice" href="{AVATAR}"/>
<circle cx="100" cy="130" r="8" fill="{C['surface']}"/>
<circle cx="100" cy="130" r="5.5" fill="{C['green']}">
  <animate attributeName="fill-opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite"/>
</circle>

<rect x="282" y="112" width="116" height="34" rx="17" fill="{C['purple']}"/>
<text x="340" y="134" font-size="14" text-anchor="middle" fill="#fff" font-weight="700">+ 팔로우</text>

<text x="24" y="176" font-size="23" class="t b">나정민</text>
<text x="96" y="176" font-size="14" class="s">@Astrum93</text>
<text x="24" y="198" font-size="13.5" class="s">Flutter Developer · 기록하는 개발자</text>

<rect x="24" y="212" width="{W-48}" height="30" rx="10" fill="{C['surface2']}"/>
<text x="36" y="232" font-size="14.5" fill="{C['purple']}" font-weight="700">›</text>
{type_texts}

<g font-size="12">
  <text x="70" y="270" text-anchor="middle" font-size="18" class="t b">40+</text>
  <text x="70" y="288" text-anchor="middle" class="s">Repositories</text>
  <line x1="140" y1="258" x2="140" y2="288" stroke="{C['border']}"/>
  <text x="210" y="270" text-anchor="middle" font-size="18" class="t b">1년 10개월</text>
  <text x="210" y="288" text-anchor="middle" class="s">실무 경력</text>
  <line x1="280" y1="258" x2="280" y2="288" stroke="{C['border']}"/>
  <text x="350" y="270" text-anchor="middle" font-size="18" class="t b">2023~</text>
  <text x="350" y="288" text-anchor="middle" class="s">Flutter</text>
</g>
"""
write("profile.svg", svg(h, body, defs))

# 3. 섹션 헤더 --------------------------------------------------------------
def section(name, title, action):
    h = 44
    body = f"""
<text x="8" y="29" font-size="17" class="t b">{title}</text>
<text x="{W-10}" y="29" font-size="13" text-anchor="end" fill="{C['purple']}" font-weight="600">{action} ›</text>
"""
    write(name, svg(h, body))


section("section-apps.svg", "📌 대표 프로젝트", "전체 레포")
section("section-lab.svg", "🧪 실험실", "더 보기")
section("section-career.svg", "💼 경력", "포트폴리오")
section("section-cert.svg", "🎖️ 자격 · 수상", "포트폴리오")

# 4. 앱 카드 ----------------------------------------------------------------
def app_card(name, title, badge, subtitle, tags, icon_grad, icon_body, extra=""):
    h = 112
    defs = (f'<linearGradient id="ig" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{icon_grad[0]}"/><stop offset="1" stop-color="{icon_grad[1]}"/>'
            f'</linearGradient>')
    bw = text_w(badge, 11) + 14 if badge else 0
    tx = 92 + text_w(title, 17) + 8
    badge_svg = (f'<rect x="{tx:.0f}" y="21" width="{bw:.0f}" height="18" rx="9" fill="{C["green"]}" fill-opacity="0.18"/>'
                 f'<text x="{tx + bw/2:.0f}" y="34" font-size="11" text-anchor="middle" fill="{C["green"]}" font-weight="700">{badge}</text>'
                 if badge else "")
    body = panel(h, 20) + f"""
<rect x="18" y="22" width="60" height="60" rx="16" fill="url(#ig)"/>
{icon_body}
<text x="92" y="36" font-size="17" class="t b">{title}</text>
{badge_svg}
<text x="92" y="58" font-size="13" class="s">{subtitle}</text>
{chips(92, 70, tags, max_x=388)}
<path d="M394 48 l7 8 l-7 8" fill="none" stroke="{C['faint']}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
{extra}
"""
    write(name, svg(h, body, defs))


eq = ""
for k, (hh, d) in enumerate([(18, 0.8), (30, 1.1), (22, 0.7), (34, 1.3)]):
    x = 32 + k * 9
    eq += (f'<rect x="{x}" y="{66-hh}" width="5" height="{hh}" rx="2.5" fill="#fff">'
           f'<animate attributeName="height" values="{hh};{hh*0.35:.0f};{hh}" dur="{d}s" repeatCount="indefinite"/>'
           f'<animate attributeName="y" values="{66-hh};{66-hh*0.35:.0f};{66-hh}" dur="{d}s" repeatCount="indefinite"/></rect>')
app_card(
    "card-music.svg", "Music is Life", "v2.1.1",
    "음악으로 연결되는 SNS · 2023 → 2026 리빌드",
    [("Flutter", C["blue"]), ("GetX", C["purple"]), ("Firebase", C["amber"]), ("Spotify", C["green"])],
    (C["pink"], C["purple"]), eq,
)

spark = (f'<path d="M26 66 L36 58 L44 62 L52 46 L60 52 L70 34" fill="none" stroke="#fff" stroke-width="3.2" '
         f'stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="80" stroke-dashoffset="0">'
         f'<animate attributeName="stroke-dashoffset" values="80;0;0;80" keyTimes="0;0.45;0.85;1" dur="3.2s" repeatCount="indefinite"/></path>'
         f'<circle cx="70" cy="34" r="3.5" fill="#fff"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.4;0.45;0.85;1" dur="3.2s" repeatCount="indefinite"/></circle>')
app_card(
    "card-coin.svg", "Coin Dashboard", "Web · iOS",
    "업비트 시세를 실시간으로 보는 대시보드",
    [("GetX", C["purple"]), ("go_router", C["teal"]), ("freezed", C["pink"]), ("Clean Arch", C["blue"])],
    (C["teal"], "#0EA5E9"), spark,
)

plane = (f'<path d="M26 68 Q48 30 72 40" fill="none" stroke="#fff" stroke-opacity="0.55" stroke-width="2" stroke-dasharray="3 4"/>'
         f'<g><text font-size="20" fill="#fff" text-anchor="middle" dy="7">✈</text>'
         f'<animateMotion path="M26 68 Q48 30 72 40" dur="3s" repeatCount="indefinite" rotate="auto"/></g>')
app_card(
    "card-airticket.svg", "AirTicket", "",
    "항공권 예매 · 클린 아키텍처 연습",
    [("Clean Architecture", C["blue"]), ("Flutter", C["teal"])],
    (C["amber"], "#F97316"), plane,
)

# 5. Todo 리믹스 -------------------------------------------------------------
h = 150
remix = [("GetX", C["purple"]), ("Bloc", C["blue"]), ("Cubit", C["teal"]), ("Riverpod", C["pink"]),
         ("Local Data", C["amber"]), ("Remote HTTP", C["green"]), ("Dart Frog 서버", C["red"])]
body = panel(h, 20) + f"""
<text x="22" y="38" font-size="16.5" class="t b">✅ Todo Remix Collection</text>
<text x="22" y="60" font-size="13" class="s">같은 Todo 앱을 7가지 방식으로 다시 만들어 봤어요</text>
{chips(22, 76, remix, gap=7, max_x=400)}
<rect x="22" y="132" width="{W-44}" height="5" rx="2.5" fill="{C['surface2']}"/>
<rect x="22" y="132" width="0" height="5" rx="2.5" fill="{C['purple']}">
  <animate attributeName="width" values="0;{W-44};{W-44}" keyTimes="0;0.7;1" dur="4s" repeatCount="indefinite"/>
</rect>
"""
write("card-todo.svg", svg(h, body))

# 6. 설정 = 기술 스택 --------------------------------------------------------
rows = [
    ("Flutter · Dart", "주력 · 2023년부터", C["blue"], True),
    ("GetX · Bloc · Riverpod", "상태관리는 상황 따라 골라 써요", C["purple"], True),
    ("Firebase · Supabase", "Auth · Firestore · 보안 규칙 · FCM", C["amber"], True),
    ("Clean Architecture", "data / domain / presentation · freezed", C["teal"], True),
    ("Python · Django · Java", "웹 백엔드 경험", C["faint"], False),
]
rh = 62
h = 52 + rh * len(rows) + 10
body = panel(h, 20) + f'<text x="22" y="36" font-size="16.5" class="t b">⚙️ 설정 · 기술 스택</text>'
for i, (title, sub, color, on) in enumerate(rows):
    y = 52 + i * rh
    if i:
        body += f'<line x1="66" y1="{y}" x2="{W-18}" y2="{y}" stroke="{C["border"]}"/>'
    body += (f'<rect x="22" y="{y+14}" width="32" height="32" rx="9" fill="{color}" fill-opacity="0.2"/>'
             f'<circle cx="38" cy="{y+30}" r="6" fill="{color}"/>'
             f'<text x="66" y="{y+28}" font-size="14.5" class="t b">{title}</text>'
             f'<text x="66" y="{y+47}" font-size="12" class="s">{sub}</text>')
    tx, ty = W - 70, y + 18
    delay = 0.3 + i * 0.25
    if on:
        k1, k2 = delay / 2.0, (delay + 0.25) / 2.0
        body += (f'<rect x="{tx}" y="{ty}" width="48" height="26" rx="13" fill="{C["green"]}">'
                 f'<animate attributeName="fill" values="{C["faint"]};{C["faint"]};{C["green"]}" keyTimes="0;{k1:.3f};{k2:.3f}" dur="2s" fill="freeze"/></rect>'
                 f'<circle cx="{tx+35}" cy="{ty+13}" r="10" fill="#fff">'
                 f'<animate attributeName="cx" values="{tx+13};{tx+13};{tx+35}" keyTimes="0;{k1:.3f};{k2:.3f}" dur="2s" fill="freeze"/></circle>')
    else:
        body += (f'<rect x="{tx-8}" y="{ty+3}" width="56" height="20" rx="10" fill="{C["surface2"]}"/>'
                 f'<text x="{tx+20}" y="{ty+17}" font-size="11" text-anchor="middle" class="s" font-weight="600">경험 있음</text>')
write("card-stack.svg", svg(h, body))

# 7. 스낵바 -----------------------------------------------------------------
h = 64
body = f"""
<g>
  <animate attributeName="opacity" values="0;0;1" keyTimes="0;0.6;1" dur="1s" fill="freeze"/>
  <animateTransform attributeName="transform" type="translate" values="0 24;0 24;0 0" keyTimes="0;0.6;1" dur="1s" fill="freeze"/>
  <rect x="10" y="8" width="{W-20}" height="48" rx="12" fill="#2A2F3D"/>
  <text x="28" y="38" font-size="14" fill="#EEF0F6">🎉 music_is_life v2.1.1 업데이트!</text>
  <text x="{W-30}" y="38" font-size="14" text-anchor="end" fill="{C['purple']}" font-weight="700">개발 일지 ›</text>
</g>
"""
write("snackbar.svg", svg(h, body))

# 7-1. 경력 위젯 (회사 + 핵심 지표) -------------------------------------------
h = 214
defs = (f'<linearGradient id="co" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="#FB7185"/><stop offset="1" stop-color="#F97316"/></linearGradient>')
metrics = [
    ("3종", "유저 · 점주 · 어드민 앱", C["blue"]),
    ("3분→1초", "정산 화면 로딩 (체감)", C["green"]),
    ("Toss", "결제 · 취소 · 정산 연동", C["purple"]),
]
tile_w = (W - 32 - 16) / 3
tiles = ""
for i, (big, small, color) in enumerate(metrics):
    x = 16 + i * (tile_w + 8)
    tiles += (f'<rect x="{x:.1f}" y="112" width="{tile_w:.1f}" height="84" rx="16" fill="{C["surface2"]}"/>'
              f'<rect x="{x + 14:.1f}" y="126" width="18" height="4" rx="2" fill="{color}"/>'
              f'<text x="{x + 14:.1f}" y="160" font-size="20" fill="{color}" font-weight="800">{big}</text>'
              f'<text x="{x + 14:.1f}" y="182" font-size="11.5" class="s">{small}</text>')
body = panel(h, 22) + f"""
<rect x="16" y="18" width="52" height="52" rx="15" fill="url(#co)"/>
<text x="42" y="52" font-size="24" text-anchor="middle">🍽️</text>
<text x="82" y="40" font-size="17" class="t b">주식회사 엔데버</text>
<text x="82" y="62" font-size="13" class="s">음식점 타임딜 플랫폼 써젯(Sugget) · Flutter 개발</text>
<rect x="16" y="82" width="190" height="22" rx="11" fill="{C['purple']}" fill-opacity="0.18"/>
<text x="111" y="97" font-size="12" text-anchor="middle" fill="{C['purple']}" font-weight="700">2024.09 – 2026.06 · 1년 10개월</text>
{tiles}
"""
write("card-career.svg", svg(h, body, defs))

# 7-2. 눈여겨볼 작업 위젯 ------------------------------------------------------
works = [
    ("💳", "정산 집계를 서버 배치로 전환", "클라이언트 계산 → 매일 10시 서버 집계 · 토스 정산 예정금 기준", C["green"]),
    ("🧾", "정산 상태 분리 · 누락 감시", "pending / settled 구분 · 3일 이상 pending이면 담당자 알림", C["teal"]),
    ("🔁", "결제 실패 보상 처리", "후처리 실패 시 자동 결제 취소 + 재고 복구 · 에러 코드별 안내", C["purple"]),
    ("📍", "지오코딩은 가입 때 한 번만", "좌표를 저장해 지도 조회 시 변환 호출 0 · 영문 주소로 정확도 ↑", C["blue"]),
    ("🔐", "SMS 인증 · 탈퇴 순서 보장", "재전송 토큰 · 중복 발송 방지 · DB 정리 후 Auth 삭제", C["amber"]),
    ("🎛️", "Remote Config + flavor", "강제 업데이트 · 점검 · 수수료율 무배포 변경 · dev/prod 분리", C["pink"]),
    ("🧱", "공통 컴포넌트 · 클린 아키텍처", "Figma 속성 단위 컴포넌트 · 기능 단위 점진 이관", C["red"]),
]
rh = 58
h = 58 + rh * len(works) + 6
body = panel(h, 22) + f'<text x="20" y="38" font-size="16.5" class="t b">🔧 이런 문제를 풀었어요</text>'
for i, (emoji, title, sub, color) in enumerate(works):
    y = 54 + i * rh
    if i:
        body += f'<line x1="64" y1="{y}" x2="{W-18}" y2="{y}" stroke="{C["border"]}"/>'
    body += (f'<rect x="18" y="{y+11}" width="36" height="36" rx="11" fill="{color}" fill-opacity="0.18"/>'
             f'<text x="36" y="{y+35}" font-size="17" text-anchor="middle">{emoji}</text>'
             f'<text x="66" y="{y+26}" font-size="14.5" class="t b">{title}</text>'
             f'<text x="66" y="{y+45}" font-size="11.8" class="s">{sub}</text>')
write("card-work.svg", svg(h, body))

# 7-2b. 스토어 링크 = iOS 설정 화면 같은 목록 카드 --------------------------------
# 모바일에서도 깨지지 않도록 가로로 자르지 않고, 링크 하나당 한 줄(통이미지)로 만든다.
# 줄 사이 틈이 0이라 위·아래 줄이 이어져 하나의 카드처럼 보인다.
STORE_DIR = sys.argv[3]


def b64png(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def list_shape(h, first, last, r=20):
    """목록 카드의 한 줄: 첫 줄은 위쪽만, 마지막 줄은 아래쪽만 둥글게."""
    x0, x1 = 1, W - 1
    y0, y1 = (1 if first else 0), (h - 1 if last else h)
    tr, br = (r if first else 0), (r if last else 0)
    fill = (f'M{x0 + tr} {y0} H{x1 - tr} Q{x1} {y0} {x1} {y0 + tr} V{y1 - br} Q{x1} {y1} {x1 - br} {y1} '
            f'H{x0 + br} Q{x0} {y1} {x0} {y1 - br} V{y0 + tr} Q{x0} {y0} {x0 + tr} {y0} Z')
    # 테두리는 옆선 + (첫 줄이면 윗선, 마지막 줄이면 아랫선)만 그려 줄 사이에 선이 겹치지 않게 한다
    edge = (f'M{x0} {h if not last else y1 - br} V{y0 + tr}' + (f' Q{x0} {y0} {x0 + tr} {y0} H{x1 - tr} Q{x1} {y0} {x1} {y0 + tr}' if first else f' M{x1} {y0}')
            + f' V{y1 - br}' + (f' Q{x1} {y1} {x1 - br} {y1} H{x0 + br} Q{x0} {y1} {x0} {y1 - br}' if last else f' V{h}'))
    return (f'<path d="{fill}" fill="{C["surface"]}"/>'
            f'<path d="{edge}" fill="none" stroke="{C["border"]}" stroke-width="1.5"/>')


def store_head():
    h = 52
    body = (list_shape(h, True, False) +
            f'<text x="20" y="34" font-size="15.5" class="t b">📲 스토어에서 만나보기</text>'
            f'<text x="{W-20}" y="34" font-size="12" text-anchor="end" class="f">Endeavor Inc.</text>')
    write("store-head.svg", svg(h, body), pad=(6, 0))


STORE_GLYPH = {
    "ios": ("App Store", "blue",
            '<path d="M-7 6 L0 -7 L7 6 M-4.5 1.5 H4.5 M-9 6 H-4 M4 6 H9" fill="none" stroke-width="2.2" '
            'stroke-linecap="round" stroke-linejoin="round"/>'),
    "play": ("Google Play", "green",
             '<path d="M-6 -8 L8 0 L-6 8 Z" fill="none" stroke-width="2.2" stroke-linejoin="round"/>'),
}


def store_item(name, icon_file, app, sub, store, last=False):
    h = 64
    label, color_key, glyph = STORE_GLYPH[store]
    color = C[color_key]
    defs = f'<clipPath id="ic"><rect x="20" y="12" width="40" height="40" rx="10"/></clipPath>'
    body = (list_shape(h, False, last) +
            f'<line x1="74" y1="0.5" x2="{W-1}" y2="0.5" stroke="{C["border"]}"/>'
            f'<image x="20" y="12" width="40" height="40" clip-path="url(#ic)" href="{b64png(os.path.join(STORE_DIR, icon_file))}"/>'
            f'<text x="74" y="29" font-size="14.5" class="t b">{app}</text>'
            f'<text x="74" y="48" font-size="12" class="s">{sub}</text>'
            f'<rect x="{W-150}" y="16" width="112" height="32" rx="16" fill="{color}" fill-opacity="0.14"/>'
            f'<g transform="translate({W-130} 32) scale(0.8)" stroke="{color}">{glyph}</g>'
            f'<text x="{W-117}" y="36.5" font-size="12" fill="{color}" font-weight="700">{label}</text>'
            f'<path d="M{W-24} 26 l6 6 l-6 6" fill="none" stroke="{C["faint"]}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
    write(name, svg(h, body, defs), pad=(0, 6 if last else 0))


store_head()
store_item("store-user-ios.svg", "user.png", "써젯", "유저앱 · 타임딜 구매", "ios")
store_item("store-user-play.svg", "user.png", "써젯", "유저앱 · 타임딜 구매", "play")
store_item("store-partner-ios.svg", "partner.png", "써젯 사장님용", "점주앱 · 티켓 확인 · 정산", "ios")
store_item("store-partner-play.svg", "partner.png", "써젯 사장님용", "점주앱 · 티켓 확인 · 정산", "play", last=True)

# 7-3. 정보처리기사 위젯 --------------------------------------------------------
h = 120
defs = (f'<linearGradient id="medal" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="#60A5FA"/><stop offset="1" stop-color="{C["purple"]}"/></linearGradient>'
        f'<linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.35"/>'
        f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<clipPath id="medalClip"><circle cx="58" cy="60" r="34"/></clipPath>')
body = panel(h, 22) + f"""
<circle cx="58" cy="60" r="34" fill="url(#medal)"/>
<circle cx="58" cy="60" r="26" fill="none" stroke="#fff" stroke-opacity="0.5" stroke-width="2" stroke-dasharray="3 3"/>
<text x="58" y="69" font-size="26" text-anchor="middle">🎖️</text>
<g clip-path="url(#medalClip)">
  <rect x="-40" y="20" width="30" height="80" fill="url(#shine)" transform="rotate(20 58 60)">
    <animate attributeName="x" values="-40;-40;140" keyTimes="0;0.6;1" dur="3s" repeatCount="indefinite"/>
  </rect>
</g>
<text x="108" y="40" font-size="12" fill="{C['blue']}" font-weight="700">국가기술자격 · 합격</text>
<text x="108" y="66" font-size="21" class="t b">정보처리기사</text>
<text x="{W-20}" y="40" font-size="12" text-anchor="end" class="f">2025.09</text>
<rect x="108" y="78" width="104" height="22" rx="11" fill="{C['amber']}" fill-opacity="0.18"/>
<text x="160" y="93" font-size="12" text-anchor="middle" fill="{C['amber']}" font-weight="700">비전공 개발자</text>
<text x="220" y="93" font-size="12" class="s">로 취득했어요</text>
"""
write("card-cert.svg", svg(h, body, defs))

# 7-4. 수상 = 푸시 알림 -------------------------------------------------------
h = 92
defs = (f'<linearGradient id="trophy" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{C["amber"]}"/><stop offset="1" stop-color="#F97316"/></linearGradient>')
body = f"""
<g>
  <animateTransform attributeName="transform" type="translate" values="0 -60;0 -60;0 0" keyTimes="0;0.4;1" dur="1.2s" fill="freeze"/>
  <animate attributeName="opacity" values="0;0;1" keyTimes="0;0.4;1" dur="1.2s" fill="freeze"/>
  <rect x="1" y="1" width="{W-2}" height="{h-2}" rx="22" fill="{C['notif']}" stroke="{C['border']}" stroke-width="1.5"/>
  <rect x="16" y="18" width="40" height="40" rx="11" fill="url(#trophy)"/>
  <text x="36" y="45" font-size="20" text-anchor="middle">🏆</text>
  <text x="68" y="32" font-size="12" class="s" font-weight="600">수상 알림</text>
  <text x="{W-18}" y="32" font-size="12" text-anchor="end" class="f">2023.07.08</text>
  <text x="68" y="54" font-size="15" class="t b">BiG(Busan is Good) Data Hackathon</text>
  <text x="68" y="75" font-size="13.5" fill="{C['amber']}" font-weight="700">인기상 수상 🎉</text>
</g>
"""
write("card-award.svg", svg(h, body, defs))

# 8. 하단 내비 = 폰 아랫부분 (플로팅 글래스 탭바 + 홈 인디케이터 + 베젤) -------------------
# iOS 26 Liquid Glass 스타일: 화면 아래에 떠 있는 반투명 캡슐, 선택 탭은 캡슐 안의 알약으로 채운다.
# 모바일에서 함께 줄어들도록 한 장(통이미지)으로 만든다.
# 그림자는 SVG filter 대신 반투명 사각형을 겹쳐 그린다 (filter를 못 그리는 렌더러 대비).
GAP_T, CAP_H, GAP_B, HOME_H = 6, 64, 10, 22
CAP_X = BZ + 14
CAP_W = WO - CAP_X * 2
CAP_Y = GAP_T
TAB_W = CAP_W / 4
GLASS = (("#FFFFFF", 0.86, "#000000", 0.08, 0.95) if THEME == "light"
         else ("#1D2230", 0.80, "#FFFFFF", 0.10, 0.22))   # 채움색, 채움 투명도, 테두리색, 테두리 투명도, 윗변 반사
SHADOW = (0.05, 0.03) if THEME == "light" else (0.10, 0.06)
tabs = [
    ("홈", '<path d="M2 9 L10 2 L18 9 V18 H2 Z"/>', '<path d="M8 18 V12.5 H12 V18"/>'),
    ("레포", '<rect x="2" y="2" width="16" height="16" rx="3"/><path d="M6 7 H14 M6 10.5 H14 M6 14 H10"/>', ""),
    ("개발 일지", '<path d="M3 15 L4 11 L13 2 L16 5 L7 14 Z"/><path d="M3 18.5 H17"/>', ""),
    ("포트폴리오", '<rect x="1" y="5" width="18" height="13" rx="3"/><path d="M7 5 V2.5 H13 V5"/><path d="M1 10.5 H19"/>', ""),
]
H = GAP_T + CAP_H + GAP_B + HOME_H + BZ
SB = H - BZ          # 화면 아래 끝
fill, fill_op, line, line_op, shine = GLASS
r = CAP_H / 2
body = (f'<defs><linearGradient id="shine" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="#fff" stop-opacity="{shine}"/><stop offset="0.5" stop-color="#fff" stop-opacity="0"/>'
        f'</linearGradient></defs>'
        f'<path d="M0 0 H{WO} V{H-R_OUT} Q{WO} {H} {WO-R_OUT} {H} H{R_OUT} Q0 {H} 0 {H-R_OUT} Z" fill="{BODY}"/>'
        f'<path d="M0.75 0 V{H-R_OUT} Q0.75 {H-0.75} {R_OUT} {H-0.75} H{WO-R_OUT} Q{WO-0.75} {H-0.75} {WO-0.75} {H-R_OUT} V0" '
        f'fill="none" stroke="{EDGE}" stroke-width="1.5"/>'
        f'<path d="M{BZ} 0 H{WO-BZ} V{SB-R_SCR} Q{WO-BZ} {SB} {WO-BZ-R_SCR} {SB} H{BZ+R_SCR} Q{BZ} {SB} {BZ} {SB-R_SCR} Z" '
        f'fill="{C["bg"]}"/>'
        # 그림자 (겹친 반투명 캡슐)
        f'<rect x="{CAP_X+2}" y="{CAP_Y+5}" width="{CAP_W-4}" height="{CAP_H}" rx="{r}" fill="#000" fill-opacity="{SHADOW[0]}"/>'
        f'<rect x="{CAP_X+5}" y="{CAP_Y+8}" width="{CAP_W-10}" height="{CAP_H-2}" rx="{r-1}" fill="#000" fill-opacity="{SHADOW[1]}"/>'
        # 유리 캡슐 + 테두리 + 윗변 반사
        f'<rect x="{CAP_X}" y="{CAP_Y}" width="{CAP_W}" height="{CAP_H}" rx="{r}" fill="{fill}" fill-opacity="{fill_op}" '
        f'stroke="{line}" stroke-opacity="{line_op}"/>'
        f'<rect x="{CAP_X+1}" y="{CAP_Y+1}" width="{CAP_W-2}" height="{CAP_H-2}" rx="{r-1}" fill="url(#shine)"/>')
# 선택된 탭(홈): 탭 칸 전체를 채우는 알약. 기본값이 최종 상태라 애니메이션이 없어도 그대로 보인다.
PX, PY = CAP_X + 6, CAP_Y + 6
PW, PH = TAB_W - 4, CAP_H - 12
body += (f'<rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" rx="{PH/2}" fill="{C["purple"]}" fill-opacity="0.22" '
         f'stroke="{C["purple"]}" stroke-opacity="0.35">'
         f'<animate attributeName="width" values="{PH};{PW}" dur="0.45s" fill="freeze"/>'
         f'<animate attributeName="x" values="{PX + (PW - PH) / 2};{PX}" dur="0.45s" fill="freeze"/></rect>')
for i, (label, icon, detail) in enumerate(tabs):
    active = i == 0
    cx = CAP_X + TAB_W * i + TAB_W / 2
    if active:
        # 선택 탭은 채워진 아이콘
        icon_svg = (f'<g transform="translate({cx-10} {CAP_Y+11})" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
                    f'<g fill="{C["purple"]}" stroke="{C["purple"]}">{icon}</g>'
                    f'<g fill="none" stroke="{C["surface"]}">{detail}</g></g>')
        label_color, weight = C["purple"], 700
    else:
        icon_svg = (f'<g transform="translate({cx-10} {CAP_Y+11})" fill="none" stroke="{C["sub"]}" stroke-width="2" '
                    f'stroke-linecap="round" stroke-linejoin="round">{icon}{detail}</g>')
        label_color, weight = C["sub"], 500
    body += (icon_svg +
             f'<text x="{cx}" y="{CAP_Y+50}" font-size="11.5" text-anchor="middle" fill="{label_color}" '
             f'font-weight="{weight}" font-family="{FONT}">{label}</text>')
body += (f'<rect x="{WO/2-67}" y="{CAP_Y + CAP_H + GAP_B + HOME_H/2 - 2.5}" width="134" height="5" rx="2.5" '
         f'fill="{C["text"]}" fill-opacity="0.85"/>')
_save("nav.svg", _outer(H, body))

print("generated:", sorted(os.listdir(OUT)))
