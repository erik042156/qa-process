---
문서유형: Automation Candidate Evaluation
상태: 자동화대상확정   # 평가중 | 사용자검토완료 | 자동화대상확정
대상 TC 문서: docs/tc/product-search.md
대상 TC 문서 최근 변경일(평가 시점 기준): 2026-08-22
관련 Feature PRD: feature/product-search.md
Google Sheet 워크시트: Automation Candidates
최초 작성일: 2026-08-24
최근 변경일: 2026-08-27
최근 Sheet 동기화일: 2026-08-24
확정일: 2026-08-27
---

# Automation Candidate 평가 - 상품 검색

## AI 평가 결과 (AI 작성 영역 — Google Sheet와 동기화됨)

| TC ID | Business Criticality | Regression Frequency | Automation Stability | Result Determinism | Manual Test Cost | Maintenance Cost | Automation Score | Candidate (AI) | 선정/제외 사유 |
|---|---|---|---|---|---|---|---|---|---|
| TC-PRODUCT-SEARCH-001 | 4 | 4 | 4 | 5 | 2 | 2 | 23 | Yes | 검색 실행 시 URL 변경/섹션 제목 변경/매칭 필터링이 동시에 맞물려야 하는 검색 기능의 핵심 진입점이며 다른 검색 TC(002~009)의 전제가 되는 시나리오(BC4). 매 Release 반복 검증 가치가 크고(RF4) URL/제목/DOM으로 결정적 판정 가능(RD5), 자동화/유지 비용도 낮아(MTC2, MC2) 자동화 적극 권장. |
| TC-PRODUCT-SEARCH-002 | 4 | 3 | 4 | 4 | 2 | 2 | 21 | Yes | 검색 결과 카드(이미지/가격/상품명/Add to cart/View Product)는 핵심 상품 탐색·구매 진입 UI 요소로(BC4), `page-ui.md` TC-PAGE-UI-015(ALL PRODUCTS 그리드 카드 구성, Approved)와 검증 대상 컴포넌트는 동일하나 검색 결과 필터링 경로에서 카드가 누락 없이 렌더링되는지는 별도 Risk Coverage(Skill 4.3)로 판단해 중복 제외하지 않음. 다만 이미 검증된 컴포넌트 재사용이라는 점에서 Automation Score 산정 시 여러 축을 크게 낮추지는 않되 후순위로 고려될 여지가 있어 사유에 명시함. |
| TC-PRODUCT-SEARCH-003 | 2 | 3 | 4 | 5 | 2 | 2 | 20 | Yes | 매칭 결과 없을 때 별도 "결과 없음" 안내 문구 없이 빈 목록만 노출되는 PRD 확정 동작으로, 실패해도 영향은 제한적이나(BC2) 조건부 렌더링을 DOM으로 결정적 판정 가능(RD5)하고 자동화/유지 비용이 낮아(MTC2, MC2) 경계 케이스 회귀 가치가 있어 자동화 권장. |
| TC-PRODUCT-SEARCH-004 | 2 | 3 | 4 | 5 | 2 | 2 | 20 | Yes | 빈 검색어 실행 시 전체 상품 노출 및 `?search=` URL 유지라는 경계값(Boundary) 동작으로 영향은 제한적이나(BC2) URL 문자열로 결정적 판정 가능(RD5)하고 비용이 낮아(MTC2, MC2) 자동화 권장. |
| TC-PRODUCT-SEARCH-005 | 4 | 4 | 4 | 5 | 2 | 2 | 23 | Yes | 부분 일치(substring) 매칭은 검색 기능의 핵심 로직으로 실패 시 검색 결과 신뢰성이 크게 훼손됨(BC4). 매 Release 반복 검증 가치가 크고(RF4) 결과 목록으로 결정적 판정 가능(RD5), 자동화/유지 비용도 낮아(MTC2, MC2) 자동화 적극 권장. |
| TC-PRODUCT-SEARCH-006 | 3 | 3 | 3 | 5 | 3 | 3 | 20 | Yes | 카테고리/브랜드명이 상품명에 포함되지 않는 한 매칭되지 않아야 한다는 검색 로직의 경계(scope) 확인으로, 오매칭 시 검색 신뢰성이 훼손됨(BC3). 다만 특정 브랜드명(`biba`/`kookie`/`allen`/`babyhug`)·카테고리명(`TOPS`)이 실제 상품명에 포함되지 않는다는 전제가 상품 데이터 변경에 따라 깨질 수 있어 Automation Stability(AS3)와 Maintenance Cost(MC3, 데이터 의존성) 모두 다소 낮게 산정함. 결과는 DOM 목록으로 결정적 판정 가능(RD5)해 자동화는 권장하되, 상품 데이터 변경 시 테스트 데이터 재검증이 필요함을 유지보수 위험으로 별도 기록. |
| TC-PRODUCT-SEARCH-007 | 2 | 2 | 4 | 4 | 3 | 3 | 18 | Hold | 검색 결과가 페이지네이션 없이 스크롤로 노출되는지 확인하는 시나리오로, 실패해도 영향은 제한적이고(BC2) 반복 검증 우선순위도 낮음(RF2, P2). 동일 패턴을 검증하는 `page-ui.md` TC-PAGE-UI-027(Home FEATURES ITEMS 스크롤 노출)은 사용자가 이미 QA Decision: Rejected로 결정한 바 있어(BC/RF 낮음 사유 동일), 검색 결과라는 별도 Risk Coverage 자체는 인정하되 동일한 저ROI 판단이 반복될 가능성이 높아 사용자 검토를 위해 Hold로 제시함. 다수 상품 매칭 검색어 준비와 스크롤 시뮬레이션으로 수행/유지 비용도 다소 높음(MTC3, MC3). |
| TC-PRODUCT-SEARCH-008 | 3 | 3 | 4 | 5 | 2 | 2 | 21 | Yes | Enter 키 입력 시 검색이 실행되지 않아야 한다는 동작으로, 실패하면 사용자 기대와 다른 화면 전환이 발생하나 돋보기 클릭이라는 대체 경로가 있어 영향은 중간 수준(BC3). URL/제목 불변으로 결정적 판정 가능(RD5)하고 단일 키 입력 이벤트 확인이라 비용이 낮아(MTC2, MC2) 자동화 권장. |
| TC-PRODUCT-SEARCH-009 | 2 | 2 | 4 | 4 | 2 | 3 | 17 | Hold | 검색창에 길이/특수문자 제한이 없다는 PRD 확정 사실을 재확인하는 경계 테스트로, 영향은 제한적이고(BC2) 반복 검증 우선순위도 낮음(RF2). 특수문자가 URL 인코딩되어 나타나 판정 로직에 인코딩 처리가 필요해 유지비용이 다소 있고(MC3), Score도 Hold 구간 하한(17)이라 사용자 검토를 위해 Hold로 제시함. |

