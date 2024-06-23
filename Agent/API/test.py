import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from agent import app, getHardwareInfo, verifyOTP
import subprocess


class TestFastAPIApp(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_status_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "online"})

    def test_status_endpoint_method_not_allowed(self):
        response = self.client.post("/")
        self.assertEqual(response.status_code, 405)

    @patch("shutil.which")
    @patch("subprocess.run")
    def test_getHardwareInfo_with_nvidia_and_cuda(self, mock_run, mock_which):
        mock_which.return_value = "/path/to/nvidia-smi"
        mock_run.return_value.stdout = "NVIDIA-SMI\nrelease"
        self.assertTrue(getHardwareInfo())

    @patch("shutil.which")
    def test_getHardwareInfo_without_nvidia(self, mock_which):
        mock_which.return_value = None
        self.assertFalse(getHardwareInfo())

    @patch("shutil.which")
    @patch("subprocess.run")
    def test_getHardwareInfo_with_nvidia_without_cuda(self, mock_run, mock_which):
        mock_which.side_effect = ["/path/to/nvidia-smi", None]
        mock_run.return_value.stdout = "NVIDIA-SMI"
        self.assertFalse(getHardwareInfo())

    @patch("shutil.which")
    @patch("subprocess.run")
    def test_getHardwareInfo_subprocess_error(self, mock_run, mock_which):
        mock_which.return_value = "/path/to/nvidia-smi"
        mock_run.side_effect = subprocess.CalledProcessError(1, "nvidia-smi")
        self.assertFalse(getHardwareInfo())

    @patch("shutil.which")
    @patch("subprocess.run")
    def test_getHardwareInfo_nvidia_smi_unexpected_result(self, mock_run, mock_which):
        mock_which.return_value = "/path/to/nvidia-smi"
        mock_run.return_value.stdout = "Unexpected result"
        self.assertFalse(getHardwareInfo())

    @patch("shutil.which")
    @patch("subprocess.run")
    def test_getHardwareInfo_nvcc_unexpected_result(self, mock_run, mock_which):
        mock_which.side_effect = ["/path/to/nvidia-smi", "/path/to/nvcc"]
        mock_run.side_effect = [
            subprocess.CompletedProcess(
                args=["nvidia-smi"], returncode=0, stdout="NVIDIA-SMI"
            ),
            subprocess.CompletedProcess(
                args=["nvcc", "--version"], returncode=0, stdout="Unexpected result"
            ),
        ]
        self.assertFalse(getHardwareInfo())

    def test_verifyOTP_valid(self):
        self.assertTrue(verifyOTP("1234"))

    def test_verifyOTP_invalid(self):
        self.assertTrue(verifyOTP("4321"))

    def test_verifyOTP_empty(self):
        self.assertTrue(verifyOTP(""))

    def test_verifyOTP_non_numeric(self):
        self.assertTrue(verifyOTP("abcd"))

    @patch("agent.getHardwareInfo")
    def test_process_endpoint_success(self, mock_getHardwareInfo):
        mock_getHardwareInfo.return_value = True
        response = self.client.post(
            "/process/", json={"uid": "123", "mid": "456", "token": "789"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Success"})

    @patch("agent.getHardwareInfo")
    def test_process_endpoint_failure(self, mock_getHardwareInfo):
        mock_getHardwareInfo.return_value = False
        response = self.client.post(
            "/process/", json={"uid": "123", "mid": "456", "token": "789"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.json(), {"message": "Success"})

    def test_process_endpoint_invalid_request(self):
        response = self.client.post("/process/", json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "Invalid request"})

    def test_process_endpoint_missing_fields(self):
        response = self.client.post("/process/", json={"uid": "123"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "Invalid request"})


if __name__ == "__main__":
    unittest.main()
