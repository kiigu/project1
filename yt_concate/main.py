# 做完logging和command line作業

import logging
import sys
sys.path.append('../')  # 增加讀取 yt_concate路徑
sys.path.append('C:\\Users\\PCC\\project1\\venv\\Lib\\site-packages')  # 加入讀取安裝在虛擬環境的套件路徑
import getopt
import time

from yt_concate.pipeline.pipeline import Pipeline
from yt_concate.pipeline.steps.preflight import Preflight
from yt_concate.pipeline.steps.get_video_list import GetVideoList
from yt_concate.pipeline.steps.initialize_yt import InitializeYT
from yt_concate.pipeline.steps.download_captions import DownloadCaptions
from yt_concate.pipeline.steps.read_caption import ReadCaption
from yt_concate.pipeline.steps.search import Search
from yt_concate.pipeline.steps.download_videos import DownloadVideos
from yt_concate.pipeline.steps.edit_videos import EditVideos
from yt_concate.pipeline.steps.postflight import Postflight
from yt_concate.utils import Utils


def print_usage():
    print('python yt_concate.py OPTIONS')
    print('OPTIONS')
    print('{:>6}{:<15}{}'.format('-c', '--channel_id', 'Channel ID of the Youtube channel'))
    print('{:>6}{:<15}{}'.format('-k', '--key_word', 'Key word to search in the channel'))
    print('{:>6}{:<15}{}'.format('-m', '--limit', 'Limit on the number of videos to be concatenated'))
    print('{:>6}{:<15}{}'.format('-e', '--level', 'Level of logging showed on the screen (ex.INFO=20)'))


def main():
    inputs = {
        'channel_id': 'UCb4-om3UY151Hu1uCR8Q19Q',
        'key_word': 'breathe',
        'limit': 100
    }
    st_level = 20

    long_opts = 'help channel_id= key_word= limit= level='.split()
    short_opts = 'hc:k:m:e:'
    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit(0)
        elif opt in ('-c', '--channel_id'):
            inputs['channel_id'] = arg
        elif opt in ('-k', '--key_word'):
            inputs['key_word'] = arg
        elif opt in ('-m', '--limit'):
            inputs['limit'] = arg
        elif opt in ('-e', '--level'):
            st_level = int(arg)

    if inputs['channel_id'] is False or inputs['key_word'] is False or inputs['limit'] is False or st_level is False:
        print_usage()
        sys.exit(2)

    steps = [
        Preflight(),
        GetVideoList(),
        InitializeYT(),
        DownloadCaptions(),
        ReadCaption(),
        Search(),
        DownloadVideos(),
        EditVideos(),
        Postflight()
    ]

    logger = logging.getLogger()
    logger.setLevel(0)
    formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(message)s')
    file_handler = logging.FileHandler('project.log')
    file_handler.setLevel(10)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(st_level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    utils = Utils()
    p = Pipeline(steps)
    start = time.time()
    p.run(inputs, utils)
    end = time.time()
    logger.info(f'Completing the whole process took {end - start} seconds')


if __name__ == '__main__':
    main()
