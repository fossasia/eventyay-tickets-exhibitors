import re

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from django.utils import timezone
from exhibition.models import Lead

from exhibition.models import ExhibitorInfo


@pytest.mark.django_db
def test_create_exhibitor_info(event):
    # CREATE: Simulate an image upload and create an exhibitor
    logo = SimpleUploadedFile("test_logo.jpg", b"file_content", content_type="image/jpeg")

    exhibitor = ExhibitorInfo.objects.create(
        event=event,
        name="Test Exhibitor",
        description="This is a test exhibitor",
        url="http://testexhibitor.com",
        email="test@example.com",
        logo=logo,
        lead_scanning_enabled=True
    )

    # Verify the exhibitor was created and the fields are correct
    assert exhibitor.name == "Test Exhibitor"
    assert exhibitor.description == "This is a test exhibitor"
    assert exhibitor.url == "http://testexhibitor.com"
    assert exhibitor.email == "test@example.com"
    assert re.fullmatch(
        r"exhibitors/logos/Test Exhibitor/test_logo(?:_[A-Za-z0-9]{7})?\.jpg",
        exhibitor.logo.name,
    )
    assert exhibitor.lead_scanning_enabled is True


@pytest.mark.django_db
def test_read_exhibitor_info(event):
    # CREATE an exhibitor first to test reading
    logo = SimpleUploadedFile("test_logo.jpg", b"file_content", content_type="image/jpeg")
    exhibitor = ExhibitorInfo.objects.create(
        event=event,
        name="Test Exhibitor",
        description="This is a test exhibitor",
        url="http://testexhibitor.com",
        email="test@example.com",
        logo=logo,
        lead_scanning_enabled=True
    )

    # READ: Fetch the exhibitor from the database and verify fields
    exhibitor_from_db = ExhibitorInfo.objects.get(id=exhibitor.id)
    assert exhibitor_from_db.name == "Test Exhibitor"
    assert exhibitor_from_db.description == "This is a test exhibitor"
    assert exhibitor_from_db.url == "http://testexhibitor.com"
    assert exhibitor_from_db.email == "test@example.com"
    assert exhibitor_from_db.lead_scanning_enabled is True


@pytest.mark.django_db
def test_update_exhibitor_info(event):
    # CREATE an exhibitor first to test updating
    logo = SimpleUploadedFile("test_logo.jpg", b"file_content", content_type="image/jpeg")
    exhibitor = ExhibitorInfo.objects.create(
        event=event,
        name="Test Exhibitor",
        description="This is a test exhibitor",
        url="http://testexhibitor.com",
        email="test@example.com",
        logo=logo,
        lead_scanning_enabled=True
    )

    # UPDATE: Modify some fields and save the changes
    exhibitor.name = "Updated Exhibitor"
    exhibitor.description = "This is an updated description"
    exhibitor.lead_scanning_enabled = False
    exhibitor.save()

    # Verify the updated fields
    updated_exhibitor = ExhibitorInfo.objects.get(id=exhibitor.id)
    assert updated_exhibitor.name == "Updated Exhibitor"
    assert updated_exhibitor.description == "This is an updated description"
    assert updated_exhibitor.lead_scanning_enabled is False


@pytest.mark.django_db
def test_delete_exhibitor_info(event):
    # CREATE an exhibitor first to test deleting
    logo = SimpleUploadedFile("test_logo.jpg", b"file_content", content_type="image/jpeg")
    exhibitor = ExhibitorInfo.objects.create(
        event=event,
        name="Test Exhibitor",
        description="This is a test exhibitor",
        url="http://testexhibitor.com",
        email="test@example.com",
        logo=logo,
        lead_scanning_enabled=True
    )

    # DELETE: Delete the exhibitor and verify it no longer exists
    exhibitor_id = exhibitor.id
    exhibitor.delete()

    with pytest.raises(ExhibitorInfo.DoesNotExist):
        ExhibitorInfo.objects.get(id=exhibitor_id)


@pytest.mark.django_db
def test_lead_create_scanned_is_server_time(api_client, exhibitor, order_position):
    # 'scanned' value sent by client should be ignored.
    # Server must always set scan time via timezone.now().
    before = timezone.now()
    response = api_client.post(
        '/api/leads/',
        data={
            'lead': order_position.pseudonymization_id,
            'scan_type': 'qr',
            'device_name': 'test_device',
            'scanned': '2000-01-01T00:00:00Z',  # 과거 시간 보내도 무시되어야 함
        },
        HTTP_EXHIBITOR=exhibitor.key
    )
    after = timezone.now()

    assert response.status_code == 201
    lead = Lead.objects.get(id=response.data['lead_id'])
    assert before <= lead.scanned <= after  # 서버 시간으로 저장됐는지 확인


@pytest.mark.django_db
def test_lead_create_open_event_string_false(api_client, exhibitor, order_position):
    # String "false" must be treated as boolean False.
    response = api_client.post(
        '/api/leads/',
        data={
            'lead': order_position.secret,
            'scan_type': 'qr',
            'device_name': 'test_device',
            'open_event': 'false',  # 문자열로 보내도 False 처리되어야 함
        },
        HTTP_EXHIBITOR=exhibitor.key
    )
    # open_event=False면 pseudonymization_id로 조회해야 함
    # secret으로 보냈으니 404가 맞음 (잘못된 lookup)
    assert response.status_code == 404
