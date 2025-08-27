Python 주식 포트폴리오 분석 스크립트

사용법:
    python ai_stock_analyzer.py

의존성:
    pip install yfinance==0.2.50

환경변수:
    PYTHONUTF8=1: Windows에서 한글 출력 문제 해결용 (선택사항)

주의사항:
    - 야후파이낸스 api를 통해 실제 주식 데이터를 수집하여 분석합니다
    - API 호출 제한을 고려하여 적절한 지연 시간을 적용했습니다


# 하드코딩된 티커 리스트
TICKERS = ['AAPL', 'AMZN', 'NVDA', 'V', 'META', 'GOOGL', 'PAVE', 'TSLA', 'MSFT', 'QQQM', 'ORCL', 'AVGO', 'PLTR', 'RKLB', 'BITQ', 'BRK-B', 'WMT']
    
