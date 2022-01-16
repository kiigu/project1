import logging
import time
import os
from threading import Thread

from pytube import YouTube

from yt_concate.pipeline.steps.step import Step
from yt_concate.settings import VIDEOS_DIR


class DownloadVideos(Step):
    def process(self, data, inputs, utils):  # 上一步驟Search所return的資料為found字典，在此會作為data傳入
        logger = logging.getLogger()
        start = time.time()
        yt_set = list(set([found.yt for found in data]))  # 利用set功能去除重複的yt清單，避免重複下載影片
        logger.info(f'Videos to download = {len(yt_set)}')
        yt_lst = [yt_set[i:i + (len(yt_set) // os.cpu_count()+1)] for i in range(0, len(yt_set), (len(yt_set) // os.cpu_count()+1))]
        threads = []
        for i in range(os.cpu_count()):
            threads.append(Thread(target=self.multi_download2, args=(yt_lst[i], utils)))
            threads[i].start()
        for thread in threads:
            thread.join()
        end = time.time()
        logger.info(f'Downloading videos took {end - start} seconds')

        return data

    def multi_download2(self, yt_set, utils):
        logger = logging.getLogger()
        for yt in yt_set:
            if utils.video_file_exists(yt):
                logger.info(f'Found existing video file for {yt.url}, skipped')
                continue
            logger.info(f'downloading {yt.url}')
            yt_dl = YouTube(yt.url).streams.get_highest_resolution()
            yt_dl.download(output_path=VIDEOS_DIR, filename=yt.id + '.mp4')
