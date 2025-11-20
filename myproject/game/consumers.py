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
        # so that rematches dont time out
        await r.expire(f"game:{self.lobby_code}:config", 630)

    async def game_start(self, message):
        # send parameters to multi_game.html
        parameters = await r.hgetall(self.redis_game_key)

        payload = {
            "type": "game_config",
            "addition_left_min": parameters["addition_left_min"],
            "addition_left_max": parameters["addition_left_max"],
            "addition_right_min": parameters["addition_right_min"],
            "addition_right_max": parameters["addition_right_max"],

            "multiplication_left_min": parameters["multiplication_left_min"],
            "multiplication_left_max": parameters["multiplication_left_max"],
            "multiplication_right_min": parameters["multiplication_right_min"],
            "multiplication_right_max": parameters["multiplication_right_max"],

            "duration": parameters["duration"],

            "allowed_operations": parameters["allowed_operations"],

            "player_role": self.player_role
        }
        await r.expire(f"game:{self.lobby_code}:config", 630)
        await self.send(text_data=json.dumps(payload))



    # called when the user disconnects from the page (closes it, timer runs out, etc)
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_code, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # this is isolated to the user whos frontend send the data back
        if text_data_json["type"] == "score_update":
            curr_score_a = await r.hget(self.redis_game_key, "score_A")
            curr_score_b = await r.hget(self.redis_game_key, "score_B")
            if self.player_role == "A":
                if text_data_json["status"] == "correct":
                    curr_score_a = int(curr_score_a or 0) + 1
                elif text_data_json["status"] == "reset":
                    curr_score_a = 0
                await r.hset(self.redis_game_key, 'score_A', curr_score_a)
            else:
                if text_data_json["status"] == "correct":
                    curr_score_b = int(curr_score_b or 0) + 1
                elif text_data_json["status"] == "reset":
                    curr_score_b = 0
                await r.hset(self.redis_game_key, 'score_B', curr_score_b)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_code, 
                {
                    "type": "score.update", 
                    "score_a": curr_score_a,
                    "score_b": curr_score_b
                }
            )

        elif text_data_json["type"] == "game_end":
            curr_score_a = await r.hget(self.redis_game_key, "score_A")
            curr_score_b = await r.hget(self.redis_game_key, "score_B")
            if curr_score_a > curr_score_b:
                print(f"CURR SCORE A {curr_score_a}")
                print(f"CURR SCORE B {curr_score_b}")
                winner = "player_A_channel"
            elif curr_score_b > curr_score_a:
                winner = "player_B_channel"
            else:
                winner = "tie"

            await self.channel_layer.group_send(
                self.room_group_code, 
                {
                    "type": "game.end", 
                    "score_a": curr_score_a,
                    "score_b": curr_score_b,
                    "winner": winner
                }
            )

        elif text_data_json["type"] == "rematch_request":
            await r.hset(self.redis_game_key, 'score_A', 0)
            await r.hset(self.redis_game_key, 'score_B', 0)

            await self.channel_layer.group_send(
                self.room_group_code,
                {
                    "type": "score.update",
                    "score_a": 0,
                    "score_b": 0
                }
            )

            await self.channel_layer.group_send(
                self.room_group_code,
                {
                    'type': 'game.start',
                    'message': 'active'
                }
            )


    async def score_update(self, message):
        score_a = message["score_a"]
        score_b = message["score_b"]
        await self.send(text_data=json.dumps({"type": "score_update", "score_a": score_a, "score_b": score_b}))

    async def game_end(self, message):
        score_a = message["score_a"]
        score_b = message["score_b"]
        winner = message["winner"]
        await self.send(text_data=json.dumps({"type": "game_end", "score_a": score_a, "score_b": score_b, "winner": winner}))

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))