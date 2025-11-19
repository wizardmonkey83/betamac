import json
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import redis.asyncio as aredis
from django.conf import settings


# connect to the redis db
try:
    r = aredis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
except:
    # quit life
    r = None

class GameConsumer(AsyncWebsocketConsumer):
    # is called automatically when the websocket connection is made on multi_game
    async def connect(self):
        self.lobby_code = self.scope["url_route"]["kwargs"]["lobby_code"]
        # channel layer group
        self.room_group_code = self.lobby_code
        # config is used to avoid future collisions with naming if features get added in the future
        self.redis_game_key = f"game:{self.lobby_code}:config"
        # this should be a redundant catch as the lobby is created in views
        lobby_exists = await r.exists(self.redis_game_key)

        if not lobby_exists:
            await self.close()
            return
        
        if await r.hget(self.redis_game_key, 'player_A_channel') is None:
            self.player_role = 'A'
            await r.hset(self.redis_game_key, 'player_A_channel', self.channel_name)
        elif await r.hget(self.redis_game_key, 'player_B_channel') is None:
            self.player_role = 'B'
            await r.hset(self.redis_game_key, 'player_B_channel', self.channel_name)
        else:
            # too many participants
            await self.close()
            return
        
        await self.accept()

        await self.channel_layer.group_add(self.room_group_code, self.channel_name)
        
        is_player_a_ready = await r.hget(self.redis_game_key, 'player_A_channel') is not None
        is_player_b_ready = await r.hget(self.redis_game_key, 'player_B_channel') is not None

        if is_player_a_ready and is_player_b_ready:
            await self.channel_layer.group_send(
                self.room_group_code,
                {
                    'type': 'game.start',
                    'message': 'active'
                }
            )

    async def game_start(self, message):
        # start game
        if message == 'active':
            # send parameters to multi_game.html
            await self.send(text_data=json.dumps({
                "addition_left_min": r.hmget(self.redis_game_key, 'addition_left_min'),
                "addition_left_max": r.hmget(self.redis_game_key, 'addition_left_max'),
                "addition_right_min": r.hmget(self.redis_game_key, 'addition_right_min'),
                "addition_right_max": r.hmget(self.redis_game_key, 'addition_right_max'),

                "multiplication_left_min": r.hmget(self.redis_game_key, 'multiplication_left_min'),
                "multiplication_left_max": r.hmget(self.redis_game_key, 'multiplication_left_max'),
                "multiplication_right_min": r.hmget(self.redis_game_key, 'multiplication_right_min'),
                "multiplication_right_max": r.hmget(self.redis_game_key, 'multiplication_right_max'),

                "duration": r.hmget(self.redis_game_key, 'duration_selector'),
                "distractions": r.hmget(self.redis_game_key, 'distractions_enabled'),

                "allowed_operations": r.hmget(self.redis_game_key, 'allowed_operations'),
            }))



    # called when the user disconnects from the page (closes it, timer runs out, etc)
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_code, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        score_a = text_data_json["score_a"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_code, {"type": "chat.message", "score_a": score_a}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))