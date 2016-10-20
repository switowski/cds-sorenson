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

from flask import current_app


def generate_json_for_encoding(file_path, preset_name):
    """Generate JSON that will be sent to Sorenson server to start encoding.

    :param file_path: string with the full file path, something like
        /eos/cds/test/sorenson/8f/m2/728-jsod98-8s9df2-89fg-lksdjf/data where
        the last part "data" is the filename and the last directory is the
        bucket id.
    :param preset: id of the preset (taken from sorenson dashboard).
    :returns: JSON that can be send to Sorenson server.
    """
    def _get_bucket_id(file_path):
        """Return bucket ID from the file path."""
        return file_path.split("/")[-2]

    output = {}

    preset_config = current_app.config['CDS_SORENSON_PRESETS'].get(preset_name)
    preset_id, extension = preset_config

    bucket_id = _get_bucket_id(file_path)

    # Use the bucket ID for sorenson dashboard as the filename will always be
    # "data"
    output['Name'] = 'CDS-' + bucket_id
    output['QueueId'] = current_app.config['CDS_SORENSON_DEFAULT_QUEUE']

    source_media = {}
    source_media['FileUri'] = file_path
    source_media['UserName'] = current_app.config['CDS_SORENSON_USERNAME']
    source_media['Password'] = current_app.config['CDS_SORENSON_PASSWORD']

    jobInfo = {}
    jobInfo['SourceMediaList'] = [source_media]

    output_folder = current_app.config['CDS_SORENSON_OUTPUT_FOLDER']

    destination_list = {}
    destination_list['FileUri'] = "{0}{1}/".format(output_folder, bucket_id)
    jobInfo['DestinationList'] = [destination_list]

    preset_id_json = {"PresetId": preset_id}
    jobInfo['CompressionPresetList'] = [preset_id_json]

    output['JobMediaInfo'] = jobInfo

    return output
