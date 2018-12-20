import ffmpy
import io
import subprocess


def transcode(data):
    stdout, _ = ffmpy.FFmpeg(
        inputs={'pipe:0': '-f h264'},
        outputs={'pipe:1': '-movflags frag_keyframe -c copy -f mp4'}
    ).run(input_data=data, stdout=subprocess.PIPE)

    return io.BytesIO(stdout)
