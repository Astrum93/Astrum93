"""Astrum93 프로필 README용 '앱 화면' SVG 생성기.

사용법: python3 -I gen_profile_svgs.py <출력 폴더> <아바타 PNG> <스토어 아이콘 폴더(user.png, partner.png)>
(아바타는 SVG 안에 base64로 넣는다. README의 <img>로 띄운 SVG는 외부 이미지를 불러오지 못하기 때문)
"""
import base64
import os
import sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
with open(sys.argv[2], "rb") as f:
    AVATAR = "data:image/png;base64," + base64.b64encode(f.read()).decode()

W = 420
C = {
    "bg": "#0F1218",
    "surface": "#161A22",
    "surface2": "#1E2330",
    "border": "#262C3A",
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


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)


# 1. AppBar + 상태바 ---------------------------------------------------------
h = 118
body = panel(h, 28) + f"""
<rect x="160" y="12" width="100" height="28" rx="14" fill="#000"/>
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
write("appbar.svg", svg(h, body))

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
    typing += f"""
<clipPath id="tc{i}"><rect x="52" y="214" width="0" height="26">
  <animate attributeName="width" values="{vals}" keyTimes="{kt}" dur="{n*3.2}s" repeatCount="indefinite"/>
</rect></clipPath>"""
type_texts = "".join(
    f'<text x="52" y="232" font-size="14.5" class="t" clip-path="url(#tc{i})">{line}</text>'
    for i, line in enumerate(lines)
)
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
  <text x="24" y="38" font-size="12" fill="#fff" fill-opacity="0.85" font-weight="600">♪ NOW CODING</text>
  <text x="24" y="58" font-size="15" fill="#fff" font-weight="700">music_is_life v2.1.1</text>
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
         f'stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="80" stroke-dashoffset="80">'
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
  <text x="28" y="38" font-size="14" class="t">🎉 music_is_life v2.1.1 업데이트!</text>
  <text x="{W-30}" y="38" font-size="14" text-anchor="end" fill="{C['purple']}" font-weight="700">릴리스 보기</text>
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

# 7-2b. 스토어 링크 위젯 (한 줄을 3조각으로 잘라 조각마다 링크) --------------------
STORE_DIR = sys.argv[3]
SLICES = [("info", 0, 252), ("ios", 252, 84), ("play", 336, 84)]


def b64png(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def store_row(prefix, icon_file, name, sub, first=False, last=False):
    h = 84
    # 위/아래 줄이 붙어 하나의 카드처럼 보이도록, 첫 줄은 위쪽만, 마지막 줄은 아래쪽만 둥글게
    top_r = 20 if first else 0
    bot_r = 20 if last else 0
    x0, x1, y0, y1 = 1, W - 1, 1 if first else 0, h - 1 if last else h
    shape = (f'M{x0 + top_r} {y0} H{x1 - top_r} Q{x1} {y0} {x1} {y0 + top_r} V{y1 - bot_r} Q{x1} {y1} {x1 - bot_r} {y1} '
             f'H{x0 + bot_r} Q{x0} {y1} {x0} {y1 - bot_r} V{y0 + top_r} Q{x0} {y0} {x0 + top_r} {y0} Z')
    sep = "" if first else f'<line x1="16" y1="0.5" x2="{W-16}" y2="0.5" stroke="{C["border"]}"/>'
    defs = f'<clipPath id="ic"><rect x="16" y="14" width="56" height="56" rx="14"/></clipPath>'
    btn = ""
    for i, (glyph, label, color) in enumerate([
        (f'<path d="M-7 6 L0 -7 L7 6 M-4.5 1.5 H4.5 M-9 6 H-4 M4 6 H9" fill="none" stroke="{C["blue"]}" '
         f'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>', "App Store", C["blue"]),
        (f'<path d="M-6 -8 L8 0 L-6 8 Z" fill="none" stroke="{C["green"]}" stroke-width="2.2" stroke-linejoin="round"/>',
         "Google Play", C["green"]),
    ]):
        cx = 252 + 84 * i + 42
        btn += (f'<rect x="{cx-34}" y="14" width="68" height="56" rx="14" fill="{color}" fill-opacity="0.12"/>'
                f'<g transform="translate({cx} 34)">{glyph}</g>'
                f'<text x="{cx}" y="60" font-size="10.5" text-anchor="middle" fill="{color}" font-weight="700">{label}</text>')
    body = (f'<path d="{shape}" fill="{C["surface"]}" stroke="{C["border"]}" stroke-width="1.5"/>{sep}'
            f'<image x="16" y="14" width="56" height="56" clip-path="url(#ic)" href="{b64png(os.path.join(STORE_DIR, icon_file))}"/>'
            f'<rect x="16" y="14" width="56" height="56" rx="14" fill="none" stroke="#fff" stroke-opacity="0.08"/>'
            f'<text x="86" y="38" font-size="15.5" class="t b">{name}</text>'
            f'<text x="86" y="59" font-size="12" class="s">{sub}</text>{btn}')
    full = svg(h, body, defs)
    for key, x, w in SLICES:
        s = full.replace(f'width="{W}" height="{h}" viewBox="0 0 {W} {h}"',
                         f'width="{w}" height="{h}" viewBox="{x} 0 {w} {h}"')
        write(f"{prefix}-{key}.svg", s)


store_row("store-user", "user.png", "써젯", "유저앱 · 타임딜 구매", first=True, last=True)
store_row("store-partner", "partner.png", "써젯 사장님용", "점주앱 · 티켓 확인 · 정산", first=True, last=True)

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
  <rect x="1" y="1" width="{W-2}" height="{h-2}" rx="22" fill="#232838" stroke="{C['border']}" stroke-width="1.5"/>
  <rect x="16" y="18" width="40" height="40" rx="11" fill="url(#trophy)"/>
  <text x="36" y="45" font-size="20" text-anchor="middle">🏆</text>
  <text x="68" y="32" font-size="12" class="s" font-weight="600">수상 알림</text>
  <text x="{W-18}" y="32" font-size="12" text-anchor="end" class="f">2023.07.08</text>
  <text x="68" y="54" font-size="15" class="t b">BiG(Busan is Good) Data Hackathon</text>
  <text x="68" y="75" font-size="13.5" fill="{C['amber']}" font-weight="700">인기상 수상 🎉</text>
</g>
"""
write("card-award.svg", svg(h, body, defs))

