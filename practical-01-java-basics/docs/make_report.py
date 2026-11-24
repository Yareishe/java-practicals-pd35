from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, KeepTogether, Preformatted
from PIL import Image as PILImage, ImageDraw, ImageFont
import textwrap

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
OUT=DOCS/'Звіт_ПР1_Основи_Java.pdf'
FONT=r'C:\Windows\Fonts\arial.ttf'; FONT_B=r'C:\Windows\Fonts\arialbd.ttf'
pdfmetrics.registerFont(TTFont('Arial',FONT)); pdfmetrics.registerFont(TTFont('Arial-Bold',FONT_B))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='Arial-Bold',italic='Arial',boldItalic='Arial-Bold')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyUA',fontName='Arial',fontSize=10,leading=14,alignment=TA_JUSTIFY,spaceAfter=6,textColor=colors.HexColor('#253643')))
styles.add(ParagraphStyle(name='HeadUA',fontName='Arial-Bold',fontSize=16,leading=20,spaceBefore=3,spaceAfter=8,textColor=colors.HexColor('#17324A')))
styles.add(ParagraphStyle(name='SubUA',fontName='Arial-Bold',fontSize=12,leading=16,spaceBefore=5,spaceAfter=4,textColor=colors.HexColor('#28516F')))
styles.add(ParagraphStyle(name='SmallUA',fontName='Arial',fontSize=8.7,leading=12,textColor=colors.HexColor('#465866')))
styles.add(ParagraphStyle(name='CoverUA',fontName='Arial-Bold',fontSize=21,leading=27,alignment=TA_CENTER,textColor=colors.HexColor('#17324A')))
styles.add(ParagraphStyle(name='CenterUA',fontName='Arial',fontSize=12,leading=19,alignment=TA_CENTER,textColor=colors.HexColor('#263746')))
styles.add(ParagraphStyle(name='CodeUA',fontName='Courier',fontSize=8.2,leading=11,leftIndent=8,rightIndent=8,spaceAfter=5,textColor=colors.HexColor('#203546')))
styles.add(ParagraphStyle(name='ConsoleUA',fontName='Arial',fontSize=8.2,leading=10,leftIndent=6,rightIndent=6,spaceBefore=4,spaceAfter=6,textColor=colors.HexColor('#203546')))
styles.add(ParagraphStyle(name='TableUA',fontName='Arial',fontSize=8.5,leading=11,textColor=colors.HexColor('#253643')))
styles.add(ParagraphStyle(name='TableHeadUA',fontName='Arial-Bold',fontSize=8.8,leading=11,textColor=colors.HexColor('#17324A')))
def P(txt,sty='BodyUA'): return Paragraph(txt,styles[sty])

