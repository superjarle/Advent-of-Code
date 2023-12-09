import java.io.File
import kotlin.system.measureTimeMillis

fun extrapolateValue(history: List<Int>): Int {
    val sequences = mutableListOf(history.toMutableList())
    while (sequences.last().toSet().size > 1) {
        sequences.add(sequences.last().windowed(2).map { it[1] - it[0] }.toMutableList())
    }
    for (i in sequences.size - 2 downTo 0) {
        sequences[i].add(sequences[i].last() + sequences[i + 1].last())
    }
    return sequences.first().last()
}

fun <T> profiler(method: () -> T): T {
    var result: T
    val elapsedTime = measureTimeMillis {
        result = method()
    }
    println("Method ${method::class.simpleName} took: ${elapsedTime / 1000.0} sec")
    return result
}

fun part1(puzzleInput: String): Int {
    val histories = File(puzzleInput).readLines().map { it.split("\\s+".toRegex()).map(String::toInt) }
    return histories.sumOf { extrapolateValue(it) }
}

fun part2(puzzleInput: String): Int {
    val histories = File(puzzleInput).readLines().map { it.split("\\s+".toRegex()).map(String::toInt).reversed() }
    return histories.sumOf { extrapolateValue(it) }
}

fun main() {
    val puzzleInput = "day9.txt"
    println("Solution to part 1 is: ${profiler { part1(puzzleInput) }}")
    println("Solution to part 2 is: ${profiler { part2(puzzleInput) }}")
}