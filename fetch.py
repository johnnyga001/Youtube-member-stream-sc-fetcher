import urllib.request
import json
import time

# 1. Paste your entire Cookie string from the Request Headers
COOKIE_STRING = ""
# 2. Paste your Authorization header from Request Headers (looks like "SAPISIDHASH ...")
AUTH_HEADER = ""
# 3. Paste the initial continuation token found in the Payload or URL of the Request
INITIAL_CONTINUATION = ""
# 4. Paste your API_KEY from the Request URL (looks like "...?key=AIza...")
API_KEY = ""

def get_chat_messages(continuation):
    url = f"https://www.youtube.com/youtubei/v1/live_chat/get_live_chat_replay?key={API_KEY}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        "Cookie": COOKIE_STRING,
        "Authorization": AUTH_HEADER,
        "Content-Type": "application/json",
        "X-Youtube-Client-Name": "1",
        "X-Youtube-Client-Version": "2.20260508.01.00",
        "Origin": "https://www.youtube.com",
    }
    
    # Minimal payload - YouTube ignores the tracking stuff, it just needs clientName and clientVersion
    payload = {
        "context": {
            "client": {
                "clientName": "WEB",
                "clientVersion": "2.20260508.01.00"
            }
        },
        "continuation": continuation
    }

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))
# Main loop
continuation = INITIAL_CONTINUATION
superchats_found = []
count = 0
with open('superchats.txt', 'w', encoding='utf-8') as f:
    pass

while continuation:
    print(f"Fetching continuation: {continuation[:10]}...")
    try:
        response_data = get_chat_messages(continuation)
        
        # Parse actions
        actions = response_data.get('continuationContents', {}).get('liveChatContinuation', {}).get('actions', [])
        for action in actions:
            # Check for AddChatItemAction
            item = action.get('replayChatItemAction', {}).get('actions', [{}])[0].get('addChatItemAction', {}).get('item', {})
            
            renderer = item.get('liveChatPaidMessageRenderer') or item.get('liveChatPaidStickerRenderer')
            if renderer:
                time_text = renderer.get('timestampText', {}).get('simpleText', '0:00')
                author = renderer.get('authorName', {}).get('simpleText', 'Unknown')
                
                # Extract message text from runs
                message = ""
                if 'message' in renderer and 'runs' in renderer['message']:
                    message = "".join(run.get('text', '') for run in renderer['message']['runs'])
                elif 'liveChatPaidStickerRenderer' in item:
                    message = "[STICKER]"
                
                log_line = f"[{time_text}] {author}: {message}\n"
                
                # Append immediately to the log file
                with open('superchats.txt', 'a', encoding='utf-8') as f:
                    f.write(log_line)
                    
                print(f"Logged: {log_line.strip()}")
                count += 1
        
        # Get next continuation token
        continuations = response_data.get('continuationContents', {}).get('liveChatContinuation', {}).get('continuations', [])
        if not continuations:
            break
            
        continuation = continuations[0].get('liveChatReplayContinuationData', {}).get('continuation')
        time.sleep(1) # Prevent rate limiting
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        print(f"YouTube Error Body: {e.read().decode('utf-8')}")
        break
    except Exception as e:
        print(f"Error: {e}")
        break

print(f"\nTotal Superchats found: {count}")