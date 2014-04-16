""" NGDS_HEADER_BEGIN

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey

Please refer the the README.txt file in the base directory of the NGDS project:
https://github.com/ngds/ckanext-ngds/blob/master/README.txt

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero
General Public License as published by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.  https://github.com/ngds/ckanext-ngds
ngds/blob/master/LICENSE.md or
http://www.gnu.org/licenses/agpl.html

NGDS_HEADER_END """

"""
Manage rendering of user-management pages, creation of users and roles, management of users and roles, and functionality for the system administrator.
"""
from ckan.lib.base import *
from ckan.lib.navl.dictization_functions import unflatten
from ckan.lib.base import (request,
                           render,
                           model,
                           abort, h, g, c)
from ckan.logic import get_action, check_access
from ckan.logic import (tuplize_dict, clean_dict, parse_params)

from ckanext.ngds.ngdsui.controllers.ngds import NGDSBaseController
from ckan.logic import NotAuthorized, NotFound
from ckanext.ngds.ngdsui.misc import helpers


class UserController(NGDSBaseController):
    def manage_users(self, group_name='public', data_dict=None):

        """
        Renders the user management page and lists users along with their roles.
        """
        context = {'model': model, 'session': model.Session, 'user': c.user or c.author}

        try:
            check_access('manage_users', context, data_dict)
        except NotAuthorized, error:
            abort(401, error.__str__())

        group_name = helpers.get_default_group()
        group_members = self.member_list(group_name)

        q = model.Session.query(model.User). \
            filter(~ model.User.name.in_((model.PSEUDO_USER__LOGGED_IN, model.PSEUDO_USER__VISITOR)))

        def role_lookup(userid, group_members):

            for user_id, role in group_members:
                if user_id == userid:
                    return role
            return ""

        roles = get_action('member_roles_list')(context, {})

        c.roles = [{'text': u'', 'value': 'default'}]
        c.roles.extend(roles)
        g.group_name = group_name

        c.members = [(m.id, m.name, m.email, role_lookup(m.id, group_members),) for m in q.all()]

        return render('user/manage_users.html')


    def logged_out_page(self):
        """
        This renders a page that informs the user of a successful logout.
        """
        url = h.url_for(controller='ckanext.ngds.ngdsui.controllers.home:HomeController', action='render_index')
        h.flash_notice(_('You are now Logged out'), allow_html=True)
        redirect(url)


    def member_new(self, data_dict=None):
        """
        Accepts a request to change the role or assign a role to a user and performs the operation.
        """
        context = {'model': model, 'session': model.Session, 'user': c.user}
        data_dict = clean_dict(unflatten(tuplize_dict(parse_params(request.params))))

        try:
            check_access('manage_users', context, data_dict)
        except NotAuthorized, error:
            abort(401, error.__str__())

        group = model.Group.get(helpers.get_default_group())

        data_dict['id'] = group.id

        role = data_dict['role']

        if role == 'default':
            get_action('group_member_delete')(context, data_dict)
            h.flash_notice(_('User rights are removed.'), allow_html=True)
        else:
            get_action('group_member_create')(context, data_dict)
            h.flash_success(_('User Role is Updated Successfully.'), allow_html=True)

        url = h.url_for(controller='ckanext.ngds.ngdsui.controllers.user:UserController', action='manage_users')
        redirect(url)


    def member_list(self, group_name):
        """
        Accepts a group name, which is configured in the site configuration file and returns users that are associated with the group.
        """

        group = model.Group.get(group_name)

        q = model.Session.query(model.Member). \
            filter(model.Member.group_id == group.id). \
            filter(model.Member.state == "active"). \
            filter(model.Member.table_name == "user")

        return [(m.table_id, m.capacity,) for m in q.all()]

    def custom_activity_stream(self, dataset):
        """
        Render custom package activity stream
        """

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True}
        data_dict = {'id': dataset}
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
            c.package_activity_stream = get_action(
                    'package_activity_list_html')(context,
                            {'id': c.pkg_dict['id']})
            c.related_count = c.pkg.related_count
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read dataset %s') % dataset)

        return render('package/activity.html')