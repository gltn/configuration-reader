# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : Test utils
Description          : Test utils
Date                 : 20-11-2020
Copyright            : (C) 2020 by UN-Habitat and implementing partners.
                       See the accompanying file CONTRIBUTORS.txt in the root
Email                : un-habitat-gltn@un.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 3 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os


def test_config_file():
    """
    Return the path of the test STDM configuration file.
    """
    conf_file = os.path.normpath(
        '{0}/data/configuration.stc'.format(os.path.dirname(__file__))
    )

    return conf_file
