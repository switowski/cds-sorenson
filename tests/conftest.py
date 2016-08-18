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


"""Pytest configuration."""

from __future__ import absolute_import, print_function

import pytest
from flask import Flask

from cds_sorenson import CDSSorenson


@pytest.fixture()
def config():
    """Custom config for testing purposes."""
    sorenson_directory = 'file://cern.ch/dfs/Users/s/switowsk/Sorenson'
    return dict(
        CDS_SORENSON_USERNAME='xxxxxx',
        CDS_SORENSON_PASSWORD='XXXXXX',
        CDS_SORENSON_INPUT_FOLDER=sorenson_directory + '/INPUT/',
        CDS_SORENSON_OUTPUT_FOLDER=sorenson_directory + '/OUTPUT/',
        TESTING=True
    )


@pytest.yield_fixture()
def app(config):
    """Flask application fixture."""
    app_ = Flask('testapp')

    CDSSorenson(app_)

    app_.config.update(config)

    with app_.app_context():
        yield app_


@pytest.fixture()
def start_response():
    """Example response when starting new encoding job."""
    return u'{"JobId":"11111111-aaaa"}'


@pytest.fixture()
def running_job_status_response():
    """Example response when checking the status of running encoding job."""
    return u"""{
        "EncodeServerId":null,
        "JobId":"11111111-aaaa",
        "LastUpdate":null,
        "LastUpdateIso8601":null,
        "Name":"CDS_TEST.mp4",
        "QueueId":"00000000-0000-0000-0000-000000000000",
        "Status": {
            "Created":null,
            "CreatedIso8601":null,
            "DestinationName":null,
            "Duration":"PT0S",
            "ErrorCode":null,
            "Id":"00000000-0000-0000-0000-000000000000",
            "Modified":null,
            "ModifiedIso8601":null,
            "PresetName":null,
            "Progress":55.810001373291016,
            "RetryCount":null,
            "Status":9,
            "StatusMessage":null,
            "TimeFinished":null,
            "TimeFinishedIso8601":null,
            "TimeStarted":"\\/Date(1471610064000+0200)\\/",
            "TimeStartedIso8601":"2016-08-19T12:34:24.0000000Z"
        },
        "TimeSubmitted":"\\/Date(1471609988000+0200)\\/",
        "TimeSubmittedIso8601":"2016-08-19T12:33:08.0000000Z",
        "TotalSourceSize":28335481
    }"""


