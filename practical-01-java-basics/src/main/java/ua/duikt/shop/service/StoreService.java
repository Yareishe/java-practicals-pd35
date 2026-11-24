package ua.duikt.shop.service;

import ua.duikt.shop.model.Cart;
import ua.duikt.shop.model.Category;
import ua.duikt.shop.model.Order;
import ua.duikt.shop.model.Product;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Optional;

/** Бізнес-операції каталогу, пошуку, кошика та замовлень. */
public class StoreService {
    private final Map<Integer, Category> categories = new LinkedHashMap<>();
    private final Map<Integer, Product> products = new LinkedHashMap<>();
    private final List<Order> orderHistory = new ArrayList<>();

    public StoreService() {
        seedCatalog();
    }

    private void seedCatalog() {
        Category electronics = new Category(1, "Електроніка");
        Category phones = new Category(2, "Смартфони");
        Category accessories = new Category(3, "Аксесуари");
        Category home = new Category(4, "Для дому");
        categories.put(electronics.getId(), electronics);
        categories.put(phones.getId(), phones);
        categories.put(accessories.getId(), accessories);
        categories.put(home.getId(), home);

        addProduct(new Product(1, "Ноутбук Lenovo IdeaPad", new BigDecimal("19999.99"),
                "Ноутбук для навчання та роботи", electronics));
        addProduct(new Product(2, "Смартфон Samsung Galaxy", new BigDecimal("12999.50"),
                "Смартфон з великим екраном", phones));
        addProduct(new Product(3, "Навушники JBL Tune", new BigDecimal("2499.00"),
                "Бездротові навушники", accessories));
        addProduct(new Product(4, "Клавіатура Logitech", new BigDecimal("1599.00"),
                "Компактна клавіатура для роботи", accessories));
        addProduct(new Product(5, "Настільна лампа", new BigDecimal("899.00"),
                "LED-лампа з регулюванням яскравості", home));
        addProduct(new Product(6, "Планшет Lenovo Tab", new BigDecimal("8499.00"),
                "Планшет для читання та мультимедіа", electronics));
    }

    public void addProduct(Product product) {
        if (product == null) throw new IllegalArgumentException("Товар не задано.");
        if (!categories.containsKey(product.getCategory().getId())) {
            throw new IllegalArgumentException("Категорія товару не зареєстрована в каталозі.");
        }
        if (products.putIfAbsent(product.getId(), product) != null) {
            throw new IllegalArgumentException("Товар з таким ID вже існує.");
        }
    }

    public List<Product> getCatalog() {
        return products.values().stream().sorted(Comparator.comparingInt(Product::getId)).toList();
    }

    public List<Category> getCategories() {
        return List.copyOf(categories.values());
    }

    public Optional<Product> findProduct(int id) {
        return Optional.ofNullable(products.get(id));
    }

    public List<Product> searchByName(String query) {
        String normalized = normalize(query);
        if (normalized.isEmpty()) return List.of();
        return getCatalog().stream()
                .filter(p -> p.getName().toLowerCase(Locale.ROOT).contains(normalized)
                        || p.getDescription().toLowerCase(Locale.ROOT).contains(normalized))
                .toList();
    }

    public List<Product> searchByCategory(String query) {
        String normalized = normalize(query);
        if (normalized.isEmpty()) return List.of();
        return getCatalog().stream()
                .filter(p -> p.getCategory().getName().toLowerCase(Locale.ROOT).contains(normalized))
                .toList();
    }

    private String normalize(String value) {
        return value == null ? "" : value.trim().toLowerCase(Locale.ROOT);
    }

    public void addToCart(Cart cart, int productId, int quantity) {
        Product product = products.get(productId);
        if (product == null) throw new IllegalArgumentException("Товар з таким ID не знайдено.");
        cart.addProduct(product, quantity);
    }

    public BigDecimal getCartTotal(Cart cart) {
        return cart.getTotal(getCatalog());
    }

    public List<Cart.CartLine> getCartLines(Cart cart) {
        return cart.getLines(getCatalog());
    }

    public Order checkout(Cart cart) {
        Order order = new Order(getCartLines(cart));
        orderHistory.add(order);
        cart.clear();
        return order;
    }

    public List<Order> getOrderHistory() {
        return List.copyOf(orderHistory);
    }
}
