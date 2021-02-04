import json
import datetime
import pytz

from pytest import fixture, mark

from programmes.management.commands.populate_packages import Command
from programmes.models import Chaines, BouquetTv, BouquetsChaines


@fixture
def db_feed():
    return Command()


@mark.django_db
def test_populate_package_free(db_feed):
    
    db_feed.populate("free")

    bouquet = BouquetTv.objects.get(nom="free")

    assert bouquet.nom == "free"