package ua.duikt.shop.model;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.math.BigDecimal;
import java.util.Objects;

/** Товар каталогу з ціною у гривнях. */
@Getter
@Setter
@NoArgsConstructor
public class Product {
    private int id;
    private String name;
    private BigDecimal price;
    private String description;
    private Category category;

    public Product(int id, String name, BigDecimal price, String description, Category category) {
        setId(id);
        setName(name);
        setPrice(price);
        setDescription(description);
        setCategory(category);
    }

    public void setId(int id) {
        if (id <= 0) throw new IllegalArgumentException("ID товару має бути додатним.");
        this.id = id;
    }

    public void setName(String name) {
        if (name == null || name.isBlank()) throw new IllegalArgumentException("Назва товару не може бути порожньою.");
        this.name = name.trim();
    }

    public void setPrice(BigDecimal price) {
        if (price == null || price.signum() < 0) throw new IllegalArgumentException("Ціна не може бути від’ємною.");
        this.price = price.setScale(2, java.math.RoundingMode.HALF_UP);
    }

    public void setDescription(String description) {
        this.description = description == null ? "" : description.trim();
    }

    public void setCategory(Category category) {
        this.category = Objects.requireNonNull(category, "Категорія є обов’язковою.");
    }

    @Override
    public String toString() {
        return "#%d | %s | %s грн | %s | %s".formatted(id, name, price, category.getName(), description);
    }
}
