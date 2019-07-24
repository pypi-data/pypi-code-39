import os
import asyncio
import time
import concurrent.futures


async def _run(task, arg_list, workers):
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(task, *args) for args in arg_list}
        for future in concurrent.futures.as_completed(futures):
            data = future.result()
            print(data)


def run_batch(task, arg_list, workers):
    _start = time.time()
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    try:
        future = asyncio.ensure_future(task, arg_list, workers)
        loop.run_until_complete(future)
        print(f"Execution time: { time.time() - _start }")
    finally:
        loop.close()
