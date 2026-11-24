package ua.duikt.shop.app;

import ua.duikt.shop.model.Cart;
import ua.duikt.shop.model.Order;
import ua.duikt.shop.model.Product;
import ua.duikt.shop.service.StoreService;

import java.util.List;
import java.util.Scanner;

/** Консольний інтерфейс інтернет-магазину. */
public class Main {
    private final Scanner scanner = new Scanner(System.in);
    private final StoreService store = new StoreService();
    private final Cart cart = new Cart();

    public static void main(String[] args) {
        new Main().run();
    }

    private void run() {
        System.out.println("=== Вітаємо в інтернет-магазині ===");
        boolean running = true;
        while (running) {
            printMenu();
            String choice = scanner.nextLine().trim();
            try {
                switch (choice) {
                    case "1" -> showCatalog();
                    case "2" -> addToCart();
                    case "3" -> showCart();
                    case "4" -> removeFromCart();
                    case "5" -> searchProducts();
                    case "6" -> checkout();
                    case "7" -> showOrderHistory();
                    case "0" -> running = false;
                    default -> System.out.println("Невідома команда. Оберіть пункт від 0 до 7.");
                }
            } catch (IllegalArgumentException | IllegalStateException exception) {
                System.out.println("Помилка: " + exception.getMessage());
            }
            if (running) System.out.println();
        }
        System.out.println("Дякуємо за покупки. До побачення!");
        scanner.close();
    }

    private void printMenu() {
        System.out.println("\nМеню:");
        System.out.println("1 - Переглянути каталог");
        System.out.println("2 - Додати товар до кошика");
        System.out.println("3 - Переглянути кошик");
        System.out.println("4 - Видалити товар з кошика");
        System.out.println("5 - Пошук товарів за назвою або категорією");
        System.out.println("6 - Оформити замовлення");
        System.out.println("7 - Історія замовлень");
        System.out.println("0 - Вийти");
        System.out.print("Ваш вибір: ");
    }

    private void showCatalog() {
        System.out.println("\n--- Каталог ---");
        store.getCatalog().forEach(System.out::println);
    }

    private void addToCart() {
        showCatalog();
        int id = readInt("Введіть ID товару: ");
        int quantity = readInt("Введіть кількість: ");
        store.addToCart(cart, id, quantity);
        System.out.println("Товар додано до кошика.");
    }

    private void showCart() {
        List<Cart.CartLine> lines = store.getCartLines(cart);
        if (lines.isEmpty()) {
            System.out.println("Кошик порожній.");
            return;
        }
        System.out.println("\n--- Ваш кошик ---");
        lines.forEach(line -> System.out.printf("ID %d | %s × %d | %s грн за шт. | Разом %s грн%n",
                line.productId(), line.name(), line.quantity(), line.unitPrice(), line.lineTotal()));
        System.out.println("Загальна вартість: " + store.getCartTotal(cart) + " грн");
    }

    private void removeFromCart() {
        showCart();
        if (cart.isEmpty()) return;
        int id = readInt("Введіть ID товару, який потрібно видалити повністю: ");
        if (cart.removeProduct(id)) System.out.println("Товар видалено з кошика.");
        else System.out.println("Товару з таким ID немає в кошику.");
    }

    private void searchProducts() {
        System.out.println("1 - пошук за назвою або описом; 2 - пошук за категорією");
        String mode = scanner.nextLine().trim();
        System.out.print("Введіть пошуковий запит: ");
        String query = scanner.nextLine();
        List<Product> results = switch (mode) {
            case "1" -> store.searchByName(query);
            case "2" -> store.searchByCategory(query);
            default -> throw new IllegalArgumentException("Оберіть тип пошуку 1 або 2.");
        };
        if (results.isEmpty()) System.out.println("За запитом нічого не знайдено.");
        else results.forEach(System.out::println);
    }

    private void checkout() {
        if (cart.isEmpty()) {
            System.out.println("Кошик порожній. Додайте товари перед оформленням замовлення.");
            return;
        }
        Order order = store.checkout(cart);
        System.out.println("\nЗамовлення оформлено:");
        System.out.println(order);
        System.out.println("Замовлення збережене в історії.");
    }

    private void showOrderHistory() {
        List<Order> history = store.getOrderHistory();
        if (history.isEmpty()) {
            System.out.println("Історія замовлень поки порожня.");
            return;
        }
        System.out.println("\n--- Історія замовлень ---");
        history.forEach(order -> System.out.println(order + "\n"));
    }

    private int readInt(String prompt) {
        System.out.print(prompt);
        String value = scanner.nextLine().trim();
        try {
            return Integer.parseInt(value);
        } catch (NumberFormatException exception) {
            throw new IllegalArgumentException("Потрібно ввести ціле число.");
        }
    }
}
