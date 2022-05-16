from __future__ import annotations
from testgen import TestCase, TestCollection
from dataclasses import dataclass


@dataclass
class ArraySum(TestCase):
    input: list[int]

    def write_in(self, input_f) -> None:
        print(len(self.input), file=input_f)
        print(' '.join(str(i) for i in self.input), file=input_f)

    def write_ans(self, answer_f, input_f) -> None:
        print(sum(self.input), file=answer_f)


MAX_ARRAY_SIZE = int(2e5)
tests = TestCollection('data/secret', ArraySum)


@tests.collect(desc='max sized array filled with zeros')
def all_zeros() -> ArraySum:
    return ArraySum([0] * MAX_ARRAY_SIZE)


@tests.collect(desc='random max sized array', repeat=3)
def random_list(random) -> ArraySum:
    return ArraySum(
        [random.randint(1, int(1e9)) for _ in range(MAX_ARRAY_SIZE)]
    )


if __name__ == '__main__':
    tests.generate()
