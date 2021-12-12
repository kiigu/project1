import os

from pprint import pprint

from yt_concate.pipeline.steps.step import Step
from yt_concate.pipeline.steps.step import StepException
from yt_concate.settings import CAPTIONS_DIR


class ReadCaption(Step):
    def process(self, data, inputs, utils):
        for yt in data:
            if not utils.caption_file_exists(yt):
                continue

            captions = {}
            with open(yt.caption_filepath, 'r', encoding='utf-8') as f:
                time_line = False
                time = None
                caption = None
                for line in f:
                    line = line.strip()  # 擷取()以外的內容
                    if '-->' in line:  # 利用標記找出呈現時間的列別
                        time_line = True
                        time = line
                        continue
                    if time_line:  # 此寫法即為time_line = True的意思
                        caption = line
                        captions[caption] = time  # 因為接下來的步驟是要辨識caption內容有沒有包含特定文字，所以把caption設定為key，比較好用for迴圈選取
                        time_line = False
            yt.captions = captions

        return data

# 採用字典的寫法，太過複雜彈性低
# class ReadCaption(Step):
#     def process(self, data, inputs, utils):
#         data = {}  # 設置一個字典裝所有字幕資料，並以檔名作為key
#         for caption_file in os.listdir(CAPTIONS_DIR):
#             captions = {}
#             with open(os.path.join(CAPTIONS_DIR, caption_file), 'r', encoding='utf-8') as f:
#                 time_line = False
#                 time = None
#                 caption = None
#                 for line in f:
#                     line = line.strip()  # 擷取()以外的內容
#                     if '-->' in line:  # 利用標記找出呈現時間的列別
#                         time_line = True
#                         time = line
#                         continue
#                     if time_line:  # 此寫法即為time_line = True的意思
#                         caption = line
#                         captions[caption] = time  # 因為接下來的步驟是要辨識caption內容有沒有包含特定文字，所以把caption設定為key，比較好用for迴圈選取
#                         time_line = False
#             data[caption_file] = captions
#
#         pprint(data)
#         return data
