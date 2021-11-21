from project1.pipeline.pipeline import Pipeline
from project1.pipeline.steps.get_video_list import GetVideoList

CHANNEL_ID = 'UCgc00bfF_PvO_2AvqJZHXFg'


def main():
    inputs = {
        'channel_id': CHANNEL_ID
    }

    steps = [
        GetVideoList(),
    ]

    p = Pipeline(steps)
    p.run(inputs)


if __name__ == '__main__':
    main()
