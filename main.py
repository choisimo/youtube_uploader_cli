import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from twisted.conch.insults.insults import privateModes

# OAuth 2.0 인증
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
DEFAULT_CLIENT_SECRETS_FILE = "client_secret.json"  # 기본 클라이언트 파일 경로


def authenticate(client_secrets_file):
    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
    credentials = flow.run_local_server(port=0)  # 포트를 0으로 설정하면 사용 가능한 임의의 포트를 선택합니다.
    return build("youtube", "v3", credentials=credentials)

def upload_video(youtube, file, title, description, tags, category="22", status="unlisted"):
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category,
            },
            "status": {
                "privacyStatus": privacy_status,  # public, private, unlisted 중 선택
            },
        },
        media_body=MediaFileUpload(file, chunksize=-1, resumable=True)
    )
    response = request.execute()
    print(f"Video uploaded: https://www.youtube.com/watch?v={response['id']}")


def get_user_input(prompt, default):
    user_input = input(prompt)
    return user_input if user_input else default

def get_client_secrets_file():
    # 기본 경로 확인
    if os.path.exists(DEFAULT_CLIENT_SECRETS_FILE):
        return DEFAULT_CLIENT_SECRETS_FILE

    print("Default client_secret.json not found.")
    while True:
        client_secrets_file = input("Enter the full path to your client_secret.json file: ")
        if os.path.exists(client_secrets_file):
            return client_secrets_file
        else:
            print("File not found. Please try again.")


if __name__ == "__main__":
    client_secrets_file = get_client_secrets_file()
    youtube = authenticate(client_secrets_file)

    file = input("Enter the file path: ")
    if not os.path.isfile(file):
        print("File not found.")
        exit(1)

    title = get_user_input("Enter the video title: ", "Test Title")
    description = get_user_input("Enter the video description: ", "Test Description")
    tags = get_user_input("Enter the video tags: ", "tag1,tag2").split(",")
    category = get_user_input("Enter the category ID: ", "22")
    privacy_status = get_user_input("Enter the privacy status [private, public, unlisted]: ", "private")

    if privacy_status not in ["private", "public", "unlisted"]:
        print("Invalid privacy status.")
        privacy_status = "private"
        print("Privacy status set to private due to invalid input.")

    upload_video(
        youtube,
        file=file,
        title=title,
        description=description,
        tags=tags,
        category=category,
        status=privacy_status
    )

