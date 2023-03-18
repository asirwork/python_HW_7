import sys
from pathlib import Path
import re
import random
import shutil

CATEGORIES = {
    "Image": [".jpeg", ".png", ".jpg", ".svg"],
    "Video": [".avi", ".mp4", ".mov", ".mkv"],
    "Documents": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"],
    "Audio": [".mp3", ".ogg", ".wav", ".amr"],
    "Archives": [".zip", ".gz", "tar"]
}

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l",
               "m", "n", "o", "p", "r", "s", "t", "u", "f", "h", "ts", "ch",
               "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name):
    fd_name = name.translate(TRANS)
    fd_name = re.sub(r'\W', '_', fd_name)
    return fd_name


def move_file(file: Path, root_dir: Path, category: str):
    target_dir = root_dir / category
    if not target_dir.exists():
        target_dir.mkdir()

    if file.suffix in CATEGORIES["Archives"]:
        shutil.unpack_archive(str(file),
                              str(target_dir.joinpath(normalize(file.stem))))

    try:
        file.rename(target_dir / f"{normalize(file.stem)}{file.suffix}")
    except FileExistsError:
        dub = random.randint(1, 999)
        file.rename(target_dir / f"{normalize(file.stem)}_{dub}{file.suffix}")
        print(f"Можливо дублікат: {file.name}")


def get_cattegories(file: Path):
    extension = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if extension in exts:
            return cat
    return "Others"


def sort_dir(root_dir: Path, current_dir: Path):

    for item in [
            f for f in current_dir.glob("*")
            if f.name not in CATEGORIES.keys()
    ]:
        if item.stem.lower() in [
                "image", "video", "documents", "audio", "archives", "others"
        ]:
            continue

        if not item.is_dir():
            category = get_cattegories(item)
            move_file(item, root_dir, category)
        else:
            sort_dir(root_dir, item)

            if item.stat().st_size == 0:
                item.rmdir()


def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return f"No path to folder"

    if not path.exists():
        return "Folder not exists"

    sort_dir(path, path)

    return "Сортування завершено"


if __name__ == "__main__":
    print(main())