from pathlib import Path
import csv
from decimal import Decimal
from datetime import datetime
from collections import defaultdict
from PIL import Image as PILImage, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image

ROOT=Path(__file__).resolve().parents[1]; DOCS=ROOT/'docs'; OUT=DOCS/'Звіт_ПР2_Фінансовий_аналізатор.pdf'
FONT=r'C:\Windows\Fonts\arial.ttf'; FONT_B=r'C:\Windows\Fonts\arialbd.ttf'
pdfmetrics.registerFont(TTFont('Arial',FONT)); pdfmetrics.registerFont(TTFont('Arial-Bold',FONT_B)); pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='Arial-Bold',italic='Arial',boldItalic='Arial-Bold')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyUA',fontName='Arial',fontSize=9.4,leading=13.2,alignment=TA_JUSTIFY,spaceAfter=6,textColor=colors.HexColor('#253643')))
styles.add(ParagraphStyle(name='HeadUA',fontName='Arial-Bold',fontSize=15.5,leading=19,spaceAfter=8,textColor=colors.HexColor('#17324A')))
styles.add(ParagraphStyle(name='SubUA',fontName='Arial-Bold',fontSize=11.4,leading=15,spaceBefore=4,spaceAfter=5,textColor=colors.HexColor('#28516F')))
styles.add(ParagraphStyle(name='SmallUA',fontName='Arial',fontSize=8,leading=11,textColor=colors.HexColor('#465866')))
styles.add(ParagraphStyle(name='CoverUA',fontName='Arial-Bold',fontSize=21,leading=27,alignment=TA_CENTER,textColor=colors.HexColor('#17324A')))
styles.add(ParagraphStyle(name='CenterUA',fontName='Arial',fontSize=11.5,leading=17,alignment=TA_CENTER,textColor=colors.HexColor('#263746')))
styles.add(ParagraphStyle(name='TableUA',fontName='Arial',fontSize=8.1,leading=10.4,textColor=colors.HexColor('#253643')))
styles.add(ParagraphStyle(name='TableHeadUA',fontName='Arial-Bold',fontSize=8.2,leading=10.5,textColor=colors.HexColor('#17324A')))
styles.add(ParagraphStyle(name='ConsoleUA',fontName='Arial',fontSize=8.1,leading=10.3,textColor=colors.HexColor('#203546')))
def P(s, style='BodyUA'): return Paragraph(s,styles[style])

# Derive the report's numeric illustration from the included methodical CSV.
rows=[]
with (ROOT/'src/main/resources/transactions_source.csv').open(encoding='utf-8',newline='') as f:
    for date,amount,description in csv.reader(f):
        rows.append((datetime.strptime(date,'%d-%m-%Y').date(),Decimal(amount),description))
balance=sum((a for _,a,_ in rows),Decimal('0'))
income=sum((a for _,a,_ in rows if a>0),Decimal('0'))
expenses=sum((-a for _,a,_ in rows if a<0),Decimal('0'))
monthly=defaultdict(lambda: [0,Decimal('0')]); cats=defaultdict(lambda: Decimal('0'))
def category(desc):
    x=desc.lower()
    if any(k in x for k in ('сільпо',"кав'яр",'ресторан')): return 'Харчування'
    if 'аптек' in x: return 'Здоров’я'
    if 'комунальн' in x: return 'Житло'
    if any(k in x for k in ('подарунк','прикраси')): return 'Подарунки'
    if any(k in x for k in ('бензин','транспорт')): return 'Транспорт'
    if 'кінотеатр' in x: return 'Дозвілля'
    return 'Інше'
for d,a,desc in rows:
    k=d.strftime('%m-%Y'); monthly[k][0]+=1
    if a<0:
        monthly[k][1]+=abs(a); cats[category(desc)]+=abs(a)
top=sorted((x for x in rows if x[1]<0),key=lambda x:x[1])[:10]
fmt=lambda x: f'{x:,.2f}'.replace(',',' ')

