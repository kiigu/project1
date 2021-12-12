from yt_concate.pipeline.steps.step import Step
from yt_concate.pipeline.steps.step import StepException
from yt_concate.model.found import Found

class Search(Step):
    def process(self, data, inputs, utils):
        key_word = inputs['key_word']

        found = []
        for yt in data:
            captions = yt.captions  # 拿出來的字幕資料為dic形式
            if not captions:
                continue

            for caption in captions:
                if key_word in caption:
                    time = captions[caption]
                    f = Found(yt, caption, time)
                    found.append(f)

        print(len(found))

        return found

