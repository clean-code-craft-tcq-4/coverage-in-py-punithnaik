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

  #Test with valid values of alertTarget
  #Mocking the functions send_to_controller() and send_to_email() for unit testing purpose
  @patch('typewise_alert.send_to_controller')
  @patch('typewise_alert.send_to_email')
  def test_check_and_alert_with_valid_value(self,mock_send_to_email,mock_send_to_controller):
    batteryChar = {'coolingType':''}
    typewise_alert.check_and_alert('TO_CONTROLLER', batteryChar,0)
    mock_send_to_controller.assert_called_once()
    typewise_alert.check_and_alert('TO_EMAIL', batteryChar,0)
    mock_send_to_email.assert_called_once()

  #Test with invalid value for alertTarget
  #Mocking the functions send_to_controller() and send_to_email() for unit testing purpose
  @patch('typewise_alert.send_to_controller')
  @patch('typewise_alert.send_to_email')
  def test_check_and_alert_with_invalid_value(self,mock_send_to_email,mock_send_to_controller): 
    batteryChar = {'coolingType':''}
    typewise_alert.check_and_alert('', batteryChar,0) #For else coverage
    mock_send_to_controller.assert_not_called()
    typewise_alert.check_and_alert('', batteryChar,0) #For else coverage
    mock_send_to_email.assert_not_called()

  #Mocking print function
  @patch('builtins.print')
  def test_send_to_controller(self,mock_print):
    typewise_alert.send_to_controller('TOO_LOW')
    mock_print.assert_called_with('65261, TOO_LOW')

  #Test with valid values of breachType
  #Mocking print function
  @patch('builtins.print')
  def test_send_to_email_with_valid_value(self,mock_print):
    typewise_alert.send_to_email('TOO_LOW')
    mock_print.assert_called_with('Hi, the temperature is too low')
    typewise_alert.send_to_email('TOO_HIGH')
    mock_print.assert_called_with('Hi, the temperature is too high')

  #Test with invalid value for breachType
  #Mocking print function
  @patch('builtins.print')
  def test_send_to_email_with_invalid_value(self,mock_print):
    typewise_alert.send_to_email('') #For else coverage
    mock_print.assert_not_called()
    
if __name__ == '__main__':
  unittest.main()