## QA Decision (Google Sheet에서 동기화됨 — 사용자 작성 영역, AI는 수정하지 않음)

| TC ID | QA Decision | QA Comment |
|---|---|---|
| TC-PRODUCT-SEARCH-001 | Approved | |
| TC-PRODUCT-SEARCH-002 | Approved | |
| TC-PRODUCT-SEARCH-003 | Approved | |
| TC-PRODUCT-SEARCH-004 | Approved | |
| TC-PRODUCT-SEARCH-005 | Approved | |
| TC-PRODUCT-SEARCH-006 | Approved | |
| TC-PRODUCT-SEARCH-007 | Rejected | |
| TC-PRODUCT-SEARCH-008 | Approved | |
| TC-PRODUCT-SEARCH-009 | Rejected | |

> 이 표는 Google Sheet의 QA Decision/QA Comment 컬럼을 그대로 옮겨온 참고용 스냅샷입니다.
> 실제 값의 Source of Truth는 항상 Google Sheet이며, 이 문서를 직접 수정해도 Sheet에는
> 반영되지 않습니다. 2026-08-27 재조회(candidate-list) 결과 TC-PRODUCT-SEARCH-001~009 전체
> QA Decision이 입력 완료되었음을 확인했습니다(Approved 7건, Rejected 2건, Hold 0건, 미검토
> 0건 — 가공/재해석 없이 Sheet 값 그대로 반영). QA Comment는 전 항목 공란입니다.

