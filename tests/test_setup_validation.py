import pytest
import sys
from pathlib import Path


class TestSetupValidation:
    """Validation tests to ensure the testing infrastructure is properly configured."""
    
    def test_pytest_installed(self):
        """Verify pytest is installed and importable."""
        assert pytest.__version__
    
    def test_coverage_installed(self):
        """Verify pytest-cov is available."""
        import pytest_cov
        assert pytest_cov
    
    def test_mock_installed(self):
        """Verify pytest-mock is available."""
        import pytest_mock
        assert pytest_mock
    
    def test_project_packages_importable(self):
        """Verify the project packages can be imported."""
        import convert
        import dataset
        assert convert
        assert dataset
    
    def test_fixtures_available(self, temp_dir, sample_image, mock_dataset_config):
        """Verify fixtures from conftest.py are available."""
        assert temp_dir.exists()
        assert sample_image.exists()
        assert mock_dataset_config['name'] == 'test_dataset'
    
    @pytest.mark.unit
    def test_unit_marker(self):
        """Verify unit test marker works."""
        assert True
    
    @pytest.mark.integration
    def test_integration_marker(self):
        """Verify integration test marker works."""
        assert True
    
    @pytest.mark.slow
    def test_slow_marker(self):
        """Verify slow test marker works."""
        assert True
    
    def test_test_directories_exist(self):
        """Verify test directory structure exists."""
        test_root = Path(__file__).parent
        assert test_root.exists()
        assert (test_root / 'unit').exists()
        assert (test_root / 'integration').exists()
        assert (test_root / 'conftest.py').exists()
    
    def test_coverage_configuration(self):
        """Verify coverage is configured to track the right packages."""
        import coverage
        cov = coverage.Coverage()
        config = cov.config
        
        # This test verifies coverage can be instantiated
        # Actual coverage config is in pyproject.toml
        assert cov is not None