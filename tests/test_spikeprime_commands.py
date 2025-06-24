import unittest
from unittest.mock import Mock, patch, AsyncMock
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'spikeprime', 'src'))

from primeCommands import Prime

class TestPrimeCommands(unittest.TestCase):
    
    @patch('primeCommands.BLEConnection')
    def setUp(self, mock_ble):
        self.mock_ble = mock_ble
        self.prime = Prime("TEST_HUB")
    
    def test_initialization(self):
        self.assertEqual(self.prime.hub_name, "TEST_HUB")
        self.assertIsNotNone(self.prime.connection)
    
    @patch('primeCommands.BLEConnection')
    def test_move_forward_command_format(self, mock_ble):
        mock_connection = Mock()
        mock_ble.return_value = mock_connection
        
        prime = Prime("TEST_HUB")
        prime.moveForward(100)
        
        # Verify command was sent (exact format depends on implementation)
        mock_connection.send_command.assert_called()
    
    def test_command_validation(self):
        # Test that invalid distances are handled
        with self.assertRaises((ValueError, TypeError)):
            self.prime.moveForward(-10)  # Negative distance
        
        with self.assertRaises((ValueError, TypeError)):
            self.prime.moveForward("invalid")  # Non-numeric input

if __name__ == '__main__':
    unittest.main()