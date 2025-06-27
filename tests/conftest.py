import os
import json
import tempfile
import shutil
from pathlib import Path
from typing import Generator, Dict, Any

import pytest
import numpy as np
from PIL import Image


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_image(temp_dir: Path) -> Path:
    """Create a sample image for testing."""
    image_path = temp_dir / "test_image.jpg"
    image = Image.new('RGB', (100, 100), color='white')
    image.save(image_path)
    return image_path


@pytest.fixture
def sample_detection_json(temp_dir: Path) -> Path:
    """Create a sample detection JSON file."""
    json_path = temp_dir / "test_detection.json"
    data = {
        "test_image.jpg": [
            {
                "points": [[10, 10], [90, 10], [90, 90], [10, 90]],
                "confidence": 0.95,
                "text": "sample text"
            }
        ]
    }
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return json_path


@pytest.fixture
def sample_recognition_txt(temp_dir: Path) -> Path:
    """Create a sample recognition text file."""
    txt_path = temp_dir / "test_recognition.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("test_image.jpg\tsample text\n")
        f.write("test_image2.jpg\tanother text\n")
    return txt_path


@pytest.fixture
def mock_dataset_config() -> Dict[str, Any]:
    """Return a mock dataset configuration."""
    return {
        "name": "test_dataset",
        "data_root": "/tmp/test_data",
        "label_file": "labels.json",
        "image_dir": "images",
        "batch_size": 32,
        "num_workers": 4
    }


@pytest.fixture
def sample_points() -> np.ndarray:
    """Create sample polygon points."""
    return np.array([
        [10, 10],
        [90, 10],
        [90, 90],
        [10, 90]
    ], dtype=np.float32)


@pytest.fixture
def mock_lmdb_env(temp_dir: Path, monkeypatch):
    """Mock LMDB environment for testing."""
    import lmdb
    
    lmdb_path = temp_dir / "test.lmdb"
    env = lmdb.open(str(lmdb_path), map_size=10485760)
    
    with env.begin(write=True) as txn:
        txn.put(b'num-samples', b'2')
        txn.put(b'image_0000000000', b'fake_image_data_1')
        txn.put(b'label_0000000000', b'test label 1')
        txn.put(b'image_0000000001', b'fake_image_data_2')
        txn.put(b'label_0000000001', b'test label 2')
    
    return env


@pytest.fixture(autouse=True)
def reset_modules():
    """Reset module imports between tests to avoid side effects."""
    import sys
    modules_to_reset = [m for m in sys.modules if m.startswith(('convert', 'dataset'))]
    for module in modules_to_reset:
        sys.modules.pop(module, None)


@pytest.fixture
def capture_stdout(monkeypatch):
    """Capture stdout for testing print statements."""
    import io
    import sys
    
    captured_output = io.StringIO()
    monkeypatch.setattr(sys, 'stdout', captured_output)
    return captured_output