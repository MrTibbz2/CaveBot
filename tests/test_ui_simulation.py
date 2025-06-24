import unittest
import math
from unittest.mock import Mock, patch
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'UI'))

from simulation import RobotSimulator

class TestRobotSimulator(unittest.TestCase):
    
    @patch('turtle.Screen')
    @patch('turtle.Turtle')
    def setUp(self, mock_turtle, mock_screen):
        self.simulator = RobotSimulator()
    
    def test_line_intersection_basic(self):
        # Test basic intersection
        p1, p2 = (0, 0), (10, 0)
        p3, p4 = (5, -5), (5, 5)
        result = self.simulator._line_segment_intersection(p1, p2, p3, p4)
        self.assertEqual(result, (5, 0))
    
    def test_line_intersection_no_collision(self):
        # Test no intersection
        p1, p2 = (0, 0), (10, 0)
        p3, p4 = (0, 5), (10, 5)
        result = self.simulator._line_segment_intersection(p1, p2, p3, p4)
        self.assertIsNone(result)
    
    def test_sensor_config_integrity(self):
        # Verify sensor configuration matches expected format
        expected_sensors = ["leftfront", "leftback", "rightfront", "rightback", 
                          "frontleft", "frontright", "backleft", "backright"]
        self.assertEqual(set(self.simulator.sensors_config.keys()), set(expected_sensors))
        
        for sensor_name, config in self.simulator.sensors_config.items():
            self.assertEqual(len(config), 3)  # x, y, angle
            self.assertIsInstance(config[0], (int, float))  # x coordinate
            self.assertIsInstance(config[1], (int, float))  # y coordinate
            self.assertIsInstance(config[2], (int, float))  # angle

if __name__ == '__main__':
    unittest.main()