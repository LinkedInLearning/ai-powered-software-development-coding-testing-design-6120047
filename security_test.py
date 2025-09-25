import pytest
from security import create_profile_html

def test_create_profile_html_basic():
    html_output = create_profile_html("Alice", 30, "Wonderland")
    assert "<h1>Alice</h1>" in html_output
    assert "<p>Age: 30</p>" in html_output
    assert "<p>Location: Wonderland</p>" in html_output

def test_create_profile_html_html_injection_name():
    malicious_name = '<script>alert("hack")</script>'
    html_output = create_profile_html(malicious_name, 25, "Paris")
    # Ensure the script tag is escaped
    assert "&lt;script&gt;alert(&quot;hack&quot;)&lt;/script&gt;" in html_output
    assert "<script>" not in html_output

def test_create_profile_html_html_injection_location():
    malicious_location = '<img src=x onerror=alert(1)>'
    html_output = create_profile_html("Bob", 40, malicious_location)
    # Ensure the img tag is escaped
    assert "&lt;img src=x onerror=alert(1)&gt;" in html_output
    assert "<img" not in html_output

def test_create_profile_html_empty_strings():
    html_output = create_profile_html("", 0, "")
    assert "<h1></h1>" in html_output
    assert "<p>Age: 0</p>" in html_output
    assert "<p>Location: </p>" in html_output

def test_create_profile_html_special_characters():
    name = 'Tom & Jerry <b>'
    location = 'New <York> & LA'
    html_output = create_profile_html(name, 5, location)
    assert "Tom &amp; Jerry &lt;b&gt;" in html_output
    assert "New &lt;York&gt; &amp; LA" in html_output