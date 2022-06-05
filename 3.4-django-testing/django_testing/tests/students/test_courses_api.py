import pytest
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND)


@pytest.mark.django_db
def test_retrieve_one(api_client, course_factory):
    """
    Проверка получения одного курса (retrieve-логика).
        * создаем курс через фабрику
        * строим урл и делаем запрос через тестовый клиент
        * проверяем, что вернулся именно тот курс, который запрашивали
    """
    courses = course_factory(_quantity=1)
    course = courses[0]
    url = reverse("courses-detail", kwargs={'pk': course.id})
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert resp_json["name"] == course.name


@pytest.mark.django_db
def test_get_list(api_client, course_factory):
    """
    Проверка получения списка курсов (list-логика).
        Аналогично – сначала вызываем фабрики,
        затем делаем запрос и проверяем результат.
    """
    courses = course_factory(_quantity=3)
    url = reverse("courses-list")
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert len(resp_json) == 3
    assert resp_json[0]["name"] == courses[0].name


@pytest.mark.django_db
def test_filter_id(api_client, course_factory):
    """
    Проверка фильтрации списка курсов по id.
        Создаем курсы через фабрику, передать id одного курса в фильтр,
        проверить результат запроса с фильтром
    """
    courses = course_factory(_quantity=3)
    course = courses[0]
    url = reverse("courses-list")
    resp = api_client.get(url, data={'id': course.id})
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert resp_json[0]["name"] == course.name


@pytest.mark.django_db
def test_filter_name(api_client, course_factory):
    """
    Проверка фильтрации списка курсов по name.
    """
    courses = course_factory(_quantity=3)
    course = courses[0]
    url = reverse("courses-list")
    resp = api_client.get(url, data={'name': course.name})
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert resp_json[0]["name"] == course.name


@pytest.mark.django_db
def test_create(api_client):
    """
    Тест успешного создания курса.
        Здесь фабрика не нужна, готовим JSON-данные и создаем курс.
    """
    url = reverse("courses-list")
    data = {'name': 'Test'}
    resp = api_client.post(url, data=data)
    assert resp.status_code == HTTP_201_CREATED
    resp_json = resp.json()
    assert resp_json["name"] == data["name"]


@pytest.mark.django_db
def test_update(api_client, course_factory):
    """
    Тест успешного обновления курса.
        Сначала через фабрику создаем, потом обновляем JSON-данными.
    """
    courses = course_factory(_quantity=1)
    course = courses[0]
    url = reverse("courses-detail", kwargs={'pk': course.id})
    data = {'name': 'New name'}
    resp = api_client.patch(url, data=data)
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert resp_json["name"] == data["name"]


@pytest.mark.django_db
def test_destroy(api_client, course_factory):
    """
    Тест успешного удаления курса
    """
    courses = course_factory(_quantity=1)
    course = courses[0]
    url = reverse("courses-detail", kwargs={'pk': course.id})
    resp = api_client.delete(url)
    assert resp.status_code == HTTP_204_NO_CONTENT

    resp = api_client.get(url)
    assert resp.status_code == HTTP_404_NOT_FOUND
