import sys
import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def client():
    sys.modules.pop("app", None)
    with patch("src.helper.get_or_create_vectorstore") as mock_vs, \
         patch("langchain_google_genai.ChatGoogleGenerativeAI"), \
         patch("langchain.chains.create_retrieval_chain") as mock_chain, \
         patch("langchain.chains.combine_documents.create_stuff_documents_chain"):
        mock_vs.return_value = MagicMock()
        mock_rag = MagicMock()
        mock_rag.invoke.return_value = {"answer": "Test answer"}
        mock_chain.return_value = mock_rag

        import app as app_module
        app_module.app.config["TESTING"] = True
        with app_module.app.test_client() as c:
            yield c


def test_index_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_get_returns_400_on_missing_msg(client):
    response = client.post("/get", data={})
    assert response.status_code == 400


def test_get_returns_400_on_empty_msg(client):
    response = client.post("/get", data={"msg": "   "})
    assert response.status_code == 400


def test_get_rejects_get_method(client):
    response = client.get("/get")
    assert response.status_code == 405
