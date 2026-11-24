package ua.duikt.finance;
import java.math.BigDecimal;import java.time.YearMonth;import java.time.format.*;import java.util.*;import java.util.stream.Collectors;
/** Calculates balance, month counts and expense summaries from transactions. */
public final class TransactionAnalyzer {
 private static final DateTimeFormatter MONTH_FORMAT=DateTimeFormatter.ofPattern("MM-yyyy");private final List<Transaction> transactions;
 public TransactionAnalyzer(List<Transaction> transactions){this.transactions=List.copyOf(transactions);}
 public BigDecimal calculateTotalBalance(){return transactions.stream().map(Transaction::getAmount).reduce(BigDecimal.ZERO,BigDecimal::add);}
 public int countTransactionsByMonth(String monthYear){YearMonth m=parseMonth(monthYear);return (int)transactions.stream().filter(t->YearMonth.from(t.getDate()).equals(m)).count();}
 public List<Transaction> findTopExpenses(){return transactions.stream().filter(t->t.getAmount().signum()<0).sorted(Comparator.comparing(Transaction::getAmount)).limit(10).toList();}
 public Transaction findLargestExpense(String monthYear){return transactions.stream().filter(t->isExpenseIn(t,parseMonth(monthYear))).min(Comparator.comparing(Transaction::getAmount)).orElse(null);}
 public Transaction findSmallestExpense(String monthYear){return transactions.stream().filter(t->isExpenseIn(t,parseMonth(monthYear))).max(Comparator.comparing(Transaction::getAmount)).orElse(null);}
 public Map<String,BigDecimal> expensesByCategory(){return transactions.stream().filter(t->t.getAmount().signum()<0).collect(Collectors.groupingBy(Transaction::getCategory,TreeMap::new,Collectors.mapping(t->t.getAmount().abs(),Collectors.reducing(BigDecimal.ZERO,BigDecimal::add))));}
 public Map<YearMonth,BigDecimal> expensesByMonth(){return transactions.stream().filter(t->t.getAmount().signum()<0).collect(Collectors.groupingBy(t->YearMonth.from(t.getDate()),TreeMap::new,Collectors.mapping(t->t.getAmount().abs(),Collectors.reducing(BigDecimal.ZERO,BigDecimal::add))));}
 public List<Transaction> getTransactions(){return transactions;}
 private boolean isExpenseIn(Transaction t,YearMonth m){return t.getAmount().signum()<0&&YearMonth.from(t.getDate()).equals(m);}
 private YearMonth parseMonth(String v){try{return YearMonth.parse(v,MONTH_FORMAT);}catch(DateTimeParseException e){throw new IllegalArgumentException("Період має бути у форматі MM-yyyy",e);}}
}
