# STDM Configuration Reader
A pure Python library for parsing an STDM configuration _(*.stc)_ file. It has been adapted 
from the one used in the STDM [plugin](https://github.com/gltn/stdm) with Qt functionality 
replaced with that provided by native Python libraries. 

All that is required is a file path to the configuration file.

## Quick Example
```
>>> from stdm_config import StdmConfigurationReader, StdmConfiguration

>>> CONFIG_PATH = '/path/to/configuration.stc'
>>> reader = StdmConfigurationReader(CONFIG_PATH)
>>> reader.load()

>>> stdm_config = StdmConfiguration.instance()
>>> for profile in stdm_config.profiles.values():
...    print(profile.name)
...
'Informal_Settlement'
'Local_Government'
'Rural_Agriculture'
```
More snippets on using the STDM configuration framework are available in the unit tests
 [here](https://github.com/gltn/configuration-reader/blob/master/tests/test_config_reader.py).

## License
`stdm_config` is free software. You can redistribute it and/or modify it under the terms of the GNU General 
Public License version 2 (GPLv2) as published by the Free Software Foundation. 

Software distributed under this 
License is distributed on an "AS IS" basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See LICENSE 
or https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html for the specific language governing rights and limitations under the License.