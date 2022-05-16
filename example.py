from __future__ import annotations
from testgen import TestCase, TestCollection
from dataclasses import dataclass


MAX_ARRAY_SIZE = int(2e5)
MAX_ELEMENT = int(1e9)


@dataclass
class ArraySum(TestCase):
    input: list[int]

    def write_input(self, input_f) -> None:
        print(len(self.input), file=input_f)
        print(' '.join(str(i) for i in self.input), file=input_f)

    def write_answer(self, answer_f, input_f) -> None:
        print(sum(self.input), file=answer_f)

    def validate(self) -> None:
        assert 1 <= len(self.input) <= MAX_ARRAY_SIZE
        for v in self.input:
            assert 1 <= v <= MAX_ELEMENT


tests = TestCollection('data/secret', ArraySum)


@tests.collect(desc='max sized array filled with ones')
def all_zeros() -> ArraySum:
    return ArraySum([1] * MAX_ARRAY_SIZE)


@tests.collect(desc='random max sized array', repeat=3)
def random_list(random) -> ArraySum:
    return ArraySum(
        [random.randint(1, MAX_ELEMENT) for _ in range(MAX_ARRAY_SIZE)]
    )


if __name__ == '__main__':
    tests.generate()
