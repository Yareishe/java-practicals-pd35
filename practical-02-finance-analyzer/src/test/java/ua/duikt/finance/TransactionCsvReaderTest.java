package ua.duikt.finance;
import org.junit.jupiter.api.Test;import org.junit.jupiter.api.io.TempDir;import java.nio.file.*;import static org.junit.jupiter.api.Assertions.*;
class TransactionCsvReaderTest {
 @TempDir Path temp;
 @Test void readsUtf8CsvWithOptionalCategoryAndQuotedComma()throws Exception{Path csv=temp.resolve("transactions.csv");Files.writeString(csv,"date,amount,description,category\n2024-01-02,-12.50,\"Кафе, центр\",Їжа\n",java.nio.charset.StandardCharsets.UTF_8);var rows=new TransactionCsvReader().readTransactions(csv);assertEquals(1,rows.size());assertEquals("Кафе, центр",rows.get(0).getDescription());assertEquals("Їжа",rows.get(0).getCategory());}
 @Test void readsThreeColumnCsvAndInfersCategory()throws Exception{Path csv=temp.resolve("legacy.csv");Files.writeString(csv,"02-01-2024,-100.00,Супермаркет\n",java.nio.charset.StandardCharsets.UTF_8);var t=new TransactionCsvReader().readTransactions(csv).get(0);assertEquals("Харчування",t.getCategory());assertEquals("2024-01-02",t.getDate().toString());}
}