@pytest.fixture()
def finished_job_status_response():
    """Example response when checking the status of finished encoding job."""
    return u"""{
        "ArchiveMetadataList":[],
        "CompressionPresetList":[
        {
            "JobId":null,
            "JobPresetId":"a72d5576-5cd4-48a5-98b9-da016342dbee",
            "PresetId":"2c5a86db-1018-4ff8-a5ad-daebd4cb4ff4",
            "PresetXmlBase64Data":"aWRlb0NvbXByZXNzb3I+DQo8L091dHB1dD4=",
            "UriLocation":null,
            "WatchFolderId":null
        }],
        "DestinationList":[
        {
            "Created":null,
            "CreatedIso8601":null,
            "CredentialId":null,
            "DestinationId":"8aff9ec1-e7cf-43bf-a7c8-4ad234c5aa6c",
            "DestinationMetadataList":[],
            "DestinationName":null,
            "ExtensionNamingMethod":"Undefined",
            "FileName":null,
            "FileNamingMethod":"Undefined",
            "FileUri":"file:\\/\\/cern.ch\\/dfs\\/Users\\/s\\/switowsk\\/Sorenson\\/OUTPUT\\/",
            "JobId":null,
            "Modified":null,
            "ModifiedIso8601":null,
            "Password":null,
            "S3BucketName":null,
            "S3ThumbBucket":null,
            "ThumbFilePattern":null,
            "ThumbUri":null,
            "Type":1,
            "UserName":null,
            "WatchFolderId":null
        }],
        "ErrorCode":null,
        "InPoint":null,
        "JobId":"350caa45-8e76-4a9e-b7af-6224b1e1b010",
        "Name":"CDS_TEST.mp4",
        "OriginalJobId":"350caa45-8e76-4a9e-b7af-6224b1e1b010",
        "OutPoint":null,
        "OutputList":[
        {
            "DestinationId":"8aff9ec1-e7cf-43bf-a7c8-4ad234c5aa6c",
            "DurationSeconds":36,
            "FileAudDataRate":"192000",
            "FileFrameRate":"25",
            "FileHeight":360,
            "FileName":"CDS_TEST.mp4",
            "FileSize":8412576,
            "FileType":"VideoOutput",
            "FileVidDataRate":"2000000",
            "FileWidth":640,
            "OutputId":"8489d19f-df20-40e1-8691-1429ed678917"
        }],
        "PercentCompleteOverall":100,
        "QueueName":"Default",
        "ServerName":"sorenson01.cern.ch",
        "SourceMedia":
        {
            "AutoDeleteSource":false,
            "CompressOrder":0,
            "Created":null,
            "CreatedIso8601":null,
            "CredentialId":null,
            "EncodeAllAudioTracks":false,
            "FileName":null,
            "FileSize":-1,
            "FileUri":"file:\\/\\/cern.ch\\/dfs\\/Users\\/s\\/switowsk\\/Sorenson\\/INPUT\\/CDS_TEST.mp4",
            "IsWatchfolder":false,
            "JobId":null,
            "JobSubmitted":null,
            "JobSubmittedIso8601":null,
            "Modified":null,
            "ModifiedIso8601":null,
            "Password":"XXXXXX",
            "S3BucketName":null,
            "SourceId":"00000000-0000-0000-0000-000000000000",
            "Type":1,
            "UserName":"xxxxxx",
            "WatchFolderId":null,
            "WatermarkInfo":
            {
                "WatermarkImageCredentialId":null,
                "WatermarkImagePassword":null,
                "WatermarkImageUri":null,
                "WatermarkImageUserName":null
            }
        },
        "SourceMediaList":[
        {
            "AutoDeleteSource":false,
            "CompressOrder":0,
            "Created":null,
            "CreatedIso8601":null,
            "CredentialId":null,
            "EncodeAllAudioTracks":false,
            "FileName":null,
            "FileSize":-1,
            "FileUri":"file:\\/\\/cern.ch\\/dfs\\/Users\\/s\\/switowsk\\/Sorenson\\/INPUT\\/CDS_TEST.mp4",
            "IsWatchfolder":false,
            "JobId":null,
            "JobSubmitted":null,
            "JobSubmittedIso8601":null,
            "Modified":null,
            "ModifiedIso8601":null,
            "Password":"XXXXXX",
            "S3BucketName":null,
            "SourceId":"00000000-0000-0000-0000-000000000000",
            "Type":1,
            "UserName":"xxxxxx",
            "WatchFolderId":null,
            "WatermarkInfo":
            {
                "WatermarkImageCredentialId":null,
                "WatermarkImagePassword":null,
                "WatermarkImageUri":null,
                "WatermarkImageUserName":null
            }
        }],
        "StatusList":[
        {
            "DestinationName":null,
            "Duration":"PT0S",
            "ErrorCode":null,
            "Message":"Job on HOLD",
            "PresetName":null,
            "Progress":0,
            "RetryCount":0,
            "Status":"Hold",
            "TimeFinished":null,
            "TimeFinishedIso8601":null,
            "TimeStarted":"\\/Date(1471610031000+0200)\\/",
            "TimeStartedIso8601":"2016-08-19T12:33:51.0000000Z"
        },
        {
            "DestinationName":null,
            "Duration":"PT0S",
            "ErrorCode":null,
            "Message":"Job on HOLD",
            "PresetName":null,
            "Progress":0,
            "RetryCount":0,
            "Status":"Hold",
            "TimeFinished":null,
            "TimeFinishedIso8601":null,
            "TimeStarted":"\\/Date(1471610031000+0200)\\/",
            "TimeStartedIso8601":"2016-08-19T12:33:51.0000000Z"
        },
        {
            "DestinationName":null,
            "Duration":"PT0S",
            "ErrorCode":null,
            "Message":"Job on HOLD",
            "PresetName":null,
            "Progress":0,
            "RetryCount":0,
            "Status":"Hold",
            "TimeFinished":null,
            "TimeFinishedIso8601":null,
            "TimeStarted":"\\/Date(1471610031000+0200)\\/",
            "TimeStartedIso8601":"2016-08-19T12:33:51.0000000Z"
        },
        {
            "DestinationName":null,
            "Duration":"PT0S",
            "ErrorCode":null,
            "Message":"Job on HOLD",
            "PresetName":null,
            "Progress":0,
            "RetryCount":0,
            "Status":"Hold",
            "TimeFinished":null,
            "TimeFinishedIso8601":null,
            "TimeStarted":"\\/Date(1471610031000+0200)\\/",
            "TimeStartedIso8601":"2016-08-19T12:33:51.0000000Z"
        },
        {
            "DestinationName":null,
            "Duration":"PT0S",
            "ErrorCode":null,
            "Message":"Job on HOLD",
            "PresetName":null,
            "Progress":0,
            "RetryCount":0,
            "Status":"Hold",
            "TimeFinished":null,
            "TimeFinishedIso8601":null,
            "TimeStarted":"\\/Date(1471610031000+0200)\\/",
            "TimeStartedIso8601":"2016-08-19T12:33:51.0000000Z"
        },
        {
            "DestinationName":null,
            "Duration":"PT0S",
            "ErrorCode":null,
            "Message":"Job on HOLD",
            "PresetName":null,
            "Progress":0,
            "RetryCount":0,
            "Status":"Hold",
            "TimeFinished":null,
            "TimeFinishedIso8601":null,
            "TimeStarted":"\\/Date(1471610031000+0200)\\/",
            "TimeStartedIso8601":"2016-08-19T12:33:51.0000000Z"
        },
        {
            "DestinationName":null,
            "Duration":"PT8M56S",
            "ErrorCode":null,
            "Message":"Job on HOLD",
            "PresetName":null,
            "Progress":0,
            "RetryCount":0,
            "Status":"Hold",
            "TimeFinished":"\\/Date(1471610568000+0200)\\/",
            "TimeFinishedIso8601":"2016-08-19T12:42:48.0000000Z",
            "TimeStarted":"\\/Date(1471610032000+0200)\\/",
            "TimeStartedIso8601":"2016-08-19T12:33:52.0000000Z"
        },
        {
            "DestinationName":null,
            "Duration":"PT2S",
            "ErrorCode":null,
            "Message":null,
            "PresetName":null,
            "Progress":100,
            "RetryCount":0,
            "Status":"Downloading",
            "TimeFinished":"\\/Date(1471610067000+0200)\\/",
            "TimeFinishedIso8601":"2016-08-19T12:34:27.0000000Z",
            "TimeStarted":"\\/Date(1471610065000+0200)\\/",
            "TimeStartedIso8601":"2016-08-19T12:34:25.0000000Z"
        },
        {
            "DestinationName":null,
            "Duration":"PT40S",
            "ErrorCode":null,
            "Message":"Job on HOLD",
            "PresetName":"YouTube_480p",
            "Progress":57.659999847412109,
            "RetryCount":0,
            "Status":"Transcoding",
            "TimeFinished":"\\/Date(1471610107000+0200)\\/",
            "TimeFinishedIso8601":"2016-08-19T12:35:07.0000000Z",
            "TimeStarted":"\\/Date(1471610067000+0200)\\/",
            "TimeStartedIso8601":"2016-08-19T12:34:27.0000000Z"
        },
        {
            "DestinationName":null,
            "Duration":"PT1S",
            "ErrorCode":null,
            "Message":null,
            "PresetName":null,
            "Progress":100,
            "RetryCount":1,
            "Status":"Downloading",
            "TimeFinished":"\\/Date(1471611333000+0200)\\/",
            "TimeFinishedIso8601":"2016-08-19T12:55:33.0000000Z",
            "TimeStarted":"\\/Date(1471611332000+0200)\\/",
            "TimeStartedIso8601":"2016-08-19T12:55:32.0000000Z"
        },
        {
            "DestinationName":null,
            "Duration":"PT35S",
            "ErrorCode":null,
            "Message":null,
            "PresetName":"YouTube_480p",
            "Progress":100,
            "RetryCount":1,
            "Status":"Transcoding",
            "TimeFinished":"\\/Date(1471611369000+0200)\\/",
            "TimeFinishedIso8601":"2016-08-19T12:56:09.0000000Z",
            "TimeStarted":"\\/Date(1471611334000+0200)\\/",
            "TimeStartedIso8601":"2016-08-19T12:55:34.0000000Z"
        },
        {
            "DestinationName":null,
            "Duration":"PT1S",
            "ErrorCode":null,
            "Message":null,
            "PresetName":null,
            "Progress":100,
            "RetryCount":0,
            "Status":"Uploading",
            "TimeFinished":"\\/Date(1471611370000+0200)\\/",
            "TimeFinishedIso8601":"2016-08-19T12:56:10.0000000Z",
            "TimeStarted":"\\/Date(1471611369000+0200)\\/",
            "TimeStartedIso8601":"2016-08-19T12:56:09.0000000Z"
        }],
        "StatusMessage":"",
        "StatusState":"Finished",
        "StatusStateId":5,
        "ThumbTime":null,
        "TimeArchived":"\\/Date(1471611370000+0200)\\/",
        "TimeArchivedIso8601":"2016-08-19T12:56:10.0000000Z",
        "TimeFinished":"\\/Date(1471611370000+0200)\\/",
        "TimeFinishedIso8601":"2016-08-19T12:56:10.0000000Z",
        "TimeNotified":null,
        "TimeNotifiedIso8601":null,
        "TimeStarted":"\\/Date(1471611332000+0200)\\/",
        "TimeStartedIso8601":"2016-08-19T12:55:32.0000000Z",
        "TimeSubmitted":"\\/Date(1471609988000+0200)\\/",
        "TimeSubmittedIso8601":"2016-08-19T12:33:08.0000000Z",
        "WatchFolderName":null
    }"""