# Draw the class diagram as a crisp local image.
W,H=1700,760; im=PILImage.new('RGB',(W,H),'#F5F8FB'); draw=ImageDraw.Draw(im)
regular=ImageFont.truetype(FONT,24); bold=ImageFont.truetype(FONT_B,28); small=ImageFont.truetype(FONT,20)
def box(x,y,w,h,title,lines):
    draw.rounded_rectangle((x,y,x+w,y+h),radius=18,fill='white',outline='#47708B',width=4)
    draw.rounded_rectangle((x,y,x+w,y+58),radius=16,fill='#DCEAF3',outline='#47708B',width=3)
    draw.text((x+w//2,y+28),title,font=bold,fill='#17324A',anchor='mm')
    for i,line in enumerate(lines): draw.text((x+18,y+82+i*42),line,font=regular,fill='#253643')
def arrow(a,b,label):
    import math
    draw.line((*a,*b),fill='#A06D39',width=4); ang=math.atan2(b[1]-a[1],b[0]-a[0]); n=14
    draw.polygon([b,(b[0]-n*math.cos(ang-.5),b[1]-n*math.sin(ang-.5)),(b[0]-n*math.cos(ang+.5),b[1]-n*math.sin(ang+.5))],fill='#A06D39')
    draw.text(((a[0]+b[0])//2,(a[1]+b[1])//2-15),label,font=small,fill='#80562F',anchor='mm')
box(35,80,420,250,'Transaction',['date: LocalDate','amount: BigDecimal','description, category'])
box(520,80,480,290,'TransactionCsvReader',['CSV path / URL','UTF-8, quoted fields','date and amount parsing'])
box(1065,80,560,310,'TransactionAnalyzer',['balance / month count','top 10 expenses','monthly extremes','category and month totals'])
box(350,475,520,210,'TransactionReportGenerator',['console reports','* = about 1 000 UAH'])
box(1010,475,480,210,'Main',['loads URL or local CSV','coordinates analysis'])
arrow((455,190),(520,190),'creates rows'); arrow((1000,210),(1065,210),'analyzes'); arrow((1065,350),(870,490),'summarizes'); arrow((1250,475),(1340,390),'runs')
diagram=DOCS/'uml_класів_практична2.png'; im.save(diagram)

doc=SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=19*mm,rightMargin=19*mm,topMargin=17*mm,bottomMargin=21*mm,title='Практична робота №2 — Фінансовий аналізатор',author='Єфіменко Максим Олександрович')
def footer(c,d):
    c.saveState(); w,h=A4; c.setStrokeColor(colors.HexColor('#D0DCE4')); c.line(19*mm,15*mm,w-19*mm,15*mm); c.setFont('Arial',8); c.setFillColor(colors.HexColor('#667784')); c.drawString(19*mm,10*mm,'Практична робота №2 • Java • ПД-35'); c.drawRightString(w-19*mm,10*mm,str(d.page)); c.restoreState()
story=[Spacer(1,16*mm),P('Виконав: Єфіменко Максим Олександрович<br/>Група: ПД-35<br/>Викладач: Шахматов Іван Олександрович','CenterUA'),Spacer(1,32*mm),P('ПРАКТИЧНА РОБОТА №2','CoverUA'),Spacer(1,7*mm),P('Об’єктно-орієнтоване програмування в Java','CenterUA'),Spacer(1,18*mm),P('Розробка програми<br/><b>«Фінансовий аналізатор»</b>','CenterUA'),Spacer(1,38*mm),P('Київ • 2026','CenterUA'),PageBreak(),
P('1. Мета та постановка задачі','HeadUA'),P('Мета роботи — закріпити ООП у Java, роботу з колекціями та CSV, обробку дат і грошових значень, модульне тестування й розділення читання даних та їх аналізу.'),P('Завдання — створити програму фінансового аналізу транзакцій: прочитати CSV, визначити баланс, кількість операцій за місяць, 10 найбільших витрат і сформувати аналітичний текстовий звіт.'),P('2. Вимоги та реалізація','HeadUA')]
req=[['Вимога з методички','Реалізація'],['Читання CSV','UTF-8, локальний файл або URL; формат з 3 полями сумісний із джерелом і 4-колонковий із категорією'],['Загальний баланс','Сума доходів і витрат через BigDecimal'],['Кількість за місяць','Період MM-yyyy; дати dd-MM-yyyy та yyyy-MM-dd'],['10 найбільших витрат','Stream-фільтр від’ємних сум, сортування за розміром витрати, обмеження 10 записів'],['Найбільша / найменша','Визначаються серед витрат вибраного місяця; доходи відкидаються'],['Категорії та місяці','Суми витрат і текстові смуги, одна зірочка приблизно на 1 000 грн'],['Модульні тести','Перевіряються читання CSV, баланс, місячні підрахунки, топ-10 та крайні значення']]
req=[[P(v,'TableHeadUA' if i==0 else 'TableUA') for v in row] for i,row in enumerate(req)]
t=Table(req,colWidths=[43*mm,127*mm],repeatRows=1);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#DCEAF3')),('GRID',(0,0),(-1,-1),.5,colors.HexColor('#9AAEBB')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
story += [t,Spacer(1,4*mm),P('Доходи зберігаються додатними, витрати — від’ємними; у звітах витрати показуються як додатні суми для читабельності. Для грошей використано BigDecimal, щоб не накопичувати похибку double.','SmallUA'),PageBreak(),
P('3. Структура та розподіл відповідальності','HeadUA'),P('Читач CSV створює об’єкти транзакцій. Аналізатор працює з незмінним списком транзакцій, а генератор звіту форматує готові результати. Main лише координує завантаження, аналіз і виведення.'),Image(str(diagram),width=170*mm,height=170*mm*760/1700),Spacer(1,3*mm),P('Для розширення можна замінити джерело CSV іншим читачем, не змінюючи правила фінансового аналізу. Парсер підтримує стандартні лапки CSV та кому всередині взятого в лапки опису.','SmallUA'),PageBreak(),
P('4. Алгоритми та модульні тести','HeadUA')]
classes=[['Клас','Призначення'],['Transaction','Незмінна модель: дата, сума, опис і категорія.'],['TransactionCsvReader','Читає CSV із файлу чи URL; розбирає 3/4 поля, лапки, дату і суму. Категорію для старого 3-колонкового формату виводить з опису.'],['TransactionAnalyzer','Обчислює баланс, лічильник місяця, екстремальні витрати, топ-10, суми за категоріями та місяцями.'],['TransactionReportGenerator','Друкує підсумки та текстові смуги витрат із масштабом зірочок.'],['Main','Вибирає джерело, за відсутності мережі використовує CSV з комплекту, запускає звіти.']]
classes=[[P(v,'TableHeadUA' if i==0 else 'TableUA') for v in row] for i,row in enumerate(classes)]
t2=Table(classes,colWidths=[48*mm,122*mm],repeatRows=1);t2.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#DCEAF3')),('GRID',(0,0),(-1,-1),.5,colors.HexColor('#9AAEBB')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
story += [t2,Spacer(1,4*mm),P('Перевірки у JUnit 5','SubUA')]
tests=[['Набір перевірок','Очікуваний результат'],['TransactionAnalyzerTest','Баланс 200, кількість за місяцями 2/1, рівно 10 найбільших витрат із сортуванням, крайні витрати без доходів.'],['TransactionCsvReaderTest','UTF-8 і категорія, лапки з комою в описі, сумісність із 3-польовим CSV та формат dd-MM-yyyy.']]
tests=[[P(v,'TableHeadUA' if i==0 else 'TableUA') for v in row] for i,row in enumerate(tests)]
t3=Table(tests,colWidths=[52*mm,118*mm],repeatRows=1);t3.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E8F0F5')),('GRID',(0,0),(-1,-1),.5,colors.HexColor('#9AAEBB')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
story += [t3,PageBreak(),P('5. Приклад результату та висновок','HeadUA'),P('Наведені нижче підсумки отримані з CSV, який надається разом із методичкою. У файлі 26 операцій за грудень 2023 та січень 2024.','BodyUA')]
lines=[f'Операцій у CSV: {len(rows)}',f'Загальний баланс: {fmt(balance)} грн',f'Доходи: {fmt(income)} грн    Витрати: {fmt(expenses)} грн']
for m,(cnt,total) in sorted(monthly.items(), key=lambda item: datetime.strptime(item[0],'%m-%Y')): lines.append(f'{m}: {cnt} транзакцій; витрати {fmt(total)} грн')
lines += ['', 'Витрати за категоріями (* ≈ 1 000 грн):']
for name,total in sorted(cats.items()): lines.append(f'{name}: {fmt(total)} грн  '+('*'*int(total//Decimal('1000'))))
lines += ['', '10 найбільших витрат:']
for d,a,desc in top: lines.append(f'{d.strftime("%d-%m-%Y")}  {desc} — {fmt(abs(a))} грн')
console=Table([[P(line,'ConsoleUA')] for line in lines],colWidths=[170*mm]);console.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#F3F6F8')),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
story += [console,Spacer(1,4*mm),P('Висновок','SubUA'),P('Створено об’єктно-орієнтований аналізатор фінансових транзакцій. Програма розділяє читання CSV, модель, обчислення та виведення звіту; підтримує підрахунок балансу й витрат, пошук крайніх операцій, топ-10 та групування за періодами й категоріями. Підготовлено JUnit тести для ключових вимог. Проєкт містить вихідний CSV, а мережеве джерело з методички використовується з локальним резервним варіантом.','BodyUA'),P('Запуск: JDK 17+, Maven 3.8+; команди mvn test і mvn exec:java. У середовищі підготовки не було встановлено JDK і Maven; компіляцію та тести не запускали.','SmallUA')]
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
