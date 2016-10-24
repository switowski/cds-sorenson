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

from __future__ import absolute_import, print_function

import json
import requests

from flask import current_app

from .utils import generate_json_for_encoding


class SorensonError(Exception):
    """Base class for exceptions in this module."""

    def _init_(self, error_message):
        self.error_message = error_message

    def _str_(self):
        return self.error_message


def start_encoding(input_file, preset_name):
    """Encode a video that is already in the input folder.

    :param input_file: string with the filename, something like
        /eos/cds/test/sorenson/8f/m2/728-jsod98-8s9df2-89fg-lksdjf/data where
        the last part "data" is the filename and the last directory is the
        bucket id.
    :param preset_name: id of the preset (taken from sorenson dashboard).
    :returns: job ID.
    """
    current_app.logger.debug("Encoding {0} with the preset {1}"
                             .format(input_file, preset_name))

    # Build the request of the encoding job
    json_params = generate_json_for_encoding(input_file, preset_name)

    headers = {'Accept': 'application/json'}
    response = requests.post(current_app.config['CDS_SORENSON_SUBMIT_URL'],
                             headers=headers, json=json_params)

    data = json.loads(response.text)

    if response.status_code == requests.codes.ok:
        job_id = data.get('JobId')
        return job_id
    else:
        # something is wrong - sorenson server is not responding or the
        # configuration is wrong and we can't contact sorenson server
        raise SorensonError(response.status_code)


def batch_start_encoding(input_file, presets_names):
    """Start encoding multiple files with multiple presets.

    :param input_file: string with the filename, something like
        /eos/cds/test/sorenson/8f/m2/728-jsod98-8s9df2-89fg-lksdjf/data where
        the last part "data" is the filename and the last directory is the
        bucket id.
    :param presets_names: list of presets.
    :returns: list with jobs_id.

    Each file will be encoded with each preset.
    """
    jobs_ids = []
    for preset in presets_names:
        jobs_ids.append(start_encoding(input_file, preset))
    return jobs_ids


def stop_encoding(job_id):
    """Stop encoding job.

    :param job_id: string with the job ID.
    :returns: None.
    """
    delete_url = (current_app.config['CDS_SORENSON_DELETE_URL']
                             .format(job_id=job_id))
    headers = {'Accept': 'application/json'}

    response = requests.delete(delete_url, headers=headers)
    if response.status_code == requests.codes.ok:
        current_app.logger.debug("Stopped job {0}".format(job_id))
    else:
        raise SorensonError("Could not stop job: {0}".format(job_id))


def batch_stop_encoding(jobs_ids):
    """Stop encoding multiple files.

    :param jobs_id: list of jobs ids to stop.
    :returns: None
    """
    for job_id in jobs_ids:
        try:
            stop_encoding(job_id)
        except SorensonError:
            # If we failed to stop the encoding job, ignore it - in the worst
            # case the encoding will finish and we won't use the file.
            pass


def get_encoding_status(job_id):
    """Get status of a given job from the Sorenson server.

    If the job can't be found in the current queue, it's probably done, so we
    check the archival queue.

    :param job_id: string with the job ID.
    :returns: tuple with the status message and progress in %.
    """
    SORENSON_STATUSES = {
        0: 'Undefined',
        1: 'Waiting',
        2: 'Downloading',
        3: 'Transcoding',
        4: 'Uploading',
        5: 'Finished',
        6: 'Error',
        7: 'Canceled',
        8: 'Deleted',
        9: 'Hold',
        10: 'Incomplete'
    }

    current_jobs_url = (current_app
                        .config['CDS_SORENSON_CURRENT_JOBS_STATUS_URL']
                        .format(job_id=job_id))
    archive_jobs_url = (current_app
                        .config['CDS_SORENSON_ARCHIVE_JOBS_STATUS_URL']
                        .format(job_id=job_id))

    headers = {'Accept': 'application/json'}

    current_app.logger.debug("Checking in the current jobs queue")
    response = requests.get(current_jobs_url, headers=headers)

    if response.status_code == 404:
        current_app.logger.debug("Checking in the archive jobs queue")
        response = requests.get(archive_jobs_url, headers=headers)

    if response.status_code == requests.codes.ok:
        if response.text == '':
            # encoding job was canceled
            return ("Canceled", 100)
        status_json = json.loads(response.text)
        # there are different ways to get the status of a job, depending if
        # the job was successful, so we should check for the status code in
        # different places
        job_status = status_json.get('Status', None).get('Status')
        job_progress = status_json.get('Status', None).get('Progress')
        if job_status:
            return (SORENSON_STATUSES.get(job_status), job_progress)
        # status not found? check in different place
        job_status = status_json.get('StatusStateId')
        if job_status:
            # job is probably either finished or failed, so the progress will
            # always be 100% in this case
            return (SORENSON_STATUSES.get(job_status), 100)
        # if there is still no status then something is wrong, so let's fail
        raise SorensonError("Failed to get status for job: {0}".
                            format(response.status_code))
    # We shouldn't get here, raise an exception
    raise SorensonError(response.status_code)


def batch_get_encoding_status(jobs_ids):
    """Get status for multiple encoding jobs.

    :param jobs_id: list of jobs ids.
    :returns: dictionary where they keys are the job IDs and values are tuples
        with status and progress
    """
    statuses = {}
    for job_id in jobs_ids:
        statuses[job_id] = get_encoding_status(job_id)
    return statuses
