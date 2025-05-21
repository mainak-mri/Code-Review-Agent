## General rules

1. Follow standard conventions.
2. Keep it simple stupid. Simpler is always better. Reduce complexity as much as possible.
3. Boy scout rule. Leave the campground cleaner than you found it.
4. Always find root cause. Always look for the root cause of a problem.

## Design rules

1. Keep configurable data at high levels.
2. Prefer polymorphism to if/else or switch/case.
3. Prevent over-configurability.
4. Use dependency injection.
5. Follow Law of Demeter. A class should know only its direct dependencies.

## Understandability tips

1. Be consistent. If the code does something a certain way, do all similar things in the same way.
2. Use explanatory variables.
3. Prefer dedicated value objects to primitive type.
4. Avoid logical dependency. Don't write methods which works correctly depending on something else in the
    same class.
5. Avoid negative conditionals.

## Names rules

1. Choose descriptive and unambiguous names within reason
2. Make meaningful distinction.
3. Use pronounceable names.
4. Use searchable names.
5. Replace magic numbers with named constants.
6. Avoid encodings. Don't append prefixes (e.g. arg, txt, ddl) or type information.


## Functions rules

1. Small.
2. Do one thing.
3. Use descriptive names.
4. Prefer fewer arguments.
5. Have no side effects.
6. Don't use flag arguments. Split method into several independent methods that can be called from the
    client without the flag.
## Source code structure

1. Separate concepts vertically.
2. Related code should appear vertically dense.
3. Declare variables close to their usage.
4. Dependent functions should be close.
5. Similar functions should be close.
6. Place functions in the downward direction.
7. Keep lines short.
8. Don't use horizontal alignment.
9. Use white space to associate related things and disassociate weakly related.
10. Don't break indentation.


## Objects and data structures

1. Hide internal structure.
2. Prefer pure data structures rather than hybrids structures (half logic and half data).
3. Should be small.
4. Do one thing.
5. Small number of instance variables.
6. Base class should know nothing about their derivatives.
7. Better to have many functions than to pass some "code/flag"into a function to select a behavior.
    EXAMPLE
8. Prefer non-static methods to static methods.

## Tests

1. Test one thing.
2. Readable.
3. Independent.
4. Repeatable.
    Unit Test Standards

## Code smells

1. Rigidity. The software is difficult to change. A small change causes a cascade of subsequent changes.
2. Fragility. The software breaks in many places due to a single change.
3. Immobility. You cannot reuse parts of the code in other projects because of involved risks and high effort.
4. Needless Complexity.
5. Needless Repetition.
6. Opacity. The code is hard to understand.

```
