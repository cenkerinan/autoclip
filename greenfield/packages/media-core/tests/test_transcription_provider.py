import pytest

from project_director_media import TranscriptionProviderRegistry


class FakeProvider:
    name = "fake"
    model = "v1"

    def transcribe(self, request):
        raise NotImplementedError


def test_registry_rejects_duplicate_provider_names() -> None:
    registry = TranscriptionProviderRegistry()
    registry.register(FakeProvider())
    with pytest.raises(ValueError):
        registry.register(FakeProvider())


def test_registry_lists_registered_providers() -> None:
    registry = TranscriptionProviderRegistry()
    registry.register(FakeProvider())
    assert registry.names() == ("fake",)
