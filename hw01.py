import sys
from pathlib import Path
import shutil
from threading import Thread
import logging


def read_input_parameters() -> tuple[Path, Path]:
    if 1 <= len(sys.argv) <= 3:
        source_folder, *rest = sys.argv[1:]
        dest_folder = rest[0] if rest else "dest"
    else:
        print("Please pass 1 or 2 arguments: source, destination folders")
        sys.exit(1)

    return (source_folder, dest_folder)


# return list of all subfolders
def get_list_of_folders(source: Path) -> list[Path]:
    if not source.exists():
        raise ValueError(f"File or folder '{source} is not existing on disk.'")
    res = [obj for obj in source.rglob("*") if obj.is_dir()]
    res.append(source)
    return res


def copy_files(from_dir: Path, dest_root_dir: Path):
    for file in from_dir.iterdir():
        if file.is_file():
            suffix = file.suffix[1:] if file.suffix else "no_extension"
            dest_dir = dest_root_dir / suffix
            # create sub-dir if not exiusting
            dest_dir.mkdir(parents=True, exist_ok=True)
            logging.debug(f"Copping file '{file}' to '{dest_dir}'")
            shutil.copy(file, dest_dir / file.name)


# паралелізація копіювання через потоки
def process_dir_threads(folders: list[Path], dest_root_dir: Path):
    threads = []
    for folder in folders:
        th = Thread(target=copy_files, args=(folder, dest_root_dir,))
        th.start()
        threads.append(th)
    [th.join() for th in threads]


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(threadName)s : %(message)s'
    )

    try:
        source_folder, dest_folder = read_input_parameters()
        folders_lst = get_list_of_folders(Path(source_folder))
        process_dir_threads(folders_lst, Path(dest_folder))
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
