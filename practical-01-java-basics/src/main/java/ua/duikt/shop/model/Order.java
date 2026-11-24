package ua.duikt.shop.model;

import lombok.Getter;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.concurrent.atomic.AtomicLong;

/** Знімок кошика на момент оформлення замовлення. */
@Getter
public class Order {
    private static final AtomicLong NEXT_ID = new AtomicLong(1001);
    private static final DateTimeFormatter FORMAT = DateTimeFormatter.ofPattern("dd.MM.yyyy HH:mm");

    private final long id;
    private final LocalDateTime createdAt;
    private final List<Cart.CartLine> lines;
    private final BigDecimal total;
    private String status;

    public Order(List<Cart.CartLine> lines) {
        if (lines == null || lines.isEmpty()) throw new IllegalArgumentException("Не можна оформити порожнє замовлення.");
        this.id = NEXT_ID.getAndIncrement();
        this.createdAt = LocalDateTime.now();
        this.lines = List.copyOf(lines);
        this.total = this.lines.stream()
                .map(Cart.CartLine::lineTotal)
                .reduce(BigDecimal.ZERO, BigDecimal::add)
                .setScale(2, java.math.RoundingMode.HALF_UP);
        this.status = "Нове";
    }

    public void setStatus(String status) {
        if (status == null || status.isBlank()) throw new IllegalArgumentException("Статус не може бути порожнім.");
        this.status = status.trim();
    }

    @Override
    public String toString() {
        StringBuilder text = new StringBuilder("Замовлення №").append(id)
                .append(" від ").append(createdAt.format(FORMAT)).append('\n');
        for (Cart.CartLine line : lines) {
            text.append("  ").append(line.name()).append(" × ").append(line.quantity())
                    .append(" = ").append(line.lineTotal()).append(" грн\n");
        }
        return text.append("Разом: ").append(total).append(" грн | Статус: ").append(status).toString();
    }
}