def draw_model():
    W,H=1800,760
    im=PILImage.new('RGB',(W,H),'#F5F8FB'); d=ImageDraw.Draw(im)
    regular=ImageFont.truetype(FONT,25); bold=ImageFont.truetype(FONT_B,28); small=ImageFont.truetype(FONT,22)
    def box(x,y,w,h,title,lines):
        d.rounded_rectangle((x,y,x+w,y+h),radius=20,fill='#FFFFFF',outline='#47708B',width=4)
        d.rounded_rectangle((x,y,x+w,y+60),radius=18,fill='#DCEAF3',outline='#47708B',width=3)
        d.text((x+w//2,y+29),title,font=bold,fill='#17324A',anchor='mm')
        for i,line in enumerate(lines): d.text((x+22,y+87+i*42),line,font=regular,fill='#253643')
    def arrow(a,b,label):
        import math
        d.line((*a,*b),fill='#A06D39',width=4)
        ang=math.atan2(b[1]-a[1],b[0]-a[0]); n=15
        d.polygon([b,(b[0]-n*math.cos(ang-.5),b[1]-n*math.sin(ang-.5)),(b[0]-n*math.cos(ang+.5),b[1]-n*math.sin(ang+.5))],fill='#A06D39')
        d.text(((a[0]+b[0])//2,(a[1]+b[1])//2-18),label,font=small,fill='#80562F',anchor='mm')
    box(65,80,360,230,'Category',['id: int','name: String'])
    box(510,80,490,360,'Product',['id: int','name: String','price: BigDecimal','description: String','category: Category'])
    box(1100,80,310,300,'Cart',['productId → quantity','add / remove','total / clear'])
    box(1435,80,310,360,'Order',['id / date','item snapshots','total / status'])
    box(300,500,500,200,'StoreService',['catalog / category search','checkout / order history'])
    box(900,500,570,200,'Main',['Scanner CLI','menu / input validation'])
    arrow((425,190),(510,190),'has category')
    arrow((1000,230),(1100,230),'selects')
    arrow((1410,230),(1435,230),'checkout')
    arrow((550,500),(740,440),'business rules')
    arrow((1100,500),(1070,360),'calls')
    p=DOCS/'uml_класів.png'; im.save(p); return p

diagram=draw_model()
doc=SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=18*mm,bottomMargin=21*mm,
    title='Практична робота №1 — Основи Java',author='Єфіменко Максим Олександрович')
def footer(c,d):
    c.saveState(); w,h=A4; c.setStrokeColor(colors.HexColor('#D0DCE4')); c.line(20*mm,15*mm,w-20*mm,15*mm)
    c.setFont('Arial',8); c.setFillColor(colors.HexColor('#667784')); c.drawString(20*mm,10*mm,'Практична робота №1 • Java • ПД-35'); c.drawRightString(w-20*mm,10*mm,str(d.page)); c.restoreState()
story=[Spacer(1,15*mm),P('Виконав: Єфіменко Максим Олександрович<br/>Група: ПД-35<br/>Викладач: Шахматов Іван Олександрович','CenterUA'),
       Spacer(1,30*mm),P('ПРАКТИЧНА РОБОТА №1','CoverUA'),Spacer(1,6*mm),P('Основи Java та синтаксис мови','CenterUA'),
       Spacer(1,18*mm),P('Розробка консольного проєкту<br/><b>«Інтернет-магазин»</b>','CenterUA'),Spacer(1,42*mm),
       P('Київ • 2026','CenterUA'),PageBreak(),
       P('1. Мета та постановка задачі','HeadUA'),
       P('Мета роботи — закріпити основи Java та об’єктно-орієнтованого програмування: створити класи предметної області, інкапсулювати поля, застосувати конструктори, гетери, сетери, колекції, цикли й умовні оператори.'),
       P('За завданням потрібно реалізувати консольний інтернет-магазин, що показує каталог, додає позиції до кошика та оформлює замовлення. Самостійне завдання з матеріалів доповнено видаленням позиції, історією замовлень і пошуком за назвою чи категорією.'),
       P('2. Вимоги та реалізація','HeadUA')]
rows=[['Вимога','Реалізація'],['Product та Category','Інкапсульовані поля, конструктори, перевірка значень, Lombok getters/setters'],['Каталог','Перегляд шести демонстраційних товарів у чотирьох категоріях'],['Кошик','Додавання кількості, перегляд позицій і підсумку, видалення за ID'],['Замовлення','Непорожній кошик формує замовлення зі знімком ціни, датою та статусом'],['Пошук','Частковий збіг за назвою/описом і за назвою категорії'],['Історія','Оформлені замовлення доступні до завершення запуску програми']]
rows=[[P(str(cell),'TableHeadUA' if ri==0 else 'TableUA') for cell in row] for ri,row in enumerate(rows)]
t=Table(rows,colWidths=[42*mm,128*mm],repeatRows=1)
t.setStyle(TableStyle([('FONTNAME',(0,0),(-1,-1),'Arial'),('FONTNAME',(0,0),(-1,0),'Arial-Bold'),('FONTSIZE',(0,0),(-1,-1),8.8),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#DCEAF3')),('TEXTCOLOR',(0,0),(-1,0),colors.HexColor('#17324A')),('GRID',(0,0),(-1,-1),.5,colors.HexColor('#9AAEBB')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
story += [t,Spacer(1,5*mm),P('Вартість зберігається у BigDecimal із двома десятковими знаками, щоб уникнути похибок двійкової арифметики для грошей. Дані каталогу та історії зберігаються в пам’яті процесу.','SmallUA'),PageBreak(),
          P('3. Структура та модель класів','HeadUA'),P('Проєкт поділено на модель предметної області, сервіс бізнес-операцій і консольний інтерфейс.'),
          Image(str(diagram),width=170*mm,height=170*mm*760/1800),Spacer(1,3*mm),
          P('Зв’язки: товар посилається на категорію; кошик зберігає ID товару та кількість; StoreService збирає незмінні рядки кошика в Order; Main приймає команди та викликає сервіс.','SmallUA'),PageBreak(),
          P('4. Опис основних класів','HeadUA')]
class_rows=[['Клас','Відповідальність'],['Category','Зберігає ID і назву категорії; контролює коректність назви.'],['Product','Зберігає ID, назву, ціну, опис і категорію. Lombok генерує getters/setters та конструктор без аргументів.'],['Cart','Зберігає кількість одиниць по ID, рахує підсумок, формує копії рядків кошика та очищується після оформлення.'],['Order','Фіксує номер, дату, рядки товарів, підсумок і початковий статус «Нове».'],['StoreService','Керує каталогом, пошуком, перевіркою ID і історією замовлень.'],['Main','Виводить меню, читає введення, обробляє помилки введення й маршрутизує команди.']]
class_rows=[[P(str(cell),'TableHeadUA' if ri==0 else 'TableUA') for cell in row] for ri,row in enumerate(class_rows)]
ct=Table(class_rows,colWidths=[38*mm,132*mm],repeatRows=1); ct.setStyle(TableStyle([('FONTNAME',(0,0),(-1,-1),'Arial'),('FONTNAME',(0,0),(-1,0),'Arial-Bold'),('FONTSIZE',(0,0),(-1,-1),9),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#DCEAF3')),('GRID',(0,0),(-1,-1),.5,colors.HexColor('#9AAEBB')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
story += [ct,Spacer(1,5*mm),P('Використання Lombok','SubUA'),P('У Category та Product використано @Getter, @Setter та @NoArgsConstructor. Бізнес-конструктори залишені явними, щоб перевіряти ID, назви, категорію й ціну. У Order використано @Getter; зміна статусу контролюється окремим методом.'),
          P('5. Алгоритм роботи','HeadUA'),P('Після запуску Main показує меню в циклі. Користувач обирає дію. Для додавання програма знаходить товар за ID і перевіряє кількість. Кошик показує рядки й суму. Оформлення порожнього кошика не дозволяється; інакше створюється Order, він додається в історію, а кошик очищується. Пошук виконується за частковим текстом без урахування регістру.'),PageBreak(),
          P('6. Запуск і приклад взаємодії','HeadUA'),P('Вимоги до середовища: JDK 17 або новіший і Maven 3.8+. У каталозі проєкту виконайте:'),
          P('mvn clean package<br/>mvn exec:java','CodeUA'),P('Maven завантажує Lombok та плагіни з Maven Central. В IDE потрібно ввімкнути annotation processing.'),P('Приклад сценарію (демонстраційний формат виводу)','SubUA')]
sample='''=== Вітаємо в інтернет-магазині ===
Ваш вибір: 1 - Переглянути каталог
#1 | Ноутбук Lenovo IdeaPad | 19999.99 грн | Електроніка | Ноутбук для навчання та роботи
#2 | Смартфон Samsung Galaxy | 12999.50 грн | Смартфони | Смартфон з великим екраном
...
Ваш вибір: 2 - Додати товар до кошика
Введіть ID товару: 2
Введіть кількість: 1
Товар додано до кошика.
Ваш вибір: 6 - Оформити замовлення
Замовлення оформлено:
Замовлення №1001 від 24.11.2026 12:00
  Смартфон Samsung Galaxy × 1 = 12999.50 грн
Разом: 12999.50 грн | Статус: Нове'''
console=Table([[P(line,'ConsoleUA')] for line in sample.splitlines()],colWidths=[170*mm]); console.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#F3F6F8')),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
story += [console,P('Час у прикладі наведений для ілюстрації; програма виводить фактичну дату й час запуску. Кожна нова сесія починається з порожньої історії та початкового каталогу.'),
          P('7. Висновок','HeadUA'),P('Створено консольний інтернет-магазин із каталогом категоризованих товарів, керуванням кошиком, пошуком, оформленням замовлень та історією поточного запуску. Застосовано інкапсуляцію, колекції, BigDecimal для грошових сум, Lombok для повторюваного коду, цикли та розгалуження меню. Код організований у Maven-проєкт і готовий до відкриття в IntelliJ IDEA або іншому середовищі Java.'),
          P('Обмеження: застосунок демонстраційний; база даних, користувацькі акаунти, платежі й постійне збереження замовлень не реалізовані. Дані каталогу та замовлень зберігаються в пам’яті й очищуються після завершення програми.','SmallUA')]
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