# 8. 하단 내비 (4조각이 이어져 하나의 바처럼 보이게) ---------------------------
# 각 조각은 420px 전체 바를 그린 뒤 자기 구간(105px)만 보여준다 → 이음새 없이 연결됨.
NAV_W, NAV_H, NAV_N = W // 4, 76, 4


def nav(name, index, label, icon, active=False):
    w, h = NAV_W, NAV_H
    cx = w / 2
    bar = (f'<g transform="translate({-index * w} 0)">'
           f'<rect x="1" y="1" width="{W-2}" height="{h-2}" rx="22" fill="{C["surface"]}" '
           f'stroke="{C["border"]}" stroke-width="1.5"/></g>')
    defs = ""
    if active:
        # 버튼 구간 전체를 칠한다. 바 모양으로 잘라서 바깥 모서리 곡선은 그대로 유지.
        defs = (f'<clipPath id="barClip"><rect x="{1 - index * w}" y="1" width="{W-2}" height="{h-2}" rx="22"/></clipPath>')
        indicator = (f'<rect x="0" y="0" width="{w}" height="{h}" fill="{C["purple"]}" fill-opacity="0.26" clip-path="url(#barClip)">'
                     f'<animate attributeName="fill-opacity" values="0;0.26" dur="0.4s" fill="freeze"/></rect>')
        icon_color, label_color, weight = C["purple"], C["text"], 700
    else:
        indicator, icon_color, label_color, weight = "", C["sub"], C["sub"], 500
    body = (f'{bar}{indicator}'
            f'<g transform="translate({cx-10} 17)" fill="none" stroke="{icon_color}" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round">{icon}</g>'
            f'<text x="{cx}" y="62" font-size="12" text-anchor="middle" fill="{label_color}" '
            f'font-weight="{weight}">{label}</text>')
    s = svg(h, body, defs).replace(f'width="{W}" height="{h}" viewBox="0 0 {W} {h}"',
                                   f'width="{w}" height="{h}" viewBox="0 0 {w} {h}"')
    write(name, s)


# 아이콘은 20x20 박스 기준
nav("nav-home.svg", 0, "홈", '<path d="M2 9 L10 2 L18 9 V18 H2 Z"/><path d="M8 18 V12 H12 V18"/>', active=True)
nav("nav-repos.svg", 1, "레포", '<rect x="2" y="2" width="16" height="16" rx="3"/><path d="M6 7 H14 M6 10.5 H14 M6 14 H10"/>')
nav("nav-devlog.svg", 2, "개발 일지", '<path d="M3 15 L4 11 L13 2 L16 5 L7 14 Z"/><path d="M3 18.5 H17"/>')
nav("nav-notion.svg", 3, "포트폴리오", '<rect x="1" y="5" width="18" height="13" rx="3"/><path d="M7 5 V2.5 H13 V5"/><path d="M1 10.5 H19"/>')

print("generated:", sorted(os.listdir(OUT)))
