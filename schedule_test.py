import unittest
from schedule import *

class TestScheduler(unittest.TestCase):
    
    def test_simple(self):
        busyBlocks = [[TimeBlock(1, 3), TimeBlock(5, 6)]]
        start = 0
        end = 6
        minDuration = 2
        self.assertEqual(scheduleEvent(busyBlocks, start, end, minDuration), 3)

    def test_earliest_time(self):
        busyBlocks = [[TimeBlock(1, 3), TimeBlock(5, 6)], [TimeBlock(1, 7)]]
        start = 0
        end = 6
        minDuration = 1
        self.assertEqual(scheduleEvent(busyBlocks, start, end, minDuration), 0)
    
    def test_last_time(self):
        busyBlocks = [[TimeBlock(0, 2)], [TimeBlock(0, 5)]]
        start = 0
        end = 6
        minDuration = 1
        self.assertEqual(scheduleEvent(busyBlocks, start, end, minDuration), 5)

    def test_failure(self):
        busyBlocks = [[TimeBlock(0, 2), TimeBlock(3, 5)], [TimeBlock(7, 10)]]
        start = 0
        end = 10
        minDuration = 5
        self.assertIsNone(scheduleEvent(busyBlocks, start, end, minDuration))
 
    def test_unordered(self):
        busyBlocks = [[TimeBlock(5, 8), TimeBlock(0, 1)], [TimeBlock(7, 8), TimeBlock(1, 4)]]
        start = 0
        end = 8
        minDuration = 1
        self.assertEqual(scheduleEvent(busyBlocks, start, end, minDuration), 4)

    def test_many_schedules(self):
        busyBlocks = [[TimeBlock(1, 3), TimeBlock(5, 6)], [TimeBlock(0, 1), TimeBlock(4, 7)], [TimeBlock(0, 2), TimeBlock(5, 8)], [TimeBlock(6, 7)]]
        start = 0
        end = 8
        minDuration = 1
        self.assertEqual(scheduleEvent(busyBlocks, start, end, minDuration), 3)


if __name__ == '__main__':
    unittest.main()
