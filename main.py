import asyncio              # asyncio is for used for asynchronous programming, here it is fetching upload URLs and uploading videos without blocking the execution of other tasks
import aiohttp              # aiohttp lib is for for making API calls to the social media platform 
import os                   # os is for interacting with files, as we are accessing local files for video downloading and deletion
import hashlib              # maintains file integrity, After downloading a video, you can compute its hash (like SHA-256) to ensure that the file has been downloaded correctly
from pathlib import Path    # File and Directory Management
from tqdm import tqdm       # It basically shows the download progress of a video
import requests             # Sends http requests to download videos from user provided urls

# Configuration
FLIC_TOKEN = "flic_834caa35ace461832f6b9bce14e5b2526b83e5765854cbe55a1f0ebc2e617393"
BASE_API_URL = "https://api.socialverseapp.com"
VIDEOS_DIR = Path("./videos")
HEADERS = {
    "Flic-Token": FLIC_TOKEN,
    "Content-Type": "application/json"
}

# Ensure the videos directory exists
VIDEOS_DIR.mkdir(exist_ok=True)

def download_video(video_url):
    """Download video from the provided URL."""
    response = requests.get(video_url, stream=True)
    if response.status_code == 200:
        video_name = video_url.split("/")[-1]  # Get the video name from the URL
        video_path = VIDEOS_DIR / video_name
        with open(video_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return video_path
    else:
        raise Exception(f"Failed to download video: {response.status_code}")

# Utility Functions
async def fetch_upload_url(session):
    async with session.get(f"{BASE_API_URL}/posts/generate-upload-url", headers=HEADERS) as response:
        response.raise_for_status()
        return await response.json()

async def upload_video(session, upload_url, video_path):
    file_size = os.path.getsize(video_path)
    with open(video_path, 'rb') as file:
        with tqdm(total=file_size, unit='B', unit_scale=True, desc=f"Uploading {video_path.name}") as pbar:
            while True:
                chunk = file.read(8192)  # Read in 8KB chunks
                if not chunk:
                    break
                async with session.put(upload_url, data=chunk) as response:
                    response.raise_for_status()
                    pbar.update(len(chunk))

async def create_post(session, title, video_hash, category_id):
    payload = {
        "title": title,
        "hash": video_hash,
        "is_available_in_public_feed": False,
        "category_id": category_id
    }
    async with session.post(f"{BASE_API_URL}/posts", headers=HEADERS, json=payload) as response:
        response.raise_for_status()
        return await response.json()

async def process_video(session, video_path):
    print(f"Processing video: {video_path}")

    try:
        # Step 1: Get Upload URL
        upload_data = await fetch_upload_url(session)
        upload_url = upload_data['url']
        video_hash = upload_data['hash']

        # Step 2: Upload Video
        await upload_video(session, upload_url, video_path)

        # Step 3: Create Post
        video_title = "video from sakshi"  
        category_id = 69  
        await create_post(session, video_title, video_hash, category_id)

        # Step 4: Delete Local File
        os.remove(video_path)  # deleting the local file
        print(f"Uploaded and deleted: {video_path}")

    except Exception as e:
        print(f"Error processing {video_path}: {e}")
    print(f"Processing video: {video_path}")

    try:
        # Step 1: Get Upload URL
        upload_data = await fetch_upload_url(session)
        upload_url = upload_data['url']
        video_hash = upload_data['hash']

        # Step 2: Upload Video
        await upload_video(session, upload_url, video_path)

        # Step 3: Create Post
        video_title = video_path.stem  # Use file name as title
        category_id = 25
        await create_post(session, video_title, video_hash, category_id)

        # Step 4: Delete Local File
        os.remove(video_path)
        print(f"Uploaded and deleted: {video_path}")

    except Exception as e:
        print(f"Error processing {video_path}: {e}")

async def main():
    video_url = input("Enter the video URL to download: ")
    try:
        video_path = download_video(video_url)
        print(f"Downloaded video to: {video_path}")
        
        # Create an asyncio session and run the process_video function
        async with aiohttp.ClientSession() as session:
            await process_video(session, video_path)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())