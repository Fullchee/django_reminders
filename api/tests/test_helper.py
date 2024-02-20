from api.services.youtube import get_youtube_id


def test_get_youtube_id():
    assert (
        get_youtube_id("https://www.youtube.com/watch?v=CPLdltN7wgE") == "CPLdltN7wgE"
    )
    assert (
        get_youtube_id(
            "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=video&cd=&cad=rja&uact=8&ved=2ahUKEwjP9ZKV8"
            "YL1AhWKk4kEHQfcCskQtwJ6BAhaEAI&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DGj0LqmNsrCc&usg=AOvV"
            "aw3RWof_KDlatC6iRBghDUbI"
        )
        == "Gj0LqmNsrCc"
    )

    assert (
        get_youtube_id(
            "https://www.google.com/url?q=https://m.youtube.com/watch%3Fv%3Dw7ejDZ8SWv8&sa=U&ved=2ahUKE"
            "wjp0fPfgZz3AhURHc0KHTAQCgEQtwJ6BAgFEAE&usg=AOvVaw1SQCih9kDQNLVV0H_s_Css"
        )
        == "w7ejDZ8SWv8"
    )
    assert (
        get_youtube_id(
            "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=video&cd=&ved=2ahUKEwihuNvmgZz3AhWxAZ0JHeWZDYE"
            "QtwJ6BAgiEAI&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Dw7ejDZ8SWv8&usg=AOvVaw1Z-eFIXGuWprmOxM5qj9UN"
        )
        == "w7ejDZ8SWv8"
    )
