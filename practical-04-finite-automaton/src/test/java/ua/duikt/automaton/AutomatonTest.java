package ua.duikt.automaton;

import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class AutomatonTest {
    private final Automaton automaton = new Automaton();

    @ParameterizedTest(name = "input '{0}' ends in state {1}")
    @CsvSource({
            "'', S",
            "abc, S",
            "T, 1",
            "abcT, 1",
            "TE, 2",
            "abcTE, 2",
            "TES, 3",
            "abcTES, 3",
            "TEST, F",
            "abcTESTabc, F",
            "TTEST, F",
            "TETEST, F",
            "TESTTEST, F",
            "TESTE, F"
    })
    void returnsExpectedFinalState(String input, String expectedLabel) {
        assertEquals(expectedLabel, automaton.run(input).label());
    }

    @ParameterizedTest(name = "from {0} on '{1}' -> {2}")
    @CsvSource({
            "S, T, 1",
            "S, x, S",
            "ONE, E, 2",
            "ONE, T, 1",
            "ONE, x, S",
            "TWO, S, 3",
            "TWO, T, 1",
            "TWO, x, S",
            "THREE, T, F",
            "THREE, E, S",
            "F, x, F"
    })
    void followsTransitionTable(Automaton.State from, char symbol, String expectedLabel) {
        assertEquals(expectedLabel, automaton.transition(from, symbol).label());
    }

    @ParameterizedTest(name = "overlap in '{0}' still finds TEST")
    @CsvSource({
            "TTEST",
            "TETEST",
            "TTTEST",
            "TETTEST",
            "abcTETESTxyz"
    })
    void findsMatchesAfterOverlappingPartialPrefixes(String input) {
        assertEquals(Automaton.State.F, automaton.run(input));
    }

    @org.junit.jupiter.api.Test
    void rejectsNullInput() {
        assertThrows(NullPointerException.class, () -> automaton.run(null));
    }
}
