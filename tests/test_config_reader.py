# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : Test STDM configuration reader
Description          : Unit tests for STDM configuration parser
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
import unittest

from stdm_config import StdmConfigurationReader, StdmConfiguration
from stdm_config.columns import GeometryColumn
from .utils import test_config_file


INF_SETTLEMENT_PROFILE = 'Informal_Settlement'
LG_PROFILE = 'Local_Government'
RA_PROFILE = 'Rural_Agriculture'

class STDMConfigurationReaderTests(unittest.TestCase):
    """
    Test STDM Configuration object.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Note config is a singleton object
        self.config = StdmConfiguration.instance()
        self.reader = StdmConfigurationReader(test_config_file())

    def setUp(self) -> None:
        self.reader.load()

    def test_config_loaded(self):
        # Assert profiles have been loaded in the configuration
        self.assertEqual(len(self.config.profiles), 3)

        # Check profile names
        profiles_names = {
            INF_SETTLEMENT_PROFILE, LG_PROFILE, RA_PROFILE
        }
        config_profile_names = set(self.config.profiles.keys())
        self.assertEqual(config_profile_names, profiles_names)

    def test_profile(self):
        # Test profile properties

        # Check if informal settlement profile exists
        inf_profile = self.config.profile(INF_SETTLEMENT_PROFILE)
        self.assertIsNotNone(inf_profile)

        # Check profile prefix (for appending to db table names)
        self.assertEqual(inf_profile.prefix, 'in')

        # Check if profile has an entity by short name (excludes prefix)
        self.assertTrue(inf_profile.has_entity('Structure'))

        # Get entity object by short name
        self.assertIsNotNone(inf_profile.entity('Person'))

        # Get entity object by table name in db
        self.assertIsNotNone(inf_profile.entity_by_name('in_person'))

        # Check user-defined entity names
        entity_names = {'Person', 'Structure'}
        inf_user_ent = [e.short_name for e in inf_profile.user_entities()]
        self.assertEqual(set(inf_user_ent), entity_names)

    def test_lookup_tables(self):
        # Test functions related to lookup tables i.e. ValueList

        inf_profile = self.config.profile(INF_SETTLEMENT_PROFILE)

        # Check if gender lookup entity exists
        lookup_tables = [lk.short_name for lk in inf_profile.value_lists()]
        self.assertIn('check_gender', lookup_tables)

        # Get lookup options
        utilities = {'Water', 'Electricity'}
        utilities_lookup = inf_profile.entity('check_utilities')
        self.assertEqual(set(utilities_lookup.lookups()), utilities)

    def test_social_tenure_relationship(self):
        # Test STR definition
        ra_profile = self.config.profile(RA_PROFILE)

        # Get Social Tenure object
        ra_str = ra_profile.social_tenure

        # Test STR party
        parties = ra_str.parties
        self.assertGreater(len(parties), 0)
        party_name = parties[0].short_name
        self.assertEqual(party_name, 'Farmer')

        # Test spatial unit
        sp_units = ra_str.spatial_units
        self.assertGreater(len(sp_units), 0)
        sp_unit_name = sp_units[0].short_name
        self.assertEqual(sp_unit_name, 'Garden')

        # Test tenure types
        tenure_value_list = ra_str.tenure_type_collection
        tenure_lookups = tenure_value_list.lookups()
        self.assertIn('Communal Ownership', tenure_lookups)

    def test_entity(self):
        # Test entity API
        lg_profile = self.config.profile(LG_PROFILE)

        person_entity = lg_profile.entity('Person')
        # Test corresponding db table name
        self.assertEqual(person_entity.name, 'lo_person')

        # Test if it allows supporting documents
        self.assertTrue(person_entity.supports_documents)
        # Check if it supports a given supporting document
        self.assertIn(
            'Identification Card',
            person_entity.document_types_non_hex()
        )

        # Get number of columns (includes 'id' serial column in db)
        col_num = len(person_entity.columns)
        self.assertEqual(col_num, 10)

        # Get column by name
        address_col = person_entity.column('physical_address')
        self.assertIsNotNone(address_col)

        # Get column type (please note that is STDM column type, not db)
        self.assertEqual(address_col.TYPE_INFO, 'VARCHAR')

        # Get columns of date type
        date_cols = person_entity.columns_by_type_info('DATE')
        date_col_names = [dt_col.name for dt_col in date_cols]
        self.assertIn('date_of_birth', date_col_names)

        # Get entities which are parents (i.e. current contains foreign key)
        parent_entities = person_entity.parents()
        self.assertEqual(len(parent_entities), 2)

        # Get entities which are children (i.e. they contain FK to current)
        child_entities = person_entity.children()
        self.assertEqual(len(child_entities), 2)

        parcel_entity = lg_profile.entity('Parcel')
        # Check if its a spatial entity
        self.assertTrue(parcel_entity.has_geometry_column())
        # Get spatial details
        sp_col = parcel_entity.geometry_columns()[0]
        self.assertEqual(sp_col.geometry_type(), 'POLYGON')
        # Same test using enum
        self.assertEqual(sp_col.geom_type, GeometryColumn.POLYGON)
        self.assertEqual(sp_col.srid, 4326)

        # 'layer_display' is a more friendly name in a layer panel
        self.assertEqual(sp_col.layer_display_name, 'Urban Parcels')


if __name__ == '__main__':
    unittest.main()