import pytest
import json
import mock
import requests_mock
import api_wrapper
import common

invalid_json = {
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


valid_json = {
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


@mock.patch("common.sleep")
@mock.patch("time.sleep", return_value=None)
def test_valid(mock_common_sleep, mock_time_sleep):
    with requests_mock.Mocker() as mocker:
        zip = 49049
        timestamp = 1620505010
        url = f'https://www.impfportal-niedersachsen.de/portal/rest/appointments/findVaccinationCenterListFree/{zip}?stiko=&count=1&birthdate={timestamp*1000}'

        mocker.get(
            url,
            json=valid_json

        )

        print(url)
        result = api_wrapper.fetch_api(
            plz=zip,
            birthdate_timestamp=timestamp,
            max_retries=0,
        )

        a, b = json.dumps(result, sort_keys=True), json.dumps(
            valid_json["resultList"], sort_keys=True)
        assert a == b


@mock.patch("common.sleep")
@mock.patch("time.sleep", return_value=None)
def test_shadowban(mock_common_sleep, mock_time_sleep):
    with requests_mock.Mocker() as mocker:
        zip = 49049
        timestamp = 1620505010000

        mocker.get(
            f'https://www.impfportal-niedersachsen.de/portal/rest/appointments/findVaccinationCenterListFree/{zip}?stiko=&count=1&birthdate={timestamp}',
            json=None

        )

        with pytest.raises(Exception):
            api_wrapper.fetch_api(
                plz=zip,
                birthdate_timestamp=timestamp,
                max_retries=1,
                sleep_after_error=0,
                sleep_after_shadowban=1
            )
            common.sleep.assert_called_once_with(0, 0)
            common.sleep.assert_called_once_with(100, 0)
