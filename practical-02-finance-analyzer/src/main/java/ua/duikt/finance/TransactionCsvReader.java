package ua.duikt.finance;
import java.io.*; import java.math.BigDecimal; import java.net.URI; import java.nio.charset.StandardCharsets; import java.nio.file.*; import java.time.LocalDate; import java.time.format.*; import java.util.*;
/** Reads UTF-8 CSV rows: date,amount,description[,category]. */
public final class TransactionCsvReader {
 private static final List<DateTimeFormatter> DATE_FORMATS=List.of(DateTimeFormatter.ISO_LOCAL_DATE,DateTimeFormatter.ofPattern("dd-MM-yyyy"),DateTimeFormatter.ofPattern("d-M-yyyy"));
 public List<Transaction> readTransactions(Path file)throws IOException{try(var r=Files.newBufferedReader(file,StandardCharsets.UTF_8)){return readRows(r);}}
 public List<Transaction> readTransactions(URI source)throws IOException{try(var in=source.toURL().openStream();var r=new BufferedReader(new InputStreamReader(in,StandardCharsets.UTF_8))){return readRows(r);}}
 private List<Transaction> readRows(BufferedReader r)throws IOException{
  List<Transaction> out=new ArrayList<>();String line;int n=0;
  while((line=r.readLine())!=null){n++;if(line.isBlank())continue;List<String> f=parseCsvLine(line);if(n==1&&!f.isEmpty()&&f.get(0).strip().equalsIgnoreCase("date"))continue;
   if(f.size()<3||f.size()>4)throw new IOException("Некоректний CSV у рядку "+n+": очікується 3 або 4 поля");
   try{LocalDate d=parseDate(f.get(0).strip());BigDecimal amount=new BigDecimal(f.get(1).strip().replace(',','.'));String desc=f.get(2).strip();String cat=f.size()==4&&!f.get(3).isBlank()?f.get(3).strip():inferCategory(desc);out.add(new Transaction(d,amount,desc,cat));}
   catch(RuntimeException e){throw new IOException("Помилка в CSV у рядку "+n+": "+e.getMessage(),e);}
  }return List.copyOf(out);
 }
 private LocalDate parseDate(String v){for(var f:DATE_FORMATS){try{return LocalDate.parse(v,f);}catch(DateTimeParseException ignored){}}throw new IllegalArgumentException("дата має бути yyyy-MM-dd або dd-MM-yyyy: "+v);}
 private List<String> parseCsvLine(String line)throws IOException{List<String> a=new ArrayList<>();StringBuilder b=new StringBuilder();boolean quoted=false;for(int i=0;i<line.length();i++){char c=line.charAt(i);if(c=='"'){if(quoted&&i+1<line.length()&&line.charAt(i+1)=='"'){b.append('"');i++;}else quoted=!quoted;}else if(c==','&&!quoted){a.add(b.toString());b.setLength(0);}else b.append(c);}if(quoted)throw new IOException("незакрита лапка у CSV");a.add(b.toString());return a;}
 private String inferCategory(String d){String t=d.toLowerCase(Locale.ROOT);if(t.contains("зарплат")||t.contains("дохід")||t.contains("salary")||t.contains("фріланс")||t.contains("фриланс")||t.contains("авторськ")||t.contains("премія"))return "Дохід";if(t.contains("кафе")||t.contains("кав\'яр")||t.contains("ресторан")||t.contains("сільпо")||t.contains("продукт")||t.contains("супермаркет")||t.contains("їжа"))return "Харчування";if(t.contains("оренд")||t.contains("комунал"))return "Житло";if(t.contains("таксі")||t.contains("транспорт")||t.contains("метро")||t.contains("бензин"))return "Транспорт";if(t.contains("аптек")||t.contains("лікар"))return "Здоров’я";if(t.contains("подарунк")||t.contains("прикраси"))return "Подарунки";if(t.contains("кінотеатр"))return "Дозвілля";return "Інше";}
}
