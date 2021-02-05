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

    tf1 = Chaines(id_chaine="1_test", nom="TF1")
    tf1.save()

    db_feed.populate("free")

    bouquet = BouquetTv.objects.get(nom="free")
    tf1 = Chaines.objects.get(nom="TF1")
    bouquets_chaines = BouquetsChaines.objects.all()

    assert bouquet.nom == "free"
    assert tf1.bouquettv_set.all()[0].nom == "free"
    assert bouquets_chaines[0].numero == 1