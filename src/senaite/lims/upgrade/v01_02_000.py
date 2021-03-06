# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.LIMS
#
# Copyright 2018 by it's authors.
# Some rights reserved. See LICENSE and CONTRIBUTING.

from Acquisition import aq_inner
from Acquisition import aq_parent
from bika.lims import logger

from bika.lims.upgrade import upgradestep
from bika.lims.upgrade.utils import UpgradeUtils

from senaite.lims.config import PROJECTNAME as product

version = '1.2.0'
profile = 'profile-{0}:default'.format(product)


@upgradestep(product, version)
def upgrade(tool):
    portal = aq_parent(aq_inner(tool))
    ut = UpgradeUtils(portal)
    ver_from = ut.getInstalledVersion(product)

    if ut.isOlderVersion(product, version):
        logger.info("Skipping upgrade of {0}: {1} > {2}".format(
            product, ver_from, version))
        # The currently installed version is more recent than the target
        # version of this upgradestep
        return True

    logger.info("Upgrading {0}: {1} -> {2}".format(product, ver_from, version))

    # Do nothing, we just only want the profile version to be 1.2.0
    fix_javascript_registry(portal)

    logger.info("{0} upgraded to version {1}".format(product, version))
    return True


def fix_javascript_registry(portal):
    """Fix JS registry
    """

    portal_javascripts = portal.portal_javascripts

    to_remove = [
        "++resource++senaite.lims.bika.static/js/bika.lims.common.js",
        "++resource++senaite.lims.bika.static/js/bika.lims.analysisrequest.js",
        "++resource++senaite.lims.jquery.js/jquery-1.12.4.min.js",
    ]

    for res_id in to_remove:
        logger.info("Removing JS resource {}".format(res_id))
        portal_javascripts.unregisterResource(res_id)
