from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "calculator-report.pdf"
FONT = r"C:\Windows\Fonts\arial.ttf"
FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
pdfmetrics.registerFont(TTFont("Arial", FONT))
pdfmetrics.registerFont(TTFont("Arial-Bold", FONT_BOLD))
pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold", italic="Arial", boldItalic="Arial-Bold")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="BodyUA", fontName="Arial", fontSize=10, leading=14, alignment=TA_JUSTIFY, spaceAfter=7, textColor=colors.HexColor("#253643")))
styles.add(ParagraphStyle(name="HeadUA", fontName="Arial-Bold", fontSize=15, leading=19, spaceBefore=5, spaceAfter=8, textColor=colors.HexColor("#17324A")))
styles.add(ParagraphStyle(name="SubUA", fontName="Arial-Bold", fontSize=11, leading=15, spaceBefore=4, spaceAfter=4, textColor=colors.HexColor("#28516F")))
styles.add(ParagraphStyle(name="SmallUA", fontName="Arial", fontSize=8.5, leading=11, textColor=colors.HexColor("#465866")))
styles.add(ParagraphStyle(name="CoverUA", fontName="Arial-Bold", fontSize=21, leading=27, alignment=TA_CENTER, textColor=colors.HexColor("#17324A")))
styles.add(ParagraphStyle(name="CenterUA", fontName="Arial", fontSize=12, leading=19, alignment=TA_CENTER, textColor=colors.HexColor("#263746")))
styles.add(ParagraphStyle(name="TableUA", fontName="Arial", fontSize=8.5, leading=11, textColor=colors.HexColor("#253643")))
styles.add(ParagraphStyle(name="TableHeadUA", fontName="Arial-Bold", fontSize=8.7, leading=11, textColor=colors.HexColor("#17324A")))

def p(text, style="BodyUA"):
    return Paragraph(text, styles[style])

def make_table(rows, widths):
    data = [[p(str(cell), "TableHeadUA" if i == 0 else "TableUA") for cell in row] for i, row in enumerate(rows)]
    table = Table(data, colWidths=widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCEAF3")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#9AAEBB")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return table

doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=18*mm, bottomMargin=22*mm,
                        title="Практична робота — Calculator", author="Єфіменко Максим Олександрович")

def footer(canvas, document):
    canvas.saveState()
    width, _ = A4
    canvas.setStrokeColor(colors.HexColor("#D0DCE4"))
    canvas.line(20*mm, 15*mm, width-20*mm, 15*mm)
    canvas.setFont("Arial", 8)
    canvas.setFillColor(colors.HexColor("#667784"))
    canvas.drawString(20*mm, 10*mm, "Практична робота • Java • ПД-35")
    canvas.drawRightString(width-20*mm, 10*mm, str(document.page))
    canvas.restoreState()

story = [
    Spacer(1, 14*mm),
    p("Виконав: Єфіменко Максим Олександрович<br/>Група: ПД-35<br/>Викладач: Шахматов Іван Олександрович", "CenterUA"),
    Spacer(1, 30*mm), p("ПРАКТИЧНА РОБОТА", "CoverUA"),
    Spacer(1, 5*mm), p("Обробка виключень у Java", "CenterUA"),
    Spacer(1, 15*mm), p("Розробка консольного застосунку<br/><b>«Calculator»</b>", "CenterUA"),
    Spacer(1, 40*mm), p("Київ • 2026", "CenterUA"), PageBreak(),
    p("1. Мета та постановка задачі", "HeadUA"),
    p("Мета роботи — реалізувати базові арифметичні операції, перевірку вхідних даних і обробку виняткових ситуацій засобами Java. Програма має взаємодіяти з користувачем через консоль, повідомляти про помилки та завершувати обробку запиту передбачувано."),
    p("2. Реалізація", "HeadUA"),
    make_table([
        ["Компонент", "Реалізація"],
        ["Calculator", "Методи add, subtract, multiply та divide працюють із double. Перед обчисленням перевіряється скінченність обох аргументів."],
        ["Ділення на нуль", "Метод divide кидає ArithmeticException для +0.0 та -0.0."],
        ["InvalidInputException", "Власний виняток для NaN та нескінченних чисел, тексту замість числа й невідомого оператора."],
        ["Main", "Зчитує два числа й операцію, виконує обчислення, обробляє помилки у catch і завжди друкує фінальне повідомлення у finally."],
        ["Тести", "JUnit 5 перевіряє арифметику, помилки вводу, невідому операцію та ділення на нуль."],
    ], [43*mm, 127*mm]),
    Spacer(1, 5*mm),
    p("Обробка числового тексту відокремлена від арифметики: parseNumber перетворює рядок на double та загортає NumberFormatException у InvalidInputException із зрозумілим повідомленням. Арифметичний клас не залежить від консолі, тому його методи можна використовувати окремо."),
    p("3. Структура проєкту", "HeadUA"),
    make_table([
        ["Файл", "Призначення"],
        ["Calculator.java", "Арифметичні операції та перевірка чисел."],
        ["InvalidInputException.java", "Власний тип помилки для некоректних значень і команд."],
        ["Main.java", "Консольний ввід, вибір операції, повідомлення catch/finally."],
        ["CalculatorTest.java", "Перевірка чотирьох операцій, ділення на нуль і нескінченних значень."],
        ["MainTest.java", "Перевірка числового парсингу, тексту, NaN та невідомої операції."],
    ], [48*mm, 122*mm]),
    PageBreak(),
    p("4. Тестові випадки", "HeadUA"),
    make_table([
        ["Сценарій", "Очікувана поведінка"],
        ["3 + 4.5; 3 − 4.5; 3 × 4.5; 9 ÷ 4.5", "Відповідно 7.5; −1.5; 13.5; 2.0."],
        ["Ділення 5 на 0 або −0", "ArithmeticException."],
        ["Рядок abc замість числа", "InvalidInputException із повідомленням, що текст не є числом."],
        ["NaN / нескінченність", "InvalidInputException до виконання арифметичної операції."],
        ["Оператор %", "InvalidInputException із повідомленням про невідому операцію."],
        ["Завершення запиту", "У блоці finally виводиться повідомлення про завершення обробки."],
    ], [58*mm, 112*mm]),
    Spacer(1, 8*mm), p("5. Приклад взаємодії", "HeadUA"),
    make_table([
        ["Ввід / повідомлення", "Приклад"],
        ["Перше число", "9"], ["Друге число", "4.5"], ["Операція", "/"],
        ["Результат", "2.0"], ["Завершення", "Обробку запиту завершено."],
    ], [58*mm, 112*mm]),
    Spacer(1, 8*mm), p("6. Висновок", "HeadUA"),
    p("Створено консольний калькулятор для додавання, віднімання, множення та ділення. Некоректні числові дані й невідомі операції обробляються власним InvalidInputException, а ділення на нуль — ArithmeticException. Підготовлено модульні тести JUnit 5 для основних функцій та помилкових сценаріїв."),
    p("Для запуску потрібні JDK 17+ і Maven 3.8+: команди mvn test та mvn exec:java. У середовищі підготовки не було встановлено JDK/Maven, тому компіляцію і тести тут не запускали.", "SmallUA"),
]

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
