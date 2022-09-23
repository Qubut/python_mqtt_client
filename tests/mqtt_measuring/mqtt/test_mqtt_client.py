from paho.mqtt.client import Client
from src.mqtt_measuring.mqtt_client import MqttClient
import pytest
import asyncio


class TestMqttClient():


    @pytest.fixture()
    def client() -> MqttClient:
        cl = MqttClient()
        cl.connect()
        return cl
    
    
    def test_client_connects(self, client):
        assert client.is_connected() == True
