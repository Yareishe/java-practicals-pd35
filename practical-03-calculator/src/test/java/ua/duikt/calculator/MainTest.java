package ua.duikt.calculator;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class MainTest {
    @Test void parsesNumericInput() { assertEquals(12.5, Main.parseNumber("12.5"), 1e-9); }
    @Test void textInsteadOfNumberThrowsCustomException() {
        InvalidInputException error = assertThrows(InvalidInputException.class, () -> Main.parseNumber("abc"));
        assertTrue(error.getMessage().contains("не є числом"));
    }
    @Test void rejectsNanAsInput() { assertThrows(InvalidInputException.class, () -> Main.parseNumber("NaN")); }
    @Test void unsupportedOperationThrowsCustomException() {
        assertThrows(InvalidInputException.class, () -> Main.calculate(new Calculator(), 1.0, 2.0, "%"));
    }
}
