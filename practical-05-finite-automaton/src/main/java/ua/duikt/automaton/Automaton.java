package ua.duikt.automaton;

import java.util.Objects;

/** Deterministic finite automaton that searches for the case-sensitive substring TEST. */
public final class Automaton {
    public enum State {
        S("S"),
        ONE("1"),
        TWO("2"),
        THREE("3"),
        F("F");

        private final String label;

        State(String label) {
            this.label = label;
        }

        public String label() {
            return label;
        }
    }

    /** Returns the next state after consuming one character. */
    public State transition(State state, char symbol) {
        Objects.requireNonNull(state, "state must not be null");

        return switch (state) {
            case S -> symbol == 'T' ? State.ONE : State.S;
            case ONE -> switch (symbol) {
                case 'E' -> State.TWO;
                // This T can start a new match after the previous T.
                case 'T' -> State.ONE;
                default -> State.S;
            };
            case TWO -> switch (symbol) {
                case 'S' -> State.THREE;
                // Keep the suffix T as a possible start of TEST.
                case 'T' -> State.ONE;
                default -> State.S;
            };
            case THREE -> symbol == 'T' ? State.F : State.S;
            case F -> State.F;
        };
    }

    /** Processes the input from left to right and returns the final automaton state. */
    public State run(String input) {
        Objects.requireNonNull(input, "input must not be null");
        State state = State.S;
        for (int i = 0; i < input.length(); i++) {
            state = transition(state, input.charAt(i));
        }
        return state;
    }
}
