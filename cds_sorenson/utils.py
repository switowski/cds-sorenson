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

from os.path import basename, dirname, normpath

import requests
from flask import current_app

from .error import SorensonError


def generate_json_for_encoding(input_file, preset_name, output_file=None):
    """Generate JSON that will be sent to Sorenson server to start encoding."""
    output_file = output_file or normpath('{0}/{1}/{2}-{3}'.format(
        current_app.config['CDS_SORENSON_OUTPUT_FOLDER'],
        dirname(input_file), basename(input_file), preset_name)
    )

    try:
        preset_id = current_app.config['CDS_SORENSON_PRESETS'][preset_name][0]
    except KeyError:
        raise SorensonError('Invalid preset "{0}"'.format(preset_name))

    return dict(
        Name='CDS File:{0} Preset:{1}'.format(input_file, preset_name),
        QueueId=current_app.config['CDS_SORENSON_DEFAULT_QUEUE'],
        JobMediaInfo=dict(
            SourceMediaList=dict(
                FileUri=input_file,
                UserName=current_app.config['CDS_SORENSON_USERNAME'],
                Password=current_app.config['CDS_SORENSON_PASSWORD'],
            ),
            DestinationList=[dict(FileUri='{}/'.format(output_file))],
            CompressionPresetList=[dict(PresetId=preset_id)],
        ),
    )


def get_status(job_id):
    """For a given job id, returns the status as JSON string.

    If the job can't be found in the current queue, it's probably done, so we
    check the archival queue. Raises an exception if there the response has a
    different code than 200.

    :param job_id: string with the job ID.
    :returns: JSON with the status or empty string if the job was not found.
    """
    current_jobs_url = (current_app
                        .config['CDS_SORENSON_CURRENT_JOBS_STATUS_URL']
                        .format(job_id=job_id))
    archive_jobs_url = (current_app
                        .config['CDS_SORENSON_ARCHIVE_JOBS_STATUS_URL']
                        .format(job_id=job_id))

    headers = {'Accept': 'application/json'}

    response = requests.get(current_jobs_url, headers=headers)

    if response.status_code == 404:
        response = requests.get(archive_jobs_url, headers=headers)

    if response.status_code == requests.codes.ok:
        return response.text
    else:
        raise SorensonError(response.status_code)
