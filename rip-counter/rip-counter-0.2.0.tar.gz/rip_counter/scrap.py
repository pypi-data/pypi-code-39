import asyncio

from rip_counter.captcha_solver import CaptchaNetSolver
from rip_counter.scraper import RIPScraper


def main():

  captcha_solver = CaptchaNetSolver(preload_model=True)

  scraper = RIPScraper(captcha_solver=captcha_solver,
                       max_captcha_try=20,
                       shuffle_urls=True)

  scrap_task = scraper.scrap(batch_size=64, show_progress=True, _test_mode=False)

  loop = asyncio.get_event_loop()
  loop.run_until_complete(scrap_task)
  loop.close()

  # Preprocess data
  scraper.process_data()


if __name__ == "__main__":
  main()
