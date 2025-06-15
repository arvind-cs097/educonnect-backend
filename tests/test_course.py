def test_get_courses(client, sample_courses):
    response = client.get("/api/courses")
    assert response.status_code == 200

    data = response.get_json()
    assert data["status"] == "success"
    assert isinstance(data["data"], list)

    course_names = [course["title"] for course in data["data"]]
    assert "Math 101" in course_names
    assert "Science 101" in course_names