## Hard Rule 적용 / Validation 특이사항

- **Hard Rule(5절, 결함을 정상처럼 고정한 TC) 해당 항목 없음**: `product-search.md` 문서 자체가
  "결함 의심으로 표시된 REQ 항목이 없다"고 명시하고 있으며, 평가 과정에서도 현재 발생 중인 결함을
  정상 Expected Result로 고정한 TC는 발견되지 않았습니다.
- **Cross-Feature 중복 검토 결과(사용자 요청에 따른 확인)**: `page-ui.md`의 CATEGORY/BRANDS
  필터링 관련 TC(TC-PAGE-UI-023~033 등, 사이드바에서 카테고리/브랜드 클릭 시 상품 목록 페이지로
  이동해 필터링되는 시나리오)와 `product-search.md`의 TC-PRODUCT-SEARCH-006(검색창에 카테고리/
  브랜드명 키워드를 입력해도 상품명에 없으면 매칭되지 않음을 확인)을 비교한 결과, **검증 목적이
  서로 다릅니다**: page-ui TC들은 "카테고리/브랜드 네비게이션 클릭 시 해당 카테고리/브랜드
  상품만 필터링되는지"를 검증하는 반면, TC-PRODUCT-SEARCH-006은 "검색창 텍스트 매칭이 상품명
  필드에만 적용되고 카테고리/브랜드 필드에는 적용되지 않는지"를 검증합니다. TC-PAGE-UI-040/041과
  cart.md TC-CART-012/013처럼 Test Steps가 사실상 동일한 수준의 중복은 아니라고 판단해
  TC-PRODUCT-SEARCH-006은 Cross-Feature 중복으로 표시하지 않았습니다.
- **부분적 컴포넌트 재사용 중복 검토**: TC-PRODUCT-SEARCH-002(검색 결과 카드 구성)는
  `page-ui.md` TC-PAGE-UI-015(ALL PRODUCTS 그리드 카드 구성, QA Decision: Approved)와 동일한
  카드 컴포넌트를 검증하지만, 검색 결과 필터링 경로에서의 렌더링을 확인한다는 별도 Risk
  Coverage가 있어 완전한 중복(Skill 4.3)으로는 보지 않았습니다. 다만 이미 검증된 컴포넌트
  재사용이라는 점은 위 표의 사유에 명시했으니 사용자 검토 시 참고 바랍니다.
- **동일 패턴 저ROI 선례 검토**: TC-PRODUCT-SEARCH-007(검색 결과 스크롤 노출)은 `page-ui.md`
  TC-PAGE-UI-027(Home FEATURES ITEMS 스크롤 노출)과 동일한 "페이지네이션 없이 스크롤로 노출"
  패턴을 검증하며, TC-PAGE-UI-027은 사용자가 이미 QA Decision: Rejected로 확정한 바 있습니다.
  완전한 중복은 아니라고 판단해 후보 표에는 포함했으나(Hold), 유사 선례가 있다는 점을 참고
  사항으로 기록합니다.
- 그 외 TC(001, 003, 004, 005, 008, 009)는 login-logout/cart/page-ui의 확정된 TC 목록과
  비교했을 때 검증 대상(검색 URL/제목/필터링 로직, 빈 검색어 처리, substring 매칭, Enter 키
  무시, 입력값 제한 없음)이 겹치지 않아 별도 중복 이슈는 발견되지 않았습니다.

