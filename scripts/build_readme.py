"""README.md 생성기.

모든 행을 폭 464px 통이미지로 두고 <br>로 이어 붙인다. img의 align="top"이 줄 사이 틈을 없애
폰 한 대처럼 보이게 하고, GitHub가 이미지마다 거는 max-width:100% 덕분에 모바일에서도 폰 전체가
같은 비율로 줄어든다. <picture>로 GitHub 라이트/다크 테마에 맞는 세트(assets / assets/light)를 고른다.

이미지 주소에는 파일 내용 해시를 ?v= 로 붙인다. GitHub CDN·브라우저·GitHub 앱이 같은 주소의 이미지를
캐시하므로, 내용이 바뀔 때마다 주소가 달라져야 웹과 앱 모두 곧바로 새 디자인을 받아간다.
SVG를 다시 만들었으면 이 스크립트도 다시 실행해야 한다.

사용법: python3 scripts/build_readme.py  (저장소 루트에서 실행)
"""
import hashlib
GH = "https://github.com/Astrum93"
NOTION = "https://astrum93.notion.site/4cafb9bffadd41aab36297dd738f9e13"
MIL = f"{GH}/music_is_life"
WIDTH = 464

ROWS = [
    ("appbar", GH, "Astrum93 앱 상단 바"),
    ("profile", NOTION, "나정민 · Flutter Developer · @Astrum93 · 실무 경력 1년 10개월"),
    ("section-career", NOTION, "경력"),
    ("card-career", NOTION, "주식회사 엔데버 · 음식점 타임딜 플랫폼 써젯(Sugget) · Flutter 개발 · 2024.09 – 2026.06 (1년 10개월) — "
                            "유저·점주·어드민 앱 3종, 정산 화면 로딩 3분→1초(체감), 토스페이먼츠 결제·취소·정산 연동"),
    ("store-head", NOTION, "스토어에서 만나보기"),
    ("store-user-ios", "https://apps.apple.com/kr/app/id6739319710", "써젯 (유저앱) App Store"),
    ("store-user-play", "https://play.google.com/store/apps/details?id=com.sugget.sugget_user", "써젯 (유저앱) Google Play"),
    ("store-partner-ios", "https://apps.apple.com/kr/app/id6738941397", "써젯 사장님용 (점주앱) App Store"),
    ("store-partner-play", "https://play.google.com/store/apps/details?id=com.sugget.sugget_partner", "써젯 사장님용 (점주앱) Google Play"),
    ("card-work", NOTION, "이런 문제를 풀었어요 — 정산 집계 서버 배치 전환, 정산 상태 분리·누락 감시, 결제 실패 보상 처리, "
                          "가입 시 1회 지오코딩, SMS 인증·탈퇴 순서 보장, Remote Config + flavor, 공통 컴포넌트·클린 아키텍처"),
    ("section-cert", NOTION, "자격 · 수상"),
    ("card-cert", NOTION, "정보처리기사 합격 (2025.09) · 비전공 개발자로 취득"),
    ("card-award", NOTION, "BiG(Busan is Good) Data Hackathon 인기상 (2023.07.08)"),
    ("section-apps", f"{GH}?tab=repositories", "대표 프로젝트"),
    ("card-music", MIL, "Music is Life — 음악으로 연결되는 SNS (Flutter, GetX, Firebase, Spotify)"),
    ("card-coin", f"{GH}/coin_dashboard", "Coin Dashboard — 업비트 시세 대시보드 (GetX, go_router, freezed)"),
    ("card-airticket", f"{GH}/AirTicket", "AirTicket — 클린 아키텍처 연습"),
    ("section-lab", f"{GH}?tab=repositories&q=Todo", "실험실"),
    ("card-todo", f"{GH}?tab=repositories&q=Todo", "Todo Remix Collection — GetX, Bloc, Cubit, Riverpod, Local Data, Remote HTTP, Dart Frog"),
    ("card-stack", f"{MIL}/blob/main/docs/ARCHITECTURE.md",
     "기술 스택 — Flutter, Dart, GetX, Bloc, Riverpod, Firebase, Supabase, Clean Architecture / 경험: Python, Django, Java"),
    ("snackbar", f"{MIL}/blob/main/docs/DEVLOG.md", "music_is_life v2.1.1 업데이트 — 개발 일지 보기"),
    ("nav", GH, "하단 탭바 — 홈 · 레포 · 개발 일지 · 포트폴리오"),
]


def versioned(path):
    with open(path, "rb") as f:
        return f"{path}?v={hashlib.sha1(f.read()).hexdigest()[:8]}"


def row(asset, href, alt):
    return (f'<a href="{href}"><picture>'
            f'<source media="(prefers-color-scheme: light)" srcset="{versioned(f"assets/light/{asset}.svg")}" />'
            f'<img src="{versioned(f"assets/{asset}.svg")}" width="{WIDTH}" align="top" alt="{alt}" />'
            f'</picture></a>')


if __name__ == "__main__":
    body = "<br>\n".join(row(*r) for r in ROWS)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(f'<div align="center">\n{body}\n</div>\n')
    print(f"README.md: {len(ROWS)} rows")
