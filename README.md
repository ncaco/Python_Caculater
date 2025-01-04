# Python_Caculater
cursur ai 결제하고 첫 번째로 만든 프로젝트입니다. 감사합니다.

# 계산기 애플리케이션

PyQt5를 이용해 만든 Windows 계산기 클론 애플리케이션입니다.

## 주요 기능

- 기본적인 사칙연산 (더하기, 빼기, 곱하기, 나누기)
- 고급 연산 기능 (제곱, 제곱근, 역수, 퍼센트)
- 메모리 기능 (MC, MR, M+, M-, MS)
- 계산 히스토리 표시
- 항상 위 표시 기능

## 기술 스택

- Python 3.x
- PyQt5
- Qt Designer

## 설치 및 실행 방법

1. Python 설치
   - [Python 공식 웹사이트](https://www.python.org/)에서 Python 3.x 버전을 다운로드하여 설치

2. 필요한 패키지 설치
   ```bash
   pip install PyQt5
   ```

3. 프로그램 실행
   ```bash
   python t001.py
   ```

## 배포 과정

### Windows 실행 파일(.exe) 생성

1. PyInstaller 설치
   ```bash
   pip install pyinstaller
   ```

2. 실행 파일 생성
   ```bash
   pyinstaller --onefile --windowed --icon=img.ico t001.py
   ```

3. dist 폴더에서 생성된 calculator.exe 파일을 실행

### 주의사항
- img.ico 파일이 실행 파일과 같은 경로에 있어야 합니다.
- Windows 10/11에서 테스트되었습니다.


