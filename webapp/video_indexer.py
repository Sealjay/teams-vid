from asyncio.tasks import sleep
import os
import aiohttp
import asyncio
import json
from dotenv import load_dotenv

load_dotenv()


class AsyncVideoIndexer:
    @classmethod
    async def create(
        cls, account_id, subscription_key, location, get_access_token=True
    ):
        self = AsyncVideoIndexer()
        self.account_id = account_id
        self.subscription_key = subscription_key
        self.location = location
        self.access_token = None
        self.session = aiohttp.ClientSession()
        if get_access_token:
            await self.get_access_token()
        return self

    async def get_access_token(self):
        self.access_token = None
        print("Rotating token for Video Indexer.")
        params = {"allowEdit": "true"}
        async with await self.video_indexer_request(
            "AccessToken", "get", operation_prefix="Auth/", params=params
        ) as response:
            self.access_token = await response.json()
        asyncio.create_task(self.wait_to_rotate_token())

    async def wait_to_rotate_token(self):
        await asyncio.sleep(3540)  # renew_token_every_hour, give or take
        await self.get_access_token()

    async def get_video_access_token(self, video_id):
        response = await self.video_indexer_request(
            f"Videos/{video_id}/AccessToken", "get", operation_prefix="Auth/"
        )
        return response

    async def upload_video_from_url(
        self, video_name, video_external_id, callback_url, video_url
    ):
        params = {
            "name": video_name,
            "externalId": video_external_id,
            "callbackUrl": callback_url,
            "videoUrl": video_url,
        }
        response = await self.video_indexer_request(f"Videos", "post", params=params)
        return response

    async def list_videos(self):
        response = await self.video_indexer_request(f"Videos", "get")
        return response

    async def get_thumbnail(self, video_id, thumbnail_id):
        params = {
            "videoId": video_id,
            "thumbnailId": thumbnail_id,
        }
        response = await self.video_indexer_request(
            f"Videos/{video_id}/Thumbnails/{thumbnail_id}", "get", params=params
        )
        return response

    async def get_video_index(self, video_id):
        params = {
            "videoId": video_id,
        }
        print(video_id)
        response = await self.video_indexer_request(
            f"Videos/{video_id}/Index", "get", params=params
        )
        return response

    async def get_video_id_by_external_id(self, external_id):
        params = {
            "externalId": external_id,
        }
        response = await self.video_indexer_request(
            f"Videos/GetIdByExternalId", "get", params=params
        )
        return response

    async def get_video_player_widget(self, video_id, headers=None):
        response = await self.video_indexer_request(
            f"Videos/{video_id}/PlayerWidget", "get", headers=headers
        )
        return response

    async def video_indexer_request(
        self, api_resource, operation, params=None, headers=None, operation_prefix=""
    ):
        operations = {"get": self.session.get, "post": self.session.post}
        assert operation in operations
        operation = operations[operation]
        if params is None:
            params = {}
        if headers is None:
            headers = {}
        if self.access_token is not None:
            if "Authorization" not in headers:
                headers["Authorization"] = f"Bearer {self.access_token}"
        headers["Ocp-Apim-Subscription-Key"] = self.subscription_key
        api_endpoint = (
            f"https://api.videoindexer.ai/{operation_prefix}{self.location}/"
            + f"Accounts/{self.account_id}/"
            + api_resource
        )
        return operation(api_endpoint, params=params, headers=headers)


async def main():
    video_indexer = await AsyncVideoIndexer.create(
        os.environ.get("VIDEO_INDEXER_ACCOUNT_ID"),
        os.environ.get("VIDEO_INDEXER_KEY"),
        os.environ.get("VIDEO_INDEXER_ACCOUNT_LOCATION"),
    )

    video_to_upload = (
        "https://teamsvid011.blob.core.windows.net/videostoprocess/"
        + "204a9799-de7d-435f-90e0-40fcf116c5c0.mov?sv=2019-12-12&st="
        + "2021-01-11T01%3A17%3A00Z&se=2021-04-12T00%3A17%3A00Z&sr=b"
        + "&sp=r&sig=bpQ4sP4GqFKcZaSslR8mPmeLVlGpr2J9FPOfou8M8B4%3D"
    )
    # async with await video_indexer.upload_video_from_url(
    #    "test video", "apple", "https://google.com", video_to_upload
    # ) as response:
    #    video_details = await response.json()
    async with await video_indexer.get_video_id_by_external_id("apple") as response:
        video_id = await response.json()
    async with await video_indexer.get_video_index(video_id) as response:
        video_details = await response.json()
        print(video_details["state"])
        print(json.dumps(video_details))
        thumbnail_id = video_details["videos"][0]["thumbnailId"]
    async with await video_indexer.get_thumbnail(video_id, thumbnail_id) as response:
        video_details = await response.json()
        print(video_details)
        # print(video_details["state"])

    if False:
        async with await video_indexer.get_video_index("5f029373e3") as response:
            video_details = await response.json()
        async with await video_indexer.get_video_access_token("5f029373e3") as response:
            video_access_token = await response.json()
        print(video_access_token)
        headers = {"Authorization": f"Bearer {video_access_token}"}
        async with await video_indexer.get_video_player_widget(
            video_details["id"], headers=headers
        ) as response:
            video_details = await response.text()
        print(video_details)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())