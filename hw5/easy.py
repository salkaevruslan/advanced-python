import os
import sys
import asyncio
import aiohttp
import aiofiles


async def download_site(url, session, idx, output_folder):
    async with session.get(url) as response:
        if response.status != 200:
            print(f"Failure: {response.status}")
            return
        async with aiofiles.open(f"{output_folder}/img_{idx}.jpg", mode="wb") as f:
            await f.write(await response.read())
            print(f"Received {response.content.total_bytes} bytes from picture {idx}")


async def download_sites(sites, output_folder):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, url in enumerate(sites):
            tasks.append(asyncio.create_task(download_site(url, session, i, output_folder)))
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as ex:
            print(repr(ex))


if __name__ == "__main__":
    if not os.path.exists("artifacts"):
        os.mkdir("artifacts")
    if not os.path.exists("artifacts/easy"):
        os.mkdir("artifacts/easy")
    args = sys.argv[1:]
    if len(args) != 2:
        print("Required args: pictures_number: int, output_dir: str")
        exit(1)
    pictures_number = 10
    try:
        pictures_number = int(args[0])
    except ValueError:
        print("First arg(pictures_number) must be int")
        exit(1)
    output_dir = "artifacts/easy"
    try:
        os.makedirs(os.path.dirname(args[1]), exist_ok=True)
        output_dir = args[1]
    except FileNotFoundError:
        print("Second arg(output_dir) must be directory")
    loop = asyncio.get_event_loop()
    try:
        task = loop.create_task(download_sites(["https://picsum.photos/200/300"] * pictures_number, output_dir))
        loop.run_until_complete(task)
    finally:
        loop.close()
