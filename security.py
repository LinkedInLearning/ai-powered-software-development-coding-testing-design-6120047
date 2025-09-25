import html

def create_profile_html(name: str, age: int, location: str) -> str:
    safe_name = html.escape(name)
    safe_location = html.escape(location)
    return f"""
    <html>
        <body>
            <h1>{safe_name}</h1>
            <p>Age: {age}</p>
            <p>Location: {safe_location}</p>
        </body>
    </html>
    """