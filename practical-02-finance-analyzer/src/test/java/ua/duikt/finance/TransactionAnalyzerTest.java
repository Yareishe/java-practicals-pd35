package ua.duikt.finance;
import org.junit.jupiter.api.Test;import java.math.BigDecimal;import java.time.LocalDate;import java.util.*;import static org.junit.jupiter.api.Assertions.*;
class TransactionAnalyzerTest {
 private Transaction tx(String d,String a,String desc){return new Transaction(LocalDate.parse(d),new BigDecimal(a),desc,"Тест");}
 @Test void calculatesTotalBalance(){var a=new TransactionAnalyzer(List.of(tx("2023-01-01","100.00","дохід"),tx("2023-01-02","-50.00","витрата"),tx("2023-01-03","150.00","дохід")));assertEquals(new BigDecimal("200.00"),a.calculateTotalBalance());}
 @Test void countsTransactionsForSelectedMonth(){var a=new TransactionAnalyzer(List.of(tx("2023-02-01","50","a"),tx("2023-02-15","-20","b"),tx("2023-03-05","100","c")));assertEquals(2,a.countTransactionsByMonth("02-2023"));assertEquals(1,a.countTransactionsByMonth("03-2023"));}
 @Test void returnsTenLargestExpenses(){var rows=new ArrayList<Transaction>();for(int i=1;i<=12;i++)rows.add(tx("2024-01-%02d".formatted(i),"-%d".formatted(i*100),"expense"+i));rows.add(tx("2024-01-13","9000","income"));var top=new TransactionAnalyzer(rows).findTopExpenses();assertEquals(10,top.size());assertEquals(new BigDecimal("-1200"),top.get(0).getAmount());assertEquals(new BigDecimal("-300"),top.get(9).getAmount());}
 @Test void findsMonthlyExpenseExtremesAndIgnoresIncome(){var a=new TransactionAnalyzer(List.of(tx("2024-01-01","20000","income"),tx("2024-01-02","-600","small"),tx("2024-01-03","-2400","large"),tx("2024-02-01","-9000","other")));assertEquals("large",a.findLargestExpense("01-2024").getDescription());assertEquals("small",a.findSmallestExpense("01-2024").getDescription());}
}
