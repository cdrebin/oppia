# Copyright 2019 The Oppia Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Controllers for the community dashboard page."""
from __future__ import absolute_import  # pylint: disable=import-only-modules
from __future__ import unicode_literals  # pylint: disable=import-only-modules

from constants import constants
from core.controllers import acl_decorators
from core.controllers import base
from core.domain import exp_fetchers
from core.domain import opportunity_services
import feconf
import utils


class CommunityDashboardPage(base.BaseHandler):
    """Page showing the community dashboard."""

    @acl_decorators.open_access
    def get(self):
        # TODO(#7402): Serve this page statically through app.yaml once
        # the COMMUNITY_DASHBOARD_ENABLED flag is removed.
        if not feconf.COMMUNITY_DASHBOARD_ENABLED:
            raise self.PageNotFoundException
        self.render_template('community-dashboard-page.mainpage.html')


class ContributionOpportunitiesHandler(base.BaseHandler):
    """Provides data for opportunities available in different categories."""

    GET_HANDLER_ERROR_RETURN_TYPE = feconf.HANDLER_TYPE_JSON

    @acl_decorators.open_access
    def get(self, opportunity_type):
        """Handles GET requests."""
        if not feconf.COMMUNITY_DASHBOARD_ENABLED:
            raise self.PageNotFoundException
        search_cursor = self.request.get('cursor', None)

        if opportunity_type == constants.OPPORTUNITY_TYPE_TRANSLATION:
            language_code = self.request.get('language_code')
            if language_code is None or not (
                    utils.is_supported_audio_language_code(language_code)):
                raise self.InvalidInputException
            opportunities, next_cursor, more = (
                opportunity_services.get_translation_opportunities(
                    language_code, search_cursor))

        elif opportunity_type == constants.OPPORTUNITY_TYPE_VOICEOVER:
            language_code = self.request.get('language_code')
            if language_code is None or not (
                    utils.is_supported_audio_language_code(language_code)):
                raise self.InvalidInputException
            opportunities, next_cursor, more = (
                opportunity_services.get_voiceover_opportunities(
                    language_code, search_cursor))

        else:
            raise self.PageNotFoundException

        self.values = {
            'opportunities': opportunities,
            'next_cursor': next_cursor,
            'more': more
        }

        self.render_json(self.values)


class TranslatableTextHandler(base.BaseHandler):
    """Provides lessons content which can be translated in a given language."""

    GET_HANDLER_ERROR_RETURN_TYPE = feconf.HANDLER_TYPE_JSON

    @acl_decorators.open_access
    def get(self):
        """Handles GET requests."""
        language_code = self.request.get('language_code')
        exp_id = self.request.get('exp_id')

        if not utils.is_supported_audio_language_code(language_code):
            raise self.InvalidInputException('Invalid language_code: %s' % (
                language_code))

        if not opportunity_services.is_exploration_available_for_contribution(
                exp_id):
            raise self.InvalidInputException('Invalid exp_id: %s' % exp_id)

        exp = exp_fetchers.get_exploration_by_id(exp_id)
        state_names_to_content_id_mapping = exp.get_translatable_text(
            language_code)

        self.values = {
            'state_names_to_content_id_mapping': (
                state_names_to_content_id_mapping),
            'version': exp.version
        }

        self.render_json(self.values)
