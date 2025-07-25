import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

def test_shorten_and_redirect(client):
    # Shorten a valid URL
    response = client.post('/api/shorten', json={"url": "https://example.com/abc"})
    assert response.status_code == 201
    data = response.get_json()
    assert 'short_code' in data
    assert 'short_url' in data
    code = data['short_code']

    # Redirect works and increments click count
    response = client.get(f'/{code}', follow_redirects=False)
    assert response.status_code == 302
    assert response.headers['Location'] == 'https://example.com/abc'

    # Analytics endpoint returns correct info
    response = client.get(f'/api/stats/{code}')
    assert response.status_code == 200
    stats = response.get_json()
    assert stats['url'] == 'https://example.com/abc'
    assert stats['clicks'] == 1
    assert 'created_at' in stats

def test_invalid_url(client):
    response = client.post('/api/shorten', json={"url": "not-a-url"})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_missing_url_field(client):
    response = client.post('/api/shorten', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_404_on_unknown_code(client):
    response = client.get('/api/stats/unknown123')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    response = client.get('/unknown123')
    assert response.status_code == 404