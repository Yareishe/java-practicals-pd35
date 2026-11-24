package ua.duikt.finance;
import java.math.*;import java.time.YearMonth;import java.time.format.DateTimeFormatter;import java.util.*;
/** Keeps console presentation separate from transaction analysis. */
public final class TransactionReportGenerator {
 private static final BigDecimal STAR_UNIT=new BigDecimal("1000");private static final DateTimeFormatter MF=DateTimeFormatter.ofPattern("MM-yyyy");
 public void printBalanceReport(BigDecimal n){System.out.println("Загальний баланс: "+money(n)+" грн");}
 public void printTransactionsCountByMonth(String m,int n){System.out.println("Кількість транзакцій за "+m+": "+n);}
 public void printTopExpensesReport(List<Transaction> rows){System.out.println("10 найбільших витрат:");if(rows.isEmpty()){System.out.println("  Витрат не знайдено.");return;}rows.forEach(t->System.out.println("  "+t.getDate()+" | "+t.getCategory()+" | "+t.getDescription()+" | "+money(t.getAmount().abs())+" грн"));}
 public void printLargestAndSmallest(String period,Transaction largest,Transaction smallest){System.out.println("Екстремальні витрати за "+period+":");System.out.println("  Найбільша: "+(largest==null?"немає витрат":largest.getDescription()+" — "+money(largest.getAmount().abs())+" грн"));System.out.println("  Найменша: "+(smallest==null?"немає витрат":smallest.getDescription()+" — "+money(smallest.getAmount().abs())+" грн"));}
 public void printExpenseBreakdown(Map<String,BigDecimal> cats,Map<YearMonth,BigDecimal> months){System.out.println("Витрати за категоріями (* ≈ 1 000 грн):");cats.forEach(this::printBar);System.out.println("Витрати за місяцями (* ≈ 1 000 грн):");months.forEach((m,n)->printBar(m.format(MF),n));}
 private void printBar(String label,BigDecimal amount){long n=amount.divide(STAR_UNIT,0,RoundingMode.FLOOR).longValue();System.out.printf("  %-18s %10s грн  %s%n",label,money(amount),"*".repeat((int)Math.min(n,60)));}
 private String money(BigDecimal n){return n.setScale(2,RoundingMode.HALF_UP).toPlainString();}
}
