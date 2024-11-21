import pytest
from unittest.mock import patch, MagicMock
from src.app_settings import IntentClassificationSettings
from src.services.intent_classifier import IntentClassifierService


@pytest.fixture
def mock_service():
    # Create a mock for IntentClassificationSettings
    settings = IntentClassificationSettings(
        candidate_labels={"sports": 0.5, "politics": 0.5, "technology": 0.5},
        threshold=0.5,
    )

    # Mock the load_pipeline method to avoid using the real model
    with patch(
        "src.services.intent_classifier.IntentClassifierService.load_pipeline"
    ) as mock_load_pipeline:
        mock_pipeline = MagicMock()
        mock_pipeline.return_value = {"sports": 0.8, "technology": 0.2}
        mock_load_pipeline.return_value = mock_pipeline
        service = IntentClassifierService(settings)
        yield service


@pytest.mark.asyncio
async def test_classify(mock_service):
    # Arrange
    mock_service.classifier = MagicMock(return_value={"sports": 0.8, "technology": 0.2})

    # Act
    result = await mock_service.classify("Is this a sports news?")

    # Assert
    assert result == {"sports": 0.8, "technology": 0.2}


@pytest.mark.asyncio
async def test_is_text_pertinent_with_weighted_average(mock_service):
    # Arrange
    mock_service.classifier = MagicMock(return_value={"sports": 0.8, "technology": 0.6})
    reference_labels = {
        "sports": 1.0,  # Weight of 1.0
        "politics": 2.0,  # Weight of 2.0 (not in classify result)
        "technology": 0.5,  # Weight of 0.5
    }

    # Act
    is_pertinent, classes = await mock_service.is_text_pertinent(
        "This is a sports technology article.", reference_labels
    )

    # Assert
    weighted_score_sum = (0.8 * 1.0) + (0.6 * 0.5)
    total_weight = 1.0 + 0.5
    weighted_average_score = weighted_score_sum / total_weight

    assert is_pertinent == (weighted_average_score > mock_service.settings.threshold)
    assert classes == {"sports": 0.8, "technology": 0.6}


@pytest.mark.asyncio
async def test_is_text_pertinent_below_threshold(mock_service):
    # Arrange
    mock_service.classifier = MagicMock(return_value={"sports": 0.4, "technology": 0.3})
    reference_labels = {"sports": 1.0, "technology": 1.0}

    # Act
    is_pertinent, classes = await mock_service.is_text_pertinent(
        "Is this sports or technology?", reference_labels
    )

    # Assert
    weighted_average_score = (0.4 * 1.0 + 0.3 * 1.0) / 2
    assert is_pertinent == (weighted_average_score > mock_service.settings.threshold)
    assert classes == {"sports": 0.4, "technology": 0.3}


@pytest.mark.asyncio
async def test_is_text_pertinent_no_classes(mock_service):
    # Arrange
    mock_service.classifier = MagicMock(return_value={})
    reference_labels = {"sports": 1.0, "technology": 1.0}

    # Act
    is_pertinent, classes = await mock_service.is_text_pertinent(
        "Unrelated text", reference_labels
    )

    # Assert
    assert not is_pertinent
    assert classes == {}
