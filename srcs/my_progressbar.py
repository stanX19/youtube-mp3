from tqdm import tqdm
from pathlib import Path

progressbar = None
filename = None


def my_hook(d):
    global progressbar, filename
    try:
        if d['status'] != 'downloading':
            if isinstance(progressbar, tqdm):
                progressbar.close()
                progressbar = None
            return

        total = round(float(d['total_bytes']))
        current = round(float(d['downloaded_bytes']))

        if filename != d['filename'] or progressbar is None:
            if isinstance(progressbar, tqdm):
                progressbar.close()
            filename = d['filename']
            basename = Path(filename).stem
            progressbar = tqdm(range(total + 1), f"Downloading [{basename}]", leave=False)

        if isinstance(progressbar, tqdm):
            progressbar.update(current - progressbar.n)

    except (TypeError, KeyError):
        pass
