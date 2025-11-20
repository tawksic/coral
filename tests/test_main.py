from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

client = TestClient(app)


class TestHealthEndpoints:

    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}

    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"message": "OK"}

    def test_version_endpoint(self):
        response = client.get("/version")
        assert response.status_code == 200
        data = response.json()
        assert "release_version" in data
        assert data["release_version"] == "0.1.0"


class TestContainerEndpoints:

    @patch('app.services.container_metrics.get_container_stats')
    def test_container_cpu_success(self, mock_get_stats):
        mock_stats = {
            "cpu_stats": {
                "cpu_usage": {
                    "total_usage": 1_500_000_000  # 1.5 seconds in nanoseconds
                }
            }
        }
        mock_get_stats.return_value = mock_stats

        response = client.get("/container/cpu")
        assert response.status_code == 200
        data = response.json()
        assert "cpu_usage" in data
        assert data["cpu_usage"]["total_usage_seconds"] == 1.5

    @patch('app.services.container_metrics.get_container_stats')
    def test_container_cpu_no_stats(self, mock_get_stats):
        mock_get_stats.return_value = None

        response = client.get("/container/cpu")
        assert response.status_code == 200
        data = response.json()
        assert data["cpu_usage"] is None

    @patch('app.services.container_metrics.get_container_stats')
    def test_container_memory_success(self, mock_get_stats):
        mock_stats = {
            "memory_stats": {
                "usage": 50 * 1024 * 1024,  # 50 MiB in bytes
                "limit": 100 * 1024 * 1024   # 100 MiB in bytes
            }
        }
        mock_get_stats.return_value = mock_stats

        response = client.get("/container/memory")
        assert response.status_code == 200
        data = response.json()
        assert "memory_usage" in data
        memory_data = data["memory_usage"]
        assert memory_data["usage_mib"] == 50.0
        assert memory_data["limit_mib"] == 100.0
        assert memory_data["percentage"] == 50.0

    @patch('app.services.container_metrics.get_container_stats')
    def test_container_memory_no_stats(self, mock_get_stats):
        mock_get_stats.return_value = None

        response = client.get("/container/memory")
        assert response.status_code == 200
        data = response.json()
        assert data["memory_usage"] is None


class TestSimulationEndpoints:

    @patch('app.api.routes.simulation.simulate_traffic')
    def test_simulation_success(self, mock_simulate):
        mock_simulate.return_value = 5

        response = client.get("/simulate/?duration=10&delay=2")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "done"
        assert data["requests_sent"] == 5

    def test_simulation_validation_duration_too_high(self):
        response = client.get("/simulate/?duration=31&delay=1")
        assert response.status_code == 422  # Validation error

    def test_simulation_validation_duration_too_low(self):
        response = client.get("/simulate/?duration=0&delay=1")
        assert response.status_code == 422  # Validation error

    def test_simulation_validation_delay_too_high(self):
        response = client.get("/simulate/?duration=10&delay=31")
        assert response.status_code == 422  # Validation error

    def test_simulation_validation_delay_too_low(self):
        response = client.get("/simulate/?duration=10&delay=0")
        assert response.status_code == 422  # Validation error

    @patch('app.api.routes.simulation.simulate_traffic')
    def test_simulation_default_parameters(self, mock_simulate):
        mock_simulate.return_value = 3
        response = client.get("/simulate/?duration=1&delay=1")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "done"
        assert data["requests_sent"] == 3

