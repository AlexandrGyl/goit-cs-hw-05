import asyncio
import argparse
import logging
from pathlib import Path
import aiofiles
import aiofiles.os

# Логування помилок у файл
logging.basicConfig(level=logging.ERROR, filename='errors.log',
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Асинхронне отримання вмісту директорії
async def async_iterdir(directory: Path):
    return await asyncio.to_thread(lambda: list(directory.iterdir()))


# Парсинг аргументів командного рядка
def parse_arguments():
    parser = argparse.ArgumentParser(description="Копіювання файлів з вихідної папки в папку призначення із сортуванням по розширенню файлів")
    parser.add_argument("source", help="Шлях до вихідної папки")
    parser.add_argument("destination", nargs='?', default="dist", help="Шлях до папки призначення (default: dist)")
    return parser.parse_args()

# Асинхронне читання директорії і копіювання файлів
async def read_folder(src_dir: Path, dst_dir: Path):
    try:
        items = await async_iterdir(src_dir)
        for item in items:
            if item.is_dir():
                await read_folder(item, dst_dir)
            else:
                await copy_file(item, dst_dir)
    except Exception as e:
        logging.error(f"Помилка при читанні {src_dir}: {e}")
        print(f"Помилка при читанні {src_dir}: {e}")

# Асинхронне копіювання файлу
async def copy_file(src_file: Path, dst_dir: Path):
    try:
        file_extension = src_file.suffix[1:] or "no_extension"

        dest_subdir = dst_dir / file_extension
        await aiofiles.os.makedirs(dest_subdir, exist_ok=True)

        dst_file_path = dest_subdir / src_file.name

        async with aiofiles.open(src_file, 'rb') as src, aiofiles.open(dst_file_path, 'wb') as dst:
            content = await src.read()
            await dst.write(content)

        print(f"Copied {src_file} to {dst_file_path}")

    except Exception as e:
        logging.error(f"Помилка при копіюванні {src_file}: {e}")
        print(f"Помилка при копіюванні {src_file}: {e}")




# Основна асинхронна функція
async def main_async():
    args = parse_arguments()
    source_dir = Path(args.source)
    dest_dir = Path(args.destination)
    try:
        await read_folder(source_dir, dest_dir)
    except Exception as e:
        logging.error(f"Помилка у main_async: {e}")



    if not source_dir.exists():
        logging.error(f"Директорія {source_dir} не існує.")
        print(f"Директорія {source_dir} не існує.")
        return

    await aiofiles.os.makedirs(dest_dir, exist_ok=True)

    await read_folder(source_dir, dest_dir)
    print("Копіювання завершено.")


if __name__ == "__main__":
    asyncio.run(main_async())