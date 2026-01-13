# BankDressing_Android

뱅크샐러드 거래내역 기반의 가계부 안드로이드 앱입니다.

## 📱 주요 기능

- **엑셀 데이터 업로드**: 뱅크샐러드에서 다운받은 거래내역 엑셀 파일을 업로드
- **거래 내역 관리**: 거래 내역 조회 및 수정 기능
- **과소비 패턴 분석**: 카테고리별, 시간대별, 반복 지출 패턴을 분석하여 과소비 구간 감지
- **과소비 규칙 관리**: 사용자 정의 과소비 규칙 생성 및 관리
- **절약 기회 제안**: 분석 결과를 바탕으로 구체적인 절약 방안 제시
- **소비 성향 분석**: 사용자의 소비 패턴을 분석하여 소비 성향 유형 분류
- **월별 통계**: 월별 지출 통계

## 🛠 기술 스택

### Backend
- **Python 3.10+**
- **FastAPI**: RESTful API 서버
- **Pandas**: 데이터 분석 및 처리
- **Pydantic**: 데이터 검증 및 모델링   
- **Uvicorn**: ASGI 서버

### Frontend
- **Flutter 3.10+**
- **Dart**: 프로그래밍 언어
- **HTTP**: API 통신
- **FL Chart**: 차트 및 그래프 시각화
- **Firebase**: 푸시 알림 및 인증 (구현중)

## 🚀 시작하기
### 프로젝트 가져오기
git clone <repository-url>

### Backend 설정
cd BankDressing/backend
pip install -r requirements.txt

### Frontend 설정
cd BankDressing/frontend
flutter pub get

### 앱 실행하기
1. 애뮬레이터 실행
- flutter emulators --launch [Emulator Name]
3. 배치파일 실행(cmd)
- BankDressing/test-app.bat [Emulator Name]
  ex. c:\01WorkSpace\BankDressing\test-app.bat Pixel_7





이 프로젝트는 개인 프로젝트입니다.
