from functools import reduce

import tasks


@tasks.task(name='multiprint')
def multi_print(msg, count=10):
    return '\n'.join(msg for _ in range(count))


class Multiply(tasks.BaseTask):
    name = 'mult'

    def run(self, operands):
        return reduce(lambda x, y: x*y, operands)


if __name__ == '__main__':
    # print(multi_print("nya", count=5))
    print("Result:", tasks.run_cli())
