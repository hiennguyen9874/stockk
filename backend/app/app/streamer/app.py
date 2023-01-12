from multiprocessing import Process
from typing import List


def main() -> None:
    workers: List[Process] = list()

    while True:
        # Get list symbols from sqlalchemy
        pass

    # while True:
    #     for topic_idx, (consume, create_topic_if_not_exists) in enumerate(TOPIC):
    #         if len(workers[topic_idx]) == 0:
    #             create_topic_if_not_exists()

    #         num_alive = len([w for w in workers[topic_idx] if w.is_alive()])

    #         if settings.STREAMER_NUM_PROCESS == num_alive:
    #             continue

    #         for _ in range(settings.STREAMER_NUM_PROCESS - num_alive):
    #             p = Process(target=consume, daemon=True)
    #             p.start()
    #             workers[topic_idx].append(p)
    #             logger.info("Starting worker #{pid}", pid=p.pid)
