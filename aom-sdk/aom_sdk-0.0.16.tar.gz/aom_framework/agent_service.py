from aom_framework.services_pb2_grpc import AgentServicer as Servicer

from aom_framework.protocols_pb2 import (
    AgentStartRequest, AgentStartReply, AgentDecideRequest,
    AgentDecideReply, AgentRewardRequest, AgentRewardReply)

from aom_framework.utils import list_versions

# Implementation of the AoM agent service.


class AgentService(Servicer):
    def __init__(self, agent_class, types):
        print("Agent Service started")
        # We will be managing a pool of agents, keyed by their session id.
        self._agents = {}
        self._agent_class = agent_class
        self._env_state_pb = types.env_state
        self._env_state_delta_pb = types.env_state_delta
        self._state_collapse_fn = types.state_collapse_fn

    # The orchestrator is requesting a new agent
    def Start(self, request, context):
        try:
            # The orchestrator will force a session id on to us, but for testing,
            # it's convenient to be able to create a unique one on demand.
            sess_id = request.session_id

            if not sess_id:
                raise Exception("No session ID provided")

            # Sanity check: We should only ever create a session once.
            if sess_id in self._agents:
                raise Exception("session already exists")

            # Instantiate the fresh agent
            agent = self._agent_class()
            self._agents[sess_id] = (agent, self._env_state_pb())

            # Send the initial state of the agent back to the client (orchestrator, normally.)
            reply = AgentStartReply()

            return reply
        except Exception as e:
            print(f'Start failure: {e}')
            raise

    # The orchestrator is ready for the environemnt to move forward in time.
    def Decide(self, request, context):
        try:
            sess_id = request.session_id

            if sess_id not in self._agents:
                raise Exception("session does not exists.")

            # Retrieve the agent that matches this session
            agent, state = self._agents[sess_id]

            if request.HasField('env_state'):
                state.ParseFromString(request.env_state.content)
            elif request.HasField('env_delta'):
                delta = self._env_state_delta_pb()
                delta.ParseFromString(request.env_delta.content)
                self._state_collapse_fn(state, delta)
            else:
                raise Exception("no env data.")

            decision = agent.decide_from_state(state)

            # Send the delta back to the orchestrator.
            reply = AgentDecideReply()
            reply.decision.content = decision.SerializeToString()

            return reply
        except Exception as e:
            print(f'Decide failure: {e}')
            raise

    def Reward(self, request, context):
        try:
            sess_id = request.session_id

            if sess_id not in self._agents:
                raise Exception("session does not exists.")

            # Retrieve the agent that matches this session
            agent, state = self._agents[sess_id]

            agent.reward(request.reward)

            reply = AgentRewardReply()

            return reply
        except Exception as e:
            print(f'Reward failure: {e}')
            raise

    def Version(self, request, context):
        try:
            return list_versions(self._agent_class)
        except Exception as e:
            print(f'Version failure: {e}')
            raise
