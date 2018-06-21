#  Copyright (c) 2018 Red Hat, Inc.
#
#  This file is part of ARA Records Ansible.
#
#  ARA is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  ARA is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with ARA.  If not, see <http://www.gnu.org/licenses/>.

import factory

from ara.api import models
from ara.api.tests import utils


# constants for things like compressed byte strings or objects
FILE_CONTENTS = '---\n# Example file'
HOST_FACTS = {
    'ansible_fqdn': 'hostname',
    'ansible_distribution': 'CentOS'
}
PLAYBOOK_PARAMETERS = {
    'ansible_version': '2.5.5',
    'inventory': '/etc/ansible/hosts'
}
RESULT_CONTENTS = {
    'results': [{
        'msg': 'something happened'
    }]
}
REPORT_DESCRIPTION = 'report description'
TASK_TAGS = ['always', 'never']


class FileContentFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.FileContent
        django_get_or_create = ('sha1',)

    sha1 = utils.sha1(FILE_CONTENTS)
    contents = utils.compressed_str(FILE_CONTENTS)


class FileFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.File

    path = '/path/playbook.yml'
    content = factory.SubFactory(FileContentFactory)


class ReportFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Report

    name = 'test report'
    description = utils.compressed_str(REPORT_DESCRIPTION)


class PlaybookFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Playbook

    ansible_version = '2.4.0'
    completed = True
    parameters = utils.compressed_obj(PLAYBOOK_PARAMETERS)
    file = factory.SubFactory(FileFactory)


class PlayFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Play

    name = 'test play'
    completed = True
    playbook = factory.SubFactory(PlaybookFactory)


class TaskFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Task

    name = 'test task'
    completed = True
    action = 'setup'
    lineno = 2
    handler = False
    tags = utils.compressed_obj(TASK_TAGS)
    play = factory.SubFactory(PlayFactory)
    file = factory.SubFactory(FileFactory)


class HostFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Host

    facts = utils.compressed_obj(HOST_FACTS)
    name = 'hostname'
    changed = 1
    failed = 0
    ok = 2
    skipped = 1
    unreachable = 0
    play = factory.SubFactory(PlayFactory)


class ResultFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Result

    content = utils.compressed_obj(RESULT_CONTENTS)
    status = 'ok'
    host = factory.SubFactory(HostFactory)
    task = factory.SubFactory(TaskFactory)
