"""Tests for obsidian-sync.py"""

import pytest
import importlib.util
from pathlib import Path

# Import the actual module
scripts_path = Path(__file__).parent.parent / 'scripts'
spec = importlib.util.spec_from_file_location("obsidian_sync", scripts_path / "obsidian-sync.py")
obsidian_sync_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(obsidian_sync_module)
ObsidianSync = obsidian_sync_module.ObsidianSync


class TestObsidianSync:
    """Test cases for ObsidianSync class"""

    @pytest.fixture
    def sync(self, tmp_path):
        """Create ObsidianSync instance with temp vault"""
        return ObsidianSync(vault_path=str(tmp_path))

    def test_init_creates_vault_structure(self, sync, tmp_path):
        """Test that init() creates the required vault structure"""
        sync.init()

        # Check vault_path exists
        assert sync.vault_path.exists(), "Vault path should exist"
        assert sync.vault_path.is_dir(), "Vault path should be a directory"

    def test_add_note_creates_file(self, sync, tmp_path):
        """Test that add_note creates a note file"""
        sync.init()

        result = sync.add_note('test-note', '# Test Note\n\nContent here')

        assert result is not None
        assert Path(result).exists(), "Note file should be created"

    def test_search_notes_finds_content(self, sync, tmp_path):
        """Test that search_notes finds notes by content"""
        sync.init()
        sync.add_note('search-test', '# Search Target\n\nThis contains search terms.')

        results = sync.search_notes('Search')

        assert len(results) >= 1
        assert any('search' in r['type'].lower() or 'search' in r['path'].lower()
                   for r in results), "Should find note with 'search' term"

    def test_search_notes_returns_list(self, sync, tmp_path):
        """Test that search_notes returns a list"""
        sync.init()
        sync.add_note('another-note', '# Another Note\n\nContent.')

        results = sync.search_notes('Another')

        assert isinstance(results, list), "Results should be a list"

    def test_index_returns_dict(self, sync, tmp_path):
        """Test that index returns a dictionary"""
        sync.init()

        index = sync.index

        assert isinstance(index, dict), "Index should be a dictionary"


class TestObsidianSyncIntegration:
    """Integration tests for ObsidianSync"""

    @pytest.fixture
    def sync(self, tmp_path):
        """Create ObsidianSync instance with temp vault"""
        return ObsidianSync(vault_path=str(tmp_path))

    def test_full_workflow(self, sync, tmp_path):
        """Test complete workflow: init -> add note -> search -> backup"""
        # Initialize vault
        sync.init()
        assert sync.vault_path.exists()

        # Add multiple notes
        note1 = sync.add_note('note-one', '# First Note\n\nContent for note one.')
        note2 = sync.add_note('note-two', '# Second Note\n\nContent for note two.')

        assert Path(note1).exists()
        assert Path(note2).exists()

        # Search for content
        results = sync.search_notes('First')
        assert len(results) >= 1

        # Get index
        index = sync.index
        assert isinstance(index, dict)

    def test_daily_note_generation(self, sync, tmp_path):
        """Test daily note generation"""
        sync.init()

        daily_note = sync.generate_daily_note()

        assert daily_note is not None
        assert Path(daily_note).exists() or 'daily' in str(daily_note).lower()

    def test_export_index(self, sync, tmp_path):
        """Test index export functionality"""
        sync.init()
        sync.add_note('export-test', '# Export Test\n\nContent for export test.')

        exported = sync.export_index()

        assert exported is not None, "Export should return a result"


class TestObsidianSyncEdgeCases:
    """Edge case tests for ObsidianSync"""

    @pytest.fixture
    def sync(self, tmp_path):
        """Create ObsidianSync instance with temp vault"""
        return ObsidianSync(vault_path=str(tmp_path))

    def test_search_with_no_notes(self, sync, tmp_path):
        """Test search returns empty list when no notes exist"""
        sync.init()

        results = sync.search_notes('nonexistent')

        assert isinstance(results, list), "Results should be a list"
        assert len(results) == 0, "Should return empty list for no matches"

    def test_add_note_with_special_characters(self, sync, tmp_path):
        """Test adding notes with special characters in title"""
        sync.init()

        result = sync.add_note('note-with-dashes', '# Special Chars\n\nContent.')

        assert result is not None

    def test_empty_content_note(self, sync, tmp_path):
        """Test adding note with minimal content"""
        sync.init()

        result = sync.add_note('empty-test', '')

        assert result is not None