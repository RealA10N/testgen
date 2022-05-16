# TESTGEN

TESTGEN is a simple Python package that is intended to be used by short
scripts to generate test cases for competitive programming problems.

By using TESTGEN you are not required to store the generated test cases on disk;
TESTGEN promises that the generated tests will be reproducible, meaning that
if you generate them again you will get the exact same test cases.

## Rational

In competitive programming, you are provided with an algorithmic problem that
you have to solve and then write a piece of code that will solve the problem
for you. Your solution is then executed with a predefined set of test cases,
and if your solution outputs the expected output on each test case in the given
amount of time, your solution is considered *CORRECT*.

Writing those test cases manually is not really practical, and often you write
a program that generates those tests for you. Instead of writing those scripts
from the ground up for every problem that you need to generate test cases for,
you can think of TESTGEN as a framework that provides you with useful functions
and boilerplate you *will* eventually use.

In addition, there my be hundreds of different test cases that you will have to
generate to a single problem, and each test case can take up to a couple of
megabytes of storage on the disk. Instead of storing all those test cases,
TESTGEN allows you to write your test generation script in such a way that will
always output the same test cases (even if they use randomness) by using a seed
and a well-formed order of generation. By using TESTGEN you are only required
to store a configuration file named `tests.toml` with your test generation
script, and TESTGEN will generate the tests every time you run the generation
script.
