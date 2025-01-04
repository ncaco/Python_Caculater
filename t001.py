import sys
from PyQt5.QtWidgets import *  # PyQt5의 위젯 관련 모듈 import
from PyQt5.QtCore import *     # PyQt5의 코어 기능 관련 모듈 import
from PyQt5.QtGui import QIcon

"""
5분만에 계산기 만들기.
PyQt5를 이용한 계산기 애플리케이션
기본적인 사칙연산과 소수점 계산이 가능한 계산기입니다.
"""
class Calculator(QWidget):
    def __init__(self): 
        super().__init__()  # 부모 클래스 초기화
        # 계산을 위한 변수들 초기화
        self.num_buffer = ''
        self.result = 0
        self.new_number = True
        self.pending_operation = ''
        self.memory = 0
        self.history = []
        self.expression = ''
        self.memButtons = {}  # 메모리 버튼 딕셔너리 초기화
        self.initUI()
        
    def initUI(self):
        # 디스플레이 위젯 초기화
        self.expression_display = QLineEdit('')
        self.expression_display.setReadOnly(True)
        self.expression_display.setAlignment(Qt.AlignRight)
        self.expression_display.setObjectName("expression")

        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(18)
        self.display.setObjectName("result")

        # 스타일시트 수정
        self.setStyleSheet("""
            QWidget {
                background-color: #F0F0F0;
                font-family: 'Segoe UI', sans-serif;
            }
            QLineEdit#expression {
                border: none;
                padding: 5px 20px;
                font-size: 12px;
                color: #666666;
                background-color: transparent;
                margin: 0;
            }
            QLineEdit#result {
                border: none;
                padding: 0 10px 15px 10px;
                font-size: 28px;
                font-weight: 500;
                color: #1A1A1A;
                background-color: transparent;
                margin-bottom: 5px;
            }
            QPushButton {
                border: none;
                border-radius: 4px;
                font-size: 16px;
                font-weight: 500;
                color: #1A1A1A;
                background-color: #FFFFFF;
                min-width: 64px;
                min-height: 48px;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #E6E6E6;
            }
            QPushButton:pressed {
                background-color: #D9D9D9;
            }
            QPushButton#memory {
                background-color: transparent;
                color: #666666;
                font-size: 14px;
                min-height: 36px;
            }
            QPushButton#memory:hover {
                background-color: #E6E6E6;
            }
            QPushButton#operator {
                background-color: #F8F8F8;
            }
            QPushButton#equal {
                background-color: #0078D4;
                color: white;
            }
            QPushButton#equal:hover {
                background-color: #006ABC;
            }
        """)

        # 버튼 매핑 딕셔너리 초기화
        self.buttons = {}

        # 연산자 버튼 생성 및 매핑
        operators = [
            ('%', '%'), ('CE', 'CE'), ('C', 'C'), ('⌫', '←'),
            ('¹/x', '1/x'), ('x²', 'x²'), ('√x', '√'), ('÷', '÷'),
            ('7', '7'), ('8', '8'), ('9', '9'), ('×', '×'),
            ('4', '4'), ('5', '5'), ('6', '6'), ('-', '－'),
            ('1', '1'), ('2', '2'), ('3', '3'), ('+', '＋'),
            ('+/-', '±'), ('0', '0'), ('.', '.'), ('=', '＝')
        ]

        # 메모리 버튼 정의
        memory_buttons = ['MC', 'MR', 'M+', 'M-', 'MS', 'M▾']

        # 메이아웃 설정
        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(0)
        mainLayout.setContentsMargins(10, 10, 10, 10)

        # 메스플레이 레이아웃
        displayLayout = QVBoxLayout()
        displayLayout.addWidget(self.expression_display)
        displayLayout.addWidget(self.display)
        displayLayout.setSpacing(0)
        mainLayout.addLayout(displayLayout)

        # 메모리 버튼 레이아웃
        memLayout = QHBoxLayout()
        memLayout.setSpacing(2)
        for mem in memory_buttons:
            btn = QPushButton(mem)
            btn.setObjectName('memory')
            self.memButtons[mem] = btn
            memLayout.addWidget(btn)
        mainLayout.addLayout(memLayout)

        # 버튼 그리드
        grid = QGridLayout()
        grid.setSpacing(2)
        
        # 버튼 배치 및 이벤트 연결
        for i, (text, op) in enumerate(operators):
            btn = QPushButton(text)
            self.buttons[text] = btn  # 버튼 저장
            
            if text == '=':
                btn.setObjectName('equal')
            elif text in ['÷', '×', '-', '+']:
                btn.setObjectName('operator')
            
            grid.addWidget(btn, i//4 + 1, i%4)
            
            # 버튼 이벤트 연결
            if text.isdigit():
                btn.clicked.connect(self.numClicked)
            elif text in ['÷', '×', '-', '+']:
                btn.clicked.connect(self.operatorClicked)
            elif text == '=':
                btn.clicked.connect(self.equalClicked)
            elif text == '.':
                btn.clicked.connect(self.pointClicked)
            elif text == 'C':
                btn.clicked.connect(self.clearClicked)
            elif text == 'CE':
                btn.clicked.connect(self.clearEntryClicked)
            elif text == '⌫':
                btn.clicked.connect(self.backspaceClicked)
            elif text == '±':
                btn.clicked.connect(self.toggleSign)
            elif text == 'x²':
                btn.clicked.connect(self.square)
            elif text == '√x':
                btn.clicked.connect(self.squareRoot)
            elif text == '¹/x':
                btn.clicked.connect(self.reciprocal)
            elif text == '%':
                btn.clicked.connect(self.percentage)

        mainLayout.addLayout(grid)
        self.setLayout(mainLayout)

        # 윈도우 설정
        self.setWindowTitle('5분만에 만든 계산기')
        self.setFixedSize(320, 500)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        # 윈도우 아이콘 설정
        app_icon = QIcon('./test/img.ico')
        self.setWindowIcon(app_icon)
        
        # 메모리 버튼 이벤트 연결
        if hasattr(self, 'memButtons'):
            self.memButtons['MC'].clicked.connect(lambda: self.handleError('not_implemented'))
            self.memButtons['MR'].clicked.connect(lambda: self.handleError('not_implemented'))
            self.memButtons['MS'].clicked.connect(lambda: self.handleError('not_implemented'))
            self.memButtons['M+'].clicked.connect(lambda: self.handleError('not_implemented'))
            self.memButtons['M-'].clicked.connect(lambda: self.handleError('not_implemented'))
        
        self.show()
        
    def numClicked(self):
        """숫자 버튼 클릭 시 호출되는 함수"""
        if len(self.display.text()) >= 15:  # 최대 자릿수 제한
            return
        button = self.sender()
        digit = button.text()
        
        if self.new_number:  # 새로운 숫자 입력 시작
            self.display.setText(digit)
            if not self.pending_operation:  # 새로운 계산 시작
                self.expression = ''
                self.expression_display.setText('')
            self.new_number = False
        else:  # 기존 숫자에 이어서 입력
            current_text = self.display.text()
            if current_text == '0' and digit != '.':  # 첫 숫자가 0인 경우 (소수점이 아닐 때만)
                self.display.setText(digit)
            else:
                self.display.setText(current_text + digit)
    
    def operatorClicked(self):
        """연산자 버튼 클릭 시 호출되는 함수"""
        try:
            current_text = self.display.text()
            button = self.sender()
            op = button.text()

            if self.new_number and self.pending_operation:
                # 연산자만 변경하는 경우
                self.pending_operation = op
                self.expression = self.expression[:-1] + op
                self.expression_display.setText(self.expression)
                return

            if not self.expression:
                self.expression = current_text + ' ' + op
            else:
                if self.pending_operation:
                    self.calculateResult()
                self.expression += ' ' + op

            self.expression_display.setText(self.expression)
            self.num_buffer = float(current_text)
            self.pending_operation = op
            self.new_number = True
            self.result = float(current_text)

        except ValueError:
            self.display.setText('Error')
            return
    
    def calculateResult(self):
        """실제 계산을 수행하는 함수"""
        try:
            from decimal import Decimal, InvalidOperation, getcontext
            # 정밀도 설정
            getcontext().prec = 28
            
            current = Decimal(str(self.display.text()))
            result = Decimal(str(self.result))
            
            if self.pending_operation == '＋':
                self.result = float(result + current)
            elif self.pending_operation == '－':
                self.result = float(result - current)
            elif self.pending_operation == '×':
                self.result = float(result * current)
            elif self.pending_operation == '÷':
                if current == 0:
                    raise ZeroDivisionError
                self.result = float(result / current)
                
            if abs(self.result) > 1e15:
                raise OverflowError
            
            # 정수인 경우와 소수인 경우 처리
            if float(self.result).is_integer():
                self.display.setText(str(int(self.result)))
            else:
                # 소수점 16자리로 반올림하고 불필요한 0 제거
                formatted_result = '{:.16f}'.format(self.result)
                # 마지막 문자가 소수점이면 제거
                if formatted_result.endswith('.'):
                    formatted_result = formatted_result[:-1]
                # 결과가 너무 길면 지수 표기법 사용
                if len(formatted_result) > 18:
                    formatted_result = '{:.10e}'.format(self.result)
                self.display.setText(formatted_result)
        except (ValueError, InvalidOperation):
            self.display.setText('Error: Invalid Input')
            self.expression = ''
        except ZeroDivisionError:
            self.display.setText('Error: Division by Zero')
            self.expression = ''
        except OverflowError:
            self.display.setText('Error: Result too large')
            self.expression = ''
        except Exception as e:
            self.display.setText('Error')
            self.expression = ''
    
    def equalClicked(self):
        """등호(=) 버튼 클릭 시 호출되는 함수"""
        if self.pending_operation:
            current_text = self.display.text()
            self.expression += ' ' + current_text
            self.expression_display.setText(self.expression + ' =')
            self.calculateResult()
            self.expression = ''
            self.pending_operation = ''
            self.new_number = True
    
    def clearClicked(self):
        """C 버튼 클릭 시 호출되는 함수"""
        self.result = 0
        self.pending_operation = ''
        self.new_number = True
        self.display.setText('0')
        self.expression = ''
        self.expression_display.setText('')
    
    def clearEntryClicked(self):
        """CE 버튼 클릭 시 호출되는 함수 - 현재 입력 초기화"""
        self.display.setText('0')
        self.new_number = True
    
    def backspaceClicked(self):
        """백스페이스 버튼 클릭 시 호출되는 함수"""
        if self.new_number:
            return
        text = self.display.text()
        if len(text) > 1:  # 두 자리 이상일 때
            self.display.setText(text[:-1])
        else:  # 한 자리일 때는 0으로 설정
            self.display.setText('0')
            self.new_number = True
    
    def pointClicked(self):
        """소수점 버튼 클릭 시 호출되는 함수"""
        if self.new_number:
            self.display.setText('0.')
            self.new_number = False
        elif '.' not in self.display.text():  # 소수점이 없을 때만 추가
            self.display.setText(self.display.text() + '.')
    
    def keyPressEvent(self, event):
        """키보드 입력 처리"""
        key_mapping = {
            Qt.Key_0: '0', Qt.Key_1: '1', Qt.Key_2: '2',
            Qt.Key_3: '3', Qt.Key_4: '4', Qt.Key_5: '5',
            Qt.Key_6: '6', Qt.Key_7: '7', Qt.Key_8: '8',
            Qt.Key_9: '9', Qt.Key_Plus: '＋', Qt.Key_Minus: '－',
            Qt.Key_Asterisk: '×', Qt.Key_Slash: '÷',
            Qt.Key_Period: '.', Qt.Key_Enter: '=',
            Qt.Key_Return: '=', Qt.Key_Backspace: '←',
            Qt.Key_Delete: 'C'
        }
        
        if event.key() in key_mapping:
            text = key_mapping[event.key()]
            button = [btn for btn in self.findChildren(QPushButton) if btn.text() == text]
            if button:
                button[0].click()
    
    def memoryClear(self):
        """메모리 초기화"""
        self.memory = 0
        self.expression_display.setText('Memory Cleared')
    
    def memoryRecall(self):
        """메모리에서 값 불러오기"""
        self.display.setText(str(self.memory))
        self.new_number = True
        # 메모리 값 표시
        self.expression_display.setText(f'Memory: {self.memory}')
    
    def memoryStore(self):
        """현재 값을 메모리에 저장"""
        try:
            self.memory = float(self.display.text())
        except ValueError:
            self.display.setText('Error')
    
    def memoryAdd(self):
        """메모리에 현재 값 더하기"""
        try:
            current = float(self.display.text())
            self.memory += current
            self.new_number = True
            # 메모리 상태 표시
            self.expression_display.setText(f'M = {self.memory}')
        except ValueError:
            self.display.setText('Error')

    def handleError(self, error_type):
        """에러 처리를 통합 관리하는 함수"""
        error_messages = {
            'division': 'Error: Division by Zero',
            'overflow': 'Error: Result too large',
            'invalid': 'Error: Invalid Input',
            'generic': 'Error'
        }
        self.display.setText(error_messages.get(error_type, 'Error'))
        self.expression = ''
        self.expression_display.setText('')
        self.new_number = True

    def toggleSign(self):
        """부호 전환"""
        try:
            value = float(self.display.text())
            self.display.setText(str(-value))
        except ValueError:
            self.handleError('invalid')

    def square(self):
        """제곱"""
        try:
            value = float(self.display.text())
            self.display.setText(str(value * value))
            self.new_number = True
        except ValueError:
            self.handleError('invalid')

    def squareRoot(self):
        """제곱근"""
        try:
            value = float(self.display.text())
            if value < 0:
                self.handleError('invalid')
                return
            self.display.setText(str(value ** 0.5))
            self.new_number = True
        except ValueError:
            self.handleError('invalid')

    def reciprocal(self):
        """역수"""
        try:
            value = float(self.display.text())
            if value == 0:
                self.handleError('division')
                return
            self.display.setText(str(1 / value))
            self.new_number = True
        except ValueError:
            self.handleError('invalid')

    def percentage(self):
        """퍼센트"""
        try:
            value = float(self.display.text())
            self.display.setText(str(value / 100))
            self.new_number = True
        except ValueError:
            self.handleError('invalid')

if __name__ == '__main__':
    app = QApplication(sys.argv)  # Qt 애플리케이션 생성
    calc = Calculator()          # 계산기 인스턴스 생성
    sys.exit(app.exec_())       # 이벤트 루프 시작
