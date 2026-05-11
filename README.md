# Youtube-member-stream-sc-fetcher

Just a project for simp like me to find where is my SC in membership stream and to find out when will my oshi waifu read it. It will write a log file so that you can search it by yourself.

---
Here is a step-by-step guide on how to extract the necessary authentication headers and tokens from a YouTube video using your browser's Developer Tools.

# How to Extract YouTube Live Chat API Tokens

This guide explains how to find the `COOKIE_STRING`, `AUTH_HEADER`, `INITIAL_CONTINUATION`, and `API_KEY` required to interact with YouTube's internal `get_live_chat_replay` API.

## Prerequisites
1. Open your web browser (Chrome, Edge, or Brave).
2. Navigate to the YouTube video containing the chat replay you want to scrape.
3. **Make sure you are logged in** and have access to the video (especially if it is members-only).

## Step 1: Open Developer Tools
1. Press **F12** (or `Ctrl+Shift+I` / `Cmd+Option+I`) to open the Developer Tools.
2. Click on the **Network** tab at the top of the Developer Tools panel.
3. Check the **Preserve log** option (optional, but helpful).
4. In the "Filter" or "Search" box, type `get_live_chat_replay`.
5. Refresh the YouTube page (`F5`).

## Step 2: Extract `COOKIE_STRING` and `AUTH_HEADER`
1. Watch the Network tab as the page loads. Click on the first request named `get_live_chat_replay?...`.
2. On the right side, click the **Headers** tab.
3. Scroll down to the **Request Headers** section.
4. **`COOKIE_STRING`**: Find the header named `cookie:`. Right-click its value and copy the entire string (it will be very long and start with things like `VISITOR_INFO1_LIVE=...`).
5. **`AUTH_HEADER`**: Find the header named `authorization:`. Copy its value (it should look like `SAPISIDHASH 1122334455_abcdef123456...`). There will be multiple start with "SAPISID1PHASH" in one header, just get one. 

## Step 3: Extract `API_KEY`
There are two ways to find the API Key in the same request:
1. **From the URL**: Look at the very top of the **Headers** tab under `Request URL`. You will see `.../get_live_chat_replay?key=AIzaSy...`. Copy the value after `key=`.
2. **From Request Headers**: Scroll through the **Request Headers** section and look for `x-goog-api-key` or `x-youtube-client-key`. Copy its value. It almost always begins with `AIza...`.

## Step 4: Extract `INITIAL_CONTINUATION`
The continuation token is what tells YouTube where to start loading the chat.
1. Still looking at the same `get_live_chat_replay` request, click the **Payload** tab (next to the Headers tab).
2. Look for the `continuation` field. 
3. Right-click and copy the value. 
4. *Important Note*: A valid base64 continuation token usually ends with URL-encoded padding, like `%3D%3D` or `==`. Make sure you copy the entire string.

## Example Python Configuration
Once you have retrieved the values, paste them into your script variables like this:

```python
COOKIE_STRING = "VISITOR_INFO1_LIVE=..."
AUTH_HEADER = "SAPISIDHASH 1778499808_..."
API_KEY = "AIzaSyAO_..."
INITIAL_CONTINUATION = "op2w0wSFAR..."
```
