def test_informations_page_renders(database, client):
    response = client.get("/informations")

    assert response.status_code == 200
    assert b"MoneyWise" in response.data


def test_contact_page_renders_form(database, client):
    response = client.get("/contact")

    assert response.status_code == 200
    assert b"form-contact" in response.data


def test_contact_post_redirects_home_when_message_is_sent(
    database,
    client,
    mocker,
):
    send_contact = mocker.patch("app.home.routes.ContactService.send_contact_message")

    response = client.post(
        "/contact",
        data={
            "name": "Person",
            "email": "person@example.com",
            "phone": "123",
            "message": "Hello",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")
    send_contact.assert_called_once_with(
        name="Person",
        email="person@example.com",
        phone="123",
        message="Hello",
    )


def test_contact_post_redirects_back_when_message_fails(
    database,
    client,
    mocker,
):
    mocker.patch(
        "app.home.routes.ContactService.send_contact_message",
        side_effect=RuntimeError("mail unavailable"),
    )

    response = client.post(
        "/contact",
        data={
            "name": "Person",
            "email": "person@example.com",
            "phone": "123",
            "message": "Hello",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/contact")


def _dashboard_payload():
    return {
        "receitas": 100.0,
        "despesas": 40.0,
        "total": 60.0,
        "meses": ["2026-05"],
        "receitas_mensais": [100.0],
        "despesas_mensais": [40.0],
        "saldos_mensais": [60.0],
        "receitas_por_categoria": [("Work", 100.0)],
        "despesas_por_categoria": [("Casa", 40.0)],
        "top5Despesas": [("Rent", 40.0, "Casa")],
    }


def test_statistics_page_renders_dashboard(
    database,
    authenticated_client,
    mocker,
):
    client, user = authenticated_client()
    dashboard = mocker.patch(
        "app.statistics.routes.StatisticsService.dashboard",
        return_value=_dashboard_payload(),
    )

    response = client.get("/statistics/")

    assert response.status_code == 200
    assert b"100.00" in response.data
    dashboard.assert_called_once_with(str(user.id))


def test_statistics_page_redirects_when_dashboard_fails(
    database,
    authenticated_client,
    mocker,
):
    client, _user = authenticated_client()
    mocker.patch(
        "app.statistics.routes.StatisticsService.dashboard",
        side_effect=RuntimeError("dashboard failed"),
    )

    response = client.get("/statistics/", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/transactions/")
