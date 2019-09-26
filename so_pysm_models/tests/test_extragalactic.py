import numpy as np
import healpy as hp
from pysm import units as u

from .. import utils
from .. import WebSkyCIB, WebSkySZ


def test_cib(tmp_path):

    nside = 4
    shape = hp.nside2npix(nside)

    path = tmp_path / "websky" / "0.3" / "512"
    path.mkdir(parents=True)
    hp.write_map(path / "cib_0094.fits", np.zeros(shape, dtype=np.float32))
    hp.write_map(path / "cib_0100.fits", np.ones(shape, dtype=np.float32))

    interp = WebSkyCIB(
        "0.3", "uK_RJ", nside, interpolation_kind="linear", local_folder=tmp_path
    )

    interpolated_map = interp.get_emission(97 * u.GHz)
    np.testing.assert_allclose(
        np.interp(97, [94, 100], [0, 1]) * np.ones((1, shape)) * u.uK_RJ,
        interpolated_map,
    )


def test_ksz(tmp_path, monkeypatch):

    monkeypatch.setattr(utils, "PREDEFINED_DATA_FOLDERS", {"C":[str(tmp_path)]})
    nside = 4
    shape = hp.nside2npix(nside)

    path = tmp_path / "websky" / "0.3" / "512"
    path.mkdir(parents=True)
    hp.write_map(path / "ksz.fits", np.ones(shape, dtype=np.float32))

    ksz = WebSkySZ("0.3", sz_type="kinetic", nside=nside)

    ksz_map = ksz.get_emission(100 * u.GHz)
    np.testing.assert_allclose(
        np.ones(ksz_map[0].shape) * 0.7772276 * u.uK_RJ, ksz_map[0], rtol=1e-4
    )
    np.testing.assert_allclose(np.zeros((2, len(ksz_map[0]))) * u.uK_RJ, ksz_map[1:])


def test_tsz(tmp_path, monkeypatch):

    monkeypatch.setattr(utils, "PREDEFINED_DATA_FOLDERS", {"C":[str(tmp_path)]})
    nside = 4
    shape = hp.nside2npix(nside)

    path = tmp_path / "websky" / "0.3" / "512"
    path.mkdir(parents=True)
    hp.write_map(path / "tsz.fits", np.ones(shape, dtype=np.float32) * 1e-6)

    tsz = WebSkySZ("0.3", sz_type="thermal", nside=nside)

    tsz_map = tsz.get_emission(100 * u.GHz)
    np.testing.assert_allclose(
        np.ones(len(tsz_map[0])) * -3.193671 * u.uK_RJ, tsz_map[0], rtol=1e-4
    )
    np.testing.assert_allclose(np.zeros((2, len(tsz_map[0]))) * u.uK_RJ, tsz_map[1:])
