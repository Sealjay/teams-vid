import os
import aiohttp
import asyncio
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
            self.access_token = await self.get_access_token()
            print(self.access_token)
        return self

    async def get_access_token(self):
        headers = {"Ocp-Apim-Subscription-Key": self.subscription_key}
        asyncio.create_task(
            asyncio.sleep(3600, self.get_access_token())
        )  # renew_token_every_hour
        response = await self.video_indexer_request(
            f"AccessToken", "get", headers=headers
        )
        return response

    async def upload_video(self):
        response = await self.video_indexer_request(f"Videos")
        return response

    async def get_thumbnail(self, video_id, thumbnail_id):
        response = await self.video_indexer_request(
            f"Videos/{video_id}/Thumbnails/{thumbnail_id}"
        )
        return response

    async def get_information(self, video_id):
        response = await self.video_indexer_request(f"Videos/{video_id}/Index")
        return response

    async def get_widget_code(self):
        pass

    async def video_indexer_request(
        self, api_resource, operation, params=None, headers=None
    ):
        operations = {"get": self.session.get, "post": self.session.post}
        assert operation in operations
        operation = operations[operation]
        if params is None:
            params = {}
        if headers is None:
            headers = {}
        api_endpoint = (
            f"https://api.videoindexer.ai/{self.location}/"
            + f"Accounts/{self.account_id}/"
        )
        async with operation(api_endpoint, params=params, headers=headers) as response:
            return response


async def main():
    video_indexer_request = await AsyncVideoIndexer.create(
        os.environ.get("VIDEO_INDEXER_ACCOUNT_ID"),
        os.environ.get("VIDEO_INDEXER_KEY"),
        os.environ.get("VIDEO_INDEXER_ACCOUNT_LOCATION"),
    )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())