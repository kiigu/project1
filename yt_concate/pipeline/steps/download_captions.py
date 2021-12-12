import os
import time

from pytube import YouTube, exceptions

from yt_concate.pipeline.steps.step import Step
from yt_concate.pipeline.steps.step import StepException


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        start = time.time()
        for yt in data:
            print('downloading caption for', yt.id)
            if utils.caption_file_exists(yt):
                print('found existing caption file')
                continue

            try:
                source = YouTube(yt.url)
                en_caption = source.captions.get_by_language_code('en')  # a.en為自動產生的英文字幕，en為頻道自製英文字幕
                en_caption_convert_to_srt = (en_caption.generate_srt_captions())
            except (KeyError, AttributeError):
                print('Error when downloading caption for', yt.url)
                continue

            text_file = open(yt.caption_filepath, 'w', encoding='utf-8')
            text_file.write(en_caption_convert_to_srt)
            text_file.close()
        end = time.time()
        print('Downloading captions took', end - start, 'seconds')

        return data

