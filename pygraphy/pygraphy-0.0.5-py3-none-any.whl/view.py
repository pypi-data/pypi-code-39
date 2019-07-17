import asyncio
import pathlib
from starlette import status
from starlette.endpoints import HTTPEndpoint, WebSocketEndpoint
from starlette.responses import PlainTextResponse, HTMLResponse, Response
from .introspection import WithMetaSchema


def get_playground_html(request_path: str) -> str:
    here = pathlib.Path(__file__).parents[0]
    path = here / "static/playground.html"

    with open(path) as f:
        template = f.read()

    return template.replace("{{REQUEST_PATH}}", request_path)


class Schema(HTTPEndpoint, WithMetaSchema):

    async def get(self, request):
        html = get_playground_html(str(request.url))
        return HTMLResponse(html)

    async def post(self, request):
        content_type = request.headers.get("Content-Type", "")

        if "application/json" in content_type:
            data = await request.json()
        elif "application/graphql" in content_type:
            body = await request.body()
            text = body.decode()
            data = {"query": text}
        elif "query" in request.query_params:
            data = request.query_params
        else:
            return PlainTextResponse(
                "Unsupported Media Type",
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )

        try:
            query = data["query"]
            variables = data.get("variables")
        except KeyError:
            return PlainTextResponse(
                "No GraphQL query found in the request",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        result, success = await self.execute(
            query, variables=variables, request=request
        )
        status_code = status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
        return Response(
            result,
            status_code=status_code,
            media_type='application/json'
        )


class SubscribableSchema(WebSocketEndpoint, WithMetaSchema):
    encoding = 'json'

    async def on_connect(self, websocket):
        self.task = None
        await websocket.accept()

    async def on_receive(self, websocket, data):
        try:
            query = data["query"]
            variables = data.get("variables")
        except KeyError:
            return await websocket.send_text(
                "No GraphQL query found in the request"
            )
        self.task = asyncio.ensure_future(
            self.execute(
                query,
                variables=variables,
                request=websocket,
                subscribable=True
            )
        )
        try:
            await self.task
        except asyncio.CancelledError:
            return

    async def on_disconnect(self, websocket, close_code):
        if self.task:
            self.task.cancel()
