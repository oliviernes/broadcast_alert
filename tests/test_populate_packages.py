from unittest.mock import patch

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


@mark.django_db
def test_populate_package_sfr(db_feed):

    france2 = Chaines(id_chaine="2_test", nom="FRANCE 2")
    france2.save()

    db_feed.populate("sfr")

    bouquet = BouquetTv.objects.get(nom="sfr")
    france2 = Chaines.objects.get(nom="FRANCE 2")
    bouquets_chaines = BouquetsChaines.objects.all()

    assert bouquet.nom == "sfr"
    assert france2.bouquettv_set.all()[0].nom == "sfr"
    assert bouquets_chaines[0].numero == 2


@mark.django_db
def test_populate_package_bouygues(db_feed):

    arte = Chaines(id_chaine="7_test", nom="ARTE")
    arte.save()

    db_feed.populate("bouygues")

    bouquet = BouquetTv.objects.get(nom="bouygues")
    arte = Chaines.objects.get(nom="ARTE")
    bouquets_chaines = BouquetsChaines.objects.all()

    assert bouquet.nom == "bouygues"
    assert arte.bouquettv_set.all()[0].nom == "bouygues"
    assert bouquets_chaines[0].numero == 7


@mark.django_db
def test_populate_package_tnt(db_feed):

    france5 = Chaines(id_chaine="5_test", nom="FRANCE 5")
    france5.save()

    db_feed.populate("tnt")

    bouquet = BouquetTv.objects.get(nom="tnt")
    france5 = Chaines.objects.get(nom="FRANCE 5")
    bouquets_chaines = BouquetsChaines.objects.all()

    assert bouquet.nom == "tnt"
    assert france5.bouquettv_set.all()[0].nom == "tnt"
    assert bouquets_chaines[0].numero == 5


@mark.django_db
def test_bad_package_name(db_feed, capsys):

    france5 = Chaines(id_chaine="47.api-tel.programme-tv.net", nom="FRANCE 5")
    france5.save()

    db_feed.populate("freeeeeeeeee")

    out, err = capsys.readouterr()

    assert (
        out == "You have to choose one of these selected packages: free,"
        "sfr, bouygues or tnt\n"
    )


@mark.django_db
def test_package_already_in_DB(db_feed, capsys):

    tf1 = Chaines(id_chaine="1_test", nom="TF1")
    tf1.save()
    free = BouquetTv(nom="free")
    free.save()

    db_feed.populate("free")

    bouquet = BouquetTv.objects.get(nom="free")
    tf1 = Chaines.objects.get(nom="TF1")
    bouquets_chaines = BouquetsChaines.objects.all()

    assert bouquet.nom == "free"
    assert tf1.bouquettv_set.all()[0].nom == "free"
    assert bouquets_chaines[0].numero == 1


# @mark.django_db
# @patch('programmes.models.BouquetsChaines')
# def test_saving_failure(mock_bouquet, db_feed, capsys):

#     france5 = Chaines(id_chaine="47.api-tel.programme-tv.net", nom="FRANCE 5")
#     france5.save()

#     mock_bouquet.numero.return_value = "5"

#     db_feed.populate("free")

#     out, err = capsys.readouterr()

#     assert (
#         out
#         == "The data could not be inserted in the DB."
#     )
