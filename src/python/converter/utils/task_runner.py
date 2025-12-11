from concurrent.futures import ThreadPoolExecutor


def run_tasks(func, jobs: list, max_workers: int = 8):
    """並列実行"""
    with ThreadPoolExecutor(max_workers=max_workers) as exe:
        # どれが好き？
        # exe.map(func, jobs)
        executor.submit(func, job)
