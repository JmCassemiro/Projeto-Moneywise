def test_app_context_and_home_page(database, client):
    response = client.get("/")

    assert response.status_code == 200


def test_authenticated_client_opens_protected_transactions_page(
    database,
    authenticated_client,
):
    client, _user = authenticated_client()

    response = client.get("/transactions/")

    assert response.status_code == 200