- **자동화 대상 확정 시점 Validation 결과(2026-08-27, 사용자의 "QA 승인이 전부 되어있다면
  확정해주세요" 요청에 따른 재조회 및 확정 처리)**:
  1. TC ID 유효성/중복: Sheet의 TC-PRODUCT-SEARCH-001~009(9건)이 `docs/tc/product-search.md`에
     실제로 존재하는 TC ID와 1:1로 정확히 일치하며, Sheet 내 중복 없음을 확인.
  2. QA Decision 값 검증: 9건 전체가 정확히 `Approved`(7건) 또는 `Rejected`(2건)이며, `Hold`나
     미검토(빈 값), 그 외 잘못된 값(Validation Error)은 없음을 확인.
  3. 원본 TC 문서 상태: `docs/tc/product-search.md`의 `상태`가 여전히 `승인완료`임을 확인.
  4. TC 변경 여부: 프런트매터의 "대상 TC 문서 최근 변경일(평가 시점 기준)"(2026-08-22)과 현재
     `docs/tc/product-search.md`의 `최근 변경일`(2026-08-22)이 동일해, 평가 이후 원본 TC 문서가
     변경되지 않았음을 확인.
  - 4개 항목 모두 통과하여 Approved 7건을 자동화 대상으로 확정함(Hold 0건, Rejected 2건). 참고로
    TC-PRODUCT-SEARCH-007(Hold로 제시했던 TC)은 QA Decision이 `Rejected`로 결정되어 확정
    대상에서 제외됨.

## Approved TC 목록 (자동화 대상 확정)

2026-08-27 확정. QA Decision이 `Approved`인 아래 7건만 자동화 대상으로 확정합니다(Rejected
2건은 확정하지 않음, Hold는 이번 평가에서 0건).

| TC ID | Automation Score | Candidate (AI) | QA Decision |
|---|---|---|---|
| TC-PRODUCT-SEARCH-001 | 23 | Yes | Approved |
| TC-PRODUCT-SEARCH-002 | 21 | Yes | Approved |
| TC-PRODUCT-SEARCH-003 | 20 | Yes | Approved |
| TC-PRODUCT-SEARCH-004 | 20 | Yes | Approved |
| TC-PRODUCT-SEARCH-005 | 23 | Yes | Approved |
| TC-PRODUCT-SEARCH-006 | 20 | Yes | Approved |
| TC-PRODUCT-SEARCH-008 | 21 | Yes | Approved |

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-08-24 | 승인완료된 TC 문서(`docs/tc/product-search.md`, TC-PRODUCT-SEARCH-001~009)를 대상으로 automation-candidate Skill 6개 축 1차 평가 수행. Hard Rule 해당 항목 없음. Yes 7건 / Hold 2건 / No 0건. 사용자 요청에 따라 login-logout/cart/page-ui(특히 CATEGORY/BRANDS 필터링 TC)와의 Cross-Feature 중복 여부를 검토했으며, page-ui TC-PAGE-UI-040/041 수준의 완전한 중복은 발견되지 않았으나 TC-PRODUCT-SEARCH-002(카드 컴포넌트 재사용)와 TC-PRODUCT-SEARCH-007(스크롤 노출 패턴, page-ui TC-PAGE-UI-027 Rejected 선례 있음)에 부분적 중복/저ROI 참고사항을 기록함. | 평가중 |
| 2026-08-27 | 사용자의 명시적 "자동화 대상 확정" 요청에 따라 Google Sheet 재조회(candidate-list) 수행. TC-PRODUCT-SEARCH-001~009 전체 QA Decision이 입력 완료(Approved 7건, Rejected 2건, Hold 0건, 미검토 0건)됨을 확인. TC ID 유효성/중복, QA Decision 값, 원본 TC 승인완료 상태, TC 변경 여부 Validation을 모두 통과해 Approved 7건(001~006, 008)을 자동화 대상으로 확정(007, 009는 Rejected로 제외). | 자동화대상확정 |
