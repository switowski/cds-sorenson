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


"""Module tests."""

from __future__ import absolute_import, print_function

import json

from flask import Flask
from mock import MagicMock, patch

from cds_sorenson import CDSSorenson
from cds_sorenson.api import start_encoding, stop_encoding, \
    get_encoding_status


def test_version():
    """Test version import."""
    from cds_sorenson import __version__
    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask('testapp')
    ext = CDSSorenson(app)
    assert 'cds-sorenson' in app.extensions

    app = Flask('testapp')
    ext = CDSSorenson()
    assert 'cds-sorenson' not in app.extensions
    ext.init_app(app)
    assert 'cds-sorenson' in app.extensions


@patch('cds_sorenson.api.requests.post')
def test_start_encoding(requests_post_mock, app, start_response):
    """Test if starting encoding works."""
    filename = 'CDS_TEST.mp4'
    preset = 'Youtube 480p'

    # Mock sorenson response
    sorenson_response = MagicMock()
    sorenson_response.text = start_response
    sorenson_response.status_code = 200
    requests_post_mock.return_value = sorenson_response

    job_id = start_encoding(filename, preset)
    assert job_id == "11111111-aaaa"


@patch('cds_sorenson.api.requests.get')
def test_encoding_status(requests_get_mock, app, running_job_status_response):
    """Test if getting encoding status works."""
    job_id = "11111111-aaaa"

    # Mock sorenson response
    sorenson_response = MagicMock()
    sorenson_response.text = running_job_status_response
    sorenson_response.status_code = 200
    requests_get_mock.return_value = sorenson_response

    status_json = get_encoding_status(job_id)
    assert status_json == json.loads(running_job_status_response)


@patch('cds_sorenson.api.requests.delete')
def test_stop_encoding(requests_delete_mock, app):
    """Test if stopping encoding works."""
    job_id = "11111111-aaaa"

    # Mock sorenson response
    sorenson_response = MagicMock()
    sorenson_response.status_code = 200
    requests_delete_mock.return_value = sorenson_response

    returned_value = stop_encoding(job_id)
    # In case of some problems, we should get an exception
    assert returned_value is None

# TODO: Test if stopping non-existing job (or stopping the same job twice)
# gives an error
