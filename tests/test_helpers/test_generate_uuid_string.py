import pytest

from epub_image_extractor.helpers import generate_uuid_string

@pytest.fixture()
def uuid_size():
    return 36

@pytest.mark.usefixtures("uuid_size")
class TestGenerateUUIDString:
    def test_string_without_prefix(self, uuid_size):
        uuid = generate_uuid_string()   
        assert isinstance(uuid, str)
        assert len(uuid) == uuid_size

    def test_uuid_string_with_prefix(self, uuid_size):
        prefix = "test-prefix"
        uuid = generate_uuid_string(prefix)

        assert isinstance(uuid, str)
        assert len(uuid) == (len(prefix) + uuid_size)

    def test_prefix_not_is_string(self):
        prefix = 12345
        uuid = generate_uuid_string(prefix)

        assert isinstance(uuid, str)
        assert len(uuid) == (len(str(prefix)) + 36)