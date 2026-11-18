"""docs/HOW_IT_WORKS.md에 들어가는 설명 다이어그램 생성기.

다이어그램은 자체 배경 카드를 가져서 GitHub 라이트/다크 테마 어디서든 읽힌다.

사용법: python3 scripts/gen_docs_diagrams.py  (저장소 루트에서 실행) → docs/images/*.svg
"""
import os

OUT = "docs/images"
os.makedirs(OUT, exist_ok=True)

FONT = ("Pretendard, 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', "
        "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif")
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
BG, LINE, TEXT, SUB = "#F6F8FA", "#D0D7DE", "#1F2328", "#59636E"
PURPLE, GREEN, RED, BLUE, AMBER = "#6D5BD0", "#1A7F37", "#CF222E", "#0969DA", "#9A6700"
PHONE, SCREEN, CARD = "#1B1F27", "#0F1218", "#1E2330"


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<style>text{{font-family:{FONT};fill:{TEXT}}} .s{{fill:{SUB}}} .b{{font-weight:700}} '
            f'.m{{font-family:{MONO}}}</style>'
            f'<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            f'<path d="M0 0 L10 5 L0 10 z" fill="{SUB}"/></marker></defs>'
            f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16" fill="{BG}" stroke="{LINE}" stroke-width="1.5"/>'
            f'{body}</svg>\n')


def box(x, y, w, h, title, sub="", color=PURPLE, mono_sub=False):
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#fff" stroke="{color}" stroke-width="1.6"/>'
         f'<rect x="{x}" y="{y}" width="6" height="{h}" rx="3" fill="{color}"/>'
         f'<text x="{x + w/2 + 3}" y="{y + (h/2 - 2 if sub else h/2 + 5)}" font-size="14" text-anchor="middle" class="b">{title}</text>')
    if sub:
        s += (f'<text x="{x + w/2 + 3}" y="{y + h/2 + 16}" font-size="11.5" text-anchor="middle" '
              f'class="s{" m" if mono_sub else ""}">{sub}</text>')
    return s


