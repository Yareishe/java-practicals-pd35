package ua.duikt.calculator;

/** Raised when a user supplies a value the calculator cannot process. */
public final class InvalidInputException extends RuntimeException {
    public InvalidInputException(String message) { super(message); }
    public InvalidInputException(String message, Throwable cause) { super(message, cause); }
}
