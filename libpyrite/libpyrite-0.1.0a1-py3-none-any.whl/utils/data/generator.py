from torch.utils.data.dataloader import default_collate


class _FiniteDataGeneratorIter:
    def __init__(self, generator, steps, batch_size, collate_fn):
        self.generator = generator
        self.steps = steps
        self.batch_size = batch_size
        self.collate_fn = collate_fn
        self._count = 0

    def __next__(self):
        if self._count >= self.steps:
            raise StopIteration()

        data = []
        for _ in range(self.batch_size):
            try:
                data.append(next(self.generator))
            except StopIteration:
                if not data:
                    raise

        self._count += 1
        return self.collate_fn(data)


class FiniteDataGenerator:
    def __init__(
        self, generator_factory, steps, batch_size=1, collate_fn=default_collate
    ):
        self.generator_factory = generator_factory
        self.steps = steps
        self.batch_size = batch_size
        self.collate_fn = collate_fn

    def __iter__(self):
        return _FiniteDataGeneratorIter(
            self.generator_factory(), self.steps, self.batch_size, self.collate_fn
        )

    def __len__(self):
        return self.steps


__all__ = ["FiniteDataGenerator"]
