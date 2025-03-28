import os
import subprocess

from django.core.management.base import BaseCommand, CommandError
from lecture.models import LectureVideo


class Command(BaseCommand):
    help = "Optimize Video"

    def handle(self, *args, **kwargs):
        try:
            obj = LectureVideo.objects.filter(status="Pending").first()
            if obj:
                obj.status = "Processing"
                obj.is_running = True
                obj.save()
                input_video_path = obj.video_file.path
                output_directory = os.path.join(
                    os.path.dirname(input_video_path), "hls_output"
                )
                os.makedirs(output_directory, exist_ok=True)
                output_filename = (
                    os.path.splitext(os.path.basename(input_video_path))[0]
                    + "_hls.m3u8"
                )
                output_hls_path = os.path.join(output_directory, output_filename)
                output_thumbnail_path = os.path.join(
                    output_directory,
                    os.path.splitext(os.path.basename(input_video_path))[0]
                    + "thumbnail.jpg",
                )

                cmd = [
                    "ffmpeg",
                    "-i",
                    input_video_path,
                    "-c:v",
                    "h264",
                    "-c:a",
                    "aac",
                    "-hls_time",
                    "5",
                    "-hls_list_size",
                    "0",
                    "-hls_base_url",
                    "{{ dynamic_path }}/",
                    "-movflags",
                    "+faststart",
                    "-y",
                    output_hls_path,
                ]

                subprocess.run(cmd, check=True)

                # generate thumbnail
                ffmpeg_cmd = [
                    "ffmpeg",
                    "-i",
                    input_video_path,
                    "-ss",
                    "2",
                    "-vframes",
                    "1",
                    "-q:v",
                    "2",
                    "-y",
                    output_thumbnail_path,
                ]
                subprocess.run(ffmpeg_cmd, check=True)

                # Update the Video object status to 'Processed' or something similar
                obj.hls = output_hls_path
                obj.thumbnail = output_thumbnail_path
                obj.status = "Completed"
                obj.is_running = False
                obj.save()

                print(f"HLS segments generated and saved at: {output_hls_path}")
            else:
                print('No video with status "Pending" found.')

        except Exception as e:
            raise CommandError(e)
