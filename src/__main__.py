import argparse, re, sys

from tqdm import tqdm

from search import get_search_results
from download import get_tube, get_streams



def main():
    argparser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Simple YouTube Downloader'
    )
    argparser.add_argument(
        'keywords',
        help='Url 또는 검색어',
        nargs='*'
    )
    args = argparser.parse_args()

    results = get_search_results(args.keywords)
    for i, row in enumerate(results, 1):
        line = "{}. {}".format(i, row['title'])
        print(line)
    print('=============================================================================')
    nlist = input('Input Your choices as seperate with comma: ')
    if not nlist:
        return

    nlist = nlist.split(',')
    nlist = list(map(int, nlist))

    for i, row in enumerate(results, 1):
        if i in nlist:
            tube = get_tube(row['link'])
            description = "Downloading {} from {}".format(tube.title, row['link'])
            print(description)

            streams = get_streams(tube, mime_type='audio/mp4')

            for stream in streams.all():
                pbar = tqdm(total=stream.filesize)
                def _on_progress(chunk, file_handler, bytes_remaining):
                    pbar.update(len(chunk))
                stream.on_progress = _on_progress
                stream.download()
                pbar.close()
  

if __name__ == "__main__":
    main()

            