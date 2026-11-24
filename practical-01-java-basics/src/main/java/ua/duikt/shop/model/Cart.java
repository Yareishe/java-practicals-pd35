package ua.duikt.shop.model;

import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Кошик зберігає ID товару та кількість вибраних одиниць. */
@NoArgsConstructor
public class Cart {
    private final Map<Integer, Integer> quantities = new LinkedHashMap<>();

    public void addProduct(Product product, int quantity) {
        if (product == null) throw new IllegalArgumentException("Товар не задано.");
        if (quantity <= 0) throw new IllegalArgumentException("Кількість має бути більшою за нуль.");
        quantities.merge(product.getId(), quantity, Integer::sum);
    }

    public boolean removeProduct(int productId) {
        return quantities.remove(productId) != null;
    }

    public Map<Integer, Integer> getQuantities() {
        return Collections.unmodifiableMap(new LinkedHashMap<>(quantities));
    }

    public boolean isEmpty() {
        return quantities.isEmpty();
    }

    public void clear() {
        quantities.clear();
    }

    public BigDecimal getTotal(List<Product> catalog) {
        Map<Integer, Product> byId = new LinkedHashMap<>();
        for (Product product : catalog) byId.put(product.getId(), product);
        BigDecimal total = BigDecimal.ZERO;
        for (var entry : quantities.entrySet()) {
            Product product = byId.get(entry.getKey());
            if (product == null) throw new IllegalStateException("У кошику є товар, відсутній у каталозі.");
            total = total.add(product.getPrice().multiply(BigDecimal.valueOf(entry.getValue())));
        }
        return total.setScale(2, java.math.RoundingMode.HALF_UP);
    }

    public List<CartLine> getLines(List<Product> catalog) {
        Map<Integer, Product> byId = new LinkedHashMap<>();
        for (Product product : catalog) byId.put(product.getId(), product);
        List<CartLine> lines = new ArrayList<>();
        for (var entry : quantities.entrySet()) {
            Product product = byId.get(entry.getKey());
            if (product == null) throw new IllegalStateException("У кошику є товар, відсутній у каталозі.");
            lines.add(new CartLine(product.getId(), product.getName(), product.getPrice(), entry.getValue(), product.getCategory().getName()));
        }
        return List.copyOf(lines);
    }

    public record CartLine(int productId, String name, BigDecimal unitPrice, int quantity, String category) {
        public BigDecimal lineTotal() {
            return unitPrice.multiply(BigDecimal.valueOf(quantity)).setScale(2, java.math.RoundingMode.HALF_UP);
        }
    }
}
