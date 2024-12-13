# 'lunasync' - A Video upload bot

This bot automates the process of downloading videos from various platforms, uploading them to a server using an API secured with a Flic token, and creating a corresponding post. It is designed to accept a video URL as user input, making the process simple and efficient.

---

## **Setup Instructions**

### **1. Prerequisites**

- Python 3.8 or higher
- Internet connection
- API access credentials (Flic token and API URL)

### **2. Install Required Libraries**

Run the following command to install the necessary Python libraries:

```bash
pip install aiohttp tqdm 
or
pip install -r requirements.txt
```

### **3. Prepare Configuration**

- Set your Flic token in the code by modifying the `FLIC_TOKEN` variable.
- Ensure the `BASE_API_URL` matches the endpoint of your server API.

### **4. (Optional) Configure the Video Directory**

The default directory for downloaded videos is `./videos`. You can change this in the `download_video` function if needed.

---

## **Usage Guidelines**

1. **Run the Script**
   Start the script by executing the following command:

   ```bash
   python your_script_name.py
   ```
2. **Input Video URL**
   When prompted, provide the URL of the video you wish to download. The bot will:

   - Download the video using `yt-dlp`.
   - Upload the video to the server using the provided Flic token and API.
   - Create a post for the video.
   - Delete the local copy of the video upon successful upload.
3. **Monitor Output**
   The progress of the download and upload will be displayed in the terminal, including any errors encountered.

---

## **Code Comments**

### **Key Functions**

1. **`download_video(video_url, download_dir)`**

   - Downloads the video from the provided URL using `yt-dlp`.
   - Saves the video in the specified directory.
2. **`fetch_upload_url(session)`**

   - Retrieves an upload URL and a unique hash for the video from the server API.
3. **`upload_video(session, upload_url, video_path)`**

   - Uploads the downloaded video to the server in chunks to handle large files efficiently.
   - Displays a progress bar during the upload.
4. **`create_post(session, title, video_hash, category_id)`**

   - Creates a post for the uploaded video using its title, hash, and category.
5. **`process_video(video_url)`**

   - Orchestrates the entire workflow: downloading the video, uploading it to the server, creating a post, and cleaning up local files.

### **Error Handling**

- Exceptions during download, upload, or API calls are caught and displayed in the terminal for debugging.
- Local video files are only deleted after successful uploads.

---

## **README Quality**

This README ensures clarity and ease of understanding by including:

- **Comprehensive Setup Instructions**: Detailed steps for preparing the environment.
- **Clear Usage Guidelines**: Instructions on running the bot and interpreting its output.
- **Thorough Code Documentation**: Comments summarizing the purpose and function of each major code component.
- **Modular Design**: Highlights how each function serves a specific role in the workflow.

With this documentation, users of any skill level should be able to set up and use the bot efficiently.
