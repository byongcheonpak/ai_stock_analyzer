# 🐍 Python 주식 포트폴리오 분석 스크립트 제작 요청

### 1. 역할 부여 (Role Assignment)
너는 15년차 Python 개발 전문가야.
yfinance 라이브러리를 사용해서 미국 주식 포트폴리오 분석 스크립트를 작성해줘.
코드는 안정성과 가독성을 최우선으로 작성하고, 예외 처리도 반드시 포함해줘.

### 2. 명확한 목표 (Objective / ASK)
하드코딩된 미국 주식 티커 목록을 기반으로, yfinance 라이브러리로 최신 데이터를 가져오고, 터미널에 출력하는 Python 스크립트를 작성한다.

### 3. 맥락 및 배경 정보 (Context)
- 개발 언어: Python
- 실행 환경: 로컬 컴퓨터의 터미널 (Command Line)
- 사용 목적: 개인 투자 포트폴리오

### 4. 구체적인 지시사항 (Instructions / Constraints)

#### 4.1 의존성/환경
- Python: 3.10–3.12 권장
- 패키지(버전 고정 권장):
    - yfinance==0.2.50
    - google-generativeai==0.7.2
- 설치 예시:
    - pip install yfinance==0.2.50 google-generativeai==0.7.2
- 콘솔 인코딩: Windows 환경에서 한글 출력 문제가 있으면 `PYTHONUTF8=1` 설정을 고려.

#### 4.2 분석 대상 티커 목록
- 코드에 다음 티커 리스트를 하드코딩한다:
    - `['AAPL', 'AMZN', 'NVDA', 'V', 'META', 'GOOGL', 'PAVE', 'TSLA', 'MSFT', 'QQQM', 'ORCL', 'AVGO', 'PLTR', 'RKLB', 'BITQ', 'BRK.B', 'WMT']`

#### 4.3 데이터 수집 함수 (get_stock_data)
- 시그니처: `get_stock_data(ticker: str) -> dict`
- 반환 데이터 항목:
    - 종목명 (예: "Apple", 없으면 "N/A")
    - 현재가 (float 또는 None)
    - 52주 최고가 (float 또는 None)
    - 고점대비하락률(%) 문자열: 유효 시 소수점 둘째 자리 반올림 후 '-12.34%' 형태, 분모 부재/0/NaN이면 'N/A'
    - 일 등락율(정규장) (예: "1.25%", 없으면 "N/A")

- 데이터 소스 및 우선순위:
    - 종목명
        1) 'ticker.info.get('shortName')'
    - 현재가
        1) `ticker.fast_info.last_price`
        2) `ticker.history(period="1d")`의 마지막 행 `Close` (DataFrame 비어있을 수 있으므로 예외 처리)
        3) `ticker.info.get("currentPrice")` 또는 `ticker.info.get("regularMarketPrice")`
    - 52주 최고가
        1) `ticker.fast_info.year_high`
        2) `ticker.info.get("fiftyTwoWeekHigh")`
    - 일 등락율(정규장)
        1) 'ticker.info.get('regularMarketChangePercent ')' 
      
- 계산 규칙:
    - 하락률 = `(year_high - price) / year_high * 100`
    - `year_high`가 None/0/NaN이면 'N/A'
    - 수치가 유효하면 `round(x, 2)` 후 문자열에 `%` 붙여 반환

#### 4.4 실행 흐름 (main)
- 하드코딩된 티커 배열을 순회: `['AAPL', 'AMZN', 'NVDA', 'V']`
- 각 티커에 대해:
    1) `get_stock_data` 호출
    2) `format_stock_summary`로 요약 생성
    3) 결과 출력 후 구분선 `---` 출력
    4) API 호출 간 0.5~1.0초 지연(`time.sleep(0.5)`)으로 과도 호출 방지

    
## 5. 출력 형식 지정 (Output Format)
모든 로직이 포함된, 바로 실행 가능한 단일 Python 스크립트 파일(.py)을 제공해줘.

코드는 단일 코드 블록 안에 작성해줘.

고점대비하락률이 10%이상이면 보라색글자

일등락율이 마이너스이면 빨간글자 그외는 파란글자

입력: 없음 (스크립트 실행 시 바로 동작)

터미널 예상 출력:

=== AAPL(종목명) ===
현재가 : $0
52주 최고가 : $0
고점대비하락률 : -0.00%
일 등락율 : 0.00%

---
=== AMZN(종목명) ===
현재가 : $0
52주 최고가 : $0
고점대비하락률 : -0.00%
일 등락율 : 0.00%

---
(나머지 티커에 대한 리포트가 순차적으로 출력)

### 7. 구현 스펙 초안 (개발 가이드)
- 파일 상단: 사용법/의존성/환경변수 안내를 주석으로 명시
