package ua.duikt.shop.model;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.Objects;

/** Категорія каталогу товарів. */
@Getter
@Setter
@NoArgsConstructor
public class Category {
    private int id;
    private String name;

    public Category(int id, String name) {
        setId(id);
        setName(name);
    }

    public void setId(int id) {
        if (id <= 0) throw new IllegalArgumentException("ID категорії має бути додатним.");
        this.id = id;
    }

    public void setName(String name) {
        if (name == null || name.isBlank()) throw new IllegalArgumentException("Назва категорії не може бути порожньою.");
        this.name = name.trim();
    }

    @Override
    public String toString() {
        return name;
    }

    @Override
    public boolean equals(Object other) {
        if (this == other) return true;
        if (!(other instanceof Category category)) return false;
        return id == category.id;
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}
