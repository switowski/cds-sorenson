# -*- coding: utf-8 -*-
#
# This file is part of CERN Document Server.
# Copyright (C) 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""API to use Sorenson transcoding server."""

import json
import requests

from __future__ import absolute_import, print_function
from flask import current_app


# TODO: Make authentication better
# TODO: Move to config file
SORENSON_USERNAME = 'xxxxxx'  # for testing, use CERN NICE credentials
SORENSON_PASSWORD = 'xxxxxx'  # for testing, use CERN NICE credentials
SORENSON_AUTHENTICATION = '?uid={0}&pwd={1}'.format(SORENSON_USERNAME,
                                                    SORENSON_PASSWORD)
SORENSON_API_URL = 'http://sorenson03.cern.ch/api/jobs/{job_id}'
SORENSON_SUBMIT_URL = 'http://sorenson03.cern.ch/api/jobs'
SORENSON_STATUS_URL = 'http://sorenson03.cern.ch/api/jobs/status/{job_id}'
SORENSON_INPUT_FOLDER = "file://cern.ch/dfs/Users/s/switowsk/Sorenson/INPUT/"
SORENSON_OUTPUT_FOLDER = "file://cern.ch/dfs/Users/s/switowsk/Sorenson/OUTPUT/"
SORENSON_DEFAULT_QUEUE = '00000000-0000-0000-0000-000000000000'
PRESET_ID = '47752c8c-5fc4-4de3-94e0-a266ce0a3188'  # Random preset


class SorensonError(Exception):
    """Base class for exceptions in this module."""

    def _init_(self, error_message):
        self.error_message = error_message

    def _str_(self):
        return self.error_message


class TranscodingSorenson(object):
    """CDS Sorenson extension."""

    # def _generate_json(slave, clip, input_name, preset):
    def _generate_json(filename, input_file_uri, preset):
        """Generate JSON that will be sent to Sorenson server.

        :param filename: string with the filename.
        :param input_file_uri: string with the location of source file.
        :param preset: id of the preset (taken from sorenson dashboard).
        :returns: JSON with Sorenson response.
        """
        output = {}

        output_file_uri = SORENSON_OUTPUT_FOLDER + filename
        output['Name'] = filename[:49]
        output['QueueId'] = SORENSON_DEFAULT_QUEUE

        jobInfo = {}

        source_media = {}
        source_media['FileUri'] = input_file_uri
        jobInfo['SourceMediaList'] = [source_media]

        destination_list = {}
        destination_list['FileUri'] = output_file_uri
        jobInfo['DestinationList'] = [destination_list]

        preset_id = {"PresetId": preset}
        jobInfo['CompressionPresetList'] = [preset_id]

        output['JobMediaInfo'] = jobInfo

        return output

    def start(self, filename, input_file_uri, preset):
        """Encode a video that is already in the input folder."""
        current_app.logger.debug("Encoding {0} with the preset {1}"
                                 .format(filename, preset))

        # Build the request of the transcoding job
        json_params = self._generate_json(filename, input_file_uri, preset)

        current_app.logger.debug("Sending request to the Sorenson server")

        response = requests.post(SORENSON_SUBMIT_URL + SORENSON_AUTHENTICATION,
                                 json=json_params)

        response_code = response.status_code
        current_app.logger.debug("Received HTTP code: {0}".
                                 format(response_code))

        data = json.load(response.text)

        current_app.logger.debug("Response from Sorenson: {}".format(data))
        if response_code == requests.codes.ok:
            job_id = data.get('JobId')
            return job_id
        else:
            raise SorensonError(
                "Failed to send transcoding request to the server. Received "
                "code: {0}".format(response_code)
            )

    def stop(self, job_id):
        """Stop transcoding job.

        :param job_id: string with the job ID.
        :returns: None.
        """
        # TODO: According to the docs, the job should be in "Hold", "Error" or
        # "Finished" state for this to work - check it
        delete_url = SORENSON_API_URL.format(job_id=job_id)
        headers = {'Accept': 'application/json'}

        response = requests.delete(delete_url + SORENSON_AUTHENTICATION,
                                   headers=headers)
        response_code = response.status_code
        if response_code == requests.codes.ok:
            current_app.logger.debug("Stopped job {0}".format(job_id))
        else:
            raise SorensonError("Could not stop job: {0}".format(job_id))

    def status(self, job_id):
        """Get status of a given job from the Sorenson server.

        :param job_id: string with the job ID.
        :returns: JSON with Sorenson response.
        """
        status_url = SORENSON_STATUS_URL.format(job_id=job_id)
        headers = {'Accept': 'application/json'}

        current_app.logger.debug("Sending request to the Sorenson server")
        response = requests.get(status_url + SORENSON_AUTHENTICATION,
                                headers=headers)

        response_code = response.status_code
        if response_code == requests.codes.ok:
            return json.load(response.text)
        else:
            raise SorensonError("Failed to get status for job: {0}".
                                format(response_code))
