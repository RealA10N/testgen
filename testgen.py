from __future__ import annotations

import os
from math import floor, log10
from abc import abstractmethod, ABC
from dataclasses import dataclass, asdict
from random import Random
from typing import Callable, TextIO, Type, TypeVar
import platform
import shutil
import inspect

import toml

from rich.console import Console
from rich.prompt import Confirm
console = Console()

SEED_RANGE = (1, 1_000_000)
DEFAULT_TESTS_CONFIG = 'testgen.toml'

T = TypeVar('T')

__all__ = ['TestCollection', 'TestCase']


@dataclass
class TestsConfig:
    name: str
    seed: int
    check: int

    def dump(self) -> None:
        data = asdict(self)
        del data['name']
        with open(self.name, 'w', encoding='utf8') as f:
            toml.dump(data, f)

    @classmethod
    def generate_config(cls: Type[T], name: str) -> T:
        """ Generate a random seed, and then use the seed to generate the check
        integer. Returns a new instance of the configuration object with the
        generated data. """

        src = Random()
        seed = src.randint(*SEED_RANGE)
        check = Random(seed).randint(*SEED_RANGE)
        return cls(name=name, seed=seed, check=check)

    @classmethod
    def load(cls: Type[T], name: str) -> T:
        """ Tries to load a configuration with the given name.
        If such configuration does not exist, creates a new one with a random
        seed. """

        data = toml.load(name)
        return cls(name=name, **data)

    def get_random(self) -> Random:
        return Random(self.seed)

    def check_seed(self) -> bool:
        return self.get_random().randint(*SEED_RANGE) == self.check


class TestCase(ABC):

    @abstractmethod
    def write_in(self, file: TextIO) -> None:
        pass

    @abstractmethod
    def write_ans(self, file: TextIO) -> None:
        pass


TestCaseT = TypeVar('TestCaseT', bound=TestCase)
TestCaseBuilder = Callable[[], TestCaseT]


@dataclass
class CollectedTestCase:
    builder: TestCaseBuilder
    name: str = None
    desc: str = None


class TestCollection:

    def __init__(
        self,
        folder: str,
        testcase_type: Type[TestCaseT],
        config: str = DEFAULT_TESTS_CONFIG,
    ) -> None:
        """ Initialize a new test collection in the given folder with the
        given configuration file. The configuration file is usually named
        tests.toml and is a sibling of the tests folder. """

        self.folder = folder
        self.testcase_type = testcase_type
        self.config = self._setup_config(config)
        self.builders: list[CollectedTestCase] = list()

    def _setup_config(self, cfgname: str) -> TestsConfig:
        """ Load or create a new tests configuration file with the given
        name. Uses prompts to talk with the user if the configuration file
        is corrupted or if the check doesn't match the seed. """

        console.rule('Environemt')
        console.print(
            'running on [yellow bold]'
            f'Python {platform.python_version()}[/]'
        )

        try:
            cfg = TestsConfig.load(cfgname)

        except FileNotFoundError:
            console.print(f'{cfgname!r} not found.')
            if not Confirm.ask(f'Generate a new {cfgname!r} file?'):
                raise SystemExit(1) from None
            cfg = TestsConfig.generate_config(cfgname)

        except (toml.TomlDecodeError, TypeError):
            console.print(f'[bold red]{cfgname!r} is corrupted.[/]')
            if not Confirm.ask(f'Generate a new {cfgname!r} file?'):
                raise SystemExit(1) from None
            cfg = TestsConfig.generate_config(cfgname)

        if cfg.check_seed():
            console.print('[green]seed check [bold]PASSED![/]')
        else:
            console.print('[red]seed check [bold]FAILED[/].')
            if not Confirm.ask('Continue test generation?'):
                raise SystemExit(1)

        cfg.dump()
        return cfg

    def collect(self, desc: str = None, repeat: int = 1) -> Callable:
        """ A function that returns a decorator. The decorated function will
        be stored in the test collection. """

        def decorator(builder: TestCaseBuilder):
            for _ in range(repeat):
                self.builders.append(
                    CollectedTestCase(
                        builder=builder,
                        name=builder.__name__,
                        desc=desc,
                    )
                )
            return builder

        return decorator

    @staticmethod
    def _generte_testcase_data(func: TestCaseBuilder, rnd: Random) -> TestCaseT:
        sig = inspect.signature(func)
        kwargs = dict()
        if 'random' in sig.parameters:
            kwargs['random'] = rnd
        return func(**kwargs)

    def _build(
        self,
        builder: TestCaseBuilder,
        name: str,
        rnd: Random,
        desc: str = None,
    ) -> None:
        console.log(f'[bold yellow]generating test case {name!r}[/]')
        test = self._generte_testcase_data(builder, rnd)
        console.log('generated test case data')

        in_path = os.path.join(self.folder, f'{name}.in')
        with open(in_path, 'w', encoding='utf8') as f:
            test.write_in(f)
        console.log(f'generated {in_path!r}')

        ans_path = os.path.join(self.folder, f'{name}.ans')
        with open(ans_path, 'w', encoding='utf8') as f:
            test.write_ans(f)
        console.log(f'generated {ans_path!r}')

        if desc:
            desc_path = os.path.join(self.folder, f'{name}.desc')
            with open(desc_path, 'w', encoding='utf8') as f:
                print(desc, file=f)
            console.log(f'generated {desc_path!r}')

    def generate(self, first_test_i: int = 1) -> None:
        console.rule('Generation')

        os.makedirs(self.folder, exist_ok=True)
        if os.path.isdir(self.folder) and os.listdir(self.folder):
            console.print(f'{self.folder!r} is not empty.')
            if not Confirm.ask('Clear directory and continue?', console=console):
                raise SystemExit(1)
            shutil.rmtree(self.folder)
            os.makedirs(self.folder, exist_ok=True)

        assert len(self.builders) > 0
        max_i = first_test_i + len(self.builders) - 1
        leading_zeros = floor(log10(max_i)) + 1

        rnd = self.config.get_random()
        with console.status('Generating Test Cases'):
            for case, i in zip(
                    self.builders,
                    range(first_test_i, first_test_i + len(self.builders))
            ):
                istr = format(i, f'0{leading_zeros}d')
                name = istr if case.name is None else f'{istr}-{case.name}'
                self._build(
                    builder=case.builder,
                    name=name,
                    desc=case.desc,
                    rnd=rnd,
                )
