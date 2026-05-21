"""Tests for obsidian-sync.py"""

import pytest
from pathlib import Path
import tempfile
import shutil

# Import the module
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
from obsidian_sync import ObsidianSync


class TestObsidianSync:
    """Test cases for ObsidianSync class"""

    @pytest.fixture
    def temp_vault(self, tmp_path):
        """Create a temporary vault for testing"""
        vault_path = tmp_path / "test-vault"
        vault_path.mkdir()
        return vault_path

    @pytest.fixture
    def sync(self, temp_vault):
        """Create ObsidianSync instance with temp vault"""
        return ObsidianSync(vault_path=str(temp_vault))

    def test_init_vault_creates_directories(self, sync, temp_vault):
        """Test that init_vault creates all required directories"""
        sync.init_vault()

        expected_dirs = ['00-项目', '01-用户访谈', '02-洞察笔记', '03-需求池', '04-报告']
        for dir_name in expected_dirs:
            assert (temp_vault / dir_name).exists(), f"Directory {dir_name} should exist"

    def test_list_files_returns_empty_for_empty_dir(self, sync):
        """Test list_files returns empty list for empty directory"""
        files = sync.list_files('interviews')
        assert files == []

    def test_get_stats_returns_directory_counts(self, sync):
        """Test get_stats returns correct count per directory"""
        stats = sync.get_stats()

        assert 'project' in stats
        assert 'interviews' in stats
        assert 'insights' in stats
        assert 'requirements' in stats
        assert 'reports' in stats

    def test_generate_id_is_consistent(self, sync):
        """Test that generate_id returns consistent results for same input"""
        content = "test content"
        id1 = sync.generate_id(content)
        id2 = sync.generate_id(content)
        assert id1 == id2

    def test_generate_id_differs_for_different_content(self, sync):
        """Test that generate_id returns different IDs for different content"""
        id1 = sync.generate_id("content A")
        id2 = sync.generate_id("content B")
        assert id1 != id2


class TestObsidianSyncIntegration:
    """Integration tests for ObsidianSync"""

    @pytest.fixture
    def temp_vault(self, tmp_path):
        """Create a temporary vault for testing"""
        vault_path = tmp_path / "test-vault"
        vault_path.mkdir()
        return vault_path

    @pytest.fixture
    def sync(self, temp_vault):
        """Create ObsidianSync instance with temp vault"""
        return ObsidianSync(vault_path=str(temp_vault))

    def test_create_and_read_note(self, sync, temp_vault):
        """Test creating and reading a note"""
        sync.init_vault()

        content = "# Test Note\n\nThis is a test."
        frontmatter = {"note_id": "test-001", "tags": ["test"]}

        file_path = sync.create_note('project', 'test-note', content, frontmatter)

        assert file_path.exists()

        # Read it back
        note = sync.read_note(file_path)
        assert note['filename'] == 'test-note.md'
        assert note['frontmatter']['note_id'] == 'test-001'
        assert 'Test Note' in note['content']

    def test_create_multiple_notes(self, sync, temp_vault):
        """Test creating multiple notes"""
        sync.init_vault()

        notes = [
            ('interviews', 'interview-1', '# Interview 1'),
            ('interviews', 'interview-2', '# Interview 2'),
            ('insights', 'insight-1', '# Insight 1'),
        ]

        for dir_name, filename, content in notes:
            sync.create_note(dir_name, filename, content)

        # Verify counts
        assert len(sync.list_files('interviews')) == 2
        assert len(sync.list_files('insights')) == 1
