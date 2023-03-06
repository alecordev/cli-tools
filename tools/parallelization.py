import time
import itertools

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, FIRST_COMPLETED, wait

HOW_MANY_TASKS_AT_ONCE = 2

initial_tasks = [1, 2, 3, 4]


def perform(task):
    time.sleep(task)
    print(task)
    return f'{task} completed.'


def get_follow_up_task(result):
    print(result)
    task = 1
    return task


def has_follow_up_task(result):
    print(result)
    return False


def threaded_run():
    with ThreadPoolExecutor() as executor:

        # Schedule the first N futures.  We don't want to schedule them all
        # at once, to avoid consuming excessive amounts of memory.
        futures = {
            executor.submit(perform, task): task
            for task in itertools.islice(initial_tasks, HOW_MANY_TASKS_AT_ONCE)
        }

        while futures:
            # Wait for the next future to complete.
            done, _ = wait(
                futures, return_when=FIRST_COMPLETED
            )

            # Process the results of any completed futures, then schedule any
            # follow-up tasks.  If there's a follow-up task, we don't want
            # to schedule a replacement task from the initial batch.
            new_tasks_to_schedule = 0

            for fut in done:
                original_task = futures.pop(fut)
                print(f"The outcome of {original_task} is {fut.result()}")

                if has_follow_up_task(fut.result()):
                    new_task = get_follow_up_task(fut.result())
                    fut = executor.submit(perform, new_task)
                    futures[fut] = new_task
                else:
                    new_tasks_to_schedule += 1

            # Schedule the next set of futures.  We don't want more than N futures
            # in the pool at a time, to keep memory consumption down.
            iterator = iter(initial_tasks)
            for task in itertools.islice(iterator, new_tasks_to_schedule):
                fut = executor.submit(perform, task)
                futures[fut] = task


def main():
    threaded_run()


if __name__ == '__main__':
    main()
