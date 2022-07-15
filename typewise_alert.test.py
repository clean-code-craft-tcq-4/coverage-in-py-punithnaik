import unittest
import typewise_alert
from unittest.mock import patch 


class TypewiseTest(unittest.TestCase):
  def test_infers_breach_as_per_limits(self):
    self.assertTrue(typewise_alert.infer_breach(20, 50, 100) == 'TOO_LOW')
    self.assertTrue(typewise_alert.infer_breach(101, 50, 100) == 'TOO_HIGH')
    self.assertTrue(typewise_alert.infer_breach(51, 50, 100) == 'NORMAL')

  def test_classify_temperature_breach(self):
    self.assertTrue(typewise_alert.classify_temperature_breach('PASSIVE_COOLING', -1) == 'TOO_LOW')
    self.assertTrue(typewise_alert.classify_temperature_breach('HI_ACTIVE_COOLING', 46) == 'TOO_HIGH')
    self.assertTrue(typewise_alert.classify_temperature_breach('MED_ACTIVE_COOLING', 1) == 'NORMAL')

  #Mocking the functions send_to_controller() and send_to_email() for unit testing purpose
  @patch('typewise_alert.send_to_controller')
  @patch('typewise_alert.send_to_email')
  def test_check_and_alert(self,mock_send_to_email,mock_send_to_controller):
    batteryChar = {'coolingType':''}
    typewise_alert.check_and_alert('TO_CONTROLLER', batteryChar,0)
    mock_send_to_controller.assert_called_once()
    typewise_alert.check_and_alert('TO_EMAIL', batteryChar,0)
    mock_send_to_email.assert_called_once()
    
if __name__ == '__main__':
  unittest.main()
