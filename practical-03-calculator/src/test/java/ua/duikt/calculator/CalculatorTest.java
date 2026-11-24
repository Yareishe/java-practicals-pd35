package ua.duikt.calculator;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class CalculatorTest {
    private final Calculator calculator = new Calculator();

    @Test void addsTwoNumbers() { assertEquals(7.5, calculator.add(3.0, 4.5), 1e-9); }
    @Test void subtractsTwoNumbers() { assertEquals(-1.5, calculator.subtract(3.0, 4.5), 1e-9); }
    @Test void multipliesTwoNumbers() { assertEquals(13.5, calculator.multiply(3.0, 4.5), 1e-9); }
    @Test void dividesTwoNumbers() { assertEquals(2.0, calculator.divide(9.0, 4.5), 1e-9); }
    @Test void divisionByZeroThrowsArithmeticException() {
        assertThrows(ArithmeticException.class, () -> calculator.divide(5.0, 0.0));
        assertThrows(ArithmeticException.class, () -> calculator.divide(5.0, -0.0));
    }
    @Test void rejectsNonFiniteInputsWithCustomException() {
        assertThrows(InvalidInputException.class, () -> calculator.add(Double.NaN, 1.0));
        assertThrows(InvalidInputException.class, () -> calculator.multiply(1.0, Double.POSITIVE_INFINITY));
    }
}
