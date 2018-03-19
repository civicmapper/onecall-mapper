import json
import requests
from .utils import Utils
from .logger import log


class Publish(Utils):

    def __init__(
        self,
        records,
        ESRI_APP_CLIENT_ID=None,
        ESRI_APP_CLIENT_SECRET=None,
        ESRI_APP_TOKEN_EXPIRATION=None,
        ESRI_AGOL_FEATURE_SERVICE_URL=None,
        ESRI_AGOL_TOKEN_URL="https://www.arcgis.com/sharing/oauth2/token"
    ):
        # data to be published
        log.info("CHECKING PUBLISHED FEATURE SERVICE...")
        self.records = self.list_of_seq_unique_by_key(records, "serial_number")

        # ESRI AGOL PROVIDER CREDENTIALS
        self.ESRI_APP_CLIENT_ID = ESRI_APP_CLIENT_ID
        self.ESRI_APP_CLIENT_SECRET = ESRI_APP_CLIENT_SECRET
        self.ESRI_APP_TOKEN_EXPIRATION = ESRI_APP_TOKEN_EXPIRATION
        self.ESRI_AGOL_FEATURE_SERVICE_URL = ESRI_AGOL_FEATURE_SERVICE_URL
        self.ESRI_AGOL_TOKEN_URL = ESRI_AGOL_TOKEN_URL

    def _get_esri_agol_token(self):
        """requests and returns an ArcGIS Token for the pre-registered application.
        Client id and secrets are managed through the ArcGIS Developer's console: https://developers.arcgis.com/
        """
        params = {
            'client_id': self.ESRI_APP_CLIENT_ID,
            'client_secret': self.ESRI_APP_CLIENT_SECRET,
            'grant_type': "client_credentials",
            'expiration': self.ESRI_APP_TOKEN_EXPIRATION
        }

        response = requests.get(
            self.ESRI_AGOL_TOKEN_URL,
            params=params
        )

        token = response.json()
        log.info("Token acquired: {0}".format(token))

        return token

    def _check_if_exists_in_esri_agol_feature_service(self, token):
        """compare new records against those in the existing service; return only those
        records not in existing service
        """
        published = requests.get(
            url="{0}/query".format(self.ESRI_AGOL_FEATURE_SERVICE_URL),
            params={
                "where": "1=1",
                "outFields": "SerialNumber",
                "returnGeometry": False,
                "f": "pjson",
                "token": token['access_token'],
            }
        )
        published = published.json()
        if "features" in published:
            to_publish = [
                # return each record
                r for r in self.records
                # but only if the id is not in
                if str(r["serial_number"]) not in list(set(
                    # this list of ids from the already published data:
                    [str(f["attributes"]["SerialNumber"])
                     for f in published["features"]]
                ))
            ]
            if to_publish:
                return to_publish
            else:
                return None
        else:
            return None

    def to_esri_agol_feature_service(
        self,
        ESRI_APP_CLIENT_ID=None,
        ESRI_APP_CLIENT_SECRET=None,
        ESRI_APP_TOKEN_EXPIRATION=None,
        ESRI_AGOL_FEATURE_SERVICE_URL=None,
        ESRI_AGOL_TOKEN_URL="https://www.arcgis.com/sharing/oauth2/token"
    ):
        # override connection params provided during class instantiation if desired
        self.ESRI_APP_CLIENT_ID = ESRI_APP_CLIENT_ID
        self.ESRI_APP_CLIENT_SECRET = ESRI_APP_CLIENT_SECRET
        self.ESRI_APP_TOKEN_EXPIRATION = ESRI_APP_TOKEN_EXPIRATION
        self.ESRI_AGOL_FEATURE_SERVICE_URL = ESRI_AGOL_FEATURE_SERVICE_URL
        self.ESRI_AGOL_TOKEN_URL = ESRI_AGOL_TOKEN_URL

        # get token for the service
        token = self._get_esri_agol_token()

        # query existing endpoint to make sure we don't publish duplicates.
        self.to_publish = self._check_if_exists_in_esri_agol_feature_service(
            token)
        if self.to_publish:
            log.info("Publishing {0} new One Call records to the feature service.".format(
                len(self.to_publish)))

            # construct request to add records
            payload = {
                'f': 'pjson',
                'token': token['access_token'],
                'features': '',
                'rollbackOnFailure': True
            }
            features = []
            for record in self.to_publish:
                # TODO: replace with dynamically generated schema, spec'd by a Transform class.
                features.append(
                    {
                        "geometry": {
                            "rings": record['coordinates'],
                            "spatialReference": {
                                "wkid": 4326
                            }
                        },
                        "attributes": {
                            "SerialNumber": int(record['serial_number']),
                            "MappedType": record['type']
                        }
                    }
                )
            payload['features'] = json.dumps(features)
            log.info(payload)
            response = requests.post(
                url="{0}/addFeatures".format(
                    self.ESRI_AGOL_FEATURE_SERVICE_URL),
                data=payload,
            )
            log.info(json.dumps(response.json(), indent=2))

            return response
        else:
            log.info("No new records to publish to the feature service.")
