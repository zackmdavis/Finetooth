# thanks to @Ish-0 for this (https://github.com/Instagram/MonkeyType/issues/28#issuecomment-353533568)

import django
django.setup()

from monkeytype.config import DefaultConfig
class MonkeyConfig(DefaultConfig):
        pass

CONFIG = MonkeyConfig()
