package ua.duikt.calculator;

import java.util.Scanner;

/** Console entry point for a single arithmetic request. */
public final class Main {
    private Main() { }

    public static void main(String[] args) {
        try (Scanner scanner = new Scanner(System.in)) {
            System.out.print("Введіть перше число: ");
            double first = parseNumber(scanner.nextLine());
            System.out.print("Введіть друге число: ");
            double second = parseNumber(scanner.nextLine());
            System.out.print("Операція (+, -, *, /): ");
            String operation = scanner.nextLine().trim();
            double result = calculate(new Calculator(), first, second, operation);
            System.out.println("Результат: " + result);
        } catch (ArithmeticException e) {
            System.out.println("Помилка арифметики: " + e.getMessage());
        } catch (InvalidInputException e) {
            System.out.println("Некоректне введення: " + e.getMessage());
        } finally {
            System.out.println("Обробку запиту завершено.");
        }
    }

    static double parseNumber(String text) {
        try {
            double value = Double.parseDouble(text.trim());
            if (!Double.isFinite(value)) {
                throw new InvalidInputException("Введіть скінченне число.");
            }
            return value;
        } catch (NumberFormatException e) {
            throw new InvalidInputException("«" + text + "» не є числом.", e);
        }
    }

    static double calculate(Calculator calculator, double first, double second, String operation) {
        return switch (operation) {
            case "+" -> calculator.add(first, second);
            case "-" -> calculator.subtract(first, second);
            case "*" -> calculator.multiply(first, second);
            case "/" -> calculator.divide(first, second);
            default -> throw new InvalidInputException("Невідома операція: " + operation);
        };
    }
}
