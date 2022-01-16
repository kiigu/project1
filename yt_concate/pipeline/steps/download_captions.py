import os
import time
import logging
from threading import Thread

from pytube import YouTube

from yt_concate.pipeline.steps.step import Step


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger()
        start = time.time()
        threads = []
        data_lst = [data[i:i + (len(data)//os.cpu_count()+1)] for i in range(0, len(data), (len(data)//os.cpu_count()+1))]
        # 將data依照Multi-threading數量拆分
        for i in range(os.cpu_count()):
            threads.append(Thread(target=self.multi_download1, args=(data_lst[i], utils)))
            threads[i].start()
        for thread in threads:
            thread.join()
        end = time.time()
        logger.info(f'Downloading captions took {end - start} seconds')
        return data

    def multi_download1(self, data, utils):
        logger = logging.getLogger()
        for yt in data:
            logger.info(f'downloading caption for {yt.id}')
            if utils.caption_file_exists(yt):
                logger.info('found existing caption file')
                continue
            try:
                source = YouTube(yt.url)
                en_caption = source.captions.get_by_language_code('en')
                # a.en為自動產生的英文字幕，en為頻道自製英文字幕
                en_caption_convert_to_srt = (en_caption.generate_srt_captions())
            except (KeyError, AttributeError):
                logger.warning(f'Error when downloading caption for {yt.url}')
                continue

            text_file = open(yt.caption_filepath, 'w', encoding='utf-8')
            text_file.write(en_caption_convert_to_srt)
            text_file.close()
