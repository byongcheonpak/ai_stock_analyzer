#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 주식 포트폴리오 분석 스크립트

사용법:
    python ai_stock_analyzer.py

의존성:
    pip install yfinance==0.2.50

환경변수:
    PYTHONUTF8=1: Windows에서 한글 출력 문제 해결용 (선택사항)

주의사항:
    - 실제 주식 데이터를 수집하여 분석합니다
    - API 호출 제한을 고려하여 적절한 지연 시간을 적용했습니다
"""

import os
import sys
import time
import yfinance as yf
import pandas as pd
from typing import Dict, Any

# Windows 인코딩 문제 해결
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


# 하드코딩된 티커 리스트
TICKERS = ['AAPL', 'AMZN', 'NVDA', 'V', 'META', 'GOOGL', 'PAVE', 'TSLA', 'MSFT', 'QQQM', 'ORCL', 'AVGO', 'PLTR', 'RKLB', 'BITQ', 'BRK-B', 'WMT']


def get_stock_data(ticker: str) -> Dict[str, Any]:
    """
    yfinance를 사용하여 실제 주식 데이터를 수집합니다.
    
    Args:
        ticker: 주식 티커 심볼
        
    Returns:
        dict: 종목명, 현재가, 52주 최고가, 고점대비하락률, 일 등락율이 포함된 딕셔너리
    """
    try:
        stock = yf.Ticker(ticker)
        
        # 1. 종목명 수집
        stock_name = "N/A"
        try:
            info = stock.info
            if info:
                name = info.get('shortName')
                if name and not pd.isna(name):
                    stock_name = str(name)
        except:
            pass
        
        # 2. 현재가 수집 - 우선순위에 따라 시도
        current_price = None
        
        # 방법 1: fast_info 사용
        try:
            if hasattr(stock, 'fast_info') and hasattr(stock.fast_info, 'last_price'):
                price = stock.fast_info.last_price
                if price and not pd.isna(price):
                    current_price = float(price)
        except:
            pass
        
        # 방법 2: history 사용 (1일)
        if current_price is None:
            try:
                hist = stock.history(period="1d", timeout=10)
                if not hist.empty and 'Close' in hist.columns:
                    current_price = float(hist['Close'].iloc[-1])
            except:
                pass
        
        # 방법 3: info 사용
        if current_price is None:
            try:
                info = stock.info
                if info:
                    price = info.get('currentPrice') or info.get('regularMarketPrice')
                    if price and not pd.isna(price):
                        current_price = float(price)
            except:
                pass
        
        # 3. 52주 최고가 수집 - 우선순위에 따라 시도
        year_high = None
        
        # 방법 1: fast_info 사용
        try:
            if hasattr(stock, 'fast_info') and hasattr(stock.fast_info, 'year_high'):
                high = stock.fast_info.year_high
                if high and not pd.isna(high):
                    year_high = float(high)
        except:
            pass
        
        # 방법 2: info 사용
        if year_high is None:
            try:
                info = stock.info
                if info:
                    high = info.get('fiftyTwoWeekHigh')
                    if high and not pd.isna(high):
                        year_high = float(high)
            except:
                pass
        
        # 4. 고점대비하락률 계산
        drop_rate = "N/A"
        if current_price is not None and year_high is not None and year_high > 0:
            try:
                rate = (year_high - current_price) / year_high * 100
                if not pd.isna(rate):
                    drop_rate = f"-{round(rate, 2)}%"
            except:
                pass
        
        # 5. 일 등락율(정규장) 수집
        daily_change = "N/A"
        try:
            info = stock.info
            if info:
                change_percent = info.get('regularMarketChangePercent')
                if change_percent is not None and not pd.isna(change_percent):
                    daily_change = f"{round(float(change_percent), 2)}%"
        except:
            pass
        
        return {
            'stock_name': stock_name,
            'current_price': current_price,
            'year_high': year_high,
            'drop_rate': drop_rate,
            'daily_change': daily_change
        }
        
    except Exception as e:
        print(f"  {ticker} 데이터 수집 실패: {str(e)[:50]}...")
        return {
            'stock_name': "N/A",
            'current_price': None,
            'year_high': None,
            'drop_rate': "N/A",
            'daily_change': "N/A"
        }


def format_stock_summary(data: Dict[str, Any], ticker: str) -> str:
    """
    수집된 주식 데이터를 포맷합니다.
    
    Args:
        data: get_stock_data에서 반환된 데이터 딕셔너리
        ticker: 주식 티커 심볼
        
    Returns:
        str: 포맷된 결과 문자열
    """
    stock_name = data['stock_name']
    current_price = data['current_price']
    year_high = data['year_high']
    drop_rate = data['drop_rate']
    daily_change = data['daily_change']
    
    price_str = f"${current_price:.2f}" if current_price is not None else "$0"
    high_str = f"${year_high:.2f}" if year_high is not None else "$0"
    drop_str = drop_rate if drop_rate != "N/A" else "-0.00%"
    daily_str = daily_change if daily_change != "N/A" else "0.00%"
    
    # 고점대비하락률에 따른 색상 설정
    def get_drop_color_code(drop_rate_str):
        if drop_rate_str == "N/A" or drop_rate_str == "-0.00%":
            return ""
        
        try:
            # "-12.34%" 에서 숫자 추출
            rate_num = float(drop_rate_str.replace("-", "").replace("%", ""))
            
            if rate_num >= 10:
                return "\033[95m"  # 보라색 (10% 이상)
            else:
                return ""
        except:
            return ""
    
    # 일등락율에 따른 색상 설정
    def get_daily_color_code(daily_change_str):
        if daily_change_str == "N/A" or daily_change_str == "0.00%":
            return "\033[94m"  # 파란색 (기본)
        
        try:
            # "1.25%" 또는 "-1.25%" 에서 숫자 추출
            rate_num = float(daily_change_str.replace("%", ""))
            
            if rate_num < 0:
                return "\033[91m"  # 빨간색 (마이너스)
            else:
                return "\033[94m"  # 파란색 (플러스 또는 0)
        except:
            return "\033[94m"  # 기본 파란색
    
    drop_color_code = get_drop_color_code(drop_str)
    daily_color_code = get_daily_color_code(daily_str)
    reset_code = "\033[0m"
    
    colored_drop_str = f"{drop_color_code}{drop_str}{reset_code}" if drop_color_code else drop_str
    colored_daily_str = f"{daily_color_code}{daily_str}{reset_code}"
    
    return f"""=== {ticker}({stock_name}) ===
현재가 : {price_str}
52주 최고가 : {high_str}
고점대비하락률 : {colored_drop_str}
일 등락율 : {colored_daily_str}"""


def main():
    """메인 실행 함수"""
    print("Python 주식 포트폴리오 분석을 시작합니다...\n")
    
    for i, ticker in enumerate(TICKERS):
        # 1. 주식 데이터 수집
        stock_data = get_stock_data(ticker)
        
        # 2. 결과 포맷팅 및 출력
        result = format_stock_summary(stock_data, ticker)
        print(result)
        print("\n---")
        
        # 3. API 호출 간 지연 (0.5초)
        if i < len(TICKERS) - 1:  # 마지막 티커가 아닌 경우에만 지연
            time.sleep(0.5)
    
    print("모든 분석이 완료되었습니다!")


if __name__ == "__main__":
    main()