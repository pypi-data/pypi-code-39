import asyncio
import concurrent.futures


async def _run(tasks, workers):
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(task[0], *task[1:]) for task in tasks}
        for future in concurrent.futures.as_completed(futures):
            data = future.result()
            print(data)


def run_concurrent(tasks, workers=2):
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    try:
        future = asyncio.ensure_future(_run(tasks, workers))
        loop.run_until_complete(future)
    finally:
        loop.close()
