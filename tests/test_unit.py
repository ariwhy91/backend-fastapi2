# tests/test_unit.py
import pytest
from pydantic import ValidationError

import schemas


def test_order_create_menolak_data_tidak_lengkap():
    """OrderCreate wajib punya field produk, jumlah, dan total."""
    with pytest.raises(ValidationError):
        schemas.OrderCreate(produk="Mouse")  # jumlah dan total sengaja dihilangkan


# tests/test_unit.py (lanjutan)
from security import hash_password, verify_password


def test_password_hash_dan_verify_konsisten():
    """Password asli harus lolos verifikasi terhadap hash-nya sendiri,
    dan password yang salah harus ditolak."""
    plain = "rahasia123"
    hashed = hash_password(plain)

    assert hashed != plain
    assert verify_password(plain, hashed) is True
    assert verify_password("password_salah", hashed) is False