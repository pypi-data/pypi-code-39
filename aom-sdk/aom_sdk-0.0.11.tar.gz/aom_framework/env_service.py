from aom_framework.services_pb2_grpc import EnvironmentServicer as Servicer
from aom_framework.protocols_pb2 import (
    EnvStartRequest, EnvStartReply, EnvUpdateRequest, EnvUpdateReply, RewardEvent)
from aom_framework.utils import list_versions

from google.protobuf.timestamp_pb2 import Timestamp

MACHINE_AGENT_ID = 0
HUMAN_AGENT_ID = 1


class Rewarder:
    def __init__(self):
        self.rewards = [[], []]

    def send_reward(self, agent_id, reward_value, reward_confidence, user_data):
        self.rewards[agent_id].append((reward_value, reward_confidence, user_data))


# Implementation of the AoM environment service.
class EnvService(Servicer):
    def __init__(self, env_class, types):
        # We will be managing a pool of environments, keyed by their session id.
        self._envs = {}
        self._env_class = env_class
        self._env_start_pb = types.env_config
        self._user_input_pb = types.human_action
        self._agent_input_pb = types.agent_action
        self._rewarder = Rewarder()

        print("Environment service started")

    # The orchestrator is requesting a new environment
    def Start(self, request, context):
        # The orchestrator will force a session id on to us, but for testing,
        # it's convenient to be able to create a unique one on demand.

        sess_id = ''
        if request.session_id != '':
            sess_id = request.session_id
        else:
            sess_id = str(uuid.uuid1())
            print("Start: Requestor did not provide a session id, creating one...")

        # Sanity check: We should only ever create a session once.
        if sess_id in self._envs:
            raise Exception("session already exists")

        print(f"spinning up new environment: {sess_id}")

        cfg = self._env_start_pb()
        cfg.ParseFromString(request.user_request.content)

        # Instantiate the fresh environment
        env = self._env_class(cfg, self._rewarder)
        self._envs[sess_id] = env

        # Send the initial state of the environment back to the client (orchestrator, normally.)
        reply = EnvStartReply(session_id=sess_id)
        reply.initial_sim_state.tick_id = 0
        reply.initial_sim_state.time_stamp.GetCurrentTime()
        reply.initial_sim_state.content = env.game_state.SerializeToString()

        return reply

    # The orchestrator is ready for the environemnt to move forward in time.
    def Update(self, request, context):
        sess_id = request.session_id

        if sess_id not in self._envs:
            raise Exception("session does not exists")

        # Retrieve the environment that matches this session
        env = self._envs[sess_id]

        # Extract the Puzzle-teach specific data from the AoM-generic structures
        user_data = self._user_input_pb()
        agent_data = self._agent_input_pb()

        # This is fine for puzzleteach since there is ALWAYS one user and one agent connected.
        user_data.ParseFromString(request.user_data[0].content)
        agent_data.ParseFromString(request.agent_data[0].content)

        # Advance time
        delta = env.update(user_data, agent_data)

        # Send the delta back to the orchestrator.
        reply = EnvUpdateReply()
        reply.delta.content = delta.SerializeToString()

        reply.delta.time_stamp.GetCurrentTime()

        for i in range(2):
            for machine_reward in self._rewarder.rewards[i]:
                re = RewardEvent(
                    agent_id=i,
                    tick_id=0,
                    reward_value=machine_reward[0],
                    reward_confidence=machine_reward[1])

                if machine_reward[2] is not None:
                    re.content = machine_reward[2].SerializeToString()
                reply.rewards.extend([re])

        self._rewarder.rewards = [[], []]

        return reply

    def Version(self, request, context):
        return list_versions(self._env_class)
