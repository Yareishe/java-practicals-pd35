package ua.duikt.calculator;

/** Basic arithmetic operations over finite double values. */
public final class Calculator {
    public double add(double first, double second) {
        validate(first, second);
        return first + second;
    }

    public double subtract(double first, double second) {
        validate(first, second);
        return first - second;
    }

    public double multiply(double first, double second) {
        validate(first, second);
        return first * second;
    }

    public double divide(double first, double second) {
        validate(first, second);
        if (second == 0.0) {
            throw new ArithmeticException("Ділити на нуль не можна.");
        }
        return first / second;
    }

    private void validate(double first, double second) {
        if (!Double.isFinite(first) || !Double.isFinite(second)) {
            throw new InvalidInputException("Числа мають бути скінченними значеннями.");
        }
    }
}