def arrow(x1, y1, x2, y2, dashed=False):
    d = ' stroke-dasharray="5 4"' if dashed else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{SUB}" stroke-width="1.8"{d} marker-end="url(#ar)"/>'


def label(x, y, t, size=12, cls="s", anchor="start", extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" class="{cls}" text-anchor="{anchor}" {extra}>{t}</text>'


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)


# 1. 전체 흐름 ------------------------------------------------------------------
W, H = 760, 360
b = label(24, 36, "① 전체 흐름 — 코드로 그리고, 조립하고, 커밋한다", 16, "b")
b += box(24, 62, 200, 64, "scripts/src/", "프로필 사진 · 앱 아이콘 · 문구", AMBER)
b += box(280, 62, 200, 64, "gen_profile_svgs.py", "dark / light 두 번 실행", PURPLE)
b += box(536, 62, 200, 64, "assets/ · assets/light/", "SVG 22장 × 2 테마", BLUE)
b += arrow(224, 94, 278, 94) + arrow(480, 94, 534, 94)
b += box(536, 170, 200, 64, "build_readme.py", "행 순서 · 링크 · ?v=해시", PURPLE)
b += box(280, 170, 200, 64, "README.md", "이미지 22장을 이어 붙인 HTML", GREEN)
b += box(24, 170, 200, 64, "GitHub 웹 · 앱", "폰 화면처럼 보임", GREEN)
b += arrow(636, 126, 636, 168) + arrow(536, 202, 482, 202) + arrow(280, 202, 226, 202)
b += (f'<rect x="24" y="262" width="712" height="74" rx="12" fill="#fff" stroke="{LINE}" stroke-dasharray="6 5"/>'
      + label(44, 290, "⏰ 매일 00:00 KST · GitHub Actions (now-coding.yml)", 13.5, "b")
      + label(44, 315, "update_now_coding.py로 최근 push한 공개 레포 + 최신 태그 → now_coding.txt → SVG 재생성 → README 해시 갱신 → 바뀌면 커밋", 12))
write("01-pipeline.svg", svg(W, H, b))

# 2. 폰을 조각으로 쌓기 -----------------------------------------------------------
W, H = 760, 470
b = label(24, 36, "② 화면 한 줄 = SVG 한 장, 조각마다 폰 몸통을 함께 그린다", 16, "b")
px, pw = 60, 230
rows = [("appbar.svg", 70, "top", "둥근 윗부분 · 다이내믹 아일랜드 · 상태바"),
        ("profile.svg", 74, "mid", "배너 · 프로필 사진 · 타이핑 문구"),
        ("section · card-*.svg", 58, "mid", "경력 · 스토어 · 자격 · 프로젝트 …"),
        ("card-stack.svg", 58, "mid", "기술 스택"),
        ("nav.svg", 70, "bottom", "플로팅 탭바 · 홈 인디케이터 · 둥근 아랫부분")]
y = 64
for i, (name, h, kind, desc) in enumerate(rows):
    r = 26
    if kind == "top":
        outer = f'M{px} {y+h} V{y+r} Q{px} {y} {px+r} {y} H{px+pw-r} Q{px+pw} {y} {px+pw} {y+r} V{y+h} Z'
    elif kind == "bottom":
        outer = f'M{px} {y} H{px+pw} V{y+h-r} Q{px+pw} {y+h} {px+pw-r} {y+h} H{px+r} Q{px} {y+h} {px} {y+h-r} Z'
    else:
        outer = f'M{px} {y} H{px+pw} V{y+h} H{px} Z'
    b += f'<path d="{outer}" fill="{PHONE}"/>'
    b += f'<rect x="{px+8}" y="{y + (8 if kind == "top" else 0)}" width="{pw-16}" height="{h - (8 if kind in ("top", "bottom") else 0)}" rx="{14 if kind != "mid" else 0}" fill="{SCREEN}"/>'
    if kind == "top":
        b += f'<rect x="{px+pw/2-30}" y="{y+16}" width="60" height="16" rx="8" fill="#000"/>'
        b += f'<rect x="{px+20}" y="{y+44}" width="90" height="10" rx="5" fill="#EEF0F6" fill-opacity="0.8"/>'
    elif kind == "bottom":
        b += f'<rect x="{px+20}" y="{y+10}" width="{pw-40}" height="30" rx="15" fill="{CARD}" stroke="#ffffff" stroke-opacity="0.12"/>'
        b += f'<rect x="{px+24}" y="{y+13}" width="{(pw-48)/4}" height="24" rx="12" fill="#8B7CF6" fill-opacity="0.35"/>'
        b += f'<rect x="{px+pw/2-30}" y="{y+50}" width="60" height="4" rx="2" fill="#EEF0F6"/>'
    else:
        b += f'<rect x="{px+20}" y="{y+8}" width="{pw-40}" height="{h-16}" rx="10" fill="{CARD}" stroke="#2C3342"/>'
    if i:
        b += f'<line x1="{px-14}" y1="{y}" x2="{px+pw+14}" y2="{y}" stroke="{RED}" stroke-width="1.2" stroke-dasharray="4 3"/>'
    b += f'<line x1="{px+pw+20}" y1="{y+h/2}" x2="{px+pw+60}" y2="{y+h/2}" stroke="{LINE}" stroke-width="1.5"/>'
    b += label(px + pw + 70, y + h/2 - 3, name, 13.5, "b m")
    b += label(px + pw + 70, y + h/2 + 16, desc, 12)
    y += h
b += label(24, y + 34, "빨간 점선 = 이미지 경계. 각 조각이 양옆 베젤과 화면 배경을 같이 그리므로, 이어 붙이면 폰 한 대가 된다 (frame() 함수).", 12)
write("02-phone-slices.svg", svg(W, H, b))

# 3. 틈 없애기 ------------------------------------------------------------------
W, H = 760, 370
b = label(24, 36, "③ 이미지 사이 틈을 0으로 — align=\"top\" + 한 덩어리로 이어 붙이기", 16, "b")
for col, (title, gap, color, mark) in enumerate([("기본: 이미지마다 문단", 10, RED, "✕ 6~16px 틈 → 테두리가 끊김"),
                                                  ("align=\"top\" + &lt;br&gt; 연결", 0, GREEN, "✓ 틈 0 → 테두리가 이어짐")]):
    x = 60 + col * 360
    b += label(x, 72, title, 13.5, "b")
    y = 88
    for k in range(3):
        b += f'<rect x="{x}" y="{y}" width="160" height="44" fill="{PHONE}"/><rect x="{x+8}" y="{y}" width="144" height="44" fill="{SCREEN}"/>'
        b += f'<rect x="{x+18}" y="{y+8}" width="124" height="28" rx="6" fill="{CARD}"/>'
        y += 44
        if gap and k < 2:
            b += f'<rect x="{x-6}" y="{y}" width="172" height="{gap}" fill="{RED}" fill-opacity="0.18"/>'
            y += gap
    b += label(x, y + 26, mark, 12.5, "b", extra=f'style="fill:{color}"')
b += (f'<rect x="24" y="302" width="712" height="46" rx="10" fill="#fff" stroke="{LINE}"/>'
      + label(40, 330, '&lt;a&gt;&lt;picture&gt;…&lt;img src="assets/x.svg?v=…" width="464" align="top"&gt;&lt;/picture&gt;&lt;/a&gt;&lt;br&gt;', 12, "m"))
write("03-zero-gap.svg", svg(W, H, b))

# 4. 모바일 --------------------------------------------------------------------
W, H = 760, 330
b = label(24, 36, "④ 모바일 — 모든 줄을 464px 통이미지로 (GitHub는 이미지마다 따로 줄인다)", 16, "b")
b += label(60, 72, "가로 조각 (이전)", 13.5, "b")
b += f'<rect x="60" y="88" width="230" height="40" fill="{PHONE}"/><rect x="68" y="88" width="214" height="40" fill="{SCREEN}"/>'
b += label(175, 113, "통이미지 → 줄어듦", 11, "s", "middle", f'style="fill:#98A1B3"')
xs = [(60, 140, "앱 정보"), (200, 56, "App Store"), (60, 74, "Google Play")]
b += f'<rect x="60" y="128" width="140" height="40" fill="{CARD}" stroke="{RED}"/><text x="130" y="153" font-size="11" text-anchor="middle" style="fill:#EEF0F6">앱 정보</text>'
b += f'<rect x="200" y="128" width="90" height="40" fill="{CARD}" stroke="{RED}"/><text x="245" y="153" font-size="11" text-anchor="middle" style="fill:#EEF0F6">App Store</text>'
b += f'<rect x="60" y="168" width="96" height="40" fill="{CARD}" stroke="{RED}"/><text x="108" y="193" font-size="11" text-anchor="middle" style="fill:#EEF0F6">Google Play</text>'
b += label(60, 236, "✕ 조각은 원래 크기로 남아 줄이 넘어가고 깨짐", 12.5, "b", extra=f'style="fill:{RED}"')
b += label(420, 72, "통이미지 (현재)", 13.5, "b")
for k in range(4):
    y = 88 + k * 34
    b += f'<rect x="420" y="{y}" width="230" height="34" fill="{PHONE}"/><rect x="428" y="{y}" width="214" height="34" fill="{SCREEN}"/>'
    b += f'<rect x="438" y="{y+6}" width="194" height="22" rx="6" fill="{CARD}"/>'
b += label(420, 236, "✓ 모든 줄이 같은 비율로 줄어 폰 모양 유지", 12.5, "b", extra=f'style="fill:{GREEN}"')
b += label(24, 290, "스토어 버튼처럼 링크가 여러 개 필요하면 '한 줄 = 링크 하나'로 나눈다. 아이콘은 두 줄에 반씩 그려 하나로 보이게 한다.", 12)
write("04-mobile.svg", svg(W, H, b))

# 5. GitHub 앱 대비 ---------------------------------------------------------------
W, H = 760, 300
b = label(24, 36, "⑤ GitHub 앱 대비 — 애니메이션이 없어도 기본값이 완성된 화면", 16, "b")
cols = [("이전: 겹쳐 그려짐", RED, ["Flutter로 구조가 탄탄한 앱을 만들어요", "GetX · Bloc · Riverpod 다 써봤어요",
                                   "Clean Architecture를 좋아합니다", "Music is Life 🎧"], True),
        ("현재: 첫 문구만 보임", GREEN, ["Flutter로 구조가 탄탄한 앱을 만들어요"], False)]
for c, (title, color, lines, overlap) in enumerate(cols):
    x = 40 + c * 360
    b += label(x, 74, title, 13.5, "b", extra=f'style="fill:{color}"')
    b += f'<rect x="{x}" y="88" width="320" height="40" rx="10" fill="{SCREEN}"/>'
    for t in lines:
        b += f'<text x="{x+16}" y="113" font-size="13" style="fill:#EEF0F6;fill-opacity:{0.55 if overlap else 1}">{t}</text>'
b += (f'<rect x="24" y="156" width="712" height="118" rx="12" fill="#fff" stroke="{LINE}"/>'
      + label(44, 184, "웹 브라우저: SMIL 애니메이션 재생 → 문구가 차례로 타이핑됨", 12.5)
      + label(44, 208, "GitHub 앱: 애니메이션 · 글자 클립 미지원 → SVG의 기본값만 그려짐", 12.5)
      + label(44, 236, "→ 기본값을 '완성된 상태'로: 타이핑은 첫 줄만, 스위치는 ON, 그래프는 다 그려짐, 그림자는 filter 대신 도형", 12.5, "b")
      + label(44, 260, "→ 외부 이미지를 못 불러오므로 프로필 사진·앱 아이콘은 base64로 SVG 안에 넣음", 12.5, "b"))
write("05-app-fallback.svg", svg(W, H, b))

# 6. 캐시 ----------------------------------------------------------------------
W, H = 760, 270
b = label(24, 36, "⑥ 캐시 — 내용이 바뀌면 주소도 바뀌게 (?v=내용 해시)", 16, "b")
b += label(40, 74, "같은 주소", 13.5, "b", extra=f'style="fill:{RED}"')
b += box(40, 88, 220, 52, "nav.svg", "주소 그대로", RED, True)
b += arrow(262, 114, 318, 114)
b += box(320, 88, 190, 52, "CDN · 브라우저 · 앱", "max-age=300 캐시", AMBER)
b += arrow(512, 114, 568, 114)
b += box(570, 88, 160, 52, "예전 그림 ✕", "", RED)
b += label(40, 176, "내용 해시", 13.5, "b", extra=f'style="fill:{GREEN}"')
b += box(40, 190, 220, 52, "nav.svg?v=33a9aa8d", "디자인 바뀌면 해시도 바뀜", GREEN, True)
b += arrow(262, 216, 318, 216)
b += box(320, 190, 190, 52, "처음 보는 주소", "캐시를 건너뜀", BLUE)
b += arrow(512, 216, 568, 216)
b += box(570, 190, 160, 52, "새 그림 ✓", "", GREEN)
write("06-cache.svg", svg(W, H, b))

print("generated:", sorted(os.listdir(OUT)))
