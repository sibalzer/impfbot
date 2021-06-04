from datetime import datetime
import unittest.mock as mock
import requests_mock

import impfbot
import common
import settings

in_stock = {
    "resultList": [
        {
            "vaccinationCenterPk": 12345678901234,
            "name": "IZ Test-Impfbot",
            "streetName": "Rainbow Road",
            "streetNumber": "42",
            "zipcode": "49000",
            "city": "Toadcity",
            "scheduleSaturday": True,
            "scheduleSunday": True,
            "vaccinationCenterType": 0,
            "vaccineName": "AstraZeneca",
            "vaccineType": "Vector",
            "interval1to2": 84,
            "offsetStart2Appointment": 0,
            "offsetEnd2Appointment": 5,
            "distance": 5,
            "outOfStock": False,
            "firstAppoinmentDateSorterOnline": 1622412000000,
            "freeSlotSizeOnline": 253,
            "maxFreeSlotPerDay": 24,
            "publicAppointment": True
        }
    ],
    "succeeded": True
}


out_of_stock = {
    "resultList": [
        {
            "vaccinationCenterPk": 12345678901234,
            "name": "IZ Test-Impfbot",
            "streetName": "Rainbow Road",
            "streetNumber": "42",
            "zipcode": "49000",
            "city": "Toadcity",
            "scheduleSaturday": True,
            "scheduleSunday": True,
            "vaccinationCenterType": 0,
            "vaccineName": "AstraZeneca",
            "vaccineType": "Vector",
            "interval1to2": 84,
            "offsetStart2Appointment": 0,
            "offsetEnd2Appointment": 5,
            "distance": 10,
            "outOfStock": True,
            "publicAppointment": True
        }
    ],
    "succeeded": True
}

empty = {
    "resultList": [],
    "succeeded": True
}

settings.load("tests/configs/test-config.ini")
zip = settings.ZIP
api_url = f'https://www.impfportal-niedersachsen.de/portal/rest/appointments/findVaccinationCenterListFree/{zip}?stiko=&count=1'

error_none = None


@mock.patch('impfbot.sleep', return_value=None)
@mock.patch('impfbot.alert', return_value=None)
@mock.patch('logging.Logger.error')
@mock.patch('logging.Logger.warning')
@mock.patch('logging.Logger.info')
def test_check_for_slot_in_stock(log_info_mock, log_warning_mock, log_error_mock, alert_mock, sleep_mock):
    settings.load("tests/configs/test-config.ini")
    with requests_mock.Mocker() as mocker:
        mocker.get(
            url=api_url,
            json=in_stock

        )
        impfbot.check_for_slot()

    alert_mock.assert_called_once_with(
        "Freier Impfslot (253)! AstraZeneca/Vector")
    log_info_mock.assert_called_once_with(
        "Free slot! (253) AstraZeneca/Vector")
    log_warning_mock.assert_not_called()
    log_error_mock.assert_not_called()

    sleep_mock.assert_called_once_with(settings.COOLDOWN_AFTER_FOUND_IN_MIN)


@mock.patch('impfbot.sleep', return_value=None)
@mock.patch('logging.Logger.error')
@mock.patch('logging.Logger.warning')
@mock.patch('logging.Logger.info')
def test_check_for_slot_out_of_stock(log_info_mock, log_warning_mock, log_error_mock, sleep_mock):
    settings.load("tests/configs/test-config.ini")
    with requests_mock.Mocker() as mocker:
        mocker.get(
            url=api_url,
            json=out_of_stock
        )
        impfbot.check_for_slot()

    log_info_mock.assert_called_with('No free slot.')
    log_warning_mock.assert_not_called()
    log_error_mock.assert_not_called()


@mock.patch('api_wrapper.sleep', return_value=None)
@mock.patch('impfbot.sleep', return_value=None)
@mock.patch('logging.Logger.error')
@mock.patch('logging.Logger.warning')
@mock.patch('logging.Logger.info')
def test_check_for_slot_shadowban(log_info_mock, log_warning_mock, log_error_mock, sleep_mock, sleep_api_mock):
    settings.load("tests/configs/test-config.ini")
    with requests_mock.Mocker() as mocker:
        mocker.get(
            url=api_url,
            json=None
        )
        impfbot.check_for_slot()

    sleep_mock.assert_called_with(
        settings.SLEEP_AFTER_DETECTED_SHADOWBAN_IN_MIN)

    log_info_mock.assert_not_called()
    log_warning_mock.assert_not_called()
    log_error_mock.assert_called_with(
        f"Couldn't fetch api. (Shadowbanned IP?) Sleeping for {settings.SLEEP_AFTER_DETECTED_SHADOWBAN_IN_MIN/60}min")

# TODO
# @mock.patch('api_wrapper.sleep', return_value=None)
# @mock.patch('impfbot.sleep', return_value=None)
# @mock.patch('logging.Logger.error')
# @mock.patch('logging.Logger.warning')
# @mock.patch('logging.Logger.info')
# def test_check_for_slot_connection_lost(log_info_mock, log_warning_mock, log_error_mock, sleep_mock, sleep_api_mock):
#    settings.load("tests/configs/test-config.ini")
#    with requests_mock.Mocker() as mocker:
#        mocker.get(
#            url=api_url,
#            json=None
#        )
#        impfbot.check_for_slot()
#
#    sleep_mock.assert_called_with(
#        settings.SLEEP_BETWEEN_REQUESTS_IN_S, settings.JITTER)
#
#    log_info_mock.assert_not_called()
#    log_warning_mock.assert_not_called()
#    log_error_mock.assert_called_with(
#        f"Couldn't fetch api. (Connection lost) Sleeping for {settings.SLEEP_BETWEEN_REQUESTS_IN_S}s.")