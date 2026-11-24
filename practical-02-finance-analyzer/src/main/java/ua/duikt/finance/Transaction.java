package ua.duikt.finance;
import java.math.BigDecimal; import java.time.LocalDate; import java.util.Objects;
/** Bank transaction: positive amount is income, negative amount is expense. */
public final class Transaction {
 private final LocalDate date; private final BigDecimal amount; private final String description; private final String category;
 public Transaction(LocalDate date, BigDecimal amount, String description, String category) {
  this.date=Objects.requireNonNull(date,"date"); this.amount=Objects.requireNonNull(amount,"amount");
  if(description==null||description.isBlank()) throw new IllegalArgumentException("Опис не може бути порожнім");
  this.description=description.trim(); this.category=category==null||category.isBlank()?"Інше":category.trim();
 }
 public LocalDate getDate(){return date;} public BigDecimal getAmount(){return amount;} public String getDescription(){return description;} public String getCategory(){return category;}
 @Override public String toString(){return date+" | "+amount.toPlainString()+" грн | "+category+" | "+description;}
}
