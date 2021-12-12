from pytube import YouTube

from yt_concate.pipeline.steps.step import Step
from yt_concate.settings import VIDEOS_DIR


class DownloadVideos(Step):
    def process(self, data, inputs, utils):  # 上一步驟Search所return的資料為found字典，在此會作為data傳入
        yt_set = set([found.yt for found in data])  # 利用set功能去除重複的yt清單，避免重複下載影片
        print('Videos to download =', len(yt_set))
        for yt in yt_set:
            if utils.video_file_exists(yt):
                print(f'Found existing video file for {yt.url}, skipped')
                continue
            print('downloading', yt.url)
            YouTube(yt.url).streams.get_highest_resolution().download(output_path=VIDEOS_DIR, filename=yt.id + '.mp4')

        return data
