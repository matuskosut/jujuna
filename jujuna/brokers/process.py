"""Process broker."""
from . import Broker, python3, load_output
from jujuna.exporters import Exporter
import logging


log = logging.getLogger('jujuna.tests.broker')


class Process(Broker):
    """Process broker."""

    def __init__(self):
        """Init Process broker."""
        super().__init__()

    async def run(self, test_case, unit, idx):
        """Run tests."""
        rows = []
        async with Exporter(unit, self.named) as exporter:
            try:
                act = await unit.run(python3(exporter), timeout=10)
                results = load_output(act.data['results'])
            except Exception as exc:
                log.debug(exc)
                results = {}
            # print(results)
            for condition in test_case:
                rows.append((idx, '{} == present'.format(condition), condition in results), )

        return rows
