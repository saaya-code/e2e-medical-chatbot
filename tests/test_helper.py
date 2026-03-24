import os
import pytest
from unittest.mock import patch, MagicMock


def test_get_or_create_vectorstore_raises_when_pdf_missing(tmp_path):
    from src.helper import get_or_create_vectorstore

    data_path = str(tmp_path / "data")
    chroma_path = str(tmp_path / "chroma_db")
    os.makedirs(data_path)

    with patch("src.helper.chromadb.PersistentClient") as mock_client:
        mock_client.return_value.get_collection.side_effect = Exception("not found")
        with pytest.raises(FileNotFoundError, match="Medical_book.pdf not found in data/. Place the PDF there and restart."):
            get_or_create_vectorstore(data_path, chroma_path, "test_col")


def test_get_or_create_vectorstore_ingests_when_count_is_zero(tmp_path):
    from src.helper import get_or_create_vectorstore

    data_path = str(tmp_path / "data")
    chroma_path = str(tmp_path / "chroma_db")
    os.makedirs(data_path)
    (tmp_path / "data" / "Medical_book.pdf").write_bytes(b"%PDF-1.4 fake")

    mock_collection = MagicMock()
    mock_collection.count.return_value = 0

    with patch("src.helper.chromadb.PersistentClient") as mock_client, \
         patch("src.helper.Chroma") as mock_chroma, \
         patch("src.helper.load_pdf_file") as mock_load, \
         patch("src.helper.text_split") as mock_split, \
         patch("src.helper.get_embeddings") as mock_emb:
        mock_client.return_value.get_collection.return_value = mock_collection
        mock_load.return_value = [MagicMock()]
        mock_split.return_value = [MagicMock()]
        mock_chroma.from_documents.return_value = MagicMock()
        mock_emb.return_value = MagicMock()

        get_or_create_vectorstore(data_path, chroma_path, "test_col")

        mock_chroma.from_documents.assert_called_once()


def test_get_or_create_vectorstore_loads_when_populated(tmp_path):
    from src.helper import get_or_create_vectorstore
    from langchain_chroma import Chroma

    data_path = str(tmp_path / "data")
    chroma_path = str(tmp_path / "chroma_db")
    os.makedirs(data_path)

    mock_collection = MagicMock()
    mock_collection.count.return_value = 10

    with patch("src.helper.chromadb.PersistentClient") as mock_client, \
         patch("src.helper.Chroma") as mock_chroma, \
         patch("src.helper.get_embeddings") as mock_emb:
        mock_client.return_value.get_collection.return_value = mock_collection
        mock_chroma.return_value = MagicMock(spec=Chroma)
        mock_emb.return_value = MagicMock()

        result = get_or_create_vectorstore(data_path, chroma_path, "test_col")

        mock_chroma.assert_called_once()
        assert result is not None
